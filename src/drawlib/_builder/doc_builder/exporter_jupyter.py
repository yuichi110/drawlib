# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Jupyter Notebook (.ipynb nbformat v4.5) exporter, HTML cell renderer, and in-process Dry-Run engine."""

from __future__ import annotations

import ast
import base64
import contextlib
import html
import io
import json
import os
import re
import sys
import traceback
import warnings
from dataclasses import dataclass, field
from typing import Any, Literal

from matplotlib import pyplot

import drawlib._core.l4_canvas
import drawlib.canvas
from drawlib._builder._common import (
    JupyterCellMode,
    JupyterImageMode,
    load_styles_and_utils,
)
from drawlib._builder.doc_builder.detector import (
    preserve_outer_fences,
    restore_outer_fences,
)
from drawlib._builder.doc_builder.highlight import pygments_highlight
from drawlib._builder.doc_builder.parser_md import parse_markdown_to_html
from drawlib._builder.doc_builder.processor.options import (
    DrawlibBlockOptions,
    parse_block_info,
    resolve_block_image_paths,
    tokenize_kv_pairs,
)
from drawlib._core.l1_core import drawlib_settings
from drawlib._core.l3_images import Dimage

_FENCE_OPEN_RE = re.compile(r"^[ \t]{0,3}(`{3}|~{3})([^\n\r]*)$")
_MAGIC_LINE_RE = re.compile(r"^([ \t]*)[!%](.*)$")
_CANVAS_IMPORT_RE = re.compile(r"^([ \t]*from\s+drawlib\.canvas\s+import\s+)(.+)$", re.MULTILINE)
_CANVAS_SAVE_CALL_RE = re.compile(r"\bcanvas\.save\s*\([^()]*\)")
_STANDALONE_SAVE_CALL_RE = re.compile(r"(?<![.\w])save\s*\([^()]*\)")


class NotebookExecutionError(RuntimeError):
    """Raised when a notebook code cell fails during sequential in-process Dry-Run execution."""

    def __init__(
        self,
        message: str,
        *,
        source_path: str,
        cell_index: int,
        cell_line: int,
        markdown_line: int,
        code: str,
        cause: BaseException | None = None,
    ) -> None:
        """Initialize NotebookExecutionError with full source location metadata."""
        super().__init__(message)
        self.source_path = source_path
        self.cell_index = cell_index
        self.cell_line = cell_line
        self.markdown_line = markdown_line
        self.code = code
        self.cause = cause


@dataclass
class NotebookSegment:
    """Single parsed segment (Markdown prose, Drawlib diagram, or Python code cell) in a notebook."""

    kind: Literal["markdown", "drawlib", "code"]
    source: str
    line_number: int
    cell_mode: JupyterCellMode = "markdown"
    drawlib_options: DrawlibBlockOptions | None = None
    block_index: int = 0
    rel_img_path: str = ""
    target_img_path: str = ""
    is_setup_cell: bool = False


@dataclass
class CellExecutionOutput:
    """Captured execution outputs for a single notebook code cell."""

    execution_count: int
    stdout: str = ""
    result_repr: str | None = None
    figures: list[bytes] = field(default_factory=list)
    figure_rel_paths: list[str] = field(default_factory=list)
    geometry_warnings: list[str] = field(default_factory=list)


@dataclass
class NotebookExecutionResult:
    """Aggregated result of executing all code cells in a notebook."""

    source_path: str
    cell_outputs: dict[int, CellExecutionOutput] = field(default_factory=dict)
    geometry_warnings: list[str] = field(default_factory=list)
    executed_cell_count: int = 0


def convert_save_to_show(code: str) -> str:
    """Convert ``save(...)`` imports and calls into ``show()`` for interactive notebook cells.

    Args:
        code: Python source code inside a ``drawlib`` block.

    Returns:
        str: Transformed Python source code using ``show()``.
    """

    def _replace_import(match: re.Match[str]) -> str:
        prefix = match.group(1)
        imports_raw = match.group(2)
        comment = ""
        if "#" in imports_raw:
            imports_raw, comment_part = imports_raw.split("#", 1)
            comment = f"  # {comment_part.strip()}"
        names = [tok.strip() for tok in imports_raw.split(",") if tok.strip()]
        new_names: list[str] = []
        for name in names:
            replacement = "show" if name == "save" else name
            if replacement not in new_names:
                new_names.append(replacement)
        return f"{prefix}{', '.join(new_names)}{comment}"

    updated = _CANVAS_IMPORT_RE.sub(_replace_import, code)
    updated = _CANVAS_SAVE_CALL_RE.sub("canvas.show()", updated)
    updated = _STANDALONE_SAVE_CALL_RE.sub("show()", updated)
    return updated


