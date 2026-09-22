# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AreaChart container class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import AreaMode, ColorType, LegendPosition, LineStyle, PointShape
from drawlib._charts.line_chart import _renderer as _renderer_module
from drawlib._charts.line_chart._base import CartesianChartBase
from drawlib._charts.line_chart._series import AreaSeries

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class AreaChart(CartesianChartBase):
    """Represents a 2D area chart supporting overlapping and stacked modes."""

    def __init__(
        self,
        categories: list[str],
        width: float = 80.0,
        height: float = 50.0,
        title: str = "",
        title_style: Style | None = None,
        mode: AreaMode = "overlap",
        fill_alpha: float = 0.35,
        show_points: bool = False,
        point_shape: PointShape = "none",
        point_size: float = 1.0,
        smooth: bool = False,
        legend_position: LegendPosition = "auto",
        show_values: bool = False,
        value_label_style: Style | None = None,
    ) -> None:
        """Initialize AreaChart.

        Args:
            categories: Category labels along horizontal axis.
            width: Total width of chart. Defaults to 80.0.
            height: Total height of chart. Defaults to 50.0.
            title: Title text at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            mode: Area layout mode ("overlap" or "stack"). Defaults to "overlap".
            fill_alpha: Transparency ratio for area polygon fill (0.0 to 1.0). Defaults to 0.35.
            show_points: Whether to render markers at data points. Defaults to False.
            point_shape: Default marker shape ("circle", "square", "none"). Defaults to "none".
            point_size: Marker radius or half-width. Defaults to 1.0.
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
        self.mode: AreaMode = mode
        self.fill_alpha: float = float(fill_alpha)
        self.show_points: bool = show_points
        self.point_shape: PointShape = point_shape
        self.point_size: float = float(point_size)
        self.smooth: bool = smooth
        self._series: list[AreaSeries] = []

    @property
    def series(self) -> list[AreaSeries]:
        """List of AreaSeries registered with this chart."""
        return list(self._series)

    def add_series(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        style: Style | None = None,
        fill_alpha: float | None = None,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape | None = None,
        point_size: float | None = None,
    ) -> AreaSeries:
        """Add a new area series to the chart.

        Args:
            name: Series label shown in legend.
            values: Numerical values corresponding to categories.
            color: Area fill and stroke color.
            style: Optional Style overriding area and boundary appearance.
            fill_alpha: Transparency ratio for this series polygon.
            line_width: Stroke thickness of upper boundary line. Defaults to 2.0.
            line_style: Stroke pattern ("solid", "dashed", etc.). Defaults to "solid".
            point_shape: Custom marker shape or inherited from chart defaults.
            point_size: Custom marker size or inherited from chart defaults.

        Returns:
            AreaSeries: The newly created and registered series.
        """
        alpha = fill_alpha if fill_alpha is not None else self.fill_alpha
        shape = point_shape if point_shape is not None else self.point_shape
        size = point_size if point_size is not None else self.point_size
        s = AreaSeries(
            name=name,
            values=values,
            color=color,
            style=style,
            fill_alpha=alpha,
            line_width=line_width,
            line_style=line_style,
            point_shape=shape,
            point_size=size,
        )
        self._series.append(s)
        return s

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this area chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas coordinate (x, y) where the bottom-left of the chart is placed.
        """
        _renderer_module.draw_area_chart(self, xy)
