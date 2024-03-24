"""write docstring later"""

import inspect
import math
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
                if not os.path.isfile(file):
                    continue
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


@error_handler
def get_function_name():
    """write docstring later"""

    return inspect.stack()[1][3]
