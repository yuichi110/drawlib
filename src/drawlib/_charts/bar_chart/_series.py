# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""BarSeries model and color palette definition."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style

# Modern default categorical color palette (Tailwind-inspired)
DEFAULT_CHART_PALETTE: list[ColorType] = [
    (59, 130, 246, 1.0),  # Blue
    (16, 185, 129, 1.0),  # Emerald
    (245, 158, 11, 1.0),  # Amber
    (244, 63, 94, 1.0),   # Rose
    (99, 102, 241, 1.0),  # Indigo
    (6, 182, 212, 1.0),   # Cyan
    (168, 85, 247, 1.0),  # Purple
    (249, 115, 22, 1.0),  # Orange
]


class BarSeries:
    """Represents a single data series in a bar chart."""

    def __init__(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize BarSeries.

        Args:
            name: Series name shown in legend and tooltips.
            values: List of numerical values corresponding to chart categories.
            color: Fill color for this series. If None, picked from default palette.
            style: Optional Style object to override bar outline/fill.
        """
        self.name = name
        self.values: list[float] = [float(v) for v in values]
        self.color: ColorType | None = color
        self.style: Style | None = style
