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

from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis
from drawlib._charts._common._types import FormatterType, LegendPosition, PointShape, ScaleType
from drawlib._charts.scatter_chart import _renderer as _renderer_module
from drawlib._charts.scatter_chart._point import ScatterPoint, ScatterSeries
from drawlib._preset_styles import get_style

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class ScatterChart:
    """Represents a 2D Scatter and Bubble Chart with continuous numerical X and Y axes."""

    def __init__(
        self,
        width: float = 88.0,
        height: float = 55.0,
        title: str = "",
        title_style: Style | None = None,
        default_radius: float = 1.0,
        default_shape: PointShape = "circle",
        legend_position: LegendPosition = "auto",
        show_labels: bool = True,
    ) -> None:
        """Initialize ScatterChart.

        Args:
            width: Total width of chart container. Defaults to 88.0.
            height: Total height of chart container. Defaults to 55.0.
            title: Title text displayed at top of chart. Defaults to "".
            title_style: Optional Style overriding chart title typography.
            default_radius: Default marker radius for data points. Defaults to 1.0.
            default_shape: Default shape ("circle", "square", "rhombus", "triangle"). Defaults to "circle".
            legend_position: Legend location ("auto", "top", "bottom", "right", "none").
            show_labels: Whether to print annotation labels next to points. Defaults to True.
        """
        self.width: float = float(width)
        self.height: float = float(height)
        self.title: str = title
        self.title_style: Style | None = title_style
        self.default_radius: float = float(default_radius)
        self.default_shape: PointShape = default_shape
        self.legend_position: LegendPosition = legend_position
        self.show_labels: bool = show_labels

        self.x_axis: Axis = Axis()
        self.y_axis: Axis = Axis()

        self._points: list[ScatterPoint] = []
        self._series: list[ScatterSeries] = []

    @property
    def points(self) -> list[ScatterPoint]:
        """List of standalone points added to this chart."""
        return list(self._points)

    @property
    def series(self) -> list[ScatterSeries]:
        """List of named series added to this chart."""
        return list(self._series)

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
        """Configure X-axis parameters.

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
        """Configure Y-axis parameters.

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

    def add(
        self,
        xy: tuple[float, float],
        radius: float | None = None,
        style: Style | str | None = None,
        shape: PointShape | None = None,
        label: str = "",
        label_style: Style | None = None,
    ) -> ScatterPoint:
        """Add a single data point to the scatter chart.

        Args:
            xy: Numerical data coordinate tuple (x, y).
            radius: Radius of the point marker (bubble size). If None, defaults to default_radius.
            style: Custom Style object or preset string.
            shape: Custom marker shape ("circle", "square", "rhombus", "triangle").
            label: Optional text label displayed next to the point.
            label_style: Optional Style for the label text.

        Returns:
            ScatterPoint: The newly created and registered point.
        """
        resolved_style = get_style(style) if style is not None else None
        eff_radius = float(radius) if radius is not None else self.default_radius
        eff_shape = shape if shape is not None else self.default_shape

        point = ScatterPoint(
            xy=xy,
            radius=eff_radius,
            style=resolved_style,
            shape=eff_shape,
            label=label,
            label_style=label_style,
        )
        self._points.append(point)
        return point

    def add_series(
        self,
        name: str,
        data: list[tuple[float, float]] | list[tuple[float, float, float]],
        radius: float | None = None,
        style: Style | str | None = None,
        shape: PointShape | None = None,
    ) -> ScatterSeries:
        """Add a named group of points to the scatter chart.

        Args:
            name: Series name displayed in chart legend.
            data: List of (x, y) or (x, y, radius) tuples.
            radius: Default radius for points in this series.
            style: Style applied to points in this series.
            shape: Shape for points in this series.

        Returns:
            ScatterSeries: The newly created and registered series.
        """
        resolved_style = get_style(style) if style is not None else None
        eff_radius = float(radius) if radius is not None else self.default_radius
        eff_shape = shape if shape is not None else self.default_shape

        points: list[ScatterPoint] = []
        for item in data:
            match item:
                case (x, y, r):
                    x_val, y_val, pt_r = float(x), float(y), float(r)
                case (x, y):
                    x_val, y_val, pt_r = float(x), float(y), eff_radius
                case _:
                    continue

            points.append(
                ScatterPoint(
                    xy=(x_val, y_val),
                    radius=pt_r,
                    style=resolved_style,
                    shape=eff_shape,
                )
            )

        series_obj = ScatterSeries(
            name=name,
            points=points,
            style=resolved_style,
            radius=eff_radius,
            shape=eff_shape,
        )
        self._series.append(series_obj)
        return series_obj

    def get_size(self) -> tuple[float, float]:
        """Get the dimensions (width, height) of this chart."""
        return (self.width, self.height)

    def draw(self, xy: tuple[float, float]) -> None:
        """Render the scatter chart onto the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y) of the chart bounding box.
        """
        _renderer_module.render_scatter_chart(self, xy)
