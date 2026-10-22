# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for 2D matrix HeatmapChart."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._style_utils import (
    clamp_ratio,
    ensure_line_style,
    ensure_shape_style,
    ensure_text_style,
)
from drawlib._charts.heatmap_chart._models import (
    extract_heatmap_color,
    format_heatmap_value,
    interpolate_color_stops,
)
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    from drawlib._charts.heatmap_chart._chart import HeatmapChart
    from drawlib._charts.heatmap_chart._models import Cell, Row
    from drawlib._core.l3_colors import Color


def _compute_matrix_dimensions(chart: HeatmapChart) -> tuple[int, int, list[str], list[str]]:
    """Determine (num_rows, num_cols, x_labels, y_labels) for the matrix."""
    max_row_override = max((c.y + 1 for c in chart._cells.values()), default=0)
    max_col_override = max((c.x + 1 for c in chart._cells.values()), default=0)
    max_row_vals = max((len(r.values) for r in chart._rows), default=0)

    num_rows = max(len(chart._rows), len(chart.y_categories), max_row_override)
    num_cols = max(len(chart.x_categories), max_row_vals, max_col_override)

    x_labels = [chart.x_categories[i] if i < len(chart.x_categories) else "" for i in range(num_cols)]
    y_labels: list[str] = []
    for i in range(num_rows):
        if i < len(chart.y_categories) and chart.y_categories[i]:
            y_labels.append(chart.y_categories[i])
        elif i < len(chart._rows) and chart._rows[i].name:
            y_labels.append(chart._rows[i].name)
        else:
            y_labels.append("")

    return (num_rows, num_cols, x_labels, y_labels)


def _compute_plot_bounds(
    chart: HeatmapChart,
    bx: float,
    by: float,
    x_labels: list[str],
    y_labels: list[str],
) -> tuple[float, float, float, float]:
    """Calculate (plot_min_x, plot_min_y, plot_max_x, plot_max_y) inside chart box."""
    cw, ch = chart.width, chart.height
    has_title = bool(chart.title and chart.title_style is not None)
    has_text = chart.axis_text_style is not None
    has_x_labels = has_text and any(bool(lbl) for lbl in x_labels)
    has_y_labels = has_text and any(bool(lbl) for lbl in y_labels)

    max_y_len = max((len(lbl) for lbl in y_labels), default=0) if has_y_labels else 0
    margin_left = max(9.0, min(26.0, max_y_len * 1.15 + 3.0)) if has_y_labels else 3.0
    margin_right = 3.0

    title_band = 5.5 if has_title else 0.0
    if chart.x_label_position == "top":
        margin_top = title_band + (5.0 if has_x_labels else 2.5)
        margin_bottom = 3.0
    else:
        margin_top = title_band + 2.5 if has_title else 3.0
        margin_bottom = 5.5 if has_x_labels else 3.0

    plot_min_x = bx + margin_left
    plot_max_x = max(plot_min_x + 2.0, bx + cw - margin_right)
    plot_min_y = by + margin_bottom
    plot_max_y = max(plot_min_y + 2.0, by + ch - margin_top)
    return (plot_min_x, plot_min_y, plot_max_x, plot_max_y)


def _build_cell_shape_style(
    chart: HeatmapChart,
    fill_color: Color,
    eff_r: float,
) -> Style:
    """Construct rectangle Style for a matrix cell."""
    if chart.cell_line_style is not None:
        line_s = chart.cell_line_style
        line_col = line_s.shape_line_color or line_s.line_color or (203, 213, 225, 1.0)
        line_w = line_s.shape_line_width if line_s.shape_line_width is not None else (line_s.line_width or 0.8)
        return Style(
            shape_fill_color=fill_color,
            shape_line_color=line_col,
            shape_line_width=line_w,
            shape_r=eff_r,
        )
    return Style(
        shape_fill_color=fill_color,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
        shape_r=eff_r,
    )


