# 8. Quantitative Charts: 10 Pure-Python Chart Types

Technical whitepapers, benchmark reports, and architecture reviews rarely stop at box-and-arrow diagrams—they need rigorous quantitative evidence. `drawlib.charts` provides **10 pure-Python chart types** built natively on Drawlib's rendering engine, all anchored at **Bottom-Left `(x0, y0)`** (`align="bottom_left"`) so charts sit alongside `SmartArts`, icons, and architecture callouts on a single unified canvas.

```drawlib align=center code=fold file=charts_bar_line.png caption="Figure 8.1: Side-by-Side Quantitative Dashboard — Grouped BarChart Throughput and LineChart Tail Latency"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.charts.line import LineChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=152, height=62)

card_bg = Styles.White.patch(shape_r=2.0, shape_line_color=Colors.Gray3)
rectangle((40.0, 31.0), width=68.0, height=50.0, style=card_bg)
rectangle((112.0, 31.0), width=68.0, height=50.0, style=card_bg)

bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Doc", "Site", "Catalog", "Slide"],
    width=62.0,
    height=38.0,
    bar_mode="group",
    bar_width_ratio=0.68,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=10.0),
    value_format="{:.0f}",
    title="Build Throughput (Pages / sec)",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
bar.add_series("v0.3.0 Baseline", [18.0, 24.0, 21.0, 29.0], style=Styles.SecondaryNeutral)
bar.add_series("v0.3.10 Cached", [42.0, 56.0, 49.0, 64.0], style=Styles.PrimaryFlat)
bar.configure_y_axis(min_value=0.0, max_value=80.0, tick_step=20.0)
bar.draw(xy=(9.0, 14.0))
bar.draw_legend(
    xy=(15.0, 10.0),
    text_style=Styles.DarkBold.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=4.5,
)

line = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["10p", "25p", "50p", "100p", "200p"],
    width=62.0,
    height=38.0,
    smooth=False,
    show_points=True,
    point_size=0.75,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Incremental Render Latency (ms)",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
line.add_series(
    "Cold",
    [14.0, 22.0, 34.0, 52.0, 72.0],
    style=Styles.Muted6Flat,
    line_width=1.9,
    line_style="dashed",
    point_shape="square",
)
line.add_series(
    "v0.3.10",
    [6.0, 8.0, 11.0, 15.0, 21.0],
    style=Styles.PrimaryFlat,
    line_width=2.4,
    point_shape="circle",
)
line.add_series(
    "SLO (60ms)",
    [60.0, 60.0, 60.0, 60.0, 60.0],
    style=Styles.Danger,
    line_width=1.5,
    line_style="dotted",
    point_shape="none",
)
line.configure_y_axis(min_value=0.0, max_value=80.0, tick_step=20.0, format="{:.0f}", unit="ms")
line.draw(xy=(81.0, 14.0))
line.draw_legend(
    xy=(84.5, 10.0),
    text_style=Styles.DarkBold.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=3.5,
)

save()
```

## 8.1 Why `drawlib.charts` Beats Matplotlib in Technical Documentation

Embedding external Matplotlib scripts into multi-language engineering docs introduces mismatched fonts, brittle `rcParams` boilerplate, and isolated image files that cannot interact with surrounding diagrams. `drawlib.charts` solves all four friction points natively:

- **Identical Cartesian Coordinate System**: Every chart draws directly at `xy=(x0, y0)` on the active Drawlib canvas, making multi-chart dashboards, framing cards, and `KpiCards` headers effortless to align on a single grid.
- **Unified `GoogleStyles` Tokens & CJK Fonts**: Charts inherit `Styles`, `Colors`, and locale-specific fonts (`ja/styles.py`) automatically—eliminating missing glyph boxes (`□□□`) and clashing color palettes.
- **Presence-Based Styling & Collision-Free Legends**: Leaving optional parameters (`grid_style`, `value_text_style`, `background_style`) as `None` cleanly omits visual clutter, while decoupled `chart.draw_legend(xy=...)` and `chart.draw_colorbar(xy=...)` calls let you place legends with zero plot collisions.
- **Layout-Preserving Animation (`show` & `draw_ratio`)**: Mutating `series.show = False` or sweeping `series.draw_ratio` from `0.0` to `1.0` animates bars, curves, wedges, and Gantt tasks while locking the full 100% dataset's axis bounds in place.

## 8.2 Complete Catalog of All 10 Chart Types

