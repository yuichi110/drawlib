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

from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    Bezier2,
    Bezier3,
    Coordinate,
    Coordinates,
    PathPoints,
)


@validate_call
def get_intermediate_points(
    xy1: Coordinate,
    xy2: Coordinate,
    num: int = 1,
    *,
    include_ends: bool = False,
) -> Coordinates:
    """Calculate a sequence of evenly spaced intermediate points between two coordinates.

    Divides the linear segment from ``xy1`` to ``xy2`` into ``num + 1`` equal
    intervals and returns the ``num`` interior intermediate coordinates (or ``num + 2``
    coordinates including ``xy1`` and ``xy2`` when ``include_ends=True``).

    Args:
        xy1: Starting coordinate tuple (x1, y1).
        xy2: Ending coordinate tuple (x2, y2).
        num: Number of intermediate points to generate (must be >= 1). Defaults to 1.
        include_ends: If True, includes ``xy1`` at the start and ``xy2`` at the
            end of the returned list. Defaults to False.

    Returns:
        list[tuple[float, float]]: List of interpolated (x, y) coordinates.

    Raises:
        ValueError: If ``num`` is less than 1.
    """
    if num < 1:
        raise ValueError(f"num must be >= 1, got {num}.")

    p1 = (float(xy1[0]), float(xy1[1]))
    p2 = (float(xy2[0]), float(xy2[1]))

    steps = num + 1
    mids: Coordinates = []
    for i in range(1, num + 1):
        t = i / steps
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        mids.append((x, y))

    if include_ends:
        return [p1, *mids, p2]
    return mids


@validate_call
def get_intermediate_point(
    xy1: Coordinate,
    xy2: Coordinate,
) -> Coordinate:
    """Calculate the midpoint (50%) intermediate point between two coordinates.

    This is a convenience wrapper around ``get_intermediate_points(xy1, xy2, num=1)[0]``.

    Args:
        xy1: First coordinate tuple (x1, y1).
        xy2: Second coordinate tuple (x2, y2).

    Returns:
        tuple[float, float]: The midpoint interpolated (x, y) coordinate.
    """
    return get_intermediate_points(xy1, xy2, num=1, include_ends=False)[0]


def _prepare_path_segments(
    xys: Coordinates,
    num: int,
) -> tuple[Coordinates, list[float], float]:
    """Validate path vertices and precalculate segment lengths."""
    if len(xys) < 2:
        raise ValueError(f"xys must contain at least 2 points, got {len(xys)}.")
    if num < 1:
        raise ValueError(f"num must be >= 1, got {num}.")

    pts: Coordinates = [(float(pt[0]), float(pt[1])) for pt in xys]
    seg_lengths = [
        math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        for i in range(len(pts) - 1)
    ]
    total_length = sum(seg_lengths)
    return pts, seg_lengths, total_length


def _sample_path_at_ratio(
    pts: Coordinates,
    seg_lengths: list[float],
    total_length: float,
    t: float,
) -> tuple[Coordinate, Coordinates]:
    """Sample a point and prefix sub-path at arc-length ratio t in [0, 1]."""
    if total_length == 0.0:
        return pts[0], [pts[0], pts[-1]]

    target_dist = t * total_length
    acc = 0.0

    for i, seg_len in enumerate(seg_lengths):
        if seg_len == 0.0:
            continue
        is_last = i == len(seg_lengths) - 1
        if acc + seg_len >= target_dist or is_last:
            local_t = max(0.0, min(1.0, (target_dist - acc) / seg_len))
            p_start = pts[i]
            p_end = pts[i + 1]
            pt: Coordinate = (
                p_start[0] + (p_end[0] - p_start[0]) * local_t,
                p_start[1] + (p_end[1] - p_start[1]) * local_t,
            )
            prefix: Coordinates = list(pts[: i + 1])
            is_duplicate_last = (
                math.isclose(pt[0], prefix[-1][0], abs_tol=1e-9)
                and math.isclose(pt[1], prefix[-1][1], abs_tol=1e-9)
            )
            if not is_duplicate_last or len(prefix) == 1:
                prefix.append(pt)
            return pt, prefix
        acc += seg_len

    return pts[-1], list(pts)


@validate_call
def get_intermediate_path_points(
    xys: Coordinates,
    num: int = 1,
    *,
    include_ends: bool = False,
) -> Coordinates:
    """Calculate evenly spaced intermediate points along a multi-point path trajectory.

    Measures the total arc length across all consecutive segments of ``xys`` and
    divides the trajectory into ``num + 1`` equal-distance intervals.

    Args:
        xys: Sequence of 2 or more (x, y) coordinates defining the polyline path.
        num: Number of interior intermediate points to generate (must be >= 1).
            Defaults to 1.
        include_ends: If True, includes the start point ``xys[0]`` at the beginning
            and the end point ``xys[-1]`` at the end of the returned list.
            Defaults to False.

    Returns:
        list[tuple[float, float]]: List of interpolated (x, y) coordinates along the path.

    Raises:
        ValueError: If ``xys`` has fewer than 2 points or ``num`` is less than 1.
    """
    pts, seg_lengths, total_length = _prepare_path_segments(xys, num)
    steps = num + 1
    mids: Coordinates = []
    for i in range(1, num + 1):
        pt, _ = _sample_path_at_ratio(pts, seg_lengths, total_length, i / steps)
        mids.append(pt)

    if include_ends:
        return [pts[0], *mids, pts[-1]]
    return mids


@validate_call
def get_intermediate_path_point(
    xys: Coordinates,
) -> Coordinate:
    """Calculate the 50% arc-length midpoint along a multi-point path trajectory.

    This is a convenience wrapper around ``get_intermediate_path_points(xys, num=1)[0]``.

    Args:
        xys: Sequence of 2 or more (x, y) coordinates defining the polyline path.

    Returns:
        tuple[float, float]: The (x, y) coordinate halfway along the path's total length.

    Raises:
        ValueError: If ``xys`` has fewer than 2 points.
    """
    return get_intermediate_path_points(xys, num=1, include_ends=False)[0]


@validate_call
def get_intermediate_paths(
    xys: Coordinates,
    num: int = 1,
    *,
    include_ends: bool = False,
) -> list[Coordinates]:
    """Calculate progressive prefix sub-paths along a multi-point path trajectory.

    Divides the total arc length of ``xys`` into ``num + 1`` equal-distance intervals
    and returns for each step the partial polyline starting at ``xys[0]``, passing
    through all intermediate corners reached so far, and ending at the current
    interpolated tip point.

    Args:
        xys: Sequence of 2 or more (x, y) coordinates defining the polyline path.
        num: Number of intermediate partial paths to generate (must be >= 1).
            Defaults to 1.
        include_ends: If True, appends the complete path ``xys`` as the final element
            of the returned list. Every returned path is guaranteed to contain at
            least 2 coordinates so it can be passed directly to ``lines()``,
            ``lines_curved()``, or ``arrow_polyline()``. Defaults to False.

    Returns:
        list[list[tuple[float, float]]]: List of progressive partial coordinate lists.

    Raises:
        ValueError: If ``xys`` has fewer than 2 points or ``num`` is less than 1.
    """
    pts, seg_lengths, total_length = _prepare_path_segments(xys, num)
    steps = num + 1
    sub_paths: list[Coordinates] = []
    for i in range(1, num + 1):
        _, prefix = _sample_path_at_ratio(pts, seg_lengths, total_length, i / steps)
        sub_paths.append(prefix)

    if include_ends:
        sub_paths.append(list(pts))
    return sub_paths


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
            b3 = pt
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
