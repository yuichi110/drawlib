::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Categorical & Trend Charts (`BarChart`, `LineChart`, `AreaChart`)
:::

::: block (80, 140) (660, 840) compact
## Cartesian Data Visualization

### 1. `BarChart` — Grouped, Stacked & Log Scales
- Supports `orientation="vertical" | "horizontal"` and `bar_mode="group" | "stack"`.
- Rounded bar corners (`r=0.8`), direct value labels (`value_format="{:.0f}M"`), and linear or logarithmic (`scale="log"`) axes.

### 2. `LineChart` — Linear Polylines & Smooth Splines
- Set `smooth=True` for cubic-like spline interpolation or `smooth=False` for exact vertex segments.
- Per-series `line_style` (`"solid"`, `"dashed"`, `"dotted"`), `line_width`, and `point_shape` (`"circle"`, `"square"`, `"none"`).

### 3. `AreaChart` — Cumulative & Overlapping Streams
- `mode="stack"` layers series cumulatively to show total volume breakdown; `mode="overlap"` renders semi-transparent overlapping polygons (`fill_alpha=0.35`).
- Shared fluent helpers across all three: `configure_x_axis(...)`, `configure_y_axis(...)`, and standalone `draw_legend(xy, ...)`.
:::

::: block (780, 140) (1060, 840)
```drawlib file:bar_line_area.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.area import AreaChart
from drawlib.charts.bar import BarChart
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

clear()
setup(width=106, height=84)

# 1. Top-Left: Grouped BarChart
bar = BarChart(
    axis_line_style=Styles.Dark,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=48.0,
    height=34.0,
    title="1. BarChart (bar_mode='group')",
    title_style=Styles.DarkBold.patch(text_size=8.8),
    bar_mode="group",
    bar_width_ratio=0.72,
    r=0.6,
    axis_text_style=Styles.Muted.patch(text_size=7.2),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.DarkBold.patch(text_size=6.5),
    value_format="{:.0f}",
    background_style=Styles.NeutralFlat,
)
bar.add_series("Cloud ARR", [45, 58, 74, 92], style=Styles.PrimaryFlat)
bar.add_series("Services", [20, 24, 22, 26], style=Styles.SecondaryFlat)
bar.configure_y_axis(min_value=0, max_value=100, tick_step=25, unit="M$")
bar.draw(xy=(3.0, 45.0))
bar.draw_legend(xy=(12.0, 80.0), text_style=Styles.Dark.patch(text_size=7.2), orientation="horizontal")

# 2. Top-Right: Smooth Spline LineChart
line_chart = LineChart(
    axis_line_style=Styles.Dark,
    categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    width=48.0,
    height=34.0,
    title="2. LineChart (smooth=True)",
    title_style=Styles.DarkBold.patch(text_size=8.8),
    smooth=True,
    show_points=True,
    point_shape="circle",
    point_size=0.65,
    axis_text_style=Styles.Muted.patch(text_size=7.2),
    grid_style=Styles.MutedDashed,
    background_style=Styles.NeutralFlat,
)
line_chart.add_series("Primary Cluster", [24, 19, 62, 86, 74, 42], style=Styles.PrimaryFlat, line_width=2.0)
line_chart.add_series(
    "Read Replica",
    [15, 12, 38, 56, 48, 28],
    style=Styles.SecondaryFlat,
    line_style="dashed",
    point_shape="square",
)
line_chart.configure_y_axis(min_value=0, max_value=100, tick_step=25, unit="%")
line_chart.draw(xy=(55.0, 45.0))
line_chart.draw_legend(xy=(61.0, 80.0), text_style=Styles.Dark.patch(text_size=7.2), orientation="horizontal")

# 3. Bottom Full-Width: Stacked AreaChart
area = AreaChart(
    axis_line_style=Styles.Dark,
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    width=100.0,
    height=33.0,
    title="3. AreaChart (mode='stack', fill_alpha=0.65) — Multi-Region Bandwidth",
    title_style=Styles.DarkBold.patch(text_size=9.0),
    mode="stack",
    fill_alpha=0.65,
    show_points=True,
    point_shape="circle",
    point_size=0.55,
    axis_text_style=Styles.Muted.patch(text_size=7.5),
    grid_style=Styles.MutedDashed,
    background_style=Styles.NeutralFlat,
)
area.add_series("North America", [120, 145, 170, 210, 250, 290], style=Styles.PrimaryFlat)
area.add_series("Europe (EU)", [80, 95, 115, 135, 160, 185], style=Styles.SecondaryFlat)
area.add_series("Asia-Pacific", [50, 65, 85, 110, 140, 175], style=Styles.AccentFlat)
area.configure_y_axis(min_value=0, max_value=700, tick_step=175, unit=" Gbps")
area.draw(xy=(3.0, 4.0))
area.draw_legend(xy=(28.0, 38.0), text_style=Styles.Dark.patch(text_size=7.5), orientation="horizontal")

save()
```
:::

::: note
- This slide demonstrates the three core Cartesian categorical/trend chart types: `BarChart`, `LineChart`, and `AreaChart`.
- **Top-Left (`BarChart`)**: Compares quarterly Cloud ARR vs. Services revenue using `bar_mode="group"`, rounded corners (`r=0.6`), and direct value labels above each bar.
- **Top-Right (`LineChart`)**: Plots 24-hour CPU utilization across a Primary Cluster (solid smooth spline curve with circle markers) and a Read Replica (dashed curve with square markers).
- **Bottom (`AreaChart`)**: Visualizes cumulative regional network bandwidth in `mode="stack"` with `fill_alpha=0.65`, showing both individual region contributions and the aggregate global bandwidth envelope.
:::
