# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's line feature implementation module."""

import math
from typing import List, Literal, Optional, Tuple, Union

from matplotlib.patches import ConnectionStyle, FancyArrowPatch
from matplotlib.path import Path

import drawlib.v0_2.private.validators.args as validator
from drawlib.v0_2.private.core.model import LineStyle
from drawlib.v0_2.private.core.util import LineUtil
from drawlib.v0_2.private.core_canvas.base import CanvasBase
from drawlib.v0_2.private.util import error_handler


class CanvasLineFeature(CanvasBase):
    """A class representing a canvas with line drawing features.

    This class extends CanvasBase and provides methods for drawing various types of lines
    on a canvas, including straight lines, curved lines, and Bezier curves.

    Attributes:
        None
    """

    def __init__(self) -> None:
        """Initialize the CanvasLineFeature object.

        This constructor initializes the CanvasLineFeature object by calling the constructor
        of its superclass CanvasBase.

        Args:
            None

        Returns:
            None
        """
        super().__init__()

    @error_handler
    def line(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw straight line from xy1 to xy2.

        Args:
            xy1 (Tuple[float, float]): Starting point of the line.
            xy2 (Tuple[float, float]): Ending point of the line.
            width (Optional[float]): Optional width of the line.
            arrowhead (Literal["", "->", "<-", "<->"]):
                    Optional arrowhead style ("", "->", "<-", "<->").
            style (Union[LineStyle, str, None]): Optional line style.

        Returns:
            None
        """
        # validation at here for better error message.
        # validated again at lines_bezier().

        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())

        self.lines_bezier(
            xy1,
            path_points=[xy2],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @error_handler
    def line_curved(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        bend: float,
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw curved line from xy1 to xy2.

        Args:
            xy1: Tuple[float, float]: Starting point of the line.
            xy2: Tuple[float, float]: Ending point of the line.
            bend: float: Additional line length between xy1 and xy2. 0 is straight.
            width: Optional[float]: Optional width of the line.
            arrowhead: Literal["", "->", "<-", "<->"]: Optional arrowhead style ("", "->", "<-", "<->").
            style: Union[LineStyle, str, None]: Optional line style.

        Returns:
            None
        """
        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())
        if width is not None:
            style.width = width

        options = LineUtil.get_fancyarrowpatch_options(arrowhead, style)
        self._artists.append(
            FancyArrowPatch(
                posA=xy1,
                posB=xy2,
                connectionstyle=ConnectionStyle.Arc3(rad=bend),  # type: ignore
                **options,
            )
        )

    @error_handler
    def line_bezier1(
        self,
        xy1: Tuple[float, float],
        cp: Tuple[float, float],
        xy2: Tuple[float, float],
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw Bezier line from xy1 to xy2 with 1 control point.

        Args:
            xy1: Tuple[float, float]: Starting point of the line.
            cp: Tuple[float, float]: Control point for the curve.
            xy2: Tuple[float, float]: Ending point of the line.
            width: Optional[float]: Optional width of the line.
            arrowhead: Literal["", "->", "<-", "<->"]: Optional arrowhead style ("", "->", "<-", "<->").
            style: Union[LineStyle, str, None]: Optional line style.

        Returns:
            None
        """
        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())

        self.lines_bezier(
            xy1,
            path_points=[(cp, xy2)],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @error_handler
    def line_bezier2(
        self,
        xy1: Tuple[float, float],
        cp1: Tuple[float, float],
        cp2: Tuple[float, float],
        xy2: Tuple[float, float],
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw Bezier line from xy1 to xy2 with 2 control points.

        Args:
            xy1: Tuple[float, float]: Starting point of the line.
            cp1: Tuple[float, float]: First control point for the curve.
            cp2: Tuple[float, float]: Second control point for the curve.
            xy2: Tuple[float, float]: Ending point of the line.
            width: Optional[float]: Optional width of the line.
            arrowhead: Literal["", "->", "<-", "<->"]: Optional arrowhead style ("", "->", "<-", "<->").
            style: Union[LineStyle, str, None]: Optional line style.

        Returns:
            None
        """
        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())

        self.lines_bezier(
            xy1,
            path_points=[(cp1, cp2, xy2)],
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @error_handler
    def lines(
        self,
        xys: List[Tuple[float, float]],
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw multiple connected lines.

        Args:
            xys: List[Tuple[float, float]]: List of points defining the lines.
            width: Optional[float]: Optional width of the lines.
            arrowhead: Literal["", "->", "<-", "<->"]: Optional arrowhead style ("", "->", "<-", "<->").
            style: Union[LineStyle, str, None]: Optional line style.

        Returns:
            None
        """
        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())

        self.lines_bezier(
            xy=xys[0],
            path_points=xys[1:],  # type: ignore
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @error_handler
    def lines_curved(
        self,
        xys: List[Tuple[float, float]],
        r: float,
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw curved lines connecting multiple points.

        Args:
            xys: List[Tuple[float, float]]: List of points defining the lines.
            r: float: Radius of curvature for the lines.
            width: Optional[float]: Optional width of the lines.
            arrowhead: Literal["", "->", "<-", "<->"]: Optional arrowhead style ("", "->", "<-", "<->").
            style: Union[LineStyle, str, None]: Optional line style.

        Returns:
            None
        """
        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())
        if len(xys) == 2:
            self.lines(xys, width=width, arrowhead=arrowhead, style=style)
            return

        path_points = []
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

        self.lines_bezier(
            xy=xys[0],
            path_points=path_points,
            width=width,
            arrowhead=arrowhead,
            style=style,
        )

    @error_handler
    def lines_bezier(
        self,
        xy: Tuple[float, float],
        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ],
        width: Optional[float] = None,
        arrowhead: Literal["", "->", "<-", "<->"] = "",
        style: Union[LineStyle, str, None] = None,
    ) -> None:
        """Draw Bezier lines based on given path points.

        Args:
            xy: Tuple[float, float]: Starting point of the line.
            path_points: List of path points and control points.
            width: Optional[float]: Optional width of the lines.
            arrowhead: Literal["", "->", "<-", "<->"]: Optional arrowhead style ("", "->", "<-", "<->").
            style: Union[LineStyle, str, None]: Optional line style.

        Returns:
            None
        """
        style = LineUtil.format_style(style)
        validator.validate_line_args(locals())

        if width is not None:
            style.width = width

        # create Path
        vertices = [xy]
        codes = [Path.MOVETO]
        for p in path_points:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError()
            if length == 2:
                if isinstance(p[0], tuple):
                    # 2 points
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
