# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Point and path builder helpers for canvas arrow shapes."""

from __future__ import annotations

import math
from typing import cast

from drawlib._core.l2_types import (
    Angle,
    Angle90,
    ArrowHead,
    Coordinate,
    Coordinates,
    PathPoints,
    ShapeRadius,
)
from drawlib._core.l3_math import get_rotated_path_points
from drawlib._core.l4_canvas._line_utils import LineArcHelper, LineUtils
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils


def build_arrow_points(
    distance: float,
    tail_width: float,
    head_width: float,
    head_length: float,
    head: ArrowHead,
) -> PathPoints:
    """Build local path points for a straight arrow of length distance."""
    max_head_len = distance / 2.0 if head == "<->" else distance
    head_length = min(head_length, max_head_len)
    p11 = (0, head_width / 2 - tail_width / 2)
    p12 = (0, head_width / 2 + tail_width / 2)
    p13 = (distance, head_width / 2 + tail_width / 2)
    p14 = (distance, head_width / 2 - tail_width / 2)

    # arrow_head_rectangle. left-bottom -> left-top ...
    distance2 = distance - head_length * 2
    p21 = (head_length, 0)
    p22 = (head_length, head_width)
    p23 = (head_length + distance2, head_width)
    p24 = (head_length + distance2, 0)

    # arrow_tail_internal_rectangle. left-bottom -> left-top ...
    p31 = (head_length, head_width / 2 - tail_width / 2)
    p32 = (head_length, head_width / 2 + tail_width / 2)
    p33 = (head_length + distance2, head_width / 2 + tail_width / 2)
    p34 = (head_length + distance2, head_width / 2 - tail_width / 2)

    # start, end
    p41 = (0, head_width / 2)
    p42 = (distance, head_width / 2)

    if head == "->":
        return [p11, p12, p33, p23, p42, p24, p34]
    if head == "<-":
        return [p41, p22, p32, p13, p14, p31, p21]
    if head == "<->":
        return [p41, p22, p32, p33, p23, p42, p24, p34, p31, p21]
    raise ValueError(f"Unsupported arrow head: {head}")


def _point_on_line(a: Coordinate, b: Coordinate, n: float) -> Coordinate:
    ab = (b[0] - a[0], b[1] - a[1])
    ab_length = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    ab_unit = (ab[0] / ab_length, ab[1] / ab_length)
    scaled_vector = (ab_unit[0] * n, ab_unit[1] * n)
    return (a[0] + scaled_vector[0], a[1] + scaled_vector[1])


def _point_parallel_to_line(a: Coordinate, b: Coordinate, distance: float) -> Coordinate:
    ab = (b[0] - a[0], b[1] - a[1])
    ab_length = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    ab_unit = (ab[0] / ab_length, ab[1] / ab_length)
    ab_perpendicular = (-ab_unit[1], ab_unit[0])
    scaled_vector = (ab_perpendicular[0] * distance, ab_perpendicular[1] * distance)
    return (a[0] + scaled_vector[0], a[1] + scaled_vector[1])


