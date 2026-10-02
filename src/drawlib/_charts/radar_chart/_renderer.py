# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for RadarChart."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from drawlib._charts._common._axis import _get_nice_step
from drawlib._charts._common._style_utils import ensure_line_style, ensure_shape_style, ensure_text_style
from drawlib._charts._common._types import ColorType, FormatterType
from drawlib._core.l3_colors import Color
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import polygon as canvas_polygon
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.radar_chart._chart import RadarChart
    from drawlib._charts.radar_chart._series import Series


def _with_alpha(color: ColorType, alpha: float) -> tuple[int, int, int, float]:
    """Return an RGBA color tuple replacing alpha with given ratio."""
    c = color if isinstance(color, Color) else Color(color)
    return (c.r, c.g, c.b, float(alpha))


def _resolve_series_colors(series_list: list[Series]) -> list[ColorType]:
    """Resolve fill/stroke colors for all series."""
    return [
        s.style.line_color or s.style.shape_fill_color or s.style.shape_line_color or (30, 41, 59, 1.0)
        for s in series_list
    ]


def _format_value(fmt: FormatterType, value: float) -> str:
    """Format numeric value using string template or function."""
    if isinstance(fmt, str):
        try:
            return fmt.format(value)
        except Exception:
            return f"{value:g}"
    if callable(fmt):
        return str(fmt(value))
    return f"{value:g}"


def _calculate_max_value(chart: RadarChart) -> float:
    """Determine effective maximum value for the radar axes."""
    if chart.max_value is not None:
        return chart.max_value

    all_vals: list[float] = []
    for s in chart.series:
        all_vals.extend(s.values)

    data_max = max(all_vals, default=100.0)
    if data_max <= chart.min_value:
        data_max = chart.min_value + 100.0

    span = data_max - chart.min_value
    step = _get_nice_step(span, target_ticks=chart.levels)
    eff_max = chart.min_value + math.ceil(span / step) * step
    if eff_max <= data_max:
        eff_max += step
    return eff_max


def _draw_radar_grid(
    chart: RadarChart,
    center: tuple[float, float],
    angles: list[float],
    eff_max: float,
) -> None:
    """Render concentric grid rings, radial spokes, and scale labels."""
    cx, cy = center
    span = eff_max - chart.min_value

    # 1. Concentric grid rings
    if chart.grid_style is not None:
        for k in range(1, chart.levels + 1):
            ratio = k / chart.levels
            ring_r = chart.radius * ratio

            if chart.grid_shape == "polygon":
                ring_pts = [(cx + ring_r * math.cos(a), cy + ring_r * math.sin(a)) for a in angles]
                canvas_lines(xys=ring_pts + [ring_pts[0]], style=ensure_line_style(chart.grid_style))
            else:
                grid_color = (
                    chart.grid_style.line_color or chart.grid_style.shape_line_color or (200, 200, 200, 1.0)
                )
                circle_grid_style = Style(
                    shape_fill_color=(0, 0, 0, 0.0),
                    shape_line_color=grid_color,
                    shape_line_width=chart.grid_style.line_width or chart.grid_style.shape_line_width or 1.0,
                    shape_line_style=chart.grid_style.line_style or chart.grid_style.shape_line_style or "solid",
                )
                canvas_circle(xy=center, radius=ring_r, style=circle_grid_style)

    # 2. Scale labels along top spoke
    if chart.scale_text_style is not None and span > 0:
        scale_style = ensure_text_style(chart.scale_text_style, halign="left", valign="bottom")
        for k in range(1, chart.levels + 1):
            ratio = k / chart.levels
            ring_r = chart.radius * ratio
            level_val = chart.min_value + ratio * span
            lbl_str = _format_value(chart.scale_format, level_val)
            canvas_text(xy=(cx + 0.8, cy + ring_r + 0.3), text=lbl_str, style=scale_style)

    # 3. Radial spokes (mandatory anchor)
    spoke_line_style = ensure_line_style(chart.axis_line_style)
    for a in angles:
        spoke_end = (cx + chart.radius * math.cos(a), cy + chart.radius * math.sin(a))
        canvas_line(xy1=center, xy2=spoke_end, style=spoke_line_style)