def _parse_python_fence_cell_mode(info_after_lang: str) -> JupyterCellMode:
    """Parse optional ``cell=markdown|code`` attribute on a ```` ```python ```` code fence."""
    for key_lower, val_clean in tokenize_kv_pairs(info_after_lang):
        if key_lower == "cell" and val_clean.lower() == "markdown":
            return "markdown"
    return "code"


def parse_notebook_segments(
    markdown_text: str,
    *,
    doc_base_name: str,
    output_dir: str | None = None,
    shared_images_dir: str | None = None,
    default_format: str = "png",
    default_drawlib_cell_mode: JupyterCellMode = "markdown",
    require_file: bool = True,
) -> list[NotebookSegment]:
    """Parse a Markdown document into ordered ``NotebookSegment`` items.

    Args:
        markdown_text: Raw Markdown source text.
        doc_base_name: Document stem used for ``<stem>_images/`` paths.
        output_dir: Target output directory for rendered images.
        shared_images_dir: Optional shared image directory for multi-locale deduplication.
        default_format: Default image extension ('png', 'webp', or 'svg').
        default_drawlib_cell_mode: Default cell mode for ``drawlib`` blocks without explicit ``cell=``.
        require_file: Whether to require ``file=<name>`` on ``drawlib`` blocks.

    Returns:
        list[NotebookSegment]: Ordered list of Markdown, Drawlib, and Python code segments.
    """
    masked_text, preserved = preserve_outer_fences(markdown_text)
    lines = masked_text.split("\n")
    segments: list[NotebookSegment] = []
    md_buffer: list[str] = []
    md_start_line = 1
    drawlib_counter = 0
    idx = 0

    def _flush_markdown() -> None:
        nonlocal md_buffer
        if not md_buffer:
            return
        restored = restore_outer_fences("\n".join(md_buffer), preserved).strip()
        md_buffer = []
        if restored:
            segments.append(
                NotebookSegment(
                    kind="markdown",
                    source=restored,
                    line_number=md_start_line,
                    cell_mode="markdown",
                )
            )

    while idx < len(lines):
        line = lines[idx]
        m_fence = _FENCE_OPEN_RE.match(line)
        if not m_fence:
            if not md_buffer and line.strip():
                md_start_line = idx + 1
            md_buffer.append(line)
            idx += 1
            continue

        fence_char = m_fence.group(1)[0]
        info_raw = m_fence.group(2).strip()
        fence_start_line = idx + 1
        close_re = re.compile(rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{3,}}[ \t\r]*$")

        body_lines: list[str] = []
        scan_idx = idx + 1
        while scan_idx < len(lines) and not close_re.match(lines[scan_idx]):
            body_lines.append(lines[scan_idx])
            scan_idx += 1
        closing_line = lines[scan_idx] if scan_idx < len(lines) else f"{fence_char * 3}"

        info_lower = info_raw.lower()
        is_drawlib = info_lower == "drawlib" or info_lower.startswith(("drawlib ", "drawlib\t"))
        is_python = info_lower in {"python", "py"} or info_lower.startswith(
            ("python ", "python\t", "py ", "py\t")
        )

        if is_drawlib:
            _flush_markdown()
            drawlib_counter += 1
            opt_str = info_raw[len("drawlib") :].strip()
            options = parse_block_info(opt_str)
            eff_cell_mode: JupyterCellMode = (
                options.cell if options.cell is not None else default_drawlib_cell_mode
            )
            rel_img, target_img = resolve_block_image_paths(
                options=options,
                doc_base_name=doc_base_name,
                block_counter=drawlib_counter,
                default_format=default_format,
                output_dir=output_dir,
                require_file=require_file,
                line_number=fence_start_line,
                shared_images_dir=shared_images_dir,
            )
            raw_code = "\n".join(line_s.rstrip("\r") for line_s in body_lines).strip()
            segments.append(
                NotebookSegment(
                    kind="drawlib",
                    source=raw_code,
                    line_number=fence_start_line + 1,
                    cell_mode=eff_cell_mode,
                    drawlib_options=options,
                    block_index=drawlib_counter,
                    rel_img_path=rel_img,
                    target_img_path=target_img,
                )
            )
            idx = scan_idx + 1
            md_start_line = idx + 1
            continue

        if is_python:
            lang_prefix = "python" if info_lower.startswith("python") else "py"
            opt_after = info_raw[len(lang_prefix) :].strip()
            py_cell_mode = _parse_python_fence_cell_mode(opt_after)
            if py_cell_mode == "code":
                _flush_markdown()
                raw_py = "\n".join(line_s.rstrip("\r") for line_s in body_lines).strip("\n")
                segments.append(
                    NotebookSegment(
                        kind="code",
                        source=raw_py,
                        line_number=fence_start_line + 1,
                        cell_mode="code",
                    )
                )
                idx = scan_idx + 1
                md_start_line = idx + 1
                continue
            # python cell=markdown stays inside the Markdown prose cell as a normal ```python block
            if not md_buffer:
                md_start_line = fence_start_line
            md_buffer.append(f"{fence_char * 3}python")
            md_buffer.extend(body_lines)
            md_buffer.append(closing_line)
            idx = scan_idx + 1
            continue

        if not md_buffer:
            md_start_line = fence_start_line
        md_buffer.append(line)
        md_buffer.extend(body_lines)
        if scan_idx < len(lines):
            md_buffer.append(closing_line)
        idx = scan_idx + 1

    _flush_markdown()
    return segments