def build_arrow_polyline_points(
    xys: Coordinates,
    tail_width: float,
    head_width: float,
    head_length: float,
    head: ArrowHead,
    shape_r: ShapeRadius | None,
) -> Coordinates:
    """Build polygon outline points for a polyline arrow."""
    xys = LineUtils.sanitize_xys(xys)
    if len(xys) < 2:
        raise ValueError("xys must contain at least 2 distinct points.")

    first_seg_len = math.hypot(xys[1][0] - xys[0][0], xys[1][1] - xys[0][1])
    last_seg_len = math.hypot(xys[-1][0] - xys[-2][0], xys[-1][1] - xys[-2][1])
    if len(xys) == 2 and head == "<->":
        eff_start_hl = min(float(head_length), first_seg_len * 0.45)
        eff_end_hl = min(float(head_length), last_seg_len * 0.45)
    else:
        eff_start_hl = min(float(head_length), first_seg_len * 0.9)
        eff_end_hl = min(float(head_length), last_seg_len * 0.9)

    if head in {"<-", "<->"}:
        xys_start = _point_on_line(xys[0], xys[1], eff_start_hl)
    else:
        xys_start = xys[0]

    if head in {"->", "<->"}:
        xys_end = _point_on_line(xys[-1], xys[-2], eff_end_hl)
    else:
        xys_end = xys[-1]

    new_xys = xys[1:-1]
    new_xys.insert(0, xys_start)
    new_xys.append(xys_end)
    aph = ArrowPolylineHelper(new_xys, shape_r, 100)
    parallel_xys1 = aph.get_parallel_points(tail_width / 2)
    parallel_xys2 = aph.get_parallel_points(tail_width / -2)
    parallel_xys2.reverse()

    if head in {"<-", "<->"}:
        ahp1 = _point_parallel_to_line(xys_start, xys[1], head_width / 2)
        ahp2 = _point_parallel_to_line(xys_start, xys[1], head_width / -2)
        parallel_xys1.insert(0, xys[0])
        parallel_xys1.insert(1, ahp1)
        parallel_xys2.append(ahp2)

    if head in {"->", "<->"}:
        ahp3 = _point_parallel_to_line(xys_end, xys[-2], head_width / -2)
        ahp4 = _point_parallel_to_line(xys_end, xys[-2], head_width / 2)
        parallel_xys1.append(ahp3)
        parallel_xys1.append(xys[-1])
        parallel_xys1.append(ahp4)

    parallel_xys1.extend(parallel_xys2)
    return parallel_xys1


def build_arrow_arc_path_points(
    xy: Coordinate,
    width: float,
    height: float,
    tail_width: float,
    head_width: float,
    head_angle: Angle,
    head: ArrowHead,
    angle_start: Angle,
    angle_end: Angle,
    angle: Angle,
) -> PathPoints:
    """Build Bezier path points for an elliptical arc arrow."""
    width_int = width - tail_width
    width_ext = width + tail_width
    height_int = height - tail_width
    height_ext = height + tail_width

    if head in {"<-", "<->"}:
        angle_start2 = (angle_start + head_angle) % 360
    else:
        angle_start2 = angle_start

    if head in {"->", "<->"}:
        angle_end2 = (angle_end - head_angle) % 360
    else:
        angle_end2 = angle_end

    if angle_start2 > angle_end2:
        pp1_fa = -1 * (360 - angle_start2)
        pp1_ta = angle_end2
        pp2_fa = angle_end2
        pp2_ta = pp1_fa
    else:
        pp1_fa = angle_start2
        pp1_ta = angle_end2
        pp2_fa = angle_end2
        pp2_ta = angle_start2

    path_points1 = LineArcHelper.get_ellipse_path_points(
        xy,
        width_int,
        height_int,
        pp1_fa,
        pp1_ta,
    )
    path_points2 = LineArcHelper.get_ellipse_path_points(
        xy,
        width_ext,
        height_ext,
        pp2_fa,
        pp2_ta,
    )

    if angle_start > angle_end:
        angle_start = -1 * (360 - angle_start)

    if head in {"<-", "<->"}:
        path_points1.insert(
            0,
            LineArcHelper.get_point_on_ellipse(
                xy,
                width,
                height,
                angle_start,
            ),
        )
        path_points1.insert(
            1,
            LineArcHelper.get_point_on_ellipse(
                xy,
                width - head_width,
                height - head_width,
                angle_start2,
            ),
        )
        path_points2.append(
            LineArcHelper.get_point_on_ellipse(
                xy,
                width + head_width,
                height + head_width,
                angle_start2,
            )
        )

    if head in {"->", "<->"}:
        path_points1.append(
            LineArcHelper.get_point_on_ellipse(
                xy,
                width - head_width,
                height - head_width,
                angle_end2,
            )
        )
        path_points1.append(
            LineArcHelper.get_point_on_ellipse(
                xy,
                width,
                height,
                angle_end,
            )
        )
        path_points2.insert(
            0,
            LineArcHelper.get_point_on_ellipse(
                xy,
                width + head_width,
                height + head_width,
                angle_end2,
            ),
        )

    path_points1.extend(path_points2)

    if angle != 0:
        return get_rotated_path_points(path_points1, xy, angle)
    return path_points1


