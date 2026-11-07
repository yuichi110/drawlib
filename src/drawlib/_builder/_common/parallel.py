# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Multi-process parallel diagram rendering pool and job scheduler for drawlib builders."""

from __future__ import annotations

import multiprocessing as mp
import os
import re
import sys
import tempfile
import threading
import warnings
from collections.abc import Sequence
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Final, Literal

from drawlib._builder._common.cache import BuildImageCache, hash_file
from drawlib._builder._common.manifest import find_project_manifest
from drawlib._builder._common.progress import BAR_WIDTH
from drawlib._builder._common.styles_loader import load_styles_and_utils
from drawlib._core.l1_core import drawlib_settings

WorkersSpec = int | Literal["auto"]
LoggingMode = Literal["normal", "quiet", "verbose", "debug", "developer"]

DEFAULT_AUTO_MAX_WORKERS: Final[int] = 8
ENV_BUILD_WORKERS: Final[str] = "DRAWLIB_BUILD_WORKERS"

_MD_DRAWLIB_RE: Final[re.Pattern[str]] = re.compile(
    r"(?<=\n)[ \t]*```drawlib([^\n]*)\n(.*?)\n[ \t]*```",
    re.DOTALL,
)
_HTML_DRAWLIB_RE: Final[re.Pattern[str]] = re.compile(
    r"""<script\b([^>]*)type=["']text/drawlib["']([^>]*)>(.*?)</script>""",
    re.DOTALL | re.IGNORECASE,
)


def _auto_worker_count() -> int:
    """Compute default auto worker count satisfying `1 <= (cpu_count - 1) <= 8`."""
    cpu_total = os.cpu_count() or 1
    return max(1, min(cpu_total - 1, DEFAULT_AUTO_MAX_WORKERS))


def _parse_positive_worker_int(raw: str | int) -> int:
    """Parse a positive integer worker count or raise ValueError."""
    if isinstance(raw, bool):
        raise ValueError("workers must be 'auto' or a positive integer >= 1.")
    try:
        val = int(raw)
    except (TypeError, ValueError) as e:
        raise ValueError("workers must be 'auto' or a positive integer >= 1.") from e
    if val < 1:
        raise ValueError("workers must be 'auto' or a positive integer >= 1.")
    return val


def resolve_build_workers(workers: int | str | None = "auto") -> int:
    """Resolve effective parallel worker count from argument, environment variable, or CPU cores.

    Priority:
    1. Explicit `workers` argument when not `'auto'` / `None`.
    2. `DRAWLIB_BUILD_WORKERS` environment variable when set.
    3. Auto formula: `max(1, min((os.cpu_count() or 1) - 1, 8))`.

    Args:
        workers: `'auto'`, positive integer `>= 1`, or string representation thereof.

    Returns:
        int: Resolved worker count (`>= 1`).

    Raises:
        ValueError: If `workers` or `DRAWLIB_BUILD_WORKERS` has an invalid value.
    """
    if isinstance(workers, bool):
        raise ValueError("workers must be 'auto' or a positive integer >= 1.")

    if isinstance(workers, int):
        return _parse_positive_worker_int(workers)

    spec_str = "auto" if workers is None else str(workers).strip()
    if not spec_str:
        raise ValueError("workers must be 'auto' or a positive integer >= 1.")

    if spec_str.lower() == "auto":
        env_raw = os.environ.get(ENV_BUILD_WORKERS, "").strip()
        if env_raw and env_raw.lower() != "auto":
            return _parse_positive_worker_int(env_raw)
        return _auto_worker_count()

    return _parse_positive_worker_int(spec_str)


def compute_processor_config_hash(
    styles_path: str | None,
    utils_path: str | None,
    extra_config_hash: str = "",
) -> str:
    """Compute the exact `config_hash` used by `DrawlibBlockProcessor`."""
    s_hash = hash_file(styles_path) if styles_path else ""
    u_hash = hash_file(utils_path) if utils_path else ""
    parts = [s_hash, u_hash]
    if extra_config_hash:
        parts.append(extra_config_hash)
    return ":".join(parts)


def resolve_processor_project_root(
    project_root: str | None,
    styles_path: str | None,
    utils_path: str | None,
) -> str | None:
    """Resolve `project_root` identically to `DrawlibBlockProcessor.__init__`."""
    if project_root:
        return os.path.abspath(project_root)
    cand_cfg = styles_path or utils_path
    if cand_cfg:
        found = find_project_manifest(cand_cfg, max_up=3)
        if found is not None:
            return found[0]
    if styles_path and os.path.isfile(styles_path):
        return os.path.dirname(os.path.abspath(styles_path))
    if utils_path and os.path.isfile(utils_path):
        return os.path.dirname(os.path.abspath(utils_path))
    return None