def _draw_category_labels(
    chart: RadarChart,
    center: tuple[float, float],
    angles: list[float],
) -> None:
    """Render category labels around the perimeter."""
    if chart.axis_text_style is None:
        return

    cx, cy = center
    offset_r = chart.radius + 3.0

    for cat, a in zip(chart.categories, angles, strict=False):
        cos_a = math.cos(a)
        sin_a = math.sin(a)

        lx = cx + offset_r * cos_a
        ly = cy + offset_r * sin_a

        if cos_a > 0.35:
            halign = "left"
        elif cos_a < -0.35:
            halign = "right"
        else:
            halign = "center"

        if sin_a > 0.35:
            valign = "bottom"
        elif sin_a < -0.35:
            valign = "top"
        else:
            valign = "center"

        lbl_style = ensure_text_style(chart.axis_text_style, halign=halign, valign=valign)
        canvas_text(xy=(lx, ly), text=cat, style=lbl_style)


def _draw_series_markers_and_labels(
    chart: RadarChart,
    s: Series,
    pts: list[tuple[float, float]],
    color: ColorType,
) -> None:
    """Render vertex markers and value text labels for a single series."""
    if s.point_shape == "none" or s.point_size <= 0.0:
        return

    marker_style = Style(
        shape_fill_color=(255, 255, 255, 1.0),
        shape_line_color=color,
        shape_line_width=1.5,
    )
    for (px, py), val in zip(pts, s.values, strict=False):
        if s.point_shape == "circle":
            canvas_circle(xy=(px, py), radius=s.point_size, style=marker_style)
        elif s.point_shape == "square":
            side = s.point_size * 1.6
            canvas_rectangle(xy=(px, py), width=side, height=side, style=marker_style)

        if chart.value_text_style is not None:
            v_str = _format_value(chart.value_format, val)
            v_style = ensure_text_style(chart.value_text_style, halign="center", valign="bottom")
            canvas_text(xy=(px, py + s.point_size + 1.2), text=v_str, style=v_style)


def _draw_series(
    chart: RadarChart,
    center: tuple[float, float],
    angles: list[float],
    series_colors: list[ColorType],
    eff_max: float,
) -> None:
    """Render closed series polygons, vertex markers, and optional value labels."""
    cx, cy = center
    span = eff_max - chart.min_value
    if span <= 0:
        return

    for s_idx, s in enumerate(chart.series):
        if not s.values:
            continue

        color = series_colors[s_idx]
        pts: list[tuple[float, float]] = []

        for i, a in enumerate(angles):
            val = s.values[i] if i < len(s.values) else chart.min_value
            clamped_val = max(chart.min_value, min(eff_max, val))
            ratio = (clamped_val - chart.min_value) / span
            r = chart.radius * ratio
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

        # 1. Filled transparent polygon
        if s.fill_alpha > 0.0:
            fill_style = Style(
                shape_fill_color=_with_alpha(color, s.fill_alpha),
                shape_line_color=(0, 0, 0, 0.0),
                shape_line_width=0,
            )
            canvas_polygon(xys=pts, style=fill_style)

        # 2. Outer border stroke
        stroke_style = ensure_line_style(
            Style(
                line_color=color,
                line_width=s.line_width,
                line_style=s.line_style,
            ).patch(s.style)
        )
        canvas_lines(xys=pts + [pts[0]], style=stroke_style)

        # 3. Vertex markers and labels
        _draw_series_markers_and_labels(chart, s, pts, color)


def draw_radar_chart(chart: RadarChart, xy: tuple[float, float]) -> None:
    """Render a complete RadarChart onto the canvas."""
    c_min_x, c_min_y = xy
    chart_w, chart_h = chart.get_size()
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    # 1. Background
    if chart.background_style is not None:
        canvas_rectangle(
            xy=(c_min_x + chart_w / 2.0, c_min_y + chart_h / 2.0),
            width=chart_w,
            height=chart_h,
            style=ensure_shape_style(chart.background_style),
        )

    # 2. Title
    if chart.title and chart.title_style is not None:
        t_style = ensure_text_style(chart.title_style, halign="center", valign="bottom")
        canvas_text(xy=((c_min_x + c_max_x) / 2.0, c_max_y - 3.5), text=chart.title, style=t_style)

    num_cats = len(chart.categories)
    if num_cats < 3:
        return

    # Angular progression: top spoke is 90 degrees, progressing clockwise
    angles = [math.radians(90.0 - i * (360.0 / num_cats)) for i in range(num_cats)]
    eff_max = _calculate_max_value(chart)
    series_colors = _resolve_series_colors(chart.series)

    has_title = bool(chart.title and chart.title_style is not None)
    center_x = c_min_x + chart_w / 2.0
    center_y = c_min_y + (chart_h - (6.0 if has_title else 0.0)) / 2.0

    _draw_radar_grid(chart, (center_x, center_y), angles, eff_max)
    _draw_category_labels(chart, (center_x, center_y), angles)
    _draw_series(chart, (center_x, center_y), angles, series_colors, eff_max)
