# Chapter 9: Quantitative Charts

`drawlib.charts` renders engineering roadmaps, project timelines, and metric visualizations with publication quality.

## 9.1 Gantt Charts (`GanttChart`)

Visualize sprint schedules, milestones, and task dependencies with automated arrow routing:

```drawlib 620px center file:fig_gantt_roadmap.png caption:"Figure 9.1: Core Platform Engineering Roadmap"
from drawlib.canvas import setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

setup(width=108, height=58)

chart = GanttChart(
    columns=["Apr", "May", "Jun", "Jul"],
    width=96.0,
    label_width=28.0,
    title="Core Platform Engineering Roadmap (2026)",
    header_height=6.0,
    row_height=5.0,
    bar_radius=1.0,
    axis_line_style=Styles.MutedDashed,
)

chart.add_section("1. Core Infrastructure")
t1 = chart.add_task("Architecture & Specs", start="Apr", end=0.9, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("Core Engine Implementation", start=0.7, end=2.2, style=Styles.PrimaryFlat, progress=0.8)

chart.add_section("2. Integration & Release")
t3 = chart.add_task("E2E Tests & Dogfooding", start=2.0, end=3.2, style=Styles.SecondaryFlat, progress=0.4)
t4 = chart.add_task("Production Deployment", start=3.0, end=3.9, style=Styles.SecondaryFlat, progress=0.0)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t3)
chart.add_milestone("Alpha Milestone", at=2.0, style=Styles.AccentFlat)
chart.add_marker(at=1.8, style=Styles.AccentFlat, label="Current Sprint")

chart.draw(xy=(6.0, 5.0))
```

## 9.2 Additional Chart Types

- **`BarChart`**: Vertical and horizontal bar plots with grouping and stacking.
- **`LineChart` / `AreaChart`**: Trend plots and multi-series metric tracking.
- **`PieChart`**: Proportional slices with smart label anti-collision.
- **`RadarChart`**: Multi-dimensional capability matrices.
- **`ScatterChart`**: Distribution plots, latency correlations, and cluster analysis.