All **10 chart classes** across the 9 `drawlib.charts.*` submodules default to **Bottom-Left `(x0, y0)`** (`align="bottom_left"`, with optional `align="center"` and `scale: float = 1.0`):

| # | Chart Class | Submodule | Default `.draw(xy=...)` Anchor | Core Modes & Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **`BarChart`** | `drawlib.charts.bar` | **Bottom-Left** `(x0, y0)` | `"vertical"` / `"horizontal"`, `"group"` / `"stack"`, `bar_r`, value labels, `"log"` scale |
| **2** | **`BoxChart`** | `drawlib.charts.box` | **Bottom-Left** `(x0, y0)` | Raw sample lists or `BoxStats`, `"iqr"` / `"percentile"` whiskers, `show_points` strip jitter |
| **3** | **`LineChart`** | `drawlib.charts.line` | **Bottom-Left** `(x0, y0)` | Multi-series polylines or `smooth=True` splines, vertex markers, `point_shape="none"` thresholds |
| **4** | **`AreaChart`** | `drawlib.charts.area` | **Bottom-Left** `(x0, y0)` | Filled `"overlap"` or cumulative `"stack"` trend curves with configurable `fill_alpha` |
| **5** | **`PieChart`** | `drawlib.charts.pie` | **Bottom-Left** `(x0, y0)` | Solid pie (`hole_ratio=0.0`) & donut (`hole_ratio=0.5..0.7`) with `center_text` KPI badge |
| **6** | **`RadarChart`** | `drawlib.charts.radar` | **Bottom-Left** `(x0, y0)` | Multi-spoke `"polygon"` or `"circle"` spider capability matrices (`levels`, `min_value`..`max_value`) |
| **7** | **`ScatterChart`** | `drawlib.charts.scatter` | **Bottom-Left** `(x0, y0)` | 2D `(x, y)` correlation plots and variable-radius bubble sizing via `Point(x, y, radius=...)` |
| **8** | **`GanttChart`** | `drawlib.charts.gantt` | **Bottom-Left** `(x0, y0)` | Project timelines with `Section`, `Task` progress bars, `Milestone`, `Marker`, and `Dependency` |
| **9** | **`HeatmapChart`** | `drawlib.charts.heatmap` | **Bottom-Left** `(x0, y0)` | 2D intensity matrices (`min_style`..`max_style` or `styles`), `auto_contrast_text`, `draw_colorbar` |
| **10** | **`HeatmapOverlay`** | `drawlib.charts.heatmap` | **Bottom-Left** `(x0, y0)` | Spatial density `Spot` fields (`mode="smooth"` or `"contour"`) layered over maps or floorplans |

### 8.2.1 Categorical, Statistical & Matrix Charts

- **`BarChart` & `BoxChart`**: Share orientation-aware `value_axis` and `category_axis` helpers (`configure_x_axis(...)` / `configure_y_axis(...)`) supporting Nice Numbers linear ticks and base-10 logarithmic (`scale="log"`) axes for wide-dynamic-range benchmarks.
- **`HeatmapChart` & `HeatmapOverlay`**: Map scalar intensities across color stops (`min_style=Styles.White, max_style=Styles.PrimaryFlat` or multi-stop `styles=[...]`). `HeatmapChart` automatically flips cell label contrast (`auto_contrast_text=True`), while `HeatmapOverlay` renders radial `Spot(x, y, value, radius=...)` fields directly over `GeoMap` or architecture canvases.

### 8.2.2 Continuous, Radial & Temporal Charts

- **`LineChart`, `AreaChart` & `ScatterChart`**: Plot continuous trajectories, stacked resource envelopes, and multidimensional `(x, y, radius)` correlations. Setting `point_shape="none"` with `line_style="dotted"` or `"dashdot"` on a `LineChart` series creates clean SLO/SLA reference lines without vertex clutter.
- **`PieChart`, `RadarChart` & `GanttChart`**: Cover part-to-whole ratios (`hole_ratio > 0.0` unlocks donut rings with multiline `center_text` badges and automatic `< 4%` slice label suppression), multi-axis architecture trade-offs (`RadarChart`), and milestone execution schedules (`GanttChart`).

## 8.3 Statistical Storytelling with `BoxChart` & Progressive Animations

