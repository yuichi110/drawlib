# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for vertical and horizontal bar charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._legend import get_legend_size, render_legend
from drawlib._charts._common._types import ColorType
from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.lines import line as canvas_line
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.bar_chart._chart import BarChart

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)  # Slate-800
_DEFAULT_MUTED_TEXT = (100, 116, 139, 1.0)  # Slate-500
_DEFAULT_GRID_COLOR = (226, 232, 240, 1.0)  # Slate-200
_DEFAULT_AXIS_COLOR = (148, 163, 184, 1.0)  # Slate-400


def draw_bar_chart(chart: BarChart, xy: tuple[float, float]) -> None:
    """Render a complete bar chart onto the canvas.

    Args:
        chart: BarChart container instance.
        xy: Base canvas coordinate (x, y) corresponding to bottom-left corner.
    """
    bx, by = float(xy[0]), float(xy[1])
    cw, ch = chart.width, chart.height

    # 1. Layer 0: Background card
    if chart.style is not None:
        canvas_rectangle(
            xy=(bx + cw / 2.0, by + ch / 2.0),
            width=cw,
            height=ch,
            style=chart.style,
        )

    # 2. Title
    title_h = 0.0
    if chart.title:
        title_h = 4.5
        title_style = Style(
            text_size=13.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="center",
        )
        if chart.title_style is not None:
            title_style = title_style.merge(chart.title_style)

        title_y = by + ch - 2.5
        canvas_text(xy=(bx + cw / 2.0, title_y), text=chart.title, style=title_style)

    # 3. Resolve series colors
    series_names = [s.name for s in chart.series]
    series_colors = [
        s.color if s.color is not None else DEFAULT_CHART_PALETTE[i % len(DEFAULT_CHART_PALETTE)]
        for i, s in enumerate(chart.series)
    ]

    # 4. Legend size & Margins
    leg_w, leg_h = get_legend_size(chart.legend_position, series_names, len(chart.series))

    if chart.orientation == "vertical":
        margin_left = 8.5
        margin_bottom = 5.0
        margin_right = 3.0 + leg_w
        margin_top = (title_h if chart.title else 2.5) + leg_h
    else:
        margin_left = 12.5
        margin_bottom = 5.5
        margin_right = 3.0 + leg_w
        margin_top = (title_h if chart.title else 2.5) + leg_h

    plot_min_x = bx + margin_left
    plot_max_x = bx + cw - margin_right
    plot_min_y = by + margin_bottom
    plot_max_y = by + ch - margin_top
    plot_w = max(1.0, plot_max_x - plot_min_x)
    plot_h = max(1.0, plot_max_y - plot_min_y)

    plot_bounds = (plot_min_x, plot_min_y, plot_max_x, plot_max_y)
    chart_bounds = (bx, by, bx + cw, by + ch)

    # 5. Render Legend
    render_legend(
        names=series_names,
        colors=series_colors,
        position=chart.legend_position,
        plot_bounds=plot_bounds,
        chart_bounds=chart_bounds,
        textstyle=chart.legend_style,
    )

    # 6. Gather and scale data
    val_axis = chart.value_axis

    data_min = 0.0
    data_max = 0.0
    num_cats = len(chart.categories)

    if chart.series:
        if chart.bar_mode == "stack":
            for c_idx in range(num_cats):
                c_sum = sum(s.values[c_idx] for s in chart.series if c_idx < len(s.values))
                data_max = max(data_max, c_sum)
        else:
            all_vals = [v for s in chart.series for v in s.values]
            if all_vals:
                data_min = min(all_vals)
                data_max = max(all_vals)

    eff_min, eff_max, ticks = calculate_axis_range_and_ticks(val_axis, data_min, data_max, is_bar=True)

    # 7. Render Plot Area based on orientation
    if chart.orientation == "vertical":
        _render_vertical_bars(
            chart=chart,
            plot_bounds=plot_bounds,
            plot_w=plot_w,
            plot_h=plot_h,
            eff_min=eff_min,
            eff_max=eff_max,
            ticks=ticks,
            series_colors=series_colors,
        )
    else:
        _render_horizontal_bars(
            chart=chart,
            plot_bounds=plot_bounds,
            plot_w=plot_w,
            plot_h=plot_h,
            eff_min=eff_min,
            eff_max=eff_max,
            ticks=ticks,
            series_colors=series_colors,
        )