def _sanitize_cell_magics(code: str) -> str:
    """Comment out IPython/Colab ``!`` and ``%`` magic lines while preserving exact line numbers."""
    out_lines: list[str] = []
    for line in code.split("\n"):
        if _MAGIC_LINE_RE.match(line):
            out_lines.append("# [magic skipped in dry-run]")
        else:
            out_lines.append(line)
    return "\n".join(out_lines)


def _capture_canvas_png_bytes() -> tuple[bytes, list[str]]:
    """Render the current Drawlib canvas state to PNG bytes in memory and return (png_bytes, warnings)."""
    canvas_inst = drawlib._core.l4_canvas.canvas
    canvas_inst._set_background()
    zorder = canvas_inst._draw_items()
    canvas_inst._remove_margin()

    is_grid = canvas_inst._grid or canvas_inst._grid_only or drawlib_settings.get_force_grid()
    buf = io.BytesIO()
    if is_grid:
        canvas_inst._render_with_grid(zorder, lambda: pyplot.savefig(buf, format="png"))
    else:
        pyplot.savefig(buf, format="png")
        canvas_inst._remove_artists_from_ax()

    warns = list(canvas_inst._geometry_warnings)
    return buf.getvalue(), warns


def _extract_cell_error_line(exc: BaseException, cell_filename: str, code_line_count: int) -> int:
    """Determine the 1-based line number inside the executed cell where ``exc`` occurred."""
    if isinstance(exc, SyntaxError) and exc.lineno is not None:
        return max(1, min(int(exc.lineno), max(code_line_count, 1)))

    tb = exc.__traceback__
    matched_line: int | None = None
    while tb is not None:
        frame = tb.tb_frame
        if frame.f_code.co_filename == cell_filename:
            matched_line = tb.tb_lineno
        tb = tb.tb_next

    if matched_line is not None:
        return max(1, min(int(matched_line), max(code_line_count, 1)))
    return 1


