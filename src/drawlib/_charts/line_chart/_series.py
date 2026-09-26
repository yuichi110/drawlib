# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Series models for line and area charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType, LineStyle, PointShape

if TYPE_CHECKING:
    from drawlib._core.types import Style


class LineSeries:
    """Represents a data series in a line chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        style: Style | None = None,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape = "circle",
        point_size: float = 0.7,
    ) -> None:
        """Initialize LineSeries.

        Args:
            name: Series name displayed in legend.
            values: Numerical values corresponding to categories.
            color: Primary stroke and point color.
            style: Optional Style overriding line and marker appearance.
            line_width: Stroke width for the series polyline. Defaults to 2.0.
            line_style: Stroke style ("solid", "dashed", "dotted"). Defaults to "solid".
            point_shape: Marker shape ("circle", "square", "none"). Defaults to "circle".
            point_size: Radius or half-width of data point markers. Defaults to 0.7.
        """
        self.name = name
        self.values: list[float] = [float(v) for v in values]
        self.color: ColorType | None = color
        self.style: Style | None = style
        self.line_width: float = float(line_width)
        self.line_style: LineStyle = line_style
        self.point_shape: PointShape = point_shape
        self.point_size: float = float(point_size)


class AreaSeries:
    """Represents a data series in an area chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        style: Style | None = None,
        fill_alpha: float = 0.35,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape = "none",
        point_size: float = 0.7,
    ) -> None:
        """Initialize AreaSeries.

        Args:
            name: Series name displayed in legend.
            values: Numerical values corresponding to categories.
            color: Primary fill and stroke color.
            style: Optional Style overriding area and boundary appearance.
            fill_alpha: Transparency ratio for area polygon (0.0 to 1.0). Defaults to 0.35.
            line_width: Top boundary stroke width. Defaults to 2.0.
            line_style: Top boundary stroke style ("solid", "dashed", etc.). Defaults to "solid".
            point_shape: Marker shape ("circle", "square", "none"). Defaults to "none".
            point_size: Radius or half-width of data point markers. Defaults to 1.0.
        """
        self.name = name
        self.values: list[float] = [float(v) for v in values]
        self.color: ColorType | None = color
        self.style: Style | None = style
        self.fill_alpha: float = float(fill_alpha)
        self.line_width: float = float(line_width)
        self.line_style: LineStyle = line_style
        self.point_shape: PointShape = point_shape
        self.point_size: float = float(point_size)