def _draw_vertical_grid_and_ticks(
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
    grid_style = val_axis.grid_style or Style(
        line_color=_DEFAULT_GRID_COLOR,
        line_width=0.8,
        line_style="dashed",
    )
    tick_label_style = val_axis.tick_label_style or Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT,
        text_halign="right",
        text_valign="center",
        text_angle=val_axis.tick_label_angle,
    )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, val_axis.scale)
        tick_y = p_min_y + ratio * plot_h

        if val_axis.show_grid and 0.001 < ratio < 0.999:
            canvas_line(xy1=(p_min_x, tick_y), xy2=(p_max_x, tick_y), style=grid_style)

        if val_axis.show_ticks:
            formatted_tick = val_axis.format_value(tick)
            canvas_text(xy=(p_min_x - 1.2, tick_y), text=formatted_tick, style=tick_label_style)


def _draw_vertical_category_labels(
    chart: BarChart,
    p_min_x: float,
    p_min_y: float,
    slot_w: float,
) -> None:
    """Render category labels below the X baseline."""
    cat_label_style = chart.x_axis.tick_label_style or Style(
        text_size=10.0,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="top",
        text_angle=chart.x_axis.tick_label_angle,
    )
    for c_idx, cat in enumerate(chart.categories):
        cat_cx = p_min_x + (c_idx + 0.5) * slot_w
        canvas_text(xy=(cat_cx, p_min_y - 1.8), text=cat, style=cat_label_style)


def _draw_vertical_grouped_bars(
    chart: BarChart,
    p_min_x: float,
    p_min_y: float,
    slot_w: float,
    plot_h: float,
    eff_min: float,
    eff_max: float,
    base_ratio: float,
    series_colors: list[ColorType],
    val_label_style: Style,
) -> None:
    """Render grouped vertical bars."""
    val_axis = chart.y_axis
    cat_count = len(chart.categories)
    num_series = len(chart.series)
    cluster_w = slot_w * chart.bar_width_ratio
    bar_w = cluster_w / num_series

    for c_idx in range(cat_count):
        cat_cx = p_min_x + (c_idx + 0.5) * slot_w
        start_x = cat_cx - cluster_w / 2.0

        for s_idx, series in enumerate(chart.series):
            if c_idx >= len(series.values):
                continue

            v = series.values[c_idx]
            bar_cx = start_x + (s_idx + 0.5) * bar_w
            val_ratio = value_to_ratio(v, eff_min, eff_max, val_axis.scale)

            h = max(0.1, abs(val_ratio - base_ratio) * plot_h)
            bar_cy = p_min_y + ((base_ratio + val_ratio) / 2.0) * plot_h

            bar_style = series.style or Style(
                fill_color=series_colors[s_idx],
                line_width=0,
            )
            canvas_rectangle(
                xy=(bar_cx, bar_cy),
                width=bar_w,
                height=h,
                r=chart.r,
                style=bar_style,
            )

            if chart.show_values:
                lbl = val_axis.format_value(v)
                canvas_text(xy=(bar_cx, p_min_y + val_ratio * plot_h + 0.8), text=lbl, style=val_label_style)


def _draw_vertical_stacked_bars(
    chart: BarChart,
    p_min_x: float,
    p_min_y: float,
    slot_w: float,
    plot_h: float,
    eff_min: float,
    eff_max: float,
    base_val: float,
    series_colors: list[ColorType],
    val_label_style: Style,
) -> None:
    """Render stacked vertical bars."""
    val_axis = chart.y_axis
    cat_count = len(chart.categories)
    bar_w = slot_w * chart.bar_width_ratio

    for c_idx in range(cat_count):
        cat_cx = p_min_x + (c_idx + 0.5) * slot_w
        accum_val = base_val

        for s_idx, series in enumerate(chart.series):
            if c_idx >= len(series.values):
                continue

            v = series.values[c_idx]
            prev_ratio = value_to_ratio(accum_val, eff_min, eff_max, val_axis.scale)
            accum_val += v
            next_ratio = value_to_ratio(accum_val, eff_min, eff_max, val_axis.scale)

            h = max(0.1, abs(next_ratio - prev_ratio) * plot_h)
            bar_cy = p_min_y + ((prev_ratio + next_ratio) / 2.0) * plot_h

            bar_style = series.style or Style(
                fill_color=series_colors[s_idx],
                line_width=0,
            )
            canvas_rectangle(
                xy=(cat_cx, bar_cy),
                width=bar_w,
                height=h,
                r=chart.r,
                style=bar_style,
            )

        if chart.show_values:
            top_ratio = value_to_ratio(accum_val, eff_min, eff_max, val_axis.scale)
            lbl = val_axis.format_value(accum_val)
            canvas_text(xy=(cat_cx, p_min_y + top_ratio * plot_h + 0.8), text=lbl, style=val_label_style)


