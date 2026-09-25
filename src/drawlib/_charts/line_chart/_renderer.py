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

from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._legend import get_legend_size, render_legend
from drawlib._charts._common._types import ColorType, LineStyle
from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._charts.line_chart._series import AreaSeries, LineSeries
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.colors import Colors
from drawlib.lines import line as canvas_line
from drawlib.lines import lines as canvas_lines
from drawlib.lines import lines_curved as canvas_lines_curved
from drawlib.shapes import circle as canvas_circle
from drawlib.shapes import polygon as canvas_polygon
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.line_chart._area import AreaChart
    from drawlib._charts.line_chart._line import LineChart

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)
_DEFAULT_MUTED_TEXT = (100, 116, 139, 1.0)
_DEFAULT_GRID_COLOR = (226, 232, 240, 1.0)
_DEFAULT_AXIS_COLOR = (148, 163, 184, 1.0)


def _with_alpha(color: ColorType, alpha: float) -> tuple[int, int, int, float]:
    """Return an RGBA color tuple replacing alpha with given ratio."""
    return (int(color[0]), int(color[1]), int(color[2]), float(alpha))


def _resolve_series_colors(series_list: list[LineSeries] | list[AreaSeries]) -> list[ColorType]:
    """Resolve fill/stroke colors for all series."""
    colors: list[ColorType] = []
    for i, s in enumerate(series_list):
        if s.color is not None:
            colors.append(s.color)
        else:
            colors.append(DEFAULT_CHART_PALETTE[i % len(DEFAULT_CHART_PALETTE)])
    return colors


def _calculate_plot_bounds(
    chart_xy: tuple[float, float],
    chart_w: float,
    chart_h: float,
    title: str,
    legend_h: float,
    legend_w: float,
) -> tuple[float, float, float, float]:
    """Calculate internal plot area bounds."""
    c_min_x, c_min_y = chart_xy
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    pad_left = 10.0
    pad_right = 5.0 + legend_w
    pad_bottom = 6.0
    pad_top = 4.0 + (5.0 if title else 0.0) + legend_h

    p_min_x = c_min_x + pad_left
    p_max_x = c_max_x - pad_right
    p_min_y = c_min_y + pad_bottom
    p_max_y = c_max_y - pad_top
    return (p_min_x, p_min_y, p_max_x, p_max_y)


def _draw_grid_and_ticks(
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
    default_grid_style = Style(
        line_color=_DEFAULT_GRID_COLOR,
        line_width=0.8,
        line_style="dashed",
    )
    grid_style = default_grid_style.patch(val_axis.grid_style)
    default_tick_label_style = Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT,
        text_halign="right",
        text_valign="center",
        text_angle=val_axis.tick_label_angle,
    )
    tick_label_style = default_tick_label_style.patch(val_axis.tick_label_style)

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, val_axis.scale)
        tick_y = p_min_y + ratio * plot_h

        if val_axis.show_grid and 0.001 < ratio < 0.999:
            canvas_line(xy1=(p_min_x, tick_y), xy2=(p_max_x, tick_y), style=grid_style)

        if val_axis.show_ticks:
            formatted_tick = val_axis.format_value(tick)
            canvas_text(xy=(p_min_x - 1.2, tick_y), text=formatted_tick, style=tick_label_style)


def _draw_category_labels(
    categories: list[str],
    cat_axis: Axis,
    p_min_x: float,
    p_min_y: float,
    slot_w: float,
) -> None:
    """Render category labels below the X baseline."""
    default_cat_label_style = Style(
        text_size=10.0,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="top",
        text_angle=cat_axis.tick_label_angle,
    )
    cat_label_style = default_cat_label_style.patch(cat_axis.tick_label_style)
    for c_idx, cat in enumerate(categories):
        cat_cx = p_min_x + (c_idx + 0.5) * slot_w
        canvas_text(xy=(cat_cx, p_min_y - 1.8), text=cat, style=cat_label_style)


