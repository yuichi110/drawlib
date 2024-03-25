"""write docstring later"""

import inspect
import math
import functools
import traceback
import sys
import os
import drawlib.settings as settings
from drawlib._logging import logger


def error_handler(caller):
    """write docstring later"""

    if settings.is_developer_debug_mode():
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
                logger.critical(
                    f'{type(e).__name__} at file:"{file}", line:"{line}"'
                )
                logger.critical(str(e))
                logger.debug("")
                logger.debug(traceback.format_exc())
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
    """write docstring later"""

    package_root = _get_package_root_path()
    script_path = ""
    for frame in inspect.stack():
        file = frame.filename
        if not os.path.isfile(file):
            continue
        if _is_path_under(package_root, file):
            continue
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

    package_root = _get_package_root_path()
    for frame in inspect.stack():
        file = frame.filename
        if not os.path.isfile(file):
            continue
        if _is_path_under(package_root, file):
            continue
        return frame[3]

    msg = "Critical Error. Unable to get last called user function name"
    raise RuntimeError(msg)


###############
### private ###
###############


def _get_package_root_path():
    error_module = inspect.stack()[0].filename
    module_path = os.path.abspath(error_module)
    package_root = module_path
    while not os.path.exists(os.path.join(package_root, "__init__.py")):
        package_root = os.path.dirname(package_root)
    return package_root


def _is_path_under(parent_path, child_path):
    common_parent = os.path.commonpath([parent_path, child_path])
    abs_parent_path = os.path.abspath(parent_path)
    abs_common_path = os.path.abspath(common_parent)
    return abs_parent_path == abs_common_path