def _render_vertical_bars(
    chart: BarChart,
    plot_bounds: tuple[float, float, float, float],
    plot_w: float,
    plot_h: float,
    eff_min: float,
    eff_max: float,
    ticks: list[float],
    series_colors: list[ColorType],
) -> None:
    """Render vertical bar chart elements (grid, ticks, bars, category labels)."""
    p_min_x, p_min_y, p_max_x, _ = plot_bounds
    val_axis = chart.y_axis

    _draw_vertical_grid_and_ticks(val_axis, ticks, eff_min, eff_max, p_min_x, p_min_y, p_max_x, plot_h)

    # Baseline stroke
    base_val = eff_min if val_axis.scale == "log" else 0.0
    base_ratio = value_to_ratio(base_val, eff_min, eff_max, val_axis.scale)
    base_y = p_min_y + base_ratio * plot_h
    if val_axis.show_axis_line:
        axis_line_style = val_axis.line_style or Style(line_color=_DEFAULT_AXIS_COLOR, line_width=1.2)
        canvas_line(xy1=(p_min_x, base_y), xy2=(p_max_x, base_y), style=axis_line_style)

    cat_count = len(chart.categories)
    slot_w = plot_w / max(1, cat_count)
    _draw_vertical_category_labels(chart, p_min_x, p_min_y, slot_w)

    if not chart.series or cat_count == 0:
        return

    val_label_style = chart.value_label_style or Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="bottom",
    )

    if chart.bar_mode == "group":
        _draw_vertical_grouped_bars(
            chart=chart,
            p_min_x=p_min_x,
            p_min_y=p_min_y,
            slot_w=slot_w,
            plot_h=plot_h,
            eff_min=eff_min,
            eff_max=eff_max,
            base_ratio=base_ratio,
            series_colors=series_colors,
            val_label_style=val_label_style,
        )
    else:
        _draw_vertical_stacked_bars(
            chart=chart,
            p_min_x=p_min_x,
            p_min_y=p_min_y,
            slot_w=slot_w,
            plot_h=plot_h,
            eff_min=eff_min,
            eff_max=eff_max,
            base_val=base_val,
            series_colors=series_colors,
            val_label_style=val_label_style,
        )


def _draw_horizontal_grid_and_ticks(
    val_axis: Axis,
    ticks: list[float],
    eff_min: float,
    eff_max: float,
    p_min_x: float,
    p_min_y: float,
    p_max_y: float,
    plot_w: float,
) -> None:
    """Render vertical gridlines and numeric tick labels along X axis."""
    grid_style = val_axis.grid_style or Style(
        line_color=_DEFAULT_GRID_COLOR,
        line_width=0.8,
        line_style="dashed",
    )
    tick_label_style = val_axis.tick_label_style or Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT,
        text_halign="center",
        text_valign="top",
        text_angle=val_axis.tick_label_angle,
    )

    for tick in ticks:
        ratio = value_to_ratio(tick, eff_min, eff_max, val_axis.scale)
        tick_x = p_min_x + ratio * plot_w

        if val_axis.show_grid and 0.001 < ratio < 0.999:
            canvas_line(xy1=(tick_x, p_min_y), xy2=(tick_x, p_max_y), style=grid_style)

        if val_axis.show_ticks:
            formatted_tick = val_axis.format_value(tick)
            canvas_text(xy=(tick_x, p_min_y - 1.5), text=formatted_tick, style=tick_label_style)


def _draw_horizontal_category_labels(
    chart: BarChart,
    p_min_x: float,
    p_max_y: float,
    slot_h: float,
) -> None:
    """Render category labels along Y axis."""
    cat_label_style = chart.y_axis.tick_label_style or Style(
        text_size=10.0,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="right",
        text_valign="center",
        text_angle=chart.y_axis.tick_label_angle,
    )
    for c_idx, cat in enumerate(chart.categories):
        cat_cy = p_max_y - (c_idx + 0.5) * slot_h
        canvas_text(xy=(p_min_x - 1.8, cat_cy), text=cat, style=cat_label_style)


def _draw_horizontal_grouped_bars(
    chart: BarChart,
    p_min_x: float,
    p_max_y: float,
    slot_h: float,
    plot_w: float,
    eff_min: float,
    eff_max: float,
    base_ratio: float,
    series_colors: list[ColorType],
    val_label_style: Style,
) -> None:
    """Render grouped horizontal bars."""
    val_axis = chart.x_axis
    cat_count = len(chart.categories)
    num_series = len(chart.series)
    cluster_h = slot_h * chart.bar_width_ratio
    bar_h = cluster_h / num_series

    for c_idx in range(cat_count):
        cat_cy = p_max_y - (c_idx + 0.5) * slot_h
        start_y = cat_cy + cluster_h / 2.0

        for s_idx, series in enumerate(chart.series):
            if c_idx >= len(series.values):
                continue

            v = series.values[c_idx]
            bar_cy = start_y - (s_idx + 0.5) * bar_h
            val_ratio = value_to_ratio(v, eff_min, eff_max, val_axis.scale)

            w = max(0.1, abs(val_ratio - base_ratio) * plot_w)
            bar_cx = p_min_x + ((base_ratio + val_ratio) / 2.0) * plot_w

            bar_style = series.style or Style(
                fill_color=series_colors[s_idx],
                line_width=0,
            )
            canvas_rectangle(
                xy=(bar_cx, bar_cy),
                width=w,
                height=bar_h,
                r=chart.r,
                style=bar_style,
            )

            if chart.show_values:
                lbl = val_axis.format_value(v)
                canvas_text(xy=(p_min_x + val_ratio * plot_w + 1.2, bar_cy), text=lbl, style=val_label_style)