def _draw_cell_label(
    chart: HeatmapChart,
    cell_override: Cell | None,
    val: float | None,
    bg_color: Color,
    col_cx: float,
    row_cy: float,
) -> None:
    """Render formatted value or custom text inside a single matrix cell."""
    has_custom_lbl = cell_override is not None and bool(cell_override.label)
    if chart.value_text_style is None and not has_custom_lbl:
        return

    if has_custom_lbl and cell_override is not None:
        lbl_text = cell_override.label
    elif val is not None:
        lbl_text = format_heatmap_value(val, chart.value_format)
    else:
        lbl_text = ""

    if not lbl_text:
        return

    base_t_style = chart.value_text_style or chart.axis_text_style or Style(text_size=9.5)
    t_style = ensure_text_style(base_t_style, halign="center", valign="center")
    if chart.auto_contrast_text:
        contrast_c = ColorUtils.get_contrast_text_color(bg_color)
        t_style = t_style.patch(text_color=contrast_c)
    canvas_text(xy=(col_cx, row_cy), text=lbl_text, style=t_style)


def _resolve_cell_value_and_ratio(
    row: Row | None,
    cell_override: Cell | None,
    c_idx: int,
    num_cols: int,
) -> tuple[bool, float | None, float]:
    """Determine (is_visible, cell_value, local_ratio) for a single matrix cell."""
    if cell_override is not None:
        visible = cell_override.show and (cell_override.value is not None or bool(cell_override.label))
        return (visible, cell_override.value, 1.0 if visible else 0.0)

    row_ratio = clamp_ratio(row.draw_ratio) if row is not None else 1.0
    val = row.values[c_idx] if (row is not None and row.show and row_ratio > 0.0 and c_idx < len(row.values)) else None
    if val is None:
        return (False, None, 0.0)

    row_dir = row.draw_direction if row is not None else "left_to_right"
    if row_ratio < 1.0 and row_dir == "left_to_right":
        local_r = clamp_ratio(row_ratio * num_cols - c_idx)
        return (local_r > 0.0, val, local_r)
    return (True, val, row_ratio)


def _render_single_cell(
    chart: HeatmapChart,
    row: Row | None,
    cell_override: Cell | None,
    c_idx: int,
    num_cols: int,
    col_cx: float,
    row_cy: float,
    cell_w: float,
    cell_h: float,
    eff_r: float,
    eff_min: float,
    span: float,
    stops: list[Color],
) -> None:
    """Resolve and draw a single matrix cell rectangle and its text label."""
    visible, val, local_ratio = _resolve_cell_value_and_ratio(row, cell_override, c_idx, num_cols)
    if not visible:
        return

    row_dir = row.draw_direction if row is not None else "left_to_right"
    if cell_override is not None and cell_override.style is not None:
        c_style = ensure_shape_style(cell_override.style).patch(shape_r=eff_r)
        bg_color = extract_heatmap_color(c_style)
    else:
        norm_t = clamp_ratio(((val if val is not None else eff_min) - eff_min) / span)
        if row_dir == "bottom_to_top" and local_ratio < 1.0:
            norm_t *= local_ratio
        bg_color = interpolate_color_stops(stops, norm_t)
        c_style = _build_cell_shape_style(chart, bg_color, eff_r)

    is_partial_horiz = row_dir == "left_to_right" and local_ratio < 1.0
    draw_w = cell_w * local_ratio if is_partial_horiz else cell_w
    draw_cx = col_cx - (cell_w - draw_w) / 2.0 if is_partial_horiz else col_cx
    canvas_rectangle(xy=(draw_cx, row_cy), width=max(0.1, draw_w), height=cell_h, style=c_style)

    if local_ratio >= 0.6:
        _draw_cell_label(chart, cell_override, val, bg_color, col_cx, row_cy)


def _render_cells(
    chart: HeatmapChart,
    plot_bounds: tuple[float, float, float, float],
    num_rows: int,
    num_cols: int,
    eff_min: float,
    eff_max: float,
) -> None:
    """Render all visible matrix cells and in-cell value annotations."""
    plot_min_x, plot_min_y, plot_max_x, plot_max_y = plot_bounds
    slot_w = (plot_max_x - plot_min_x) / num_cols
    slot_h = (plot_max_y - plot_min_y) / num_rows
    cell_w = max(0.3, slot_w - chart.cell_gap)
    cell_h = max(0.3, slot_h - chart.cell_gap)
    eff_r = min(chart.cell_r, cell_w * 0.45, cell_h * 0.45)

    stops = chart.color_stops
    span = max(1e-9, eff_max - eff_min)

    for r_idx in range(num_rows):
        row = chart._rows[r_idx] if r_idx < len(chart._rows) else None
        row_cy = (
            plot_max_y - (r_idx + 0.5) * slot_h
            if chart.y_origin == "top"
            else plot_min_y + (r_idx + 0.5) * slot_h
        )
        for c_idx in range(num_cols):
            col_cx = plot_min_x + (c_idx + 0.5) * slot_w
            _render_single_cell(
                chart=chart,
                row=row,
                cell_override=chart._cells.get((c_idx, r_idx)),
                c_idx=c_idx,
                num_cols=num_cols,
                col_cx=col_cx,
                row_cy=row_cy,
                cell_w=cell_w,
                cell_h=cell_h,
                eff_r=eff_r,
                eff_min=eff_min,
                span=span,
                stops=stops,
            )


