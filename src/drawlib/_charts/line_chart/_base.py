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

from pydantic import validate_call

import drawlib._charts._common._legend as _legend_module
from drawlib._charts._common._axis import Axis
from drawlib._charts._common._types import FormatterType, Orientation, ScaleType
from drawlib._core.l3_styles import Style


class CartesianChartBase:
    """Base container for 2D Cartesian charts with categories and numerical values."""

    @validate_call
    def __init__(
        self,
        *,
        axis_line_style: Style,
        categories: list[str],
        width: float = 80.0,
        height: float = 50.0,
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None:
        """Initialize CartesianChartBase.

        Args:
            axis_line_style: Style defining baseline coordinate axis lines.
            categories: Category labels along horizontal axis.
            width: Total width of chart container. Defaults to 80.0.
            height: Total height of chart container. Defaults to 50.0.
            axis_text_style: Optional Style for axis tick labels and category names.
            grid_style: Optional Style for background gridlines.
            value_text_style: Optional Style for value labels on data points.
            background_style: Optional Style for the chart background card.
            title: Title text displayed at top of chart. Defaults to "".
            title_style: Optional Style overriding chart title typography.
        """
        self.axis_line_style: Style = axis_line_style
        self.categories: list[str] = list(categories)
        self.width: float = float(width)
        self.height: float = float(height)
        self.axis_text_style: Style | None = axis_text_style
        self.grid_style: Style | None = grid_style
        self.value_text_style: Style | None = value_text_style
        self.background_style: Style | None = background_style
        self.title: str = title
        self.title_style: Style | None = title_style

        # Value axis (Y) and Category axis (X)
        self.y_axis = Axis()
        self.x_axis = Axis(show_grid=False, show_axis_line=True)

    def draw_legend(
        self,
        xy: tuple[float, float],
        text_style: Style,
        orientation: Orientation = "vertical",
        swatch_size: tuple[float, float] = (2.4, 1.2),
        item_gap: float = 4.0,
    ) -> None:
        """Render legend for series at coordinate xy.

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
                s.style.line_color or s.style.shape_fill_color or s.style.shape_line_color or (30, 41, 59, 1.0),
                getattr(s, "legend_text_style", None),
            )
            for s in getattr(self, "_series", [])
        ]
        _legend_module.draw_legend(
            items=items,
            xy=xy,
            text_style=text_style,
            orientation=orientation,
            swatch_size=swatch_size,
            item_gap=item_gap,
        )

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
