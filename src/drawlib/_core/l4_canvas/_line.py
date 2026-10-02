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
from typing import Any, Literal

from matplotlib.patches import ConnectionStyle, FancyArrowPatch
from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    ArrowHead,
    Bend,
    Coordinate,
    Coordinates,
    PathPoints,
    PosFloat,
)
from drawlib._core.l3_math import get_rotated_path_points
from drawlib._core.l3_styles import ColorUtil, Style
from drawlib._core.l4_canvas._base import CanvasBase


class LineUtil:
    """A utility class for handling line styles and options."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def _remove_consecutive_duplicates(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Remove consecutive duplicate points from a list of coordinates."""
        return [v for i, v in enumerate(xys) if i == 0 or v != xys[i - 1]]

    @staticmethod
    def _merge_straight_lines(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:  # noqa: C901
        """Merge consecutive points that form a straight line."""
        if len(xys) < 3:
            return xys

        points: list[tuple[float, float]] = []
        skip_next = False
        for i in range(len(xys) - 1):
            if skip_next:
                skip_next = False
                continue

            if i == 0:
                points.append(xys[i])
                continue

            p_prev = points[-1]
            p_curr = xys[i]
            p_next = xys[i + 1]

            if p_prev[0] == p_curr[0] == p_next[0] or p_prev[1] == p_curr[1] == p_next[1]:
                continue

            points.append(p_curr)

        points.append(xys[-1])
        return points

    @staticmethod
    def sanitize_xys(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Sanitize a list of coordinates by removing duplicates and merging straight lines."""
        xys = LineUtil._remove_consecutive_duplicates(xys)
        return LineUtil._merge_straight_lines(xys)

    @staticmethod
    def validate_line_style(style: Style) -> None:
        """Validate that the Style supports line drawing."""
        style.validate_for("line")

    @staticmethod
    def format_style(style: Style) -> Style:
        """Validate and return line style."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
        style.validate_for("line")
        return style

    @staticmethod
    def get_fancyarrowpatch_options(
        arrowhead: ArrowHead,
        style: Style,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's FancyArrowPatch options."""
        color = None if style.line_color is None else ColorUtil.get_mplot_rgba(style.line_color)
        options: dict[str, Any] = {
            "linewidth": style.line_width,
            "linestyle": style.line_style if style.line_style is not None else "solid",
            "color": color,
            "alpha": style.line_alpha,
        }

        if not arrowhead:
            options["arrowstyle"] = "-"
        else:
            scale = style.line_arrow_head_scale if style.line_arrow_head_scale is not None else 20.0
            options["mutation_scale"] = scale
            if style.line_arrow_head_fill:
                if arrowhead == "->":
                    options["arrowstyle"] = "-|>"
                elif arrowhead == "<-":
                    options["arrowstyle"] = "<|-"
                else:
                    options["arrowstyle"] = "<|-|>"
            else:
                options["arrowstyle"] = arrowhead

        return {k: v for k, v in options.items() if v is not None}


class CanvasLineFeature(CanvasBase):
    """A class representing a canvas with line drawing features."""

    def __init__(self) -> None:
        """Initialize the CanvasLineFeature object."""
        super().__init__()

    @validate_call
    def line(
        self,
        xy1: Coordinate,
        xy2: Coordinate,
        *,
        style: Style,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
    ) -> None:
        """Draw straight line from xy1 to xy2.

        Args:
            xy1 (tuple[float, float]): Starting point of the line.
            xy2 (tuple[float, float]): Ending point of the line.
            style (Style): Line style (required).
            width (float | None): Optional width of the line override.
            arrowhead (Literal["->", "<-", "<->", "-"] | str): Optional arrowhead style.
        """
        style.validate_for("line")

        self.lines_bezier(
            xy1,
            path_points=[xy2],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @validate_call
    def line_curved(
        self,
        xy1: Coordinate,
        xy2: Coordinate,
        *,
        style: Style,
        bend: Bend = 0,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
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
        style.validate_for("line")
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

    @validate_call
    def line_bezier1(
        self,
        xy1: Coordinate,
        xy2: Coordinate,
        cp: Coordinate,
        *,
        style: Style,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
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
        style.validate_for("line")

        self.lines_bezier(
            xy1,
            path_points=[(cp, xy2)],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @validate_call
    def line_bezier2(
        self,
        xy1: Coordinate,
        xy2: Coordinate,
        cp1: Coordinate,
        cp2: Coordinate,
        *,
        style: Style,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
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
        style.validate_for("line")

        self.lines_bezier(
            xy1,
            path_points=[(cp1, cp2, xy2)],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @validate_call
    def line_arc(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        angle_start: Angle = 0,
        angle_end: Angle = 180,
        angle: Angle = 0,
        linewidth: PosFloat | None = None,
        arrowhead: ArrowHead = "",
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
        style.validate_for("line")

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

    @validate_call
    def lines(
        self,
        xys: Coordinates,
        *,
        style: Style,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
    ) -> None:
        """Draw multiple connected lines.

        Args:
            xys: list[tuple[float, float]]: List of points defining the lines.
            style: Style: Line style (required).
            width: float | None: Optional width of the lines override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style.validate_for("line")
        xys = LineUtil._remove_consecutive_duplicates(list(xys))
        self.lines_bezier(
            xy=xys[0],
            path_points=xys[1:],  # type: ignore
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @validate_call
    def lines_curved(
        self,
        xys: Coordinates,
        r: PosFloat,
        *,
        style: Style,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
    ) -> None:
        """Draw curved lines connecting multiple points.

        Args:
            xys: list[tuple[float, float]]: List of points defining the lines.
            r: float: Radius of curvature for the lines.
            style: Style: Line style (required).
            width: float | None: Optional width of the lines override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style.validate_for("line")

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

    @validate_call
    def lines_bezier(
        self,
        xy: Coordinate,
        path_points: PathPoints,
        *,
        style: Style,
        width: PosFloat | None = None,
        arrowhead: ArrowHead = "",
    ) -> None:
        """Draw Bezier lines based on given path points.

        Args:
            xy: tuple[float, float]: Starting point of the line.
            path_points: List of path points and control points.
            style: Style: Line style (required).
            width: float | None: Optional width of the lines override.
            arrowhead: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style.validate_for("line")

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
        xy: Coordinate,
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
        xy: Coordinate,
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
        xy: Coordinate,
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
