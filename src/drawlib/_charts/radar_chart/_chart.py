# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""RadarChart container class."""

from __future__ import annotations

from pydantic import validate_call

from drawlib._charts._common._base import RadialChartMixin
from drawlib._charts._common._types import (
    DrawDirection,
    FormatterType,
    GridShape,
    LineStyle,
    PointShape,
)
from drawlib._charts.radar_chart import _renderer as _renderer_module
from drawlib._charts.radar_chart._series import Series
from drawlib._core.l3_styles import Style


class RadarChart(RadialChartMixin):
    """Represents a 2D radar (spider web) chart."""

    @validate_call
    def __init__(
        self,
        *,
        categories: list[str],
        axis_line_style: Style,
        radius: float = 25.0,
        min_value: float = 0.0,
        max_value: float | None = None,
        levels: int = 5,
        grid_shape: GridShape = "polygon",
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        scale_text_style: Style | None = None,
        scale_format: FormatterType = None,
        value_text_style: Style | None = None,
        value_format: FormatterType = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> None:
        """Initialize RadarChart.

        Args:
            categories: List of category/dimension names (minimum 3).
            axis_line_style: Required Style for radial spoke lines.
            radius: Outer radius of the radar web. Defaults to 25.0.
            min_value: Baseline value at the center origin. Defaults to 0.0.
            max_value: Outer boundary value. If None, calculated automatically.
            levels: Number of concentric grid rings. Defaults to 5.
            grid_shape: Grid contour style ("polygon" or "circle"). Defaults to "polygon".
            axis_text_style: Optional Style for category labels around the perimeter.
            grid_style: Optional Style for concentric grid rings. If None, rings are omitted.
            scale_text_style: Optional Style for numeric scale labels along spokes.
            scale_format: Formatter string or function for scale levels.
            value_text_style: Optional Style for vertex data values. If None, values are omitted.
            value_format: Formatter string or function for vertex values.
            background_style: Optional Style for chart background card.
            title: Title text at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            width: Optional total chart width override.
            height: Optional total chart height override.

        Raises:
            ValueError: If fewer than 3 categories are provided.
        """
        if len(categories) < 3:
            raise ValueError(f"RadarChart requires at least 3 categories, but got {len(categories)}.")

        self._categories = list(categories)
        self.axis_line_style: Style = axis_line_style
        self.radius = float(radius)
        self.min_value = float(min_value)
        self.max_value = float(max_value) if max_value is not None else None
        self.levels = max(1, int(levels))
        self.grid_shape: GridShape = grid_shape
        self.axis_text_style: Style | None = axis_text_style
        self.grid_style: Style | None = grid_style
        self.scale_text_style: Style | None = scale_text_style
        self.scale_format: FormatterType = scale_format
        self.value_text_style: Style | None = value_text_style
        self.value_format: FormatterType = value_format
        self.background_style: Style | None = background_style
        self.title = title
        self.title_style: Style | None = title_style

        self._custom_width = float(width) if width is not None else None
        self._custom_height = float(height) if height is not None else None
        self._series: list[Series] = []

    @property
    def categories(self) -> list[str]:
        """List of category labels."""
        return list(self._categories)

    @property
    def series(self) -> list[Series]:
        """List of registered Series."""
        return list(self._series)

    def configure_axis(
        self,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        levels: int | None = None,
        scale_format: FormatterType = None,
    ) -> RadarChart:
        """Configure radial scale bounds, concentric ring count, and scale formatter.

        Args:
            min_value: Optional baseline value at the center origin.
            max_value: Optional outer boundary value.
            levels: Optional number of concentric grid rings.
            scale_format: Optional formatter string or function for scale levels.

        Returns:
            RadarChart: Self for method chaining.
        """
        if min_value is not None:
            self.min_value = float(min_value)
        if max_value is not None:
            self.max_value = float(max_value)
        if levels is not None:
            self.levels = max(1, int(levels))
        if scale_format is not None:
            self.scale_format = scale_format
        return self

    def add_series(
        self,
        name: str,
        values: list[float],
        style: Style,
        fill_alpha: float = 0.25,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape = "circle",
        point_size: float = 0.8,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "bottom_to_top",
    ) -> Series:
        """Add a new data series to the radar chart.

        Args:
            name: Series name displayed in legend.
            values: Numeric values for each category.
            style: Style defining polygon outline, fill, and marker appearance.
            fill_alpha: Transparency of polygon fill (0.0 to 1.0). Defaults to 0.25.
            line_width: Perimeter stroke width. Defaults to 2.0.
            line_style: Perimeter stroke pattern. Defaults to "solid".
            point_shape: Marker shape ("circle", "square", "none"). Defaults to "circle".
            point_size: Marker radius. Defaults to 0.8.
            legend_text_style: Optional custom text style for this series in legend.
            show: Whether this series is rendered. Defaults to True.
            draw_ratio: Spatial rendering progress ratio in [0.0, 1.0]. Defaults to 1.0.
            draw_direction: Direction of partial rendering ("bottom_to_top" or "left_to_right").

        Returns:
            Series: The newly created and registered series.
        """
        s = Series(
            name=name,
            values=values,
            style=style,
            fill_alpha=fill_alpha,
            line_width=line_width,
            line_style=line_style,
            point_shape=point_shape,
            point_size=point_size,
            legend_text_style=legend_text_style,
            show=show,
            draw_ratio=draw_ratio,
            draw_direction=draw_direction,
        )
        self._series.append(s)
        return s

    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        radius: float | None = None,
        width: float | None = None,
        height: float | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render this radar chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) where the bottom-left corner is anchored.
            radius: Optional temporary override for radar web outer radius.
            width: Optional temporary override for chart container width.
            height: Optional temporary override for chart container height.
            scale: Uniform scaling factor applied around xy. Defaults to 1.0.
        """
        self._draw_with_radial_overrides(
            _renderer_module.draw_radar_chart,
            xy,
            radius=radius,
            width=width,
            height=height,
            scale=scale,
        )
