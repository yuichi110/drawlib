# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""RadarSeries model representing a single data polygon in a radar chart."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType, LineStyle, PointShape

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class RadarSeries:
    """Represents a data series (closed polygon) in a radar chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        fill_alpha: float = 0.25,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        show_points: bool = True,
        point_shape: PointShape = "circle",
        point_size: float = 0.8,
        style: Style | None = None,
    ) -> None:
        """Initialize RadarSeries.

        Args:
            name: Series label displayed in the legend.
            values: Numerical values corresponding to each radar axis/category.
            color: Primary color for polygon fill and line stroke.
            fill_alpha: Transparency of the filled polygon (0.0 to 1.0). Defaults to 0.25.
            line_width: Width of the bounding polygon perimeter line. Defaults to 2.0.
            line_style: Line stroke pattern ("solid", "dashed", "dotted", "dashdot"). Defaults to "solid".
            show_points: Whether to render markers at category vertices. Defaults to True.
            point_shape: Marker shape ("circle", "square", "none"). Defaults to "circle".
            point_size: Radius or half-width of the vertex markers. Defaults to 0.8.
            style: Optional custom Style overriding polygon appearance.
        """
        self.name = name
        self.values = [float(v) for v in values]
        self.color: ColorType | None = color
        self.fill_alpha = float(fill_alpha)
        self.line_width = float(line_width)
        self.line_style: LineStyle = line_style
        self.show_points = show_points
        self.point_shape: PointShape = point_shape
        self.point_size = float(point_size)
        self.style: Style | None = style
