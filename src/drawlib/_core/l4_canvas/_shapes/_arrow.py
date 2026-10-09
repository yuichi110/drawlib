# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's original arrow feature implementation module."""

import math
from typing import Any, Literal

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    ArrowHead,
    Coordinate,
    Coordinates,
    PathPoints,
    PosFloat,
    ShapeRadius,
    Size,
)
from drawlib._core.l3_math import (
    get_angle,
    get_distance,
    get_rotated_path_points,
    get_rotated_points,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._line_util import LineUtil
from drawlib._core.l4_canvas._lines import LineArcHelper
from drawlib._core.l4_canvas._shapes._basic import CanvasShapeBasicFeature
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


class CanvasShapeArrowFeature(CanvasShapeBasicFeature):
    """Canvas arrow shape feature implementation module.

    This class provides methods to draw single-headed and double-headed arrows
    on a canvas. The arrows can be customized with various styles for the tail,
    head, and optional text annotations.
    """

    def __init__(self) -> None:
        """Initialize CanvasShapeArrowFeature."""
        super().__init__()

    @validate_call
    def arrow(
        self,
        xy1: Coordinate,
        xy2: Coordinate,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a straight arrow between two coordinates.

        Args:
            xy1: Starting point coordinates tuple (x, y).
            xy2: Ending point coordinates tuple (x, y).
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        x1, y1 = xy1
        x2, y2 = xy2
        x, y = ((x1 + x2) / 2, (y1 + y2) / 2)
        angle = get_angle(xy1, xy2)
        style = style.patch(halign="center", valign="center", angle=angle)

        # arrow_tail_external_rectangle. left-bottom -> left-top ...
        distance = get_distance(xy1, xy2)
        if distance <= 1e-9:
            return
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

        points: PathPoints
        if head == "->":
            points = [p11, p12, p33, p23, p42, p24, p34]
        elif head == "<-":
            points = [p41, p22, p32, p13, p14, p31, p21]
        elif head == "<->":
            points = [p41, p22, p32, p33, p23, p42, p24, p34, p31, p21]
        else:
            raise Exception()

        self.shape(
            xy=(x, y),
            path_points=points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def arrow_polyline(
        self,
        xys: Coordinates,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
    ) -> None:
        """Draw a polyline arrow along multiple coordinates.

        Args:
            xys: Sequence of coordinate tuples.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
        )

        def point_on_line(a: Coordinate, b: Coordinate, n: float) -> Coordinate:
            ab = (b[0] - a[0], b[1] - a[1])
            ab_length = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = (ab[0] / ab_length, ab[1] / ab_length)
            scaled_vector = (ab_unit[0] * n, ab_unit[1] * n)
            new_point = (a[0] + scaled_vector[0], a[1] + scaled_vector[1])
            return new_point

        def point_parallel_to_line(a: Coordinate, b: Coordinate, distance: float) -> Coordinate:
            ab = (b[0] - a[0], b[1] - a[1])
            ab_length = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = (ab[0] / ab_length, ab[1] / ab_length)
            ab_perpendicular = (-ab_unit[1], ab_unit[0])
            scaled_vector = (ab_perpendicular[0] * distance, ab_perpendicular[1] * distance)
            new_point = (a[0] + scaled_vector[0], a[1] + scaled_vector[1])
            return new_point

        xys = LineUtil.sanitize_xys(xys)
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
            xys_start = point_on_line(xys[0], xys[1], eff_start_hl)
        else:
            xys_start = xys[0]

        if head in {"->", "<->"}:
            xys_end = point_on_line(xys[-1], xys[-2], eff_end_hl)
        else:
            xys_end = xys[-1]

        new_xys = xys[1:-1]
        new_xys.insert(0, xys_start)
        new_xys.append(xys_end)
        aph = ArrowPolylineHelper(new_xys, style.shape_r, 100)
        parallel_xys1 = aph.get_parallel_points(tail_width / 2)
        parallel_xys2 = aph.get_parallel_points(tail_width / -2)
        parallel_xys2.reverse()

        if head in {"<-", "<->"}:
            ahp1 = point_parallel_to_line(xys_start, xys[1], head_width / 2)
            ahp2 = point_parallel_to_line(xys_start, xys[1], head_width / -2)
            parallel_xys1.insert(0, xys[0])
            parallel_xys1.insert(1, ahp1)
            parallel_xys2.append(ahp2)

        if head in {"->", "<->"}:
            ahp3 = point_parallel_to_line(xys_end, xys[-2], head_width / -2)
            ahp4 = point_parallel_to_line(xys_end, xys[-2], head_width / 2)
            parallel_xys1.append(ahp3)
            parallel_xys1.append(xys[-1])
            parallel_xys1.append(ahp4)

        parallel_xys1.extend(parallel_xys2)
        self.polygon(xys=parallel_xys1, style=style.patch(shape_r=0.0), text="", text_style=None)


    @validate_call
    def arrow_arc(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_angle: Angle = 10,
        head: ArrowHead = "->",
        angle_start: Angle = 0,
        angle_end: Angle = 180,
        *,
        style: Style,
    ) -> None:
        """Draw an arc-shaped arrow on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            width: Width of arc.
            height: Height of arc.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_angle: Angular length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            angle_start: Starting angle in degrees.
            angle_end: Ending angle in degrees.
            style: Style object.
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        width_int = width - tail_width
        width_ext = width + tail_width
        height_int = height - tail_width
        height_ext = height + tail_width

        if head in {"<-", "<->"}:
            angle_start2 = angle_start + head_angle
            angle_start2 %= 360
        else:
            angle_start2 = angle_start

        if head in {"->", "<->"}:
            angle_end2 = angle_end - head_angle
            angle_end2 %= 360
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
            path_points1 = get_rotated_path_points(path_points1, xy, angle)  # type: ignore

        path = self._get_path_from_points(path_points1)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

    @validate_call
    def arrow_l(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
    ) -> None:
        """Draw an L-shaped arrow on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            width: Width of L-shape.
            height: Height of L-shape.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        p1 = (xy[0] - width / 2, xy[1] + height / 2)
        p2 = (xy[0] - width / 2, xy[1] - height / 2)
        p3 = (xy[0] + width / 2, xy[1] - height / 2)

        xys = [p1, p2, p3]
        if angle != 0:
            xys = get_rotated_points(xys=xys, center=xy, angle=angle)

        self.arrow_polyline(
            xys=xys,
            tail_width=tail_width,
            head_width=head_width,
            head_length=head_length,
            head=head,
            style=style,
        )

    @validate_call
    def arrow_u(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_width: PosFloat,
        head_width: PosFloat,
        head_length: PosFloat,
        head: ArrowHead = "->",
        *,
        style: Style,
    ) -> None:
        """Draw a U-shaped arrow on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            width: Width of U-shape.
            height: Height of U-shape.
            tail_width: Width of arrow tail.
            head_width: Width of arrow head.
            head_length: Length of arrow head.
            head: Arrow head type ("->", "<-", "<->").
            style: Style object.
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        p1 = (xy[0] - width / 2, xy[1] + height / 2)
        p2 = (xy[0] - width / 2, xy[1] - height / 2)
        p3 = (xy[0] + width / 2, xy[1] - height / 2)
        p4 = (xy[0] + width / 2, xy[1] + height / 2)

        xys = [p1, p2, p3, p4]
        if angle != 0:
            xys = get_rotated_points(xys=xys, center=xy, angle=angle)

        self.arrow_polyline(
            xys=xys,
            tail_width=tail_width,
            head_width=head_width,
            head_length=head_length,
            head=head,
            style=style,
        )

    @staticmethod
    def _get_path_from_points(path_points: list[Any]) -> Path:
        """Create a matplotlib Path object from a list of points and curve data.

        Args:
            path_points (list[Any]):of points, where each point can be a coordinate
                tuple or a list representing curve data.

        Returns:
            Path: The generated matplotlib Path object.
        """
        if not path_points:
            return Path([])

        vertices = [path_points[0]]
        codes = [Path.MOVETO]

        for p in path_points[1:]:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError(f"Invalid point data length: {length}")

            if not isinstance(p[0], tuple):
                vertices.append(p)
                codes.append(Path.LINETO)
            elif length == 2:
                vertices.extend([p[0], p[1]])
                codes.extend([Path.CURVE3] * 2)
            else:
                vertices.extend([p[0], p[1], p[2]])
                codes.extend([Path.CURVE4] * 3)

        vertices.append(path_points[0])
        codes.append(Path.CLOSEPOLY)
        return Path(vertices=vertices, codes=codes)


class ArrowPolylineHelper:
    """Internal class"""

    @staticmethod
    def _normalize_joint_radii(num_joints: int, r: ShapeRadius | None) -> list[float]:
        if r is None:
            return [0.0] * num_joints
        if isinstance(r, (int, float)):
            return [float(r)] * num_joints
        if len(r) != num_joints:
            raise ValueError(
                f"shape_r tuple length ({len(r)}) must match the number of joints ({num_joints})."
            )
        return [float(val) for val in r]

    def __init__(
        self,
        xys: Coordinates,
        r: ShapeRadius | None,
        num_points: int = 100,
    ) -> None:
        """Internal function"""

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
        """Internal function"""
        if self._r == 0:
            return self._get_parallel_straight_points(distance)
        return self._get_parallel_curved_points(distance)

    def _get_parallel_curved_points(self, distance: float) -> Coordinates:
        """Internal function"""

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
        """Internal function"""

        def get_parallel_line_xys(
            xy1: Coordinate,
            xy2: Coordinate,
        ) -> tuple[Coordinate, Coordinate]:
            """Internal function"""
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
            """Internal function"""
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
    "CanvasShapeArrowFeature",
]
