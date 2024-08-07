# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's original arrow feature implementation module."""

import math
from typing import Any, List, Literal, Optional, Tuple, Union

from matplotlib.patches import PathPatch
from matplotlib.path import Path

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core.util import LineUtil, ShapeUtil
from drawlib.v0_2.private.core_canvas.base import CanvasBase
from drawlib.v0_2.private.core_canvas.line import LineArcHelper
from drawlib.v0_2.private.util import (
    error_handler,
    get_angle,
    get_distance,
    get_rotated_path_points,
    get_rotated_points,
)


class CanvasOriginalArrowFeature(CanvasBase):
    """Canvas's original arrow feature implementation module.

    This class provides methods to draw single-headed and double-headed arrows
    on a canvas. The arrows can be customized with various styles for the tail,
    head, and optional text annotations.
    """

    def __init__(self) -> None:
        """Initialize CanvasOriginalArrowFeature.

        This initializes the CanvasOriginalArrowFeature class, inheriting from
        CanvasBase. It sets up the basic canvas features required for drawing
        original arrow shapes.
        """
        super().__init__()

    @error_handler
    def arrow(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        tail_width: float,
        head_width: float,
        head_length: float,
        head: Literal[
            "->",
            "<-",
            "<->",
        ] = "->",
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw single and double-headed arrow.

        Args:
            xy1: Tuple[float, float]: Arrow start point.
            xy2: Tuple[float, float]: Arrow end point.
            tail_width: float: Width of the arrow tail.
            head_width: float: Width of the arrow head.
            head_length: float: Length of the arrow head.
            head: Literal["->", "<-", "<->"]: Arrow head style ("->", "<-", "<->").
            style: Union[ShapeStyle, str, None]: Optional style of the arrow.
            text: str: Optional text to display at the center of the arrow.
            textsize: Optional[float]: Optional size of the text.
            textstyle: Union[ShapeTextStyle, str, None]: Optional style of the text.

        Returns:
            None
        """
        # matplotlib FancyArrow, FancyArrowPatch seems not good
        # for implement this function.
        # Calculate arrow points pass it to shape().

        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.get,
        )
        validator.validate_shape_args(locals())

        x1, y1 = xy1
        x2, y2 = xy2
        x, y = ((x1 + x2) / 2, (y1 + y2) / 2)
        angle = get_angle(xy1, xy2)
        style.halign = "center"  # no choice
        style.valign = "center"  # no choice

        # arrow_tail_external_rectangle. left-bottom -> left-top ...
        distance = get_distance(xy1, xy2)
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
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @error_handler
    def arrow_polyline(
        self,
        xys: List[Tuple[float, float]],
        tail_width: float,
        head_width: float,
        head_length: float,
        head: Literal[
            "->",
            "<-",
            "<->",
        ] = "->",
        r: float = 0,
        style: Union[ShapeStyle, str, None] = None,
    ) -> None:
        """Draw single and double-headed arrow.

        Args:
            xys: List[Tuple[float, float]]: Arrow points.
            tail_width: float: Width of the arrow tail.
            head_width: float: Width of the arrow head.
            head_length: float: Length of the arrow head.
            head: Literal["->", "<-", "<->"]: Arrow head style ("->", "<-", "<->").
            r (float, optional): Radius for rounded connections (default is 0.0).
            style: Union[ShapeStyle, str, None]: Optional style of the arrow.

        Returns:
            None
        """
        # matplotlib FancyArrow, FancyArrowPatch seems not good
        # for implement this function.
        # Calculate arrow points pass it to shape().

        style, _ = ShapeUtil.format_styles(
            style,
            None,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.get,
        )
        validator.validate_shape_args(locals())

        def point_on_line(a: Tuple[float, float], b: Tuple[float, float], n: float) -> Tuple[float, float]:
            ab = (b[0] - a[0], b[1] - a[1])
            ab_length = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = (ab[0] / ab_length, ab[1] / ab_length)
            scaled_vector = (ab_unit[0] * n, ab_unit[1] * n)
            new_point = (a[0] + scaled_vector[0], a[1] + scaled_vector[1])
            return new_point

        def point_parallel_to_line(
            a: Tuple[float, float], b: Tuple[float, float], distance: float
        ) -> Tuple[float, float]:
            ab = (b[0] - a[0], b[1] - a[1])
            ab_length = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = (ab[0] / ab_length, ab[1] / ab_length)
            ab_perpendicular = (-ab_unit[1], ab_unit[0])
            scaled_vector = (ab_perpendicular[0] * distance, ab_perpendicular[1] * distance)
            new_point = (a[0] + scaled_vector[0], a[1] + scaled_vector[1])
            return new_point

        xys = LineUtil.sanitize_xys(xys)
        if head in {"<-", "<->"}:
            xys_start = point_on_line(xys[0], xys[1], head_length)
        else:
            xys_start = xys[0]

        if head in {"->", "<->"}:
            xys_end = point_on_line(xys[-1], xys[-2], head_length)
        else:
            xys_end = xys[-1]

        new_xys = xys[1:-1]
        new_xys.insert(0, xys_start)
        new_xys.append(xys_end)
        aph = ArrowPolylineHelper(new_xys, r, 100)
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
        self.polygon(xys=parallel_xys1, style=style, text="", textstyle=None)

    @error_handler
    def arrow_arc(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        tail_width: float,
        head_width: float,
        head_angle: float = 10,
        head: Literal["->", "<-", "<->"] = "->",
        angle_start: float = 0,
        angle_end: float = 180,
        angle: float = 0,
        style: Union[ShapeStyle, str, None] = None,
    ) -> None:
        """Draw arc arrow.

        Args:
            xy: Tuple[float, float]: The center point of the circle from which the arc arrow is drawn.
            width: float: The width of the ellipse.
            height: float: The height of the ellipse
            tail_width: float: The width of the tail of the arrow.
            head_width: float: The width of the head of the arrow.
            head_angle: float: The angle of the arrowhead in degrees (default is 10).
            head: Literal["->", "<-", "<->"]: The arrowhead style ("->", "<-", "<->").
            angle_start: float: The starting angle of the arc in degrees (default is 0).
            angle_end: float: The ending angle of the arc in degrees (default is 180).
            angle (float): The angle of ellipse.
            style: Union[ShapeStyle, str, None]: Optional shape style.

        Returns:
            None
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.get,
        )
        validator.validate_shape_args(locals())

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

        # create Path
        vertices = [path_points1[0]]
        codes = [Path.MOVETO]
        for p in path_points1[1:]:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError()

            if not isinstance(p[0], tuple):
                vertices.append(p)
                codes.append(Path.LINETO)

            elif length == 2:
                vertices.extend([p[0], p[1]])  # type: ignore
                codes.extend([Path.CURVE3] * 2)

            else:
                vertices.extend([p[0], p[1], p[2]])  # type: ignore
                codes.extend([Path.CURVE4] * 3)

        vertices.append(path_points1[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

    @error_handler
    def arrow_l(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        tail_width: float,
        head_width: float,
        head_length: float,
        head: Literal["->", "<-", "<->"] = "->",
        r: float = 0,
        angle: float = 0,
        style: Union[ShapeStyle, str, None] = None,
    ) -> None:
        """Draw "L" shape arrow.

        Args:
            xy: Tuple[float, float]: The center point of L arrow.
            width: float: The width L arrow.
            height: float: The height of L arrow.
            tail_width: float: The width of the tail of the arrow.
            head_width: float: The width of the head of the arrow.
            head_length: float: Length of the arrow head.
            head: Literal["->", "<-", "<->"]: Arrow head style ("->", "<-", "<->").
            r (float, optional): Radius for rounded connections (default is 0.0).
            angle: float: rotate angle.
            style: Union[ShapeStyle, str, None]: Optional shape style.

        Returns:
            None
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.get,
        )
        validator.validate_shape_args(locals())

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
            r=r,
            style=style,
        )

    @error_handler
    def arrow_u(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        tail_width: float,
        head_width: float,
        head_length: float,
        head: Literal["->", "<-", "<->"] = "->",
        r: float = 0,
        angle: float = 0,
        style: Union[ShapeStyle, str, None] = None,
    ) -> None:
        """Draw "U" shape arrow.

        Args:
            xy: Tuple[float, float]: The center point U arrow.
            width: float: The width of the U arrow.
            height: float: The height of the U arrow.
            tail_width: float: The width of the tail of the arrow.
            head_width: float: The width of the head of the arrow.
            head_length: float: Length of the arrow head.
            head: Literal["->", "<-", "<->"]: Arrow head style ("->", "<-", "<->").
            r (float, optional): Radius for rounded connections (default is 0.0).
            angle: float: rotate angle.
            style: Union[ShapeStyle, str, None]: Optional shape style.

        Returns:
            None
        """
        style, _ = ShapeUtil.format_styles(
            style,
            None,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.get,
        )
        validator.validate_shape_args(locals())

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
            r=r,
            style=style,
        )


class ArrowPolylineHelper:
    """Internal class"""

    def __init__(
        self,
        xys: List[Tuple[float, float]],
        r: float,
        num_points: int = 100,
    ) -> None:
        """Internal function"""

        def get_mid_points(
            a: Tuple[float, float],
            b: Tuple[float, float],
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
            ab = [b[0] - a[0], b[1] - a[1]]
            ab_distance = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
            ab_unit = [ab[0] / ab_distance, ab[1] / ab_distance]
            c = (a[0] + r * ab_unit[0], a[1] + r * ab_unit[1])
            d = (b[0] - r * ab_unit[0], b[1] - r * ab_unit[1])
            return c, d

        def bernstein_poly(i: int, n: int, t: float) -> float:
            return math.comb(n, i) * (t**i) * ((1 - t) ** (n - i))

        def get_points(
            bezier_points: List[Tuple[float, float]],
        ) -> List[Tuple[float, float]]:
            n = len(bezier_points) - 1
            curve = []
            for t in [i / (num_points - 1) for i in range(num_points)]:
                x = sum(bernstein_poly(i, n, t) * bezier_points[i][0] for i in range(n + 1))
                y = sum(bernstein_poly(i, n, t) * bezier_points[i][1] for i in range(n + 1))
                curve.append((x, y))
            return curve

        self._r = r
        if r == 0:
            self._original_points = xys[:]
            return

        points = []
        bezier_start: Tuple[float, float] = (0, 0)
        last_i = len(xys) - 2
        # last_xy = (0, 0)
        for i in range(len(xys)):
            # first straight line
            if i == 0:
                _, bezier_start = get_mid_points(xys[0], xys[1])
                points.append(xys[0])
                continue

            # last straight line
            if i == last_i:
                p1, _ = get_mid_points(xys[i], xys[i + 1])
                bezier_points = [bezier_start, xys[i], p1]
                points.extend(get_points(bezier_points))
                points.append(xys[i + 1])
                break

            p1, p2 = get_mid_points(xys[i], xys[i + 1])
            bezier_points = [bezier_start, xys[i], p1]
            points.extend(get_points(bezier_points))
            bezier_start = p2

        self._original_points = points

    def get_parallel_points(self, distance: float) -> List[Tuple[float, float]]:
        """Internal function"""
        if self._r == 0:
            return self._get_parallel_straight_points(distance)
        return self._get_parallel_curved_points(distance)

    def _get_parallel_curved_points(self, distance: float) -> List[Tuple[float, float]]:
        """Internal function"""

        def get_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        parallel_curve_points = []
        for i in range(1, len(self._original_points)):
            p0, p1 = self._original_points[i - 1], self._original_points[i]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            length = get_distance(p0, p1)
            nx, ny = -dy / length, dx / length
            px0, py0 = p0[0] + distance * nx, p0[1] + distance * ny
            px1, py1 = p1[0] + distance * nx, p1[1] + distance * ny
            parallel_curve_points.append((px0, py0))
            if i == len(self._original_points) - 1:
                parallel_curve_points.append((px1, py1))

        return parallel_curve_points

    def _get_parallel_straight_points(self, distance: float) -> List[Tuple[float, float]]:
        """Internal function"""

        def get_parallel_line_xys(
            xy1: Tuple[float, float],
            xy2: Tuple[float, float],
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
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
            xy1: Tuple[float, float],
            xy2: Tuple[float, float],
            xy3: Tuple[float, float],
            xy4: Tuple[float, float],
        ) -> Tuple[float, float]:
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
        parallel_lines: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []
        for i in range(len(xys) - 1):
            xy1, xy2 = get_parallel_line_xys(xys[i], xys[i + 1])
            parallel_lines.append((xy1, xy2))

        points: List[Tuple[float, float]] = []
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
