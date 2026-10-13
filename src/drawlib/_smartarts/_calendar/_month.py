# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""MonthCalendar SmartArt implementation module."""

from __future__ import annotations

import calendar
from datetime import date, timedelta
from typing import Literal, Self

from pydantic import validate_call

from drawlib._core.l2_types import Coordinate, PosFloat, PosInt  # noqa: TC001
from drawlib._core.l3_styles import Style  # noqa: TC001
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform
from drawlib._smartarts._calendar._models import (
    MONTH_NAMES_EN,
    WEEKDAYS_SUN_EN,
    WEEKDAYS_SUN_JA,
    CalendarItem,
    derive_default_event_styles,
    draw_event_card,
    make_outer_frame_style,
    make_subtle_fill_style,
    pack_closed_intervals,
    parse_iso_date_strict,
    resolve_box_origin,
    resolve_item_span,
)


class MonthCalendar:
    """SmartArt component for rendering Outlook/Google-style monthly or multi-week grid calendars."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        start_date: str = "2026-10-01",
        end_date: str | None = None,
        first_weekday: Literal["sun", "mon"] = "sun",
        title: str | None = None,
        lang: Literal["en", "ja"] = "en",
        max_tracks: PosInt = 3,
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
        """Initialize MonthCalendar with explicit styles and ISO date configuration.

        Args:
            start_date: Target month start date or range start date in 'YYYY-MM-DD' format.
                Defaults to '2026-10-01'.
            end_date: Optional range end date in 'YYYY-MM-DD' format. When None, renders the
                entire calendar month of `start_date`.
            first_weekday: Leftmost column weekday ('sun' or 'mon'). Defaults to 'sun'.
            title: Custom title text displayed in the top banner. When None, auto-generates
                the month/year title (e.g. 'October 2026'). Pass '' to hide the title bar.
            lang: Label language ('en' or 'ja'). Defaults to 'en'.
            max_tracks: Maximum number of stacked event bar tracks per week row. Defaults to 3.
            cell_style: Default background style for in-month date cells.
            text_style: Default text style for weekday date numbers.
            header_style: Background style for the weekday header row.
            header_text_style: Text style for weekday column headers.
            border_style: Line style for grid borders.
            event_style: Default style for event bars added via `add()`.
            event_text_style: Default text style for event bar labels.
            sunday_text_style: Optional override text style for Sunday headers and date numbers.
            saturday_text_style: Optional override text style for Saturday headers and date numbers.
            title_style: Optional background style for the top title bar (defaults to `header_style`).
            title_text_style: Optional text style for the top title bar (defaults to `header_text_style`).

        Raises:
            ValueError: If `start_date` or `end_date` is not in 'YYYY-MM-DD' format or `end_date < start_date`.
        """
        self._start_date: date = parse_iso_date_strict(start_date, param_name="start_date")
        self._end_date: date | None = (
            parse_iso_date_strict(end_date, param_name="end_date") if end_date is not None else None
        )
        if self._end_date is not None and self._end_date < self._start_date:
            raise ValueError(
                f"end_date ({end_date}) must not be earlier than start_date ({start_date})."
            )

        self._first_weekday: Literal["sun", "mon"] = first_weekday
        self._title: str | None = title
        self._lang: Literal["en", "ja"] = lang
        self._max_tracks: int = int(max_tracks)

        self._cell_style: Style = cell_style
        self._text_style: Style = text_style
        self._header_style: Style = header_style
        self._header_text_style: Style = header_text_style
        self._border_style: Style = border_style

        ev_st, ev_txt_st = derive_default_event_styles(
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
        self._title_text_style: Style = (
            title_text_style if title_text_style is not None else header_text_style
        )
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
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a single-day or multi-day spanning event bar on the month calendar.

        Args:
            start: Event start date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            end: Optional event end date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
                Defaults to `start` when None.
            text: Primary event label text. Defaults to ''.
            description: Optional secondary subtitle text. Defaults to ''.
            style: Custom box style for this event bar. Defaults to `event_style`.
            text_style: Custom text style for this event label. Defaults to `event_text_style`.
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
            all_day=True,
            span_mode="all_day",
            style=eff_style,
            text_style=eff_text_style,
            description_style=description_style,
            show=show,
        )
        resolve_item_span(item)
        self._items.append(item)
        return item

    def _build_weeks(self) -> list[list[date]]:
        """Construct the list of 7-day week rows for the configured month or date range."""
        first_wd = calendar.SUNDAY if self._first_weekday == "sun" else calendar.MONDAY
        cal = calendar.Calendar(firstweekday=first_wd)

        if self._end_date is None:
            month_dates = list(cal.itermonthdates(self._start_date.year, self._start_date.month))
            return [month_dates[i : i + 7] for i in range(0, len(month_dates), 7)]

        # Custom range mode: align start_date back to first_weekday and end_date forward to week end
        start_offset = (self._start_date.weekday() - first_wd) % 7
        grid_start = self._start_date - timedelta(days=start_offset)
        end_offset = (6 - ((self._end_date.weekday() - first_wd) % 7)) % 7
        grid_end = self._end_date + timedelta(days=end_offset)
        total_days = (grid_end - grid_start).days + 1
        all_dates = [grid_start + timedelta(days=i) for i in range(total_days)]
        return [all_dates[i : i + 7] for i in range(0, len(all_dates), 7)]

    def _resolve_title_text(self) -> str:
        """Resolve the header title string based on language and date range."""
        if self._title is not None:
            return self._title
        y, m = self._start_date.year, self._start_date.month
        if self._end_date is not None and (
            self._end_date.year != y or self._end_date.month != m
        ):
            ey, em = self._end_date.year, self._end_date.month
            if self._lang == "ja":
                return f"{y}年{m}月 – {ey}年{em}月"
            return f"{MONTH_NAMES_EN[m]} {y} – {MONTH_NAMES_EN[em]} {ey}"
        if self._lang == "ja":
            return f"{y}年 {m}月"
        return f"{MONTH_NAMES_EN[m]} {y}"

    def _compute_geometry(
        self,
        x0: float,
        y0: float,
        w: float,
        h: float,
        num_weeks: int,
    ) -> tuple[float, float, float, float, float, float]:
        """Compute (title_h, weekday_h, grid_top, weekday_top, col_w, row_h)."""
        title_str = self._resolve_title_text()
        title_h = min(6.4, h * 0.11) if title_str else 0.0
        weekday_h = min(4.6, h * 0.08)
        grid_h = max(1.0, h - title_h - weekday_h)
        grid_top = y0 + grid_h
        weekday_top = grid_top + weekday_h
        col_w = w / 7.0
        row_h = grid_h / max(1, num_weeks)
        return title_h, weekday_h, grid_top, weekday_top, col_w, row_h

    @validate_call
    def get_date_xy(
        self,
        date: str,
        xy: Coordinate,
        width: PosFloat = 100.0,
        height: PosFloat = 60.0,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> tuple[float, float]:
        """Return the canvas center coordinate (cx, cy) of a specific date cell.

        Args:
            date: Target date in 'YYYY-MM-DD' format.
            xy: Anchor coordinate (x, y) of the calendar bounding box.
            width: Unscaled width of the calendar. Defaults to 100.0.
            height: Unscaled height of the calendar. Defaults to 60.0.
            align: Anchor alignment of `xy` ('bottom_left', 'center', or 'top_left').
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            tuple[float, float]: Center coordinate `(cx, cy)` of the target date cell.

        Raises:
            ValueError: If `date` is invalid or not present in the displayed calendar grid.
        """
        d_obj = parse_iso_date_strict(date, param_name="date")
        weeks = self._build_weeks()
        w = float(width) * float(scale)
        h = float(height) * float(scale)
        x0, y0 = resolve_box_origin(xy, w, h, align)
        _, _, grid_top, _, col_w, row_h = self._compute_geometry(
            x0,
            y0,
            w,
            h,
            len(weeks),
        )
        for w_idx, week in enumerate(weeks):
            for c_idx, cell_d in enumerate(week):
                if cell_d == d_obj:
                    cx = x0 + (c_idx + 0.5) * col_w
                    cy = grid_top - (w_idx + 0.5) * row_h
                    return (cx, cy)
        raise ValueError(f"Date '{date}' is outside the displayed MonthCalendar grid.")

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
        """Render the monthly or multi-week grid calendar onto the canvas.

        Args:
            xy: Anchor coordinate (x, y) of the calendar bounding box.
            width: Total width of the calendar. Defaults to 100.0.
            height: Total height of the calendar. Defaults to 60.0.
            align: Anchor alignment of `xy` ('bottom_left', 'center', or 'top_left').
                Defaults to 'bottom_left'.
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            Self: This MonthCalendar instance for method chaining.
        """
        total_w = float(width)
        total_h = float(height)
        x0, y0 = resolve_box_origin(xy, total_w, total_h, align)
        weeks = self._build_weeks()
        title_h, weekday_h, grid_top, weekday_top, col_w, row_h = self._compute_geometry(
            x0,
            y0,
            total_w,
            total_h,
            len(weeks),
        )

        with transform(origin=xy, scale=scale):
            self._draw_title_and_headers(
                x0=x0,
                y0=y0,
                w=total_w,
                h=total_h,
                title_h=title_h,
                weekday_h=weekday_h,
                weekday_top=weekday_top,
                col_w=col_w,
            )
            self._draw_cells_and_dates(
                x0=x0,
                grid_top=grid_top,
                col_w=col_w,
                row_h=row_h,
                weeks=weeks,
            )
            self._draw_grid_lines(
                x0=x0,
                y0=y0,
                w=total_w,
                h=total_h,
                grid_top=grid_top,
                weekday_top=weekday_top,
                col_w=col_w,
                row_h=row_h,
                num_weeks=len(weeks),
            )
            self._draw_events(
                x0=x0,
                grid_top=grid_top,
                col_w=col_w,
                row_h=row_h,
                weeks=weeks,
            )

        return self

    def _weekday_order(self) -> tuple[tuple[str, int], ...]:
        """Return 7 tuples of (label, sun_based_index 0=Sun..6=Sat)."""
        labels = WEEKDAYS_SUN_JA if self._lang == "ja" else WEEKDAYS_SUN_EN
        indices = (0, 1, 2, 3, 4, 5, 6) if self._first_weekday == "sun" else (1, 2, 3, 4, 5, 6, 0)
        return tuple((labels[i], i) for i in indices)

    def _draw_title_and_headers(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        title_h: float,
        weekday_h: float,
        weekday_top: float,
        col_w: float,
    ) -> None:
        """Draw the top title bar and the 7-column weekday header strip."""
        title_str = self._resolve_title_text()
        if title_h > 0 and title_str:
            t_cy = y0 + h - title_h / 2.0
            canvas_rectangle(
                xy=(x0 + w / 2.0, t_cy),
                width=w,
                height=title_h,
                style=self._title_style.patch(shape_r=0, shape_line_width=0),
            )
            canvas_text(
                xy=(x0 + w / 2.0, t_cy),
                text=title_str,
                style=self._title_text_style.patch(halign="center", valign="center"),
            )

        wd_cy = weekday_top - weekday_h / 2.0
        canvas_rectangle(
            xy=(x0 + w / 2.0, wd_cy),
            width=w,
            height=weekday_h,
            style=self._header_style.patch(shape_r=0, shape_line_width=0),
        )
        for c_idx, (wd_label, sun_idx) in enumerate(self._weekday_order()):
            cx = x0 + (c_idx + 0.5) * col_w
            if sun_idx == 0 and self._sunday_text_style is not None:
                st = self._sunday_text_style
            elif sun_idx == 6 and self._saturday_text_style is not None:
                st = self._saturday_text_style
            else:
                st = self._header_text_style
            canvas_text(
                xy=(cx, wd_cy),
                text=wd_label,
                style=st.patch(halign="center", valign="center"),
            )

    def _is_in_active_range(self, d: date) -> bool:
        """Check whether date `d` belongs to the primary month or custom range."""
        if self._end_date is None:
            return d.month == self._start_date.month and d.year == self._start_date.year
        return self._start_date <= d <= self._end_date

    def _draw_cells_and_dates(  # noqa: PLR0913
        self,
        *,
        x0: float,
        grid_top: float,
        col_w: float,
        row_h: float,
        weeks: list[list[date]],
    ) -> None:
        """Render cell backgrounds and top-left date numbers for all week rows."""
        in_style = self._cell_style.patch(shape_r=0, shape_line_width=0)
        out_style = make_subtle_fill_style(self._cell_style, (246, 248, 250))
        date_band_h = row_h * 0.30
        wd_meta = self._weekday_order()

        for w_idx, week in enumerate(weeks):
            row_top = grid_top - w_idx * row_h
            row_cy = row_top - row_h / 2.0
            for c_idx, d in enumerate(week):
                cell_cx = x0 + (c_idx + 0.5) * col_w
                active = self._is_in_active_range(d)
                canvas_rectangle(
                    xy=(cell_cx, row_cy),
                    width=col_w,
                    height=row_h,
                    style=in_style if active else out_style,
                )
                sun_idx = wd_meta[c_idx][1]
                if not active:
                    d_st = self._text_style.patch(alpha=0.45)
                elif sun_idx == 0 and self._sunday_text_style is not None:
                    d_st = self._sunday_text_style
                elif sun_idx == 6 and self._saturday_text_style is not None:
                    d_st = self._saturday_text_style
                else:
                    d_st = self._text_style

                label_str = f"{d.month}/{d.day}" if (d.day == 1 and not active) else str(d.day)
                num_x = x0 + c_idx * col_w + min(1.4, col_w * 0.12)
                num_y = row_top - date_band_h * 0.52
                canvas_text(
                    xy=(num_x, num_y),
                    text=label_str,
                    style=d_st.patch(halign="left", valign="center"),
                )

    def _draw_grid_lines(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        grid_top: float,
        weekday_top: float,
        col_w: float,
        row_h: float,
        num_weeks: int,
    ) -> None:
        """Render internal cell grid lines and outer calendar frame."""
        for c_idx in range(1, 7):
            lx = x0 + c_idx * col_w
            canvas_line(xy1=(lx, y0), xy2=(lx, weekday_top), style=self._border_style)
        for w_idx in range(num_weeks):
            ly = grid_top - w_idx * row_h
            canvas_line(xy1=(x0, ly), xy2=(x0 + w, ly), style=self._border_style)
        canvas_line(xy1=(x0, weekday_top), xy2=(x0 + w, weekday_top), style=self._border_style)
        outer_style = make_outer_frame_style(self._border_style)
        canvas_rectangle(xy=(x0 + w / 2.0, y0 + h / 2.0), width=w, height=h, style=outer_style)

    def _draw_events(  # noqa: PLR0913
        self,
        *,
        x0: float,
        grid_top: float,
        col_w: float,
        row_h: float,
        weeks: list[list[date]],
    ) -> None:
        """Render single-day and multi-day spanning event bars across week rows."""
        if not self._items:
            return
        parsed_items = [(item, *resolve_item_span(item)[:2]) for item in self._items]
        date_band_h = row_h * 0.30
        track_area_h = max(1.0, row_h - date_band_h - 0.6)
        gap_y = 0.35
        track_h = max(1.2, (track_area_h / self._max_tracks) - gap_y)

        for w_idx, week in enumerate(weeks):
            w_start, w_end = week[0], week[6]
            row_top = grid_top - w_idx * row_h
            overlapping: list[tuple[CalendarItem, date, date, int, int]] = []
            intervals: list[tuple[int, int]] = []

            for item, s_date, e_date in parsed_items:
                if e_date < w_start or s_date > w_end:
                    continue
                c_start = (max(s_date, w_start) - w_start).days
                c_end = (min(e_date, w_end) - w_start).days
                overlapping.append((item, s_date, e_date, c_start, c_end))
                intervals.append((c_start, c_end))

            lanes, _ = pack_closed_intervals(intervals)
            for (item, s_date, e_date, c_start, c_end), lane_idx in zip(
                overlapping,
                lanes,
                strict=True,
            ):
                if not item.show or lane_idx >= self._max_tracks:
                    continue
                cont_l = s_date < w_start
                cont_r = e_date > w_end
                pad_l = 0.15 if cont_l else 0.55
                pad_r = 0.15 if cont_r else 0.55
                bx0 = x0 + c_start * col_w + pad_l
                bx1 = x0 + (c_end + 1) * col_w - pad_r
                bw = max(0.5, bx1 - bx0)
                bcy = (row_top - date_band_h - 0.25) - (lane_idx + 0.5) * (track_h + gap_y)

                label = item.text
                if label:
                    if cont_l:
                        label = f"← {label}"
                    if cont_r:
                        label = f"{label} →"
                draw_event_card(
                    cx=bx0 + bw / 2.0,
                    cy=bcy,
                    width=bw,
                    height=track_h,
                    text=label,
                    description=item.description,
                    style=item.style,
                    text_style=item.text_style,
                    description_style=item.description_style,
                )
