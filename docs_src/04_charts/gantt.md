# GanttChart: Project Roadmaps, Milestones & Dependencies

`GanttChart` provides declarative, vector-grade project roadmaps, sprint schedules, and milestone timelines. Drawing inspiration from sequence diagrams, timeline intervals are structured horizontally along the X-axis while task rows, section divider banners, and milestones stack sequentially downwards.

---

## 1. Overview & Structural Hierarchy

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

- **Section Dividers (`add_section`)**: Categorize tasks into functional domains (e.g. "Core Engine", "Observability").
- **Task Bars (`add_task`)**: Represent working durations with optional percentage completion progress bars (`progress=0.85`).
- **Milestones (`add_milestone`)**: Diamond marker indicators representing key delivery dates or code freezes.
- **Vertical Time Markers (`add_marker`)**: Full-height vertical indicators highlighting the current date or sprint boundaries.
- **Dependency Connectors (`add_dependency`)**: Orthogonal routing arrows linking prerequisite tasks to downstream deliverables.

---

## 2. Constructor & Configuration

```python
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

chart = GanttChart(
    columns=["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Black.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    header_style=Styles.MutedThin,
    zebra_style=Styles.MutedThin,
    progress_text_style=Styles.WhiteBold.patch(text_size=8.5),
    width=95.0,                 # Total chart bounding width
    label_width=28.0,           # Width reserved for task label column
    header_height=6.0,          # Height of the top timeline header band
    row_height=5.0,             # Height allocated per task/milestone row
    title="Engineering Roadmap (2026)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    bar_radius=1.0,             # Rounded corners for task duration bars
)

# Register sections, tasks, milestones, markers, and dependencies with visibility & partial rendering
sec = chart.add_section("1. Core Services", show=True)
t1 = chart.add_task(
    "Storage Engine",
    start="Apr",
    end=2.2,
    style=Styles.PrimaryFlat,
    progress=0.85,
    show=True,
    draw_ratio=1.0,
    draw_direction="left_to_right",  # "left_to_right" (duration extension) or "bottom_to_top" (vertical bar growth)
)
m1 = chart.add_milestone("Alpha Freeze", at="Jun", style=Styles.PrimaryFlat, show=True)
mk = chart.add_marker(at=1.7, style=Styles.DarkDashed, label="Today", show=True)
dep = chart.add_dependency(t1, t1, show=True)

# Render chart with optional dimension overrides and uniform proportional scaling
chart.draw(xy=(8.0, 10.0), width=None, height=None, scale=1.0)
```

---

## 3. Engineering Release Roadmap with Dependencies

The following complete example demonstrates sections, tasks with progress indicators, milestones, dependency arrows, and a "Today" marker:

```drawlib 650px center file:gantt_chart_roadmap.png caption:"Engineering Release Roadmap with Dependencies"
from drawlib import canvas
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=110, height=85)

chart = GanttChart(
    columns=["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Black.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    header_style=Styles.MutedThin,
    zebra_style=Styles.MutedThin,
    progress_text_style=Styles.WhiteBold.patch(text_size=8.5),
    width=95.0,
    label_width=28.0,
    title="Core Platform Engineering Roadmap (2026)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    header_height=6.0,
    row_height=5.0,
    bar_radius=1.0,
)

# 1. Core Services Section
chart.add_section("1. Architecture & Core Services")
t1 = chart.add_task("Spec & Protocol Definition", start="Apr", end=0.8, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("Storage Engine Overhaul", start=0.6, end=2.2, style=Styles.PrimaryFlat, progress=0.85)
t3 = chart.add_task("Distributed Consensus Protocol", start=1.5, end=3.2, style=Styles.PrimaryFlat, progress=0.4)

# 2. APIs & Observability Section
chart.add_section("2. APIs & Observability")
t4 = chart.add_task("gRPC & HTTP/3 Gateway", start=2.5, end=4.0, style=Styles.SecondaryNeutral, progress=0.2)
t5 = chart.add_task("Distributed Tracing Exporter", start=3.2, end=4.8, style=Styles.SecondaryNeutral, progress=0.0)

# 3. Milestones & Today Marker
chart.add_milestone("Alpha Architecture Freeze", at="Jun", style=Styles.PrimaryFlat)
chart.add_milestone("Public Beta Launch", at=4.0, style=Styles.PrimaryFlat)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t4)
chart.add_dependency(t3, t4)
chart.add_marker(at=1.7, style=Styles.DarkDashed, label="Today (Mid-May)")

chart.draw(xy=(8.0, 10.0))
```

---

## 4. Time Coordinate Indexing

In `GanttChart`, time coordinates can be passed as:
1. **Column Name String**: Matches the exact string in `columns` (e.g., `start="Apr"` aligns with the beginning of the "Apr" column).
2. **Floating-point Offset**: `0.0` represents the left edge of the first column, `1.0` is the start of the second column, `1.5` is halfway through the second column, etc.

---

## 5. Agile Sprint Schedule with Status Theming

Tasks can also accept explicit styles to designate project phases, teams, or status:

```drawlib 650px center file:gantt_chart_sprint_schedule.png caption:"Agile Sprint Schedule with Status Theming"
from drawlib import canvas
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=100, height=70)

chart = GanttChart(
    columns=["Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Black.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    header_style=Styles.MutedThin,
    progress_text_style=Styles.WhiteBold.patch(text_size=8.5),
    width=88.0,
    label_width=24.0,
    title="Q3 Core Feature Sprints",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    bar_radius=1.2,
)

s1 = chart.add_task("Auth Microservice", start=0.0, end=1.8, style=Styles.PrimaryFlat, progress=1.0)
s2 = chart.add_task("Payment Gateway", start=1.2, end=3.0, style=Styles.SecondaryNeutral, progress=0.6)
s3 = chart.add_task("Load Testing & Tuning", start=2.5, end=4.0, style=Styles.Neutral, progress=0.1)

chart.add_dependency(s1, s2)
chart.add_milestone("Feature Complete", at=3.0, style=Styles.PrimaryFlat)

chart.draw(xy=(6.0, 15.0))
```
