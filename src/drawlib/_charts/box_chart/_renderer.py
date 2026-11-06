# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for vertical and horizontal BoxChart."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._style_utils import (
    clamp_ratio,
    ensure_line_style,
    ensure_shape_style,
    ensure_text_style,
    with_alpha,
)
from drawlib._charts._common._types import ColorType, FormatterType, PointShape
from drawlib._charts.box_chart._stats import BoxStats, generate_jitter_offsets
from drawlib._core.l3_colors import Color
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import rhombus as canvas_rhombus
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import triangle as canvas_triangle

if TYPE_CHECKING:
    from drawlib._charts.box_chart._chart import BoxChart
    from drawlib._charts.box_chart._series import Series


@dataclass(frozen=True)
class _ResolvedSeriesStyles:
    """Resolved sub-element styles for a single BoxChart series."""

    box: Style
    whisker: Style
    median: Style
    point: Style
    outlier: Style
    mean: Style


@dataclass(frozen=True)
class _PlotContext:
    """Geometry and axis domain context for rendering BoxChart."""

    p_min_x: float
    p_min_y: float
    p_max_x: float
    p_max_y: float
    plot_w: float
    plot_h: float
    eff_min: float
    eff_max: float
    ticks: list[float]
    cat_count: int


def _is_visible_color(c: ColorType | None) -> bool:
    """Return True if color is non-None and has alpha > 0.01."""
    if c is None:
        return False
    col = c if isinstance(c, Color) else Color(c)
    return col.a > 0.01


def _first_visible_color(*candidates: ColorType | None) -> ColorType:
    """Return the first color candidate with visible alpha, or dark slate fallback."""
    for c in candidates:
        if _is_visible_color(c) and c is not None:
            return c
    return (30, 41, 59, 1.0)


def _rel_luminance(c: ColorType) -> float:
    """Compute approximate perceptual luminance in [0.0, 1.0]."""
    col = c if isinstance(c, Color) else Color(c)
    return (0.2126 * col.r + 0.7152 * col.g + 0.0722 * col.b) / 255.0


def _resolve_series_styles(chart: BoxChart, series: Series) -> _ResolvedSeriesStyles:
    """Derive high-contrast styles for box, whisker, median, point, outlier, and mean."""
    base = series.style
    box_style = ensure_shape_style(base)
    if chart.box_r > 0.0 and base.shape_r is None:
        box_style = box_style.patch(shape_r=chart.box_r)

    fill_col = base.shape_fill_color
    is_dark_box = _is_visible_color(fill_col) and fill_col is not None and _rel_luminance(fill_col) < 0.58

    accent_col = _first_visible_color(base.line_color, base.shape_line_color, base.shape_fill_color)
    deep_col = _first_visible_color(base.text_color, base.line_color, base.shape_line_color, base.shape_fill_color)
    lw = base.line_width or (base.shape_line_width if (base.shape_line_width or 0.0) > 0.0 else None) or 1.4

    whisker_style = (
        ensure_line_style(series.whisker_style)
        if series.whisker_style is not None
        else Style(line_color=accent_col, line_width=max(1.0, lw * 0.9), line_style="solid")
    )

    med_col: ColorType = (255, 255, 255, 0.96) if (series.show_box and is_dark_box) else deep_col
    median_style = (
        ensure_line_style(series.median_style)
        if series.median_style is not None
        else Style(line_color=med_col, line_width=max(2.0, lw * 1.45), line_style="solid")
    )

    if series.point_style is not None:
        point_style = ensure_shape_style(series.point_style)
    elif series.show_box and is_dark_box:
        point_style = Style(
            shape_fill_color=with_alpha(accent_col, 0.90),
            shape_line_color=(255, 255, 255, 0.94),
            shape_line_width=1.0,
        )
    else:
        point_style = Style(
            shape_fill_color=with_alpha(accent_col, 0.72),
            shape_line_color=deep_col,
            shape_line_width=0.9,
        )

    outlier_style = (
        ensure_shape_style(series.outlier_style)
        if series.outlier_style is not None
        else Style(
            shape_fill_color=with_alpha(accent_col, 0.30),
            shape_line_color=accent_col,
            shape_line_width=1.25,
        )
    )

    if series.mean_style is not None:
        mean_style = ensure_shape_style(series.mean_style)
    elif series.show_box and is_dark_box:
        mean_style = Style(
            shape_fill_color=(255, 255, 255, 0.95),
            shape_line_color=deep_col,
            shape_line_width=1.2,
        )
    else:
        mean_style = Style(
            shape_fill_color=deep_col,
            shape_line_color=(255, 255, 255, 0.95),
            shape_line_width=1.1,
        )

    return _ResolvedSeriesStyles(
        box=box_style,
        whisker=whisker_style,
        median=median_style,
        point=point_style,
        outlier=outlier_style,
        mean=mean_style,
    )


