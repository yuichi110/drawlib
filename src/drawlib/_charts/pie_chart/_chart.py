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

from drawlib._charts._common._types import ColorType, FormatterType, LegendPosition
from drawlib._charts.pie_chart import _renderer as _renderer_module
from drawlib._charts.pie_chart._slice import PieSlice

if TYPE_CHECKING:
    from drawlib._core.types import Style


class PieChart:
    """Represents a 2D pie or donut chart."""

    def __init__(
        self,
        radius: float = 20.0,
        title: str = "",
        title_style: Style | None = None,
        hole_ratio: float = 0.0,
        center_text: str = "",
        center_text_style: Style | None = None,
        start_angle: float = 90.0,
        clockwise: bool = True,
        show_values: bool = True,
        value_format: FormatterType = "{:.1f}%",
        value_label_style: Style | None = None,
        legend_position: LegendPosition = "right",
        width: float | None = None,
        height: float | None = None,
    ) -> None:
        """Initialize PieChart.

        Args:
            radius: Outer radius of the pie circle. Defaults to 20.0.
            title: Title text at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            hole_ratio: Inner hole radius ratio (0.0 for solid pie, > 0.0 for donut). Defaults to 0.0.
            center_text: Text displayed inside the donut hole. Defaults to "".
            center_text_style: Optional Style for center text.
            start_angle: Starting angle in degrees (90.0 is 12 o'clock). Defaults to 90.0.
            clockwise: Whether slices progress clockwise. Defaults to True.
            show_values: Whether to print percentages or values on slices. Defaults to True.
            value_format: Formatter string or callable for slice values. Defaults to "{:.1f}%".
            value_label_style: Optional Style for slice value labels.
            legend_position: Legend location ("right", "bottom", "top", "none", "auto"). Defaults to "right".
            width: Optional total chart container width. If None, computed from radius and legend.
            height: Optional total chart container height. If None, computed from radius and title.
        """
        self.radius = float(radius)
        self.title = title
        self.title_style: Style | None = title_style
        self.hole_ratio = max(0.0, min(0.9, float(hole_ratio)))
        self.center_text = center_text
        self.center_text_style: Style | None = center_text_style
        self.start_angle = float(start_angle)
        self.clockwise = clockwise
        self.show_values = show_values
        self.value_format = value_format
        self.value_label_style: Style | None = value_label_style
        self.legend_position: LegendPosition = legend_position

        self._custom_width = float(width) if width is not None else None
        self._custom_height = float(height) if height is not None else None
        self._slices: list[PieSlice] = []

    @property
    def slices(self) -> list[PieSlice]:
        """List of PieSlice instances registered with this chart."""
        return list(self._slices)

    def add_slice(
        self,
        name: str,
        value: float,
        color: ColorType | None = None,
        style: Style | None = None,
        explode: float = 0.0,
    ) -> PieSlice:
        """Add a new slice to the pie chart.

        Args:
            name: Slice label shown in legend.
            value: Numerical magnitude of this slice.
            color: Slice fill color.
            style: Optional Style overriding slice appearance.
            explode: Outward offset distance from center. Defaults to 0.0.

        Returns:
            PieSlice: The newly created and registered slice.
        """
        s = PieSlice(name=name, value=value, color=color, style=style, explode=explode)
        self._slices.append(s)
        return s

    def get_size(self) -> tuple[float, float]:
        """Get the total dimensions (width, height) of this chart."""
        if self._custom_width is not None and self._custom_height is not None:
            return (self._custom_width, self._custom_height)

        diameter = self.radius * 2.0
        extra_w = 20.0 if self.legend_position == "right" else 8.0
        extra_h = (6.0 if self.title else 0.0) + (10.0 if self.legend_position in {"top", "bottom"} else 8.0)
        w = self._custom_width if self._custom_width is not None else diameter + extra_w
        h = self._custom_height if self._custom_height is not None else diameter + extra_h
        return (w, h)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this pie chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) where the bottom-left corner is anchored.
        """
        _renderer_module.draw_pie_chart(self, xy)
