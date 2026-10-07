# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ScatterChart container class."""

from __future__ import annotations

from pydantic import validate_call

from drawlib._charts._common._axis import Axis
from drawlib._charts._common._base import AxisChartMixin, draw_with_box_overrides
from drawlib._charts._common._types import DrawDirection, PointShape
from drawlib._charts.scatter_chart import _renderer as _renderer_module
from drawlib._charts.scatter_chart._point import Point, Series
from drawlib._core.l3_styles import Style


class ScatterChart(AxisChartMixin):
    """Represents a 2D Scatter and Bubble Chart with continuous numerical X and Y axes."""

    @validate_call
    def __init__(
        self,
        *,
        axis_line_style: Style,
        width: float = 88.0,
        height: float = 55.0,
        default_radius: float = 1.0,
        default_shape: PointShape = "circle",
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None:
        """Initialize ScatterChart.

        Args:
            axis_line_style: Style defining baseline coordinate axis lines.
            width: Total width of chart container. Defaults to 88.0.
            height: Total height of chart container. Defaults to 55.0.
            default_radius: Default marker radius for data points. Defaults to 1.0.
            default_shape: Default shape ("circle", "square", "rhombus", "triangle"). Defaults to "circle".
            axis_text_style: Optional Style for axis tick labels.
            grid_style: Optional Style for background gridlines.
            value_text_style: Optional Style for point annotation text.
            background_style: Optional Style for chart background card.
            title: Title text displayed at top of chart. Defaults to "".
            title_style: Optional Style overriding chart title typography.
        """
        self.axis_line_style: Style = axis_line_style
        self.width: float = float(width)
        self.height: float = float(height)
        self.default_radius: float = float(default_radius)
        self.default_shape: PointShape = default_shape
        self.axis_text_style: Style | None = axis_text_style
        self.grid_style: Style | None = grid_style
        self.value_text_style: Style | None = value_text_style
        self.background_style: Style | None = background_style
        self.title: str = title
        self.title_style: Style | None = title_style

        self.x_axis: Axis = Axis()
        self.y_axis: Axis = Axis()

        self._points: list[Point] = []
        self._series: list[Series] = []

    @property
    def points(self) -> list[Point]:
        """List of standalone points added to this chart."""
        return list(self._points)

    @property
    def series(self) -> list[Series]:
        """List of named series added to this chart."""
        return list(self._series)

    def add(
        self,
        xy: tuple[float, float],
        style: Style,
        radius: float | None = None,
        shape: PointShape | None = None,
        label: str = "",
        label_style: Style | None = None,
        *,
        show: bool = True,
    ) -> Point:
        """Add a single data point to the scatter chart.

        Args:
            xy: Numerical data coordinate tuple (x, y).
            style: Style defining marker outline and fill.
            radius: Radius of the point marker (bubble size). If None, defaults to default_radius.
            shape: Custom marker shape ("circle", "square", "rhombus", "triangle").
            label: Optional text label displayed next to the point.
            label_style: Optional Style for the label text.
            show: Whether to render this point on the canvas. Defaults to True.

        Returns:
            Point: The newly created and registered point.
        """
        eff_radius = float(radius) if radius is not None else self.default_radius
        eff_shape = shape if shape is not None else self.default_shape

        point = Point(
            xy=xy,
            style=style,
            radius=eff_radius,
            shape=eff_shape,
            label=label,
            label_style=label_style,
            show=show,
        )
        self._points.append(point)
        return point

    def add_series(
        self,
        name: str,
        data: list[tuple[float, float]] | list[tuple[float, float, float]],
        style: Style,
        radius: float | None = None,
        shape: PointShape | None = None,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> Series:
        """Add a named group of points to the scatter chart.

        Args:
            name: Series name displayed in chart legend.
            data: List of (x, y) or (x, y, radius) tuples.
            style: Style applied to points in this series.
            radius: Default radius for points in this series.
            shape: Shape for points in this series.
            legend_text_style: Optional custom text style for this series in legend.
            show: Whether to render this series on the canvas. Defaults to True.
            draw_ratio: Spatial rendering ratio from 0.0 to 1.0. Defaults to 1.0.
            draw_direction: Partial rendering direction ("left_to_right" or "bottom_to_top").

        Returns:
            Series: The newly created and registered series.
        """
        eff_radius = float(radius) if radius is not None else self.default_radius
        eff_shape = shape if shape is not None else self.default_shape

        points: list[Point] = []
        for item in data:
            match item:
                case (x, y, r):
                    x_val, y_val, pt_r = float(x), float(y), float(r)
                case (x, y):
                    x_val, y_val, pt_r = float(x), float(y), eff_radius
                case _:
                    continue

            points.append(
                Point(
                    xy=(x_val, y_val),
                    style=style,
                    radius=pt_r,
                    shape=eff_shape,
                )
            )

        series_obj = Series(
            name=name,
            points=points,
            style=style,
            radius=eff_radius,
            shape=eff_shape,
            legend_text_style=legend_text_style,
            show=show,
            draw_ratio=draw_ratio,
            draw_direction=draw_direction,
        )
        self._series.append(series_obj)
        return series_obj

    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        width: float | None = None,
        height: float | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render the scatter chart onto the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y) of the chart bounding box. Defaults to (0.0, 0.0).
            width: Optional temporary width override for this draw call.
            height: Optional temporary height override for this draw call.
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        draw_with_box_overrides(
            self,
            _renderer_module.render_scatter_chart,
            xy,
            width=width,
            height=height,
            scale=scale,
        )
