# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""BarChart container class implementation."""

from __future__ import annotations

from pydantic import validate_call

import drawlib._charts.bar_chart._renderer as _renderer_module
from drawlib._charts._common._axis import Axis
from drawlib._charts._common._base import AxisChartMixin, draw_with_box_overrides
from drawlib._charts._common._types import BarMode, DrawDirection, FormatterType, Orientation
from drawlib._charts.bar_chart._series import Series
from drawlib._core.l3_styles import Style


class BarChart(AxisChartMixin):
    """Configurable container and builder for vertical and horizontal bar charts."""

    @validate_call
    def __init__(
        self,
        *,
        axis_line_style: Style,
        width: float = 60.0,
        height: float = 40.0,
        categories: list[str] | None = None,
        orientation: Orientation = "vertical",
        bar_mode: BarMode = "group",
        bar_width_ratio: float = 0.7,
        r: float = 0.0,
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        value_format: FormatterType = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None:
        """Initialize BarChart.

        Args:
            axis_line_style: Style defining baseline coordinate axis lines.
            width: Width of the chart on the canvas. Defaults to 60.0.
            height: Height of the chart on the canvas. Defaults to 40.0.
            categories: Category names (e.g. ["Q1", "Q2", "Q3"]).
            orientation: Bar orientation ("vertical" or "horizontal"). Defaults to "vertical".
            bar_mode: Multi-series layout ("group" or "stack"). Defaults to "group".
            bar_width_ratio: Ratio of category slot occupied by bars (0.1 to 1.0). Defaults to 0.7.
            r: Corner radius for bars. Defaults to 0.0.
            axis_text_style: Optional Style for axis tick labels and category names.
            grid_style: Optional Style for background gridlines.
            value_text_style: Optional Style for data value labels drawn on bars.
            value_format: Custom format for value labels.
            background_style: Optional Style for the chart background card.
            title: Title of the chart.
            title_style: Optional Style for the chart title typography.
        """
        self.axis_line_style: Style = axis_line_style
        self.width: float = float(width)
        self.height: float = float(height)
        self.categories: list[str] = list(categories) if categories is not None else []
        self.orientation: Orientation = orientation
        self.bar_mode: BarMode = bar_mode
        self.bar_width_ratio: float = float(bar_width_ratio)
        self.r: float = float(r)
        self.axis_text_style: Style | None = axis_text_style
        self.grid_style: Style | None = grid_style
        self.value_text_style: Style | None = value_text_style
        self.value_format: FormatterType = value_format
        self.background_style: Style | None = background_style
        self.title: str = title
        self.title_style: Style | None = title_style

        self.x_axis: Axis = Axis()
        self.y_axis: Axis = Axis()
        self._series: list[Series] = []

    @property
    def series(self) -> list[Series]:
        """Get list of registered Series."""
        return list(self._series)

    @property
    def value_axis(self) -> Axis:
        """Get the numerical value axis (y_axis for vertical, x_axis for horizontal)."""
        return self.y_axis if self.orientation == "vertical" else self.x_axis

    @property
    def category_axis(self) -> Axis:
        """Get the categorical axis (x_axis for vertical, y_axis for horizontal)."""
        return self.x_axis if self.orientation == "vertical" else self.y_axis

    def add_series(
        self,
        name: str,
        values: list[float],
        style: Style,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection | None = None,
    ) -> Series:
        """Add a data series to the chart.

        Args:
            name: Series label shown in the legend.
            values: Numerical values corresponding to categories.
            style: Style object defining bar outline and fill.
            legend_text_style: Optional custom text style for this series in legend.
            show: Whether to render this series on the canvas. Defaults to True.
            draw_ratio: Spatial rendering ratio from 0.0 to 1.0. Defaults to 1.0.
            draw_direction: Partial rendering direction ("bottom_to_top" or "left_to_right").

        Returns:
            Series: The newly created and registered series.
        """
        eff_dir: DrawDirection = (
            draw_direction
            if draw_direction is not None
            else ("bottom_to_top" if self.orientation == "vertical" else "left_to_right")
        )
        s = Series(
            name=name,
            values=values,
            style=style,
            legend_text_style=legend_text_style,
            show=show,
            draw_ratio=draw_ratio,
            draw_direction=eff_dir,
        )
        self._series.append(s)
        return s

    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        width: float | None = None,
        height: float | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render this bar chart onto the canvas at base coordinate xy (bottom-left).

        Args:
            xy: Canvas placement coordinate (x, y) where the bottom-left of the chart is anchored.
            width: Optional temporary width override for this draw call.
            height: Optional temporary height override for this draw call.
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        draw_with_box_overrides(
            self,
            _renderer_module.draw_bar_chart,
            xy,
            width=width,
            height=height,
            scale=scale,
        )
