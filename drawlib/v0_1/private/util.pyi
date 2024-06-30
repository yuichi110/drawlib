"""
This type stub file was generated by pyright.
"""

from typing import Tuple

"""Utility module."""
def error_handler(caller): # -> _Wrapped[Callable[..., Any], Any, Callable[..., Any], None]:
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
    ...

@error_handler
def get_angle(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> float:
    """Calculate the angle in degrees between two points.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        float: Angle in degrees between the points (xy1 to xy2).

    """
    ...

@error_handler
def get_distance(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        float: Euclidean distance between the points (xy1 to xy2).

    """
    ...

@error_handler
def get_center_and_size(xys: list[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Calculate the center coordinates and size of a group of points.

    Args:
        xys: List of tuples [(x1, y1), (x2, y2), ...] representing the coordinates of points.

    Returns:
        Tuple[Tuple[float, float], Tuple[float, float]]: Tuple containing:
            - Center coordinates (center_x, center_y).
            - Size as width and height (maxx - minx, maxy - miny).

    """
    ...

@error_handler
def plus_2points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Tuple[float, float]:
    """Add two points (vectors).

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        Tuple[float, float]: Resultant point coordinates (x1 + x2, y1 + y2).

    """
    ...

@error_handler
def minus_2points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Tuple[float, float]:
    """Subtract one point (vector) from another.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        Tuple[float, float]: Resultant point coordinates (x1 - x2, y1 - y2).

    """
    ...

@error_handler
def get_script_path() -> str:
    """Retrieve the absolute path of the user script that calls this function.

    Returns:
        str: Absolute path of the user script.

    Raises:
        FileNotFoundError: If the script path cannot be determined.

    """
    ...

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
    ...

@error_handler
def get_script_function_name() -> str:
    """Retrieve the name of the function in the user script that calls this function.

    Returns:
        str: Function name in the user script.

    Raises:
        RuntimeError: If the function name cannot be determined.

    """
    ...

@error_handler
def purge_font_cache() -> None:
    """Delete downloaded font file cache."""
    ...