def _draw_horizontal_stacked_bars(
    chart: BarChart,
    p_min_x: float,
    p_max_y: float,
    slot_h: float,
    plot_w: float,
    eff_min: float,
    eff_max: float,
    base_val: float,
    series_colors: list[ColorType],
    val_label_style: Style,
) -> None:
    """Render stacked horizontal bars."""
    val_axis = chart.x_axis
    cat_count = len(chart.categories)
    bar_h = slot_h * chart.bar_width_ratio

    for c_idx in range(cat_count):
        cat_cy = p_max_y - (c_idx + 0.5) * slot_h
        accum_val = base_val

        for s_idx, series in enumerate(chart.series):
            if c_idx >= len(series.values):
                continue

            v = series.values[c_idx]
            prev_ratio = value_to_ratio(accum_val, eff_min, eff_max, val_axis.scale)
            accum_val += v
            next_ratio = value_to_ratio(accum_val, eff_min, eff_max, val_axis.scale)

            w = max(0.1, abs(next_ratio - prev_ratio) * plot_w)
            bar_cx = p_min_x + ((prev_ratio + next_ratio) / 2.0) * plot_w

            bar_style = series.style or Style(
                fill_color=series_colors[s_idx],
                line_width=0,
            )
            canvas_rectangle(
                xy=(bar_cx, cat_cy),
                width=w,
                height=bar_h,
                r=chart.r,
                style=bar_style,
            )

        if chart.show_values:
            top_ratio = value_to_ratio(accum_val, eff_min, eff_max, val_axis.scale)
            lbl = val_axis.format_value(accum_val)
            canvas_text(xy=(p_min_x + top_ratio * plot_w + 1.2, cat_cy), text=lbl, style=val_label_style)


def _render_horizontal_bars(
    chart: BarChart,
    plot_bounds: tuple[float, float, float, float],
    plot_w: float,
    plot_h: float,
    eff_min: float,
    eff_max: float,
    ticks: list[float],
    series_colors: list[ColorType],
) -> None:
    """Render horizontal bar chart elements."""
    p_min_x, p_min_y, _, p_max_y = plot_bounds
    val_axis = chart.x_axis

    _draw_horizontal_grid_and_ticks(val_axis, ticks, eff_min, eff_max, p_min_x, p_min_y, p_max_y, plot_w)

    # Baseline stroke (vertical line at x=0 or x=min)
    base_val = eff_min if val_axis.scale == "log" else 0.0
    base_ratio = value_to_ratio(base_val, eff_min, eff_max, val_axis.scale)
    base_x = p_min_x + base_ratio * plot_w
    if val_axis.show_axis_line:
        axis_line_style = val_axis.line_style or Style(line_color=_DEFAULT_AXIS_COLOR, line_width=1.2)
        canvas_line(xy1=(base_x, p_min_y), xy2=(base_x, p_max_y), style=axis_line_style)

    cat_count = len(chart.categories)
    slot_h = plot_h / max(1, cat_count)
    _draw_horizontal_category_labels(chart, p_min_x, p_max_y, slot_h)

    if not chart.series or cat_count == 0:
        return

    val_label_style = chart.value_label_style or Style(
        text_size=9.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="left",
        text_valign="center",
    )

    if chart.bar_mode == "group":
        _draw_horizontal_grouped_bars(
            chart=chart,
            p_min_x=p_min_x,
            p_max_y=p_max_y,
            slot_h=slot_h,
            plot_w=plot_w,
            eff_min=eff_min,
            eff_max=eff_max,
            base_ratio=base_ratio,
            series_colors=series_colors,
            val_label_style=val_label_style,
        )
    else:
        _draw_horizontal_stacked_bars(
            chart=chart,
            p_min_x=p_min_x,
            p_max_y=p_max_y,
            slot_h=slot_h,
            plot_w=plot_w,
            eff_min=eff_min,
            eff_max=eff_max,
            base_val=base_val,
            series_colors=series_colors,
            val_label_style=val_label_style,
        )
