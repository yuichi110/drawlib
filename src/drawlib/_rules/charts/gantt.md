# Drawlib GanttChart Guidelines (`lib-charts-gantt`)

`GanttChart` (`drawlib.charts.gantt`) provides declarative, vector-grade project roadmaps, sprint schedules, and milestone timelines. Timeline intervals are structured horizontally along the X-axis while section divider banners, task rows, and milestones stack sequentially downwards along the Y-axis.

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.gantt import (
    Dependency,
    DrawDirection,
    GanttChart,
    Marker,
    Milestone,
    Section,
    Task,
)
```

```text
  Task / Milestone         Sprint 1       Sprint 2       Sprint 3       Sprint 4
 ┌──────────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
 │ ▼ Core Engine        │              │              │              │              │
 │ Database Migration   │ [██████████] │              │              │              │
 │ API Gateway V2       │       └──────┼───────────►[████████]       │              │
 │ ◆ Beta Code Freeze   │              │              │       ◆      │              │
 └──────────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                                                       │
                                                Today's Marker
```

- **Time Coordinate Indexing (`start`, `end`, `at`)**:
  - **Column Name String**: Matches an exact string in `columns` (`start="Apr"` resolves to the left edge of `"Apr"`, `end="Apr"` resolves to the right edge of `"Apr"`, and `at="Jun"` resolves to the midpoint of `"Jun"`).
  - **Floating-Point Offset**: `0.0` is the left edge of column `0`, `1.0` is the boundary between column `0` and column `1`, `1.5` is the midpoint of column `1`, etc.
- **Task Completion Progress (`progress`)**: Clamped to `[0.0, 1.0]`. When `progress > 0`, the full scheduled duration is drawn as a translucent tint (`alpha=0.28`) while the completed portion (`progress * width`) is drawn with the solid `style`.
- **Dependency Visibility Cascading (`show`)**: Hiding a `Task` (`task.show = False` or `task.draw_ratio = 0.0`) preserves its row position and **automatically hides any `Dependency` arrows** connected to `from_task` or `to_task`.

---

## 2. Constructor Parameters (`GanttChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`columns`** | `list[str]` | **Required** | Ordered timeline interval labels along the top header band (**at least 1 required**). |
| **`axis_line_style`** | `Style` | **Required** | Style for column divider lines and header baseline. Mandatory anchor. |
| `axis_text_style` | `Style \| None` | `None` | Style for column header labels and left-column task/milestone labels. If `None`, labels are omitted. |
| `header_style` | `Style \| None` | `None` | Style overriding the top column header row background card. If `None`, header card fill is omitted. |
| `grid_style` | `Style \| None` | `None` | Style for vertical timeline column separator lines across rows. If `None`, vertical lines are omitted. |
| `zebra_style` | `Style \| None` | `None` | Style for alternating horizontal row background stripes. If `None`, zebra striping is omitted. |
| `progress_text_style` | `Style \| None` | `None` | Default style for task completion percentage text (`"85%"`). If `None`, progress text is omitted. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |
| `width` | `float` | `90.0` | Overall chart bounding box width in canvas units. |
| `height` | `float \| None` | `None` | Overall height. If `None` *(default)*, calculated dynamically from total row count (minimum `20.0`). |
| `row_height` | `float` | `4.5` | Vertical height per task, milestone, or section row. |
| `header_height` | `float` | `5.5` | Height of the top column header band. |
| `label_width` | `float` | `24.0` | Horizontal width allocated for the left task/milestone name column. |
| `bar_radius` | `float` | `0.8` | Corner rounding radius for task bars (when `task.style.shape_r` is `None`). |

---

## 3. Methods, Properties & Schedule Models

### 3.1 Methods
- **`add_section(name: str, style: Style | None = None, text_style: Style | None = None, *, show: bool = True) -> Section`**:
  Adds a category section divider row and returns the mutable `Section` instance (`style` overrides the banner rectangle appearance; `text_style` overrides `chart.axis_text_style` for the section title).
- **`add_task(name: str, start: str | float, end: str | float, style: Style, progress: float = 0.0, progress_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Task`**:
  Adds a scheduled task bar row and returns the mutable `Task` instance.
  - `progress_text_style`: Per-task override for completion percentage text (falls back to `chart.progress_text_style`).
  - `draw_direction`: `"left_to_right"` *(default)* extends the task bar horizontally from `start` toward `end`; `"bottom_to_top"` grows the bar vertically from its bottom edge.
- **`add_milestone(name: str, at: str | float, style: Style, *, show: bool = True) -> Milestone`**:
  Adds a milestone row with a diamond marker anchored at `at` and returns the mutable `Milestone` instance.
- **`add_marker(at: str | float, style: Style, label: str = "", label_style: Style | None = None, *, show: bool = True) -> Marker`**:
  Adds a full-height vertical reference line at `at` with an optional top badge (`label` + `label_style`) and returns the mutable `Marker` instance.
- **`add_dependency(from_task: Task, to_task: Task, style: Style | None = None, *, show: bool = True) -> Dependency`**:
  Adds an orthogonal dependency arrow connecting `from_task` to `to_task` and returns the mutable `Dependency` instance.
