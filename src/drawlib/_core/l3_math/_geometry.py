# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Geometry and transformation math functions for 2D graphics."""

from __future__ import annotations

import math
from typing import cast

from drawlib._core.l2_types import (
    Angle,
    Bezier2,
    Bezier3,
    Coordinate,
    Coordinates,
    PathPoints,
)


def rotate_point(
    xy: Coordinate,
    angle: Angle,
    center: Coordinate = (0.0, 0.0),
) -> Coordinate:
    """Rotate a single point around a given center by a given angle in degrees.

    Args:
        xy: The (x, y) coordinates of the point to rotate.
        angle: The angle to rotate the point by, in degrees.
        center: The (cx, cy) coordinates of the center point. Defaults to (0.0, 0.0).

    Returns:
        Coordinate: The rotated (x, y) coordinate.
    """
    angle_rad = math.radians(angle)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)

    cx, cy = center
    translated_x = xy[0] - cx
    translated_y = xy[1] - cy

    rotated_x = translated_x * cos_theta - translated_y * sin_theta
    rotated_y = translated_x * sin_theta + translated_y * cos_theta

    return (rotated_x + cx, rotated_y + cy)


def get_point_on_ellipse(
    center: Coordinate,
    width: float,
    height: float,
    angle: Angle,
) -> Coordinate:
    """Calculate the coordinate of a point on an ellipse circumference.

    Args:
        center: Center coordinate (cx, cy) of the ellipse.
        width: Total horizontal width of the ellipse (2 * rx).
        height: Total vertical height of the ellipse (2 * ry).
        angle: Angle in degrees from the positive X axis (0 degrees = right).

    Returns:
        Coordinate: Calculated (x, y) point on the ellipse edge.
    """
    angle_rad = math.radians(angle)
    return (
        center[0] + (width / 2.0) * math.cos(angle_rad),
        center[1] + (height / 2.0) * math.sin(angle_rad),
    )


def get_rotated_points(
    xys: Coordinates,
    center: Coordinate,
    angle: Angle,
) -> Coordinates:
    """Rotate a list of points around a given center by a given angle.

    Args:
        xys: List of (x, y) points to rotate.
        center: The (x, y) coordinates of the center point.
        angle: The angle to rotate the points by, in degrees.

    Returns:
        Coordinates: The rotated points.
    """
    return [rotate_point(xy, angle=angle, center=center) for xy in xys]


def get_rotated_path_points(
    path_points: PathPoints,
    center: Coordinate,
    angle: Angle,
) -> PathPoints:
    """Rotate a list of path points (including control points) around a center by an angle.

    Args:
        path_points: List of path points (tuples of coordinates) to rotate.
        center: The (x, y) coordinates of the center point.
        angle: The angle to rotate the points by, in degrees.

    Returns:
        PathPoints: The rotated path points.
    """
    rotated: PathPoints = []
    for pt in path_points:
        if isinstance(pt[0], (int, float)):
            coord = cast(Coordinate, pt)
            rotated.append(rotate_point(coord, angle=angle, center=center))
        elif len(pt) == 2:
            b2 = cast(Bezier2, pt)
            rotated.append((
                rotate_point(b2[0], angle=angle, center=center),
                rotate_point(b2[1], angle=angle, center=center),
            ))
        elif len(pt) == 3:
            b3 = cast(Bezier3, pt)
            rotated.append((
                rotate_point(b3[0], angle=angle, center=center),
                rotate_point(b3[1], angle=angle, center=center),
                rotate_point(b3[2], angle=angle, center=center),
            ))
    return rotated


def get_angle(xy1: Coordinate, xy2: Coordinate) -> Angle:
    """Calculate the angle in degrees between two points.

    Args:
        xy1: Coordinate tuple (x1, y1) representing the first point.
        xy2: Coordinate tuple (x2, y2) representing the second point.

    Returns:
        Angle: Angle in degrees between the points (from xy1 to xy2, in range [0, 360)).
    """
    dx = xy2[0] - xy1[0]
    dy = xy2[1] - xy1[1]
    angle_deg = math.degrees(math.atan2(dy, dx))
    return (angle_deg + 360.0) % 360.0


def get_distance(xy1: Coordinate, xy2: Coordinate) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        xy1: Coordinate tuple (x1, y1) representing the first point.
        xy2: Coordinate tuple (x2, y2) representing the second point.

    Returns:
        float: Euclidean distance between xy1 and xy2.
    """
    return math.hypot(xy2[0] - xy1[0], xy2[1] - xy1[1])


def get_center_and_size(
    xys: Coordinates,
) -> tuple[Coordinate, Coordinate]:
    """Calculate the center coordinates and bounding box size of a group of points.

    Args:
        xys: List of coordinate tuples [(x1, y1), (x2, y2), ...].

    Returns:
        tuple[Coordinate, Coordinate]: Tuple containing:
            - Center coordinates (center_x, center_y).
            - Dimensions (width, height).

    Raises:
        ValueError: If xys list is empty.
    """
    if not xys:
        raise ValueError("Points list must not be empty.")

    xs = [x for x, _ in xys]
    ys = [y for _, y in xys]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    center = ((min_x + max_x) / 2.0, (min_y + max_y) / 2.0)
    size = (max_x - min_x, max_y - min_y)

    return center, size


def plus_2points(xy1: Coordinate, xy2: Coordinate) -> Coordinate:
    """Add two 2D points element-wise.

    Args:
        xy1: First coordinate tuple (x1, y1).
        xy2: Second coordinate tuple (x2, y2).

    Returns:
        Coordinate: Vector sum (x1 + x2, y1 + y2).
    """
    return (xy1[0] + xy2[0], xy1[1] + xy2[1])


def minus_2points(xy1: Coordinate, xy2: Coordinate) -> Coordinate:
    """Subtract the second 2D point from the first element-wise.

    Args:
        xy1: First coordinate tuple (x1, y1).
        xy2: Second coordinate tuple (x2, y2).

    Returns:
        Coordinate: Vector difference (x1 - x2, y1 - y2).
    """
    return (xy1[0] - xy2[0], xy1[1] - xy2[1])
