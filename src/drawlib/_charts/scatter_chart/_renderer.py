# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for ScatterChart."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._style_utils import (
    clamp_ratio,
    ensure_line_style,
    ensure_shape_style,
    ensure_text_style,
)
from drawlib._charts._common._types import PointShape
from drawlib._charts.scatter_chart._point import Point
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import rhombus as canvas_rhombus
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import triangle as canvas_triangle

if TYPE_CHECKING:
    from drawlib._charts.scatter_chart._chart import ScatterChart


def _calculate_plot_bounds(
    chart_xy: tuple[float, float],
    chart_w: float,
    chart_h: float,
    has_title: bool,
    has_axis_text: bool,
    has_x_label: bool,
    has_y_label: bool,
) -> tuple[float, float, float, float]:
    """Calculate internal plot area bounds accounting for labels, ticks, and titles."""
    c_min_x, c_min_y = chart_xy
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    pad_left = (11.0 + (4.0 if has_y_label else 0.0)) if has_axis_text else 3.0
    pad_bottom = (8.0 + (4.0 if has_x_label else 0.0)) if has_axis_text else 3.0
    pad_right = 5.0
    pad_top = 4.0 + (5.0 if has_title else 0.0)

    p_min_x = c_min_x + pad_left
    p_max_x = c_max_x - pad_right
    p_min_y = c_min_y + pad_bottom
    p_max_y = c_max_y - pad_top
    return (p_min_x, p_min_y, p_max_x, p_max_y)


def _draw_y_grid_and_ticks(
    chart: ScatterChart,
    y_axis: Axis,
    ticks: list[float],
    eff_min: float,
    eff_max: float,
    p_min_x: float,
    p_min_y: float,
    p_max_x: float,
    plot_h: float,
) -> None:
    """Render horizontal gridlines and numeric tick labels along Y axis."""
    grid_style = y_axis.grid_style or chart.grid_style
    tick_label_style = y_axis.tick_label_style or chart.axis_text_style
    if tick_label_style is not None:
        tick_label_style = tick_label_style.patch(
            text_halign="right",
            text_valign="center",
            angle=y_axis.tick_label_angle,
        )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, y_axis.scale)
        y = p_min_y + ratio * plot_h

        if y_axis.show_grid and grid_style is not None:
            canvas_line(xy1=(p_min_x, y), xy2=(p_max_x, y), style=ensure_line_style(grid_style))

        if y_axis.show_ticks and tick_label_style is not None:
            label_text = y_axis.format_value(tick)
            canvas_text(xy=(p_min_x - 1.5, y), text=label_text, style=ensure_text_style(tick_label_style))


def _draw_x_grid_and_ticks(
    chart: ScatterChart,
    x_axis: Axis,
    ticks: list[float],
    eff_min: float,
    eff_max: float,
    p_min_x: float,
    p_min_y: float,
    p_max_y: float,
    plot_w: float,
) -> None:
    """Render vertical gridlines and numeric tick labels along X axis."""
    grid_style = x_axis.grid_style or chart.grid_style
    tick_label_style = x_axis.tick_label_style or chart.axis_text_style
    if tick_label_style is not None:
        tick_label_style = tick_label_style.patch(
            text_halign="center",
            text_valign="top",
            angle=x_axis.tick_label_angle,
        )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, x_axis.scale)
        x = p_min_x + ratio * plot_w

        if x_axis.show_grid and grid_style is not None:
            canvas_line(xy1=(x, p_min_y), xy2=(x, p_max_y), style=ensure_line_style(grid_style))

        if x_axis.show_ticks and tick_label_style is not None:
            label_text = x_axis.format_value(tick)
            canvas_text(xy=(x, p_min_y - 1.5), text=label_text, style=ensure_text_style(tick_label_style))


