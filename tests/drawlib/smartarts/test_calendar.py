# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts Calendar classes."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Literal

import pytest

from drawlib import canvas
from drawlib.smartarts import CalendarItem, DayCalendar, MonthCalendar, WeekCalendar
from drawlib.styles import Styles


def _base_kwargs() -> dict[str, Any]:
    """Return common calendar style initialization keyword arguments."""
    return {
        "cell_style": Styles.Neutral,
        "text_style": Styles.DarkBold,
        "header_style": Styles.SecondaryNeutral,
        "header_text_style": Styles.DarkBold,
        "border_style": Styles.Neutral,
        "event_style": Styles.PrimaryNeutral,
        "event_text_style": Styles.DarkBold,
    }


class TestCalendarValidation:
    """Unit tests for strict ISO 8601 date/datetime parsing and configuration validation."""

    @pytest.mark.parametrize(
        "invalid_str",
        [
            "2026/10/10",
            "2026/10/10 09:00",
            "09:00",
            "10-10-2026",
            "2026-10-10T09:00",
            "2026-10-10 09:00:00",
            "2026-10-10 9:00",
            "2025-02-29",
            "2026-13-01",
            "2026-10-10 25:00",
        ],
    )
    def test_strict_iso_rejects_invalid_formats(self, invalid_str: str) -> None:
        """Verify slash-separated, time-only, and invalid calendar dates raise ValueError."""
        cal = WeekCalendar(start_date="2026-10-05", **_base_kwargs())
        with pytest.raises(ValueError, match="Invalid"):
            cal.add(invalid_str, text="Bad Format")

    def test_leap_year_date_accepted(self) -> None:
        """Verify valid leap year date '2024-02-29' is accepted."""
        cal = DayCalendar(date="2024-02-29", **_base_kwargs())
        item = cal.add("2024-02-29 09:00", "2024-02-29 10:30", text="Leap Day Sync")
        assert isinstance(item, CalendarItem)
        assert item.start == "2024-02-29 09:00"

    def test_end_before_start_raises_error(self) -> None:
        """Verify end date/time earlier than or equal to start raises ValueError."""
        cal = WeekCalendar(start_date="2026-10-05", **_base_kwargs())
        with pytest.raises(ValueError, match="earlier than"):
            cal.add("2026-10-10", "2026-10-08", text="Reversed Dates")

        with pytest.raises(ValueError, match="later than"):
            cal.add("2026-10-10 14:00", "2026-10-10 14:00", text="Zero Duration")

        with pytest.raises(ValueError, match="later than"):
            cal.add("2026-10-10 15:00", "2026-10-10 12:00", text="Negative Time")

    def test_invalid_hour_range_raises_error(self) -> None:
        """Verify invalid start_hour and end_hour combinations raise ValueError."""
        with pytest.raises(ValueError, match="Invalid hour range"):
            WeekCalendar(
                start_date="2026-10-05",
                start_hour=18,
                end_hour=9,
                **_base_kwargs(),
            )

        with pytest.raises(ValueError, match="Invalid hour range"):
            DayCalendar(
                date="2026-10-10",
                start_hour=0,
                end_hour=25,
                **_base_kwargs(),
            )

    def test_auto_derived_event_styles_when_omitted(self) -> None:
        """Verify omitting event_style and event_text_style derives defaults from header_style."""
        kwargs = _base_kwargs()
        kwargs.pop("event_style")
        kwargs.pop("event_text_style")
        cal = DayCalendar(date="2026-10-10", **kwargs)
        item = cal.add("2026-10-10 09:00", "2026-10-10 10:00", text="Derived Style")
        assert item.style == Styles.SecondaryNeutral.patch(shape_r=0.55)
        assert item.text_style == Styles.DarkBold.patch(text_size=9.5)


