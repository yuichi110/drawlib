# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for LineChart and AreaChart."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._style_utils import (
    clamp_ratio,
    ensure_line_style,
    ensure_shape_style,
    ensure_text_style,
    resolve_series_color,
    with_alpha,
)
from drawlib._charts._common._types import ColorType
from drawlib._charts.area_chart._series import Series as AreaSeries
from drawlib._charts.line_chart._series import Series as LineSeries
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import lines_curved as canvas_lines_curved
from drawlib._core.l4_canvas import polygon as canvas_polygon
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    from drawlib._charts.area_chart._chart import AreaChart
    from drawlib._charts.line_chart._base import CartesianChartBase
    from drawlib._charts.line_chart._line import LineChart


def _build_series_stroke_style(s: LineSeries | AreaSeries, color: ColorType) -> Style:
    """Build normalized stroke Style for a line or area series."""
    stroke_style = s.style
    if stroke_style.line_color is None or stroke_style.line_width is None:
        default_stroke_style = Style(
            line_color=color,
            line_width=s.line_width,
            line_style=s.line_style,
        )
        stroke_style = default_stroke_style.patch(s.style)
    return ensure_line_style(stroke_style)


def _build_area_fill_style(chart: AreaChart, s: AreaSeries, color: ColorType) -> Style:
    """Build polygon fill Style for an area series."""
    alpha = s.fill_alpha if s.fill_alpha is not None else chart.fill_alpha
    fill_color = s.style.shape_fill_color or with_alpha(color, alpha)
    return Style(
        shape_fill_color=fill_color,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
    )


def _clip_polyline_left_to_right(
    pts: list[tuple[float, float]],
    draw_ratio: float,
) -> tuple[list[tuple[float, float]], int]:
    """Clip polyline vertices horizontally according to draw_ratio in [0.0, 1.0]."""
    m = len(pts)
    if m == 0 or draw_ratio <= 0.0:
        return ([], 0)
    if draw_ratio >= 1.0 or m == 1:
        return (list(pts), m)

    pos = draw_ratio * (m - 1)
    k = int(math.floor(pos))
    frac = pos - k
    clipped = list(pts[: k + 1])
    reached_count = k + 1
    if k < m - 1 and frac > 1e-6:
        x0, y0 = pts[k]
        x1, y1 = pts[k + 1]
        clipped.append((x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac))
    return (clipped, reached_count)


def _calculate_plot_bounds(
    chart_xy: tuple[float, float],
    chart_w: float,
    chart_h: float,
    has_title: bool,
    has_axis_text: bool,
) -> tuple[float, float, float, float]:
    """Calculate internal plot area bounds."""
    c_min_x, c_min_y = chart_xy
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    pad_left = 10.0 if has_axis_text else 3.0
    pad_right = 3.0
    pad_bottom = 6.0 if has_axis_text else 3.0
    pad_top = 4.0 + (5.0 if has_title else 0.0)

    p_min_x = c_min_x + pad_left
    p_max_x = c_max_x - pad_right
    p_min_y = c_min_y + pad_bottom
    p_max_y = c_max_y - pad_top
    return (p_min_x, p_min_y, p_max_x, p_max_y)


def _draw_grid_and_ticks(
    chart: CartesianChartBase,
    val_axis: Axis,
    ticks: list[float],
    eff_min: float,
    eff_max: float,
    p_min_x: float,
    p_min_y: float,
    p_max_x: float,
    plot_h: float,
) -> None:
    """Render horizontal gridlines and numeric tick labels along Y axis."""
    grid_style = val_axis.grid_style or chart.grid_style
    tick_label_style = val_axis.tick_label_style or chart.axis_text_style
    if tick_label_style is not None:
        tick_label_style = ensure_text_style(
            tick_label_style.patch(angle=val_axis.tick_label_angle),
            halign="right",
            valign="center",
        )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, val_axis.scale)
        tick_y = p_min_y + ratio * plot_h

        if val_axis.show_grid and grid_style is not None and 0.001 < ratio < 0.999:
            canvas_line(xy1=(p_min_x, tick_y), xy2=(p_max_x, tick_y), style=ensure_line_style(grid_style))

        if val_axis.show_ticks and tick_label_style is not None:
            formatted_tick = val_axis.format_value(tick)
            canvas_text(xy=(p_min_x - 1.2, tick_y), text=formatted_tick, style=tick_label_style)


