# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""BoxChart container class implementation."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Literal

import drawlib._charts.box_chart._renderer as _renderer_module
from drawlib._charts._common._axis import Axis
from drawlib._charts._common._base import AxisChartMixin, draw_with_box_overrides
from drawlib._charts._common._types import (
    DrawDirection,
    FormatterType,
    Orientation,
    PointShape,
    WhiskerMode,
)
from drawlib._charts.box_chart._series import Series
from drawlib._charts.box_chart._stats import BoxStats
from drawlib._core.l1_core import validate_call
from drawlib._core.l3_styles import Style

__all__ = ["BoxChart"]


def _check_finite_range(
    val: float,
    name: str,
    *,
    min_val: float | None = None,
    max_val: float | None = None,
    strict_min: bool = False,
) -> float:
    """Validate that a numeric parameter is finite and within expected bounds."""
    f = float(val)
    if not math.isfinite(f):
        raise ValueError(f"{name} must be a finite number, got {val!r}.")
    if min_val is not None:
        if strict_min and f <= min_val:
            raise ValueError(f"{name} must be > {min_val}, got {f}.")
        if not strict_min and f < min_val:
            raise ValueError(f"{name} must be >= {min_val}, got {f}.")
    if max_val is not None and f > max_val:
        raise ValueError(f"{name} must be <= {max_val}, got {f}.")
    return f


