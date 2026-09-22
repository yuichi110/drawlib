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
from drawlib._charts._common._legend import get_legend_size, render_legend
from drawlib._charts._common._types import ColorType, LegendPosition, PointShape
from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._charts.scatter_chart._point import ScatterPoint, ScatterSeries
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.lines import line as canvas_line
from drawlib.shapes import circle as canvas_circle
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.shapes import rhombus as canvas_rhombus
from drawlib.shapes import triangle as canvas_triangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.scatter_chart._chart import ScatterChart

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)
_DEFAULT_MUTED_TEXT = (100, 116, 139, 1.0)
_DEFAULT_GRID_COLOR = (226, 232, 240, 1.0)
_DEFAULT_AXIS_COLOR = (148, 163, 184, 1.0)


def _with_alpha(color: ColorType, alpha: float) -> tuple[int, int, int, float]:
    """Return an RGBA color tuple replacing alpha with given ratio."""
    return (int(color[0]), int(color[1]), int(color[2]), float(alpha))


def _calculate_plot_bounds(
    chart_xy: tuple[float, float],
    chart_w: float,
    chart_h: float,
    title: str,
    x_title: str,
    y_title: str,
    legend_h: float,
    legend_w: float,
    legend_pos: LegendPosition,
) -> tuple[float, float, float, float]:
    """Calculate internal plot area bounds accounting for labels, ticks, and legend."""
    c_min_x, c_min_y = chart_xy
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    pad_left = 11.0 + (4.0 if y_title else 0.0)
    pad_bottom = 8.0 + (4.0 if x_title else 0.0)
    pad_right = 10.0
    pad_top = 4.0 + (5.0 if title else 0.0)

    if legend_pos in {"top", "auto"} and legend_h > 0:
        pad_top += legend_h + 2.0
    elif legend_pos == "bottom" and legend_h > 0:
        pad_bottom += legend_h + 2.0
    elif legend_pos == "right" and legend_w > 0:
        pad_right += legend_w + 2.0

    p_min_x = c_min_x + pad_left
    p_max_x = c_max_x - pad_right
    p_min_y = c_min_y + pad_bottom
    p_max_y = c_max_y - pad_top
    return (p_min_x, p_min_y, p_max_x, p_max_y)


def _draw_y_grid_and_ticks(
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
    grid_style = y_axis.grid_style or Style(
        line_color=_DEFAULT_GRID_COLOR,
        line_width=0.8,
        line_style="dashed",
    )
    tick_label_style = y_axis.tick_label_style or Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT,
        text_halign="right",
        text_valign="center",
    )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, y_axis.scale)
        y = p_min_y + ratio * plot_h

        if y_axis.show_grid:
            canvas_line(xy1=(p_min_x, y), xy2=(p_max_x, y), style=grid_style)

        if y_axis.show_ticks:
            label_text = y_axis.format_value(tick)
            canvas_text(xy=(p_min_x - 1.5, y), text=label_text, style=tick_label_style)


def _draw_x_grid_and_ticks(
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
    grid_style = x_axis.grid_style or Style(
        line_color=_DEFAULT_GRID_COLOR,
        line_width=0.8,
        line_style="dashed",
    )
    tick_label_style = x_axis.tick_label_style or Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT,
        text_halign="center",
        text_valign="top",
    )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, x_axis.scale)
        x = p_min_x + ratio * plot_w

        if x_axis.show_grid:
            canvas_line(xy1=(x, p_min_y), xy2=(x, p_max_y), style=grid_style)

        if x_axis.show_ticks:
            label_text = x_axis.format_value(tick)
            canvas_text(xy=(x, p_min_y - 1.5), text=label_text, style=tick_label_style)


def _draw_axes_lines(
    x_axis: Axis,
    y_axis: Axis,
    p_min_x: float,
    p_min_y: float,
    p_max_x: float,
    p_max_y: float,
) -> None:
    """Render solid baseline strokes for X and Y axes."""
    axis_stroke = Style(line_color=_DEFAULT_AXIS_COLOR, line_width=1.2)

    if x_axis.show_axis_line:
        canvas_line(
            xy1=(p_min_x, p_min_y),
            xy2=(p_max_x, p_min_y),
            style=x_axis.line_style or axis_stroke,
        )

    if y_axis.show_axis_line:
        canvas_line(
            xy1=(p_min_x, p_min_y),
            xy2=(p_min_x, p_max_y),
            style=y_axis.line_style or axis_stroke,
        )


def _draw_axis_titles(
    x_axis: Axis,
    y_axis: Axis,
    p_min_x: float,
    p_min_y: float,
    p_max_x: float,
    p_max_y: float,
) -> None:
    """Render descriptive labels for X and Y axes."""
    title_style = Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )

    if x_axis.label:
        x_cx = (p_min_x + p_max_x) / 2.0
        x_cy = p_min_y - 5.5
        canvas_text(xy=(x_cx, x_cy), text=x_axis.label, style=title_style)

    if y_axis.label:
        y_cx = p_min_x - 9.0
        y_cy = (p_min_y + p_max_y) / 2.0
        canvas_text(xy=(y_cx, y_cy), text=y_axis.label, angle=90.0, style=title_style)


