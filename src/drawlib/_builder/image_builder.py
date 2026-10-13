# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Python drawing script and package executor for drawlib build image."""

from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import os
import re
import sys
import traceback
import warnings
from collections.abc import Callable, Sequence
from typing import Literal

from pydantic import validate_call

import drawlib._core.l4_canvas
import drawlib.canvas
from drawlib._builder._common import (
    BuildImageCache,
    FileBuildProgress,
    format_duplicate_output_error,
    hash_file,
    load_styles_and_utils,
    resolve_styles_and_utils,
)
from drawlib._builder._image_ast import (
    _collect_target_files,
    _extract_single_static_save,
    _get_python_files,
    _has_local_imports,
    _is_save_call_node,
    _normalize_build_inputs_and_output,
    _parse_static_save_call,
    _resolve_execution_mode,
    _SaveCallVisitor,
    check_duplicate_script_outputs,
    resolve_effective_output_dir,
    resolve_static_save_target,
)
from drawlib._core.l1_core import dutil_settings, get_script_relative_path, logger
from drawlib._core.l4_canvas import clear
from drawlib._core.l4_canvas._canvas import Canvas


class DrawlibExecuter:
    """Executor for running Python files or directories containing drawing code.

    Executes Python files specified as targets or recursively runs all Python files
    within a specified directory. Handles logging, module loading, and error handling.
    """

    def __init__(
        self,
        mode: Literal["none", "auto_clear", "auto_initialize"] = "auto_clear",
        styles_path: str | None = None,
        utils_path: str | None = None,
        output_dir: str | None = None,
        output_file: str | None = None,
        image_format: Literal["png", "webp", "jpg", "pdf"] | None = None,
        grid: bool = False,
        no_cache: bool = False,
        target_roots: Sequence[str] | None = None,
    ) -> None:
        """Initialize a DrawlibExecuter instance.

        Args:
            mode (Literal["none", "auto_clear", "auto_initialize"]):
                The execution mode for handling Python file execution:
                - "none": Executes Python files without clearing canvas between executions.
                - "auto_clear": Automatically clears the canvas between executing each Python file.
                - "auto_initialize": Automatically initializes canvas per execution.
            styles_path (str | None): Optional path to Python styles script.
            utils_path (str | None): Optional path to Python utils script.
            output_dir (str | None): Optional path to directory where images should be saved.
            output_file (str | None): Optional explicit output file path when executing a single script.
            image_format (Literal["png", "webp", "jpg", "pdf"] | None): Optional image format override.
            grid (bool): Whether to generate coordinate grid overlaid images in addition to normal images.
            no_cache (bool): If True, disable reading/writing the SQLite build image cache.
            target_roots (Sequence[str] | None): Optional base directory paths for preserving subdirectories.

        Raises:
            ValueError: If mode is not one of ["none", "auto_clear", "auto_initialize"].
        """
        if mode not in {"none", "auto_clear", "auto_initialize"}:
            raise ValueError(f'Arg mode is "{mode}". But it must be one of ["none", "auto_clear", "auto_initialize"].')
        self._mode = mode
        self._styles_path = styles_path
        self._utils_path = utils_path
        s_hash = hash_file(styles_path) if styles_path else ""
        u_hash = hash_file(utils_path) if utils_path else ""
        self._config_hash = f"{s_hash}:{u_hash}"
        self._output_dir = output_dir
        self._output_file = output_file
        self._image_format: Literal["png", "webp", "jpg", "pdf"] | None = image_format
        self._grid = grid
        self._no_cache = no_cache
        self._cache = BuildImageCache(enabled=not no_cache)
        self._current_cache_info: tuple[str, str, str, str] | None = None
        self._topdir_path: str = ""
        self._target_roots: list[str] = [os.path.abspath(r) for r in target_roots] if target_roots else []
        self._current_target_root: str = ""
        self._current_source_label: str = ""
        self._current_progress: FileBuildProgress | None = None
        self._current_save_step: int = 0
        self._current_total_saves: int = 1
        self._runtime_seen_outputs: dict[str, str] = {}

    def set_target_roots(self, roots: Sequence[str]) -> None:
        """Set base target directory roots for preserving relative subdirectory output structure."""
        self._target_roots = [os.path.abspath(r) for r in roots]

    def _get_effective_output_dir(self, script_path: str) -> str | None:
        """Compute the effective output directory for a script, preserving subdirectories if under a target dir."""
        return resolve_effective_output_dir(
            output_dir=self._output_dir,
            script_path=script_path,
            current_target_root=self._current_target_root,
            target_roots=self._target_roots,
        )

    def _resolve_static_save_target(
        self,
        script_path: str,
        call_file: str | None,
        call_format: str | None,
    ) -> str:
        """Resolve the output file path that a static `save(file, format)` call in `script_path` will write."""
        return resolve_static_save_target(
            script_path=script_path,
            call_file=call_file,
            call_format=call_format,
            output_file=self._output_file,
            output_dir=self._output_dir,
            image_format=self._image_format,
            current_target_root=self._current_target_root,
            target_roots=self._target_roots,
        )

    @staticmethod
    def _parse_static_save_call(node: ast.Call) -> tuple[str | None, str | None] | None:
        """Extract static `(call_file, call_format)` from an AST `save(...)` call node, or None if not static."""
        return _parse_static_save_call(node)

    def _check_duplicate_outputs(
        self,
        file_paths: Sequence[str],
        display_names: Sequence[str],
    ) -> dict[str, int]:
        """Pre-check all target Python scripts via AST for duplicate output image paths and count saves per file."""
        return check_duplicate_script_outputs(
            file_paths=file_paths,
            display_names=display_names,
            resolve_target_fn=self._resolve_static_save_target,
        )

    def _create_wrapped_save(
        self,
        orig_canvas_save: Callable[..., None],
        canvas_inst: Canvas,
    ) -> Callable[..., None]:
        """Create a wrapped save function that applies output overrides and guards against duplicate outputs."""

        def _wrapped_save(
            file: str | None = None,
            format: Literal["png", "webp", "jpg", "pdf"] | None = None,
        ) -> None:
            eff_format: Literal["png", "webp", "jpg", "pdf"] | None = (
                self._image_format if self._image_format else format
            )
            if self._output_file is not None:
                target = os.path.abspath(self._output_file)
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
            current_src = self._current_source_label or "<script>"
            if resolved_abs in self._runtime_seen_outputs:
                raise ValueError(
                    format_duplicate_output_error(
                        resolved_abs,
                        self._runtime_seen_outputs[resolved_abs],
                        current_src,
                    )
                )
            self._runtime_seen_outputs[resolved_abs] = current_src
            orig_canvas_save(file=eff_file, format=eff_format)
            if self._current_cache_info is not None and os.path.isfile(resolved_abs):
                c_key, c_code_hash, c_cfg_hash, c_ext = self._current_cache_info
                base_stem, ext_dot = os.path.splitext(resolved_abs)
                grid_candidate = f"{base_stem}_grid{ext_dot}"
                with open(resolved_abs, "rb") as f_img:
                    img_bytes = f_img.read()
                grid_bytes = None
                if os.path.isfile(grid_candidate):
                    with open(grid_candidate, "rb") as f_grid:
                        grid_bytes = f_grid.read()
                self._cache.put(
                    cache_key=c_key,
                    code_hash=c_code_hash,
                    config_hash=c_cfg_hash,
                    image_format=c_ext,
                    image_blob=img_bytes,
                    grid_blob=grid_bytes,
                )
            self._current_save_step += 1
            if self._current_progress is not None:
                self._current_progress.update(
                    self._current_save_step,
                    max(self._current_total_saves, self._current_save_step),
                    done=False,
                )

        return _wrapped_save

    @staticmethod
    def _has_local_imports(tree: ast.AST, script_dir: str, topdir_path: str) -> bool:
        """Check whether the AST imports any local Python modules from script_dir or topdir_path."""
        return _has_local_imports(tree, script_dir, topdir_path)

    def _extract_single_static_save(
        self,
        tree: ast.AST,
        script_dir: str,
    ) -> tuple[str | None, str | None] | None:
        """Extract static save arguments if script has no local module imports, else None."""
        return _extract_single_static_save(tree, script_dir, self._topdir_path)

    def _restore_cached_image(
        self,
        target_abs: str,
        ext: str,
        need_grid: bool,
        cache_key: str,
    ) -> bool:
        """Restore normal and optional grid images from cache to disk if available."""
        cached_entry = self._cache.get(cache_key, image_format=ext)
        if cached_entry is None:
            return False

        norm_bytes, grid_bytes = cached_entry
        if need_grid and grid_bytes is None:
            return False

        os.makedirs(os.path.dirname(target_abs), exist_ok=True)
        with open(target_abs, "wb") as f_out:
            f_out.write(norm_bytes)
        if need_grid and grid_bytes is not None:
            base_stem, ext_dot = os.path.splitext(target_abs)
            with open(f"{base_stem}_grid{ext_dot}", "wb") as f_grid_out:
                f_grid_out.write(grid_bytes)

        self._runtime_seen_outputs[target_abs] = self._current_source_label or "<script>"
        self._current_save_step += 1
        if self._current_progress is not None:
            self._current_progress.update(
                self._current_save_step,
                max(self._current_total_saves, self._current_save_step),
                done=False,
            )
        return True

    def _try_cache_or_prepare(self, file_path: str, total_saves: int) -> bool:
        """Attempt to restore a single-save script output from cache or prepare cache metadata for storing."""
        self._current_cache_info = None
        if self._no_cache or self._mode not in {"auto_clear", "auto_initialize"} or total_saves != 1:
            return False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            tree = ast.parse(code, filename=file_path)
        except (OSError, SyntaxError):
            return False

        script_dir = os.path.dirname(os.path.abspath(file_path))
        parsed_save = None if "grid_only" in code else self._extract_single_static_save(tree, script_dir)
        if parsed_save is None:
            return False

        call_file, call_format = parsed_save
        target_abs = self._resolve_static_save_target(file_path, call_file, call_format)
        ext = os.path.splitext(target_abs)[1].lower().lstrip(".")
        if ext not in {"png", "webp"}:
            return False

        need_grid = self._grid or dutil_settings.get_force_grid() or bool(re.search(r"\bgrid\s*=\s*True\b", code))
        project_root = self._topdir_path or (self._target_roots[0] if self._target_roots else None)
        cache_key, code_hash = self._cache.compute_keys(
            code=code,
            config_hash=self._config_hash,
            context_dir=script_dir,
            project_root=project_root,
            source_file=file_path,
            target_file=target_abs,
        )
        if self._restore_cached_image(target_abs, ext, need_grid, cache_key):
            return True

        self._current_cache_info = (cache_key, code_hash, self._config_hash, ext)
        return False

    def _execute_target_path(self, path: str) -> None:
        """Execute a resolved Python file or directory path."""
        self._current_target_root = (
            os.path.abspath(path) if os.path.isdir(path) else os.path.dirname(os.path.abspath(path))
        )
        self._add_topdir_to_syspath(path)
        logger.info("Execute python files")
        if os.path.isfile(path):
            if not path.endswith(".py"):
                raise ValueError(f'Unable to run "{path}"')
            single_name = f"/{os.path.basename(path)}"
            save_counts = self._check_duplicate_outputs([path], [single_name])
            total_saves = save_counts.get(path, 0)
            self._current_source_label = single_name
            self._current_save_step = 0
            self._current_total_saves = total_saves
            eff_out = self._get_effective_output_dir(path)
            if eff_out is not None:
                dutil_settings.set_output_dir(eff_out)
                os.makedirs(eff_out, exist_ok=True)
            progress = FileBuildProgress(
                1,
                1,
                file_name=single_name,
                name_width=len(single_name),
                image_width=len(str(max(total_saves, 0))),
            )
            self._current_progress = progress
            progress.update(0, total_saves, done=False)
            if not self._try_cache_or_prepare(path, total_saves):
                self._exec_module(path)
            self._current_cache_info = None
            final_saves = max(total_saves, self._current_save_step)
            progress.update(final_saves, final_saves, done=True)
            self._current_progress = None
            return

        file_paths = [fp for fp in self._get_python_files(path) if not os.path.basename(fp).startswith("__")]
        total_files = len(file_paths)
        display_names = ["/" + os.path.relpath(fp, path).replace(os.sep, "/") for fp in file_paths]
        save_counts = self._check_duplicate_outputs(file_paths, display_names)
        max_saves = max(save_counts.values(), default=0)
        image_width = len(str(max(max_saves, 0)))
        name_width = max((len(n) for n in display_names), default=0)
        for idx, (file_path, disp_name) in enumerate(zip(file_paths, display_names), start=1):
            total_saves = save_counts.get(file_path, 0)
            self._current_source_label = disp_name
            self._current_save_step = 0
            self._current_total_saves = total_saves
            eff_out = self._get_effective_output_dir(file_path)
            if eff_out is not None:
                dutil_settings.set_output_dir(eff_out)
                os.makedirs(eff_out, exist_ok=True)
            progress = FileBuildProgress(
                idx,
                total_files,
                file_name=disp_name,
                name_width=name_width,
                image_width=image_width,
            )
            self._current_progress = progress
            progress.update(0, total_saves, done=False)
            if not self._try_cache_or_prepare(file_path, total_saves):
                self._exec_module(file_path)
            self._current_cache_info = None
            final_saves = max(total_saves, self._current_save_step)
            progress.update(final_saves, final_saves, done=True)
            self._current_progress = None

    @validate_call
    def execute(self, file_or_directory: str) -> None:
        """Execute the specified Python file or all Python files in the specified directory.

        Args:
            file_or_directory (str): Path to the Python file or directory containing Python files to execute.

        Raises:
            ValueError: If the specified path `file_or_directory` does not exist or is not a .py file.
        """
        if self._output_dir is not None:
            dutil_settings.set_output_dir(os.path.abspath(self._output_dir))
        if self._grid:
            dutil_settings.set_force_grid(True)

        canvas_inst = drawlib._core.l4_canvas.canvas
        orig_canvas_save = canvas_inst.save
        orig_core_save = drawlib._core.l4_canvas.save
        orig_canvas_mod_save = getattr(drawlib.canvas, "save", None)
        self._runtime_seen_outputs.clear()

        try:
            wrapped = self._create_wrapped_save(orig_canvas_save, canvas_inst)
            canvas_inst.save = wrapped  # ty: ignore
            drawlib._core.l4_canvas.save = wrapped  # ty: ignore
            drawlib.canvas.save = wrapped  # ty: ignore

            path = get_script_relative_path(file_or_directory)
            if not os.path.exists(path):
                raise ValueError(f'"{path}" does not exist')

            self._execute_target_path(path)
        finally:
            canvas_inst.save = orig_canvas_save  # ty: ignore
            drawlib._core.l4_canvas.save = orig_core_save  # type: ignore[assignment]
            if orig_canvas_mod_save is not None:
                drawlib.canvas.save = orig_canvas_mod_save  # type: ignore[assignment]
            if self._grid:
                dutil_settings.set_force_grid(False)
            if self._output_dir is not None:
                dutil_settings.set_output_dir(None)
            self._current_target_root = ""

    def _add_topdir_to_syspath(self, path: str) -> None:
        """Add the top directory of the specified path to the Python sys.path."""
        if os.path.isfile(path):
            topdir = os.path.dirname(path)
            package_dir = ""
            while os.path.exists(os.path.join(topdir, "__init__.py")):
                package_dir = topdir
                topdir = os.path.dirname(topdir)
        else:
            init_path = os.path.join(path, "__init__.py")
            if not os.path.exists(init_path):
                topdir = path
                package_dir = ""
            else:
                topdir = path
                package_dir = ""
                while os.path.exists(os.path.join(topdir, "__init__.py")):
                    package_dir = topdir
                    topdir = os.path.dirname(topdir)

        self._topdir_path = topdir
        if package_dir:
            logger.info(f'Detect package root "{package_dir}".')
            if topdir not in sys.path:
                sys.path.insert(0, topdir)
                logger.info(f'    - Add parent directory of package root "{topdir}" to Python Path.')
            else:
                logger.info(f'    - Parent of package directory "{topdir}" is already in Python Path.')
        else:
            logger.info(f'Target directory "{topdir}".')
            if topdir not in sys.path:
                sys.path.insert(0, topdir)
                logger.info(f'    - Add directory "{topdir}" to Python Path.')
        logger.info("")

    @staticmethod
    def _get_python_files(directory: str) -> list[str]:
        """Retrieve all Python files recursively within the specified directory."""
        return _get_python_files(directory)

    def _resolve_module_name(self, file_path: str) -> str:
        """Resolve module name and ensure parent packages/directories are loaded."""
        is_package = False
        if self._topdir_path:
            rel = os.path.relpath(file_path, self._topdir_path)
            parts = rel.split(os.sep)
            if len(parts) > 1 and os.path.exists(os.path.join(self._topdir_path, parts[0], "__init__.py")):
                is_package = True

        if is_package:
            words = self._get_package_words(file_path)
            self._load_parent_modules(words)
            return ".".join(words).replace(".py", "")

        script_dir = os.path.dirname(os.path.abspath(file_path))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        return os.path.splitext(os.path.basename(file_path))[0]

    def _prepare_canvas_for_module(self) -> None:
        """Reset/initialize canvas and apply optional styles and utils scripts before module execution."""
        if self._mode in {"auto_clear", "auto_initialize"}:
            clear()

        load_styles_and_utils(styles_path=self._styles_path, utils_path=self._utils_path)

    def _exec_module(self, file_path: str) -> None:
        """Execute the specified Python module file."""
        if self._is_module_loaded(file_path) and self._current_cache_info is None:
            if self._current_progress is None:
                logger.info(f"    - {file_path}")
            return

        name = self._resolve_module_name(file_path)
        mspec = importlib.util.spec_from_file_location(
            name=name,
            location=file_path,
        )
        if mspec is None or mspec.loader is None:
            if self._current_progress is None:
                logger.info(f"    - {file_path} : skipped with unknown reason.")
            return
        module = importlib.util.module_from_spec(mspec)

        try:
            self._prepare_canvas_for_module()
            if self._current_progress is None:
                logger.info(f"    - {file_path}")
            with warnings.catch_warnings():
                if dutil_settings.get_logging_mode() not in {"verbose", "developer"}:
                    warnings.filterwarnings("ignore", message=r"Glyph .* missing from font", category=UserWarning)
                    with contextlib.redirect_stdout(io.StringIO()):
                        mspec.loader.exec_module(module)
                else:
                    mspec.loader.exec_module(module)
            sys.modules[name] = module

        except Exception as e:
            file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
            logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
            logger.critical(str(e))
            logger.debug("")
            logger.debug(traceback.format_exc())
            raise

    @staticmethod
    def _exec_styles_and_utils(styles_path: str | None = None, utils_path: str | None = None) -> None:
        """Execute external styles and utils scripts before running drawing code."""
        load_styles_and_utils(styles_path=styles_path, utils_path=utils_path)

    @staticmethod
    def _is_module_loaded(module_path: str) -> bool:
        """Check if the specified module is already loaded."""
        module_path = os.path.abspath(module_path)

        for _, module in sys.modules.items():
            if module is None:
                continue
            mod_file = getattr(module, "__file__", None)
            if mod_file is None:
                continue
            if os.path.abspath(mod_file) == module_path:
                return True

        return False

    def _get_package_words(self, file_path: str) -> list[str]:
        """Retrieve the package words from the specified file path relative to the top directory."""
        last_path = file_path.replace(self._topdir_path, "")
        words = last_path.split(os.sep)
        if words[0] == "":
            words = words[1:]
        return words

    def _load_parent_modules(self, words: list[str]) -> None:
        """Load parent modules for the specified package words."""
        for i in range(1, len(words)):
            name = ".".join(words[:i])
            if name in sys.modules:
                continue

            location = os.path.join(self._topdir_path, os.sep.join(words[:i]), "__init__.py")
            if not os.path.exists(location):
                raise ValueError(f'"{location}" does not exist. Please create it first.')

            mspec = importlib.util.spec_from_file_location(
                name=name,
                location=location,
            )
            if mspec and mspec.loader:
                module = importlib.util.module_from_spec(mspec)
                mspec.loader.exec_module(module)
                sys.modules[name] = module