class TestMonthCalendar:
    """Unit and rendering tests for MonthCalendar."""

    def test_init_validation(self) -> None:
        """Verify MonthCalendar validates start_date and end_date order and ISO format."""
        with pytest.raises(ValueError, match="Invalid ISO date format"):
            MonthCalendar(start_date="2026/10/01", **_base_kwargs())

        with pytest.raises(ValueError, match="end_date"):
            MonthCalendar(
                start_date="2026-10-20",
                end_date="2026-10-10",
                **_base_kwargs(),
            )

    def test_single_month_and_get_date_xy(self) -> None:
        """Verify single-month layout and get_date_xy coordinates."""
        cal = MonthCalendar(
            start_date="2026-10-01",
            first_weekday="sun",
            title="2026年 10月",
            lang="ja",
            sunday_text_style=Styles.PrimaryBold,
            saturday_text_style=Styles.SecondaryBold,
            **_base_kwargs(),
        )
        e1 = cal.add("2026-10-06", "2026-10-09", text="Design Sprint")
        e2 = cal.add("2026-10-10 09:00", "2026-10-13 15:00", text="Cross-Week Migration")
        e3 = cal.add("2026-10-12", text="Sports Day", style=Styles.SecondaryNeutral)

        assert len(cal.items) == 3
        assert e1.text == "Design Sprint"
        assert e2.start == "2026-10-10 09:00"
        assert e3.show is True

        cx1, cy1 = cal.get_date_xy("2026-10-01", xy=(10.0, 10.0), width=120.0, height=70.0)
        cx2, cy2 = cal.get_date_xy("2026-10-31", xy=(10.0, 10.0), width=120.0, height=70.0)
        assert cx2 > cx1
        assert cy1 > cy2

        with pytest.raises(ValueError, match="outside the displayed MonthCalendar grid"):
            cal.get_date_xy("2025-01-01", xy=(10.0, 10.0), width=120.0, height=70.0)

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "month.png"
            canvas.clear()
            canvas.setup(width=140, height=90)
            cal.draw(xy=(10.0, 10.0), width=120.0, height=70.0)
            canvas.save(str(out_path))
            assert out_path.exists()
            assert out_path.stat().st_size > 0

    def test_cross_month_custom_range_and_visibility(self) -> None:
        """Verify multi-week cross-month range ('2026-10-19' to '2026-11-08') and item.show toggle."""
        cal = MonthCalendar(
            start_date="2026-10-19",
            end_date="2026-11-08",
            first_weekday="mon",
            **_base_kwargs(),
        )
        cal.add("2026-10-20", "2026-10-23", text="Oct Release Prep")
        item_nov = cal.add("2026-10-30", "2026-11-04", text="Cross-Month Cutover")

        with tempfile.TemporaryDirectory() as tmpdir:
            f_all = Path(tmpdir) / "month_all.png"
            f_hide = Path(tmpdir) / "month_hide.png"

            canvas.clear()
            canvas.setup(width=140, height=80)
            cal.draw(xy=(10.0, 10.0), width=120.0, height=60.0)
            canvas.save(str(f_all))

            item_nov.show = False
            canvas.clear()
            canvas.setup(width=140, height=80)
            cal.draw(xy=(10.0, 10.0), width=120.0, height=60.0)
            canvas.save(str(f_hide))

            assert f_all.read_bytes() != f_hide.read_bytes()