def _format_inline_value(val_axis: Axis, value_format: FormatterType, value: float) -> str:
    """Format an inline median label using chart.value_format or val_axis.format_value."""
    if isinstance(value_format, str):
        try:
            return value_format.format(value)
        except Exception:
            return val_axis.format_value(value)
    if callable(value_format):
        return str(value_format(value))
    return val_axis.format_value(value)


def _draw_marker(cx: float, cy: float, radius: float, shape: PointShape, style: Style) -> None:
    """Render a single point/outlier/mean marker on the canvas."""
    if shape == "none" or radius <= 0.0:
        return
    if shape == "square":
        d = radius * 2.0
        canvas_rectangle(xy=(cx, cy), width=d, height=d, style=style)
    elif shape == "rhombus":
        d = radius * 2.2
        canvas_rhombus(xy=(cx, cy), width=d, height=d, style=style)
    elif shape == "triangle":
        canvas_triangle(xy=(cx, cy), width=radius * 2.2, height=radius * 2.0, style=style)
    else:
        canvas_circle(xy=(cx, cy), radius=radius, style=style)


def _compute_margins(chart: BoxChart) -> tuple[float, float, float, float]:
    """Compute (left, bottom, right, top) plot margins from chart typography flags."""
    has_text = (
        chart.axis_text_style is not None
        or chart.x_axis.tick_label_style is not None
        or chart.y_axis.tick_label_style is not None
    )
    has_x_label = bool(
        chart.x_axis.label and (chart.x_axis.label_style is not None or chart.axis_text_style is not None)
    )
    has_y_label = bool(
        chart.y_axis.label and (chart.y_axis.label_style is not None or chart.axis_text_style is not None)
    )
    has_title = bool(chart.title and chart.title_style is not None)

    if chart.orientation == "vertical":
        m_left = (9.5 if has_text else 3.5) + (4.2 if has_y_label else 0.0)
        m_bottom = (5.5 if has_text else 3.0) + (4.0 if has_x_label else 0.0)
        m_right = 3.5
        m_top = (5.0 if has_title else 2.8) + (1.8 if chart.value_text_style is not None else 0.0)
    else:
        m_left = (13.0 if has_text else 3.5) + (4.2 if has_y_label else 0.0)
        m_bottom = (5.5 if has_text else 3.0) + (4.0 if has_x_label else 0.0)
        m_right = 3.5 + (3.5 if chart.value_text_style is not None else 0.0)
        m_top = 5.0 if has_title else 2.8
    return (m_left, m_bottom, m_right, m_top)


def _gather_data_domain(chart: BoxChart) -> tuple[float, float, int]:
    """Gather full-dataset min/max across all series (independent of show/draw_ratio)."""
    cat_count = max(
        len(chart.categories),
        max((len(s.stats) for s in chart.series), default=0),
    )
    all_vals: list[float] = []
    for s in chart.series:
        for st in s.stats:
            if st is not None:
                all_vals.extend(
                    st.extent_values(
                        show_box=s.show_box,
                        show_points=s.show_points,
                        show_outliers=s.show_outliers,
                        show_mean=s.show_mean,
                    )
                )
    if not all_vals:
        return (0.0, 10.0, cat_count)
    d_min = min(all_vals)
    d_max = max(all_vals)
    if abs(d_max - d_min) <= 1e-6:
        pad = max(1.0, abs(d_min) * 0.1)
        return (d_min - pad, d_max + pad, cat_count)
    return (d_min, d_max, cat_count)


