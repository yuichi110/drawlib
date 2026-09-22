# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for GanttChart."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType
from drawlib._charts.bar_chart._series import DEFAULT_CHART_PALETTE
from drawlib._charts.gantt_chart._item import (
    GanttDependency,
    GanttMarker,
    GanttMilestone,
    GanttSection,
    GanttTask,
)
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib.lines import line as canvas_line
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.shapes import rhombus as canvas_rhombus
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._charts.gantt_chart._chart import GanttChart

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)
_DEFAULT_MUTED_TEXT = (100, 116, 139, 1.0)
_DEFAULT_HEADER_BG = (241, 245, 249, 1.0)
_DEFAULT_HEADER_BORDER = (203, 213, 225, 1.0)
_DEFAULT_GRID_COLOR = (226, 232, 240, 1.0)
_DEFAULT_ZEBRA_BG = (248, 250, 252, 1.0)
_DEFAULT_SECTION_BG = (226, 232, 240, 0.7)
_DEFAULT_MILESTONE_COLOR = (245, 158, 11, 1.0)
_DEFAULT_MARKER_COLOR = (239, 68, 68, 1.0)


def _with_alpha(color: ColorType, alpha: float) -> tuple[int, int, int, float]:
    """Return an RGBA color tuple with updated alpha ratio."""
    return (int(color[0]), int(color[1]), int(color[2]), float(alpha))


def _resolve_time(chart: GanttChart, val: str | float, is_end: bool = False) -> float:
    """Translate column label or float into timeline unit offset."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        if val in chart.columns:
            idx = chart.columns.index(val)
            return float(idx + 1.0) if is_end else float(idx)
        raise ValueError(f"Time column '{val}' not found in GanttChart columns: {chart.columns}")
    raise TypeError(f"Time specification must be str or float, got {type(val).__name__}")


def _resolve_point_time(chart: GanttChart, val: str | float) -> float:
    """Translate column label or float into a discrete point in time (column midpoint)."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        if val in chart.columns:
            idx = chart.columns.index(val)
            return float(idx + 0.5)
        raise ValueError(f"Time column '{val}' not found in GanttChart columns: {chart.columns}")
    raise TypeError(f"Time specification must be str or float, got {type(val).__name__}")


def _draw_header(
    chart: GanttChart,
    header_bounds: tuple[float, float, float, float],
    x_tl_start: float,
    col_w: float,
) -> None:
    """Render the top timeline header and column dividers."""
    left_x, right_x, bottom_y, top_y = header_bounds
    header_w = right_x - left_x
    header_h = top_y - bottom_y
    header_cy = (top_y + bottom_y) / 2.0

    # Header full background
    bg_style = chart.header_style or Style(
        fill_color=_DEFAULT_HEADER_BG,
        line_color=_DEFAULT_HEADER_BORDER,
        line_width=1.0,
    )
    canvas_rectangle(
        xy=((left_x + right_x) / 2.0, header_cy),
        width=header_w,
        height=header_h,
        style=bg_style,
    )

    # Label column header
    canvas_text(
        xy=(left_x + 1.5, header_cy),
        text="Task / Phase",
        style=Style(
            text_size=10.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_MUTED_TEXT,
            text_halign="left",
            text_valign="center",
        ),
    )

    # Column names
    col_label_style = Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    for i, col_name in enumerate(chart.columns):
        col_cx = x_tl_start + (i + 0.5) * col_w
        canvas_text(xy=(col_cx, header_cy), text=col_name, style=col_label_style)

        # Subtle vertical separator between column headers
        if i > 0:
            canvas_line(
                xy1=(x_tl_start + i * col_w, bottom_y),
                xy2=(x_tl_start + i * col_w, top_y),
                style=Style(line_color=_DEFAULT_HEADER_BORDER, line_width=0.8),
            )


