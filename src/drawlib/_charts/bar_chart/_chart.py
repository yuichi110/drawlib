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

from typing import TYPE_CHECKING

import drawlib._charts.bar_chart._renderer as _renderer_module
from drawlib._charts._common._axis import Axis
from drawlib._charts._common._types import BarMode, ColorType, FormatterType, LegendPosition, Orientation, ScaleType
from drawlib._charts.bar_chart._series import BarSeries

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class BarChart:
    """Configurable container and builder for vertical and horizontal bar charts."""

    def __init__(
        self,
        title: str = "",
        categories: list[str] | None = None,
        width: float = 60.0,
        height: float = 40.0,
        orientation: Orientation = "vertical",
        bar_mode: BarMode = "group",
        bar_width_ratio: float = 0.7,
        r: float = 0.0,
        show_values: bool = False,
        value_format: FormatterType = None,
        value_label_style: Style | None = None,
        legend_position: LegendPosition = "auto",
        legend_style: Style | None = None,
        style: Style | None = None,
        title_style: Style | None = None,
    ) -> None:
        """Initialize BarChart.

        Args:
            title: Title of the chart.
            categories: Category names (e.g. ["Q1", "Q2", "Q3"]).
            width: Width of the chart on the canvas. Defaults to 60.0.
            height: Height of the chart on the canvas. Defaults to 40.0.
            orientation: Bar orientation ("vertical" or "horizontal"). Defaults to "vertical".
            bar_mode: Multi-series layout ("group" or "stack"). Defaults to "group".
            bar_width_ratio: Ratio of category slot occupied by bars (0.1 to 1.0). Defaults to 0.7.
            r: Corner radius for bars. Defaults to 0.0.
            show_values: Whether to render data values on bars. Defaults to False.
            value_format: Custom format for value labels.
            value_label_style: Style for value label typography.
            legend_position: Legend placement ("top", "bottom", "right", "none", "auto").
            legend_style: Style for legend text.
            style: Optional Style for the chart background card.
            title_style: Optional Style for the chart title typography.
        """
        self.title: str = title
        self.categories: list[str] = list(categories) if categories is not None else []
        self.width: float = float(width)
        self.height: float = float(height)
        self.orientation: Orientation = orientation
        self.bar_mode: BarMode = bar_mode
        self.bar_width_ratio: float = float(bar_width_ratio)
        self.r: float = float(r)
        self.show_values: bool = show_values
        self.value_format: FormatterType = value_format
        self.value_label_style: Style | None = value_label_style
        self.legend_position: LegendPosition = legend_position
        self.legend_style: Style | None = legend_style
        self.style: Style | None = style
        self.title_style: Style | None = title_style

        self.x_axis: Axis = Axis()
        self.y_axis: Axis = Axis()
        self._series: list[BarSeries] = []

    @property
    def series(self) -> list[BarSeries]:
        """Get list of registered BarSeries."""
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
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> BarSeries:
        """Add a data series to the chart.

        Args:
            name: Series label shown in the legend.
            values: Numerical values corresponding to categories.
            color: Bar fill color.
            style: Optional Style object to override bar appearance.

        Returns:
            BarSeries: The newly created and registered series.
        """
        s = BarSeries(name=name, values=values, color=color, style=style)
        self._series.append(s)
        return s

    def configure_y_axis(
        self,
        scale: ScaleType | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        ticks: list[float] | None = None,
        tick_step: float | None = None,
        format: FormatterType = None,  # noqa: A002
        unit: str | None = None,
        label: str | None = None,
        show_grid: bool | None = None,
        grid_style: Style | None = None,
        show_axis_line: bool | None = None,
        line_style: Style | None = None,
        show_ticks: bool | None = None,
        tick_label_style: Style | None = None,
        tick_label_angle: float | None = None,
    ) -> Axis:
        """Configure Y-axis parameters in a single call.

        Returns:
            Axis: The updated Y-axis instance for chaining.
        """
        self.y_axis.configure(
            scale=scale,
            min_value=min_value,
            max_value=max_value,
            ticks=ticks,
            tick_step=tick_step,
            format=format,
            unit=unit,
            label=label,
            show_grid=show_grid,
            grid_style=grid_style,
            show_axis_line=show_axis_line,
            line_style=line_style,
            show_ticks=show_ticks,
            tick_label_style=tick_label_style,
            tick_label_angle=tick_label_angle,
        )
        return self.y_axis

    def configure_x_axis(
        self,
        scale: ScaleType | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        ticks: list[float] | None = None,
        tick_step: float | None = None,
        format: FormatterType = None,  # noqa: A002
        unit: str | None = None,
        label: str | None = None,
        show_grid: bool | None = None,
        grid_style: Style | None = None,
        show_axis_line: bool | None = None,
        line_style: Style | None = None,
        show_ticks: bool | None = None,
        tick_label_style: Style | None = None,
        tick_label_angle: float | None = None,
    ) -> Axis:
        """Configure X-axis parameters in a single call.

        Returns:
            Axis: The updated X-axis instance for chaining.
        """
        self.x_axis.configure(
            scale=scale,
            min_value=min_value,
            max_value=max_value,
            ticks=ticks,
            tick_step=tick_step,
            format=format,
            unit=unit,
            label=label,
            show_grid=show_grid,
            grid_style=grid_style,
            show_axis_line=show_axis_line,
            line_style=line_style,
            show_ticks=show_ticks,
            tick_label_style=tick_label_style,
            tick_label_angle=tick_label_angle,
        )
        return self.x_axis

    def get_size(self) -> tuple[float, float]:
        """Get the dimensions (width, height) of this chart."""
        return (self.width, self.height)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this bar chart onto the canvas at base coordinate xy (bottom-left).

        Args:
            xy: Canvas placement coordinate (x, y) where the bottom-left of the chart is anchored.
        """
        _renderer_module.draw_bar_chart(self, xy)