def _render_markers_and_labels(
    pts: list[tuple[float, float]],
    values: list[float],
    point_shape: str,
    point_size: float,
    color: ColorType,
    val_axis: Axis,
    show_values: bool,
    val_label_style: Style,
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

        if show_values:
            lbl = val_axis.format_value(v)
            canvas_text(xy=(px, py + point_size + 1.4), text=lbl, style=val_label_style)


def draw_line_chart(chart: LineChart, xy: tuple[float, float]) -> None:
    """Render a complete LineChart onto the canvas."""
    c_min_x, c_min_y = xy
    c_max_x = c_min_x + chart.width
    c_max_y = c_min_y + chart.height

    series_names = [s.name for s in chart.series]
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

    plot_bounds = _calculate_plot_bounds(xy, chart.width, chart.height, chart.title, legend_h, legend_w)
    p_min_x, p_min_y, p_max_x, p_max_y = plot_bounds
    plot_w = p_max_x - p_min_x
    plot_h = p_max_y - p_min_y

    series_colors = _resolve_series_colors(chart.series)
    render_legend(
        names=series_names,
        colors=series_colors,
        position=chart.legend_position,
        plot_bounds=plot_bounds,
        chart_bounds=(c_min_x, c_min_y, c_max_x, c_max_y),
    )

    all_vals = [v for s in chart.series for v in s.values]
    data_min = min(all_vals) if all_vals else 0.0
    data_max = max(all_vals) if all_vals else 10.0
    val_axis = chart.y_axis

    eff_min, eff_max, ticks = calculate_axis_range_and_ticks(val_axis, data_min, data_max, is_bar=False)
    _draw_grid_and_ticks(val_axis, ticks, eff_min, eff_max, p_min_x, p_min_y, p_max_x, plot_h)

    base_val = eff_min if val_axis.scale == "log" else max(0.0, eff_min)
    base_ratio = value_to_ratio(base_val, eff_min, eff_max, val_axis.scale)
    base_y = p_min_y + base_ratio * plot_h
    if val_axis.show_axis_line:
        default_axis_stroke = Style(line_color=_DEFAULT_AXIS_COLOR, line_width=1.2)
        axis_line_style = default_axis_stroke.patch(val_axis.line_style)
        canvas_line(xy1=(p_min_x, base_y), xy2=(p_max_x, base_y), style=axis_line_style)

    num_cats = len(chart.categories)
    slot_w = plot_w / max(1, num_cats)
    _draw_category_labels(chart.categories, chart.x_axis, p_min_x, p_min_y, slot_w)

    default_val_label_style = Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="bottom",
    )
    val_label_style = default_val_label_style.patch(chart.value_label_style)

    for s_idx, s in enumerate(chart.series):
        if not s.values or num_cats == 0:
            continue

        color = series_colors[s_idx]
        pts: list[tuple[float, float]] = []
        for c_idx in range(min(num_cats, len(s.values))):
            v = s.values[c_idx]
            ratio = value_to_ratio(v, eff_min, eff_max, val_axis.scale)
            px = p_min_x + (c_idx + 0.5) * slot_w
            py = p_min_y + ratio * plot_h
            pts.append((px, py))

        default_stroke_style = Style(
            line_color=color,
            line_width=s.line_width,
            line_style=s.line_style,
        )
        stroke_style = default_stroke_style.patch(s.style)

        if len(pts) >= 2:
            if chart.smooth and len(pts) >= 3:
                canvas_lines_curved(xys=pts, r=slot_w * 0.4, style=stroke_style)
            else:
                canvas_lines(xys=pts, style=stroke_style)

        if chart.show_points and s.point_shape != "none":
            _render_markers_and_labels(
                pts=pts,
                values=s.values[: len(pts)],
                point_shape=s.point_shape,
                point_size=s.point_size,
                color=color,
                val_axis=val_axis,
                show_values=chart.show_values,
                val_label_style=val_label_style,
            )


