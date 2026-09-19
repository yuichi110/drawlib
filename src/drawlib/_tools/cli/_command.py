# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
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
from drawlib._core.l1_core import (
    dutil_settings,
    get_script_relative_path,
    guarded,
    logger,
)
from drawlib._core.l3_external import purge_font_cache
from drawlib._core.l4_canvas import clear
from drawlib._tools.doc_builder import (
    build_document,
    export_default_template,
    validate_template,
)
from drawlib._tools.http_server import run_server
from drawlib._utils import dutil_canvas


def call_command() -> None:
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
        logger.critical(f"software={drawlib.LIB_VERSION}")
        logger.critical(f"api={drawlib.LIB_VERSION}")
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

    # handle build subcommand
    if argparser.is_build_command():
        build_args = argparser.get_build_args()
        try:
            out_file = build_document(
                input_path=build_args.input,
                output_path=build_args.output,
                output_format=build_args.format,
                image_format=build_args.image_format,
                css_mode=build_args.css_mode,
                config_path=build_args.config,
                css_path=build_args.css,
                template_path=build_args.template,
            )
            print(f"Successfully compiled document(s): {out_file}")
            sys.exit(0)
        except Exception as e:
            print(f"Build Error: {e}", file=sys.stderr)
            if logging_mode in {"verbose", "developer"}:
                traceback.print_exc()
            sys.exit(1)

    # handle serve subcommand
    if argparser.is_serve_command():
        serve_args = argparser.get_serve_args()
        try:
            run_server(
                directory=serve_args.directory,
                port=serve_args.port,
                open_browser=not serve_args.no_browser,
            )
            sys.exit(0)
        except Exception as e:
            print(f"Serve Error: {e}", file=sys.stderr)
            if logging_mode in {"verbose", "developer"}:
                traceback.print_exc()
            sys.exit(1)

    # handle template subcommand
    if argparser.is_template_command():
        template_args = argparser.get_template_args()
        action = template_args.template_action
        try:
            if action == "export":
                out_file = export_default_template(template_args.output)
                print(f"Successfully exported default template to: {out_file}")
                sys.exit(0)
            elif action == "validate":
                is_valid, msgs = validate_template(template_args.template_file)
                for msg in msgs:
                    print(msg)
                sys.exit(0 if is_valid else 1)
            else:
                print(f"Template Error: Unknown action '{action}'", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"Template Error: {e}", file=sys.stderr)
            if logging_mode in {"verbose", "developer"}:
                traceback.print_exc()
            sys.exit(1)

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
        main_parser = argparse.ArgumentParser(
            description="Ilustration as code by python",
        )

        # main
        main_parser.add_argument(
            "file_or_directory",
            nargs="*",
            help="Target python file or directory which contains python codes",
        )

        # special mode options
        main_parser.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Show version.",
        )
        main_parser.add_argument(
            "--purge_font_cache",
            action="store_true",
            help="Purge cached font files.",
        )

        # exec mode options
        main_parser.add_argument(
            "--disable_auto_clear",
            action="store_true",
            help="Disable clearing canvas per executing drawing code files.",
        )
        main_parser.add_argument(
            "--enable_auto_initialize",
            action="store_true",
            help="Enable initializing theme/canvas/image_cache per executing drawing code files.",
        )

        # log options
        main_parser.add_argument(
            "--quiet",
            action="store_true",
            help="Enable quiet logging. show only error messages",
        )
        main_parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose logging.",
        )
        main_parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable verbose logging. Equivalent to --verbose",
        )
        main_parser.add_argument(
            "--developer",
            action="store_true",
            help=("Enable verbose logging. Disable error handling which is designed for library users."),
        )

        # build subcommand parser
        build_parser = argparse.ArgumentParser(
            prog="drawlib build",
            description="Compile Markdown or HTML document containing drawlib code blocks.",
        )
        build_parser.add_argument(
            "input",
            help="Input Markdown (.md) or HTML (.html) file path or directory path.",
        )
        build_parser.add_argument(
            "-o",
            "--output",
            help="Output file path (e.g. output.html, output.pdf, output.rendered.md).",
        )
        build_parser.add_argument(
            "-f",
            "--format",
            choices=["html", "pdf", "markdown"],
            help="Output format: html, pdf, or markdown.",
        )
        build_parser.add_argument(
            "--image-format",
            choices=["png", "svg", "inline_svg"],
            default="png",
            help="Image output format for drawlib code blocks: png, svg, or inline_svg (default: png).",
        )
        build_parser.add_argument(
            "--css-mode",
            choices=["auto", "embed", "external"],
            default="auto",
            help="CSS styling mode for HTML documents: auto, embed, or external (default: auto).",
        )
        build_parser.add_argument(
            "--config",
            help="Path to Python config/setup script (e.g. config.py).",
        )
        build_parser.add_argument(
            "--css",
            help="Path to custom CSS file for HTML styling.",
        )
        build_parser.add_argument(
            "-t",
            "--template",
            help="Path to custom Jinja2 HTML template file.",
        )

        # serve subcommand parser
        serve_parser = argparse.ArgumentParser(
            prog="drawlib serve",
            description="Start a local HTTP server to preview documentation.",
        )
        serve_parser.add_argument(
            "directory",
            nargs="?",
            default=None,
            help="Directory to serve (default: auto-detect docs/html, docs, or current directory).",
        )
        serve_parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=8000,
            help="Port to run the HTTP server on (default: 8000).",
        )
        serve_parser.add_argument(
            "--no-browser",
            action="store_true",
            help="Do not open browser automatically.",
        )

        # template subcommand parser
        template_parser = argparse.ArgumentParser(
            prog="drawlib template",
            description="Manage Jinja2 HTML templates for drawlib document compilation.",
        )
        template_subparsers = template_parser.add_subparsers(dest="template_action", required=True)

        export_parser = template_subparsers.add_parser(
            "export",
            help="Export built-in default HTML template to a file.",
        )
        export_parser.add_argument(
            "output",
            nargs="?",
            default="template.html.j2",
            help="Output file path (default: template.html.j2).",
        )

        validate_parser = template_subparsers.add_parser(
            "validate",
            help="Validate a Jinja2 template file for syntax and required placeholders.",
        )
        validate_parser.add_argument(
            "template_file",
            help="Path to Jinja2 template file to validate.",
        )

        self._main_parser = main_parser
        self._build_parser = build_parser
        self._serve_parser = serve_parser
        self._template_parser = template_parser
        self._is_build = False
        self._is_serve = False
        self._is_template = False
        self._build_args: Optional[argparse.Namespace] = None
        self._serve_args: Optional[argparse.Namespace] = None
        self._template_args: Optional[argparse.Namespace] = None
        self._positional_args: Optional[List[str]] = None
        self._name_args: Optional[argparse.Namespace] = None

    def parse(self) -> None:
        """Parse command line options."""
        if "build" in sys.argv[1:]:
            idx = sys.argv.index("build")
            self._is_build = True
            self._is_serve = False
            self._is_template = False
            global_args, _ = self._main_parser.parse_known_args(sys.argv[1:idx])
            self._name_args = global_args
            self._build_args = self._build_parser.parse_args(sys.argv[idx + 1 :])
        elif "serve" in sys.argv[1:]:
            idx = sys.argv.index("serve")
            self._is_build = False
            self._is_serve = True
            self._is_template = False
            global_args, _ = self._main_parser.parse_known_args(sys.argv[1:idx])
            self._name_args = global_args
            self._serve_args = self._serve_parser.parse_args(sys.argv[idx + 1 :])
        elif "template" in sys.argv[1:]:
            idx = sys.argv.index("template")
            self._is_build = False
            self._is_serve = False
            self._is_template = True
            global_args, _ = self._main_parser.parse_known_args(sys.argv[1:idx])
            self._name_args = global_args
            self._template_args = self._template_parser.parse_args(sys.argv[idx + 1 :])
        else:
            self._is_build = False
            self._is_serve = False
            self._is_template = False
            args = self._main_parser.parse_args()
            self._name_args = args
            self._positional_args = args.file_or_directory

    def is_build_command(self) -> bool:
        """Check if build subcommand was called."""
        if not self._is_build and self._name_args is None and self._build_args is None:
            self.parse()
        return self._is_build

    def get_build_args(self) -> argparse.Namespace:
        """Get parsed arguments for build subcommand."""
        if self._build_args is None:
            self.parse()
        if self._build_args is None:
            raise ValueError("Not a build command")
        return self._build_args

    def is_serve_command(self) -> bool:
        """Check if serve subcommand was called."""
        if not self._is_serve and self._name_args is None and self._serve_args is None:
            self.parse()
        return self._is_serve

    def get_serve_args(self) -> argparse.Namespace:
        """Get parsed arguments for serve subcommand."""
        if self._serve_args is None:
            self.parse()
        if self._serve_args is None:
            raise ValueError("Not a serve command")
        return self._serve_args

    def is_template_command(self) -> bool:
        """Check if template subcommand was called."""
        if not self._is_template and self._name_args is None and self._template_args is None:
            self.parse()
        return self._is_template

    def get_template_args(self) -> argparse.Namespace:
        """Get parsed arguments for template subcommand."""
        if self._template_args is None:
            self.parse()
        if self._template_args is None:
            raise ValueError("Not a template command")
        return self._template_args

    def is_show_version(self) -> bool:
        """Check if the version option is specified.

        Checks whether the command line options include `-v` or `--version`.
        If either option is present, it returns True; otherwise, False.

        Returns:
            bool: True if version option is specified, False otherwise.

        """
        if self._is_build or self._is_serve or self._is_template:
            return False
        if self._name_args is None:
            self.parse()
        return bool(self._name_args and self._name_args.version)

    def is_purge_font_cache(self) -> bool:
        """Check if the purge font cache option is specified.

        Checks whether the command line options include `--purge_font_cache`.
        If the option is present, it returns True; otherwise, False.

        Returns:
            bool: True if purge font cache option is specified, False otherwise.

        """
        if self._is_build or self._is_serve or self._is_template:
            return False
        if self._name_args is None:
            self.parse()
        return bool(self._name_args and self._name_args.purge_font_cache)

    def get_logging_mode(self) -> Literal["quiet", "normal", "verbose", "developer"]:
        """Retrieve the logging mode based on command line options.

        Checks the command line options for logging-related flags:
        - `--quiet`: Returns "quiet" logging mode.
        - `--verbose` or `--debug`: Returns "verbose" logging mode.
        - `--developer`: Returns "developer" logging mode.

        Returns:
            Literal["quiet", "normal", "verbose", "developer"]: Logging mode.

        Raises:
            ValueError: If conflicting logging options are specified.
        """
        if self._is_build or self._is_serve or self._is_template:
            return "normal"
        if self._name_args is None:
            raise ValueError("Parsed arguments unavailable.")

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

    @guarded
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
                dutil_canvas.initialize()
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
