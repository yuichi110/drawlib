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

from pydantic import validate_call

from drawlib._charts._common._axis import Axis
from drawlib._charts._common._base import AxisChartMixin
from drawlib._core.l3_styles import Style


class CartesianChartBase(AxisChartMixin):
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