class BoxChart(AxisChartMixin):
    """Configurable container and builder for box plots, strip plots, and hybrid overlays.

    Attributes:
        axis_line_style: Style defining baseline coordinate axis lines.
        width: Total width of the chart container on the canvas.
        height: Total height of the chart container on the canvas.
        categories: List of category names along the categorical axis.
        orientation: Distribution orientation ("vertical" or "horizontal").
        show_box: Default visibility of Q1-Q3 boxes, whiskers, and median lines.
        show_points: Default visibility of strip/jitter sample markers.
        show_outliers: Default visibility of outlier markers when ``show_points=False``.
        show_mean: Default visibility of arithmetic mean markers.
        whisker_mode: Whisker calculation rule ("iqr", "min_max", or "percentile").
        iqr_k: Multiplier applied to IQR when ``whisker_mode="iqr"``.
        whisker_percentiles: ``(low_p, high_p)`` percentiles for ``whisker_mode="percentile"``.
        box_width_ratio: Ratio of category slot occupied by the box cluster.
        cap_width_ratio: Ratio of individual box width occupied by whisker T-caps.
        box_r: Corner rounding radius applied to Q1-Q3 boxes.
        jitter: Default normalized horizontal/vertical spread ratio for strip points.
        jitter_seed: Deterministic integer seed for strip point jitter offsets.
        point_radius: Default marker radius for strip, outlier, and mean points.
        point_shape: Default marker shape for strip points.
        outlier_shape: Marker shape for outlier points.
        mean_shape: Marker shape for mean points.
        axis_text_style: Optional Style for axis tick labels and category names.
        grid_style: Optional Style for background gridlines.
        value_text_style: Optional Style for inline median value labels.
        value_format: Custom string template or callable formatter for inline value labels.
        background_style: Optional Style for the outer chart background card.
        title: Chart title text displayed at the top of the container.
        title_style: Optional Style for the chart title typography.
        x_axis: Horizontal Axis configuration model.
        y_axis: Vertical Axis configuration model.
    """

    @validate_call
    def __init__(
        self,
        *,
        axis_line_style: Style,
        width: float = 68.0,
        height: float = 44.0,
        categories: list[str] | None = None,
        orientation: Literal["vertical", "horizontal"] = "vertical",
        show_box: bool = True,
        show_points: bool = False,
        show_outliers: bool = True,
        show_mean: bool = False,
        whisker_mode: Literal["iqr", "min_max", "percentile"] = "iqr",
        iqr_k: float = 1.5,
        whisker_percentiles: tuple[float, float] = (5.0, 95.0),
        box_width_ratio: float = 0.65,
        cap_width_ratio: float = 0.45,
        box_r: float = 0.0,
        jitter: float = 0.45,
        jitter_seed: int = 42,
        point_radius: float = 0.58,
        point_shape: Literal["circle", "square", "rhombus", "triangle", "none"] = "circle",
        outlier_shape: Literal["circle", "square", "rhombus", "triangle", "none"] = "circle",
        mean_shape: Literal["circle", "square", "rhombus", "triangle", "none"] = "rhombus",
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        value_format: FormatterType = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None:
        """Initialize BoxChart.

        Args:
            axis_line_style: Style defining baseline coordinate axis lines.
            width: Width of the chart on the canvas. Defaults to 68.0.
            height: Height of the chart on the canvas. Defaults to 44.0.
            categories: Category names (e.g. ["Baseline", "Streaming", "Batch"]).
            orientation: Distribution orientation ("vertical" or "horizontal").
                Defaults to "vertical".
            show_box: Whether to draw boxes, whiskers, and medians by default.
                Defaults to True.
            show_points: Whether to draw strip/jitter sample points by default.
                Defaults to False.
            show_outliers: Whether to draw outlier markers when ``show_box=True`` and
                ``show_points=False``. Defaults to True.
            show_mean: Whether to draw arithmetic mean markers by default.
                Defaults to False.
            whisker_mode: Whisker calculation rule ("iqr", "min_max", or "percentile").
                Defaults to "iqr".
            iqr_k: IQR fence multiplier when ``whisker_mode="iqr"``. Defaults to 1.5.
            whisker_percentiles: ``(low_p, high_p)`` percentiles in [0.0, 100.0] when
                ``whisker_mode="percentile"``. Defaults to ``(5.0, 95.0)``.
            box_width_ratio: Ratio of category slot occupied by boxes (0.05 to 1.0).
                Defaults to 0.65.
            cap_width_ratio: Ratio of box width occupied by whisker T-caps (0.0 to 1.0).
                Defaults to 0.45.
            box_r: Corner rounding radius for Q1-Q3 boxes. Defaults to 0.0.
            jitter: Normalized transverse spread ratio for strip points (0.0 to 1.0).
                Set to 0.0 for an aligned 1D strip plot. Defaults to 0.45.
            jitter_seed: Deterministic seed for strip point jitter. Defaults to 42.
            point_radius: Default marker radius for points, outliers, and means.
                Defaults to 0.58.
            point_shape: Default marker shape for strip points. Defaults to "circle".
            outlier_shape: Marker shape for outlier points. Defaults to "circle".
            mean_shape: Marker shape for mean points. Defaults to "rhombus".
            axis_text_style: Optional Style for axis tick labels and category names.
            grid_style: Optional Style for background gridlines.
            value_text_style: Optional Style for inline median value labels.
            value_format: Format string (e.g. "{:.1f}ms") or callable for value labels.
            background_style: Optional Style for the chart background card.
            title: Title of the chart. Defaults to "".
            title_style: Optional Style for the chart title typography.
        """
        if not show_box and not show_points:
            raise ValueError("At least one of show_box or show_points must be True.")

        self.axis_line_style: Style = axis_line_style
        self.width: float = _check_finite_range(width, "width", min_val=0.0, strict_min=True)
        self.height: float = _check_finite_range(height, "height", min_val=0.0, strict_min=True)
        self.categories: list[str] = list(categories) if categories is not None else []
        self.orientation: Orientation = orientation
        self.show_box: bool = bool(show_box)
        self.show_points: bool = bool(show_points)
        self.show_outliers: bool = bool(show_outliers)
        self.show_mean: bool = bool(show_mean)
        self.whisker_mode: WhiskerMode = whisker_mode
        self.iqr_k: float = _check_finite_range(iqr_k, "iqr_k", min_val=0.0)

        low_p = _check_finite_range(whisker_percentiles[0], "whisker_percentiles[0]", min_val=0.0, max_val=100.0)
        high_p = _check_finite_range(whisker_percentiles[1], "whisker_percentiles[1]", min_val=0.0, max_val=100.0)
        if low_p >= high_p:
            raise ValueError(f"whisker_percentiles must satisfy low < high, got ({low_p}, {high_p}).")
        self.whisker_percentiles: tuple[float, float] = (low_p, high_p)

        self.box_width_ratio: float = _check_finite_range(
            box_width_ratio, "box_width_ratio", min_val=0.0, max_val=1.0, strict_min=True
        )
        self.cap_width_ratio: float = _check_finite_range(
            cap_width_ratio, "cap_width_ratio", min_val=0.0, max_val=1.0
        )
        self.box_r: float = _check_finite_range(box_r, "box_r", min_val=0.0)
        self.jitter: float = _check_finite_range(jitter, "jitter", min_val=0.0, max_val=1.0)
        self.jitter_seed: int = int(jitter_seed)
        self.point_radius: float = _check_finite_range(point_radius, "point_radius", min_val=0.0, strict_min=True)
        self.point_shape: PointShape = point_shape
        self.outlier_shape: PointShape = outlier_shape
        self.mean_shape: PointShape = mean_shape
        self.axis_text_style: Style | None = axis_text_style
        self.grid_style: Style | None = grid_style
        self.value_text_style: Style | None = value_text_style
        self.value_format: FormatterType = value_format
        self.background_style: Style | None = background_style
        self.title: str = title
        self.title_style: Style | None = title_style

        self.x_axis: Axis = Axis()
        self.y_axis: Axis = Axis()
        self._series: list[Series] = []

    @property
    def series(self) -> list[Series]:
        """Get list of registered Series."""
        return list(self._series)

    @property
    def value_axis(self) -> Axis:
        """Get the numerical value axis (y_axis for vertical, x_axis for horizontal)."""
        return self.y_axis if self.orientation == "vertical" else self.x_axis

    @property
    def category_axis(self) -> Axis:
        """Get the categorical axis (x_axis for vertical, y_axis for horizontal)."""
        return self.x_axis if self.orientation == "vertical" else self.y_axis

    @validate_call
    def add_series(
        self,
        name: str,
        data: Sequence[BoxStats | Sequence[float] | None],
        style: Style,
        legend_text_style: Style | None = None,
        *,
        show_box: bool | None = None,
        show_points: bool | None = None,
        show_outliers: bool | None = None,
        show_mean: bool | None = None,
        median_style: Style | None = None,
        whisker_style: Style | None = None,
        point_style: Style | None = None,
        outlier_style: Style | None = None,
        mean_style: Style | None = None,
        point_radius: float | None = None,
        point_shape: Literal["circle", "square", "rhombus", "triangle", "none"] | None = None,
        jitter: float | None = None,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: Literal["bottom_to_top", "left_to_right"] | None = None,
    ) -> Series:
        """Add a categorical distribution series to the chart.

        Args:
            name: Series label shown in the legend.
            data: Per-category items, where each item is a sequence of sample floats,
                a pre-aggregated ``BoxStats`` object, an empty sequence ``[]``, or ``None``.
            style: Base Style defining box fill/outline and automatic marker colors.
            legend_text_style: Optional custom text style for this series in the legend.
            show_box: Optional per-series override for drawing Q1-Q3 boxes and whiskers.
            show_points: Optional per-series override for drawing strip/jitter points.
            show_outliers: Optional per-series override for drawing outlier markers.
            show_mean: Optional per-series override for drawing arithmetic mean markers.
            median_style: Optional Style override for the median line.
            whisker_style: Optional Style override for whisker stems and caps.
            point_style: Optional Style override for strip/jitter sample markers.
            outlier_style: Optional Style override for outlier markers.
            mean_style: Optional Style override for the mean marker.
            point_radius: Optional per-series marker radius override.
            point_shape: Optional per-series strip point marker shape override.
            jitter: Optional per-series normalized jitter spread override in [0.0, 1.0].
            show: Whether to render this series on the canvas. Defaults to True.
            draw_ratio: Spatial rendering ratio from 0.0 to 1.0. Defaults to 1.0.
            draw_direction: Partial rendering direction ("bottom_to_top" or "left_to_right").

        Returns:
            Series: The newly created and registered distribution series.
        """
        eff_show_box = self.show_box if show_box is None else bool(show_box)
        eff_show_points = self.show_points if show_points is None else bool(show_points)
        eff_show_outliers = self.show_outliers if show_outliers is None else bool(show_outliers)
        eff_show_mean = self.show_mean if show_mean is None else bool(show_mean)
        if not eff_show_box and not eff_show_points:
            raise ValueError("At least one of show_box or show_points must be True.")

        eff_radius = (
            _check_finite_range(point_radius, "point_radius", min_val=0.0, strict_min=True)
            if point_radius is not None
            else self.point_radius
        )
        eff_shape: PointShape = point_shape if point_shape is not None else self.point_shape
        eff_jitter = (
            _check_finite_range(jitter, "jitter", min_val=0.0, max_val=1.0)
            if jitter is not None
            else self.jitter
        )
        eff_dir: DrawDirection = (
            draw_direction
            if draw_direction is not None
            else ("bottom_to_top" if self.orientation == "vertical" else "left_to_right")
        )

        normalized_stats: list[BoxStats | None] = []
        for item in data:
            if item is None:
                normalized_stats.append(None)
            elif isinstance(item, BoxStats):
                if eff_show_points and not eff_show_box and not item.points:
                    raise ValueError(
                        "BoxStats without 'points' cannot be rendered when show_box=False and show_points=True."
                    )
                normalized_stats.append(item)
            elif len(item) == 0:
                normalized_stats.append(None)
            else:
                normalized_stats.append(
                    BoxStats.from_values(
                        item,
                        whisker_mode=self.whisker_mode,
                        iqr_k=self.iqr_k,
                        whisker_percentiles=self.whisker_percentiles,
                    )
                )

        s = Series(
            name=name,
            stats=normalized_stats,
            style=style,
            legend_text_style=legend_text_style,
            show_box=eff_show_box,
            show_points=eff_show_points,
            show_outliers=eff_show_outliers,
            show_mean=eff_show_mean,
            median_style=median_style,
            whisker_style=whisker_style,
            point_style=point_style,
            outlier_style=outlier_style,
            mean_style=mean_style,
            point_radius=eff_radius,
            point_shape=eff_shape,
            jitter=eff_jitter,
            show=show,
            draw_ratio=draw_ratio,
            draw_direction=eff_dir,
        )
        self._series.append(s)
        return s

    @validate_call
    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        width: float | None = None,
        height: float | None = None,
        align: Literal["bottom_left", "center"] = "bottom_left",
        scale: float = 1.0,
    ) -> None:
        """Render this box/strip chart onto the canvas at base coordinate xy.

        Args:
            xy: Canvas placement coordinate (x, y) (interpreted via align).
            width: Optional temporary width override for this draw call.
            height: Optional temporary height override for this draw call.
            align: Anchor alignment of xy ("bottom_left" or "center").
                Defaults to "bottom_left".
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        draw_with_box_overrides(
            self,
            _renderer_module.draw_box_chart,
            xy,
            width=width,
            height=height,
            align=align,
            scale=scale,
        )