def _execute_single_code_cell(
    *,
    code: str,
    cell_index: int,
    seg_line_number: int,
    source_path: str,
    shared_globals: dict[str, Any],
) -> CellExecutionOutput:
    """Execute one notebook code cell in ``shared_globals`` and capture stdout, expr value, and figures."""
    canvas_inst = drawlib._core.l4_canvas.canvas
    orig_canvas_show = canvas_inst.show
    orig_core_show = drawlib._core.l4_canvas.show
    orig_mod_show = getattr(drawlib.canvas, "show", None)
    orig_canvas_save = canvas_inst.save
    orig_core_save = drawlib._core.l4_canvas.save
    orig_mod_save = getattr(drawlib.canvas, "save", None)
    orig_plt_show = pyplot.show

    captured_figures: list[bytes] = []
    captured_warnings: list[str] = []

    def _intercept_show(*_args: Any, **_kwargs: Any) -> None:  # noqa: ANN401
        png_bytes, warns = _capture_canvas_png_bytes()
        captured_figures.append(png_bytes)
        for w in warns:
            if w not in captured_warnings:
                captured_warnings.append(w)

    cell_filename = f"<notebook:{os.path.basename(source_path)}:In[{cell_index}]>"
    sanitized = _sanitize_cell_magics(code)
    code_lines = code.split("\n")
    stdout_buf = io.StringIO()
    result_repr: str | None = None

    canvas_inst._geometry_warnings.clear()

    try:
        setattr(canvas_inst, "show", _intercept_show)
        setattr(drawlib._core.l4_canvas, "show", _intercept_show)
        setattr(drawlib.canvas, "show", _intercept_show)
        setattr(canvas_inst, "save", _intercept_show)
        setattr(drawlib._core.l4_canvas, "save", _intercept_show)
        setattr(drawlib.canvas, "save", _intercept_show)
        setattr(pyplot, "show", _intercept_show)

        # Keep any imported show/save bindings in shared_globals synchronized with the interceptor
        if "show" in shared_globals and shared_globals["show"] is orig_core_show:
            shared_globals["show"] = _intercept_show
        if "save" in shared_globals and shared_globals["save"] is orig_core_save:
            shared_globals["save"] = _intercept_show

        tree = ast.parse(sanitized, filename=cell_filename, mode="exec")
        suppress_last = sanitized.rstrip().endswith(";")

        with warnings.catch_warnings(), contextlib.redirect_stdout(stdout_buf):
            if drawlib_settings.get_logging_mode() not in {"verbose", "developer"}:
                warnings.filterwarnings("ignore", message=r"Glyph .* missing from font", category=UserWarning)

            if tree.body and isinstance(tree.body[-1], ast.Expr):
                prefix_mod = ast.Module(body=tree.body[:-1], type_ignores=[])
                if prefix_mod.body:
                    exec(compile(prefix_mod, filename=cell_filename, mode="exec"), shared_globals)
                last_expr = ast.Expression(body=tree.body[-1].value)
                val = eval(compile(last_expr, filename=cell_filename, mode="eval"), shared_globals)  # noqa: S307
                if val is not None and not suppress_last:
                    if isinstance(val, Dimage):
                        img_buf = io.BytesIO()
                        val.get_pil_image().save(img_buf, format="PNG")
                        captured_figures.append(img_buf.getvalue())
                    else:
                        result_repr = repr(val)
            else:
                exec(compile(tree, filename=cell_filename, mode="exec"), shared_globals)

            # Re-bind intercepted show/save if the cell imported them from drawlib.canvas
            if shared_globals.get("show") is orig_core_show:
                shared_globals["show"] = _intercept_show
            if shared_globals.get("save") is orig_core_save:
                shared_globals["save"] = _intercept_show

    except Exception as exc:
        cell_line = _extract_cell_error_line(exc, cell_filename, len(code_lines))
        md_line = seg_line_number + cell_line - 1
        offending = code_lines[cell_line - 1].strip() if 1 <= cell_line <= len(code_lines) else ""
        tb_short = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        msg = (
            f'Notebook Dry-Run failed in "{source_path}" at cell In [{cell_index}] '
            f"(markdown line {md_line}, cell line {cell_line}): {tb_short}\n"
            f"  Line {cell_line}: {offending}"
        )
        raise NotebookExecutionError(
            msg,
            source_path=source_path,
            cell_index=cell_index,
            cell_line=cell_line,
            markdown_line=md_line,
            code=code,
            cause=exc,
        ) from exc
    finally:
        setattr(canvas_inst, "show", orig_canvas_show)
        setattr(drawlib._core.l4_canvas, "show", orig_core_show)
        if orig_mod_show is not None:
            setattr(drawlib.canvas, "show", orig_mod_show)
        setattr(canvas_inst, "save", orig_canvas_save)
        setattr(drawlib._core.l4_canvas, "save", orig_core_save)
        if orig_mod_save is not None:
            setattr(drawlib.canvas, "save", orig_mod_save)
        setattr(pyplot, "show", orig_plt_show)

    return CellExecutionOutput(
        execution_count=cell_index,
        stdout=stdout_buf.getvalue(),
        result_repr=result_repr,
        figures=captured_figures,
        geometry_warnings=captured_warnings,
    )


