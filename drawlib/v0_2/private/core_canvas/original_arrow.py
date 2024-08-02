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
from typing import List, Literal, Optional, Tuple, Union

from matplotlib.patches import PathPatch
from matplotlib.path import Path

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.core.theme import dtheme
from drawlib.v0_2.private.core.util import ShapeUtil
from drawlib.v0_2.private.core_canvas.base import CanvasBase
from drawlib.v0_2.private.core_canvas.line import LineArcHelper
from drawlib.v0_2.private.util import (
    error_handler,
    get_angle,
    get_distance,
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
    def arrows(
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

        parallel_xys1 = ArrowsHelper.get_parallel_lines_xys(xys, tail_width / 2)
        parallel_xys2 = ArrowsHelper.get_parallel_lines_xys(xys, tail_width / 2 * -1)

        arrowhead_start_tail_xy1 = ArrowsHelper.get_point_on_line(parallel_xys1[0], parallel_xys1[1], head_length)
        arrowhead_start_tail_xy2 = ArrowsHelper.get_point_on_line(parallel_xys2[0], parallel_xys2[1], head_length)
        arrowhead_end_tail_xy1 = ArrowsHelper.get_point_on_line(
            parallel_xys1[len(parallel_xys1) - 1],
            parallel_xys1[len(parallel_xys1) - 2],
            head_length,
        )
        arrowhead_end_tail_xy2 = ArrowsHelper.get_point_on_line(
            parallel_xys2[len(parallel_xys1) - 1],
            parallel_xys2[len(parallel_xys1) - 2],
            head_length,
        )

        xy1, xy2 = ArrowsHelper.get_parallel_line_xys(xys[0], xys[1], head_width / 2)
        arrowhead_start_head_xy1 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)
        xy1, xy2 = ArrowsHelper.get_parallel_line_xys(xys[0], xys[1], head_width / 2 * -1)
        arrowhead_start_head_xy2 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)
        xy1, xy2 = ArrowsHelper.get_parallel_line_xys(
            xys[len(xys) - 1], xys[len(xys) - 2], head_width / 2 * -1
        )  # since poinrts are reversed, having * -1 here
        arrowhead_end_head_xy1 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)
        xy1, xy2 = ArrowsHelper.get_parallel_line_xys(xys[len(xys) - 1], xys[len(xys) - 2], head_width / 2)
        arrowhead_end_head_xy2 = ArrowsHelper.get_point_on_line(xy1, xy2, head_length)

        points1: List[Tuple[float, float]] = []
        if head == "->":
            points1.append(parallel_xys1[0])
        else:
            points1.append(arrowhead_start_tail_xy1)
        points1.extend(parallel_xys1[1:-1])
        if head == "<-":
            points1.append(parallel_xys1[len(parallel_xys1) - 1])
        else:
            points1.append(arrowhead_end_tail_xy1)

        points2: List[Tuple[float, float]] = []
        if head == "<-":
            points2.append(parallel_xys2[len(parallel_xys2) - 1])
        else:
            points2.append(arrowhead_end_tail_xy2)
        temp = parallel_xys2[1:-1]
        temp.reverse()
        points2.extend(temp)
        if head == "->":
            points2.append(parallel_xys2[0])
        else:
            points2.append(arrowhead_start_tail_xy2)

        # apply r here
        if r != 0:
            path_points1: List[
                Union[
                    Tuple[float, float],
                    Tuple[Tuple[float, float], Tuple[float, float]],
                    Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
                ]
            ] = ArrowsHelper.get_path_points(points1, r)
            path_points2: List[
                Union[
                    Tuple[float, float],
                    Tuple[Tuple[float, float], Tuple[float, float]],
                    Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
                ]
            ] = ArrowsHelper.get_path_points(points2, r)
        else:
            path_points1 = points1  # type: ignore
            path_points2 = points2  # type: ignore

        if head != "->":
            path_points1.insert(0, xys[0])
            path_points1.insert(1, arrowhead_start_head_xy1)
        if head != "<-":
            path_points1.append(arrowhead_end_head_xy1)
            path_points1.append(xys[len(xys) - 1])

        if head != "<-":
            path_points2.insert(0, arrowhead_end_head_xy2)
        if head != "->":
            path_points2.append(arrowhead_start_head_xy2)

        path_points1.extend(path_points2)

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
    def arrow_arc(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        tail_width: float,
        head_width: float,
        head_angle: float = 10,
        head: Literal["->", "<-", "<->"] = "->",
        from_angle: float = 0,
        to_angle: float = 180,
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
            from_angle: float: The starting angle of the arc in degrees (default is 0).
            to_angle: float: The ending angle of the arc in degrees (default is 180).
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
            from_angle2 = from_angle + head_angle
            from_angle2 %= 360
        else:
            from_angle2 = from_angle

        if head in {"->", "<->"}:
            to_angle2 = to_angle - head_angle
            to_angle2 %= 360
        else:
            to_angle2 = to_angle

        if from_angle2 > to_angle2:
            pp1_fa = -1 * (360 - from_angle2)
            pp1_ta = to_angle2
            pp2_fa = to_angle2
            pp2_ta = pp1_fa
        else:
            pp1_fa = from_angle2
            pp1_ta = to_angle2
            pp2_fa = to_angle2
            pp2_ta = from_angle2

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

        if from_angle > to_angle:
            from_angle = -1 * (360 - from_angle)

        if head in {"<-", "<->"}:
            path_points1.insert(
                0,
                LineArcHelper.get_point_on_ellipse(
                    xy,
                    width,
                    height,
                    from_angle,
                ),
            )
            path_points1.insert(
                1,
                LineArcHelper.get_point_on_ellipse(
                    xy,
                    width - head_width,
                    height - head_width,
                    from_angle2,
                ),
            )
            path_points2.append(
                LineArcHelper.get_point_on_ellipse(
                    xy,
                    width + head_width,
                    height + head_width,
                    from_angle2,
                )
            )

        if head in {"->", "<->"}:
            path_points1.append(
                LineArcHelper.get_point_on_ellipse(
                    xy,
                    width - head_width,
                    height - head_width,
                    to_angle2,
                )
            )
            path_points1.append(
                LineArcHelper.get_point_on_ellipse(
                    xy,
                    width,
                    height,
                    to_angle,
                )
            )
            path_points2.insert(
                0,
                LineArcHelper.get_point_on_ellipse(
                    xy,
                    width + head_width,
                    height + head_width,
                    to_angle2,
                ),
            )

        path_points1.extend(path_points2)

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


class ArrowsHelper:
    """Internal class"""

    @classmethod
    def get_path_points(
        cls,
        xys: List[Tuple[float, float]],
        r: float,
    ) -> List[
        Union[
            Tuple[float, float],
            Tuple[Tuple[float, float], Tuple[float, float]],
            Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
        ]
    ]:
        """Internal function"""

        def _get_mid_points(
            a: Tuple[float, float],
            b: Tuple[float, float],
            r: float,
        ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
            # Calculate the vector from A to B
            ab = [b[0] - a[0], b[1] - a[1]]

            # Calculate the distance from A to B
            ab_distance = math.sqrt(ab[0] ** 2 + ab[1] ** 2)

            # Normalize the vector AB to get the unit vector
            ab_unit = [ab[0] / ab_distance, ab[1] / ab_distance]

            # Calculate point C: A + X * unit vector AB
            c = (a[0] + r * ab_unit[0], a[1] + r * ab_unit[1])

            # Calculate point D: B - X * unit vector AB
            d = (b[0] - r * ab_unit[0], b[1] - r * ab_unit[1])

            return c, d

        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ] = []

        last_i = len(xys) - 2
        # last_xy = (0, 0)
        for i, xy in enumerate(xys):
            if i == 0:
                _, p = _get_mid_points(xy, xys[i + 1], r)
                path_points.append(p)
                continue

            if i == last_i:
                p, _ = _get_mid_points(xy, xys[i + 1], r)
                path_points.append((xy, p))
                path_points.append(xys[i + 1])
                break

            p1, p2 = _get_mid_points(xy, xys[i + 1], r)
            path_points.append((xy, p1))
            path_points.append(p2)

        path_points.insert(0, xys[0])
        return path_points

    @classmethod
    def get_point_on_line(
        cls,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        distance: float,
    ) -> Tuple[float, float]:
        """Internal function"""
        x1, y1 = xy1
        x2, y2 = xy2

        v_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        u_x = (x2 - x1) / v_length
        u_y = (y2 - y1) / v_length

        x = x1 + distance * u_x
        y = y1 + distance * u_y

        return (x, y)

    @classmethod
    def get_parallel_lines_xys(
        cls,
        xys: List[Tuple[float, float]],
        distance: float,
    ) -> List[Tuple[float, float]]:
        """Internal function"""
        parallel_lines: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []
        for i in range(len(xys) - 1):
            xy1, xy2 = cls.get_parallel_line_xys(xys[i], xys[i + 1], distance)
            parallel_lines.append((xy1, xy2))

        points: List[Tuple[float, float]] = []
        for i in range(len(parallel_lines) - 1):
            xy1, xy2 = parallel_lines[i]
            xy3, xy4 = parallel_lines[i + 1]
            xy = cls.find_lines_intersection(xy1, xy2, xy3, xy4)
            points.append(xy)

        first_point = parallel_lines[0][0]
        last_point = parallel_lines[len(parallel_lines) - 1][1]

        points.insert(0, first_point)
        points.append(last_point)

        return points

    @classmethod
    def get_parallel_line_xys(
        cls,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        distance: float,
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

    @classmethod
    def find_lines_intersection(
        cls,
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

        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3

        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

        return (x, y)
