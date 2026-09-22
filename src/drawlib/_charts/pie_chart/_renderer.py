# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for PieChart and DonutChart."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from drawlib._charts._common._legend import get_legend_size, render_legend
from drawlib._charts._common._types import ColorType, FormatterType
from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.shapes import wedge as canvas_wedge
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.pie_chart._chart import PieChart
    from drawlib._charts.pie_chart._slice import PieSlice

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)
_DEFAULT_WHITE_TEXT = (255, 255, 255, 1.0)


def _resolve_slice_colors(slices: list[PieSlice]) -> list[ColorType]:
    """Resolve fill colors for all slices."""
    colors: list[ColorType] = []
    for i, s in enumerate(slices):
        if s.color is not None:
            colors.append(s.color)
        else:
            colors.append(DEFAULT_CHART_PALETTE[i % len(DEFAULT_CHART_PALETTE)])
    return colors


def _format_slice_label(fmt: FormatterType, pct: float, value: float) -> str:
    """Format slice label using format string or function."""
    if isinstance(fmt, str):
        try:
            return fmt.format(pct)
        except Exception:
            return f"{pct:.1f}%"
    if callable(fmt):
        return str(fmt(pct))
    return f"{pct:.1f}%"


def _draw_pie_slices(
    chart: PieChart,
    center: tuple[float, float],
    slice_colors: list[ColorType],
    total_val: float,
) -> None:
    """Render all wedges and slice percentage labels."""
    cx, cy = center
    ring_width = chart.radius * (1.0 - chart.hole_ratio) if chart.hole_ratio > 0.0 else None
    lbl_r = (
        chart.radius * (1.0 + chart.hole_ratio) / 2.0
        if chart.hole_ratio > 0.0
        else chart.radius * 0.65
    )

    val_label_style = chart.value_label_style or Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_WHITE_TEXT,
        text_halign="center",
        text_valign="center",
    )

    cur_angle = chart.start_angle
    for s_idx, s in enumerate(chart.slices):
        if s.value <= 0:
            continue

        pct = (s.value / total_val) * 100.0
        span = (s.value / total_val) * 360.0

        if chart.clockwise:
            next_angle = cur_angle - span
            theta1, theta2 = next_angle, cur_angle
            mid_angle = (cur_angle + next_angle) / 2.0
            cur_angle = next_angle
        else:
            next_angle = cur_angle + span
            theta1, theta2 = cur_angle, next_angle
            mid_angle = (cur_angle + next_angle) / 2.0
            cur_angle = next_angle

        if span >= 360.0 - 1e-6:
            w_start, w_end = 0.0, 360.0
        else:
            w_start = theta1 % 360.0
            w_end = theta2 % 360.0

        mid_rad = math.radians(mid_angle)
        exp_x = s.explode * math.cos(mid_rad)
        exp_y = s.explode * math.sin(mid_rad)

        slice_style = s.style or Style(
            fill_color=slice_colors[s_idx],
            line_color=(255, 255, 255, 1.0),
            line_width=1.0,
        )

        canvas_wedge(
            xy=(cx + exp_x, cy + exp_y),
            radius=chart.radius,
            width=ring_width,
            angle_start=w_start,
            angle_end=w_end,
            style=slice_style,
        )

        if chart.show_values and pct >= 4.0:
            lx = cx + exp_x + lbl_r * math.cos(mid_rad)
            ly = cy + exp_y + lbl_r * math.sin(mid_rad)
            lbl_text = _format_slice_label(chart.value_format, pct, s.value)
            canvas_text(xy=(lx, ly), text=lbl_text, style=val_label_style)


def _draw_center_badge(chart: PieChart, center: tuple[float, float]) -> None:
    """Render centered KPI badge text inside donut hole."""
    if chart.hole_ratio <= 0.0 or not chart.center_text:
        return

    c_style = chart.center_text_style or Style(
        text_size=11.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    canvas_text(xy=center, text=chart.center_text, style=c_style)


def draw_pie_chart(chart: PieChart, xy: tuple[float, float]) -> None:
    """Render a complete PieChart or DonutChart onto the canvas."""
    c_min_x, c_min_y = xy
    chart_w, chart_h = chart.get_size()
    c_max_x = c_min_x + chart_w
    c_max_y = c_min_y + chart_h

    total_val = sum(s.value for s in chart.slices if s.value > 0)
    if total_val <= 0 or not chart.slices:
        return

    slice_names = [s.name for s in chart.slices]
    slice_colors = _resolve_slice_colors(chart.slices)
    legend_w, legend_h = get_legend_size(chart.legend_position, slice_names, len(chart.slices))

    if chart.title:
        t_style = chart.title_style or Style(
            text_size=12.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=((c_min_x + c_max_x) / 2.0, c_max_y - 3.5), text=chart.title, style=t_style)

    # Compute center coordinates based on legend placement
    if chart.legend_position == "right":
        center_x = c_min_x + chart.radius + 4.0
        center_y = c_min_y + (chart_h - (4.0 if chart.title else 0.0)) / 2.0
        p_bounds = (c_min_x, c_min_y, center_x + chart.radius + 2.0, c_max_y)
    elif chart.legend_position in {"top", "bottom"}:
        center_x = c_min_x + chart_w / 2.0
        center_y = c_min_y + chart.radius + (6.0 if chart.legend_position == "bottom" else 2.0)
        p_bounds = (c_min_x, c_min_y, c_max_x, c_max_y)
    else:
        center_x = c_min_x + chart_w / 2.0
        center_y = c_min_y + chart_h / 2.0
        p_bounds = (c_min_x, c_min_y, c_max_x, c_max_y)

    render_legend(
        names=slice_names,
        colors=slice_colors,
        position=chart.legend_position,
        plot_bounds=p_bounds,
        chart_bounds=(c_min_x, c_min_y, c_max_x, c_max_y),
    )

    _draw_pie_slices(chart, (center_x, center_y), slice_colors, total_val)
    _draw_center_badge(chart, (center_x, center_y))
