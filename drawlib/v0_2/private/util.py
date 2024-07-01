# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: ANN001, ANN201, ANN401

"""Utility module."""

import functools
import inspect
import math
import os
import os.path
import shutil
import sys
import traceback
from typing import Any, Tuple

import drawlib.assets.v0_2.fonticons
import drawlib.assets.v0_2.fonts
import drawlib.v0_2.private.validators.coordinate as validator
from drawlib.v0_2.private.dutil.settings import dutil_settings
from drawlib.v0_2.private.logging import logger


# Please don't set type annotation for this decorator function.
# It will break IDE's "arguments" and "return type" help suggestions.
def error_handler(caller):
    """Drawlib error handling decorator function.

    Decorates functions to handle errors gracefully. Depending on the logging mode:
    - quiet/normal: Shows minimal error information and exits with code 1.
    - verbose: Adds stack trace to the error information.
    - developer: Disables error handling for debugging purposes.

    Args:
        caller: Function to be decorated.

    Returns:
        Decorated function.

    Raises:
        SystemExit: Exits with code 1 on error.

    Note:
        Avoid applying this decorator to functions that raise and handle their own errors,
        or to the 'settings' module due to potential circular imports.

    """

    @functools.wraps(caller)
    def wrapper(*args: Any, **kwargs: Any) -> None:
        # without error handling
        if dutil_settings.is_developer_debug_mode():
            return caller(*args, **kwargs)

        # with error handling
        try:
            return caller(*args, **kwargs)
        except Exception as e:
            package_root = _get_package_root_path()
            for frame in inspect.stack():
                file = frame.filename
                if not os.path.isfile(file):
                    continue
                if _is_path_under(package_root, file):
                    continue
                line = frame.lineno
                logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
                logger.critical(str(e))
                logger.debug("")
                logger.debug(traceback.format_exc())
                break
            sys.exit(1)

    return wrapper


@error_handler
def get_angle(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> float:
    """Calculate the angle in degrees between two points.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        float: Angle in degrees between the points (xy1 to xy2).

    """
    validator.validate_xy("xy1", xy1)
    validator.validate_xy("xy2", xy2)

    x1, y1 = xy1
    x2, y2 = xy2
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


@error_handler
def get_distance(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        float: Euclidean distance between the points (xy1 to xy2).

    """
    validator.validate_xy("xy1", xy1)
    validator.validate_xy("xy2", xy2)

    x1, y1 = xy1
    x2, y2 = xy2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


@error_handler
def get_center_and_size(
    xys: list[Tuple[float, float]],
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Calculate the center coordinates and size of a group of points.

    Args:
        xys: List of tuples [(x1, y1), (x2, y2), ...] representing the coordinates of points.

    Returns:
        Tuple[Tuple[float, float], Tuple[float, float]]: Tuple containing:
            - Center coordinates (center_x, center_y).
            - Size as width and height (maxx - minx, maxy - miny).

    """
    validator.validate_xys("xys", xys)

    minx = xys[0][0]
    maxx = xys[0][0]
    miny = xys[0][1]
    maxy = xys[0][1]
    for x, y in xys:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2

    return ((center_x, center_y), (maxx - minx, maxy - miny))


@error_handler
def plus_2points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Tuple[float, float]:
    """Add two points (vectors).

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        Tuple[float, float]: Resultant point coordinates (x1 + x2, y1 + y2).

    """
    validator.validate_xy("xy1", xy1)
    validator.validate_xy("xy2", xy2)
    return (xy1[0] + xy2[0], xy1[1] + xy2[1])


@error_handler
def minus_2points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Tuple[float, float]:
    """Subtract one point (vector) from another.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        Tuple[float, float]: Resultant point coordinates (x1 - x2, y1 - y2).

    """
    validator.validate_xy("xy1", xy1)
    validator.validate_xy("xy2", xy2)
    return (xy1[0] - xy2[0], xy1[1] - xy2[1])


@error_handler
def get_script_path() -> str:
    """Retrieve the absolute path of the user script that calls this function.

    Returns:
        str: Absolute path of the user script.

    Raises:
        FileNotFoundError: If the script path cannot be determined.

    """
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

    if not script_path:
        message = "Critical Error. Unable to detect call script file"
        raise FileNotFoundError(message)

    return script_path


@error_handler
def get_script_relative_path(path: str) -> str:
    """Construct the absolute file path from a script file path.

    Args:
        path: Relative path from the user script.

    Returns:
        str: Absolute file path.

    Raises:
        ValueError: If path is not a string.

    """
    if not isinstance(path, str):
        raise ValueError(f'Arg "path" must be str. But {path} is given.')

    if os.path.isabs(path):
        return path

    script_path = get_script_path()
    script_parent_dir = os.path.dirname(script_path)
    merged_path = os.path.join(script_parent_dir, path)
    return os.path.realpath(merged_path)


@error_handler
def get_script_function_name() -> str:
    """Retrieve the name of the function in the user script that calls this function.

    Returns:
        str: Function name in the user script.

    Raises:
        RuntimeError: If the function name cannot be determined.

    """
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


@error_handler
def purge_font_cache() -> None:
    """Delete downloaded font file cache."""
    fonts_dir_path = os.path.dirname(drawlib.assets.v0_2.fonts.__file__)
    fonticons_dir_path = os.path.dirname(drawlib.assets.v0_2.fonticons.__file__)

    for dir_path in [fonts_dir_path, fonticons_dir_path]:
        for file_name in os.listdir(dir_path):
            if file_name == "__init__.py":
                continue

            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)


#
# private
#


def _get_package_root_path() -> str:
    """Retrieve the root path of the package.

    Returns:
        str: Absolute path of the package root.

    """
    first_module = inspect.stack()[0].filename
    module_path = os.path.abspath(first_module)
    package_root = module_path
    while not os.path.exists(os.path.join(package_root, "__init__.py")):
        package_root = os.path.dirname(package_root)
    return package_root


def _is_path_under(parent_path: str, child_path: str) -> bool:
    """Check if a child path is under a parent path.

    Args:
        parent_path: Parent directory path.
        child_path: Child directory or file path.

    Returns:
        bool: True if child path is under parent path, False otherwise.

    """
    try:
        common_parent = os.path.commonpath([parent_path, child_path])
    except Exception:
        # ValueError happens when compare windows N-Drive and M-Drive
        # But use Exception class for catch for handling unexpected situation.
        return False

    abs_parent_path = os.path.abspath(parent_path)
    abs_common_path = os.path.abspath(common_parent)
    return abs_parent_path == abs_common_path