def _get_slot_draw_ratio(c_idx: int, cat_count: int, series: Series, orientation: str) -> float:
    """Compute effective partial rendering ratio [0.0, 1.0] for category slot c_idx."""
    if not series.show:
        return 0.0
    r = clamp_ratio(series.draw_ratio)
    if r <= 0.0 or r >= 1.0 or cat_count <= 0:
        return r
    if orientation == "vertical" and series.draw_direction == "left_to_right":
        return max(0.0, min(1.0, r * cat_count - c_idx))
    if orientation == "horizontal" and series.draw_direction == "bottom_to_top":
        bottom_idx = (cat_count - 1) - c_idx
        return max(0.0, min(1.0, r * cat_count - bottom_idx))
    return r


def _interp_from_median(median_pos: float, target_pos: float, ratio: float) -> float:
    """Interpolate a coordinate outward from median_pos according to ratio in [0.0, 1.0]."""
    return median_pos + (target_pos - median_pos) * ratio


def _draw_vertical_axes_and_grid(chart: BoxChart, ctx: _PlotContext) -> None:
    """Render gridlines, ticks, category labels, baselines, and axis titles for vertical chart."""
    val_axis = chart.y_axis
    grid_style = val_axis.grid_style or chart.grid_style
    tick_style = val_axis.tick_label_style or chart.axis_text_style
    if tick_style is not None:
        tick_style = ensure_text_style(tick_style, halign="right", valign="center")

    for tick in ctx.ticks:
        ratio = value_to_ratio(tick, ctx.eff_min, ctx.eff_max, val_axis.scale)
        ty = ctx.p_min_y + ratio * ctx.plot_h
        if val_axis.show_grid and grid_style is not None and 0.001 < ratio < 0.999:
            canvas_line(xy1=(ctx.p_min_x, ty), xy2=(ctx.p_max_x, ty), style=ensure_line_style(grid_style))
        if val_axis.show_ticks and tick_style is not None:
            canvas_text(xy=(ctx.p_min_x - 1.2, ty), text=val_axis.format_value(tick), style=tick_style)

    cat_style = chart.x_axis.tick_label_style or chart.axis_text_style
    if cat_style is not None and ctx.cat_count > 0:
        c_style = ensure_text_style(cat_style, halign="center", valign="top")
        slot_w = ctx.plot_w / ctx.cat_count
        for c_idx, cat in enumerate(chart.categories):
            if c_idx < ctx.cat_count:
                cx = ctx.p_min_x + (c_idx + 0.5) * slot_w
                canvas_text(xy=(cx, ctx.p_min_y - 1.6), text=cat, style=c_style)


def _draw_horizontal_axes_and_grid(chart: BoxChart, ctx: _PlotContext) -> None:
    """Render gridlines, ticks, category labels, baselines, and axis titles for horizontal chart."""
    val_axis = chart.x_axis
    grid_style = val_axis.grid_style or chart.grid_style
    tick_style = val_axis.tick_label_style or chart.axis_text_style
    if tick_style is not None:
        tick_style = ensure_text_style(tick_style, halign="center", valign="top")

    for tick in ctx.ticks:
        ratio = value_to_ratio(tick, ctx.eff_min, ctx.eff_max, val_axis.scale)
        tx = ctx.p_min_x + ratio * ctx.plot_w
        if val_axis.show_grid and grid_style is not None and 0.001 < ratio < 0.999:
            canvas_line(xy1=(tx, ctx.p_min_y), xy2=(tx, ctx.p_max_y), style=ensure_line_style(grid_style))
        if val_axis.show_ticks and tick_style is not None:
            canvas_text(xy=(tx, ctx.p_min_y - 1.5), text=val_axis.format_value(tick), style=tick_style)

    cat_style = chart.y_axis.tick_label_style or chart.axis_text_style
    if cat_style is not None and ctx.cat_count > 0:
        c_style = ensure_text_style(cat_style, halign="right", valign="center")
        slot_h = ctx.plot_h / ctx.cat_count
        for c_idx, cat in enumerate(chart.categories):
            if c_idx < ctx.cat_count:
                cy = ctx.p_max_y - (c_idx + 0.5) * slot_h
                canvas_text(xy=(ctx.p_min_x - 1.8, cy), text=cat, style=c_style)


