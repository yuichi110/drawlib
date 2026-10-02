# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Series model for area charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import LineStyle, PointShape

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class Series:
    """Represents a data series in an area chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
        fill_alpha: float | None = None,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape = "none",
        point_size: float = 1.0,
        legend_text_style: Style | None = None,
    ) -> None:
        """Initialize Series.

        Args:
            name: Series name displayed in legend.
            values: Numerical values corresponding to categories.
            style: Style defining area polygon fill, outline, and marker appearance.
            fill_alpha: Custom alpha override for this series fill (0.0 to 1.0).
            line_width: Stroke width for perimeter line. Defaults to 2.0.
            line_style: Stroke style ("solid", "dashed", "dotted"). Defaults to "solid".
            point_shape: Marker shape at data vertices. Defaults to "none".
            point_size: Marker radius. Defaults to 1.0.
            legend_text_style: Optional custom text style for this series in legend.
        """
        self.name = name
        self.values: list[float] = [float(v) for v in values]
        self.style: Style = style
        self.fill_alpha: float | None = float(fill_alpha) if fill_alpha is not None else None
        self.line_width: float = float(line_width)
        self.line_style: LineStyle = line_style
        self.point_shape: PointShape = point_shape
        self.point_size: float = float(point_size)
        self.legend_text_style: Style | None = legend_text_style
