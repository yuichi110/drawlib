"""write docstring later"""

from typing import Optional
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
                file = frame.filename
                if is_path_under(package_root, file):
                    continue
                line = frame.lineno
                print(f'Error at file:"{file}", line:"{line}"')
                print(str(e))
                if "--debug" in sys.argv:
                    print()
                    print(traceback.format_exc())
                break
            exit(1)

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
def get_script_relative_path(path: str) -> str:
    """write docstring later"""

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
    script_file = ""
    for frame in inspect.stack():
        file = frame.filename
        if is_path_under(package_root, file):
            continue
        script_file = file
        break

    if script_file == "":
        raise FileNotFoundError("Error")

    parent_directory = os.path.dirname(script_file)
    merged_path = os.path.join(parent_directory, path)
    return os.path.realpath(merged_path)


@error_handler
def load(file_or_directory: str):
    """write docstring later"""
    path = get_script_relative_path(file_or_directory)
    if not os.path.exists(path):
        raise ValueError(f'"{path}" does not exist')

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
        return python_files

    if os.path.isfile(path):
        code_path = path
        mspec = importlib.util.spec_from_file_location(
            name="t",
            location=code_path,
        )
        module = importlib.util.module_from_spec(mspec)
        mspec.loader.exec_module(module)

    else:
        dir_path = path
        for code_path in get_python_files(dir_path):
            mspec = importlib.util.spec_from_file_location(
                name="t",
                location=code_path,
            )
            module = importlib.util.module_from_spec(mspec)
            mspec.loader.exec_module(module)


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
