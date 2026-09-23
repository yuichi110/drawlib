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

import importlib.util
import os
import runpy
import sys
import traceback
from typing import Any, Callable, List, Literal, Optional, Sequence, Tuple, Union

import drawlib._core.l4_canvas._canvas
import drawlib.canvas
from drawlib._core.l1_core import (
    dutil_settings,
    get_script_relative_path,
    guarded,
    logger,
)
from drawlib._core.l4_canvas import clear
from drawlib._utils import dutil_canvas


class DrawlibExecuter:
    """Executor for running Python files or directories containing drawing code.

    Executes Python files specified as targets or recursively runs all Python files
    within a specified directory. Handles logging, module loading, and error handling.
    """

    def __init__(
        self,
        mode: Literal["none", "auto_clear", "auto_initialize"] = "auto_clear",
        config_path: Optional[str] = None,
        output_dir: Optional[str] = None,
        output_file: Optional[str] = None,
        image_format: Optional[Literal["png", "webp", "jpg", "pdf"]] = None,
        grid: bool = False,
    ) -> None:
        """Initialize a DrawlibExecuter instance.

        Args:
            mode (Literal["none", "auto_clear", "auto_initialize"]):
                The execution mode for handling Python file execution:
                - "none": Executes Python files without clearing canvas between executions.
                - "auto_clear": Automatically clears the canvas between executing each Python file.
                - "auto_initialize": Automatically initializes canvas per execution.
            config_path (Optional[str]): Optional path to Python config script.
            output_dir (Optional[str]): Optional path to directory where images should be saved.
            output_file (Optional[str]): Optional explicit output file path when executing a single script.
            image_format (Optional[Literal["png", "webp", "jpg", "pdf"]]): Optional image format override.
            grid (bool): Whether to generate coordinate grid overlaid images in addition to normal images.

        Raises:
            ValueError: If mode is not one of ["none", "auto_clear", "auto_initialize"].
        """
        if mode not in {"none", "auto_clear", "auto_initialize"}:
            raise ValueError(f'Arg mode is "{mode}". But it must be one of ["none", "auto_clear", "auto_initialize"].')
        self._mode = mode
        self._config_path = config_path
        self._output_dir = output_dir
        self._output_file = output_file
        self._image_format: Optional[Literal["png", "webp", "jpg", "pdf"]] = image_format
        self._grid = grid
        self._topdir_path: str = ""

    def _create_wrapped_save(
        self,
        orig_canvas_save: Callable[..., None],
    ) -> Callable[..., None]:
        """Create a wrapped save function that applies output file and format overrides."""

        def _wrapped_save(
            file: Optional[str] = None,
            format: Optional[Literal["png", "webp", "jpg", "pdf"]] = None,
        ) -> None:
            eff_format: Optional[Literal["png", "webp", "jpg", "pdf"]] = (
                self._image_format if self._image_format else format
            )
            if self._output_file is not None:
                target = os.path.abspath(self._output_file)
                if eff_format:
                    stem, _ = os.path.splitext(target)
                    target = f"{stem}.{eff_format}"
                orig_canvas_save(file=target, format=eff_format)
            elif file is not None and eff_format:
                stem, _ = os.path.splitext(file)
                orig_canvas_save(file=f"{stem}.{eff_format}", format=eff_format)
            else:
                orig_canvas_save(file=file, format=eff_format)

        return _wrapped_save

    def _execute_target_path(self, path: str) -> None:
        """Execute a resolved Python file or directory path."""
        self._add_topdir_to_syspath(path)
        logger.info("Execute python files")
        if os.path.isfile(path):
            if not path.endswith(".py"):
                raise ValueError(f'Unable to run "{path}"')
            self._exec_module(path)
            return

        file_paths = self._get_python_files(path)
        for file_path in file_paths:
            if not os.path.basename(file_path).startswith("__"):
                self._exec_module(file_path)

    @guarded
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

        canvas_inst = drawlib._core.l4_canvas._canvas.canvas
        orig_canvas_save = canvas_inst.save
        orig_core_save = drawlib._core.l4_canvas._canvas.save
        orig_canvas_mod_save = getattr(drawlib.canvas, "save", None)
        need_save_override = bool(self._output_file or self._image_format)

        try:
            if need_save_override:
                wrapped = self._create_wrapped_save(orig_canvas_save)
                canvas_inst.save = wrapped  # ty: ignore
                drawlib._core.l4_canvas._canvas.save = wrapped  # ty: ignore
                drawlib.canvas.save = wrapped  # ty: ignore

            path = get_script_relative_path(file_or_directory)
            if not os.path.exists(path):
                raise ValueError(f'"{path}" does not exist')

            self._execute_target_path(path)
        finally:
            if need_save_override:
                canvas_inst.save = orig_canvas_save  # ty: ignore
                drawlib._core.l4_canvas._canvas.save = orig_core_save  # type: ignore[assignment]
                if orig_canvas_mod_save is not None:
                    drawlib.canvas.save = orig_canvas_mod_save  # type: ignore[assignment]
            if self._grid:
                dutil_settings.set_force_grid(False)
            if self._output_dir is not None:
                dutil_settings.set_output_dir(None)

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
    def _get_python_files(directory: str) -> List[str]:
        """Retrieve all Python files recursively within the specified directory."""
        python_files: List[str] = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        def sort_key(path: str) -> Tuple[int, str]:
            return (path.count(os.sep), path)

        return sorted(python_files, key=sort_key)

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
        """Reset/initialize canvas and apply optional config script before module execution."""
        if self._mode == "auto_clear":
            clear()
        elif self._mode == "auto_initialize":
            dutil_canvas.initialize()

        if self._config_path:
            self._exec_config(self._config_path)

    def _exec_module(self, file_path: str) -> None:
        """Execute the specified Python module file."""
        if self._is_module_loaded(file_path):
            logger.info(f"    - {file_path}")
            return

        name = self._resolve_module_name(file_path)
        mspec = importlib.util.spec_from_file_location(
            name=name,
            location=file_path,
        )
        if mspec is None or mspec.loader is None:
            logger.info(f"    - {file_path} : skipped with unknown reason.")
            return
        module = importlib.util.module_from_spec(mspec)

        try:
            self._prepare_canvas_for_module()
            logger.info(f"    - {file_path}")
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
    def _exec_config(config_path: str) -> None:
        """Execute external config script before running drawing code."""
        abs_config = os.path.abspath(config_path)
        if not os.path.exists(abs_config):
            raise FileNotFoundError(f'Config file "{abs_config}" does not exist.')
        config_dir = os.path.dirname(abs_config)
        if config_dir not in sys.path:
            sys.path.insert(0, config_dir)

        runpy.run_path(abs_config, run_name="__drawlib_config__")

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

    def _get_package_words(self, file_path: str) -> List[str]:
        """Retrieve the package words from the specified file path relative to the top directory."""
        last_path = file_path.replace(self._topdir_path, "")
        words = last_path.split(os.sep)
        if words[0] == "":
            words = words[1:]
        return words

    def _load_parent_modules(self, words: List[str]) -> None:
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
    inputs: Union[str, Sequence[str]],
    output: Optional[str] = None,
    format: Optional[Literal["png", "webp", "jpg", "pdf"]] = None,
    config: Optional[str] = None,
    grid: bool = False,
    disable_auto_clear: bool = False,
    enable_auto_initialize: bool = False,
) -> List[str]:
    """Execute one or more Python drawing scripts or directories to generate images.

    Args:
        inputs (Union[str, Sequence[str]]): One or more target Python files (.py) or directories.
        output (Optional[str]): Output image file path (for single script) or output directory path.
        format (Optional[Literal["png", "webp", "jpg", "pdf"]]): Image format override ('png', 'webp', 'jpg', 'pdf').
        config (Optional[str]): Optional path to Python config/setup script.
        grid (bool): Whether to save companion *_grid.<ext> images with coordinate grid overlaid.
        disable_auto_clear (bool): Disable clearing canvas per executing drawing code file.
        enable_auto_initialize (bool): Enable full canvas re-initialization per executing drawing code file.

    Returns:
        List[str]: List of executed target paths.

    Raises:
        ValueError: If no valid target files or directories are provided.
    """
    target_list: List[str] = [inputs] if isinstance(inputs, str) else list(inputs)
    if not target_list:
        raise ValueError("No input files or directories specified for build_image.")

    exec_mode: Literal["none", "auto_clear", "auto_initialize"] = "auto_clear"
    if disable_auto_clear:
        exec_mode = "none"
    elif enable_auto_initialize:
        exec_mode = "auto_initialize"

    output_dir: Optional[str] = None
    output_file: Optional[str] = None
    if output:
        ext = os.path.splitext(output)[1].lower()
        is_single_file = len(target_list) == 1 and os.path.isfile(target_list[0])
        if is_single_file and ext in {".png", ".webp", ".jpg", ".jpeg", ".pdf"} and not os.path.isdir(output):
            output_file = output
        else:
            output_dir = output

    executer = DrawlibExecuter(
        mode=exec_mode,
        config_path=config,
        output_dir=output_dir,
        output_file=output_file,
        image_format=format,
        grid=grid,
    )

    executed: List[str] = []
    for target_file in target_list:
        if not os.path.isfile(target_file) and not os.path.isdir(target_file):
            msg = f'ignore arg "{target_file}" since it is not a file/dir path'
            logger.warning(msg)
            continue

        abspath = os.path.abspath(target_file)
        realpath = os.path.realpath(abspath)
        executer.execute(realpath)
        executed.append(realpath)

    if not executed:
        raise ValueError("No valid Python files or directories were executed.")

    return executed