- **`get_size() -> tuple[float, float]`**:
  Returns total computed `(width, height)` dimensions.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the Gantt chart onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary size overrides and uniform `scale`.

### 3.2 Properties & Schedule Models (`Section`, `Task`, `Milestone`, `Marker`, `Dependency`)
- **`chart.columns -> list[str]`**: Copy of timeline column labels.
- **`chart.items -> list[Task | Section | Milestone]`**: Copy of registered schedule rows in top-to-bottom order.
- **`chart.markers -> list[Marker]`**: Copy of registered vertical reference markers.
- **`chart.dependencies -> list[Dependency]`**: Copy of registered task dependency arrows.
- **Data Models**:
  - `Section(name: str, style: Style | None = None, text_style: Style | None = None, show: bool = True)`
  - `Task(name: str, start: str | float, end: str | float, style: Style, progress: float = 0.0, progress_text_style: Style | None = None, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right")`
  - `Milestone(name: str, at: str | float, style: Style, show: bool = True)`
  - `Marker(at: str | float, style: Style, label: str = "", label_style: Style | None = None, show: bool = True)`
  - `Dependency(from_task: Task, to_task: Task, style: Style | None = None, show: bool = True)`

---

## 4. Production Examples

### Example 4.1: Engineering Release Roadmap with Sections, Dependencies & Marker
```drawlib code=show align=center file=rules_gantt_roadmap.png caption="Engineering Release Roadmap with Dependencies and Today Marker"
from drawlib.canvas import save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

setup(width=118, height=85)

chart = GanttChart(
    columns=["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Black.patch(text_size=10.5),
    grid_style=Styles.MutedThin,
    header_style=Styles.Neutral,
    zebra_style=Styles.NeutralFlat,
    progress_text_style=Styles.WhiteBold.patch(text_size=10.0),
    width=106.0,
    label_width=32.0,
    title="Core Platform Engineering Roadmap (2026)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    header_height=6.0,
    row_height=5.0,
    bar_radius=1.0,
)

chart.add_section("1. Architecture & Core Services", text_style=Styles.BlackBold.patch(text_size=10.5))
t1 = chart.add_task("Spec & Protocol Definition", start="Apr", end=1.0, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("Storage Engine Overhaul", start=1.0, end=2.5, style=Styles.PrimaryFlat, progress=0.85)
t3 = chart.add_task(
    "Distributed Consensus Protocol",
    start=1.5,
    end=3.0,
    style=Styles.PrimaryNeutral,
    progress=0.45,
    progress_text_style=Styles.DarkBold.patch(text_size=10.0),
)

chart.add_section("2. APIs & Observability", text_style=Styles.BlackBold.patch(text_size=10.5))
t4 = chart.add_task(
    "gRPC & HTTP/3 Gateway",
    start=3.0,
    end=4.5,
    style=Styles.SecondaryNeutral,
    progress=0.35,
    progress_text_style=Styles.DarkBold.patch(text_size=10.0),
)
t5 = chart.add_task("Distributed Tracing Exporter", start=3.5, end=5.2, style=Styles.Neutral, progress=0.0)

chart.add_milestone("Alpha Architecture Freeze", at="Jun", style=Styles.PrimaryFlat)
chart.add_milestone("Public Beta Launch", at=4.5, style=Styles.PrimaryFlat)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t4)
chart.add_dependency(t3, t4)
chart.add_marker(at=1.7, style=Styles.DarkDashed, label="Today (Mid-May)", label_style=Styles.WhiteBold.patch(text_size=10.0))

chart.draw(xy=(6.0, 10.0))
save()
```

### Example 4.2: Agile Sprint Schedule with Per-Task Progress Styling
```drawlib code=show align=center file=rules_gantt_sprint_schedule.png caption="Agile Sprint Schedule with GanttChart"
from drawlib.canvas import save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

setup(width=115, height=66)

chart = GanttChart(
    columns=["Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Black.patch(text_size=10.5),
    grid_style=Styles.MutedThin,
    header_style=Styles.Neutral,
    progress_text_style=Styles.WhiteBold.patch(text_size=10.0),
    width=103.0,
    label_width=28.0,
    title="Q3 Core Feature Sprints",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    bar_radius=1.2,
)

s1 = chart.add_task("Auth Microservice", start=0.0, end=1.2, style=Styles.PrimaryFlat, progress=1.0)
s2 = chart.add_task(
    "Payment Gateway",
    start=1.2,
    end=2.6,
    style=Styles.SecondaryNeutral,
    progress=0.6,
    progress_text_style=Styles.DarkBold.patch(text_size=10.0),
)
s3 = chart.add_task(
    "Load Testing & Tuning",
    start=2.5,
    end=3.8,
    style=Styles.Neutral,
    progress=0.25,
    progress_text_style=Styles.DarkBold.patch(text_size=10.0),
)

chart.add_dependency(s1, s2)
chart.add_dependency(s2, s3)
chart.add_milestone("Feature Complete", at=3.0, style=Styles.PrimaryFlat)

chart.draw(xy=(6.0, 12.0))
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Bar Charts: `uv run drawlib rules show lib-charts-bar`
- Sequence Diagrams: `uv run drawlib rules show lib-diagrams-sequence`