def _draw_baselines_and_titles(chart: BoxChart, ctx: _PlotContext) -> None:
    """Render X/Y axis baseline strokes and descriptive axis titles."""
    x_line_style = chart.x_axis.line_style or chart.axis_line_style
    y_line_style = chart.y_axis.line_style or chart.axis_line_style

    if chart.x_axis.show_axis_line and x_line_style is not None:
        canvas_line(
            xy1=(ctx.p_min_x, ctx.p_min_y),
            xy2=(ctx.p_max_x, ctx.p_min_y),
            style=ensure_line_style(x_line_style),
        )
    if chart.y_axis.show_axis_line and y_line_style is not None:
        canvas_line(
            xy1=(ctx.p_min_x, ctx.p_min_y),
            xy2=(ctx.p_min_x, ctx.p_max_y),
            style=ensure_line_style(y_line_style),
        )

    x_lbl_style = chart.x_axis.label_style or chart.axis_text_style
    if chart.x_axis.label and x_lbl_style is not None:
        xs = ensure_text_style(x_lbl_style, halign="center", valign="center")
        canvas_text(xy=((ctx.p_min_x + ctx.p_max_x) / 2.0, ctx.p_min_y - 5.8), text=chart.x_axis.label, style=xs)

    y_lbl_style = chart.y_axis.label_style or chart.axis_text_style
    if chart.y_axis.label and y_lbl_style is not None:
        left_offset = 10.8 if chart.orientation == "horizontal" else 8.2
        y_angle = y_lbl_style.angle if y_lbl_style.angle is not None else 90.0
        ys = ensure_text_style(y_lbl_style.patch(angle=y_angle), halign="center", valign="center")
        canvas_text(
            xy=(ctx.p_min_x - left_offset, (ctx.p_min_y + ctx.p_max_y) / 2.0),
            text=chart.y_axis.label,
            style=ys,
        )


def _val_to_pos(val: float, val_axis: Axis, ctx: _PlotContext, *, is_vertical: bool) -> float:
    """Convert a data value into a canvas Y (vertical) or X (horizontal) coordinate."""
    ratio = value_to_ratio(val, ctx.eff_min, ctx.eff_max, val_axis.scale)
    if is_vertical:
        return ctx.p_min_y + ratio * ctx.plot_h
    return ctx.p_min_x + ratio * ctx.plot_w


def _draw_single_box_and_whiskers(
    chart: BoxChart,
    st: BoxStats,
    styles: _ResolvedSeriesStyles,
    val_axis: Axis,
    ctx: _PlotContext,
    slot_center: float,
    box_thickness: float,
    cat_r: float,
    *,
    is_vertical: bool,
) -> float:
    """Render whiskers, T-caps, Q1-Q3 box, and median line; return median coordinate."""
    med_pos = _val_to_pos(st.median, val_axis, ctx, is_vertical=is_vertical)
    q1_pos = _interp_from_median(med_pos, _val_to_pos(st.q1, val_axis, ctx, is_vertical=is_vertical), cat_r)
    q3_pos = _interp_from_median(med_pos, _val_to_pos(st.q3, val_axis, ctx, is_vertical=is_vertical), cat_r)
    min_pos = _interp_from_median(med_pos, _val_to_pos(st.min, val_axis, ctx, is_vertical=is_vertical), cat_r)
    max_pos = _interp_from_median(med_pos, _val_to_pos(st.max, val_axis, ctx, is_vertical=is_vertical), cat_r)

    cap_half = (box_thickness * chart.cap_width_ratio) / 2.0
    box_half = box_thickness / 2.0
    box_span = max(0.15, abs(q3_pos - q1_pos))
    box_mid = (q1_pos + q3_pos) / 2.0

    if is_vertical:
        if q1_pos - min_pos > 1e-4:
            canvas_line(xy1=(slot_center, q1_pos), xy2=(slot_center, min_pos), style=styles.whisker)
        if max_pos - q3_pos > 1e-4:
            canvas_line(xy1=(slot_center, q3_pos), xy2=(slot_center, max_pos), style=styles.whisker)
        if cap_half > 1e-4:
            c0, c1 = slot_center - cap_half, slot_center + cap_half
            canvas_line(xy1=(c0, min_pos), xy2=(c1, min_pos), style=styles.whisker)
            canvas_line(xy1=(c0, max_pos), xy2=(c1, max_pos), style=styles.whisker)
        canvas_rectangle(xy=(slot_center, box_mid), width=box_thickness, height=box_span, style=styles.box)
        canvas_line(xy1=(slot_center - box_half, med_pos), xy2=(slot_center + box_half, med_pos), style=styles.median)
    else:
        if q1_pos - min_pos > 1e-4:
            canvas_line(xy1=(q1_pos, slot_center), xy2=(min_pos, slot_center), style=styles.whisker)
        if max_pos - q3_pos > 1e-4:
            canvas_line(xy1=(q3_pos, slot_center), xy2=(max_pos, slot_center), style=styles.whisker)
        if cap_half > 1e-4:
            c0, c1 = slot_center - cap_half, slot_center + cap_half
            canvas_line(xy1=(min_pos, c0), xy2=(min_pos, c1), style=styles.whisker)
            canvas_line(xy1=(max_pos, c0), xy2=(max_pos, c1), style=styles.whisker)
        canvas_rectangle(xy=(box_mid, slot_center), width=box_span, height=box_thickness, style=styles.box)
        canvas_line(xy1=(med_pos, slot_center - box_half), xy2=(med_pos, slot_center + box_half), style=styles.median)

    return med_pos