@dataclass(frozen=True)
class BlockRenderJob:
    """Serializable specification for rendering a single embedded drawlib code block."""

    job_id: str
    code: str
    source_filename: str
    working_dir: str
    line_number: int
    target_abs_path: str | None
    cache_target_file: str
    image_format: str
    dpi: int | None
    styles_path: str | None
    utils_path: str | None
    project_root: str | None
    slide_ctx: tuple[int, int] | None
    static_anim_frame: Literal["first", "last"] | None
    cache_key: str
    code_hash: str
    config_hash: str
    prerender_key: str
    read_cache: bool
    write_cache: bool
    logging_mode: LoggingMode


@dataclass(frozen=True)
class BlockRenderResult:
    """Serialized rendering output returned from a worker process to the parent process."""

    job_id: str
    normal_bytes: bytes
    grid_bytes: bytes | None


@dataclass(frozen=True)
class ScriptSavedFile:
    """Single output image written during standalone Python script execution."""

    resolved_abs: str
    normal_bytes: bytes | None
    grid_bytes: bytes | None


@dataclass(frozen=True)
class ScriptRenderJob:
    """Serializable specification for executing a standalone `.py` drawing script in a worker."""

    job_index: int
    file_path: str
    disp_name: str
    code_len: int
    has_anim: bool
    mode: Literal["auto_clear", "auto_initialize"]
    styles_path: str | None
    utils_path: str | None
    output_dir: str | None
    output_file: str | None
    image_format: Literal["png", "webp", "gif", "jpg", "pdf"] | None
    grid: bool
    force_grid: bool
    target_roots: tuple[str, ...]
    current_target_root: str
    cache_info: tuple[str, str, str, str] | None
    logging_mode: LoggingMode


@dataclass(frozen=True)
class ScriptRenderResult:
    """Result returned after executing a standalone `.py` drawing script in a worker."""

    job_index: int
    file_path: str
    disp_name: str
    saved_files: tuple[ScriptSavedFile, ...]
    cache_info: tuple[str, str, str, str] | None


class ParallelRenderProgress:
    """Terminal progress reporter for multi-worker diagram rendering."""

    def __init__(self, total_jobs: int, workers: int) -> None:
        """Initialize progress state for `total_jobs` across `workers`."""
        self.total_jobs = total_jobs
        self.workers = workers
        self._quiet = drawlib_settings.get_logging_mode() == "quiet"
        self._is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def update(self, completed: int) -> None:
        """Emit progress bar update to stdout."""
        if self._quiet or self.total_jobs <= 0:
            return

        done = completed >= self.total_jobs
        if done:
            bar = "#" * BAR_WIDTH
            pct = 100
        else:
            ratio = max(0.0, min(1.0, completed / self.total_jobs))
            pct = min(99, int(round(ratio * 100)))
            filled = min(BAR_WIDTH - 1, int(BAR_WIDTH * ratio))
            bar = ("#" * filled) + "." + (" " * (BAR_WIDTH - filled - 1))

        w_digit = len(str(self.total_jobs))
        line = (
            f"render ({self.workers} workers) "
            f"images:{completed:>{w_digit}}/{self.total_jobs:>{w_digit}} : {bar} {pct:>3d}%"
        )
        if self._is_tty:
            end_char = "\n" if done else ""
            sys.stdout.write(f"\r{line}{end_char}")
            sys.stdout.flush()
        elif done:
            print(line, flush=True)


def _evict_worker_project_utils(project_root: str | None, active_utils: str | None) -> None:
    """Evict cached top-level `utils` module if loaded from another path under `project_root`."""
    if not project_root:
        return
    mod = sys.modules.get("utils")
    if mod is None:
        return
    mod_file = getattr(mod, "__file__", None)
    if not mod_file:
        return
    mod_abs = os.path.abspath(mod_file)
    root_abs = os.path.abspath(project_root)
    if mod_abs.startswith(root_abs + os.sep) and (active_utils is None or mod_abs != os.path.abspath(active_utils)):
        sys.modules.pop("utils", None)


