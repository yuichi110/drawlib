# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Series container model for BoxChart."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import DrawDirection, PointShape

if TYPE_CHECKING:
    from drawlib._charts.box_chart._stats import BoxStats
    from drawlib._core.l3_styles import Style

__all__ = ["Series"]


class Series:
    """Represents a single distribution data series in a BoxChart.

    Attributes:
        name: Series label shown in the legend.
        stats: Per-category computed or pre-aggregated ``BoxStats`` (or ``None`` for empty slots).
        style: Base Style defining box fill/border and automatic sub-element colors.
        legend_text_style: Optional custom text style for this series in the legend.
        show_box: Whether to draw the Q1-Q3 box, whiskers, and median line.
        show_points: Whether to draw individual sample strip/jitter markers.
        show_outliers: Whether to draw outlier markers when ``show_box=True`` and ``show_points=False``.
        show_mean: Whether to draw the arithmetic mean marker.
        median_style: Optional Style override for the median line.
        whisker_style: Optional Style override for whisker stems and T-caps.
        point_style: Optional Style override for strip/jitter sample markers.
        outlier_style: Optional Style override for outlier markers.
        mean_style: Optional Style override for the mean marker.
        point_radius: Marker radius for points, outliers, and mean markers.
        point_shape: Marker shape for strip/jitter sample points.
        jitter: Normalized jitter width ratio in [0.0, 1.0].
        show: Whether to render this series on the canvas.
        draw_ratio: Spatial partial rendering ratio from 0.0 to 1.0.
        draw_direction: Partial rendering direction ("bottom_to_top" or "left_to_right").
    """

    def __init__(
        self,
        name: str,
        stats: list[BoxStats | None],
        style: Style,
        legend_text_style: Style | None = None,
        *,
        show_box: bool = True,
        show_points: bool = False,
        show_outliers: bool = True,
        show_mean: bool = False,
        median_style: Style | None = None,
        whisker_style: Style | None = None,
        point_style: Style | None = None,
        outlier_style: Style | None = None,
        mean_style: Style | None = None,
        point_radius: float = 0.58,
        point_shape: PointShape = "circle",
        jitter: float = 0.45,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "bottom_to_top",
    ) -> None:
        """Initialize Series."""
        if not show_box and not show_points:
            raise ValueError("At least one of show_box or show_points must be True.")
        if point_radius <= 0.0:
            raise ValueError(f"point_radius must be > 0.0, got {point_radius}.")
        if not (0.0 <= jitter <= 1.0):
            raise ValueError(f"jitter must be between 0.0 and 1.0, got {jitter}.")

        self.name: str = name
        self.stats: list[BoxStats | None] = list(stats)
        self.style: Style = style
        self.legend_text_style: Style | None = legend_text_style
        self.show_box: bool = bool(show_box)
        self.show_points: bool = bool(show_points)
        self.show_outliers: bool = bool(show_outliers)
        self.show_mean: bool = bool(show_mean)
        self.median_style: Style | None = median_style
        self.whisker_style: Style | None = whisker_style
        self.point_style: Style | None = point_style
        self.outlier_style: Style | None = outlier_style
        self.mean_style: Style | None = mean_style
        self.point_radius: float = float(point_radius)
        self.point_shape: PointShape = point_shape
        self.jitter: float = float(jitter)
        self.show: bool = bool(show)
        self.draw_ratio: float = float(draw_ratio)
        self.draw_direction: DrawDirection = draw_direction
