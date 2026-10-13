# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DayCalendar SmartArt implementation module."""

from __future__ import annotations

from datetime import date as dt_date
from typing import Literal, Self

from pydantic import validate_call

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
    derive_default_event_styles,
    draw_event_card,
    make_outer_frame_style,
    make_subtle_fill_style,
    pack_half_open_intervals,
    parse_iso_date_or_datetime,
    parse_iso_date_strict,
    resolve_box_origin,
    resolve_item_span,
    validate_hour_range,
)


class DayCalendar:
    """SmartArt component for rendering a single-day schedule in vertical or horizontal orientation."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        date: str = "2026-10-13",
        direction: Literal["vertical", "horizontal"] = "vertical",
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
        title_style: Style | None = None,
        title_text_style: Style | None = None,
    ) -> None:
        """Initialize DayCalendar with explicit styles, target date, orientation, and hour range.

        Args:
            date: Target date in 'YYYY-MM-DD' format. Defaults to '2026-10-13'.
            direction: Layout orientation ('vertical' for top-to-bottom time axis, 'horizontal'
                for left-to-right time axis). Defaults to 'vertical'.
            start_hour: Start hour on the 24-hour axis (0..23). Defaults to 9.
            end_hour: End hour on the 24-hour axis (1..24). Defaults to 18.
            hour_step: Hour label interval along the time axis. Defaults to 1.
            show_all_day: Controls top All-Day field visibility. When None (default), automatically
                displays only if at least one all-day event is registered.
            all_day_label: Custom label for the All-Day field (defaults to 'All-day' or '全日').
            title: Custom title text in the top banner. When None, auto-generates the date and weekday.
                Pass '' to hide the title bar.
            lang: Label language ('en' or 'ja'). Defaults to 'en'.
            cell_style: Background style for the time grid.
            text_style: Text style for time axis labels.
            header_style: Background style for time headers (in horizontal mode) or secondary bands.
            header_text_style: Text style for header labels.
            border_style: Line style for grid borders.
            event_style: Default box style for events added via `add()`.
            event_text_style: Default text style for event titles.
            title_style: Optional background style for the top title bar (defaults to `header_style`).
            title_text_style: Optional text style for the top title bar (defaults to `header_text_style`).

        Raises:
            ValueError: If `date` is not in 'YYYY-MM-DD' format or hours are invalid.
        """
        validate_hour_range(start_hour, end_hour, int(hour_step))
        self._date: dt_date = parse_iso_date_strict(date, param_name="date")
        self._direction: Literal["vertical", "horizontal"] = direction
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

        ev_st, ev_txt_st = derive_default_event_styles(
            header_style,
            header_text_style,
            event_style,
            event_text_style,
        )
        self._event_style: Style = ev_st
        self._event_text_style: Style = ev_txt_st
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
        all_day: bool | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a timed block ('YYYY-MM-DD HH:MM') or all-day banner ('YYYY-MM-DD') on the day schedule.

        Args:
            start: Event start date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            end: Optional event end date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            text: Primary event title text. Defaults to ''.
            description: Optional secondary subtitle text. Defaults to ''.
            all_day: Optional explicit override to force rendering in the All-Day field.
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
            style=eff_style,
            text_style=eff_text_style,
            description_style=description_style,
            show=show,
        )
        resolve_item_span(item)
        self._items.append(item)
        return item

    def _resolve_title_text(self) -> str:
        """Resolve top banner title text."""
        if self._title is not None:
            return self._title
        sun_idx = (self._date.weekday() + 1) % 7
        if self._lang == "ja":
            return f"{self._date.isoformat()} ({WEEKDAYS_SUN_JA[sun_idx]})"
        return f"{WEEKDAYS_SUN_EN[sun_idx]}, {self._date.isoformat()}"

    def _partition_items(self) -> tuple[list[CalendarItem], list[tuple[CalendarItem, float, float]]]:
        """Partition items overlapping `self._date` into all_day items and timed segments."""
        all_day_items: list[CalendarItem] = []
        timed_segs: list[tuple[CalendarItem, float, float]] = []
        s_hr_f = float(self._start_hour)
        e_hr_f = float(self._end_hour)

        for item in self._items:
            s_date, e_date, s_hr, e_hr, is_all_day = resolve_item_span(item)
            if e_date < self._date or s_date > self._date:
                continue
            if is_all_day or s_hr is None or e_hr is None:
                all_day_items.append(item)
                continue
            seg_s = s_hr if s_date == self._date else s_hr_f
            seg_e = e_hr if e_date == self._date else e_hr_f
            clamped_s = max(s_hr_f, min(e_hr_f, seg_s))
            clamped_e = max(s_hr_f, min(e_hr_f, seg_e))
            if clamped_e > clamped_s:
                timed_segs.append((item, clamped_s, clamped_e))

        return all_day_items, timed_segs

    def _resolve_all_day_height(self, h: float, num_all_day: int) -> tuple[float, float]:
        """Compute (all_day_h, track_h) preserving layout across item.show changes."""
        has_all_day = (
            self._show_all_day
            if self._show_all_day is not None
            else (num_all_day > 0)
        )
        if not has_all_day:
            return 0.0, 0.0
        eff_lanes = max(1, num_all_day)
        track_h = min(3.0, h * 0.065)
        all_day_h = eff_lanes * (track_h + 0.5) + 0.8
        return all_day_h, track_h

    @validate_call
    def get_time_xy(
        self,
        dt: str,
        xy: Coordinate,
        width: PosFloat = 100.0,
        height: PosFloat = 60.0,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> tuple[float, float]:
        """Return the canvas center coordinate (cx, cy) at a specific datetime or all-day slot.

        Args:
            dt: Target ISO date ('YYYY-MM-DD') or datetime ('YYYY-MM-DD HH:MM').
            xy: Anchor coordinate (x, y) of the calendar bounding box.
            width: Unscaled width of the calendar. Defaults to 100.0.
            height: Unscaled height of the calendar. Defaults to 60.0.
            align: Anchor alignment of `xy` ('bottom_left', 'center', or 'top_left').
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            tuple[float, float]: Canvas coordinate `(cx, cy)` of the target time slot.

        Raises:
            ValueError: If `dt` does not match `self._date` or is outside the displayed hour range.
        """
        target_d, target_hr = parse_iso_date_or_datetime(dt, param_name="dt")
        if target_d != self._date:
            raise ValueError(
                f"Date '{target_d}' in '{dt}' does not match DayCalendar date '{self._date}'."
            )

        w = float(width) * float(scale)
        h = float(height) * float(scale)
        x0, y0 = resolve_box_origin(xy, w, h, align)
        all_day_items, _ = self._partition_items()
        title_str = self._resolve_title_text()
        title_h = min(5.4, h * 0.11) if title_str else 0.0
        all_day_h, _ = self._resolve_all_day_height(h, len(all_day_items))

        if target_hr is None:
            ad_top = y0 + h - title_h
            cy = (ad_top - all_day_h / 2.0) if all_day_h > 0 else ad_top
            return (x0 + w / 2.0, cy)

        if not (self._start_hour <= target_hr <= self._end_hour):
            raise ValueError(
                f"Hour {target_hr} in '{dt}' is outside [{self._start_hour}, {self._end_hour}]."
            )
        ratio = (target_hr - self._start_hour) / (self._end_hour - self._start_hour)
        if self._direction == "vertical":
            gutter_w = min(9.0, w * 0.22)
            grid_top = y0 + h - title_h - all_day_h
            grid_h = max(1.0, grid_top - y0)
            return (x0 + gutter_w + (w - gutter_w) / 2.0, grid_top - ratio * grid_h)

        hdr_h = min(4.2, h * 0.12)
        body_top = y0 + h - title_h - all_day_h - hdr_h
        body_h = max(1.0, body_top - y0)
        return (x0 + ratio * w, y0 + body_h / 2.0)

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
        """Render the single-day schedule onto the canvas.

        Args:
            xy: Anchor coordinate (x, y) of the calendar bounding box.
            width: Total width of the calendar. Defaults to 100.0.
            height: Total height of the calendar. Defaults to 60.0.
            align: Anchor alignment of `xy` ('bottom_left', 'center', or 'top_left').
                Defaults to 'bottom_left'.
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            Self: This DayCalendar instance for method chaining.
        """
        total_w = float(width)
        total_h = float(height)
        x0, y0 = resolve_box_origin(xy, total_w, total_h, align)
        all_day_items, timed_segs = self._partition_items()

        with transform(origin=xy, scale=scale):
            if self._direction == "vertical":
                self._draw_vertical(
                    x0=x0,
                    y0=y0,
                    w=total_w,
                    h=total_h,
                    all_day_items=all_day_items,
                    timed_segs=timed_segs,
                )
            else:
                self._draw_horizontal(
                    x0=x0,
                    y0=y0,
                    w=total_w,
                    h=total_h,
                    all_day_items=all_day_items,
                    timed_segs=timed_segs,
                )

        return self

    def _draw_title_and_all_day(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        gutter_w: float,
        all_day_items: list[CalendarItem],
    ) -> tuple[float, float]:
        """Draw top title bar and optional All-Day band; return (title_h, all_day_h)."""
        title_str = self._resolve_title_text()
        title_h = min(5.4, h * 0.11) if title_str else 0.0
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

        all_day_h, track_h = self._resolve_all_day_height(h, len(all_day_items))
        if all_day_h > 0:
            ad_top = y0 + h - title_h
            ad_cy = ad_top - all_day_h / 2.0
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
            if gutter_w > 0:
                canvas_text(
                    xy=(x0 + gutter_w / 2.0, ad_cy),
                    text=ad_lbl,
                    style=self._header_text_style.patch(halign="center", valign="center"),
                )
            bar_x0 = x0 + gutter_w + 0.55
            bar_w = max(1.0, w - gutter_w - 1.1)
            for idx, item in enumerate(all_day_items):
                if not item.show:
                    continue
                bcy = ad_top - 0.45 - (idx + 0.5) * (track_h + 0.5)
                draw_event_card(
                    cx=bar_x0 + bar_w / 2.0,
                    cy=bcy,
                    width=bar_w,
                    height=track_h,
                    text=item.text,
                    description=item.description,
                    style=item.style,
                    text_style=item.text_style,
                    description_style=item.description_style,
                )
            canvas_line(xy1=(x0, ad_top), xy2=(x0 + w, ad_top), style=self._border_style)

        return title_h, all_day_h

    def _draw_vertical(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        all_day_items: list[CalendarItem],
        timed_segs: list[tuple[CalendarItem, float, float]],
    ) -> None:
        """Render vertical DayCalendar (top-to-bottom time axis)."""
        gutter_w = min(9.0, w * 0.22)
        title_h, all_day_h = self._draw_title_and_all_day(
            x0=x0,
            y0=y0,
            w=w,
            h=h,
            gutter_w=gutter_w,
            all_day_items=all_day_items,
        )
        grid_top = y0 + h - title_h - all_day_h
        grid_h = max(1.0, grid_top - y0)
        body_w = max(1.0, w - gutter_w)

        canvas_rectangle(
            xy=(x0 + gutter_w / 2.0, y0 + grid_h / 2.0),
            width=gutter_w,
            height=grid_h,
            style=make_subtle_fill_style(self._cell_style, (250, 251, 253)),
        )
        canvas_rectangle(
            xy=(x0 + gutter_w + body_w / 2.0, y0 + grid_h / 2.0),
            width=body_w,
            height=grid_h,
            style=self._cell_style.patch(shape_r=0, shape_line_width=0),
        )

        total_hours = self._end_hour - self._start_hour
        hour_h = grid_h / total_hours
        for h_offset in range(total_hours + 1):
            hy = grid_top - h_offset * hour_h
            if 0 < h_offset < total_hours:
                canvas_line(xy1=(x0 + gutter_w, hy), xy2=(x0 + w, hy), style=self._border_style)
            hr_val = self._start_hour + h_offset
            if h_offset < total_hours and (h_offset % self._hour_step == 0):
                canvas_text(
                    xy=(x0 + gutter_w / 2.0, hy - (hour_h * self._hour_step) / 2.0),
                    text=f"{hr_val:02d}:00",
                    style=self._text_style.patch(halign="center", valign="center"),
                )

        canvas_line(xy1=(x0 + gutter_w, y0), xy2=(x0 + gutter_w, y0 + h - title_h), style=self._border_style)
        canvas_line(xy1=(x0, grid_top), xy2=(x0 + w, grid_top), style=self._border_style)

        if timed_segs:
            intervals = [(hs, he) for _, hs, he in timed_segs]
            lane_of, total_lanes_of = pack_half_open_intervals(intervals)
            for (item, hs, he), l_idx, tot_lanes in zip(
                timed_segs,
                lane_of,
                total_lanes_of,
                strict=True,
            ):
                if not item.show:
                    continue
                slot_w = (body_w - 1.0) / max(1, tot_lanes)
                cx = x0 + gutter_w + 0.5 + (l_idx + 0.5) * slot_w
                y_top = grid_top - ((hs - self._start_hour) / total_hours) * grid_h - 0.2
                y_bot = grid_top - ((he - self._start_hour) / total_hours) * grid_h + 0.2
                ch = max(0.8, y_top - y_bot)
                draw_event_card(
                    cx=cx,
                    cy=(y_top + y_bot) / 2.0,
                    width=max(0.5, slot_w - 0.25),
                    height=ch,
                    text=item.text,
                    description=item.description,
                    style=item.style,
                    text_style=item.text_style,
                    description_style=item.description_style,
                )

        outer_style = make_outer_frame_style(self._border_style)
        canvas_rectangle(xy=(x0 + w / 2.0, y0 + h / 2.0), width=w, height=h, style=outer_style)

    def _draw_horizontal(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        w: float,
        h: float,
        all_day_items: list[CalendarItem],
        timed_segs: list[tuple[CalendarItem, float, float]],
    ) -> None:
        """Render horizontal DayCalendar (left-to-right time axis)."""
        title_h, all_day_h = self._draw_title_and_all_day(
            x0=x0,
            y0=y0,
            w=w,
            h=h,
            gutter_w=0.0,
            all_day_items=all_day_items,
        )
        hdr_top = y0 + h - title_h - all_day_h
        hdr_h = min(4.2, h * 0.12)
        body_top = hdr_top - hdr_h
        body_h = max(1.0, body_top - y0)

        canvas_rectangle(
            xy=(x0 + w / 2.0, hdr_top - hdr_h / 2.0),
            width=w,
            height=hdr_h,
            style=self._header_style.patch(shape_r=0, shape_line_width=0),
        )
        canvas_rectangle(
            xy=(x0 + w / 2.0, y0 + body_h / 2.0),
            width=w,
            height=body_h,
            style=self._cell_style.patch(shape_r=0, shape_line_width=0),
        )

        total_hours = self._end_hour - self._start_hour
        col_w = w / total_hours
        for h_offset in range(total_hours):
            if h_offset > 0:
                lx = x0 + h_offset * col_w
                canvas_line(xy1=(lx, y0), xy2=(lx, hdr_top), style=self._border_style)
            if h_offset % self._hour_step == 0:
                hr_val = self._start_hour + h_offset
                cx = x0 + (h_offset + 0.5 * self._hour_step) * col_w
                canvas_text(
                    xy=(cx, hdr_top - hdr_h / 2.0),
                    text=f"{hr_val:02d}:00",
                    style=self._header_text_style.patch(halign="center", valign="center"),
                )

        canvas_line(xy1=(x0, hdr_top), xy2=(x0 + w, hdr_top), style=self._border_style)
        canvas_line(xy1=(x0, body_top), xy2=(x0 + w, body_top), style=self._border_style)

        if timed_segs:
            intervals = [(hs, he) for _, hs, he in timed_segs]
            lane_of, total_lanes_of = pack_half_open_intervals(intervals)
            for (item, hs, he), l_idx, tot_lanes in zip(
                timed_segs,
                lane_of,
                total_lanes_of,
                strict=True,
            ):
                if not item.show:
                    continue
                lane_h = (body_h - 1.0) / max(1, tot_lanes)
                cy = body_top - 0.5 - (l_idx + 0.5) * lane_h
                x_left = x0 + ((hs - self._start_hour) / total_hours) * w + 0.2
                x_right = x0 + ((he - self._start_hour) / total_hours) * w - 0.2
                ew = max(0.8, x_right - x_left)
                draw_event_card(
                    cx=(x_left + x_right) / 2.0,
                    cy=cy,
                    width=ew,
                    height=max(0.5, lane_h - 0.25),
                    text=item.text,
                    description=item.description,
                    style=item.style,
                    text_style=item.text_style,
                    description_style=item.description_style,
                )

        outer_style = make_outer_frame_style(self._border_style)
        canvas_rectangle(xy=(x0 + w / 2.0, y0 + h / 2.0), width=w, height=h, style=outer_style)