def _draw_rows_and_items(
    chart: GanttChart,
    left_x: float,
    right_x: float,
    rows_top: float,
    rows_bottom: float,
    x_tl_start: float,
    col_w: float,
) -> None:
    """Render zebra rows, vertical grid, tasks, sections, and milestones."""
    full_w = right_x - left_x
    num_cols = len(chart.columns)

    # 1. Vertical timeline gridlines across rows area
    if chart.show_vertical_grid:
        v_grid_style = chart.grid_style or Style(
            line_color=_DEFAULT_GRID_COLOR,
            line_width=0.8,
            line_style="dotted",
        )
        for i in range(num_cols + 1):
            gx = x_tl_start + i * col_w
            canvas_line(xy1=(gx, rows_top), xy2=(gx, rows_bottom), style=v_grid_style)

    # 2. Rows
    for k, item in enumerate(chart.items):
        row_top = rows_top - k * chart.row_height
        row_bottom = row_top - chart.row_height
        row_cy = (row_top + row_bottom) / 2.0

        # Zebra striping
        if chart.show_zebra and (k % 2 == 1) and not isinstance(item, GanttSection):
            canvas_rectangle(
                xy=((left_x + right_x) / 2.0, row_cy),
                width=full_w,
                height=chart.row_height,
                style=Style(fill_color=_DEFAULT_ZEBRA_BG, line_width=0),
            )

        # Row bottom hairline
        canvas_line(
            xy1=(left_x, row_bottom),
            xy2=(right_x, row_bottom),
            style=Style(line_color=_DEFAULT_GRID_COLOR, line_width=0.5),
        )

        # Cache row_y
        if isinstance(item, GanttTask):
            item._cached_row_y = row_cy
            _draw_task_row(chart, item, left_x, row_cy, x_tl_start, col_w, k)
        elif isinstance(item, GanttSection):
            item._cached_row_y = row_cy
            _draw_section_row(chart, item, left_x, right_x, row_cy)
        elif isinstance(item, GanttMilestone):
            item._cached_row_y = row_cy
            _draw_milestone_row(chart, item, left_x, row_cy, x_tl_start, col_w)


def _draw_section_row(
    chart: GanttChart,
    section: GanttSection,
    left_x: float,
    right_x: float,
    row_cy: float,
) -> None:
    """Render full-width section header banner."""
    full_w = right_x - left_x
    sec_style = section.style or Style(
        fill_color=_DEFAULT_SECTION_BG,
        line_width=0,
    )
    canvas_rectangle(
        xy=((left_x + right_x) / 2.0, row_cy),
        width=full_w,
        height=chart.row_height,
        style=sec_style,
    )
    canvas_text(
        xy=(left_x + 1.5, row_cy),
        text=section.name,
        style=Style(
            text_size=10.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="left",
            text_valign="center",
        ),
    )


def _draw_task_row(
    chart: GanttChart,
    task: GanttTask,
    left_x: float,
    row_cy: float,
    x_tl_start: float,
    col_w: float,
    idx: int,
) -> None:
    """Render single task label, scheduled bar, and progress."""
    # Label text
    canvas_text(
        xy=(left_x + 1.5, row_cy),
        text=task.name,
        style=Style(
            text_size=9.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="left",
            text_valign="center",
        ),
    )

    start_t = _resolve_time(chart, task.start, is_end=False)
    end_t = _resolve_time(chart, task.end, is_end=True)
    if end_t <= start_t:
        end_t = start_t + 0.1

    bx1 = x_tl_start + start_t * col_w
    bx2 = x_tl_start + end_t * col_w
    task._cached_start_x = bx1
    task._cached_end_x = bx2

    bar_w = max(0.5, bx2 - bx1)
    bar_h = chart.row_height * 0.58
    bar_cx = (bx1 + bx2) / 2.0
    color = task.color or DEFAULT_CHART_PALETTE[idx % len(DEFAULT_CHART_PALETTE)]

    if task.progress <= 0.0:
        # Solid scheduled bar
        bar_style = task.style or Style(
            fill_color=color,
            line_color=_with_alpha(color, 0.9),
            line_width=0.8,
        )
        canvas_rectangle(
            xy=(bar_cx, row_cy),
            width=bar_w,
            height=bar_h,
            r=chart.bar_radius,
            style=bar_style,
        )
    else:
        # Background bar (remaining/total span)
        bg_style = Style(
            fill_color=_with_alpha(color, 0.28),
            line_color=_with_alpha(color, 0.5),
            line_width=0.8,
        )
        canvas_rectangle(
            xy=(bar_cx, row_cy),
            width=bar_w,
            height=bar_h,
            r=chart.bar_radius,
            style=bg_style,
        )

        # Progress bar (completed portion)
        prog_w = max(0.2, bar_w * task.progress)
        prog_cx = bx1 + prog_w / 2.0
        prog_style = task.style or Style(
            fill_color=color,
            line_color=_with_alpha(color, 0.9),
            line_width=0.8,
        )
        canvas_rectangle(
            xy=(prog_cx, row_cy),
            width=prog_w,
            height=bar_h,
            r=chart.bar_radius,
            style=prog_style,
        )

        # Optional percentage text
        if task.show_progress_text:
            pct_label = f"{int(round(task.progress * 100))}%"
            if prog_w >= 4.0:
                canvas_text(
                    xy=(prog_cx, row_cy),
                    text=pct_label,
                    style=Style(
                        text_size=8.0,
                        text_font=Font.SANSSERIF_BOLD,
                        text_color=(255, 255, 255, 1.0),
                        text_halign="center",
                        text_valign="center",
                    ),
                )
            else:
                canvas_text(
                    xy=(bx2 + 1.0, row_cy),
                    text=pct_label,
                    style=Style(
                        text_size=8.0,
                        text_font=Font.SANSSERIF_BOLD,
                        text_color=color,
                        text_halign="left",
                        text_valign="center",
                    ),
                )