def _draw_category_labels(
    chart: CartesianChartBase,
    p_min_x: float,
    p_min_y: float,
    slot_w: float,
) -> None:
    """Render category labels below the X baseline."""
    cat_axis = chart.x_axis
    cat_label_style = cat_axis.tick_label_style or chart.axis_text_style
    if cat_label_style is None:
        return
    cat_label_style = ensure_text_style(
        cat_label_style.patch(angle=cat_axis.tick_label_angle),
        halign="center",
        valign="top",
    )
    for c_idx, cat in enumerate(chart.categories):
        cat_cx = p_min_x + (c_idx + 0.5) * slot_w
        canvas_text(xy=(cat_cx, p_min_y - 1.8), text=cat, style=cat_label_style)


def _prepare_cartesian_frame(
    chart: LineChart | AreaChart,
    xy: tuple[float, float],
    data_min: float,
    data_max: float,
    *,
    is_bar: bool,
    clamp_base_at_zero: bool,
) -> tuple[float, float, float, float, float, float, float, float, list[ColorType]]:
    """Render background, title, grid, baseline, and category labels, returning plot geometry."""
    c_min_x, c_min_y = float(xy[0]), float(xy[1])
    c_max_x = c_min_x + chart.width
    c_max_y = c_min_y + chart.height

    if chart.background_style is not None:
        canvas_rectangle(
            xy=((c_min_x + c_max_x) / 2.0, (c_min_y + c_max_y) / 2.0),
            width=chart.width,
            height=chart.height,
            style=ensure_shape_style(chart.background_style),
        )

    has_title = bool(chart.title and chart.title_style is not None)
    if chart.title and chart.title_style is not None:
        t_style = ensure_text_style(chart.title_style, halign="center", valign="bottom")
        canvas_text(xy=((c_min_x + c_max_x) / 2.0, c_max_y - 3.5), text=chart.title, style=t_style)

    has_axis_text = (
        chart.axis_text_style is not None
        or chart.x_axis.tick_label_style is not None
        or chart.y_axis.tick_label_style is not None
    )
    p_min_x, p_min_y, p_max_x, p_max_y = _calculate_plot_bounds(
        xy, chart.width, chart.height, has_title=has_title, has_axis_text=has_axis_text
    )
    plot_w = p_max_x - p_min_x
    plot_h = p_max_y - p_min_y

    series_colors = [resolve_series_color(s.style) for s in chart.series]

    val_axis = chart.y_axis
    eff_min, eff_max, ticks = calculate_axis_range_and_ticks(val_axis, data_min, data_max, is_bar=is_bar)
    _draw_grid_and_ticks(chart, val_axis, ticks, eff_min, eff_max, p_min_x, p_min_y, p_max_x, plot_h)

    if val_axis.scale == "log":
        base_val = eff_min
    else:
        base_val = max(0.0, eff_min) if clamp_base_at_zero else 0.0
    base_ratio = value_to_ratio(base_val, eff_min, eff_max, val_axis.scale)
    base_y = p_min_y + base_ratio * plot_h

    axis_line_style = val_axis.line_style or chart.axis_line_style
    if val_axis.show_axis_line and axis_line_style is not None:
        canvas_line(xy1=(p_min_x, base_y), xy2=(p_max_x, base_y), style=ensure_line_style(axis_line_style))

    num_cats = len(chart.categories)
    slot_w = plot_w / max(1, num_cats)
    _draw_category_labels(chart, p_min_x, p_min_y, slot_w)

    return p_min_x, p_min_y, plot_h, slot_w, eff_min, eff_max, base_val, base_y, series_colors


def _render_markers_and_labels(
    pts: list[tuple[float, float]],
    values: list[float],
    point_shape: str,
    point_size: float,
    color: ColorType,
    val_axis: Axis,
    val_label_style: Style | None,
) -> None:
    """Render markers and numeric value labels at points."""
    marker_style = Style(
        shape_fill_color=(255, 255, 255, 1.0),
        shape_line_color=color,
        shape_line_width=1.2,
    )
    for (px, py), v in zip(pts, values, strict=False):
        if point_shape == "circle":
            canvas_circle(xy=(px, py), radius=point_size, style=marker_style)
        elif point_shape == "square":
            side = point_size * 1.6
            canvas_rectangle(xy=(px, py), width=side, height=side, style=marker_style)

        if val_label_style is not None:
            lbl = val_axis.format_value(v)
            v_style = ensure_text_style(val_label_style, halign="center", valign="bottom")
            canvas_text(xy=(px, py + point_size + 1.4), text=lbl, style=v_style)