def execute_notebook_cells(
    segments: list[NotebookSegment],
    *,
    source_path: str,
    styles_path: str | None = None,
    utils_path: str | None = None,
    project_root: str | None = None,
    doc_base_name: str = "notebook",
    output_dir: str | None = None,
    shared_images_dir: str | None = None,
) -> NotebookExecutionResult:
    """Execute all code cells in ``segments`` sequentially in a shared Python namespace.

    Args:
        segments: Ordered notebook segments from ``parse_notebook_segments()``.
        source_path: Path to the source Markdown file for diagnostics and working directory context.
        styles_path: Optional path to ``styles.py``.
        utils_path: Optional path to ``utils.py``.
        project_root: Optional root directory of the Drawlib project.
        doc_base_name: Document stem used when saving ``show()`` outputs to disk for HTML preview.
        output_dir: Optional output directory where HTML preview images are written.
        shared_images_dir: Optional shared image directory across locales.

    Returns:
        NotebookExecutionResult: Captured outputs, execution counts, and geometry warnings.

    Raises:
        NotebookExecutionError: If any code cell raises a SyntaxError or runtime exception.
    """
    shared_globals: dict[str, Any] = {"__name__": "__main__"}
    load_styles_and_utils(
        styles_path=styles_path,
        utils_path=utils_path,
        shared_globals=shared_globals,
    )

    source_abs = os.path.abspath(source_path) if os.path.exists(source_path) else source_path
    file_dir = os.path.dirname(source_abs) if os.path.exists(source_abs) else os.getcwd()
    exec_dir = file_dir
    if (
        project_root
        and not os.path.exists(os.path.join(file_dir, "_assets"))
        and os.path.exists(os.path.join(project_root, "_assets"))
    ):
        exec_dir = project_root

    orig_cwd = os.getcwd()
    added_paths: list[str] = []
    result = NotebookExecutionResult(source_path=source_path)

    drawlib._core.l4_canvas.clear()

    try:
        if os.path.isdir(exec_dir):
            os.chdir(exec_dir)
        for p in (file_dir, project_root):
            if p and os.path.isdir(p) and p not in sys.path:
                sys.path.insert(0, p)
                added_paths.append(p)

        exec_counter = 0
        for seg_idx, seg in enumerate(segments):
            is_exec_cell = seg.kind == "code" or (seg.kind == "drawlib" and seg.cell_mode == "code")
            if not is_exec_cell:
                continue

            exec_counter += 1
            cell_code = convert_save_to_show(seg.source) if seg.kind == "drawlib" else seg.source
            cell_out = _execute_single_code_cell(
                code=cell_code,
                cell_index=exec_counter,
                seg_line_number=seg.line_number,
                source_path=source_path,
                shared_globals=shared_globals,
            )

            for warn_msg in cell_out.geometry_warnings:
                formatted_warn = f"In [{exec_counter}]: {warn_msg}"
                result.geometry_warnings.append(formatted_warn)
                print(f"[Geometry Warning] ({source_path} In [{exec_counter}]) {warn_msg}", file=sys.stderr)

            # Save rendered figures to disk when output_dir is provided so HTML preview can display them
            if output_dir and cell_out.figures:
                if seg.kind == "drawlib" and seg.target_img_path:
                    os.makedirs(os.path.dirname(os.path.abspath(seg.target_img_path)), exist_ok=True)
                    with open(seg.target_img_path, "wb") as f:
                        f.write(cell_out.figures[0])
                    cell_out.figure_rel_paths.append(seg.rel_img_path)
                else:
                    for fig_i, png_bytes in enumerate(cell_out.figures, start=1):
                        fig_name = f"cell_{exec_counter}_{fig_i}.png"
                        if shared_images_dir is not None:
                            target_fig = os.path.abspath(os.path.join(shared_images_dir, fig_name))
                            rel_fig = os.path.relpath(target_fig, os.path.abspath(output_dir)).replace(os.sep, "/")
                        else:
                            rel_fig = f"{doc_base_name}_images/{fig_name}"
                            target_fig = os.path.join(output_dir, rel_fig)
                        os.makedirs(os.path.dirname(target_fig), exist_ok=True)
                        with open(target_fig, "wb") as f:
                            f.write(png_bytes)
                        cell_out.figure_rel_paths.append(rel_fig)

            result.cell_outputs[seg_idx] = cell_out
            result.executed_cell_count = exec_counter
    finally:
        os.chdir(orig_cwd)
        for p in added_paths:
            if p in sys.path:
                sys.path.remove(p)

    return result


def _to_ipynb_lines(text: str) -> list[str]:
    r"""Split text into a list of ``\n``-terminated lines per nbformat v4 conventions."""
    if not text:
        return []
    lines = text.split("\n")
    return [f"{line}\n" for line in lines[:-1]] + [lines[-1]]


def _resolve_public_diagram_url(
    rel_img_path: str,
    *,
    site_url: str,
    lang: str | None,
) -> str:
    """Resolve a public URL for a rendered diagram when ``image_mode == 'url'``."""
    clean_rel = rel_img_path.replace("\\", "/")
    if not site_url:
        return clean_rel
    base = site_url.rstrip("/")
    if lang:
        norm = os.path.normpath(os.path.join(lang, clean_rel)).replace("\\", "/").lstrip("/")
    else:
        norm = clean_rel.lstrip("/")
    return f"{base}/{norm}"