def _draw_slot_markers_and_label(
    chart: BoxChart,
    series: Series,
    st: BoxStats,
    styles: _ResolvedSeriesStyles,
    val_axis: Axis,
    ctx: _PlotContext,
    s_idx: int,
    c_idx: int,
    slot_center: float,
    box_thickness: float,
    cat_r: float,
    *,
    is_vertical: bool,
) -> None:
    """Render mean marker, outlier markers or jittered strip points, and inline median label."""
    med_pos = _val_to_pos(st.median, val_axis, ctx, is_vertical=is_vertical)

    if series.show_mean and st.mean is not None:
        m_pos = _interp_from_median(med_pos, _val_to_pos(st.mean, val_axis, ctx, is_vertical=is_vertical), cat_r)
        m_xy = (slot_center, m_pos) if is_vertical else (m_pos, slot_center)
        _draw_marker(m_xy[0], m_xy[1], series.point_radius * 1.05, chart.mean_shape, styles.mean)

    if series.show_points and st.points:
        offsets = generate_jitter_offsets(
            len(st.points),
            jitter=series.jitter,
            jitter_seed=chart.jitter_seed,
            series_idx=s_idx,
            category_idx=c_idx,
        )
        has_explicit_outlier_style = series.outlier_style is not None
        for pt_val, norm_off in zip(st.points, offsets, strict=True):
            p_pos = _interp_from_median(med_pos, _val_to_pos(pt_val, val_axis, ctx, is_vertical=is_vertical), cat_r)
            transverse = slot_center + norm_off * box_thickness
            p_xy = (transverse, p_pos) if is_vertical else (p_pos, transverse)
            is_out = has_explicit_outlier_style and (pt_val < st.min or pt_val > st.max)
            m_style = styles.outlier if is_out else styles.point
            m_shape = chart.outlier_shape if is_out else series.point_shape
            _draw_marker(p_xy[0], p_xy[1], series.point_radius, m_shape, m_style)
    elif series.show_box and series.show_outliers and st.outliers:
        for out_val in st.outliers:
            o_pos = _interp_from_median(med_pos, _val_to_pos(out_val, val_axis, ctx, is_vertical=is_vertical), cat_r)
            o_xy = (slot_center, o_pos) if is_vertical else (o_pos, slot_center)
            _draw_marker(o_xy[0], o_xy[1], series.point_radius, chart.outlier_shape, styles.outlier)

    if chart.value_text_style is not None and cat_r >= 0.5:
        lbl = _format_inline_value(val_axis, chart.value_format, st.median)
        extra_out = st.outliers if (series.show_outliers and not series.show_points) else []
        extra_pts = st.points if series.show_points else []
        anchor_val = max(st.max, *extra_out, *extra_pts)
        tip_pos = _interp_from_median(med_pos, _val_to_pos(anchor_val, val_axis, ctx, is_vertical=is_vertical), cat_r)
        if is_vertical:
            v_style = ensure_text_style(chart.value_text_style, halign="center", valign="bottom")
            canvas_text(xy=(slot_center, tip_pos + 0.9), text=lbl, style=v_style)
        else:
            v_style = ensure_text_style(chart.value_text_style, halign="left", valign="center")
            canvas_text(xy=(tip_pos + 1.1, slot_center), text=lbl, style=v_style)


