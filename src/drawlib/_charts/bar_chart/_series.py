# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Series model for bar charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import DrawDirection

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style

__all__ = ["Series"]


class Series:
    """Represents a single data series in a bar chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "bottom_to_top",
    ) -> None:
        """Initialize Series.

        Args:
            name: Series name shown in legend and tooltips.
            values: List of numerical values corresponding to chart categories.
            style: Style object defining bar outline and fill.
            legend_text_style: Optional custom text style for this series in legend.
            show: Whether to render this series on the canvas. Defaults to True.
            draw_ratio: Spatial rendering ratio from 0.0 to 1.0. Defaults to 1.0.
            draw_direction: Partial rendering direction ("bottom_to_top" or "left_to_right").
        """
        self.name = name
        self.values: list[float] = [float(v) for v in values]
        self.style: Style = style
        self.legend_text_style: Style | None = legend_text_style
        self.show: bool = bool(show)
        self.draw_ratio: float = float(draw_ratio)
        self.draw_direction: DrawDirection = draw_direction
