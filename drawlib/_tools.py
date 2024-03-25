import os
from typing import Set, List
import importlib.util
import traceback
import sys

from drawlib._logging import logger
from drawlib._util import (
    error_handler,
    get_script_relative_path,
)
from drawlib._canvas import clear


# escape original help
__help = help

# store which dynamic modules are loaded
# for avoiding execute twice
__run_executed_files: Set[str] = set()

__stack_of_run = 0
__indent_size = 4


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
        indent = ' ' * (__stack_of_run - 1) * __indent_size
        logger.info(f"{indent}---")
        logger.info(f"{indent}Execute file")
        _exec_module(path, auto_clear)
        logger.info(f'{indent}End')
        logger.info(f"{indent}---")
        __stack_of_run -= 1
        return

    # directory
    __stack_of_run += 1
    indent = ' ' * (__stack_of_run - 1) * __indent_size
    logger.info(f"{indent}---")
    logger.info(f'{indent}Execute files under: {path}')
    file_paths = _get_python_files(path)
    for file_path in file_paths:
        _exec_module(file_path, auto_clear)
    logger.info(f'{indent}End')
    logger.info(f"{indent}---")
    __stack_of_run -= 1


@error_handler
def help(object, open_webdoc=True) -> None:
    """getting help of drawlib
    - function
    - class
    """

    # get module objects
    module_name = (lambda x: x).__module__
    module = sys.modules[module_name]
    module_objects = set()
    g = globals()
    for object_name in dir(module):
        if object_name.startswith("_"):
            continue
        if object_name == "help":
            continue
        module_objects.add(g[object_name])

    # show document
    if object in module_objects:
        print(object.__doc__)
    else:
        __help(object)


###############
### private ###
###############


def _get_python_files(directory: str) -> List[str]:
    python_files: List[str] = []
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a .py extension
            if file.endswith('.py'):
                # Get the absolute path of the Python file
                file_path = os.path.join(root, file)
                # Append the file path to the list
                python_files.append(file_path)

    return sorted(python_files, key=lambda path: path.count(os.sep))


def _exec_module(file_path: str, auto_clear: bool) -> None:
    """write docstring later"""
    global __stack_of_run

    # run only 1 time.
    # don't move add() to bottom for avoiding loop
    if file_path in __run_executed_files:
        return
    __run_executed_files.add(file_path)

    mspec = importlib.util.spec_from_file_location(
        name="t",
        location=file_path,
    )
    module = importlib.util.module_from_spec(mspec)

    try:
        if auto_clear:
            # clear previous module's drawing status
            clear()

        # call module for drawing
        indent = ' ' * (__stack_of_run - 1) * __indent_size
        logger.info(f"{indent} - {file_path}")
        mspec.loader.exec_module(module)
    except Exception as e:
        file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
        logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
        logger.critical(str(e))
        logger.debug("")
        logger.debug(traceback.format_exc())
        sys.exit(1)