def _format_worker_exception(exc: Exception, source_filename: str, line_number: int | None = None) -> Exception:
    """Convert worker exceptions into guaranteed-picklable built-in exception instances."""
    loc = f"{source_filename}:{line_number}" if line_number else source_filename
    msg = f"{exc} (in {loc})"
    if isinstance(exc, FileNotFoundError):
        return FileNotFoundError(msg)
    if isinstance(exc, ValueError):
        return ValueError(msg)
    return RuntimeError(f"{type(exc).__name__} in {loc}: {exc}")


def _infer_format_from_path(path_or_ext: str) -> str:
    """Map target file extension or format name to DrawlibBlockProcessor canonical format."""
    ext_lower = os.path.splitext(path_or_ext)[1].lower()
    if not ext_lower:
        ext_lower = f".{path_or_ext.lower().lstrip('.')}"
    if ext_lower == ".svg":
        return "svg"
    if ext_lower == ".webp":
        return "webp"
    if ext_lower == ".apng":
        return "apng"
    if ext_lower == ".gif":
        return "gif"
    return "png"


def build_block_render_job(
    *,
    code: str,
    source_filename: str,
    working_dir: str,
    line_number: int,
    target_abs_path: str | None,
    cache_target_file: str,
    image_format: str,
    dpi: int | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    project_root: str | None = None,
    extra_config_hash: str = "",
    extra_cache_salt: str = "",
    slide_ctx: tuple[int, int] | None = None,
    static_anim_frame: Literal["first", "last"] | None = None,
    no_cache_global: bool = False,
    no_cache_block: bool = False,
) -> BlockRenderJob:
    """Construct a `BlockRenderJob` with cache/prerender keys matching `DrawlibBlockProcessor`."""
    fmt = _infer_format_from_path(f"x.{image_format}")
    config_hash = compute_processor_config_hash(styles_path, utils_path, extra_config_hash)
    eff_project_root = resolve_processor_project_root(project_root, styles_path, utils_path)

    source_abs = os.path.abspath(source_filename)
    context_dir = os.path.dirname(source_abs) if os.path.exists(source_abs) else os.path.abspath(working_dir)
    if os.path.isabs(cache_target_file):
        eff_cache_target = os.path.abspath(cache_target_file)
    else:
        eff_cache_target = os.path.abspath(os.path.join(context_dir, cache_target_file))

    eff_salt = f"{extra_cache_salt}:svg-fonts-v1" if fmt == "svg" else extra_cache_salt
    if dpi is not None and dpi != 100:
        eff_salt = f"{eff_salt}:dpi={dpi}" if eff_salt else f"dpi={dpi}"

    use_cache = (not no_cache_global) and (not no_cache_block)
    cache_key, code_hash = BuildImageCache.compute_keys(
        code=code,
        config_hash=config_hash,
        context_dir=context_dir,
        project_root=eff_project_root,
        source_file=source_abs,
        target_file=eff_cache_target,
        extra_salt=eff_salt,
    )
    prerender_key = BuildImageCache.compute_prerender_key(
        code=code,
        config_hash=config_hash,
        source_file=source_abs,
        target_file=eff_cache_target,
        image_format=fmt,
        dpi=dpi,
        extra_salt=extra_cache_salt,
    )
    resolved_target_abs = os.path.abspath(target_abs_path) if target_abs_path is not None else None
    job_id = resolved_target_abs if resolved_target_abs is not None else f"inline:{prerender_key}"

    return BlockRenderJob(
        job_id=job_id,
        code=code,
        source_filename=source_abs,
        working_dir=os.path.abspath(working_dir),
        line_number=line_number,
        target_abs_path=resolved_target_abs,
        cache_target_file=eff_cache_target,
        image_format=fmt,
        dpi=dpi,
        styles_path=os.path.abspath(styles_path) if styles_path else None,
        utils_path=os.path.abspath(utils_path) if utils_path else None,
        project_root=eff_project_root,
        slide_ctx=slide_ctx,
        static_anim_frame=static_anim_frame,
        cache_key=cache_key,
        code_hash=code_hash,
        config_hash=config_hash,
        prerender_key=prerender_key,
        read_cache=use_cache,
        write_cache=use_cache,
        logging_mode=drawlib_settings.get_logging_mode(),
    )


