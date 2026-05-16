# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Utility module for converting drawlib data to matplotlib data."""

import math
from typing import Any, Callable, Literal

from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib.v0_2.private.l1_core import guarded
from drawlib.v0_2.private.l2_types import (
    TypeAngle,
    TypeArrowHead,
    TypeColor,
    TypeColorRGBA,
    TypeCoordinate,
    TypeCoordinates,
    TypeFloat,
    TypePathPoints,
)
from drawlib.v0_2.private.l3_external import download_if_not_exist
from drawlib.v0_2.private.l3_fonts import get_font_metadata
from drawlib.v0_2.private.l3_styles import (
    SYSTEM_DEFAULT_ICON_STYLE,
    SYSTEM_DEFAULT_IMAGE_STYLE,
    SYSTEM_DEFAULT_LINE_STYLE,
    SYSTEM_DEFAULT_SHAPE_STYLE,
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    SYSTEM_DEFAULT_TEXT_STYLE,
    Colors,
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l4_theme import dtheme


@guarded
def get_rotated_points(
    xys: TypeCoordinates,
    center: TypeCoordinate,
    angle: TypeAngle,
) -> TypeCoordinates:
    """
    Rotate a list of points around a given center by a given angle.

    Args:
        xys (list of tuples): List of (x, y) points to rotate.
        center (tuple): The (x, y) coordinates of the center point.
        angle (float): The angle to rotate the points by, in degrees.

    Returns:
    list of tuples: The rotated points.
    """
    angle = math.radians(angle)
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    rotated_points = []
    cx, cy = center

    for x, y in xys:
        # Translate point to origin
        translated_x = x - cx
        translated_y = y - cy
        # Rotate point
        rotated_x = translated_x * cos_theta - translated_y * sin_theta
        rotated_y = translated_x * sin_theta + translated_y * cos_theta
        # Translate point back
        final_x = rotated_x + cx
        final_y = rotated_y + cy
        rotated_points.append((final_x, final_y))

    return rotated_points


@guarded
def get_rotated_path_points(
    path_points: TypePathPoints,
    center: TypeCoordinate,
    angle: TypeAngle,
) -> TypePathPoints:
    """
    Rotate a list of points around a given center by a given angle.

    Args:
        path_points (list of tuples): List of (x, y) points to rotate.
        center (tuple): The (x, y) coordinates of the center point.
        angle (float): The angle to rotate the points by, in degrees.

    Returns:
    list of tuples: The rotated points.
    """
    angle = math.radians(angle)
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    rotated_path_points: TypePathPoints = []
    cx, cy = center

    for t in path_points:
        # Translate point to origin
        if not isinstance(t[0], tuple):
            x: float = t[0]
            y: float = t[1]  # type: ignore
            translated_x = x - cx
            translated_y = y - cy
            # Rotate point
            rotated_x = translated_x * cos_theta - translated_y * sin_theta
            rotated_y = translated_x * sin_theta + translated_y * cos_theta
            # Translate point back
            final_x = rotated_x + cx
            final_y = rotated_y + cy
            rotated_path_points.append((final_x, final_y))

        else:
            new_path_point = []
            for xy in t:
                x: float = xy[0]  # type: ignore
                y: float = xy[1]  # type: ignore
                translated_x = x - cx
                translated_y = y - cy
                # Rotate point
                rotated_x = translated_x * cos_theta - translated_y * sin_theta
                rotated_y = translated_x * sin_theta + translated_y * cos_theta
                # Translate point back
                final_x = rotated_x + cx
                final_y = rotated_y + cy
                new_path_point.append((final_x, final_y))
            rotated_path_points.append(tuple(new_path_point))

    return rotated_path_points


@guarded
def get_angle(xy1: TypeCoordinate, xy2: TypeCoordinate) -> TypeAngle:
    """Calculate the angle in degrees between two points.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        float: Angle in degrees between the points (xy1 to xy2).

    """
    x1, y1 = xy1
    x2, y2 = xy2
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


@guarded
def get_distance(xy1: TypeCoordinate, xy2: TypeCoordinate) -> TypeFloat:
    """Calculate the Euclidean distance between two points.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        float: Euclidean distance between the points (xy1 to xy2).

    """
    x1, y1 = xy1
    x2, y2 = xy2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


@guarded
def get_center_and_size(
    xys: TypeCoordinates,
) -> tuple[TypeCoordinate, TypeCoordinate]:
    """Calculate the center coordinates and size of a group of points.

    Args:
        xys: List of tuples [(x1, y1), (x2, y2), ...] representing the coordinates of points.

    Returns:
        Tuple[Tuple[float, float], Tuple[float, float]]: Tuple containing:
            - Center coordinates (center_x, center_y).
            - Size as width and height (maxx - minx, maxy - miny).

    """
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


@guarded
def plus_2points(xy1: TypeCoordinate, xy2: TypeCoordinate) -> TypeCoordinate:
    """Add two points (vectors).

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        Tuple[float, float]: Resultant point coordinates (x1 + x2, y1 + y2).

    """
    return (xy1[0] + xy2[0], xy1[1] + xy2[1])


@guarded
def minus_2points(xy1: TypeCoordinate, xy2: TypeCoordinate) -> TypeCoordinate:
    """Subtract one point (vector) from another.

    Args:
        xy1: Tuple of floats (x1, y1) representing the coordinates of the first point.
        xy2: Tuple of floats (x2, y2) representing the coordinates of the second point.

    Returns:
        Tuple[float, float]: Resultant point coordinates (x1 - x2, y1 - y2).

    """
    return (xy1[0] - xy2[0], xy1[1] - xy2[1])


def get_dict_value_none_keys_removed(options: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in options.items() if value is not None}
