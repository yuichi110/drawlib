# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared base classes and mixins for chart containers."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol, TypeVar

import drawlib._charts._common._legend as _legend_module
from drawlib._charts._common._style_utils import resolve_series_color
from drawlib._charts._common._types import FormatterType, Orientation, ScaleType
from drawlib._core import l4_canvas as canvas
from drawlib._core.l3_styles import Style

if TYPE_CHECKING:
    from drawlib._charts._common._axis import Axis


class _LegendElementProtocol(Protocol):
    name: str
    style: Style
    show: bool


_ChartT = TypeVar("_ChartT")
_RadialChartT = TypeVar("_RadialChartT", bound="RadialChartMixin")


def draw_with_box_overrides(
    chart: _ChartT,
    render_fn: Callable[[_ChartT, tuple[float, float]], None],
    xy: tuple[float, float],
    *,
    width: float | None = None,
    height: float | None = None,
    scale: float = 1.0,
) -> None:
    """Execute render_fn with temporary width/height overrides and canvas scale transform."""
    orig_w = getattr(chart, "width")
    orig_h = getattr(chart, "height")
    try:
        if width is not None:
            setattr(chart, "width", float(width))
        if height is not None:
            setattr(chart, "height", float(height))
        with canvas.transform(origin=xy, scale=scale):
            render_fn(chart, xy)
    finally:
        setattr(chart, "width", orig_w)
        setattr(chart, "height", orig_h)


class LegendChartMixin:
    """Mixin providing unified draw_legend() for charts with _series or _slices."""

    def _get_legend_elements(self) -> list[_LegendElementProtocol]:
        """Return registered series or slice objects for legend rendering."""
        if hasattr(self, "_series"):
            return list(getattr(self, "_series"))
        if hasattr(self, "_slices"):
            return list(getattr(self, "_slices"))
        return []

    def draw_legend(
        self,
        xy: tuple[float, float],
        text_style: Style,
        orientation: Orientation = "vertical",
        swatch_size: tuple[float, float] = (2.4, 1.2),
        item_gap: float = 4.0,
        *,
        scale: float = 1.0,
    ) -> None:
        """Render legend for series or slices at coordinate xy.

        Args:
            xy: Starting placement coordinate (x, y).
            text_style: Base Style for legend text labels.
            orientation: Legend orientation ("vertical" or "horizontal"). Defaults to "vertical".
            swatch_size: (width, height) size of color swatches. Defaults to (2.4, 1.2).
            item_gap: Spacing between consecutive legend items. Defaults to 4.0.
            scale: Proportional scaling factor around xy. Defaults to 1.0.
        """
        items = [
            (
                elem.name,
                resolve_series_color(elem.style),
                getattr(elem, "legend_text_style", None),
                bool(getattr(elem, "show", True)),
            )
            for elem in self._get_legend_elements()
        ]
        _legend_module.draw_legend(
            items=items,
            xy=xy,
            text_style=text_style,
            orientation=orientation,
            swatch_size=swatch_size,
            item_gap=item_gap,
            scale=scale,
        )


class AxisChartMixin(LegendChartMixin):
    """Mixin for 2D Cartesian charts with configurable X and Y axes and fixed (width, height)."""

    width: float
    height: float
    x_axis: Axis
    y_axis: Axis

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
        )
        return self.x_axis

    def get_size(self) -> tuple[float, float]:
        """Get the dimensions (width, height) of this chart."""
        return (self.width, self.height)


class RadialChartMixin(LegendChartMixin):
    """Mixin for radial charts (PieChart, RadarChart) with radius and optional custom width/height."""

    radius: float
    title: str
    title_style: Style | None
    _custom_width: float | None
    _custom_height: float | None

    def get_size(self) -> tuple[float, float]:
        """Compute the total dimensions (width, height) of this radial chart."""
        if self._custom_width is not None and self._custom_height is not None:
            return (self._custom_width, self._custom_height)

        diameter = self.radius * 2.0
        has_title = bool(self.title and self.title_style is not None)
        pad = 16.0 if getattr(self, "axis_text_style", None) is not None else 8.0
        w = self._custom_width if self._custom_width is not None else diameter + pad
        h = self._custom_height if self._custom_height is not None else diameter + pad + (6.0 if has_title else 0.0)
        return (w, h)

    def _draw_with_radial_overrides(
        self: _RadialChartT,
        render_fn: Callable[[_RadialChartT, tuple[float, float]], None],
        xy: tuple[float, float],
        *,
        radius: float | None = None,
        width: float | None = None,
        height: float | None = None,
        scale: float = 1.0,
    ) -> None:
        """Execute render_fn with temporary radius/width/height overrides and scale transform."""
        orig_radius = self.radius
        orig_w, orig_h = self._custom_width, self._custom_height
        try:
            if width is not None:
                self._custom_width = float(width)
            if height is not None:
                self._custom_height = float(height)
            if radius is not None:
                self.radius = float(radius)
            elif width is not None or height is not None:
                has_title = bool(self.title and self.title_style is not None)
                pad = 16.0 if getattr(self, "axis_text_style", None) is not None else 8.0
                candidates: list[float] = []
                if self._custom_width is not None:
                    candidates.append(max(2.0, self._custom_width - pad) / 2.0)
                if self._custom_height is not None:
                    candidates.append(max(2.0, self._custom_height - pad - (6.0 if has_title else 0.0)) / 2.0)
                if candidates:
                    self.radius = min(candidates)
            with canvas.transform(origin=xy, scale=scale):
                render_fn(self, xy)
        finally:
            self.radius = orig_radius
            self._custom_width, self._custom_height = orig_w, orig_h