def _execute_block_render_job(job: BlockRenderJob) -> BlockRenderResult:
    """Worker process entrypoint that renders a single `BlockRenderJob` identically to `DrawlibBlockProcessor`."""
    import drawlib._core.l4_canvas  # noqa: PLC0415
    from drawlib._builder.doc_builder.processor.processor import DrawlibBlockProcessor  # noqa: PLC0415
    from drawlib._core.l4_canvas import save  # noqa: PLC0415
    from drawlib._core.l4_canvas._base import CanvasBase  # noqa: PLC0415
    from drawlib._slide.base import reset_slide_context, set_slide_context  # noqa: PLC0415

    drawlib_settings.set_logging_mode(job.logging_mode)

    orig_cwd = os.getcwd()
    sys_path_added = False
    ctx_token = None
    orig_default_dpi = CanvasBase.DEFAULT_DPI

    try:
        os.chdir(job.working_dir)
        if job.working_dir not in sys.path:
            sys.path.insert(0, job.working_dir)
            sys_path_added = True

        _evict_worker_project_utils(job.project_root, job.utils_path)
        shared_globals: dict[str, Any] = {}
        load_styles_and_utils(
            styles_path=job.styles_path,
            utils_path=job.utils_path,
            shared_globals=shared_globals,
        )

        if job.slide_ctx is not None:
            ctx_token = set_slide_context(index=job.slide_ctx[0], total=job.slide_ctx[1])
        if job.dpi is not None:
            setattr(CanvasBase, "DEFAULT_DPI", int(job.dpi))

        DrawlibBlockProcessor._exec_code_block(
            job.code,
            source_filename=job.source_filename,
            shared_globals=shared_globals,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_out = os.path.join(tmp_dir, f"render.{job.image_format}")
            tmp_grid = os.path.join(tmp_dir, f"render_grid.{job.image_format}")
            with warnings.catch_warnings():
                if job.logging_mode not in {"verbose", "developer"}:
                    warnings.filterwarnings("ignore", message=r"Glyph .* missing from font", category=UserWarning)
                save(tmp_out)

            with open(tmp_out, "rb") as f_norm:
                unflattened_bytes = f_norm.read()
            grid_bytes: bytes | None = None
            if os.path.isfile(tmp_grid):
                with open(tmp_grid, "rb") as f_grid:
                    grid_bytes = f_grid.read()

            if job.target_abs_path is not None:
                dest_dir = os.path.dirname(job.target_abs_path)
                os.makedirs(dest_dir, exist_ok=True)
                atomic_tmp = os.path.join(
                    dest_dir,
                    f".tmp_{os.getpid()}_{threading.get_ident()}_{os.path.basename(job.target_abs_path)}",
                )
                try:
                    with open(atomic_tmp, "wb") as f_dst:
                        f_dst.write(unflattened_bytes)
                    if job.static_anim_frame is not None:
                        from drawlib._slide.compiler import _flatten_slide_animation_in_place  # noqa: PLC0415

                        _flatten_slide_animation_in_place(atomic_tmp, job.static_anim_frame)
                    os.replace(atomic_tmp, job.target_abs_path)
                except BaseException:
                    if os.path.exists(atomic_tmp):
                        os.unlink(atomic_tmp)
                    raise

                if grid_bytes is not None:
                    t_stem, t_ext = os.path.splitext(job.target_abs_path)
                    grid_dest = f"{t_stem}_grid{t_ext}"
                    grid_atomic = os.path.join(
                        dest_dir,
                        f".tmp_{os.getpid()}_{threading.get_ident()}_{os.path.basename(grid_dest)}",
                    )
                    try:
                        with open(grid_atomic, "wb") as fg_dst:
                            fg_dst.write(grid_bytes)
                        os.replace(grid_atomic, grid_dest)
                    except BaseException:
                        if os.path.exists(grid_atomic):
                            os.unlink(grid_atomic)
                        raise

            drawlib._core.l4_canvas.clear()
            return BlockRenderResult(
                job_id=job.job_id,
                normal_bytes=unflattened_bytes,
                grid_bytes=grid_bytes,
            )
    except Exception as exc:
        raise _format_worker_exception(exc, job.source_filename, job.line_number) from None
    finally:
        if job.dpi is not None:
            setattr(CanvasBase, "DEFAULT_DPI", orig_default_dpi)
        if ctx_token is not None:
            reset_slide_context(ctx_token)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if os.path.isdir(orig_cwd):
                os.chdir(orig_cwd)
        if sys_path_added and job.working_dir in sys.path:
            sys.path.remove(job.working_dir)


def _job_priority_key(job: BlockRenderJob) -> tuple[bool, bool, int]:
    """Longest-Job-First priority key (Animations first, multi-frame formats next, larger code first)."""
    has_anim = "Animation(" in job.code
    is_anim_fmt = job.image_format in {"webp", "gif", "apng"}
    return (has_anim, is_anim_fmt, len(job.code))


def prerender_document_blocks(
    jobs: Sequence[BlockRenderJob],
    *,
    cache: BuildImageCache,
    workers: int | str | None = "auto",
) -> int:
    """Pre-render uncached `BlockRenderJob` items across a multi-process worker pool.

    When `effective_workers <= 1` or cache misses are `<= 1`, returns `0` immediately
    without spawning child processes so the caller's sequential compiler handles them
    in-process with zero multiprocessing startup overhead.

    Args:
        jobs: Candidate `BlockRenderJob` items in document encounter order.
        cache: Active `BuildImageCache` shared with the downstream compiler.
        workers: `'auto'` or positive integer worker count.

    Returns:
        int: Number of blocks rendered in the parallel worker pool (`0` if skipped).
    """
    effective_workers = resolve_build_workers(workers)
    if effective_workers <= 1 or len(jobs) <= 1:
        return 0

    unique_jobs: list[BlockRenderJob] = []
    seen_job_ids: set[str] = set()
    for job in jobs:
        if job.job_id in seen_job_ids:
            continue
        seen_job_ids.add(job.job_id)
        unique_jobs.append(job)

    if len(unique_jobs) <= 1:
        return 0

    miss_jobs: list[BlockRenderJob] = []
    hit_jobs_to_materialize: list[tuple[BlockRenderJob, bytes, bytes | None]] = []

    for job in unique_jobs:
        if job.target_abs_path is not None and (
            job.target_abs_path in cache.rendered_targets and os.path.isfile(job.target_abs_path)
        ):
            continue

        if cache.enabled and job.read_cache:
            cached = cache.get(job.cache_key, image_format=job.image_format)
            if cached is not None:
                hit_jobs_to_materialize.append((job, cached[0], cached[1]))
                continue

        miss_jobs.append(job)

    # Materialize already-cached files/blobs so Phase 3 skips duplicate SQLite lookups
    for hit_job, norm_bytes, grid_bytes in hit_jobs_to_materialize:
        if hit_job.target_abs_path is not None:
            os.makedirs(os.path.dirname(hit_job.target_abs_path), exist_ok=True)
            with open(hit_job.target_abs_path, "wb") as f_out:
                f_out.write(norm_bytes)
            if hit_job.static_anim_frame is not None:
                from drawlib._slide.compiler import _flatten_slide_animation_in_place  # noqa: PLC0415

                _flatten_slide_animation_in_place(hit_job.target_abs_path, hit_job.static_anim_frame)
            if grid_bytes is not None:
                t_stem, t_ext = os.path.splitext(hit_job.target_abs_path)
                with open(f"{t_stem}_grid{t_ext}", "wb") as f_grid:
                    f_grid.write(grid_bytes)
            cache.rendered_targets.add(hit_job.target_abs_path)
        elif hit_job.static_anim_frame is None:
            cache.prerendered_blobs[hit_job.prerender_key] = (norm_bytes, grid_bytes)

    if len(miss_jobs) <= 1:
        return 0

    scheduled_jobs = sorted(miss_jobs, key=_job_priority_key, reverse=True)
    actual_workers = min(effective_workers, len(scheduled_jobs))
    progress = ParallelRenderProgress(total_jobs=len(scheduled_jobs), workers=actual_workers)
    progress.update(0)

    mp_ctx = mp.get_context("spawn")
    executor = ProcessPoolExecutor(max_workers=actual_workers, mp_context=mp_ctx)
    completed_count = 0
    try:
        future_to_job: dict[Future[BlockRenderResult], BlockRenderJob] = {
            executor.submit(_execute_block_render_job, job): job for job in scheduled_jobs
        }
        for fut in as_completed(future_to_job):
            job = future_to_job[fut]
            res = fut.result()
            if cache.enabled and job.write_cache:
                cache.put(
                    cache_key=job.cache_key,
                    code_hash=job.code_hash,
                    config_hash=job.config_hash,
                    image_format=job.image_format,
                    image_blob=res.normal_bytes,
                    grid_blob=res.grid_bytes,
                )
            if job.target_abs_path is not None:
                cache.rendered_targets.add(job.target_abs_path)
            elif not (cache.enabled and job.write_cache):
                cache.prerendered_blobs[job.prerender_key] = (res.normal_bytes, res.grid_bytes)

            completed_count += 1
            progress.update(completed_count)
    except BaseException:
        executor.shutdown(wait=False, cancel_futures=True)
        raise
    else:
        executor.shutdown(wait=True)

    return completed_count


def collect_standard_document_block_jobs(
    *,
    src_abs: str,
    dest_abs: str | None,
    is_md: bool,
    image_format: str,
    embed_images: bool,
    styles_path: str | None,
    utils_path: str | None,
    project_root: str | None,
    shared_images_dir: str | None = None,
    require_file: bool = True,
    no_cache_global: bool = False,
) -> list[BlockRenderJob]:
    """Extract `BlockRenderJob` items from a Markdown or HTML source file matching `DrawlibBlockProcessor`."""
    from drawlib._builder.doc_builder.detector import preserve_outer_fences  # noqa: PLC0415
    from drawlib._builder.doc_builder.processor.options import (  # noqa: PLC0415
        parse_block_info,
        resolve_block_image_paths,
    )

    try:
        with open(src_abs, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return []

    src_dir = os.path.dirname(os.path.abspath(src_abs))
    if embed_images or dest_abs is None:
        output_dir: str | None = None
        doc_base_name = os.path.splitext(os.path.basename(src_abs))[0]
    else:
        output_dir = os.path.dirname(os.path.abspath(dest_abs))
        doc_base_name = os.path.splitext(os.path.basename(dest_abs))[0]

    jobs: list[BlockRenderJob] = []
    if is_md:
        masked_text, _ = preserve_outer_fences(content)
        text_to_search = "\n" + masked_text if not masked_text.startswith("\n") else masked_text
        for counter, match in enumerate(_MD_DRAWLIB_RE.finditer(text_to_search), start=1):
            info_str = match.group(1).strip()
            code = match.group(2).strip()
            options = parse_block_info(info_str)
            line_no = text_to_search[: match.start()].count("\n") + 1
            _, target_img_path = resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=counter,
                default_format=image_format,
                output_dir=output_dir,
                require_file=require_file,
                line_number=line_no,
                shared_images_dir=shared_images_dir,
            )
            if embed_images:
                eff_fmt = _infer_format_from_path(f"x.{image_format}")
                target_abs_out: str | None = None
            else:
                eff_fmt = _infer_format_from_path(target_img_path)
                target_abs_out = (
                    os.path.abspath(target_img_path)
                    if os.path.isabs(target_img_path)
                    else os.path.abspath(os.path.join(src_dir, target_img_path))
                )
            jobs.append(
                build_block_render_job(
                    code=code,
                    source_filename=src_abs,
                    working_dir=src_dir,
                    line_number=line_no,
                    target_abs_path=target_abs_out,
                    cache_target_file=target_img_path,
                    image_format=eff_fmt,
                    styles_path=styles_path,
                    utils_path=utils_path,
                    project_root=project_root,
                    no_cache_global=no_cache_global,
                    no_cache_block=options.no_cache,
                )
            )
    else:
        for counter, match in enumerate(_HTML_DRAWLIB_RE.finditer(content), start=1):
            info_str = (match.group(1) + " " + match.group(2)).strip()
            code = match.group(3).strip()
            options = parse_block_info(info_str)
            line_no = content[: match.start()].count("\n") + 1
            _, target_img_path = resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=counter,
                default_format=image_format,
                output_dir=output_dir,
                require_file=require_file,
                line_number=line_no,
                shared_images_dir=shared_images_dir,
            )
            if embed_images:
                eff_fmt = _infer_format_from_path(f"x.{image_format}")
                target_abs_out = None
            else:
                eff_fmt = _infer_format_from_path(target_img_path)
                target_abs_out = (
                    os.path.abspath(target_img_path)
                    if os.path.isabs(target_img_path)
                    else os.path.abspath(os.path.join(src_dir, target_img_path))
                )
            jobs.append(
                build_block_render_job(
                    code=code,
                    source_filename=src_abs,
                    working_dir=src_dir,
                    line_number=line_no,
                    target_abs_path=target_abs_out,
                    cache_target_file=target_img_path,
                    image_format=eff_fmt,
                    styles_path=styles_path,
                    utils_path=utils_path,
                    project_root=project_root,
                    no_cache_global=no_cache_global,
                    no_cache_block=options.no_cache,
                )
            )

    return jobs