def build_image(
    input_path: str | Sequence[str],
    output_path: str | None = None,
    *,
    format: Literal["png", "webp", "jpg", "pdf"] | None = None,
    styles_path: str | None = None,
    utils_path: str | None = None,
    grid: bool = False,
    disable_auto_clear: bool = False,
    enable_auto_initialize: bool = False,
    no_cache: bool = False,
) -> list[str]:
    """Execute one or more Python drawing scripts or directories to generate images.

    Args:
        input_path (str | Sequence[str]): Target Python file(s) or directories.
        output_path (str | None): Output image file path or output directory path.
        format (Literal["png", "webp", "jpg", "pdf"] | None): Image format override ('png', 'webp', 'jpg', 'pdf').
        styles_path (str | None): Optional path to Python styles script.
        utils_path (str | None): Optional path to Python utils script.
        grid (bool): Whether to save companion *_grid.<ext> images with coordinate grid overlaid.
        disable_auto_clear (bool): Disable clearing canvas per executing drawing code file.
        enable_auto_initialize (bool): Enable full canvas re-initialization per executing drawing code file.
        no_cache (bool): If True, disable reading/writing the SQLite build image cache.

    Returns:
        list[str]: List of executed target paths.

    Raises:
        ValueError: If no valid target files or directories are provided.
    """
    if not input_path:
        raise ValueError("No input files or directories specified for build_image.")
    raw_targets: list[str] = [input_path] if isinstance(input_path, str) else list(input_path)

    first_target = os.path.abspath(raw_targets[0])
    search_dir = first_target if os.path.isdir(first_target) else os.path.dirname(first_target)
    styles_abs, utils_abs = resolve_styles_and_utils(search_dir, styles_path, utils_path)

    target_list, output_dir, output_file = _normalize_build_inputs_and_output(raw_targets, output_path)
    exec_mode = _resolve_execution_mode(disable_auto_clear, enable_auto_initialize)
    target_roots = [os.path.abspath(t) for t in target_list if os.path.isdir(t)]
    executer = DrawlibExecuter(
        mode=exec_mode,
        styles_path=styles_abs,
        utils_path=utils_abs,
        output_dir=output_dir,
        output_file=output_file,
        image_format=format,
        grid=grid,
        no_cache=no_cache,
        target_roots=target_roots,
    )

    resolved_targets, all_py_files, all_md_files = _collect_target_files(target_list, executer)
    executer.set_target_roots([t for t in resolved_targets if os.path.isdir(t)])
    if len(all_py_files) > 1:
        common = os.path.commonpath(all_py_files)
        base_root = common if os.path.isdir(common) else os.path.dirname(common)
        all_disp = ["/" + os.path.relpath(fp, base_root).replace(os.sep, "/") for fp in all_py_files]
        executer._check_duplicate_outputs(all_py_files, all_disp)

    executed: list[str] = []
    if all_py_files:
        for realpath in resolved_targets:
            if realpath in all_py_files or os.path.isdir(realpath):
                executer.execute(realpath)
                executed.append(realpath)

    if all_md_files:
        from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor

        out_img_dir = os.path.abspath(
            output_dir
            or (
                os.path.join(resolved_targets[0], "images")
                if os.path.isdir(resolved_targets[0])
                else os.path.join(os.path.dirname(resolved_targets[0]), "images")
            )
        )
        os.makedirs(out_img_dir, exist_ok=True)
        root_target_dir = (
            resolved_targets[0] if (len(resolved_targets) == 1 and os.path.isdir(resolved_targets[0])) else None
        )
        processor = DrawlibBlockProcessor(
            styles_path=styles_abs,
            utils_path=utils_abs,
            no_cache=no_cache,
            require_file=False,
            project_root=root_target_dir,
        )
        md_pattern = re.compile(r"(?:^|\n)[ \t]*```drawlib\b", re.IGNORECASE)
        orig_cwd = os.getcwd()
        try:
            if root_target_dir:
                os.chdir(root_target_dir)
            for md_file in all_md_files:
                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()
                except OSError:
                    continue

                if not md_pattern.search(content):
                    continue

                os.chdir(os.path.dirname(md_file))
                if root_target_dir:
                    rel_md = os.path.relpath(md_file, root_target_dir)
                    stem = os.path.splitext(rel_md)[0].replace(os.sep, "/")
                else:
                    stem = os.path.splitext(os.path.basename(md_file))[0]
                fmt = str(format or "png")
                processor.process_markdown(
                    markdown_text=content,
                    doc_base_name=stem,
                    output_dir=out_img_dir,
                    image_format=fmt,
                    source_filename=md_file,
                )
                if md_file not in executed:
                    executed.append(md_file)
        finally:
            os.chdir(orig_cwd)

    if not executed:
        raise ValueError("No valid Python files or Markdown files with drawing code were executed.")

    return executed


__all__ = [
    "DrawlibExecuter",
    "_SaveCallVisitor",
    "_collect_target_files",
    "_extract_single_static_save",
    "_get_python_files",
    "_has_local_imports",
    "_is_save_call_node",
    "_normalize_build_inputs_and_output",
    "_parse_static_save_call",
    "_resolve_execution_mode",
    "build_image",
    "check_duplicate_script_outputs",
    "resolve_effective_output_dir",
    "resolve_static_save_target",
]