def _draw_axes_lines(
    chart: ScatterChart,
    x_axis: Axis,
    y_axis: Axis,
    p_min_x: float,
    p_min_y: float,
    p_max_x: float,
    p_max_y: float,
) -> None:
    """Render solid baseline strokes for X and Y axes."""
    x_line_style = x_axis.line_style or chart.axis_line_style
    y_line_style = y_axis.line_style or chart.axis_line_style

    if x_axis.show_axis_line and x_line_style is not None:
        canvas_line(
            xy1=(p_min_x, p_min_y),
            xy2=(p_max_x, p_min_y),
            style=ensure_line_style(x_line_style),
        )

    if y_axis.show_axis_line and y_line_style is not None:
        canvas_line(
            xy1=(p_min_x, p_min_y),
            xy2=(p_min_x, p_max_y),
            style=ensure_line_style(y_line_style),
        )


def _draw_axis_titles(
    chart: ScatterChart,
    x_axis: Axis,
    y_axis: Axis,
    p_min_x: float,
    p_min_y: float,
    p_max_x: float,
    p_max_y: float,
) -> None:
    """Render descriptive labels for X and Y axes."""
    x_label_style = x_axis.label_style or chart.axis_text_style
    if x_axis.label and x_label_style is not None:
        x_cx = (p_min_x + p_max_x) / 2.0
        x_cy = p_min_y - 5.5
        x_style = x_label_style.patch(text_halign="center", text_valign="center")
        canvas_text(xy=(x_cx, x_cy), text=x_axis.label, style=ensure_text_style(x_style))

    y_label_style = y_axis.label_style or chart.axis_text_style
    if y_axis.label and y_label_style is not None:
        y_cx = p_min_x - 9.0
        y_cy = (p_min_y + p_max_y) / 2.0
        y_style = y_label_style.patch(text_halign="center", text_valign="center")
        canvas_text(xy=(y_cx, y_cy), text=y_axis.label, angle=90.0, style=ensure_text_style(y_style))


def _draw_point_marker(
    cx: float,
    cy: float,
    radius: float,
    shape: PointShape,
    style: Style,
) -> None:
    """Render a single point marker on canvas."""
    safe_style = ensure_shape_style(style)
    if shape == "circle":
        canvas_circle(xy=(cx, cy), radius=radius, style=safe_style)
    elif shape == "square":
        d = radius * 2.0
        canvas_rectangle(xy=(cx, cy), width=d, height=d, style=safe_style)
    elif shape == "rhombus":
        d = radius * 2.2
        canvas_rhombus(xy=(cx, cy), width=d, height=d, style=safe_style)
    elif shape == "triangle":
        canvas_triangle(xy=(cx, cy), width=radius * 2.2, height=radius * 2.0, style=safe_style)
    else:
        canvas_circle(xy=(cx, cy), radius=radius, style=safe_style)


def _collect_all_points(
    chart: ScatterChart,
) -> list[tuple[Point, Style, PointShape, float, str]]:
    """Gather all points for plotting with their effective (show, draw_ratio, draw_direction) metadata."""
    all_points: list[tuple[Point, Style, PointShape, float, str]] = []

    # Standalone points
    for pt in chart.points:
        ratio = 1.0 if pt.show else 0.0
        all_points.append((pt, pt.style, pt.shape, ratio, "left_to_right"))

    # Series points
    for s in chart.series:
        s_ratio = clamp_ratio(s.draw_ratio) if s.show else 0.0
        for pt in s.points:
            pt_style = s.style.patch(pt.style)
            eff_ratio = s_ratio if pt.show else 0.0
            all_points.append((pt, pt_style, pt.shape or s.shape, eff_ratio, s.draw_direction))

    return all_points


def _draw_points_and_labels(
    chart: ScatterChart,
    all_points: list[tuple[Point, Style, PointShape, float, str]],
    eff_min_x: float,
    eff_max_x: float,
    eff_min_y: float,
    eff_max_y: float,
    x_axis: Axis,
    y_axis: Axis,
    p_min_x: float,
    p_min_y: float,
    plot_w: float,
    plot_h: float,
) -> None:
    """Render scatter markers and optional text labels on the canvas."""
    for pt, pt_style, shape, dr, direction in all_points:
        if dr <= 0.0:
            continue

        ratio_x = value_to_ratio(pt.xy[0], eff_min_x, eff_max_x, x_axis.scale)
        ratio_y = value_to_ratio(pt.xy[1], eff_min_y, eff_max_y, y_axis.scale)

        if dr < 1.0:
            if direction == "bottom_to_top" and ratio_y > dr + 1e-6:
                continue
            if direction == "left_to_right" and ratio_x > dr + 1e-6:
                continue

        cx = p_min_x + ratio_x * plot_w
        cy = p_min_y + ratio_y * plot_h

        _draw_point_marker(cx, cy, pt.radius, shape, pt_style)

        if pt.label:
            l_style = pt.label_style or chart.value_text_style
            if l_style is not None:
                l_style = l_style.patch(text_halign="left", text_valign="center")
                canvas_text(xy=(cx + pt.radius + 0.8, cy), text=pt.label, style=ensure_text_style(l_style))


