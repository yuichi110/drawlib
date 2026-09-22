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

from typing import TYPE_CHECKING

from drawlib._charts._common._types import (
    ColorType,
    FormatterType,
    GridShape,
    LegendPosition,
    LineStyle,
    PointShape,
)
from drawlib._charts.radar_chart import _renderer as _renderer_module
from drawlib._charts.radar_chart._series import RadarSeries

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class RadarChart:
    """Represents a 2D radar (spider web) chart."""

    def __init__(
        self,
        categories: list[str],
        radius: float = 25.0,
        min_value: float = 0.0,
        max_value: float | None = None,
        levels: int = 5,
        grid_shape: GridShape = "polygon",
        show_grid_labels: bool = True,
        grid_label_format: FormatterType = None,
        grid_style: Style | None = None,
        spoke_style: Style | None = None,
        category_label_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
        legend_position: LegendPosition = "right",
        show_values: bool = False,
        value_format: FormatterType = None,
        value_label_style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> None:
        """Initialize RadarChart.

        Args:
            categories: List of category/dimension names (minimum 3).
            radius: Outer radius of the radar web. Defaults to 25.0.
            min_value: Baseline value at the center origin. Defaults to 0.0.
            max_value: Outer boundary value. If None, calculated automatically.
            levels: Number of concentric grid rings. Defaults to 5.
            grid_shape: Grid contour style ("polygon" or "circle"). Defaults to "polygon".
            show_grid_labels: Whether to display numeric scale values along reference spoke. Defaults to True.
            grid_label_format: Formatter string or function for scale levels.
            grid_style: Optional Style overriding concentric grid lines.
            spoke_style: Optional Style overriding radial spoke lines.
            category_label_style: Optional Style overriding category label typography.
            title: Title text at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            legend_position: Legend placement ("right", "bottom", "top", "none", "auto"). Defaults to "right".
            show_values: Whether to print numeric values next to series vertices. Defaults to False.
            value_format: Formatter string or function for vertex values.
            value_label_style: Optional Style overriding vertex value typography.
            width: Optional total chart width override.
            height: Optional total chart height override.

        Raises:
            ValueError: If fewer than 3 categories are provided.
        """
        if len(categories) < 3:
            raise ValueError(f"RadarChart requires at least 3 categories, but got {len(categories)}.")

        self._categories = list(categories)
        self.radius = float(radius)
        self.min_value = float(min_value)
        self.max_value = float(max_value) if max_value is not None else None
        self.levels = max(1, int(levels))
        self.grid_shape: GridShape = grid_shape
        self.show_grid_labels = show_grid_labels
        self.grid_label_format: FormatterType = grid_label_format
        self.grid_style: Style | None = grid_style
        self.spoke_style: Style | None = spoke_style
        self.category_label_style: Style | None = category_label_style
        self.title = title
        self.title_style: Style | None = title_style
        self.legend_position: LegendPosition = legend_position
        self.show_values = show_values
        self.value_format: FormatterType = value_format
        self.value_label_style: Style | None = value_label_style

        self._custom_width = float(width) if width is not None else None
        self._custom_height = float(height) if height is not None else None
        self._series: list[RadarSeries] = []

    @property
    def categories(self) -> list[str]:
        """List of category labels."""
        return list(self._categories)

    @property
    def series(self) -> list[RadarSeries]:
        """List of registered RadarSeries."""
        return list(self._series)

    def add_series(
        self,
        name: str,
        values: list[float],
        color: ColorType | None = None,
        fill_alpha: float = 0.25,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        show_points: bool = True,
        point_shape: PointShape = "circle",
        point_size: float = 0.8,
        style: Style | None = None,
    ) -> RadarSeries:
        """Add a new data series to the radar chart.

        Args:
            name: Series name displayed in legend.
            values: Numeric values for each category.
            color: Series fill and stroke color.
            fill_alpha: Transparency of polygon fill (0.0 to 1.0). Defaults to 0.25.
            line_width: Perimeter stroke width. Defaults to 2.0.
            line_style: Perimeter stroke pattern. Defaults to "solid".
            show_points: Whether to render vertex markers. Defaults to True.
            point_shape: Marker shape. Defaults to "circle".
            point_size: Marker radius. Defaults to 0.8.
            style: Optional Style overriding series appearance.

        Returns:
            RadarSeries: The newly created and registered series.
        """
        s = RadarSeries(
            name=name,
            values=values,
            color=color,
            fill_alpha=fill_alpha,
            line_width=line_width,
            line_style=line_style,
            show_points=show_points,
            point_shape=point_shape,
            point_size=point_size,
            style=style,
        )
        self._series.append(s)
        return s

    def get_size(self) -> tuple[float, float]:
        """Compute the total dimensions (width, height) of this chart."""
        if self._custom_width is not None and self._custom_height is not None:
            return (self._custom_width, self._custom_height)

        diameter = self.radius * 2.0
        extra_w = 26.0 if self.legend_position == "right" else 16.0
        extra_h = (8.0 if self.title else 0.0) + (14.0 if self.legend_position in {"top", "bottom"} else 0.0) + 16.0
        w = self._custom_width if self._custom_width is not None else diameter + extra_w
        h = self._custom_height if self._custom_height is not None else diameter + extra_h
        return (w, h)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this radar chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) where the bottom-left corner is anchored.
        """
        _renderer_module.draw_radar_chart(self, xy)
