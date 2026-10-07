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

from drawlib._charts._common._style_utils import ensure_shape_style, ensure_text_style
from drawlib._charts._common._types import FormatterType
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import wedge as canvas_wedge

if TYPE_CHECKING:
    from drawlib._charts.pie_chart._chart import PieChart
    from drawlib._charts.pie_chart._slice import Slice


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


def _compute_slice_wedge_params(
    chart: PieChart,
    s: Slice,
    slice_start: float,
    next_angle: float,
    span: float,
    dr: float,
    ring_width: float | None,
) -> tuple[float, float | None, float, float]:
    """Compute effective radius, ring_width, angle_start, and angle_end for a slice."""
    if s.draw_direction == "left_to_right":
        eff_span = span * dr
        theta1, theta2 = (
            (slice_start - eff_span, slice_start)
            if chart.clockwise
            else (slice_start, slice_start + eff_span)
        )
        eff_radius = chart.radius
        eff_ring_width = ring_width
    else:
        eff_span = span
        theta1, theta2 = (next_angle, slice_start) if chart.clockwise else (slice_start, next_angle)
        if chart.hole_ratio > 0.0:
            inner_r = chart.radius * chart.hole_ratio
            eff_ring_width = (chart.radius - inner_r) * dr
            eff_radius = inner_r + eff_ring_width
        else:
            eff_radius = chart.radius * dr
            eff_ring_width = None

    if eff_span >= 360.0 - 1e-6:
        w_start, w_end = 0.0, 360.0
    else:
        w_start = theta1 % 360.0
        w_end = theta2 % 360.0

    return eff_radius, eff_ring_width, w_start, w_end


def _draw_pie_slices(
    chart: PieChart,
    center: tuple[float, float],
    total_val: float,
) -> None:
    """Render all wedges and slice percentage labels."""
    cx, cy = center
    ring_width = chart.radius * (1.0 - chart.hole_ratio) if chart.hole_ratio > 0.0 else None
    lbl_r = chart.radius * (1.0 + chart.hole_ratio) / 2.0 if chart.hole_ratio > 0.0 else chart.radius * 0.65

    cur_angle = chart.start_angle
    for s in chart.slices:
        if s.value <= 0:
            continue

        pct = (s.value / total_val) * 100.0
        span = (s.value / total_val) * 360.0
        slice_start = cur_angle
        next_angle = cur_angle - span if chart.clockwise else cur_angle + span
        mid_angle = (cur_angle + next_angle) / 2.0
        cur_angle = next_angle

        if not s.show:
            continue

        dr = max(0.0, min(1.0, float(s.draw_ratio)))
        if dr <= 0.0:
            continue

        eff_radius, eff_ring_width, w_start, w_end = _compute_slice_wedge_params(
            chart, s, slice_start, next_angle, span, dr, ring_width
        )

        mid_rad = math.radians(mid_angle)
        exp_x = s.explode * math.cos(mid_rad)
        exp_y = s.explode * math.sin(mid_rad)

        slice_style = ensure_shape_style(s.style)
        canvas_wedge(
            xy=(cx + exp_x, cy + exp_y),
            radius=eff_radius,
            width=eff_ring_width,
            angle_start=w_start,
            angle_end=w_end,
            style=slice_style,
        )

        if chart.value_text_style is not None and pct >= 4.0 and dr >= 0.6:
            lx = cx + exp_x + lbl_r * math.cos(mid_rad)
            ly = cy + exp_y + lbl_r * math.sin(mid_rad)
            lbl_text = _format_slice_label(chart.value_format, pct, s.value)
            val_style = ensure_text_style(chart.value_text_style, halign="center", valign="center")
            canvas_text(xy=(lx, ly), text=lbl_text, style=val_style)


def _draw_center_badge(chart: PieChart, center: tuple[float, float]) -> None:
    """Render centered KPI badge text inside donut hole."""
    if chart.hole_ratio <= 0.0 or not chart.center_text or chart.center_text_style is None:
        return

    c_style = ensure_text_style(chart.center_text_style, halign="center", valign="center")
    canvas_text(xy=center, text=chart.center_text, style=c_style)


def draw_pie_chart(chart: PieChart, xy: tuple[float, float]) -> None:
    """Render a complete PieChart or DonutChart onto the canvas."""
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

    total_val = sum(s.value for s in chart.slices if s.value > 0)
    if total_val <= 0 or not chart.slices:
        return

    has_title = bool(chart.title and chart.title_style is not None)
    center_x = c_min_x + chart_w / 2.0
    center_y = c_min_y + (chart_h - (6.0 if has_title else 0.0)) / 2.0

    _draw_pie_slices(chart, (center_x, center_y), total_val)
    _draw_center_badge(chart, (center_x, center_y))
