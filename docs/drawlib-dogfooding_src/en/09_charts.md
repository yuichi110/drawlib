# Chapter 9: Quantitative Charts

`drawlib.charts` renders engineering roadmaps, project timelines, and metric visualizations with publication quality. Every chart anchors its bounding container at the **bottom-left coordinate `(x0, y0)`** via `.draw(xy=...)`.

## 9.1 Gantt Charts (`GanttChart`)

Visualize sprint schedules, milestones, and task dependencies with automated arrow routing:

```drawlib align=center file=fig_gantt_roadmap.png caption="Figure 9.1: Core Platform Engineering Roadmap"
from drawlib.canvas import save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

setup(width=112, height=62)

chart = GanttChart(
    columns=["Apr", "May", "Jun", "Jul"],
    width=102.0,
    label_width=32.0,
    title="Core Platform Engineering Roadmap (2026)",
    title_style=Styles.DarkBold.patch(text_size=12.0),
    header_height=6.0,
    row_height=5.2,
    bar_radius=1.0,
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    header_style=Styles.PrimaryNeutral,
    grid_style=Styles.MutedDashed,
    zebra_style=Styles.Neutral,
    progress_text_style=Styles.WhiteBold.patch(text_size=9.5),
)

chart.add_section("1. Core Infrastructure", style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=10.0))
t1 = chart.add_task("Architecture & Specs", start="Apr", end=0.9, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("Core Engine Implementation", start=0.7, end=2.2, style=Styles.PrimaryFlat, progress=0.8)

chart.add_section("2. Integration & Release", style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=10.0))
t3 = chart.add_task("E2E Tests & Dogfooding", start=2.0, end=3.2, style=Styles.SecondaryFlat, progress=0.4)
t4 = chart.add_task("Production Deployment", start=3.0, end=3.9, style=Styles.SecondaryFlat, progress=0.0)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t3)
chart.add_milestone("Alpha Milestone", at=2.0, style=Styles.AccentFlat)
chart.add_marker(at=1.8, style=Styles.Accent, label="Current Sprint", label_style=Styles.WhiteBold.patch(text_size=9.5))

chart.draw(xy=(5.0, 5.0))
save()
```

## 9.2 Additional Chart Types

- **`BarChart`**: Vertical and horizontal bar plots with grouping (`bar_mode="group"`), stacking (`bar_mode="stack"`), outer corner rounding (`bar_r`), and logarithmic axes (`Axis(scale="log")`).
- **`LineChart` / `AreaChart`**: Continuous trend plots and multi-series tracking with smooth spline interpolation (`smooth=True`) and overlapping or stacked area volumes.
- **`PieChart`**: Proportional sector compositions supporting donut rings (`hole_ratio`), center KPI badges (`center_text`), and exploded slice callouts (`explode`).
- **`RadarChart`**: Multivariate capability and architecture trade-off matrices (polygon and circular grid contours).
- **`ScatterChart`**: 2D coordinate scatter plots and 3-variable bubble charts (`(x, y, radius)`) with logarithmic axis scaling (`Axis(scale="log")`) for latency and throughput correlation analysis.
