import os
from typing import Set
import importlib.util
import traceback
import sys

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


@error_handler
def run(directory: str, auto_clear: bool = True):
    """write docstring later"""
    dir_path = get_script_relative_path(directory)
    if not os.path.exists(dir_path):
        raise ValueError(f'"{dir_path}" does not exist')

    def get_python_files(directory):
        python_files = []
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

    def exec_module(file_path):
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
            mspec.loader.exec_module(module)
        except Exception as e:
            file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
            print(f'{type(e).__name__} at file:"{file}", line:"{line}"')
            print(str(e))
            if "--debug" in sys.argv:
                print()
                print(traceback.format_exc())
            sys.exit(1)

    # single python file.
    if os.path.isfile(dir_path):
        file_path = dir_path
        if not file_path.endswith(".py"):
            raise ValueError(f'Unable to run "{file_path}"')
        exec_module(file_path)
        return

    # directory
    file_paths = get_python_files(dir_path)
    for file_path in file_paths:
        exec_module(file_path)


@error_handler
def help(object, open_webdoc=True):
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
