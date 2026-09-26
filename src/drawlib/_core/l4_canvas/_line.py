# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's line feature implementation module."""

import math
from typing import Literal

from matplotlib.patches import ConnectionStyle, FancyArrowPatch
from matplotlib.path import Path

from drawlib._core.l1_core import guarded
from drawlib._core.l2_types import (
    TypeAngle,
    TypeArrowHead,
    TypeBend,
    TypeCoordinate,
    TypeCoordinates,
    TypePathPoints,
    TypePosFloat,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import LineUtil, get_rotated_path_points


class CanvasLineFeature(CanvasBase):
    """A class representing a canvas with line drawing features."""

    def __init__(self) -> None:
        """Initialize the CanvasLineFeature object."""
        super().__init__()

    @guarded
    def line(
        self,
        xy1: TypeCoordinate,
        xy2: TypeCoordinate,
        *,
        style: Style,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw straight line from xy1 to xy2.

        Args:
            xy1 (tuple[float, float]): Starting point of the line.
            xy2 (tuple[float, float]): Ending point of the line.
            style (Style): Line style (required).
            width (float | None): Optional width of the line override.
            arrowhead (Literal["->", "<-", "<->", "-"] | str): Optional arrowhead style.
        """
        style = LineUtil.format_style(style)

        self.lines_bezier(
            xy1,
            path_points=[xy2],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @guarded
    def line_curved(
        self,
        xy1: TypeCoordinate,
        xy2: TypeCoordinate,
        *,
        style: Style,
        bend: TypeBend = 0,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw curved line from xy1 to xy2.

        Args:
            xy1: tuple[float, float]: Starting point of the line.
            xy2: tuple[float, float]: Ending point of the line.
            style: Style: Line style (required).
            bend: float: Additional line length between xy1 and xy2. 0 is straight.
            width: float | None: Optional width of the line override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style = LineUtil.format_style(style)
        if width is not None:
            style = style.patch(line_width=width)

        options = LineUtil.get_fancyarrowpatch_options(arrowhead, style)
        self._artists.append(
            FancyArrowPatch(
                posA=xy1,
                posB=xy2,
                connectionstyle=ConnectionStyle.Arc3(rad=bend),  # type: ignore
                **options,
            )
        )

    @guarded
    def line_bezier1(
        self,
        xy1: TypeCoordinate,
        xy2: TypeCoordinate,
        cp: TypeCoordinate,
        *,
        style: Style,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw Bezier line from xy1 to xy2 with 1 control point.

        Args:
            xy1: tuple[float, float]: Starting point of the line.
            xy2: tuple[float, float]: Ending point of the line.
            cp: tuple[float, float]: Control point for the curve.
            style: Style: Line style (required).
            width: float | None: Optional width of the line override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style = LineUtil.format_style(style)

        self.lines_bezier(
            xy1,
            path_points=[(cp, xy2)],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @guarded
    def line_bezier2(
        self,
        xy1: TypeCoordinate,
        xy2: TypeCoordinate,
        cp1: TypeCoordinate,
        cp2: TypeCoordinate,
        *,
        style: Style,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw Bezier line from xy1 to xy2 with 2 control points.

        Args:
            xy1: tuple[float, float]: Starting point of the line.
            xy2: tuple[float, float]: Ending point of the line.
            cp1: tuple[float, float]: First control point for the curve.
            cp2: tuple[float, float]: Second control point for the curve.
            xy2: tuple[float, float]: Ending point of the line.
            style: Style: Line style (required).
            width: float | None: Optional width of the line override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style = LineUtil.format_style(style)

        self.lines_bezier(
            xy1,
            path_points=[(cp1, cp2, xy2)],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @guarded
    def line_arc(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        *,
        style: Style,
        angle_start: TypeAngle = 0,
        angle_end: TypeAngle = 180,
        angle: TypeAngle = 0,
        linewidth: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
        ccw: bool = True,
    ) -> None:
        """Draw arc line on ellipse.

        Args:
            xy: tuple[float, float]: The center point of the ellipse from which the arc is drawn.
            width: float: The width of the ellipse.
            height: float: The height of the ellipse.
            style: Style: Line style (required).
            angle_start: float: The starting angle of the arc in degrees.
            angle_end: float: The ending angle of the arc in degrees.
            angle: float: The angle of ellipse.
            linewidth: float | None: Optional width of the line override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
            ccw: bool: Counter-clockwise direction if True.
        """
        style = LineUtil.format_style(style)

        diff = angle_end - angle_start
        if diff == 0:
            diff = 360.0 if ccw else -360.0
        elif ccw:
            while diff < 0:
                diff += 360
        else:
            while diff > 0:
                diff -= 360
        effective_angle_end = angle_start + diff

        path_points = LineArcHelper.get_ellipse_path_points(
            xy,
            width,
            height,
            angle_start,
            effective_angle_end,
        )

        if angle != 0:
            path_points = get_rotated_path_points(path_points, xy, angle)  # type: ignore

        start_point = path_points[0]
        path_points = path_points[1:]

        self.lines_bezier(
            start_point,  # type: ignore
            path_points=path_points,  # type: ignore
            width=linewidth,
            arrowhead=arrowhead,
            style=style,
        )

    @guarded
    def lines(
        self,
        xys: TypeCoordinates,
        *,
        style: Style,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw multiple connected lines.

        Args:
            xys: list[tuple[float, float]]: List of points defining the lines.
            style: Style: Line style (required).
            width: float | None: Optional width of the lines override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style = LineUtil.format_style(style)
        xys = LineUtil._remove_consecutive_duplicates(list(xys))
        self.lines_bezier(
            xy=xys[0],
            path_points=xys[1:],  # type: ignore
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @guarded
    def lines_curved(
        self,
        xys: TypeCoordinates,
        r: TypePosFloat,
        *,
        style: Style,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw curved lines connecting multiple points.

        Args:
            xys: list[tuple[float, float]]: List of points defining the lines.
            r: float: Radius of curvature for the lines.
            style: Style: Line style (required).
            width: float | None: Optional width of the lines override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style = LineUtil.format_style(style)

        if len(xys) == 2:
            self.line(xys[0], xys[1], width=width, arrowhead=arrowhead, style=style)
            return

        xys = LineUtil._remove_consecutive_duplicates(list(xys))
        path_points = []
        last_i = len(xys) - 2
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

        self.lines_bezier(
            xy=xys[0],
            path_points=path_points,
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @guarded
    def lines_bezier(
        self,
        xy: TypeCoordinate,
        path_points: TypePathPoints,
        *,
        style: Style,
        width: TypePosFloat | None = None,
        arrowhead: TypeArrowHead = "",
    ) -> None:
        """Draw Bezier lines based on given path points.

        Args:
            xy: tuple[float, float]: Starting point of the line.
            path_points: List of path points and control points.
            style: Style: Line style (required).
            width: float | None: Optional width of the lines override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style = LineUtil.format_style(style)

        if width is not None:
            style = style.patch(line_width=width)

        # create Path
        vertices = [xy]
        codes = [Path.MOVETO]
        for p in path_points:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError()
            if length == 2:
                if isinstance(p[0], tuple):
                    vertices.extend([p[0], p[1]])  # type: ignore
                    codes.extend([Path.CURVE3] * 2)
                else:
                    vertices.append(p)  # type: ignore
                    codes.append(Path.LINETO)
            else:
                vertices.extend([p[0], p[1], p[2]])  # type: ignore
                codes.extend([Path.CURVE4] * 3)

        path = Path(vertices=vertices, codes=codes)
        options = LineUtil.get_fancyarrowpatch_options(arrowhead, style)
        self._artists.append(FancyArrowPatch(path=path, **options))


class LineArcHelper:
    """Internal class"""

    @classmethod
    def get_point_on_ellipse(
        cls,
        xy: TypeCoordinate,
        width: float,
        height: float,
        angle: float,
    ) -> tuple[float, float]:
        """Get coordinates of a point on an ellipse at a given angle."""
        x, y = xy
        angle_rad = math.radians(angle)
        point_x = x + (width / 2) * math.cos(angle_rad)
        point_y = y + (height / 2) * math.sin(angle_rad)
        return (point_x, point_y)

    @classmethod
    def get_ellipse_path_points(
        cls,
        xy: TypeCoordinate,
        width: float,
        height: float,
        angle_start: float,
        angle_end: float,
    ) -> list[tuple[float, float] | tuple[tuple[float, float], tuple[float, float], tuple[float, float]]]:
        """Get bezier path points along an ellipse arc."""
        diff = angle_end - angle_start
        if diff == 0:
            return [cls.get_point_on_ellipse(xy, width, height, angle_start)]

        sweep = abs(diff)
        num_segments = max(1, math.ceil(sweep / 90.0))
        step = diff / num_segments
        path_points: list[
            tuple[float, float] | tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
        ] = []
        start: tuple[float, float] | None = None
        for i in range(num_segments):
            a_start = angle_start + i * step
            a_end = angle_start + (i + 1) * step
            p1, p2, p3, p4 = cls.bezier_ellipse_arc_approximation(
                xy,
                width,
                height,
                a_start,
                a_end,
            )
            if start is None:
                start = p1
            path_points.append((p2, p3, p4))

        if start is not None:
            path_points.insert(0, start)
        return path_points

    @classmethod
    def bezier_ellipse_arc_approximation(
        cls,
        xy: TypeCoordinate,
        width: float,
        height: float,
        start_angle: float,
        end_angle: float,
    ) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        """Calculate Bezier curve approximation points for an elliptical arc."""
        x, y = xy

        start_angle_rad = math.radians(start_angle)
        end_angle_rad = math.radians(end_angle)

        start_point = (x + width / 2 * math.cos(start_angle_rad), y + height / 2 * math.sin(start_angle_rad))
        end_point = (x + width / 2 * math.cos(end_angle_rad), y + height / 2 * math.sin(end_angle_rad))

        t = (4 / 3) * math.tan((end_angle_rad - start_angle_rad) / 4)
        control_point1 = (
            start_point[0] - t * width / 2 * math.sin(start_angle_rad),
            start_point[1] + t * height / 2 * math.cos(start_angle_rad),
        )
        control_point2 = (
            end_point[0] + t * width / 2 * math.sin(end_angle_rad),
            end_point[1] - t * height / 2 * math.cos(end_angle_rad),
        )

        return start_point, control_point1, control_point2, end_point


def _get_mid_points(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    r: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    x1, y1 = xy1
    x2, y2 = xy2
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if dist == 0:
        return xy1, xy2

    ratio = min(r / dist, 0.5)
    p1 = (x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio)
    p2 = (x2 - (x2 - x1) * ratio, y2 - (y2 - y1) * ratio)
    return p1, p2