def build_ipynb_dict(
    segments: list[NotebookSegment],
    *,
    execution_result: NotebookExecutionResult | None = None,
    image_mode: JupyterImageMode = "attachment",
    colab_url: str = "",
    setup_packages: tuple[str, ...] = ("drawlib",),
    site_url: str = "",
    lang: str | None = None,
    notebook_name: str = "notebook.ipynb",
) -> dict[str, Any]:
    """Assemble a valid ``nbformat v4.5`` Jupyter/Colab notebook dictionary.

    Args:
        segments: Ordered notebook segments.
        execution_result: Optional dry-run execution results for code cells.
        image_mode: ``'attachment'``, ``'url'``, or ``'relative'``.
        colab_url: Optional ``https://colab.research.google.com/github/...`` URL for top badge.
        setup_packages: Packages for automatic ``!pip install -q ...`` setup cell (empty disables).
        site_url: Public base URL used when ``image_mode == 'url'``.
        lang: Locale code used when resolving public image URLs.
        notebook_name: Notebook filename stored in Colab metadata.

    Returns:
        dict[str, Any]: JSON-serializable ``nbformat v4.5`` dictionary.
    """
    cells: list[dict[str, Any]] = []
    md_parts: list[str] = []
    md_attachments: dict[str, dict[str, str]] = {}
    badge_injected = False
    setup_injected = False
    exec_counter = 0

    colab_badge_md = (
        f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"
        if colab_url
        else ""
    )

    def _inject_setup_cell_if_needed() -> None:
        nonlocal setup_injected
        if setup_injected or not setup_packages:
            return
        setup_injected = True
        pkgs_str = " ".join(setup_packages)
        setup_code = f"!pip install -q {pkgs_str}"
        cells.append(
            {
                "cell_type": "code",
                "execution_count": None,
                "id": "cell-setup",
                "metadata": {},
                "outputs": [],
                "source": _to_ipynb_lines(setup_code),
            }
        )

    def _flush_md_cell() -> None:
        nonlocal md_parts, md_attachments, badge_injected
        if not md_parts:
            return
        combined = "\n\n".join(part for part in md_parts if part.strip())
        md_parts = []
        if not combined:
            return
        if colab_badge_md and not badge_injected:
            badge_injected = True
            lines = combined.split("\n")
            if lines and lines[0].startswith("# "):
                combined = "\n".join([lines[0], "", colab_badge_md, *lines[1:]])
            else:
                combined = f"{colab_badge_md}\n\n{combined}"

        cell_dict: dict[str, Any] = {
            "cell_type": "markdown",
            "id": f"cell-{len(cells) + 1}",
            "metadata": {},
            "source": _to_ipynb_lines(combined),
        }
        if md_attachments:
            cell_dict["attachments"] = dict(md_attachments)
            md_attachments = {}
        cells.append(cell_dict)
        _inject_setup_cell_if_needed()

    if colab_badge_md and (not segments or segments[0].kind == "code"):
        md_parts.append(colab_badge_md)
        badge_injected = True
        _flush_md_cell()

    for seg_idx, seg in enumerate(segments):
        if seg.kind == "markdown":
            md_parts.append(seg.source)
            continue

        if seg.kind == "drawlib" and seg.cell_mode == "markdown":
            caption = (seg.drawlib_options.caption if seg.drawlib_options else None) or "Diagram"
            img_basename = os.path.basename(seg.rel_img_path) or f"diagram_{seg.block_index}.png"
            if image_mode == "attachment" and seg.target_img_path and os.path.isfile(seg.target_img_path):
                with open(seg.target_img_path, "rb") as f:
                    b64_str = base64.b64encode(f.read()).decode("ascii")
                mime = "image/svg+xml" if img_basename.lower().endswith(".svg") else "image/png"
                md_attachments[img_basename] = {mime: b64_str}
                img_md = f"![{caption}](attachment:{img_basename})"
            elif image_mode == "url" and site_url:
                pub_url = _resolve_public_diagram_url(seg.rel_img_path, site_url=site_url, lang=lang)
                img_md = f"![{caption}]({pub_url})"
            else:
                img_md = f"![{caption}]({seg.rel_img_path})"

            if seg.drawlib_options and seg.drawlib_options.caption:
                img_md = f"{img_md}\n\n*{seg.drawlib_options.caption}*"
            md_parts.append(img_md)
            continue

        # Code cell (either ```python or ```drawlib cell=code)
        _flush_md_cell()
        _inject_setup_cell_if_needed()

        exec_counter += 1
        cell_code = convert_save_to_show(seg.source) if seg.kind == "drawlib" else seg.source
        cell_out = execution_result.cell_outputs.get(seg_idx) if execution_result is not None else None

        outputs_list: list[dict[str, Any]] = []
        if cell_out is not None:
            if cell_out.stdout:
                outputs_list.append(
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": _to_ipynb_lines(cell_out.stdout),
                    }
                )
            if cell_out.result_repr is not None:
                outputs_list.append(
                    {
                        "data": {"text/plain": _to_ipynb_lines(cell_out.result_repr)},
                        "execution_count": cell_out.execution_count,
                        "metadata": {},
                        "output_type": "execute_result",
                    }
                )
            if cell_out.figures:
                for fig_bytes in cell_out.figures:
                    b64_fig = base64.b64encode(fig_bytes).decode("ascii")
                    outputs_list.append(
                        {
                            "data": {
                                "image/png": b64_fig,
                                "text/plain": ["<Figure size rendered by drawlib>"],
                            },
                            "metadata": {},
                            "output_type": "display_data",
                        }
                    )

        cells.append(
            {
                "cell_type": "code",
                "execution_count": cell_out.execution_count if cell_out is not None else None,
                "id": f"cell-{len(cells) + 1}",
                "metadata": {},
                "outputs": outputs_list,
                "source": _to_ipynb_lines(cell_code),
            }
        )

    _flush_md_cell()

    return {
        "cells": cells,
        "metadata": {
            "colab": {
                "name": notebook_name,
                "provenance": [],
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_ipynb_file(ipynb_dict: dict[str, Any], output_path: str) -> None:
    """Write ``ipynb_dict`` to ``output_path`` as deterministic, human-readable JSON."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ipynb_dict, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _render_drawlib_markdown_figure_html(seg: NotebookSegment) -> str:
    """Render a ``cell=markdown`` Drawlib diagram block into HTML figure + optional code fold/show."""
    opts = seg.drawlib_options or DrawlibBlockOptions()
    esc_src = html.escape(seg.rel_img_path, quote=True)
    esc_alt = html.escape(opts.caption or os.path.basename(seg.rel_img_path), quote=True)

    style_parts: list[str] = []
    if opts.width:
        style_parts.append(f"width: {html.escape(opts.width, quote=True)};")
    if opts.height:
        style_parts.append(f"height: {html.escape(opts.height, quote=True)};")
    style_attr = f' style="{" ".join(style_parts)}"' if style_parts else ""

    align_cls = f" align-{opts.align}" if opts.align in {"left", "center", "right"} else " align-center"
    fig_parts = [
        f'<figure class="drawlib-figure{align_cls}">',
        f'  <img src="{esc_src}" alt="{esc_alt}"{style_attr} loading="lazy">',
    ]
    if opts.caption:
        fig_parts.append(f"  <figcaption>{html.escape(opts.caption)}</figcaption>")
    fig_parts.append("</figure>")

    if opts.code in {"show", "fold"}:
        highlighted = pygments_highlight(seg.source, "python")
        code_inner = highlighted if highlighted else html.escape(seg.source)
        code_block = f'<pre><code class="language-python">{code_inner}</code></pre>'
        if opts.code == "fold":
            fig_parts.append(
                '<details class="drawlib-code-fold">\n'
                "  <summary>View Drawlib Python Code</summary>\n"
                f"  {code_block}\n"
                "</details>"
            )
        else:
            fig_parts.append(f'<div class="drawlib-code-show">{code_block}</div>')

    return "\n".join(fig_parts)


def render_notebook_body_html(
    segments: list[NotebookSegment],
    *,
    execution_result: NotebookExecutionResult | None = None,
    ipynb_href: str = "",
    colab_url: str = "",
    setup_packages: tuple[str, ...] = ("drawlib",),
) -> str:
    """Render notebook segments and dry-run outputs into a Jupyter/Colab-style HTML body.

    Args:
        segments: Ordered notebook segments.
        execution_result: Optional dry-run execution results for code cells.
        ipynb_href: Relative href to the companion ``.ipynb`` file for download button.
        colab_url: Optional ``https://colab.research.google.com/github/...`` URL.
        setup_packages: Tuple of pip packages shown in the optional setup cell.

    Returns:
        str: HTML body string containing the notebook action toolbar and cells.
    """
    parts: list[str] = ['<div class="jupyter-notebook">']

    # Top Notebook Action Toolbar
    toolbar_items: list[str] = []
    if colab_url:
        esc_colab = html.escape(colab_url, quote=True)
        toolbar_items.append(
            f'<a class="nb-btn nb-btn-colab" href="{esc_colab}" target="_blank" rel="noopener noreferrer">'
            '<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">'
            "</a>"
        )
    if ipynb_href:
        esc_ipynb = html.escape(ipynb_href, quote=True)
        esc_dl_name = html.escape(os.path.basename(ipynb_href), quote=True)
        toolbar_items.append(
            f'<a class="nb-btn nb-btn-download" href="{esc_ipynb}" download="{esc_dl_name}">'
            "⬇ Download .ipynb"
            "</a>"
        )
    if execution_result is not None and execution_result.executed_cell_count > 0:
        cnt = execution_result.executed_cell_count
        label = "cell" if cnt == 1 else "cells"
        toolbar_items.append(f'<span class="nb-status-pill">✓ Dry-Run Verified ({cnt} {label})</span>')

    if toolbar_items:
        parts.append('  <div class="nb-toolbar">\n    ' + "\n    ".join(toolbar_items) + "\n  </div>")

    md_html_chunks: list[str] = []
    setup_rendered = False
    exec_counter = 0

    def _render_setup_cell_html() -> None:
        nonlocal setup_rendered
        if setup_rendered or not setup_packages:
            return
        setup_rendered = True
        pkgs_str = " ".join(setup_packages)
        setup_src = f"!pip install -q {pkgs_str}"
        hl_setup = pygments_highlight(setup_src, "bash") or html.escape(setup_src)
        parts.append(
            '  <div class="nb-cell nb-code-cell nb-setup-cell">\n'
            '    <div class="nb-input">\n'
            '      <div class="nb-prompt nb-in-prompt">In [setup]:</div>\n'
            '      <div class="nb-code-area">\n'
            f'        <pre><code class="language-bash">{hl_setup}</code></pre>\n'
            "      </div>\n"
            "    </div>\n"
            "  </div>"
        )

    def _flush_md_html() -> None:
        nonlocal md_html_chunks
        if not md_html_chunks:
            return
        combined_md_html = "\n".join(md_html_chunks)
        md_html_chunks = []
        parts.append(f'  <div class="nb-cell nb-markdown-cell">\n{combined_md_html}\n  </div>')
        _render_setup_cell_html()

    for seg_idx, seg in enumerate(segments):
        if seg.kind == "markdown":
            md_html_chunks.append(parse_markdown_to_html(seg.source))
            continue

        if seg.kind == "drawlib" and seg.cell_mode == "markdown":
            md_html_chunks.append(_render_drawlib_markdown_figure_html(seg))
            continue

        _flush_md_html()
        _render_setup_cell_html()

        exec_counter += 1
        cell_code = convert_save_to_show(seg.source) if seg.kind == "drawlib" else seg.source
        cell_out = execution_result.cell_outputs.get(seg_idx) if execution_result is not None else None
        prompt_num = str(cell_out.execution_count) if cell_out is not None else str(exec_counter)

        hl_code = pygments_highlight(cell_code, "python") or html.escape(cell_code)
        cell_lines = [
            '  <div class="nb-cell nb-code-cell">',
            '    <div class="nb-input">',
            f'      <div class="nb-prompt nb-in-prompt">In [{prompt_num}]:</div>',
            '      <div class="nb-code-area">',
            f'        <pre><code class="language-python">{hl_code}</code></pre>',
            "      </div>",
            "    </div>",
        ]

        if cell_out is not None and (cell_out.stdout or cell_out.result_repr is not None or cell_out.figure_rel_paths):
            cell_lines.append('    <div class="nb-output">')
            cell_lines.append(f'      <div class="nb-prompt nb-out-prompt">Out [{prompt_num}]:</div>')
            cell_lines.append('      <div class="nb-output-area">')
            if cell_out.stdout:
                esc_stdout = html.escape(cell_out.stdout)
                cell_lines.append(f'        <pre class="nb-stream-stdout">{esc_stdout}</pre>')
            if cell_out.result_repr is not None:
                esc_repr = html.escape(cell_out.result_repr)
                cell_lines.append(f'        <pre class="nb-execute-result">{esc_repr}</pre>')
            for fig_rel in cell_out.figure_rel_paths:
                esc_fig = html.escape(fig_rel, quote=True)
                cell_lines.append(
                    f'        <div class="nb-output-figure"><img src="{esc_fig}" alt="Output [{prompt_num}]"></div>'
                )
            cell_lines.append("      </div>")
            cell_lines.append("    </div>")

        cell_lines.append("  </div>")
        parts.append("\n".join(cell_lines))

    _flush_md_html()
    parts.append("</div>")
    return "\n".join(parts)
