# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# type: ignore

"""Implementation of drawlib command."""

import argparse
import importlib.util
import os
import sys
import traceback
from typing import List, Literal, Optional, Tuple

import drawlib
import drawlib.v0_1
from drawlib.v0_1.private.core_canvas.canvas import clear
from drawlib.v0_1.private.dutil.dutil_canvas import initialize
from drawlib.v0_1.private.dutil.settings import dutil_settings
from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.util import (
    error_handler,
    get_script_relative_path,
    purge_font_cache,
)


def call() -> None:
    """Handle drawlib command execution.

    This function serves as the entry point for executing drawlib commands.
    It parses command-line arguments, processes options like showing version info
    or purging font cache, sets logging levels, retrieves target files and directories,
    and executes each target file using the DrawlibExecuter.

    Raises:
        ValueError: If an invalid logging mode is specified.
    """
    argparser = DrawlibArgParser()
    argparser.parse()

    # show version
    if argparser.is_show_version():
        logger.critical(f"software={drawlib.VERSION}")
        logger.critical(f"api={drawlib.v0_1.VERSION}")
        sys.exit(0)

    # purge font cache
    if argparser.is_purge_font_cache():
        purge_font_cache()
        sys.exit(0)

    # set logging mode
    logging_mode = argparser.get_logging_mode()
    if logging_mode == "quiet":
        dutil_settings.set_logging_mode("quiet")
    elif logging_mode == "normal":
        dutil_settings.set_logging_mode("normal")
    elif logging_mode == "verbose":
        dutil_settings.set_logging_mode("verbose")
    elif logging_mode == "developer":
        dutil_settings.set_logging_mode("developer")
    else:
        raise ValueError()

    # get execution mode
    exec_mode = argparser.get_exec_mode()

    # get target files and directories
    target_files = argparser.get_target_files()

    # if no target, quit with error code
    if len(target_files) == 0:
        logger.critical("no input files and directories")
        logger.critical('check options with "drawlib --help"')
        sys.exit(1)

    # handle target one by one.
    for target_file in target_files:
        # skip wrong file
        if not os.path.isfile(target_file) and not os.path.isdir(target_file):
            msg = f'ignore arg "{target_file}" since it is not a file/dir path'
            logger.warning(msg)
            continue

        # get file path
        abspath = os.path.abspath(target_file)
        realpath = os.path.realpath(abspath)

        # execute file or directory
        executer = DrawlibExecuter(mode=exec_mode)
        executer.execute(realpath)