class TestWeekCalendar:
    """Unit and rendering tests for WeekCalendar."""

    def test_show_all_day_modes_and_slot_xy(self) -> None:
        """Verify show_all_day=None/True/False behavior and get_slot_xy coordinates."""
        # 1. show_all_day=None with 0 all-day items -> All-day row disappears (all_day_h == 0)
        cal_auto = WeekCalendar(
            start_date="2026-10-05",
            start_hour=9,
            end_hour=18,
            show_all_day=None,
            **_base_kwargs(),
        )
        cal_auto.add("2026-10-05 10:00", "2026-10-05 12:00", text="Morning Review")
        _, cy_before_ad = cal_auto.get_slot_xy(
            "2026-10-05 09:00",
            xy=(10.0, 10.0),
            width=120.0,
            height=70.0,
        )

        # 2. Adding an all-day item (even with show=False) makes All-day row appear when show_all_day=None
        hidden_all_day = cal_auto.add(
            "2026-10-06",
            "2026-10-08",
            text="All-Day Conference",
            show=False,
        )
        _, cy_after_ad = cal_auto.get_slot_xy(
            "2026-10-05 09:00",
            xy=(10.0, 10.0),
            width=120.0,
            height=70.0,
        )
        cx_ad, cy_ad = cal_auto.get_slot_xy("2026-10-06", xy=(10.0, 10.0), width=120.0, height=70.0)
        cx_tm, cy_tm = cal_auto.get_slot_xy(
            "2026-10-06 12:00",
            xy=(10.0, 10.0),
            width=120.0,
            height=70.0,
        )
        assert cy_after_ad < cy_before_ad
        assert cx_ad == pytest.approx(cx_tm)
        assert cy_ad > cy_tm
        assert hidden_all_day.show is False

        # 3. Explicit show_all_day=True reserves the All-day row even with 0 all-day items
        cal_forced_on = WeekCalendar(
            start_date="2026-10-05",
            show_all_day=True,
            **_base_kwargs(),
        )
        _, cy_forced_on_9 = cal_forced_on.get_slot_xy(
            "2026-10-05 09:00",
            xy=(10.0, 10.0),
            width=120.0,
            height=70.0,
        )
        assert cy_forced_on_9 == pytest.approx(cy_after_ad)

        # 4. Explicit show_all_day=False hides the All-day row even when all-day items exist
        cal_forced_off = WeekCalendar(
            start_date="2026-10-05",
            show_all_day=False,
            **_base_kwargs(),
        )
        cal_forced_off.add("2026-10-05", "2026-10-07", text="Hidden All-Day")
        _, cy_forced_off_9 = cal_forced_off.get_slot_xy(
            "2026-10-05 09:00",
            xy=(10.0, 10.0),
            width=120.0,
            height=70.0,
        )
        assert cy_forced_off_9 == pytest.approx(cy_before_ad)

    def test_render_week_calendar_span_modes_and_overlaps(self) -> None:
        """Test rendering WeekCalendar with all-day bars, columns/box span_modes, and parallel overlaps."""
        cal = WeekCalendar(
            start_date="2026-10-08",
            end_date="2026-10-14",
            start_hour=9,
            end_hour=18,
            title="Week Schedule (Oct 8 - Oct 14)",
            sunday_text_style=Styles.PrimaryBold,
            saturday_text_style=Styles.SecondaryBold,
            **_base_kwargs(),
        )
        # All-day bars
        cal.add("2026-10-08", "2026-10-11", text="Cloud Next Summit")
        cal.add("2026-10-10", "2026-10-13", text="Code Freeze Window")

        # Multi-day timed ("columns" mode: 10th 09:00 to 13th 15:00)
        cal.add(
            "2026-10-10 09:00",
            "2026-10-13 15:00",
            text="On-Call Shift",
            description="10th 09:00 - 13th 15:00",
            span_mode="columns",
        )
        # Multi-day timed ("box" mode)
        cal.add(
            "2026-10-08 13:00",
            "2026-10-09 16:00",
            text="2-Day Workshop",
            span_mode="box",
        )
        # Overlapping single-day timed events
        cal.add("2026-10-14 10:00", "2026-10-14 12:30", text="API Review")
        cal.add("2026-10-14 11:00", "2026-10-14 13:30", text="Security Audit")

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "week.png"
            canvas.clear()
            canvas.setup(width=150, height=90)
            cal.draw(xy=(10.0, 10.0), width=130.0, height=70.0)
            canvas.save(str(out_path))
            assert out_path.exists()
            assert out_path.stat().st_size > 0


class TestDayCalendar:
    """Unit and rendering tests for DayCalendar in vertical and horizontal orientations."""

    @pytest.mark.parametrize("direction", ["vertical", "horizontal"])
    def test_vertical_and_horizontal_rendering_and_get_time_xy(
        self,
        direction: Literal["vertical", "horizontal"],
    ) -> None:
        """Test DayCalendar in both vertical and horizontal modes with overlapping events."""
        cal = DayCalendar(
            date="2026-10-10",
            direction=direction,
            start_hour=9,
            end_hour=18,
            hour_step=1,
            title=f"2026-10-10 ({direction})",
            **_base_kwargs(),
        )
        cal.add("2026-10-10", text="Release Freeze Day")
        cal.add("2026-10-10 09:00", "2026-10-10 10:30", text="Kickoff", description="Room A")
        cal.add("2026-10-10 10:00", "2026-10-10 12:00", text="DB Migration", description="Primary")
        cal.add("2026-10-10 13:00", "2026-10-10 15:30", text="Canary Verification")

        cx_ad, cy_ad = cal.get_time_xy("2026-10-10", xy=(10.0, 10.0), width=120.0, height=70.0)
        cx_t1, cy_t1 = cal.get_time_xy("2026-10-10 09:30", xy=(10.0, 10.0), width=120.0, height=70.0)
        cx_t2, cy_t2 = cal.get_time_xy("2026-10-10 16:30", xy=(10.0, 10.0), width=120.0, height=70.0)

        if direction == "vertical":
            assert cy_ad > cy_t1 > cy_t2
        else:
            assert cx_t2 > cx_t1
            assert cy_ad > cy_t1

        with pytest.raises(ValueError, match="does not match"):
            cal.get_time_xy("2026-10-11 10:00", xy=(10.0, 10.0), width=120.0, height=70.0)

        with pytest.raises(ValueError, match="outside"):
            cal.get_time_xy("2026-10-10 20:00", xy=(10.0, 10.0), width=120.0, height=70.0)

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / f"day_{direction}.png"
            canvas.clear()
            canvas.setup(width=140, height=90)
            cal.draw(xy=(10.0, 10.0), width=120.0, height=70.0)
            canvas.save(str(out_path))
            assert out_path.exists()
            assert out_path.stat().st_size > 0