def render_scatter_chart(chart: ScatterChart, xy: tuple[float, float]) -> None:
    """Render a complete ScatterChart onto the canvas."""
    chart_w, chart_h = chart.get_size()
    bx, by = float(xy[0]), float(xy[1])

    if chart.background_style is not None:
        canvas_rectangle(
            xy=(bx + chart_w / 2.0, by + chart_h / 2.0),
            width=chart_w,
            height=chart_h,
            style=ensure_shape_style(chart.background_style),
        )

    all_points = _collect_all_points(chart)

    all_xs = [pt.xy[0] for pt, _, _, _, _ in all_points]
    all_ys = [pt.xy[1] for pt, _, _, _, _ in all_points]

    data_min_x = min(all_xs) if all_xs else 0.0
    data_max_x = max(all_xs) if all_xs else 10.0
    data_min_y = min(all_ys) if all_ys else 0.0
    data_max_y = max(all_ys) if all_ys else 10.0

    if data_min_x == data_max_x:
        data_min_x -= 1.0
        data_max_x += 1.0
    if data_min_y == data_max_y:
        data_min_y -= 1.0
        data_max_y += 1.0

    eff_min_x, eff_max_x, x_ticks = calculate_axis_range_and_ticks(chart.x_axis, data_min_x, data_max_x, is_bar=False)
    eff_min_y, eff_max_y, y_ticks = calculate_axis_range_and_ticks(chart.y_axis, data_min_y, data_max_y, is_bar=False)

    has_title = bool(chart.title and chart.title_style is not None)
    has_axis_text = (
        chart.axis_text_style is not None
        or chart.x_axis.tick_label_style is not None
        or chart.y_axis.tick_label_style is not None
    )
    p_min_x, p_min_y, p_max_x, p_max_y = _calculate_plot_bounds(
        chart_xy=xy,
        chart_w=chart_w,
        chart_h=chart_h,
        has_title=has_title,
        has_axis_text=has_axis_text,
        has_x_label=bool(chart.x_axis.label),
        has_y_label=bool(chart.y_axis.label),
    )
    plot_w = p_max_x - p_min_x
    plot_h = p_max_y - p_min_y

    if chart.title and chart.title_style is not None:
        title_y = by + chart_h - 2.5
        t_style = chart.title_style.patch(text_halign="center", text_valign="center")
        canvas_text(xy=(bx + chart_w / 2.0, title_y), text=chart.title, style=ensure_text_style(t_style))

    _draw_y_grid_and_ticks(chart, chart.y_axis, y_ticks, eff_min_y, eff_max_y, p_min_x, p_min_y, p_max_x, plot_h)
    _draw_x_grid_and_ticks(chart, chart.x_axis, x_ticks, eff_min_x, eff_max_x, p_min_x, p_min_y, p_max_y, plot_w)
    _draw_axes_lines(chart, chart.x_axis, chart.y_axis, p_min_x, p_min_y, p_max_x, p_max_y)
    _draw_axis_titles(chart, chart.x_axis, chart.y_axis, p_min_x, p_min_y, p_max_x, p_max_y)

    _draw_points_and_labels(
        chart,
        all_points,
        eff_min_x,
        eff_max_x,
        eff_min_y,
        eff_max_y,
        chart.x_axis,
        chart.y_axis,
        p_min_x,
        p_min_y,
        plot_w,
        plot_h,
    )
