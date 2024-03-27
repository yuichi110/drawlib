"""write docstring later"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=global-statement

import os
from typing import Set, List, Final
import importlib.util
import traceback
import sys

from drawlib._logging import logger
from drawlib._util import (
    error_handler,
    get_script_relative_path,
)
from drawlib._canvas import clear

__INDENT_SIZE: Final[int] = 4

# store which dynamic modules are loaded
# for avoiding execute twice
__run_executed_files: Set[str] = set()

# run method can be called recursively
# on that time, 2nd has 4 indent, 3rd has 8 indent ...
__stack_of_run: int = 0


@error_handler
def run(file_or_directory: str, auto_clear: bool = True) -> None:
    """write docstring later"""
    global __stack_of_run

    path = get_script_relative_path(file_or_directory)
    if not os.path.exists(path):
        raise ValueError(f'"{path}" does not exist')

    # single python file.
    if os.path.isfile(path):
        if not path.endswith(".py"):
            raise ValueError(f'Unable to run "{path}"')
        __stack_of_run += 1
        indent = ' ' * (__stack_of_run - 1) * __INDENT_SIZE
        logger.info(f"{indent}---")
        logger.info(f"{indent}Execute file")
        _exec_module(path, auto_clear)
        logger.info(f'{indent}End')
        logger.info(f"{indent}---")
        __stack_of_run -= 1
        return

    # directory
    __stack_of_run += 1
    indent = ' ' * (__stack_of_run - 1) * __INDENT_SIZE
    logger.info(f"{indent}---")
    logger.info(f'{indent}Execute files under: {path}')
    file_paths = _get_python_files(path)
    for file_path in file_paths:
        _exec_module(file_path, auto_clear)
    logger.info(f'{indent}End')
    logger.info(f"{indent}---")
    __stack_of_run -= 1


###############
### private ###
###############


def _get_python_files(directory: str) -> List[str]:
    python_files: List[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)

    return sorted(python_files, key=lambda path: path.count(os.sep))


def _exec_module(file_path: str, auto_clear: bool) -> None:
    """write docstring later"""

    # run only 1 time.
    # don't move .add() to bottom. It makes loop
    if file_path in __run_executed_files:
        return
    __run_executed_files.add(file_path)

    mspec = importlib.util.spec_from_file_location(
        name="dynamically_loaded_module",
        location=file_path,
    )
    if mspec is None:
        # need to investigate what situation
        return
    module = importlib.util.module_from_spec(mspec)

    try:
        if auto_clear:
            # clear previous module's drawing status
            clear()

        # call module for drawing
        indent = ' ' * (__stack_of_run - 1) * __INDENT_SIZE
        logger.info(f"{indent} - {file_path}")
        mspec.loader.exec_module(module)  # type: ignore[union-attr]
    except Exception as e:  # pylint: disable=broad-exception-caught
        file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
        logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
        logger.critical(str(e))
        logger.debug("")
        logger.debug(traceback.format_exc())
        sys.exit(1)