def _render_axes_and_labels(
    chart: HeatmapChart,
    plot_bounds: tuple[float, float, float, float],
    num_rows: int,
    num_cols: int,
    x_labels: list[str],
    y_labels: list[str],
) -> None:
    """Render outer matrix frame and X/Y category labels."""
    plot_min_x, plot_min_y, plot_max_x, plot_max_y = plot_bounds
    plot_w = plot_max_x - plot_min_x
    plot_h = plot_max_y - plot_min_y

    if chart.axis_line_style is not None:
        line_s = ensure_line_style(chart.axis_line_style)
        canvas_line(xy1=(plot_min_x, plot_min_y), xy2=(plot_max_x, plot_min_y), style=line_s)
        canvas_line(xy1=(plot_min_x, plot_max_y), xy2=(plot_max_x, plot_max_y), style=line_s)
        canvas_line(xy1=(plot_min_x, plot_min_y), xy2=(plot_min_x, plot_max_y), style=line_s)
        canvas_line(xy1=(plot_max_x, plot_min_y), xy2=(plot_max_x, plot_max_y), style=line_s)

    if chart.axis_text_style is None:
        return

    if num_rows > 0:
        slot_h = plot_h / num_rows
        y_text_style = ensure_text_style(chart.axis_text_style, halign="right", valign="center")
        for r_idx, y_lbl in enumerate(y_labels):
            if y_lbl:
                row_cy = (
                    plot_max_y - (r_idx + 0.5) * slot_h
                    if chart.y_origin == "top"
                    else plot_min_y + (r_idx + 0.5) * slot_h
                )
                canvas_text(xy=(plot_min_x - 1.2, row_cy), text=y_lbl, style=y_text_style)

    if num_cols > 0:
        slot_w = plot_w / num_cols
        is_top = chart.x_label_position == "top"
        x_text_style = ensure_text_style(
            chart.axis_text_style,
            halign="center",
            valign="bottom" if is_top else "top",
        )
        lbl_y = plot_max_y + 1.0 if is_top else plot_min_y - 1.2
        for c_idx, x_lbl in enumerate(x_labels):
            if x_lbl:
                canvas_text(xy=(plot_min_x + (c_idx + 0.5) * slot_w, lbl_y), text=x_lbl, style=x_text_style)


def draw_heatmap_chart(chart: HeatmapChart, xy: tuple[float, float]) -> None:
    """Render a complete 2D matrix heatmap chart onto the canvas.

    Args:
        chart: HeatmapChart container instance.
        xy: Base canvas coordinate (x, y) corresponding to bottom-left corner.
    """
    bx, by = float(xy[0]), float(xy[1])
    cw, ch = chart.width, chart.height

    # 1. Background card
    if chart.background_style is not None:
        canvas_rectangle(
            xy=(bx + cw / 2.0, by + ch / 2.0),
            width=cw,
            height=ch,
            style=ensure_shape_style(chart.background_style),
        )

    # 2. Title
    if chart.title and chart.title_style is not None:
        title_y = by + ch - 2.6
        title_s = ensure_text_style(chart.title_style, halign="center", valign="center")
        canvas_text(xy=(bx + cw / 2.0, title_y), text=chart.title, style=title_s)

    # 3. Matrix dimensions & plot bounds
    num_rows, num_cols, x_labels, y_labels = _compute_matrix_dimensions(chart)
    plot_bounds = _compute_plot_bounds(chart, bx, by, x_labels, y_labels)

    if num_rows > 0 and num_cols > 0:
        eff_min, eff_max = chart._get_effective_range()
        _render_cells(chart, plot_bounds, num_rows, num_cols, eff_min, eff_max)

    _render_axes_and_labels(chart, plot_bounds, num_rows, num_cols, x_labels, y_labels)
