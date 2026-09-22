# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""LineChart container class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType, LegendPosition, LineStyle, PointShape
from drawlib._charts.line_chart import _renderer as _renderer_module
from drawlib._charts.line_chart._base import CartesianChartBase
from drawlib._charts.line_chart._series import LineSeries

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class LineChart(CartesianChartBase):
    """Represents a 2D line chart with straight or smooth curves."""

    def __init__(
        self,
        categories: list[str],
        width: float = 80.0,
        height: float = 50.0,
        title: str = "",
        title_style: Style | None = None,
        show_points: bool = True,
        point_shape: PointShape = "circle",
        point_size: float = 0.7,
        smooth: bool = False,
        legend_position: LegendPosition = "auto",
        show_values: bool = False,
        value_label_style: Style | None = None,
    ) -> None:
        """Initialize LineChart.

        Args:
            categories: Category labels along horizontal axis.
            width: Total width of chart. Defaults to 80.0.
            height: Total height of chart. Defaults to 50.0.
            title: Title text at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            show_points: Whether to render markers at data points. Defaults to True.
            point_shape: Default marker shape ("circle", "square", "none"). Defaults to "circle".
            point_size: Marker radius or half-width. Defaults to 1.2.
            smooth: Whether to render smooth curves instead of straight line segments.
            legend_position: Legend location ("auto", "top", "bottom", "right", "none").
            show_values: Whether to render numerical values above points. Defaults to False.
            value_label_style: Optional Style for data point labels.
        """
        super().__init__(
            categories=categories,
            width=width,
            height=height,
            title=title,
            title_style=title_style,
            legend_position=legend_position,
            show_values=show_values,
            value_label_style=value_label_style,
        )
        self.show_points: bool = show_points
        self.point_shape: PointShape = point_shape
        self.point_size: float = float(point_size)
        self.smooth: bool = smooth
        self._series: list[LineSeries] = []

    @property
    def series(self) -> list[LineSeries]:
        """List of LineSeries registered with this chart."""
        return list(self._series)

    def add_series(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        style: Style | None = None,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape | None = None,
        point_size: float | None = None,
    ) -> LineSeries:
        """Add a new line series to the chart.

        Args:
            name: Series label shown in legend.
            values: Numerical values corresponding to categories.
            color: Line and marker color.
            style: Optional Style overriding line and marker appearance.
            line_width: Stroke thickness. Defaults to 2.0.
            line_style: Stroke pattern ("solid", "dashed", etc.). Defaults to "solid".
            point_shape: Custom marker shape or inherited from chart defaults.
            point_size: Custom marker size or inherited from chart defaults.

        Returns:
            LineSeries: The newly created and registered series.
        """
        shape = point_shape if point_shape is not None else self.point_shape
        size = point_size if point_size is not None else self.point_size
        s = LineSeries(
            name=name,
            values=values,
            color=color,
            style=style,
            line_width=line_width,
            line_style=line_style,
            point_shape=shape,
            point_size=size,
        )
        self._series.append(s)
        return s

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this line chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas coordinate (x, y) where the bottom-left of the chart is placed.
        """
        _renderer_module.draw_line_chart(self, xy)
