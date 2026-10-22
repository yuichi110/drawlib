# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's line feature implementation module."""

from __future__ import annotations

from typing import cast

from matplotlib.patches import ConnectionStyle, FancyArrowPatch
from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    ArrowHead,
    Bend,
    Bezier2,
    Bezier3,
    Coordinate,
    Coordinates,
    PathPoints,
    PosFloat,
)
from drawlib._core.l3_math import get_rotated_path_points
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas._line_utils import LineArcHelper, LineUtils


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
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw straight line from xy1 to xy2.

        Args:
            xy1 (tuple[float, float]): Starting point of the line.
            xy2 (tuple[float, float]): Ending point of the line.
            style (Style): Line style (required).
            arrow_head (Literal["->", "<-", "<->", "-"] | str): Optional arrowhead style.
        """
        style.validate_for("line")

        self.lines_bezier(
            xy1,
            path_points=[xy2],
            arrow_head=arrow_head,
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
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw curved line from xy1 to xy2.

        Args:
            xy1: tuple[float, float]: Starting point of the line.
            xy2: tuple[float, float]: Ending point of the line.
            style: Style: Line style (required).
            bend: float: Additional line length between xy1 and xy2. 0 is straight.
            arrow_head: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style.validate_for("line")

        options = LineUtils.get_fancyarrowpatch_options(arrow_head, style)
        self._artists.append(
            FancyArrowPatch(
                posA=xy1,
                posB=xy2,
                connectionstyle=ConnectionStyle("arc3", rad=bend),
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
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw Bezier line from xy1 to xy2 with 1 control point.

        Args:
            xy1: tuple[float, float]: Starting point of the line.
            xy2: tuple[float, float]: Ending point of the line.
            cp: tuple[float, float]: Control point for the curve.
            style: Style: Line style (required).
            arrow_head: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style.validate_for("line")

        self.lines_bezier(
            xy1,
            path_points=[(cp, xy2)],
            arrow_head=arrow_head,
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
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw Bezier line from xy1 to xy2 with 2 control points.

        Args:
            xy1: tuple[float, float]: Starting point of the line.
            xy2: tuple[float, float]: Ending point of the line.
            cp1: tuple[float, float]: First control point for the curve.
            cp2: tuple[float, float]: Second control point for the curve.
            style: Style: Line style (required).
            arrow_head: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
        """
        style.validate_for("line")

        self.lines_bezier(
            xy1,
            path_points=[(cp1, cp2, xy2)],
            arrow_head=arrow_head,
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
        arrow_head: ArrowHead = "",
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
            arrow_head: Literal["->", "<-", "<->", "-"] | str: Optional arrowhead style.
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
            path_points = get_rotated_path_points(path_points, xy, angle)

        start_point = cast(Coordinate, path_points[0])
        rest_points: PathPoints = path_points[1:]

        self.lines_bezier(
            start_point,
            path_points=rest_points,
            arrow_head=arrow_head,
            style=style,
        )

    @validate_call
    def lines(
        self,
        xys: Coordinates,
        *,
        style: Style,
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw multiple connected lines.

        Args:
            xys: list[tuple[float, float]]: List of points defining the lines.
            style: Style: Line style (required).
            arrow_head (Literal["->", "<-", "<->", "-"] | str): Optional arrowhead style.
        """
        style.validate_for("line")
        xys = LineUtils._remove_consecutive_duplicates(list(xys))
        rest_points: PathPoints = list(xys[1:])
        self.lines_bezier(
            xy=xys[0],
            path_points=rest_points,
            arrow_head=arrow_head,
            style=style,
        )

    @validate_call
    def lines_curved(
        self,
        xys: Coordinates,
        r: PosFloat,
        *,
        style: Style,
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw curved lines connecting multiple points.

        Args:
            xys: list[tuple[float, float]]: List of points defining the lines.
            r: float: Radius of curvature for the lines.
            style: Style: Line style (required).
            arrow_head (Literal["->", "<-", "<->", "-"] | str): Optional arrowhead style.
        """
        style.validate_for("line")

        if len(xys) == 2:
            self.line(xys[0], xys[1], arrow_head=arrow_head, style=style)
            return

        xys = LineUtils._remove_consecutive_duplicates(list(xys))
        path_points: PathPoints = []
        last_i = len(xys) - 2
        for i, xy in enumerate(xys):
            if i == 0:
                _, p = LineUtils.get_mid_points(xy, xys[i + 1], r)
                path_points.append(p)
                continue

            if i == last_i:
                p, _ = LineUtils.get_mid_points(xy, xys[i + 1], r)
                path_points.append((xy, p))
                path_points.append(xys[i + 1])
                break

            p1, p2 = LineUtils.get_mid_points(xy, xys[i + 1], r)
            path_points.append((xy, p1))
            path_points.append(p2)

        self.lines_bezier(
            xy=xys[0],
            path_points=path_points,
            arrow_head=arrow_head,
            style=style,
        )

    @validate_call
    def lines_bezier(
        self,
        xy: Coordinate,
        path_points: PathPoints,
        *,
        style: Style,
        arrow_head: ArrowHead = "",
    ) -> None:
        """Draw Bezier lines based on given path points.

        Args:
            xy: tuple[float, float]: Starting point of the line.
            path_points: List of path points and control points.
            style: Style: Line style (required).
            arrow_head (Literal["->", "<-", "<->", "-"] | str): Optional arrowhead style.
        """
        style.validate_for("line")

        # create Path
        vertices: list[Coordinate] = [xy]
        codes = [Path.MOVETO]
        for p in path_points:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError()
            if length == 2:
                if isinstance(p[0], tuple):
                    p2 = cast(Bezier2, p)
                    vertices.extend([p2[0], p2[1]])
                    codes.extend([Path.CURVE3] * 2)
                else:
                    pt = cast(Coordinate, p)
                    vertices.append(pt)
                    codes.append(Path.LINETO)
            else:
                p3 = cast(Bezier3, p)
                vertices.extend([p3[0], p3[1], p3[2]])
                codes.extend([Path.CURVE4] * 3)

        path = Path(vertices=vertices, codes=codes)
        options = LineUtils.get_fancyarrowpatch_options(arrow_head, style)
        self._artists.append(FancyArrowPatch(path=path, **options))


__all__ = [
    "CanvasLineFeature",
]
