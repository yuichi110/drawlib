# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared models, strict ISO date/datetime parsers, and layout helpers for Calendar SmartArts."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from drawlib._core.l2_types import Coordinate  # noqa: TC001
from drawlib._core.l3_colors import BaseColors
from drawlib._core.l3_styles import Style  # noqa: TC001
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

WEEKDAYS_SUN_EN = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
WEEKDAYS_SUN_JA = ("日", "月", "火", "水", "木", "金", "土")

MONTH_NAMES_EN = (
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


class CalendarItem(BaseModel):
    """Mutable item model for an event block or all-day spanning bar on a Calendar.

    Attributes:
        start: Start date ("YYYY-MM-DD") or datetime ("YYYY-MM-DD HH:MM").
        end: Optional end date ("YYYY-MM-DD") or datetime ("YYYY-MM-DD HH:MM").
            Defaults to start when None for single-day all-day events.
        text: Primary event title or label displayed inside the frame.
        description: Optional secondary subtitle or time/detail note.
        all_day: Optional explicit override to force rendering in the All-Day ("全日") field.
            When None, inferred automatically (True if start/end are "YYYY-MM-DD", False if "YYYY-MM-DD HH:MM").
        span_mode: How multi-day timed events ("2026-10-10 09:00" to "2026-10-13 15:00") are rendered in WeekCalendar:
            - "columns" (default): Fills 10th (09:00..end), 11th-12th (start..end), 13th (start..15:00).
            - "box": Draws a single unified rectangle spanning across columns 10th..13th and hours 09:00..15:00.
            - "all_day": Renders as an X-axis bar in the top All-Day field.
        style: Style for the event box/banner container.
        text_style: Text style for the primary event label.
        description_style: Optional text style for the secondary description.
        show: Whether to render this event while preserving calendar grid geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    start: str
    end: str | None = None
    text: str = ""
    description: str = ""
    all_day: bool | None = None
    span_mode: Literal["columns", "box", "all_day"] = "columns"
    style: Style
    text_style: Style
    description_style: Style | None = None
    show: bool = True


def parse_iso_date_strict(value: str, param_name: str = "date") -> date:
    """Parse a strict 'YYYY-MM-DD' string into a datetime.date object.

    Raises:
        ValueError: If value does not match 'YYYY-MM-DD' or is an invalid calendar date.
    """
    if not isinstance(value, str) or not _DATE_RE.match(value):
        raise ValueError(
            f"Invalid ISO date format for '{param_name}': '{value}'. Expected 'YYYY-MM-DD'."
        )
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid calendar date for '{param_name}': '{value}' ({exc})."
        ) from exc


def parse_iso_date_or_datetime(
    value: str,
    param_name: str = "start",
) -> tuple[date, float | None]:
    """Parse a strict 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM' string.

    Returns:
        tuple[date, float | None]: Parsed `(date_obj, fractional_hour_or_none)`.

    Raises:
        ValueError: If value does not strictly match 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'.
    """
    if not isinstance(value, str):
        raise ValueError(
            f"Invalid ISO format for '{param_name}': '{value}'. "
            "Expected 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'."
        )
    if _DATE_RE.match(value):
        return parse_iso_date_strict(value, param_name=param_name), None
    if _DATETIME_RE.match(value):
        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M")  # noqa: DTZ007
        except ValueError as exc:
            raise ValueError(
                f"Invalid calendar datetime for '{param_name}': '{value}' ({exc})."
            ) from exc
        return dt.date(), float(dt.hour) + float(dt.minute) / 60.0
    raise ValueError(
        f"Invalid ISO format for '{param_name}': '{value}'. "
        "Expected 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'."
    )


def resolve_item_span(
    item: CalendarItem,
) -> tuple[date, date, float | None, float | None, bool]:
    """Validate and resolve a CalendarItem's start/end dates, hours, and all_day flag.

    Returns:
        tuple[date, date, float | None, float | None, bool]:
        `(start_date, end_date, start_hour, end_hour, is_all_day)`.
    """
    s_date, s_hour = parse_iso_date_or_datetime(item.start, param_name="start")
    if item.end is None:
        e_date = s_date
        e_hour = (s_hour + 1.0) if s_hour is not None else None
    else:
        e_date, e_hour = parse_iso_date_or_datetime(item.end, param_name="end")

    if e_date < s_date:
        raise ValueError(
            f"Event 'end' date ({item.end}) must not be earlier than 'start' date ({item.start})."
        )
    if s_date == e_date and s_hour is not None and e_hour is not None and e_hour <= s_hour:
        raise ValueError(
            f"Event 'end' time ({item.end}) must be later than 'start' time ({item.start})."
        )

    if item.all_day is not None:
        is_all_day = bool(item.all_day)
    elif item.span_mode == "all_day":
        is_all_day = True
    else:
        is_all_day = s_hour is None and e_hour is None

    return s_date, e_date, s_hour, e_hour, is_all_day


def validate_hour_range(start_hour: int, end_hour: int, hour_step: int) -> None:
    """Validate start_hour, end_hour, and hour_step for time-grid calendars."""
    if not (0 <= start_hour < end_hour <= 24):
        raise ValueError(
            f"Invalid hour range: start_hour={start_hour}, end_hour={end_hour}. "
            "Must satisfy 0 <= start_hour < end_hour <= 24."
        )
    if hour_step <= 0:
        raise ValueError("hour_step must be a positive integer.")


def resolve_box_origin(
    xy: Coordinate,
    width: float,
    height: float,
    align: Literal["bottom_left", "center", "top_left"],
) -> tuple[float, float]:
    """Compute bottom-left (x0, y0) of a bounding box given anchor xy and align."""
    x, y = float(xy[0]), float(xy[1])
    if align == "center":
        return x - width / 2.0, y - height / 2.0
    if align == "top_left":
        return x, y - height
    return x, y


def pack_closed_intervals(intervals: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Assign 0-based lane indices to inclusive integer intervals [start, end] greedily."""
    if not intervals:
        return [], 0
    lane_available: list[list[tuple[int, int]]] = []
    assignments: list[int] = []
    for s_val, e_val in intervals:
        chosen = -1
        for l_idx, occupied in enumerate(lane_available):
            if all(e_val < occ_s or s_val > occ_e for occ_s, occ_e in occupied):
                chosen = l_idx
                occupied.append((s_val, e_val))
                break
        if chosen == -1:
            chosen = len(lane_available)
            lane_available.append([(s_val, e_val)])
        assignments.append(chosen)
    return assignments, len(lane_available)


def pack_half_open_intervals(
    intervals: list[tuple[float, float]],
) -> tuple[list[int], list[int]]:
    """Assign 0-based parallel lane indices and cluster lane counts for [start, end) intervals."""
    n = len(intervals)
    if n == 0:
        return [], []

    order = sorted(range(n), key=lambda idx: (intervals[idx][0], intervals[idx][1]))
    lanes: list[float] = []
    lane_of = [0] * n
    cluster_id_of = [0] * n
    cluster_max_lane: dict[int, int] = {}

    current_cluster = -1
    cluster_end = -1.0

    for idx in order:
        s_val, e_val = intervals[idx]
        if s_val >= cluster_end - 1e-6:
            current_cluster += 1
            lanes = [e_val]
            lane_of[idx] = 0
            cluster_id_of[idx] = current_cluster
            cluster_max_lane[current_cluster] = 1
            cluster_end = e_val
            continue

        placed = False
        for l_idx, l_end in enumerate(lanes):
            if s_val >= l_end - 1e-6:
                lanes[l_idx] = e_val
                lane_of[idx] = l_idx
                placed = True
                break
        if not placed:
            lane_of[idx] = len(lanes)
            lanes.append(e_val)

        cluster_id_of[idx] = current_cluster
        cluster_max_lane[current_cluster] = max(cluster_max_lane[current_cluster], len(lanes))
        cluster_end = max(cluster_end, e_val)

    total_lanes_of = [cluster_max_lane[cluster_id_of[i]] for i in range(n)]
    return lane_of, total_lanes_of


def draw_event_card(  # noqa: PLR0913
    *,
    cx: float,
    cy: float,
    width: float,
    height: float,
    text: str,
    description: str,
    style: Style,
    text_style: Style,
    description_style: Style | None,
    corner_r: float = 0.55,
) -> None:
    """Draw a rounded event bar or card with centered title and optional subtitle."""
    r_val = style.shape_r if style.shape_r is not None else min(corner_r, height * 0.28)
    box_style = style.patch(shape_r=r_val)
    canvas_rectangle(xy=(cx, cy), width=width, height=height, style=box_style)

    has_text = bool(text.strip())
    has_desc = bool(description.strip())
    if has_text and has_desc:
        d_style = (description_style if description_style is not None else text_style.patch(alpha=0.88)).patch(
            halign="center",
            valign="center",
        )
        t_style = text_style.patch(halign="center", valign="center")
        dy_top = min(height * 0.16, 1.8)
        dy_bot = min(height * 0.22, 2.2)
        canvas_text(xy=(cx, cy + dy_top), text=text, style=t_style)
        canvas_text(xy=(cx, cy - dy_bot), text=description, style=d_style)
    elif has_text:
        t_style = text_style.patch(halign="center", valign="center")
        canvas_text(xy=(cx, cy), text=text, style=t_style)
    elif has_desc:
        d_style = (description_style if description_style is not None else text_style).patch(
            halign="center",
            valign="center",
        )
        canvas_text(xy=(cx, cy), text=description, style=d_style)


def derive_default_event_styles(
    header_style: Style,
    header_text_style: Style,
    event_style: Style | None,
    event_text_style: Style | None,
) -> tuple[Style, Style]:
    """Resolve fallback event_style and event_text_style from header styles when omitted."""
    resolved_ev_style = (
        event_style
        if event_style is not None
        else header_style.patch(shape_r=0.55)
    )
    resolved_ev_text = (
        event_text_style
        if event_text_style is not None
        else header_text_style.patch(text_size=9.5)
    )
    return resolved_ev_style, resolved_ev_text


def make_subtle_fill_style(base_cell_style: Style, rgb: tuple[int, int, int]) -> Style:
    """Create a borderless background fill style from base_cell_style."""
    return base_cell_style.patch(
        shape_fill_color=rgb,
        shape_line_width=0,
        shape_r=0,
    )


def make_outer_frame_style(border_style: Style) -> Style:
    """Create a transparent outer frame rectangle style from a line border_style."""
    line_col = border_style.line_color if border_style.line_color is not None else (180, 188, 200)
    line_w = border_style.line_width if border_style.line_width is not None else 1.0
    return Style(
        shape_fill_color=BaseColors.Transparent,
        shape_line_color=line_col,
        shape_line_width=max(1.0, float(line_w)),
        shape_r=0,
        supports={"shape"},
    )
