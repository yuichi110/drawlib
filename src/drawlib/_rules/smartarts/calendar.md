# Drawlib Calendar SmartArt Guidelines (`lib-smartarts-calendar`)

Drawlib provides three Outlook / Google Calendar-style schedule components—**`MonthCalendar`**, **`WeekCalendar`**, and **`DayCalendar`**—along with the mutable **`CalendarItem`** model.

---

## 1. Strict ISO 8601 Date/Datetime Format & Anchor Rules

- **Strict ISO 8601 Strings Only**:
  All Calendar constructors, `.add()`, and coordinate query methods (`get_date_xy`, `get_slot_xy`, `get_time_xy`) accept **only two formats** (slash-separated dates like `"2026/10/10"` or time-only strings like `"09:00"` raise a `ValueError`):
  1. **`"YYYY-MM-DD"`** (e.g. `"2026-10-10"`): Treated automatically as an **All-Day (`全日`)** date or multi-day date span.
  2. **`"YYYY-MM-DD HH:MM"`** (e.g. `"2026-10-10 09:00"`): Treated automatically as a **Timed (`時間指定`)** slot or multi-day continuous datetime span.
- **Anchor (`align`)**:
  All three calendars default to `align="bottom_left"` and also support `align="center"` and `align="top_left"`.
- **Important — `sunday_text_style` and `saturday_text_style` Scope**:
  Only **`MonthCalendar`** and **`WeekCalendar`** accept `sunday_text_style` and `saturday_text_style`. **`DayCalendar` does NOT accept `sunday_text_style` or `saturday_text_style`** (passing them to `DayCalendar` raises a validation error).

---

## 2. `CalendarItem` Model

Every `.add(...)` call on `MonthCalendar`, `WeekCalendar`, or `DayCalendar` returns a mutable `CalendarItem` (and appends it to `.items`):

```python
class CalendarItem(BaseModel):
    start: str                                                 # "YYYY-MM-DD" or "YYYY-MM-DD HH:MM"
    end: str | None = None                                     # Optional end date/datetime
    text: str = ""                                             # Primary event label
    description: str = ""                                      # Optional secondary subtitle/note
    all_day: bool | None = None                                # Explicit All-Day override
    span_mode: Literal["columns", "box", "all_day"] = "columns" # Multi-day timed mode in WeekCalendar
    style: Style                                               # Event bar/box style
    text_style: Style                                          # Primary label text style
    description_style: Style | None = None                     # Secondary subtitle text style
    show: bool = True                                          # Layout-preserving visibility flag
```

---

## 3. Component 1: `MonthCalendar`

`MonthCalendar` renders a 7-column monthly (`end_date=None`) or multi-week cross-month (`end_date="YYYY-MM-DD"`) calendar grid with automatic cross-week wrapping (`←` / `→`) and vertical lane stacking (`max_tracks`) for overlapping multi-day bars.

```python
mcal = MonthCalendar(
    *,
    start_date: str = "2026-10-01",
    end_date: str | None = None,
    first_weekday: Literal["sun", "mon"] = "sun",
    title: str | None = None,             # None auto-generates month title; "" hides title bar
    lang: Literal["en", "ja"] = "en",
    max_tracks: int = 3,                  # Max stacked event bar tracks per week row
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
)

item = mcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

cx, cy = mcal.get_date_xy(
    date: str,                            # "YYYY-MM-DD"
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: float = 1.0,
) -> tuple[float, float]

mcal.draw(
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

---

## 4. Component 2: `WeekCalendar`

`WeekCalendar` renders a multi-day time-grid calendar (`start_date`, `end_date` or `num_days=7`, plus optional custom `columns` header labels) with a top **"All-day" (`全日`)** banner (`show_all_day=None` auto-shows when `>= 1` all-day item exists; customize gutter text via `all_day_label`) and multi-day timed `span_mode="columns" | "box" | "all_day"`.

```python
wcal = WeekCalendar(
    *,
    start_date: str = "2026-10-11",
    end_date: str | None = None,
    num_days: int = 7,
    columns: list[str] | None = None,     # Optional custom column header labels matching displayed days
    start_hour: int = 9,
    end_hour: int = 18,
    hour_step: int = 1,
    show_all_day: bool | None = None,
    all_day_label: str | None = None,     # Defaults to "All-day" (en) or "全日" (ja)
    title: str | None = None,             # None auto-generates date range title; "" hides title bar
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
)