def _draw_single_line_series(
    chart: LineChart,
    s: LineSeries,
    color: ColorType,
    num_cats: int,
    slot_w: float,
    plot_h: float,
    p_min_x: float,
    p_min_y: float,
    base_y: float,
    eff_min: float,
    eff_max: float,
    val_axis: Axis,
) -> None:
    """Render a single series polyline, markers, and value labels."""
    if not s.show:
        return
    dr = clamp_ratio(s.draw_ratio)
    if dr <= 0.0:
        return

    pts: list[tuple[float, float]] = []
    for c_idx in range(min(num_cats, len(s.values))):
        v = s.values[c_idx]
        ratio = value_to_ratio(v, eff_min, eff_max, val_axis.scale)
        px = p_min_x + (c_idx + 0.5) * slot_w
        full_py = p_min_y + ratio * plot_h
        py = base_y + (full_py - base_y) * dr if s.draw_direction == "bottom_to_top" else full_py
        pts.append((px, py))

    if s.draw_direction == "left_to_right" and dr < 1.0:
        line_pts, reached_count = _clip_polyline_left_to_right(pts, dr)
        marker_pts = pts[:reached_count]
        marker_vals = s.values[:reached_count]
    else:
        line_pts = pts
        marker_pts = pts
        marker_vals = s.values[: len(pts)]

    stroke_style = _build_series_stroke_style(s, color)

    if len(line_pts) >= 2:
        if chart.smooth and len(line_pts) >= 3:
            canvas_lines_curved(xys=line_pts, r=slot_w * 0.4, style=stroke_style)
        else:
            canvas_lines(xys=line_pts, style=stroke_style)

    if chart.show_points and s.point_shape != "none":
        _render_markers_and_labels(
            pts=marker_pts,
            values=marker_vals,
            point_shape=s.point_shape,
            point_size=s.point_size,
            color=color,
            val_axis=val_axis,
            val_label_style=chart.value_text_style,
        )


def draw_line_chart(chart: LineChart, xy: tuple[float, float]) -> None:
    """Render a complete LineChart onto the canvas."""
    all_vals = [v for s in chart.series for v in s.values]
    data_min = min(all_vals) if all_vals else 0.0
    data_max = max(all_vals) if all_vals else 10.0

    (
        p_min_x,
        p_min_y,
        plot_h,
        slot_w,
        eff_min,
        eff_max,
        _,
        base_y,
        series_colors,
    ) = _prepare_cartesian_frame(
        chart,
        xy,
        data_min,
        data_max,
        is_bar=False,
        clamp_base_at_zero=True,
    )

    num_cats = len(chart.categories)
    val_axis = chart.y_axis
    for s_idx, s in enumerate(chart.series):
        if not s.values or num_cats == 0:
            continue
        _draw_single_line_series(
            chart,
            s,
            series_colors[s_idx],
            num_cats,
            slot_w,
            plot_h,
            p_min_x,
            p_min_y,
            base_y,
            eff_min,
            eff_max,
            val_axis,
        )


def draw_area_chart(chart: AreaChart, xy: tuple[float, float]) -> None:
    """Render a complete AreaChart onto the canvas."""
    num_cats = len(chart.categories)
    data_min = 0.0
    data_max = 10.0

    if chart.mode == "stack":
        for c_idx in range(num_cats):
            c_sum = sum(s.values[c_idx] for s in chart.series if c_idx < len(s.values))
            data_max = max(data_max, c_sum)
    else:
        all_vals = [v for s in chart.series for v in s.values]
        if all_vals:
            data_min = min(0.0, *all_vals)
            data_max = max(all_vals)

    (
        p_min_x,
        p_min_y,
        plot_h,
        slot_w,
        eff_min,
        eff_max,
        base_val,
        base_y,
        series_colors,
    ) = _prepare_cartesian_frame(
        chart,
        xy,
        data_min,
        data_max,
        is_bar=True,
        clamp_base_at_zero=False,
    )

    val_label_style = chart.value_text_style

    if chart.mode == "stack":
        _draw_stacked_areas(
            chart=chart,
            p_min_x=p_min_x,
            p_min_y=p_min_y,
            plot_h=plot_h,
            slot_w=slot_w,
            num_cats=num_cats,
            eff_min=eff_min,
            eff_max=eff_max,
            base_val=base_val,
            series_colors=series_colors,
            val_label_style=val_label_style,
        )
    else:
        _draw_overlap_areas(
            chart=chart,
            p_min_x=p_min_x,
            p_min_y=p_min_y,
            plot_h=plot_h,
            slot_w=slot_w,
            num_cats=num_cats,
            eff_min=eff_min,
            eff_max=eff_max,
            base_y=base_y,
            series_colors=series_colors,
            val_label_style=val_label_style,
        )