class DrawlibArgParser:
    """Command-line argument parser for drawlib.

    Parses command-line options related to drawlib execution, such as target files,
    version display, font cache purging, logging modes, and execution modes.
    """

    def __init__(self) -> None:
        """
        Initializes a DrawlibArgParser instance.

        In this method, an ArgumentParser instance is created to define command line options
        for drawlib execution related parameters such as target files, version display, font cache purging,
        logging modes, and execution modes.

        Returns:
            None
        """
        parser = argparse.ArgumentParser(
            description="Ilustration as code by python",
        )

        # main
        parser.add_argument(
            "file_or_directory",
            nargs="...",
            help="Target python file or directory which contains python codes",
        )

        # special mode options
        parser.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Show version.",
        )
        parser.add_argument(
            "--purge_font_cache",
            action="store_true",
            help="Purge cached font files.",
        )

        # exec mode options
        parser.add_argument(
            "--disable_auto_clear",
            action="store_true",
            help="Disable clearing canvas per executing drawing code files.",
        )
        parser.add_argument(
            "--enable_auto_initialize",
            action="store_true",
            help="Enable initializing theme/canvas/image_cache per executing drawing code files.",
        )

        # log options
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Enable quiet logging. show only error messages",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose logging.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable verbose logging. Equivalent to --verbose",
        )
        parser.add_argument(
            "--developer",
            action="store_true",
            help=("Enable verbose logging. Disable error handling which is designed for library users."),
        )

        self._parser = parser
        self._positional_args: Optional[List[str]] = None
        self._name_args: Optional[argparse.Namespace] = None

    def parse(self) -> None:
        """Parse command line options.

        Parses command line options using the ArgumentParser instance.
        It separates special options from main positional arguments and stores them internally.

        This method must be called before calling any other methods that retrieve parsed options.

        Returns:
            None
        """
        # special options
        self._name_args, _ = self._parser.parse_known_args()

        # main option
        args = self._parser.parse_args()
        self._positional_args = args.file_or_directory

    def is_show_version(self) -> bool:
        """Check if the version option is specified.

        Checks whether the command line options include `-v` or `--version`.
        If either option is present, it returns True; otherwise, False.

        Returns:
            bool: True if version option is specified, False otherwise.

        """
        if self._name_args is None:
            self.parse()

        return self._name_args.version

    def is_purge_font_cache(self) -> bool:
        """Check if the purge font cache option is specified.

        Checks whether the command line options include `--purge_font_cache`.
        If the option is present, it returns True; otherwise, False.

        Returns:
            bool: True if purge font cache option is specified, False otherwise.

        """
        if self._name_args is None:
            self.parse()

        return self._name_args.purge_font_cache

    def get_logging_mode(self) -> Literal["quiet", "normal", "verbose", "developer"]:
        """Retrieve the logging mode based on command line options.

        Checks the command line options for logging-related flags:
        - `--quiet`: Returns "quiet" logging mode.
        - `--verbose` or `--debug`: Returns "verbose" logging mode.
        - `--developer`: Returns "developer" logging mode.

        Raises:
            ValueError: If conflicting logging options are specified.

        Returns:
            Literal["quiet", "normal", "verbose", "developer"]: Logging mode.
        """
        if self._name_args is None:
            self.parse()

        if self._name_args.quiet and (self._name_args.verbose or self._name_args.developer):
            raise ValueError("option --quiet can't use with option --debug and --devdebug")

        if self._name_args.quiet:
            return "quiet"

        if self._name_args.verbose:
            return "verbose"

        if self._name_args.debug:
            return "verbose"

        if self._name_args.developer:
            return "developer"

        return "normal"

    def get_exec_mode(self) -> Literal["none", "auto_clear", "auto_initialize"]:
        """Retrieve the execution mode based on command line options.

        Checks the command line options for execution mode flags:
        - `--disable_auto_clear`: Returns "none" execution mode.
        - `--enable_auto_initialize`: Returns "auto_initialize" execution mode.

        Returns:
            Literal["none", "auto_clear", "auto_initialize"]: Execution mode.
        """
        if self._name_args is None:
            self.parse()

        if self._name_args.enable_auto_initialize:
            return "auto_initialize"

        if self._name_args.disable_auto_clear:
            return "none"

        return "auto_clear"

    def get_target_files(self) -> List[str]:
        """Retrieve positional arguments representing target files and directories.

        Retrieves the positional arguments passed to the drawlib command,
        which are intended as target files or directories for execution.

        Returns:
            List[str]: List of positional arguments (files and directories).
        """
        if self._positional_args is None:
            self.parse()

        return self._positional_args