item = wcal.add(
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
) -> CalendarItem

cx, cy = wcal.get_slot_xy(
    dt: str,                              # "YYYY-MM-DD" (all-day) or "YYYY-MM-DD HH:MM" (time slot)
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: float = 1.0,
) -> tuple[float, float]

wcal.draw(
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

---

## 5. Component 3: `DayCalendar`

`DayCalendar` renders a single-day schedule in either `direction="vertical"` (default, top-to-bottom time axis with automatic X-axis parallel lane splitting) or `direction="horizontal"` (left-to-right time axis with automatic Y-axis parallel lane splitting, ideal for 16:9 slides and wide Hero banners).

```python
dcal = DayCalendar(
    *,
    date: str = "2026-10-13",
    direction: Literal["vertical", "horizontal"] = "vertical",
    start_hour: int = 9,
    end_hour: int = 18,
    hour_step: int = 1,
    show_all_day: bool | None = None,
    all_day_label: str | None = None,     # Defaults to "All-day" (en) or "全日" (ja)
    title: str | None = None,             # None auto-generates weekday & date; "" hides title bar
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
)

item = dcal.add(
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
) -> CalendarItem

cx, cy = dcal.get_time_xy(
    dt: str,                              # "YYYY-MM-DD" (all-day) or "YYYY-MM-DD HH:MM" (time slot)
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: float = 1.0,
) -> tuple[float, float]

dcal.draw(
    xy: tuple[float, float],
    width: float = 100.0,
    height: float = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

---

## 6. Production Example: `WeekCalendar` & Horizontal `DayCalendar`

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.smartarts import DayCalendar, WeekCalendar
from drawlib.styles import Styles

setup(width=136, height=62)

line((68.0, 4.0), (68.0, 58.0), style=Styles.MutedDashed)

# 1. Left: WeekCalendar (3-Day Release Window with Top All-Day Bar + Timed Slots)
wcal = WeekCalendar(
    start_date="2026-10-12",
    end_date="2026-10-14",
    start_hour=9,
    end_hour=18,
    hour_step=3,
    show_all_day=None,
    all_day_label="Freeze",
    title="Release Window (Oct 12 – Oct 14)",
    lang="en",
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=9.5),
    header_style=Styles.SecondaryNeutral,
    header_text_style=Styles.DarkBold.patch(text_size=9.5),
    border_style=Styles.Neutral,
    event_style=Styles.SecondaryNeutral,
    event_text_style=Styles.DarkBold.patch(text_size=9.5),
    sunday_text_style=Styles.DangerBold.patch(text_size=9.5),
    saturday_text_style=Styles.PrimaryBold.patch(text_size=9.5),
)
wcal.add("2026-10-12", "2026-10-14", text="Code Freeze Window", style=Styles.PrimaryNeutral)
wcal.add("2026-10-12 09:30", "2026-10-12 12:30", text="Planning")
wcal.add(
    "2026-10-13 13:00",
    "2026-10-14 16:00",
    text="Canary Rollout",
    span_mode="columns",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
wcal.draw(xy=(4.0, 5.0), width=60.5, height=52.0)

# 2. Right: DayCalendar (Horizontal Timeline — no sunday_text_style / saturday_text_style)
dcal = DayCalendar(
    date="2026-10-14",
    direction="horizontal",
    start_hour=9,
    end_hour=18,
    hour_step=3,
    show_all_day=None,
    title="Oct 14 — Production Cutover Schedule",
    lang="en",
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=9.5),
    header_style=Styles.SecondaryNeutral,
    header_text_style=Styles.DarkBold.patch(text_size=9.5),
    border_style=Styles.Neutral,
    event_style=Styles.SecondaryNeutral,
    event_text_style=Styles.DarkBold.patch(text_size=9.5),
)
dcal.add("2026-10-14", text="Change Freeze Active (All-Day)", style=Styles.PrimaryNeutral)
dcal.add("2026-10-14 09:00", "2026-10-14 12:00", text="DB Snapshot")
dcal.add("2026-10-14 11:00", "2026-10-14 14:30", text="Shadow Traffic")
dcal.add(
    "2026-10-14 14:30",
    "2026-10-14 17:30",
    text="Primary Cutover",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
dcal.draw(xy=(71.5, 5.0), width=60.5, height=52.0)

save()
```