def _draw_overlap_areas(
    chart: AreaChart,
    p_min_x: float,
    p_min_y: float,
    plot_h: float,
    slot_w: float,
    num_cats: int,
    eff_min: float,
    eff_max: float,
    base_y: float,
    series_colors: list[ColorType],
    val_label_style: Style | None,
) -> None:
    """Render overlapping semi-transparent area polygons."""
    val_axis = chart.y_axis

    for s_idx, s in enumerate(chart.series):
        if not s.values or num_cats == 0 or not s.show:
            continue

        dr = clamp_ratio(s.draw_ratio)
        if dr <= 0.0:
            continue

        color = series_colors[s_idx]
        pts: list[tuple[float, float]] = []
        for c_idx in range(min(num_cats, len(s.values))):
            v = s.values[c_idx]
            ratio = value_to_ratio(v, eff_min, eff_max, val_axis.scale)
            px = p_min_x + (c_idx + 0.5) * slot_w
            full_py = p_min_y + ratio * plot_h
            py = base_y + (full_py - base_y) * dr if s.draw_direction == "bottom_to_top" else full_py
            pts.append((px, py))

        if s.draw_direction == "left_to_right" and dr < 1.0:
            line_pts, reached_count = _clip_polyline_left_to_right(pts, dr)
            marker_pts = pts[:reached_count]
            marker_vals = s.values[:reached_count]
        else:
            line_pts = pts
            marker_pts = pts
            marker_vals = s.values[: len(pts)]

        if len(line_pts) >= 2:
            poly_pts = [(line_pts[0][0], base_y)] + line_pts + [(line_pts[-1][0], base_y)]
            canvas_polygon(xys=poly_pts, style=_build_area_fill_style(chart, s, color))
            canvas_lines(xys=line_pts, style=_build_series_stroke_style(s, color))

        if chart.show_points and s.point_shape != "none":
            _render_markers_and_labels(
                pts=marker_pts,
                values=marker_vals,
                point_shape=s.point_shape,
                point_size=s.point_size,
                color=color,
                val_axis=val_axis,
                val_label_style=val_label_style,
            )


def _draw_stacked_areas(
    chart: AreaChart,
    p_min_x: float,
    p_min_y: float,
    plot_h: float,
    slot_w: float,
    num_cats: int,
    eff_min: float,
    eff_max: float,
    base_val: float,
    series_colors: list[ColorType],
    val_label_style: Style | None,
) -> None:
    """Render cumulative stacked area polygons."""
    val_axis = chart.y_axis
    accum_prev = [base_val] * num_cats

    for s_idx, s in enumerate(chart.series):
        if not s.values or num_cats == 0 or not s.show:
            continue

        dr = clamp_ratio(s.draw_ratio)
        if dr <= 0.0:
            continue

        color = series_colors[s_idx]
        accum_cur: list[float] = []
        pts_cur: list[tuple[float, float]] = []
        pts_prev: list[tuple[float, float]] = []

        v_scale = dr if s.draw_direction == "bottom_to_top" else 1.0
        for c_idx in range(num_cats):
            v = (s.values[c_idx] if c_idx < len(s.values) else 0.0) * v_scale
            prev_v = accum_prev[c_idx]
            cur_v = prev_v + v
            accum_cur.append(cur_v)

            px = p_min_x + (c_idx + 0.5) * slot_w
            py_prev = p_min_y + value_to_ratio(prev_v, eff_min, eff_max, val_axis.scale) * plot_h
            py_cur = p_min_y + value_to_ratio(cur_v, eff_min, eff_max, val_axis.scale) * plot_h

            pts_cur.append((px, py_cur))
            pts_prev.append((px, py_prev))

        if s.draw_direction == "left_to_right" and dr < 1.0:
            line_pts_cur, reached_count = _clip_polyline_left_to_right(pts_cur, dr)
            line_pts_prev, _ = _clip_polyline_left_to_right(pts_prev, dr)
            marker_pts = pts_cur[:reached_count]
            marker_vals = s.values[:reached_count]
        else:
            line_pts_cur = pts_cur
            line_pts_prev = pts_prev
            marker_pts = pts_cur
            marker_vals = s.values[: len(pts_cur)]

        if len(line_pts_cur) >= 2:
            # Closed polygon: upper curve forward, lower curve reversed
            poly_pts = line_pts_cur + list(reversed(line_pts_prev))
            canvas_polygon(xys=poly_pts, style=_build_area_fill_style(chart, s, color))
            canvas_lines(xys=line_pts_cur, style=_build_series_stroke_style(s, color))

        if chart.show_points and s.point_shape != "none":
            _render_markers_and_labels(
                pts=marker_pts,
                values=marker_vals,
                point_shape=s.point_shape,
                point_size=s.point_size,
                color=color,
                val_axis=val_axis,
                val_label_style=val_label_style,
            )

        accum_prev = accum_cur