def collect_docx_chapter_block_jobs(
    *,
    src_abs: str,
    markdown_text: str,
    dpi: int,
    styles_path: str | None,
    utils_path: str | None,
    project_root: str | None,
    no_cache_global: bool = False,
) -> list[BlockRenderJob]:
    """Extract `BlockRenderJob` items from a Markdown chapter matching `_DocxChapterRenderer`."""
    from markdown_it import MarkdownIt  # noqa: PLC0415

    from drawlib._builder.doc_builder.processor.options import (  # noqa: PLC0415
        parse_block_info,
        resolve_block_image_paths,
    )

    md_parser = MarkdownIt("gfm-like", {"html": True, "linkify": False, "typographer": True})
    tokens = md_parser.parse(markdown_text)

    src_dir = os.path.dirname(os.path.abspath(src_abs))
    doc_base_name = os.path.splitext(os.path.basename(src_abs))[0]
    drawlib_counter = 0
    jobs: list[BlockRenderJob] = []

    for tok in tokens:
        if tok.type != "fence":
            continue
        stripped = tok.info.strip()
        if not stripped or stripped.split()[0] != "drawlib":
            continue

        drawlib_counter += 1
        info_rest = stripped[len("drawlib") :].strip()
        options = parse_block_info(info_rest)
        line_no = (tok.map[0] + 1) if tok.map else 1

        _, canonical_target = resolve_block_image_paths(
            options=options,
            doc_base_name=doc_base_name,
            block_counter=drawlib_counter,
            default_format="png",
            output_dir=None,
            require_file=True,
            line_number=line_no,
        )
        cand_ext = os.path.splitext(canonical_target)[1].lower()
        render_ext = cand_ext if cand_ext in {".png", ".webp", ".apng", ".gif"} else ".png"

        jobs.append(
            build_block_render_job(
                code=tok.content.strip(),
                source_filename=src_abs,
                working_dir=src_dir,
                line_number=line_no,
                target_abs_path=None,
                cache_target_file=canonical_target,
                image_format=render_ext.lstrip("."),
                dpi=dpi,
                styles_path=styles_path,
                utils_path=utils_path,
                project_root=project_root,
                no_cache_global=no_cache_global,
                no_cache_block=options.no_cache,
            )
        )

    return jobs