def _render_all_series(chart: BoxChart, ctx: _PlotContext) -> None:
    """Render all grouped series across categories for vertical or horizontal orientation."""
    if ctx.cat_count <= 0 or not chart.series:
        return

    is_vertical = chart.orientation == "vertical"
    val_axis = chart.value_axis
    num_series = len(chart.series)
    cat_span = (ctx.plot_w if is_vertical else ctx.plot_h) / ctx.cat_count
    cluster_span = cat_span * chart.box_width_ratio
    series_pitch = cluster_span / num_series
    box_thickness = series_pitch * (0.80 if num_series > 1 else 1.0)

    resolved_styles = [_resolve_series_styles(chart, s) for s in chart.series]

    for c_idx in range(ctx.cat_count):
        if is_vertical:
            cat_center = ctx.p_min_x + (c_idx + 0.5) * cat_span
            start_pos = cat_center - cluster_span / 2.0
        else:
            cat_center = ctx.p_max_y - (c_idx + 0.5) * cat_span
            start_pos = cat_center + cluster_span / 2.0

        for s_idx, series in enumerate(chart.series):
            if c_idx >= len(series.stats):
                continue
            st = series.stats[c_idx]
            if st is None:
                continue

            cat_r = _get_slot_draw_ratio(c_idx, ctx.cat_count, series, chart.orientation)
            if cat_r <= 0.0:
                continue

            slot_center = (
                start_pos + (s_idx + 0.5) * series_pitch
                if is_vertical
                else start_pos - (s_idx + 0.5) * series_pitch
            )
            styles = resolved_styles[s_idx]

            if series.show_box:
                _draw_single_box_and_whiskers(
                    chart=chart,
                    st=st,
                    styles=styles,
                    val_axis=val_axis,
                    ctx=ctx,
                    slot_center=slot_center,
                    box_thickness=box_thickness,
                    cat_r=cat_r,
                    is_vertical=is_vertical,
                )

            _draw_slot_markers_and_label(
                chart=chart,
                series=series,
                st=st,
                styles=styles,
                val_axis=val_axis,
                ctx=ctx,
                s_idx=s_idx,
                c_idx=c_idx,
                slot_center=slot_center,
                box_thickness=box_thickness,
                cat_r=cat_r,
                is_vertical=is_vertical,
            )


def draw_box_chart(chart: BoxChart, xy: tuple[float, float]) -> None:
    """Render a complete BoxChart onto the canvas.

    Args:
        chart: BoxChart container instance.
        xy: Base canvas coordinate (x, y) corresponding to bottom-left corner.
    """
    bx, by = float(xy[0]), float(xy[1])
    cw, ch = chart.width, chart.height

    if chart.background_style is not None:
        canvas_rectangle(
            xy=(bx + cw / 2.0, by + ch / 2.0),
            width=cw,
            height=ch,
            style=ensure_shape_style(chart.background_style),
        )

    if chart.title and chart.title_style is not None:
        t_style = ensure_text_style(chart.title_style, halign="center", valign="center")
        canvas_text(xy=(bx + cw / 2.0, by + ch - 2.5), text=chart.title, style=t_style)

    m_left, m_bottom, m_right, m_top = _compute_margins(chart)
    p_min_x = bx + m_left
    p_max_x = bx + cw - m_right
    p_min_y = by + m_bottom
    p_max_y = by + ch - m_top
    plot_w = max(1.0, p_max_x - p_min_x)
    plot_h = max(1.0, p_max_y - p_min_y)

    d_min, d_max, cat_count = _gather_data_domain(chart)
    eff_min, eff_max, ticks = calculate_axis_range_and_ticks(chart.value_axis, d_min, d_max, is_bar=False)

    ctx = _PlotContext(
        p_min_x=p_min_x,
        p_min_y=p_min_y,
        p_max_x=p_min_x + plot_w,
        p_max_y=p_min_y + plot_h,
        plot_w=plot_w,
        plot_h=plot_h,
        eff_min=eff_min,
        eff_max=eff_max,
        ticks=ticks,
        cat_count=cat_count,
    )

    if chart.orientation == "vertical":
        _draw_vertical_axes_and_grid(chart, ctx)
    else:
        _draw_horizontal_axes_and_grid(chart, ctx)

    _render_all_series(chart, ctx)
    _draw_baselines_and_titles(chart, ctx)
