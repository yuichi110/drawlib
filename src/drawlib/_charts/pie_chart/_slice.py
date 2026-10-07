# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
"""Slice model representing a single sector in a pie or donut chart."""

from __future__ import annotations

from drawlib._charts._common._types import DrawDirection
from drawlib._core.l3_styles import Style


class Slice:
    """Represents a single data slice in a pie or donut chart."""

    def __init__(
        self,
        name: str,
        value: float,
        style: Style,
        explode: float = 0.0,
        legend_text_style: Style | None = None,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> None:
        """Initialize Slice.

        Args:
            name: Slice label displayed in legend and annotations.
            value: Numerical value determining slice proportion.
            style: Style defining wedge fill, outline, and appearance.
            explode: Distance to shift the slice outward from center. Defaults to 0.0.
            legend_text_style: Optional custom text style for this slice in legend.
            show: Whether this slice is rendered. Defaults to True.
            draw_ratio: Spatial rendering progress ratio in [0.0, 1.0]. Defaults to 1.0.
            draw_direction: Direction of partial rendering ("left_to_right" or "bottom_to_top").
        """
        self.name = name
        self.value = float(value)
        self.style: Style = style
        self.explode = float(explode)
        self.legend_text_style: Style | None = legend_text_style
        self.show: bool = show
        self.draw_ratio: float = float(draw_ratio)
        self.draw_direction: DrawDirection = draw_direction