def _draw_point_marker(
    cx: float,
    cy: float,
    radius: float,
    shape: PointShape,
    style: Style,
) -> None:
    """Render a single point marker on canvas."""
    if shape == "circle":
        canvas_circle(xy=(cx, cy), radius=radius, style=style)
    elif shape == "square":
        d = radius * 2.0
        canvas_rectangle(xy=(cx, cy), width=d, height=d, style=style)
    elif shape == "rhombus":
        d = radius * 2.2
        canvas_rhombus(xy=(cx, cy), width=d, height=d, style=style)
    elif shape == "triangle":
        canvas_triangle(xy=(cx, cy), width=radius * 2.2, height=radius * 2.0, style=style)
    else:
        canvas_circle(xy=(cx, cy), radius=radius, style=style)


def _collect_all_points(
    chart: ScatterChart,
) -> tuple[list[tuple[ScatterPoint, Style, PointShape]], list[ColorType]]:
    """Gather all points and series colors for plotting."""
    all_points: list[tuple[ScatterPoint, Style, PointShape]] = []
    series_colors: list[ColorType] = []

    # Standalone points
    for i, pt in enumerate(chart.points):
        p_style = pt.style or Style(
            fill_color=DEFAULT_CHART_PALETTE[i % len(DEFAULT_CHART_PALETTE)],
            line_color=(255, 255, 255, 0.9),
            line_width=0.8,
        )
        all_points.append((pt, p_style, pt.shape))

    # Series points
    for k, s in enumerate(chart.series):
        s_color = DEFAULT_CHART_PALETTE[(len(chart.points) + k) % len(DEFAULT_CHART_PALETTE)]
        series_colors.append(s_color)
        default_s_style = s.style or Style(
            fill_color=s_color,
            line_color=(255, 255, 255, 0.9),
            line_width=0.8,
        )
        for pt in s.points:
            pt_style = pt.style or default_s_style
            all_points.append((pt, pt_style, pt.shape or s.shape))

    return all_points, series_colors


def _draw_points_and_labels(
    all_points: list[tuple[ScatterPoint, Style, PointShape]],
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
    show_labels: bool,
) -> None:
    """Render scatter markers and optional text labels on the canvas."""
    for pt, pt_style, shape in all_points:
        ratio_x = value_to_ratio(pt.xy[0], eff_min_x, eff_max_x, x_axis.scale)
        ratio_y = value_to_ratio(pt.xy[1], eff_min_y, eff_max_y, y_axis.scale)

        cx = p_min_x + ratio_x * plot_w
        cy = p_min_y + ratio_y * plot_h

        _draw_point_marker(cx, cy, pt.radius, shape, pt_style)

        if show_labels and pt.label:
            l_style = pt.label_style or Style(
                text_size=8.5,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=_DEFAULT_TEXT_COLOR,
                text_halign="left",
                text_valign="center",
            )
            canvas_text(xy=(cx + pt.radius + 0.8, cy), text=pt.label, style=l_style)


def render_scatter_chart(chart: ScatterChart, xy: tuple[float, float]) -> None:
    """Render a complete ScatterChart onto the canvas."""
    chart_w, chart_h = chart.get_size()
    all_points, series_colors = _collect_all_points(chart)

    all_xs = [pt.xy[0] for pt, _, _ in all_points]
    all_ys = [pt.xy[1] for pt, _, _ in all_points]

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

    series_names = [s.name for s in chart.series]
    legend_w, legend_h = (0.0, 0.0)
    if series_names and chart.legend_position != "none":
        legend_w, legend_h = get_legend_size(chart.legend_position, series_names, len(series_names))

    p_min_x, p_min_y, p_max_x, p_max_y = _calculate_plot_bounds(
        chart_xy=xy,
        chart_w=chart_w,
        chart_h=chart_h,
        title=chart.title,
        x_title=chart.x_axis.label,
        y_title=chart.y_axis.label,
        legend_h=legend_h,
        legend_w=legend_w,
        legend_pos=chart.legend_position,
    )
    plot_w = p_max_x - p_min_x
    plot_h = p_max_y - p_min_y

    if chart.title:
        title_y = xy[1] + chart_h - 2.5
        t_style = chart.title_style or Style(
            text_size=12.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="center",
        )
        canvas_text(xy=((xy[0] + xy[0] + chart_w) / 2.0, title_y), text=chart.title, style=t_style)

    _draw_y_grid_and_ticks(chart.y_axis, y_ticks, eff_min_y, eff_max_y, p_min_x, p_min_y, p_max_x, plot_h)
    _draw_x_grid_and_ticks(chart.x_axis, x_ticks, eff_min_x, eff_max_x, p_min_x, p_min_y, p_max_y, plot_w)
    _draw_axes_lines(chart.x_axis, chart.y_axis, p_min_x, p_min_y, p_max_x, p_max_y)
    _draw_axis_titles(chart.x_axis, chart.y_axis, p_min_x, p_min_y, p_max_x, p_max_y)

    _draw_points_and_labels(
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
        chart.show_labels,
    )

    if series_names and chart.legend_position != "none":
        chart_bounds = (xy[0], xy[1], xy[0] + chart_w, xy[1] + chart_h)
        render_legend(
            names=series_names,
            colors=series_colors,
            position=chart.legend_position,
            plot_bounds=(p_min_x, p_min_y, p_max_x, p_max_y),
            chart_bounds=chart_bounds,
        )
