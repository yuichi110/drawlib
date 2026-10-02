# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""PieChart container class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._charts._common._legend as _legend_module
from drawlib._charts._common._types import FormatterType, Orientation
from drawlib._charts.pie_chart import _renderer as _renderer_module
from drawlib._charts.pie_chart._slice import Slice

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class PieChart:
    """Represents a 2D pie or donut chart."""

    def __init__(
        self,
        radius: float = 20.0,
        hole_ratio: float = 0.0,
        start_angle: float = 90.0,
        clockwise: bool = True,
        value_text_style: Style | None = None,
        value_format: FormatterType = "{:.1f}%",
        center_text: str = "",
        center_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> None:
        """Initialize PieChart.

        Args:
            radius: Outer radius of the pie circle. Defaults to 20.0.
            hole_ratio: Inner hole radius ratio (0.0 for solid pie, > 0.0 for donut). Defaults to 0.0.
            start_angle: Starting angle in degrees (90.0 is 12 o'clock). Defaults to 90.0.
            clockwise: Whether slices progress clockwise. Defaults to True.
            value_text_style: Optional Style for value percentage labels on slices.
            value_format: Formatter string or callable for slice values. Defaults to "{:.1f}%".
            center_text: Text displayed inside the donut hole. Defaults to "".
            center_text_style: Optional Style for center text.
            background_style: Optional Style for chart background card.
            title: Title text at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            width: Optional total chart container width. If None, computed from radius.
            height: Optional total chart container height. If None, computed from radius and title.
        """
        self.radius = float(radius)
        self.hole_ratio = max(0.0, min(0.9, float(hole_ratio)))
        self.start_angle = float(start_angle)
        self.clockwise = clockwise
        self.value_text_style: Style | None = value_text_style
        self.value_format = value_format
        self.center_text = center_text
        self.center_text_style: Style | None = center_text_style
        self.background_style: Style | None = background_style
        self.title = title
        self.title_style: Style | None = title_style

        self._custom_width = float(width) if width is not None else None
        self._custom_height = float(height) if height is not None else None
        self._slices: list[Slice] = []

    @property
    def slices(self) -> list[Slice]:
        """List of Slice instances registered with this chart."""
        return list(self._slices)

    def add_slice(
        self,
        name: str,
        value: float,
        style: Style,
        explode: float = 0.0,
        legend_text_style: Style | None = None,
    ) -> Slice:
        """Add a new slice to the pie chart.

        Args:
            name: Slice label shown in legend.
            value: Numerical magnitude of this slice.
            style: Style defining wedge appearance.
            explode: Outward offset distance from center. Defaults to 0.0.
            legend_text_style: Optional custom text style for this slice in legend.

        Returns:
            Slice: The newly created and registered slice.
        """
        s = Slice(name=name, value=value, style=style, explode=explode, legend_text_style=legend_text_style)
        self._slices.append(s)
        return s

    def get_size(self) -> tuple[float, float]:
        """Get the total dimensions (width, height) of this chart."""
        if self._custom_width is not None and self._custom_height is not None:
            return (self._custom_width, self._custom_height)

        diameter = self.radius * 2.0
        has_title = bool(self.title and self.title_style is not None)
        w = self._custom_width if self._custom_width is not None else diameter + 8.0
        h = self._custom_height if self._custom_height is not None else diameter + 8.0 + (6.0 if has_title else 0.0)
        return (w, h)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this pie chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) where the bottom-left corner is anchored.
        """
        _renderer_module.draw_pie_chart(self, xy)

    def draw_legend(
        self,
        xy: tuple[float, float],
        text_style: Style,
        orientation: Orientation = "vertical",
        swatch_size: tuple[float, float] = (2.4, 1.2),
        item_gap: float = 4.0,
    ) -> None:
        """Render legend for slices at coordinate xy.

        Args:
            xy: Starting placement coordinate (x, y).
            text_style: Base Style for legend text labels.
            orientation: Legend orientation ("vertical" or "horizontal"). Defaults to "vertical".
            swatch_size: (width, height) size of color swatches. Defaults to (2.4, 1.2).
            item_gap: Spacing between consecutive legend items. Defaults to 4.0.
        """
        items = [
            (
                s.name,
                s.style.shape_fill_color or s.style.shape_line_color or (30, 41, 59, 1.0),
                s.legend_text_style,
            )
            for s in self._slices
        ]
        _legend_module.draw_legend(
            items=items,
            xy=xy,
            text_style=text_style,
            orientation=orientation,
            swatch_size=swatch_size,
            item_gap=item_gap,
        )
