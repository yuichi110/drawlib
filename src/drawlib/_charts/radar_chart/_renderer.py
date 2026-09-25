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
from drawlib._charts._common._legend import get_legend_size, render_legend
from drawlib._charts._common._types import ColorType, FormatterType
from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.colors import Colors
from drawlib.lines import line as canvas_line
from drawlib.lines import lines as canvas_lines
from drawlib.shapes import circle as canvas_circle
from drawlib.shapes import polygon as canvas_polygon
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.radar_chart._chart import RadarChart
    from drawlib._charts.radar_chart._series import RadarSeries

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)
_DEFAULT_MUTED_TEXT = (148, 163, 184, 1.0)
_DEFAULT_GRID_COLOR = (226, 232, 240, 1.0)
_DEFAULT_SPOKE_COLOR = (203, 213, 225, 1.0)


def _with_alpha(color: ColorType, alpha: float) -> tuple[int, int, int, float]:
    """Return an RGBA color tuple replacing alpha with given ratio."""
    return (int(color[0]), int(color[1]), int(color[2]), float(alpha))


def _resolve_series_colors(series_list: list[RadarSeries]) -> list[ColorType]:
    """Resolve fill/stroke colors for all series."""
    colors: list[ColorType] = []
    for i, s in enumerate(series_list):
        if s.color is not None:
            colors.append(s.color)
        else:
            colors.append(DEFAULT_CHART_PALETTE[i % len(DEFAULT_CHART_PALETTE)])
    return colors


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

    default_grid_style = Style(
        line_color=_DEFAULT_GRID_COLOR,
        line_width=1.0,
    )
    grid_style = default_grid_style.patch(chart.grid_style)
    circle_grid_style = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=grid_style.line_color if grid_style.line_color is not None else _DEFAULT_GRID_COLOR,
        shape_line_width=grid_style.line_width if grid_style.line_width is not None else 1.0,
    )
    default_spoke_style = Style(
        line_color=_DEFAULT_SPOKE_COLOR,
        line_width=1.0,
    )
    spoke_style = default_spoke_style.patch(chart.spoke_style)
    scale_label_style = Style(
        text_size=8.5,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT,
        text_halign="left",
        text_valign="bottom",
    )

    # 1. Concentric grid rings
    for k in range(1, chart.levels + 1):
        ratio = k / chart.levels
        ring_r = chart.radius * ratio
        level_val = chart.min_value + ratio * span

        if chart.grid_shape == "polygon":
            ring_pts = [(cx + ring_r * math.cos(a), cy + ring_r * math.sin(a)) for a in angles]
            canvas_lines(xys=ring_pts + [ring_pts[0]], style=grid_style)
        else:
            canvas_circle(xy=center, radius=ring_r, style=circle_grid_style)

        if chart.show_grid_labels:
            lbl_str = _format_value(chart.grid_label_format, level_val)
            # Render slightly offset from the top spoke
            canvas_text(xy=(cx + 0.8, cy + ring_r + 0.3), text=lbl_str, style=scale_label_style)

    # 2. Radial spokes
    for a in angles:
        spoke_end = (cx + chart.radius * math.cos(a), cy + chart.radius * math.sin(a))
        canvas_line(xy1=center, xy2=spoke_end, style=spoke_style)


def _draw_category_labels(
    chart: RadarChart,
    center: tuple[float, float],
    angles: list[float],
) -> None:
    """Render category labels around the perimeter."""
    cx, cy = center
    offset_r = chart.radius + 3.0

    for i, (cat, a) in enumerate(zip(chart.categories, angles, strict=False)):
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

        default_lbl_style = Style(
            text_size=10.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign=halign,
            text_valign=valign,
        )
        lbl_style = default_lbl_style.patch(chart.category_label_style)
        canvas_text(xy=(lx, ly), text=cat, style=lbl_style)


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

    default_val_label_style = Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="bottom",
    )
    val_label_style = default_val_label_style.patch(chart.value_label_style)

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
        fill_style = Style(
            shape_fill_color=_with_alpha(color, s.fill_alpha),
            shape_line_color=Colors.Transparent,
            shape_line_width=0,
        )
        canvas_polygon(xys=pts, style=fill_style)

        # 2. Outer border stroke
        default_stroke_style = Style(
            line_color=color,
            line_width=s.line_width,
            line_style=s.line_style,
        )
        stroke_style = default_stroke_style.patch(s.style)
        canvas_lines(xys=pts + [pts[0]], style=stroke_style)

        # 3. Vertex markers
        if s.show_points and s.point_shape != "none":
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

                if chart.show_values:
                    v_str = _format_value(chart.value_format, val)
                    canvas_text(xy=(px, py + s.point_size + 1.2), text=v_str, style=val_label_style)


def draw_radar_chart(chart: RadarChart, xy: tuple[float, float]) -> None:
    """Render a complete RadarChart onto the canvas."""
    c_min_x, c_min_y = xy
    chart_w, chart_h = chart.get_size()
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    num_cats = len(chart.categories)
    if num_cats < 3:
        return

    # Angular progression: top spoke is 90 degrees, progressing clockwise
    angles = [math.radians(90.0 - i * (360.0 / num_cats)) for i in range(num_cats)]
    eff_max = _calculate_max_value(chart)

    series_names = [s.name for s in chart.series]
    series_colors = _resolve_series_colors(chart.series)
    legend_w, legend_h = get_legend_size(chart.legend_position, series_names, len(chart.series))

    if chart.title:
        default_t_style = Style(
            text_size=12.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        t_style = default_t_style.patch(chart.title_style)
        canvas_text(xy=((c_min_x + c_max_x) / 2.0, c_max_y - 3.5), text=chart.title, style=t_style)

    # Compute center coordinates based on legend placement
    if chart.legend_position == "right":
        center_x = c_min_x + chart.radius + 8.0
        center_y = c_min_y + (chart_h - (4.0 if chart.title else 0.0)) / 2.0
        p_bounds = (c_min_x, c_min_y, center_x + chart.radius + 6.0, c_max_y)
    elif chart.legend_position in {"top", "bottom"}:
        center_x = c_min_x + chart_w / 2.0
        center_y = c_min_y + chart.radius + (12.0 if chart.legend_position == "bottom" else 4.0)
        p_min_y_bound = c_min_y + (7.0 if chart.legend_position == "bottom" else 0.0)
        p_max_y_bound = c_max_y - (7.0 if chart.legend_position == "top" else 0.0)
        p_bounds = (c_min_x, p_min_y_bound, c_max_x, p_max_y_bound)
    else:
        center_x = c_min_x + chart_w / 2.0
        center_y = c_min_y + chart_h / 2.0
        p_bounds = (c_min_x, c_min_y, c_max_x, c_max_y)

    render_legend(
        names=series_names,
        colors=series_colors,
        position=chart.legend_position,
        plot_bounds=p_bounds,
        chart_bounds=(c_min_x, c_min_y, c_max_x, c_max_y),
    )

    _draw_radar_grid(chart, (center_x, center_y), angles, eff_max)
    _draw_category_labels(chart, (center_x, center_y), angles)
    _draw_series(chart, (center_x, center_y), angles, series_colors, eff_max)