def _execute_script_render_job(job: ScriptRenderJob) -> ScriptRenderResult:
    """Worker process entrypoint executing a single standalone Python script via `DrawlibExecuter`."""
    import contextlib  # noqa: PLC0415
    import io  # noqa: PLC0415

    import drawlib._core.l4_canvas  # noqa: PLC0415
    import drawlib.canvas  # noqa: PLC0415
    from drawlib._builder.image_builder import DrawlibExecuter  # noqa: PLC0415

    suppress_stdout = job.logging_mode not in {"verbose", "debug", "developer"}
    drawlib_settings.set_logging_mode("quiet" if suppress_stdout else job.logging_mode)
    stdout_ctx = contextlib.redirect_stdout(io.StringIO()) if suppress_stdout else contextlib.nullcontext()

    with stdout_ctx:
        executer = DrawlibExecuter(
            mode=job.mode,
            styles_path=job.styles_path,
            utils_path=job.utils_path,
            output_dir=job.output_dir,
            output_file=job.output_file,
            image_format=job.image_format,
            grid=job.grid,
            no_cache=True,
            target_roots=job.target_roots,
        )
        executer._current_target_root = job.current_target_root
        executer._current_source_label = job.disp_name
        executer._add_topdir_to_syspath(
            job.current_target_root if os.path.isdir(job.current_target_root) else job.file_path
        )

    eff_out = executer._get_effective_output_dir(job.file_path)
    if eff_out is not None:
        drawlib_settings.set_output_dir(eff_out)
        os.makedirs(eff_out, exist_ok=True)
    elif job.output_dir is not None:
        drawlib_settings.set_output_dir(os.path.abspath(job.output_dir))

    if job.grid or job.force_grid:
        drawlib_settings.set_force_grid(True)

    canvas_inst = drawlib._core.l4_canvas.canvas
    orig_canvas_save = canvas_inst.save
    orig_core_save = drawlib._core.l4_canvas.save
    orig_canvas_mod_save = getattr(drawlib.canvas, "save", None)
    saved_records: list[ScriptSavedFile] = []

    def _worker_save(
        file: str | None = None,
        format: Literal["png", "webp", "gif", "jpg", "pdf"] | None = None,
    ) -> None:
        eff_format: Literal["png", "webp", "gif", "jpg", "pdf"] | None = (
            job.image_format if job.image_format else format
        )
        if job.output_file is not None:
            target = os.path.abspath(job.output_file)
            if eff_format:
                stem, _ = os.path.splitext(target)
                target = f"{stem}.{eff_format}"
            eff_file: str | None = target
        elif file is not None and eff_format:
            stem, _ = os.path.splitext(file)
            eff_file = f"{stem}.{eff_format}"
        else:
            eff_file = file

        resolved_abs = os.path.abspath(canvas_inst._get_save_file_path(eff_file, eff_format))
        if resolved_abs in executer._runtime_seen_outputs:
            from drawlib._builder._common.progress import format_duplicate_output_error  # noqa: PLC0415

            raise ValueError(
                format_duplicate_output_error(
                    resolved_abs,
                    executer._runtime_seen_outputs[resolved_abs],
                    job.disp_name,
                )
            )
        executer._runtime_seen_outputs[resolved_abs] = job.disp_name
        orig_canvas_save(file=eff_file, format=eff_format)

        norm_bytes: bytes | None = None
        grid_bytes: bytes | None = None
        if job.cache_info is not None and os.path.isfile(resolved_abs):
            base_stem, ext_dot = os.path.splitext(resolved_abs)
            grid_candidate = f"{base_stem}_grid{ext_dot}"
            with open(resolved_abs, "rb") as f_img:
                norm_bytes = f_img.read()
            if os.path.isfile(grid_candidate):
                with open(grid_candidate, "rb") as f_grid:
                    grid_bytes = f_grid.read()

        saved_records.append(
            ScriptSavedFile(
                resolved_abs=resolved_abs,
                normal_bytes=norm_bytes,
                grid_bytes=grid_bytes,
            )
        )

    try:
        setattr(canvas_inst, "save", _worker_save)
        drawlib._core.l4_canvas.save = _worker_save  # ty: ignore
        drawlib.canvas.save = _worker_save  # ty: ignore

        executer._current_cache_info = job.cache_info
        with contextlib.redirect_stdout(io.StringIO()) if suppress_stdout else contextlib.nullcontext():
            executer._exec_module(job.file_path)
        drawlib._core.l4_canvas.clear()
        return ScriptRenderResult(
            job_index=job.job_index,
            file_path=job.file_path,
            disp_name=job.disp_name,
            saved_files=tuple(saved_records),
            cache_info=job.cache_info,
        )
    except Exception as exc:
        raise _format_worker_exception(exc, job.file_path) from None
    finally:
        setattr(canvas_inst, "save", orig_canvas_save)
        drawlib._core.l4_canvas.save = orig_core_save  # type: ignore[assignment]
        if orig_canvas_mod_save is not None:
            drawlib.canvas.save = orig_canvas_mod_save  # type: ignore[assignment]
        if job.grid or job.force_grid:
            drawlib_settings.set_force_grid(False)
        drawlib_settings.set_output_dir(None)


