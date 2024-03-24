"""write docstring later"""

from typing import Set
import inspect
import math
import importlib.util

import functools
import traceback
import sys
import os


def error_handler(caller):
    """write docstring later"""

    if sys.argv[0].endswith("pytest") or "--devdebug" in sys.argv:
        # disable wrapper and get pure error message
        return caller

    @functools.wraps(caller)
    def wrapper(*args, **kwargs):
        try:
            return caller(*args, **kwargs)
        except Exception as e:

            def get_package_root_path():
                error_module = inspect.stack()[0].filename
                module_path = os.path.abspath(error_module)
                package_root = module_path
                while not os.path.exists(
                    os.path.join(package_root, "__init__.py"),
                ):
                    package_root = os.path.dirname(package_root)
                return package_root

            def is_path_under(parent_path, child_path):
                common_parent = os.path.commonpath([parent_path, child_path])
                abs_parent_path = os.path.abspath(parent_path)
                abs_common_path = os.path.abspath(common_parent)
                return abs_parent_path == abs_common_path

            package_root = get_package_root_path()
            for frame in inspect.stack():
                print(frame)
                file = frame.filename
                if is_path_under(package_root, file):
                    continue
                line = frame.lineno
                print(f'{type(e).__name__} at file:"{file}", line:"{line}"')
                print(str(e))
                if "--debug" in sys.argv:
                    print()
                    print(traceback.format_exc())
                break
            sys.exit(1)

    return wrapper


@error_handler
def get_angle(x1: float, y1: float, x2: float, y2: float) -> float:
    """write docstring later"""

    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


@error_handler
def get_user_script_path() -> str:
    def get_package_root_path():
        error_module = inspect.stack()[0].filename
        module_path = os.path.abspath(error_module)
        package_root = module_path
        while not os.path.exists(
            os.path.join(package_root, "__init__.py"),
        ):
            package_root = os.path.dirname(package_root)
        return package_root

    def is_path_under(parent_path, child_path):
        common_parent = os.path.commonpath([parent_path, child_path])
        abs_parent_path = os.path.abspath(parent_path)
        abs_common_path = os.path.abspath(common_parent)
        return abs_parent_path == abs_common_path

    package_root = get_package_root_path()
    script_path = ""

    # backtrack call stack and find user call point
    for frame in inspect.stack():
        file = frame.filename
        if file == "<string>":
            # filename becomes <string> when function is called by exec string
            continue
        if is_path_under(package_root, file):
            # file is drawlib library code. not users.
            continue

        # found user code file which calles this function.
        script_path = file
        break

    if script_path == "":
        message = "Critical Error. Unable to detect call script file"
        raise FileNotFoundError(message)

    return script_path


@error_handler
def get_script_relative_path(path: str) -> str:
    """write docstring later"""

    if os.path.isabs(path):
        return path

    script_path = get_user_script_path()
    script_parent_dir = os.path.dirname(script_path)
    merged_path = os.path.join(script_parent_dir, path)
    return os.path.realpath(merged_path)


__run_executed_files: Set[str] = set()


@error_handler
def run(directory: str):
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


# escape original help
__help = help


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
