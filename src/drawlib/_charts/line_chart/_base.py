# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base container class for Cartesian line and area charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis
from drawlib._charts._common._types import FormatterType, LegendPosition, ScaleType

if TYPE_CHECKING:
    from drawlib._core.types import Style


class CartesianChartBase:
    """Base container for 2D Cartesian charts with categories and numerical values."""

    def __init__(
        self,
        categories: list[str],
        width: float = 80.0,
        height: float = 50.0,
        title: str = "",
        title_style: Style | None = None,
        legend_position: LegendPosition = "auto",
        show_values: bool = False,
        value_label_style: Style | None = None,
    ) -> None:
        """Initialize CartesianChartBase.

        Args:
            categories: Category labels along horizontal axis.
            width: Total width of chart container. Defaults to 80.0.
            height: Total height of chart container. Defaults to 50.0.
            title: Title text displayed at top of chart. Defaults to "".
            title_style: Optional Style overriding chart title typography.
            legend_position: Legend location ("auto", "top", "bottom", "right", "none").
            show_values: Whether to print numeric values at data points. Defaults to False.
            value_label_style: Optional Style for value labels.
        """
        self.categories: list[str] = list(categories)
        self.width: float = float(width)
        self.height: float = float(height)
        self.title: str = title
        self.title_style: Style | None = title_style
        self.legend_position: LegendPosition = legend_position
        self.show_values: bool = show_values
        self.value_label_style: Style | None = value_label_style

        # Value axis (Y) and Category axis (X)
        self.y_axis = Axis()
        self.x_axis = Axis(show_grid=False, show_axis_line=True)

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
