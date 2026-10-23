# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""WeekCalendar SmartArt implementation module."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Literal, Self

from drawlib._core.l1_core import validate_call
from drawlib._core.l2_types import Coordinate, PosFloat, PosInt  # noqa: TC001
from drawlib._core.l3_styles import Style  # noqa: TC001
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform
from drawlib._smartarts._calendar._models import (
    WEEKDAYS_SUN_EN,
    WEEKDAYS_SUN_JA,
    CalendarItem,
    _draw_calendar_title_bar,
    _draw_vertical_hour_grid,
    _resolve_default_event_styles,
    _resolve_weekday_text_style,
    draw_event_card,
    make_outer_frame_style,
    make_subtle_fill_style,
    pack_closed_intervals,
    pack_half_open_intervals,
    parse_iso_date_or_datetime,
    parse_iso_date_strict,
    resolve_box_origin,
    resolve_item_span,
    validate_hour_range,
)


class WeekCalendar:
    """SmartArt component for rendering multi-day time-grid calendars (7-day week, 5-day workweek, or custom range)."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        start_date: str = "2026-10-11",
        end_date: str | None = None,
        num_days: PosInt = 7,
        columns: list[str] | None = None,
        start_hour: int = 9,
        end_hour: int = 18,
        hour_step: PosInt = 1,
        show_all_day: bool | None = None,
        all_day_label: str | None = None,
        title: str | None = None,
        lang: Literal["en", "ja"] = "en",
        cell_style: Style,
        text_style: Style,
        header_style: Style,
        header_text_style: Style,
        border_style: Style,
        event_style: Style | None = None,
        event_text_style: Style | None = None,
        sunday_text_style: Style | None = None,
        saturday_text_style: Style | None = None,
        title_style: Style | None = None,
        title_text_style: Style | None = None,
    ) -> None:
        """Initialize WeekCalendar with explicit styles, date span, and hour range.

        Args:
            start_date: First displayed date in 'YYYY-MM-DD' format. Defaults to '2026-10-11'.
            end_date: Optional last displayed date in 'YYYY-MM-DD' format. Overrides `num_days` when set.
            num_days: Number of displayed day columns when `end_date` is None. Defaults to 7.
            columns: Optional custom column header labels. Must match the number of displayed days when set.
            start_hour: Start hour on the 24-hour vertical axis (0..23). Defaults to 9.
            end_hour: End hour on the 24-hour vertical axis (1..24). Defaults to 18.
            hour_step: Hour label interval on the vertical axis. Defaults to 1.
            show_all_day: Controls top All-Day field visibility. When None (default), automatically
                displays only if at least one all-day event is registered.
            all_day_label: Custom label for the All-Day gutter cell (defaults to 'All-day' or '全日').
            title: Custom title text in the top banner. When None, auto-generates the date range title.
                Pass '' to hide the title bar.
            lang: Label language ('en' or 'ja'). Defaults to 'en'.
            cell_style: Background style for the hourly time grid.
            text_style: Text style for time gutter labels.
            header_style: Background style for the day column headers.
            header_text_style: Text style for weekday column headers.
            border_style: Line style for grid borders.
            event_style: Default box style for events added via `add()`.
            event_text_style: Default text style for event titles.
            sunday_text_style: Optional override text style for Sunday column headers.
            saturday_text_style: Optional override text style for Saturday column headers.
            title_style: Optional background style for the top title bar (defaults to `header_style`).
            title_text_style: Optional text style for the top title bar (defaults to `header_text_style`).

        Raises:
            ValueError: If dates, hours, or column counts are invalid.
        """
        validate_hour_range(start_hour, end_hour, int(hour_step))
        self._start_date: date = parse_iso_date_strict(start_date, param_name="start_date")
        if end_date is not None:
            e_date = parse_iso_date_strict(end_date, param_name="end_date")
            if e_date < self._start_date:
                raise ValueError(f"end_date ({end_date}) must not be earlier than start_date ({start_date}).")
            resolved_days = (e_date - self._start_date).days + 1
        elif columns is not None and len(columns) > 0:
            resolved_days = len(columns)
        else:
            resolved_days = int(num_days)

        if columns is not None and len(columns) != resolved_days:
            raise ValueError(f"Length of 'columns' ({len(columns)}) must match displayed days ({resolved_days}).")

        self._num_days: int = resolved_days
        self._columns: list[str] | None = list(columns) if columns is not None else None
        self._start_hour: int = int(start_hour)
        self._end_hour: int = int(end_hour)
        self._hour_step: int = int(hour_step)
        self._show_all_day: bool | None = show_all_day
        self._all_day_label: str | None = all_day_label
        self._title: str | None = title
        self._lang: Literal["en", "ja"] = lang

        self._cell_style: Style = cell_style
        self._text_style: Style = text_style
        self._header_style: Style = header_style
        self._header_text_style: Style = header_text_style
        self._border_style: Style = border_style

        ev_st, ev_txt_st = _resolve_default_event_styles(
            header_style,
            header_text_style,
            event_style,
            event_text_style,
        )
        self._event_style: Style = ev_st
        self._event_text_style: Style = ev_txt_st
        self._sunday_text_style: Style | None = sunday_text_style
        self._saturday_text_style: Style | None = saturday_text_style
        self._title_style: Style = title_style if title_style is not None else header_style
        self._title_text_style: Style = title_text_style if title_text_style is not None else header_text_style
        self._items: list[CalendarItem] = []

    @property
    def items(self) -> list[CalendarItem]:
        """Return the registered calendar event items."""
        return self._items

    @validate_call
    def add(  # noqa: PLR0913
        self,
        start: str,
        end: str | None = None,
        text: str = "",
        *,
        description: str = "",
        all_day: bool | None = None,
        span_mode: Literal["columns", "box", "all_day"] = "columns",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register an all-day X-axis bar or a timed event on the week calendar.

        Args:
            start: Event start date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            end: Optional event end date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            text: Primary event title text. Defaults to ''.
            description: Optional secondary subtitle text. Defaults to ''.
            all_day: Optional explicit override to force rendering in the All-Day field.
            span_mode: Multi-day timed rendering mode ('columns', 'box', or 'all_day').
                Defaults to 'columns'.
            style: Custom box style for this event. Defaults to `event_style`.
            text_style: Custom text style for this event title. Defaults to `event_text_style`.
            description_style: Optional text style for `description`.
            show: Whether to render this event while preserving layout. Defaults to True.

        Returns:
            CalendarItem: The created mutable calendar item instance.
        """
        eff_style = style if style is not None else self._event_style
        eff_text_style = text_style if text_style is not None else self._event_text_style
        item = CalendarItem(
            start=start,
            end=end,
            text=text,
            description=description,
            all_day=all_day,
            span_mode=span_mode,
            style=eff_style,
            text_style=eff_text_style,
            description_style=description_style,
            show=show,
        )
        resolve_item_span(item)
        self._items.append(item)
        return item

    def _build_dates(self) -> list[date]:
        """Return the list of dates for each column."""
        return [self._start_date + timedelta(days=i) for i in range(self._num_days)]

    def _resolve_title_text(self, dates: list[date]) -> str:
        """Resolve top banner title text."""
        if self._title is not None:
            return self._title
        d0, d1 = dates[0], dates[-1]
        if self._lang == "ja":
            return f"{d0.year}年 {d0.month}/{d0.day} – {d1.month}/{d1.day}"
        return f"{d0.isoformat()} – {d1.isoformat()}"

    def _collect_all_day_lanes(
        self,
        dates: list[date],
    ) -> tuple[list[tuple[CalendarItem, int, int, bool, bool, int]], int]:
        """Collect all-day items (including show=False for layout stability) and pack lanes."""
        w_start, w_end = dates[0], dates[-1]
        entries: list[tuple[CalendarItem, int, int, bool, bool]] = []
        intervals: list[tuple[int, int]] = []

        for item in self._items:
            s_date, e_date, _, _, is_all_day = resolve_item_span(item)
            if not is_all_day:
                continue
            if e_date < w_start or s_date > w_end:
                continue
            c_start = (max(s_date, w_start) - w_start).days
            c_end = (min(e_date, w_end) - w_start).days
            entries.append((item, c_start, c_end, s_date < w_start, e_date > w_end))
            intervals.append((c_start, c_end))

        lanes, num_lanes = pack_closed_intervals(intervals)
        packed = [(item, cs, ce, cl, cr, l_idx) for (item, cs, ce, cl, cr), l_idx in zip(entries, lanes, strict=True)]
        return packed, num_lanes

    def _compute_geometry(  # noqa: PLR0913
        self,
        x0: float,
        y0: float,
        w: float,
        h: float,
        dates: list[date],
        all_day_lanes: int,
    ) -> tuple[float, float, float, float, float, float, float, float]:
        """Compute layout metrics for WeekCalendar."""
        title_str = self._resolve_title_text(dates)
        title_h = min(5.6, h * 0.10) if title_str else 0.0
        col_hdr_h = min(4.6, h * 0.085)

        has_all_day = self._show_all_day if self._show_all_day is not None else (all_day_lanes > 0)
        eff_lanes = max(1, all_day_lanes) if has_all_day else 0
        track_h = min(2.9, h * 0.052)
        all_day_h = (eff_lanes * (track_h + 0.5) + 0.9) if has_all_day else 0.0

        gutter_w = min(9.5, w * 0.11)
        body_w = max(1.0, w - gutter_w)
        col_w = body_w / self._num_days

        title_top = y0 + h
        col_hdr_top = title_top - title_h
        all_day_top = col_hdr_top - col_hdr_h
        grid_top = all_day_top - all_day_h
        return title_h, col_hdr_h, all_day_h, track_h, gutter_w, col_w, all_day_top, grid_top

    @validate_call
    def get_slot_xy(
        self,
        dt: str,
        xy: Coordinate,
        width: PosFloat = 100.0,
        height: PosFloat = 60.0,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> tuple[float, float]:
        """Return the canvas coordinate (cx, cy) for 'YYYY-MM-DD' (all-day) or 'YYYY-MM-DD HH:MM' (time slot).

        Args:
            dt: Target ISO date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            xy: Anchor coordinate (x, y) of the calendar bounding box.
            width: Unscaled width of the calendar. Defaults to 100.0.
            height: Unscaled height of the calendar. Defaults to 60.0.
            align: Anchor alignment of `xy` ('bottom_left', 'center', or 'top_left').
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            tuple[float, float]: Canvas coordinate `(cx, cy)` of the target slot.

        Raises:
            ValueError: If `dt` is outside the displayed date or hour range.
        """
        target_d, target_hr = parse_iso_date_or_datetime(dt, param_name="dt")
        dates = self._build_dates()
        if target_d < dates[0] or target_d > dates[-1]:
            raise ValueError(f"Date '{target_d}' is outside the displayed WeekCalendar range.")

        w = float(width) * float(scale)
        h = float(height) * float(scale)
        x0, y0 = resolve_box_origin(xy, w, h, align)
        _, all_day_lanes = self._collect_all_day_lanes(dates)
        _, _, all_day_h, _, gutter_w, col_w, all_day_top, grid_top = self._compute_geometry(
            x0,
            y0,
            w,
            h,
            dates,
            all_day_lanes,
        )
        col_idx = (target_d - dates[0]).days
        cx = x0 + gutter_w + (col_idx + 0.5) * col_w

        if target_hr is None:
            cy = (all_day_top - all_day_h / 2.0) if all_day_h > 0 else grid_top
            return (cx, cy)

        if not (self._start_hour <= target_hr <= self._end_hour):
            raise ValueError(f"Hour {target_hr} in '{dt}' is outside [{self._start_hour}, {self._end_hour}].")
        grid_h = max(1.0, grid_top - y0)
        ratio = (target_hr - self._start_hour) / (self._end_hour - self._start_hour)
        cy = grid_top - ratio * grid_h
        return (cx, cy)

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat = 100.0,
        height: PosFloat = 60.0,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self:
        """Render the week calendar onto the canvas.

        Args:
            xy: Anchor coordinate (x, y) of the calendar bounding box.
            width: Total width of the calendar. Defaults to 100.0.
            height: Total height of the calendar. Defaults to 60.0.
            align: Anchor alignment of `xy` ('bottom_left', 'center', or 'top_left').
                Defaults to 'bottom_left'.
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            Self: This WeekCalendar instance for method chaining.
        """
        total_w = float(width)
        total_h = float(height)
        x0, y0 = resolve_box_origin(xy, total_w, total_h, align)
        dates = self._build_dates()
        packed_all_day, all_day_lanes = self._collect_all_day_lanes(dates)
        (
            title_h,
            col_hdr_h,
            all_day_h,
            track_h,
            gutter_w,
            col_w,
            all_day_top,
            grid_top,
        ) = self._compute_geometry(x0, y0, total_w, total_h, dates, all_day_lanes)

        with transform(origin=xy, scale=scale):
            self._draw_headers_and_backgrounds(
                x0=x0,
                y0=y0,
                w=total_w,
                h=total_h,
                title_h=title_h,
                col_hdr_h=col_hdr_h,
                all_day_h=all_day_h,
                gutter_w=gutter_w,
                col_w=col_w,
                all_day_top=all_day_top,
                grid_top=grid_top,
                dates=dates,
            )
            self._draw_grid_and_hour_labels(
                x0=x0,
                y0=y0,
                w=total_w,
                h=total_h,
                title_h=title_h,
                all_day_h=all_day_h,
                gutter_w=gutter_w,
                col_w=col_w,
                all_day_top=all_day_top,
                grid_top=grid_top,
            )
            self._draw_all_day_events(
                x0=x0,
                gutter_w=gutter_w,
                col_w=col_w,
                all_day_top=all_day_top,
                all_day_h=all_day_h,
                track_h=track_h,
                packed_all_day=packed_all_day,
            )
            self._draw_timed_events(
                x0=x0,
                y0=y0,
                gutter_w=gutter_w,
                col_w=col_w,
                grid_top=grid_top,
                dates=dates,
            )

        return self

    def _draw_headers_and_backgrounds(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        title_h: float,
        col_hdr_h: float,
        all_day_h: float,
        gutter_w: float,
        col_w: float,
        all_day_top: float,
        grid_top: float,
        dates: list[date],
    ) -> None:
        """Render title bar, column headers, All-Day field background, and hourly grid background."""
        title_str = self._resolve_title_text(dates)
        _draw_calendar_title_bar(
            x0=x0,
            y0=y0,
            w=w,
            h=h,
            title_h=title_h,
            title_str=title_str,
            title_style=self._title_style,
            title_text_style=self._title_text_style,
        )

        col_hdr_cy = all_day_top + col_hdr_h / 2.0
        canvas_rectangle(
            xy=(x0 + w / 2.0, col_hdr_cy),
            width=w,
            height=col_hdr_h,
            style=self._header_style.patch(shape_r=0, shape_line_width=0),
        )
        wd_names = WEEKDAYS_SUN_JA if self._lang == "ja" else WEEKDAYS_SUN_EN
        for i, d in enumerate(dates):
            cx = x0 + gutter_w + (i + 0.5) * col_w
            sun_idx = (d.weekday() + 1) % 7
            if self._columns is not None:
                lbl = self._columns[i]
            elif self._lang == "ja":
                lbl = f"{d.month}/{d.day} ({wd_names[sun_idx]})"
            else:
                lbl = f"{wd_names[sun_idx]} {d.month}/{d.day}"

            st = _resolve_weekday_text_style(
                sun_idx,
                self._header_text_style,
                self._sunday_text_style,
                self._saturday_text_style,
            )
            canvas_text(xy=(cx, col_hdr_cy), text=lbl, style=st.patch(halign="center", valign="center"))

        if all_day_h > 0:
            ad_cy = all_day_top - all_day_h / 2.0
            canvas_rectangle(
                xy=(x0 + w / 2.0, ad_cy),
                width=w,
                height=all_day_h,
                style=make_subtle_fill_style(self._cell_style, (245, 248, 252)),
            )
            ad_lbl = (
                self._all_day_label
                if self._all_day_label is not None
                else ("全日" if self._lang == "ja" else "All-day")
            )
            canvas_text(
                xy=(x0 + gutter_w / 2.0, ad_cy),
                text=ad_lbl,
                style=self._header_text_style.patch(halign="center", valign="center"),
            )

        grid_h = max(1.0, grid_top - y0)
        canvas_rectangle(
            xy=(x0 + gutter_w / 2.0, y0 + grid_h / 2.0),
            width=gutter_w,
            height=grid_h,
            style=make_subtle_fill_style(self._cell_style, (250, 251, 253)),
        )
        body_w = w - gutter_w
        canvas_rectangle(
            xy=(x0 + gutter_w + body_w / 2.0, y0 + grid_h / 2.0),
            width=body_w,
            height=grid_h,
            style=self._cell_style.patch(shape_r=0, shape_line_width=0),
        )

    def _draw_grid_and_hour_labels(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        title_h: float,
        all_day_h: float,
        gutter_w: float,
        col_w: float,
        all_day_top: float,
        grid_top: float,
    ) -> None:
        """Render hour labels, horizontal hour lines, and vertical day column dividers."""
        grid_h = max(1.0, grid_top - y0)
        _draw_vertical_hour_grid(
            x0=x0,
            w=w,
            gutter_w=gutter_w,
            grid_top=grid_top,
            grid_h=grid_h,
            start_hour=self._start_hour,
            end_hour=self._end_hour,
            hour_step=self._hour_step,
            border_style=self._border_style,
            text_style=self._text_style,
        )

        col_hdr_top = y0 + h - title_h
        for i in range(self._num_days):
            lx = x0 + gutter_w + i * col_w
            canvas_line(xy1=(lx, y0), xy2=(lx, col_hdr_top), style=self._border_style)

        canvas_line(xy1=(x0, col_hdr_top), xy2=(x0 + w, col_hdr_top), style=self._border_style)
        canvas_line(xy1=(x0, all_day_top), xy2=(x0 + w, all_day_top), style=self._border_style)
        if all_day_h > 0:
            canvas_line(xy1=(x0, grid_top), xy2=(x0 + w, grid_top), style=self._border_style)

        outer_style = make_outer_frame_style(self._border_style)
        canvas_rectangle(xy=(x0 + w / 2.0, y0 + h / 2.0), width=w, height=h, style=outer_style)

    def _draw_all_day_events(  # noqa: PLR0913
        self,
        *,
        x0: float,
        gutter_w: float,
        col_w: float,
        all_day_top: float,
        all_day_h: float,
        track_h: float,
        packed_all_day: list[tuple[CalendarItem, int, int, bool, bool, int]],
    ) -> None:
        """Render X-axis spanning event bars inside the top All-Day field."""
        if all_day_h <= 0:
            return
        for item, c_start, c_end, cont_l, cont_r, lane_idx in packed_all_day:
            if not item.show:
                continue
            pad_l = 0.15 if cont_l else 0.50
            pad_r = 0.15 if cont_r else 0.50
            bx0 = x0 + gutter_w + c_start * col_w + pad_l
            bx1 = x0 + gutter_w + (c_end + 1) * col_w - pad_r
            bw = max(0.5, bx1 - bx0)
            bcy = all_day_top - 0.50 - (lane_idx + 0.5) * (track_h + 0.5)

            lbl = item.text
            if lbl:
                if cont_l:
                    lbl = f"← {lbl}"
                if cont_r:
                    lbl = f"{lbl} →"
            draw_event_card(
                cx=bx0 + bw / 2.0,
                cy=bcy,
                width=bw,
                height=track_h,
                text=lbl,
                description=item.description,
                style=item.style,
                text_style=item.text_style,
                description_style=item.description_style,
            )

    def _collect_timed_segments(
        self,
        dates: list[date],
    ) -> tuple[
        dict[int, list[tuple[CalendarItem, float, float]]],
        list[tuple[CalendarItem, int, int, float, float]],
    ]:
        """Collect per-column timed segments and multi-column span boxes."""
        w_start, w_end = dates[0], dates[-1]
        s_hr_f = float(self._start_hour)
        e_hr_f = float(self._end_hour)

        col_segments: dict[int, list[tuple[CalendarItem, float, float]]] = {i: [] for i in range(self._num_days)}
        box_spans: list[tuple[CalendarItem, int, int, float, float]] = []

        for item in self._items:
            s_date, e_date, s_hr, e_hr, is_all_day = resolve_item_span(item)
            if is_all_day or s_hr is None or e_hr is None or e_date < w_start or s_date > w_end:
                continue

            if item.span_mode == "box" and s_date != e_date:
                c_start = (max(s_date, w_start) - w_start).days
                c_end = (min(e_date, w_end) - w_start).days
                box_spans.append((item, c_start, c_end, s_hr, e_hr))
                continue

            cur_d = max(s_date, w_start)
            last_d = min(e_date, w_end)
            while cur_d <= last_d:
                c_idx = (cur_d - w_start).days
                seg_s = s_hr if cur_d == s_date else s_hr_f
                seg_e = e_hr if cur_d == e_date else e_hr_f
                clamped_s = max(s_hr_f, min(e_hr_f, seg_s))
                clamped_e = max(s_hr_f, min(e_hr_f, seg_e))
                if clamped_e > clamped_s:
                    col_segments[c_idx].append((item, clamped_s, clamped_e))
                cur_d += timedelta(days=1)

        return col_segments, box_spans

    def _draw_timed_events(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        gutter_w: float,
        col_w: float,
        grid_top: float,
        dates: list[date],
    ) -> None:
        """Render timed events (per-day columns or multi-day unified span boxes)."""
        grid_h = max(1.0, grid_top - y0)
        s_hr_f = float(self._start_hour)
        e_hr_f = float(self._end_hour)

        def hr_to_y(hr: float) -> float:
            clamped = max(s_hr_f, min(e_hr_f, hr))
            return grid_top - ((clamped - s_hr_f) / (e_hr_f - s_hr_f)) * grid_h

        col_segments, box_spans = self._collect_timed_segments(dates)

        # Render per-column timed segments with automatic parallel lane splitting
        for c_idx, segs in col_segments.items():
            if not segs:
                continue
            intervals = [(hs, he) for _, hs, he in segs]
            lane_of, total_lanes_of = pack_half_open_intervals(intervals)
            for (item, hs, he), l_idx, tot_lanes in zip(
                segs,
                lane_of,
                total_lanes_of,
                strict=True,
            ):
                if not item.show:
                    continue
                avail_w = col_w - 0.8
                slot_w = avail_w / max(1, tot_lanes)
                cx = x0 + gutter_w + c_idx * col_w + 0.4 + (l_idx + 0.5) * slot_w
                y_top = hr_to_y(hs) - 0.2
                y_bot = hr_to_y(he) + 0.2
                ch = max(0.8, y_top - y_bot)
                draw_event_card(
                    cx=cx,
                    cy=(y_top + y_bot) / 2.0,
                    width=max(0.5, slot_w - 0.2),
                    height=ch,
                    text=item.text,
                    description=item.description,
                    style=item.style,
                    text_style=item.text_style,
                    description_style=item.description_style,
                )

        # Render multi-column spanning boxes ("box" mode)
        for item, c_start, c_end, hs, he in box_spans:
            if not item.show:
                continue
            bx0 = x0 + gutter_w + c_start * col_w + 0.45
            bx1 = x0 + gutter_w + (c_end + 1) * col_w - 0.45
            bw = max(0.5, bx1 - bx0)
            y_top = hr_to_y(hs) - 0.2
            y_bot = hr_to_y(he) + 0.2
            bh = max(0.8, y_top - y_bot)
            draw_event_card(
                cx=bx0 + bw / 2.0,
                cy=(y_top + y_bot) / 2.0,
                width=bw,
                height=bh,
                text=item.text,
                description=item.description,
                style=item.style,
                text_style=item.text_style,
                description_style=item.description_style,
            )