Effective quantitative figures follow strict **data storytelling discipline**: never assign five saturated rainbow colors to five competing series. Ground historical baselines, control groups, and secondary tiers in calm neutral tokens (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, or dashed `Styles.Muted`), and reserve `Styles.PrimaryFlat` or `Styles.AccentFlat` exclusively for the target series under evaluation.

While bar charts hide tail spikes behind averages, `BoxChart` exposes medians, interquartile spreads (`Q1`–`Q3`), whiskers, and p99 outliers simultaneously—accepting either raw sample sequences (`list[float]`) or pre-aggregated telemetry (`BoxStats`) with automatic high-contrast median strokes:

```drawlib align=center code=fold file=charts_box_distribution.png caption="Figure 8.2: Tail-Latency Distribution Across Service Tiers Using BoxChart and BoxStats"
from drawlib.canvas import save, setup
from drawlib.charts.box import BoxChart, BoxStats
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=148, height=62)

rectangle(
    (74.0, 31.0),
    width=136.0,
    height=50.0,
    style=Styles.White.patch(shape_r=2.0, shape_line_color=Colors.Gray3),
)

box = BoxChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Edge CDN", "Auth Gateway", "Order Engine", "Vector Search"],
    width=124.0,
    height=38.0,
    box_width_ratio=0.62,
    box_r=0.6,
    show_outliers=True,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Service Tier Response Time Distribution (ms) — Legacy Pool vs. v0.3.10 Async Runtime",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
box.add_series(
    "Legacy Pool (p5–p95 + p99)",
    [
        BoxStats(min=5.0, q1=8.0, median=11.0, q3=15.0, max=24.0, outliers=[34.0]),
        BoxStats(min=12.0, q1=18.0, median=24.0, q3=33.0, max=48.0, outliers=[66.0]),
        BoxStats(min=16.0, q1=24.0, median=32.0, q3=44.0, max=62.0, outliers=[76.0]),
        BoxStats(min=22.0, q1=32.0, median=43.0, q3=56.0, max=70.0, outliers=[78.0]),
    ],
    style=Styles.SecondaryNeutral,
)
box.add_series(
    "v0.3.10 Async Runtime (Target)",
    [
        BoxStats(min=3.0, q1=4.5, median=6.0, q3=8.0, max=12.0, outliers=[16.0]),
        BoxStats(min=6.0, q1=9.0, median=12.0, q3=16.0, max=22.0, outliers=[29.0]),
        BoxStats(min=8.0, q1=12.0, median=15.5, q3=20.0, max=28.0, outliers=[36.0]),
        BoxStats(min=11.0, q1=16.0, median=21.0, q3=27.0, max=38.0, outliers=[46.0]),
    ],
    style=Styles.PrimaryFlat,
)
box.configure_y_axis(
    min_value=0.0,
    max_value=85.0,
    tick_step=20.0,
    format="{:.0f}",
    unit="ms",
)
box.draw(xy=(12.0, 14.0))
box.draw_legend(
    xy=(38.0, 9.8),
    text_style=Styles.DarkBold.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=7.0,
)

save()
```

When working with small benchmark runs (`N = 8..25`), pass raw `list[float]` samples with `show_box=True, show_points=True, jitter=0.42` to overlay deterministic strip points on top of each quartile box—or sweep `draw_ratio` (`0.0` to `1.0`) on `LineChart` / `BarChart` series to render smooth multi-frame `drawlib.anim` builds:

```python
from drawlib.canvas import save, setup
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

setup(width=110, height=56)

trend = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["T1", "T2", "T3", "T4", "T5"],
    width=90.0,
    height=38.0,
    smooth=True,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Progressive Rollout Throughput (60% Keyframe)",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
trend.add_series("Baseline", [40, 42, 41, 43, 42], style=Styles.SecondaryNeutral, line_style="dashed")
# Renders 60% of the curve left-to-right while keeping full T1..T5 axis bounds fixed!
focal = trend.add_series("v0.3.10 Canary", [42, 58, 74, 89, 96], style=Styles.PrimaryFlat, draw_ratio=0.6)

trend.configure_y_axis(min_value=0, max_value=100, tick_step=25, unit="k rps")
trend.draw(xy=(10.0, 10.0))
save()
```

Inspect detailed axis, legend, colorbar, and constructor options for any chart family via `uv run drawlib rules show lib-charts-overview` (or `lib-charts-bar`, `lib-charts-box`, `lib-charts-line`, `lib-charts-pie`, `lib-charts-gantt`, and `lib-charts-heatmap`).