def execute_scripts_parallel(
    jobs: Sequence[ScriptRenderJob],
    *,
    workers: int,
) -> list[ScriptRenderResult]:
    """Execute standalone `.py` `ScriptRenderJob` items across `workers` child processes."""
    scheduled = sorted(jobs, key=lambda j: (j.has_anim, j.code_len), reverse=True)
    actual_workers = min(workers, len(scheduled))
    progress = ParallelRenderProgress(total_jobs=len(scheduled), workers=actual_workers)
    progress.update(0)

    mp_ctx = mp.get_context("spawn")
    executor = ProcessPoolExecutor(max_workers=actual_workers, mp_context=mp_ctx)
    results_by_idx: dict[int, ScriptRenderResult] = {}
    completed_count = 0
    try:
        future_to_job: dict[Future[ScriptRenderResult], ScriptRenderJob] = {
            executor.submit(_execute_script_render_job, job): job for job in scheduled
        }
        for fut in as_completed(future_to_job):
            res = fut.result()
            results_by_idx[res.job_index] = res
            completed_count += 1
            progress.update(completed_count)
    except BaseException:
        executor.shutdown(wait=False, cancel_futures=True)
        raise
    else:
        executor.shutdown(wait=True)

    return [results_by_idx[j.job_index] for j in jobs]


__all__ = [
    "DEFAULT_AUTO_MAX_WORKERS",
    "ENV_BUILD_WORKERS",
    "BlockRenderJob",
    "BlockRenderResult",
    "ParallelRenderProgress",
    "ScriptRenderJob",
    "ScriptRenderResult",
    "ScriptSavedFile",
    "WorkersSpec",
    "build_block_render_job",
    "collect_docx_chapter_block_jobs",
    "collect_standard_document_block_jobs",
    "compute_processor_config_hash",
    "execute_scripts_parallel",
    "prerender_document_blocks",
    "resolve_build_workers",
    "resolve_processor_project_root",
]
