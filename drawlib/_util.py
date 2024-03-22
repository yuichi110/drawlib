from typing import Optional
import inspect
import math
import warnings
import functools
import traceback
import sys
import os


def error_handler(caller):
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
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


@error_handler
def warning_suppress(module: Optional[str] = None):
    if module is None:
        warnings.filterwarnings("ignore")
    else:
        warnings.filterwarnings("ignore", module=module)


@error_handler
def get_function_name():
    return inspect.stack()[1][3]