def _draw_milestone_row(
    chart: GanttChart,
    milestone: GanttMilestone,
    left_x: float,
    row_cy: float,
    x_tl_start: float,
    col_w: float,
) -> None:
    """Render milestone label and diamond marker."""
    canvas_text(
        xy=(left_x + 1.5, row_cy),
        text=milestone.name,
        style=Style(
            text_size=9.5,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="left",
            text_valign="center",
        ),
    )

    at_t = _resolve_point_time(chart, milestone.at)
    mx = x_tl_start + at_t * col_w
    milestone._cached_at_x = mx

    color = milestone.color or _DEFAULT_MILESTONE_COLOR
    d_size = chart.row_height * 0.65
    m_style = milestone.style or Style(
        fill_color=color,
        line_color=(255, 255, 255, 1.0),
        line_width=1.0,
    )
    canvas_rhombus(xy=(mx, row_cy), width=d_size, height=d_size, style=m_style)


def _avoid_grid(
    x: float,
    grid_lines: list[float],
    min_dist: float = 1.0,
    prefer_dir: float = -1.0,
) -> float:
    """Shift an x coordinate away from vertical gridlines if too close."""
    for gx in grid_lines:
        dist = x - gx
        if abs(dist) < min_dist:
            if prefer_dir >= 0:
                return gx + min_dist
            return gx - min_dist
    return x