def build_chevron_points(
    width: float,
    height: float,
    corner_angle: Angle90,
    mirror: bool,
    shape_r: ShapeRadius | None,
) -> PathPoints:
    """Build local path points for a chevron shape with optional corner rounding."""
    half_h = height / 2.0
    angle_rad = math.radians(corner_angle)
    x_offset = half_h / math.tan(angle_rad)

    p1 = (0.0, 0.0)
    p2 = (x_offset, half_h)
    p3 = (0.0, height)
    p4 = (width, height)
    p5 = (width + p2[0], height / 2)
    p6 = (width, 0.0)

    if mirror:
        p2 = (p2[0] * -1, p2[1])
        p4 = (p4[0] * -1, p4[1])
        p5 = (p5[0] * -1, p5[1])
        p6 = (p6[0] * -1, p6[1])

    return ShapeUtils.round_polygon_points([p1, p2, p3, p4, p5, p6], shape_r)


class ArrowPolylineHelper:
    """Internal helper for computing parallel offset curves along rounded or sharp polylines."""

    @staticmethod
    def _normalize_joint_radii(num_joints: int, r: ShapeRadius | None) -> list[float]:
        if r is None:
            return [0.0] * num_joints
        if isinstance(r, (int, float)):
            return [float(r)] * num_joints
        if len(r) != num_joints:
            raise ValueError(f"shape_r tuple length ({len(r)}) must match the number of joints ({num_joints}).")
        return [float(val) for val in r]

    def __init__(
        self,
        xys: Coordinates,
        r: ShapeRadius | None,
        num_points: int = 100,
    ) -> None:
        """Initialize ArrowPolylineHelper with polyline points and joint rounding radius."""

        def get_mid_points(
            a: Coordinate,
            b: Coordinate,
            radius: float,
        ) -> tuple[Coordinate, Coordinate]:
            ab = [b[0] - a[0], b[1] - a[1]]
            ab_distance = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = [ab[0] / ab_distance, ab[1] / ab_distance]
            c = (a[0] + radius * ab_unit[0], a[1] + radius * ab_unit[1])
            d = (b[0] - radius * ab_unit[0], b[1] - radius * ab_unit[1])
            return c, d

        def bernstein_poly(i: int, n: int, t: float) -> float:
            return math.comb(n, i) * (t**i) * ((1 - t) ** (n - i))

        def get_points(
            bezier_points: Coordinates,
        ) -> Coordinates:
            n = len(bezier_points) - 1
            curve = []
            for t in [i / (num_points - 1) for i in range(num_points)]:
                x = sum(bernstein_poly(i, n, t) * bezier_points[i][0] for i in range(n + 1))
                y = sum(bernstein_poly(i, n, t) * bezier_points[i][1] for i in range(n + 1))
                curve.append((x, y))
            return curve

        num_joints = max(0, len(xys) - 2)
        radii = self._normalize_joint_radii(num_joints, r)

        if not radii or all(val == 0.0 for val in radii):
            self._r = 0.0
            self._original_points = xys[:]
            return

        self._r = max(radii)
        points: Coordinates = [xys[0]]
        last_joint_idx = len(xys) - 2
        for i in range(1, len(xys) - 1):
            r_joint = radii[i - 1]
            prev_dist = math.hypot(xys[i][0] - xys[i - 1][0], xys[i][1] - xys[i - 1][1])
            next_dist = math.hypot(xys[i + 1][0] - xys[i][0], xys[i + 1][1] - xys[i][1])
            max_prev = prev_dist * (0.9 if i == 1 else 0.49)
            max_next = next_dist * (0.9 if i == last_joint_idx else 0.49)
            eff_r = min(r_joint, max_prev, max_next)
            if eff_r <= 0.0:
                points.append(xys[i])
            else:
                _, p_in = get_mid_points(xys[i - 1], xys[i], eff_r)
                p_out, _ = get_mid_points(xys[i], xys[i + 1], eff_r)
                bezier_points = [p_in, xys[i], p_out]
                points.extend(get_points(bezier_points))
        points.append(xys[-1])

        self._original_points = points

    def get_parallel_points(self, distance: float) -> Coordinates:
        """Compute parallel offset points at perpendicular distance from the polyline."""
        if self._r == 0:
            return self._get_parallel_straight_points(distance)
        return self._get_parallel_curved_points(distance)

    def _get_parallel_curved_points(self, distance: float) -> Coordinates:
        """Compute parallel offset points when joints are curved."""

        def get_distance(p1: Coordinate, p2: Coordinate) -> float:
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        parallel_curve_points = []
        for i in range(1, len(self._original_points)):
            p0, p1 = self._original_points[i - 1], self._original_points[i]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            length = get_distance(p0, p1)
            if length == 0:
                continue
            nx, ny = -dy / length, dx / length
            px0, py0 = p0[0] + distance * nx, p0[1] + distance * ny
            px1, py1 = p1[0] + distance * nx, p1[1] + distance * ny
            parallel_curve_points.append((px0, py0))
            if i == len(self._original_points) - 1:
                parallel_curve_points.append((px1, py1))

        return parallel_curve_points

    def _get_parallel_straight_points(self, distance: float) -> Coordinates:
        """Compute parallel offset points when joints are sharp straight lines."""

        def get_parallel_line_xys(
            xy1: Coordinate,
            xy2: Coordinate,
        ) -> tuple[Coordinate, Coordinate]:
            x1, y1 = xy1
            x2, y2 = xy2

            # calc vector
            vx = x2 - x1
            vy = y2 - y1
            length = math.sqrt(vx**2 + vy**2)
            dx = -vy / length * distance
            dy = vx / length * distance

            # add vector
            x1_prime = x1 + dx
            y1_prime = y1 + dy
            x2_prime = x2 + dx
            y2_prime = y2 + dy

            return (x1_prime, y1_prime), (x2_prime, y2_prime)

        def find_lines_intersection(
            xy1: Coordinate,
            xy2: Coordinate,
            xy3: Coordinate,
            xy4: Coordinate,
        ) -> Coordinate:
            x1, y1 = xy1
            x2, y2 = xy2
            x3, y3 = xy3
            x4, y4 = xy4

            # Check if lines are vertical
            if x1 == x2 and x3 == x4:
                raise ValueError(f'line "{xy1}" -> "{xy2}" and "{xy3}" => "{xy4}" are parallel.')

            # Handle vertical lines
            if x1 == x2:
                m2 = (y4 - y3) / (x4 - x3)
                b2 = y3 - m2 * x3
                x = x1
                y = m2 * x + b2
                return (x, y)

            if x3 == x4:
                m1 = (y2 - y1) / (x2 - x1)
                b1 = y1 - m1 * x1
                x = x3
                y = m1 * x + b1
                return (x, y)

            m1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - m1 * x1
            m2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - m2 * x3

            if m1 == m2:
                raise ValueError(f'line "{xy1}" -> "{xy2}" and "{xy3}" => "{xy4}" are parallel.')

            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1

            return (x, y)

        xys = self._original_points
        parallel_lines: list[tuple[Coordinate, Coordinate]] = []
        for i in range(len(xys) - 1):
            xy1, xy2 = get_parallel_line_xys(xys[i], xys[i + 1])
            parallel_lines.append((xy1, xy2))

        points: Coordinates = []
        for i in range(len(parallel_lines) - 1):
            xy1, xy2 = parallel_lines[i]
            xy3, xy4 = parallel_lines[i + 1]
            xy = find_lines_intersection(xy1, xy2, xy3, xy4)
            points.append(xy)

        first_point = parallel_lines[0][0]
        last_point = parallel_lines[len(parallel_lines) - 1][1]

        points.insert(0, first_point)
        points.append(last_point)

        return points


__all__ = [
    "ArrowPolylineHelper",
    "build_arrow_arc_path_points",
    "build_arrow_points",
    "build_arrow_polyline_points",
    "build_chevron_points",
]
