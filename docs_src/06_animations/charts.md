# Animating Charts

All 7 chart classes in `drawlib.charts` (`BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`) follow the **Pre-Build & Mutate** lifecycle:
1. Instantiate the chart and register all series, slices, or tasks **once** outside the loop (`s = chart.add_series(...)`, `sl = chart.add_slice(...)`, `t = chart.add_task(...)`).
2. Inside `with anim.frame():`, mutate `.show`, `.draw_ratio` (`0.0` to `1.0`), or `.draw_direction` (`"bottom_to_top"` or `"left_to_right"`), and call `chart.draw(xy=..., scale=1.0)`.

---

## 1. Progressive Series Reveal (`s.show`)

Because Drawlib computes automatic axis bounds (`min_value`, `max_value`, `tick_step`), pie proportions, and Gantt row heights across **all registered elements regardless of `show=False`**, toggling `s.show = True` across frames reveals series one by one without ever shifting or rescaling the chart axes:

```drawlib 650px center show-code file:anim_charts_series_reveal.png caption:"Progressive Multi-Series LineChart Reveal with Locked Y-Axis"
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

setup(width=105, height=66)
anim = Animation(fps=1.2)

chart = LineChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    width=80,
    height=44,
    title="Quarterly Throughput (K req/s)",
    title_style=Styles.BlackBold.patch(text_size=12.5),
    smooth=True,
)

s1 = chart.add_series("2024 Baseline", [42, 48, 54, 60], style=Styles.Secondary, line_style="dashed")
s2 = chart.add_series("2025 Target", [50, 65, 78, 92], style=Styles.Accent)
s3 = chart.add_series("2026 Actual", [55, 76, 94, 115], style=Styles.Primary, line_width=2.5)
series_list = [s1, s2, s3]

for step in range(len(series_list)):
    for i, s in enumerate(series_list):
        s.show = (i <= step)
    is_last = (step == len(series_list) - 1)
    with anim.frame(duration=2.5 if is_last else 0.9):
        chart.draw(xy=(12, 8))
        chart.draw_legend(xy=(18, 56), text_style=Styles.Muted.patch(text_size=8.5), orientation="horizontal")

save()
```

---

## 2. Partial Spatial Growth (`s.draw_ratio` & `s.draw_direction`)

Every `Series`, `Slice`, and `Task` supports built-in partial spatial rendering via `draw_ratio: float` (`0.0` to `1.0`) and `draw_direction: DrawDirection` (`"bottom_to_top"` or `"left_to_right"`):
- **`BarChart`**: `"bottom_to_top"` *(default)* grows all bars vertically from the baseline; `"left_to_right"` reveals bars sequentially category-by-category.
- **`LineChart` / `AreaChart`**: `"left_to_right"` *(default)* sweeps the curve continuously from left to right; `"bottom_to_top"` rises vertically from the baseline.
- **`PieChart`**: `"left_to_right"` *(default)* sweeps the wedge angularly; `"bottom_to_top"` expands radially outward.
- **`RadarChart`**: `"bottom_to_top"` *(default)* expands the polygon radially from the center; `"left_to_right"` sweeps spoke-by-spoke.

```drawlib 650px center show-code file:anim_charts_bar_growth.png caption:"Smooth BarChart Growth via s.draw_ratio"
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=105, height=64)
anim = Animation(fps=10.0)

chart = BarChart(
    categories=["Gateway", "Auth", "Catalog", "Checkout"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    width=80,
    height=44,
    title="Service Cache Hit Ratio (%)",
    title_style=Styles.BlackBold.patch(text_size=12.5),
    r=0.8,
)
chart.configure_y_axis(min_value=0, max_value=100, unit="%")

s1 = chart.add_series("2025 Baseline", [65, 50, 75, 58], style=Styles.SecondaryNeutral)
s2 = chart.add_series("2026 Optimized", [92, 78, 96, 84], style=Styles.PrimaryFlat)

for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
    s2.draw_ratio = r
    is_last = (r == 1.0)
    with anim.frame(duration=2.2 if is_last else 0.12):
        chart.draw(xy=(12, 8))
        chart.draw_legend(xy=(24, 56), text_style=Styles.Muted.patch(text_size=8.5), orientation="horizontal")

save()
```

---

## 3. Project Schedule Reveal (`GanttChart`)

In `GanttChart`, mutating `task.show` and `task.draw_ratio` (`draw_direction="left_to_right"`) reveals and extends task bars along the timeline while keeping all row lanes and column headers fixed:

```drawlib 650px center show-code file:anim_charts_gantt_reveal.png caption:"GanttChart Progressive Task Schedule Reveal"
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

setup(width=110, height=56)
anim = Animation(fps=8.0)

gantt = GanttChart(
    columns=["W1", "W2", "W3", "W4", "W5"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Black.patch(text_size=9.0),
    grid_style=Styles.MutedThin,
    header_style=Styles.MutedThin,
    zebra_style=Styles.MutedThin,
    width=94.0,
    label_width=28.0,
    header_height=6.0,
    row_height=6.0,
    title="Release Rollout Schedule",
    title_style=Styles.BlackBold.patch(text_size=12.5),
    bar_radius=1.0,
)

t1 = gantt.add_task("1. Schema Design", start="W1", end=1.2, style=Styles.PrimaryNeutral)
t2 = gantt.add_task("2. Core Engine", start="W2", end=3.2, style=Styles.PrimaryFlat, show=False)
t3 = gantt.add_task("3. Production GA", start="W4", end=4.8, style=Styles.SecondaryNeutral, show=False)
tasks = [t1, t2, t3]

for idx, active_task in enumerate(tasks):
    active_task.show = True
    for r in [0.4, 0.8, 1.0]:
        active_task.draw_ratio = r
        is_final = (idx == len(tasks) - 1 and r == 1.0)
        with anim.frame(duration=2.5 if is_final else 0.14):
            gantt.draw(xy=(8, 8))

save()
```