def _draw_dependencies(chart: GanttChart, x_tl_start: float, col_w: float) -> None:
    """Render right-angled dependency arrows linking tasks."""
    grid_lines = [x_tl_start + i * col_w for i in range(len(chart.columns) + 1)]
    min_entry = 2.8  # Minimum lead-in horizontal length for arrow ("---->")
    min_exit = 1.5

    for dep in chart.dependencies:
        x1 = dep.from_task._cached_end_x
        y1 = dep.from_task._cached_row_y
        x2 = dep.to_task._cached_start_x
        y2 = dep.to_task._cached_row_y

        if x1 <= 0 or x2 <= 0:
            continue

        color = dep.color or _DEFAULT_MUTED_TEXT
        style = dep.style or Style(
            line_color=color,
            line_width=1.2,
        )

        if x2 >= x1 + (min_exit + min_entry):
            # Forward dependency with sufficient horizontal clearance
            mid_x = (x1 + x2) / 2.0
            # If mid_x lands too close to a vertical gridline, shift it.
            # Prefer shifting left (earlier) so the horizontal lead-in into x2 stays long (---->).
            for gx in grid_lines:
                if abs(mid_x - gx) < 1.0:
                    left_cand = gx - 1.2
                    right_cand = gx + 1.2
                    if left_cand >= x1 + min_exit:
                        mid_x = left_cand
                    elif right_cand <= x2 - min_entry:
                        mid_x = right_cand
                    break

            canvas_line(xy1=(x1, y1), xy2=(mid_x, y1), style=style)
            canvas_line(xy1=(mid_x, y1), xy2=(mid_x, y2), style=style)
            canvas_line(xy1=(mid_x, y2), xy2=(x2, y2), arrowhead="->", style=style)
        else:
            # Overlapping, narrow gap, or backward dependency: route cleanly around
            mid_y = (y1 + y2) / 2.0
            p_right = x1 + 1.8
            p_left = x2 - min_entry

            # Avoid gridlines for both vertical routing paths
            p_right = _avoid_grid(p_right, grid_lines, min_dist=1.0, prefer_dir=1.0)
            p_left = _avoid_grid(p_left, grid_lines, min_dist=1.0, prefer_dir=-1.0)
            if x2 - p_left < min_entry:
                p_left = x2 - min_entry

            canvas_line(xy1=(x1, y1), xy2=(p_right, y1), style=style)
            canvas_line(xy1=(p_right, y1), xy2=(p_right, mid_y), style=style)
            canvas_line(xy1=(p_right, mid_y), xy2=(p_left, mid_y), style=style)
            canvas_line(xy1=(p_left, mid_y), xy2=(p_left, y2), style=style)
            canvas_line(xy1=(p_left, y2), xy2=(x2, y2), arrowhead="->", style=style)


def _draw_markers(
    chart: GanttChart,
    rows_top: float,
    rows_bottom: float,
    x_tl_start: float,
    col_w: float,
) -> None:
    """Render vertical reference lines and header badges."""
    for mark in chart.markers:
        at_t = _resolve_point_time(chart, mark.at)
        mx = x_tl_start + at_t * col_w
        color = mark.color or _DEFAULT_MARKER_COLOR
        style = mark.style or Style(
            line_color=color,
            line_width=1.5,
            line_style="dashed",
        )

        canvas_line(xy1=(mx, rows_top), xy2=(mx, rows_bottom), style=style)

        if mark.label:
            tag_w = max(7.0, len(mark.label) * 1.5)
            tag_h = 2.4
            tag_y = rows_top - 1.4
            canvas_rectangle(
                xy=(mx, tag_y),
                width=tag_w,
                height=tag_h,
                r=0.6,
                style=Style(fill_color=color, line_width=0),
            )
            canvas_text(
                xy=(mx, tag_y),
                text=mark.label,
                style=Style(
                    text_size=8.0,
                    text_font=Font.SANSSERIF_BOLD,
                    text_color=(255, 255, 255, 1.0),
                    text_halign="center",
                    text_valign="center",
                ),
            )


def draw_gantt_chart(chart: GanttChart, xy: tuple[float, float]) -> None:
    """Render a complete GanttChart onto the canvas."""
    min_x, min_y = xy
    chart_w, chart_h = chart.get_size()
    max_x = min_x + chart_w
    max_y = min_y + chart_h

    pad_x = 2.0
    pad_y = 2.0

    # Title
    content_top = max_y - pad_y
    if chart.title:
        t_style = chart.title_style or Style(
            text_size=12.0,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=((min_x + max_x) / 2.0, max_y - 3.2), text=chart.title, style=t_style)
        content_top = max_y - 6.5

    header_top = content_top
    header_bottom = header_top - chart.header_height
    num_items = len(chart.items)
    rows_top = header_bottom
    rows_bottom = rows_top - num_items * chart.row_height

    left_x = min_x + pad_x
    right_x = max_x - pad_x
    x_tl_start = left_x + chart.label_width
    timeline_w = right_x - x_tl_start
    col_w = timeline_w / len(chart.columns)

    _draw_header(chart, (left_x, right_x, header_bottom, header_top), x_tl_start, col_w)
    _draw_rows_and_items(chart, left_x, right_x, rows_top, rows_bottom, x_tl_start, col_w)
    _draw_dependencies(chart, x_tl_start, col_w)
    _draw_markers(chart, rows_top, rows_bottom, x_tl_start, col_w)