def draw_area_chart(chart: AreaChart, xy: tuple[float, float]) -> None:
    """Render a complete AreaChart onto the canvas."""
    c_min_x, c_min_y = xy
    c_max_x = c_min_x + chart.width
    c_max_y = c_min_y + chart.height

    series_names = [s.name for s in chart.series]
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

    plot_bounds = _calculate_plot_bounds(xy, chart.width, chart.height, chart.title, legend_h, legend_w)
    p_min_x, p_min_y, p_max_x, p_max_y = plot_bounds
    plot_w = p_max_x - p_min_x
    plot_h = p_max_y - p_min_y

    series_colors = _resolve_series_colors(chart.series)
    render_legend(
        names=series_names,
        colors=series_colors,
        position=chart.legend_position,
        plot_bounds=plot_bounds,
        chart_bounds=(c_min_x, c_min_y, c_max_x, c_max_y),
    )

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

    val_axis = chart.y_axis
    eff_min, eff_max, ticks = calculate_axis_range_and_ticks(val_axis, data_min, data_max, is_bar=True)
    _draw_grid_and_ticks(val_axis, ticks, eff_min, eff_max, p_min_x, p_min_y, p_max_x, plot_h)

    base_val = eff_min if val_axis.scale == "log" else 0.0
    base_ratio = value_to_ratio(base_val, eff_min, eff_max, val_axis.scale)
    base_y = p_min_y + base_ratio * plot_h
    if val_axis.show_axis_line:
        default_axis_stroke = Style(line_color=_DEFAULT_AXIS_COLOR, line_width=1.2)
        axis_line_style = default_axis_stroke.patch(val_axis.line_style)
        canvas_line(xy1=(p_min_x, base_y), xy2=(p_max_x, base_y), style=axis_line_style)

    slot_w = plot_w / max(1, num_cats)
    _draw_category_labels(chart.categories, chart.x_axis, p_min_x, p_min_y, slot_w)

    default_val_label_style = Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="bottom",
    )
    val_label_style = default_val_label_style.patch(chart.value_label_style)

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
    val_label_style: Style,
) -> None:
    """Render overlapping semi-transparent area polygons."""
    val_axis = chart.y_axis

    for s_idx, s in enumerate(chart.series):
        if not s.values or num_cats == 0:
            continue

        color = series_colors[s_idx]
        pts: list[tuple[float, float]] = []
        for c_idx in range(min(num_cats, len(s.values))):
            v = s.values[c_idx]
            ratio = value_to_ratio(v, eff_min, eff_max, val_axis.scale)
            px = p_min_x + (c_idx + 0.5) * slot_w
            py = p_min_y + ratio * plot_h
            pts.append((px, py))

        if len(pts) >= 2:
            poly_pts = [(pts[0][0], base_y)] + pts + [(pts[-1][0], base_y)]
            fill_style = Style(
                shape_fill_color=_with_alpha(color, s.fill_alpha),
                shape_line_color=Colors.Transparent,
                shape_line_width=0,
            )
            canvas_polygon(xys=poly_pts, style=fill_style)

            default_stroke_style = Style(
                line_color=color,
                line_width=s.line_width,
                line_style=s.line_style,
            )
            stroke_style = default_stroke_style.patch(s.style)
            canvas_lines(xys=pts, style=stroke_style)

        if chart.show_points and s.point_shape != "none":
            _render_markers_and_labels(
                pts=pts,
                values=s.values[: len(pts)],
                point_shape=s.point_shape,
                point_size=s.point_size,
                color=color,
                val_axis=val_axis,
                show_values=chart.show_values,
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
    val_label_style: Style,
) -> None:
    """Render cumulative stacked area polygons."""
    val_axis = chart.y_axis
    accum_prev = [base_val] * num_cats

    for s_idx, s in enumerate(chart.series):
        if not s.values or num_cats == 0:
            continue

        color = series_colors[s_idx]
        accum_cur: list[float] = []
        pts_cur: list[tuple[float, float]] = []
        pts_prev: list[tuple[float, float]] = []

        for c_idx in range(num_cats):
            v = s.values[c_idx] if c_idx < len(s.values) else 0.0
            prev_v = accum_prev[c_idx]
            cur_v = prev_v + v
            accum_cur.append(cur_v)

            px = p_min_x + (c_idx + 0.5) * slot_w
            py_prev = p_min_y + value_to_ratio(prev_v, eff_min, eff_max, val_axis.scale) * plot_h
            py_cur = p_min_y + value_to_ratio(cur_v, eff_min, eff_max, val_axis.scale) * plot_h

            pts_cur.append((px, py_cur))
            pts_prev.append((px, py_prev))

        # Closed polygon: upper curve forward, lower curve reversed
        poly_pts = pts_cur + list(reversed(pts_prev))
        fill_style = Style(
            shape_fill_color=_with_alpha(color, s.fill_alpha),
            shape_line_color=Colors.Transparent,
            shape_line_width=0,
        )
        canvas_polygon(xys=poly_pts, style=fill_style)

        default_stroke_style = Style(
            line_color=color,
            line_width=s.line_width,
            line_style=s.line_style,
        )
        stroke_style = default_stroke_style.patch(s.style)
        canvas_lines(xys=pts_cur, style=stroke_style)

        if chart.show_points and s.point_shape != "none":
            _render_markers_and_labels(
                pts=pts_cur,
                values=s.values[: len(pts_cur)],
                point_shape=s.point_shape,
                point_size=s.point_size,
                color=color,
                val_axis=val_axis,
                show_values=chart.show_values,
                val_label_style=val_label_style,
            )

        accum_prev = accum_cur