class DrawlibExecuter:
    """Executor for running Python files or directories containing drawing code.

    Executes Python files specified as targets or recursively runs all Python files
    within a specified directory. Handles logging, module loading, and error handling.
    """

    def __init__(self, mode: Literal["none", "auto_clear", "auto_initialize"]) -> None:
        """Initializes a DrawlibExecuter instance with the specified mode.

        Args:
            mode (Literal["none", "auto_clear", "auto_initialize"]):
                The execution mode for handling Python file execution:
                - "none": Executes Python files without clearing canvas between executions.
                - "auto_clear": Automatically clears the canvas between executing each Python file.
                - "auto_initialize": Automatically initializes theme/canvas/image_cache per execution.

                Raises ValueError if mode is not one of ["none", "auto_clear", "auto_initialize"].

        Raises:
            ValueError: If mode is not one of ["none", "auto_clear", "auto_initialize"].
        """
        if mode not in {"none", "auto_clear", "auto_initialize"}:
            raise ValueError(f'Arg mode is "{mode}". But it must be one of ["none", "auto_clear", "auto_initialize"].')
        self._mode = mode
        self._topdir_path: str = ""

    @error_handler
    def execute(self, file_or_directory: str) -> None:
        """Execute the specified Python file or all Python files in the specified directory.

        Executes the Python file specified by `file_or_directory` or recursively executes all Python files
        found within the specified directory. Each Python file is executed only once.

        For directories, strongly recommend setting `auto_clear=True` to avoid shared canvas state
        between different Python files.

        Args:
            file_or_directory (str): Path to the Python file or directory containing Python files to execute.

        Returns:
            None

        Raises:
            ValueError: If the specified path `file_or_directory` does not exist.

        """
        path = get_script_relative_path(file_or_directory)
        if not os.path.exists(path):
            raise ValueError(f'"{path}" does not exist')

        self._add_topdir_to_syspath(path)

        logger.info("Execute python files")
        if os.path.isfile(path):
            if not path.endswith(".py"):
                raise ValueError(f'Unable to run "{path}"')
            self._exec_module(path)
        else:
            file_paths = self._get_python_files(path)
            for file_path in file_paths:
                self._exec_module(file_path)

    def _add_topdir_to_syspath(self, path: str) -> None:
        """Add the top directory of the specified path to the Python sys.path.

        Determines the top directory of the specified path (either file or directory) and adds it to
        the Python sys.path to enable module loading.

        Args:
            path (str): Path to the Python file or directory.

        Returns:
            None

        Raises:
            ValueError: If the specified directory does not have __init__.py, indicating it's not a valid package.

        """
        if os.path.isfile(path):
            topdir = os.path.dirname(path)
        else:
            init_path = os.path.join(path, "__init__.py")
            if not os.path.exists(init_path):
                logger.critical(f'Target directory "{path}" does not have __init__.py. Abort.')
                sys.exit(1)
            topdir = path

        package_dir = ""
        while os.path.exists(os.path.join(topdir, "__init__.py")):
            package_dir = topdir
            topdir = os.path.dirname(topdir)

        self._topdir_path = topdir
        logger.info(f'Detect package root "{package_dir}".')
        if topdir not in sys.path:
            sys.path.append(topdir)
            logger.info(f'    - Add parent directory of package root "{topdir}" to Python Path.')
        else:
            logger.info(f'    - Parent of package directory "{topdir}" is already in Python Path.')
        logger.info("")

    @staticmethod
    def _get_python_files(directory: str) -> List[str]:
        """Retrieve all Python files recursively within the specified directory.

        Recursively searches the specified directory for Python files (*.py) and returns a sorted list
        of their paths.

        Args:
            directory (str): Path to the directory to search for Python files.

        Returns:
            List[str]: Sorted list of paths to Python files found within the directory.
        """
        python_files: List[str] = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        def sort_key(path: str) -> Tuple[int, str]:
            # 1. depth
            # 2. alphabetical order
            return (path.count(os.sep), path)

        sorted_files = sorted(python_files, key=sort_key)
        return sorted_files

    def _exec_module(self, file_path: str) -> None:
        """Execute the specified Python module file.

        Loads and executes the Python module specified by `file_path`. It handles module loading,
        initialization (if specified by the execution mode), and error handling.

        Args:
            file_path (str): Path to the Python module file (.py) to execute.

        Returns:
            None
        """
        words = self._get_package_words(file_path)
        self._load_parent_modules(words)

        if self._is_module_loaded(file_path):
            logger.info(f"    - {file_path}")
            return

        # load module
        name = ".".join(words).replace(".py", "")
        mspec = importlib.util.spec_from_file_location(
            name=name,
            location=file_path,
        )
        if mspec is None:
            # need to investigate what situation make this
            logger.info(f"    - {file_path} : skipped with unknown reason.")
            return
        module = importlib.util.module_from_spec(mspec)

        # execute and cache
        try:
            if self._mode == "auto_clear":
                clear()
            elif self._mode == "auto_initialize":
                initialize()
            else:
                ...
            logger.info(f"    - {file_path}")
            mspec.loader.exec_module(module)  # type: ignore[union-attr]
            sys.modules[name] = module

        except Exception as e:
            # Please don't raise again.
            # Error handler can't detect exact error location of imported module
            file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
            logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
            logger.critical(str(e))
            logger.debug("")
            logger.debug(traceback.format_exc())
            sys.exit(1)

    @staticmethod
    def _is_module_loaded(module_path: str) -> bool:
        """Check if the specified module is already loaded.

        Checks if the module specified by `module_path` is already loaded in the Python environment.

        Args:
            module_path (str): Path to the Python module file to check.

        Returns:
            bool: True if the module is already loaded, False otherwise.
        """
        # Normalize the module path to ensure consistent comparison
        module_path = os.path.abspath(module_path)

        for _, module in sys.modules.items():
            if module is None:
                continue
            if not hasattr(module, "__file__"):
                continue
            if module.__file__ is None:
                continue

            loaded_module_path = os.path.abspath(module.__file__)
            if loaded_module_path == module_path:
                return True

        return False

    def _get_package_words(self, file_path: str) -> List[str]:
        """Retrieve the package words from the specified file path relative to the top directory.

        Determines the hierarchical package structure of the specified `file_path` relative to the
        top directory and returns a list of package words.

        Args:
            file_path (str): Path to the Python module file.

        Returns:
            List[str]: List of words representing the package structure.
        """
        last_path = file_path.replace(self._topdir_path, "")
        words = last_path.split(os.sep)
        if words[0] == "":
            words = words[1:]
        return words

    def _load_parent_modules(self, words: List[str]) -> None:
        """Load parent modules for the specified package words.

        Loads parent modules iteratively for the specified `words`, which represent the hierarchical
        package structure relative to the top directory.

        Args:
            words (List[str]): List of words representing the package structure.

        Returns:
            None

        Raises:
            ValueError: If any parent module directory does not have __init__.py, indicating it's not a valid package.
        """
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
            module = importlib.util.module_from_spec(mspec)
            mspec.loader.exec_module(module)
            sys.modules[name] = module
