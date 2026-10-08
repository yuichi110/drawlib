::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Radial & Relational Charts (`PieChart`, `RadarChart`, `ScatterChart`)
:::

::: block (80, 140) (660, 840) compact
## Proportions, Trade-Offs & Correlations

### 1. `PieChart` — Solid Pies & KPI Donuts
- Set `hole_ratio=0.5` (up to `0.9`) with `center_text` to render executive KPI donut rings.
- Supports per-slice outward emphasis (`explode=2.5`) and automatic label suppression on tiny wedges ($<4\%$).

### 2. `RadarChart` — Multi-Axis Trade-Off Polygons
- Evaluates 3+ symmetric dimensions radiating from a central origin (`grid_shape="polygon" | "circle"`).
- Ideal for comparing architectural trade-offs (e.g., Microservices vs. Monolith across Scalability, Latency, Reliability, Operability, and Velocity).

### 3. `ScatterChart` — XY Plots & 3D Bubbles
- Plots continuous `(x, y)` coordinates or 3-tuple `(x, y, radius)` bubbles across dual independent `linear` or `log` axes.
- Combine named `add_series(...)` clusters with individually labeled benchmark points via `chart.add(xy, label=...)`.
:::

::: block (780, 140) (1060, 840)
```drawlib file:pie_radar_scatter.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.pie import PieChart
from drawlib.charts.radar import RadarChart
from drawlib.charts.scatter import ScatterChart
from drawlib.styles import Styles

clear()
setup(width=106, height=84)

# 1. Top-Left: Donut PieChart with hole_ratio=0.5
pie = PieChart(
    radius=12.5,
    hole_ratio=0.5,
    center_text="$4.8M\nCloud",
    center_text_style=Styles.DarkBold.patch(text_size=7.2),
    title="1. PieChart (hole_ratio=0.5)",
    title_style=Styles.DarkBold.patch(text_size=8.5),
    value_text_style=Styles.WhiteBold.patch(text_size=6.8),
    background_style=Styles.NeutralFlat,
)
pie.add_slice("Compute (GKE)", 48.0, style=Styles.PrimaryFlat, explode=1.2)
pie.add_slice("Storage & DB", 27.0, style=Styles.SecondaryFlat)
pie.add_slice("Network Egress", 15.0, style=Styles.AccentFlat)
pie.add_slice("Observability", 10.0, style=Styles.MutedFlat)
pie.draw(xy=(3.0, 45.0), width=48.0, height=36.0)
pie.draw_legend(xy=(33.5, 68.0), text_style=Styles.Dark.patch(text_size=6.5), orientation="vertical")

# 2. Top-Right: 5-Axis Polygon RadarChart
radar = RadarChart(
    axis_line_style=Styles.Dark,
    categories=["Scale", "Reliability", "Security", "Velocity", "Low Latency"],
    radius=11.5,
    min_value=0.0,
    max_value=100.0,
    levels=4,
    grid_shape="polygon",
    title="2. RadarChart (5-Axis Polygon)",
    title_style=Styles.DarkBold.patch(text_size=8.5),
    axis_text_style=Styles.Dark.patch(text_size=6.8),
    grid_style=Styles.MutedDashed,
    background_style=Styles.NeutralFlat,
)
radar.add_series("Microservices", [95, 88, 82, 90, 62], style=Styles.PrimaryFlat, fill_alpha=0.28)
radar.add_series(
    "Monolith",
    [55, 75, 85, 65, 94],
    style=Styles.SecondaryFlat,
    fill_alpha=0.25,
    line_style="dashed",
)
radar.draw(xy=(55.0, 45.0), width=48.0, height=36.0)
radar.draw_legend(xy=(60.0, 47.0), text_style=Styles.Dark.patch(text_size=6.8), orientation="horizontal")

# 3. Bottom Full-Width: ScatterChart (Throughput vs p99 Latency Benchmark)
scatter = ScatterChart(
    axis_line_style=Styles.Dark,
    width=100.0,
    height=35.0,
    title="3. ScatterChart — Throughput (req/s) vs. p99 Latency (ms) Benchmark",
    title_style=Styles.DarkBold.patch(text_size=8.8),
    axis_text_style=Styles.Muted.patch(text_size=7.2),
    value_text_style=Styles.DarkBold.patch(text_size=7.0),
    grid_style=Styles.MutedDashed,
    background_style=Styles.NeutralFlat,
)
scatter.configure_x_axis(label="Throughput (req/sec)", unit=" rps", min_value=0, max_value=1000, tick_step=200)
scatter.configure_y_axis(label="p99 Latency (ms)", unit=" ms", min_value=0, max_value=160, tick_step=40)

scatter.add_series(
    name="Async Rust Runtime",
    data=[(200, 14.0), (400, 16.0), (600, 19.0), (800, 23.0), (950, 28.0)],
    style=Styles.PrimaryFlat,
    radius=1.1,
    shape="circle",
)
scatter.add_series(
    name="Thread-Pool Worker",
    data=[(150, 32.0), (300, 54.0), (450, 88.0), (600, 132.0)],
    style=Styles.SecondaryFlat,
    radius=1.1,
    shape="square",
)
scatter.add(xy=(880.0, 42.0), style=Styles.AccentFlat, radius=1.6, shape="rhombus", label="SLO Target Ceiling")

scatter.draw(xy=(3.0, 3.0))
scatter.draw_legend(xy=(28.0, 39.0), text_style=Styles.Dark.patch(text_size=7.2), orientation="horizontal")

save()
```
:::

::: note
- This slide highlights three specialized chart types for proportional, multi-dimensional, and relational analysis:
  1. **`PieChart` (Top-Left)**: Configured as a Donut chart (`hole_ratio=0.5`) with a `$4.8M Cloud` center summary badge and an exploded primary slice (`explode=1.2`).
  2. **`RadarChart` (Top-Right)**: Compares **Microservices** vs. **Monolith** architectures across 5 non-functional dimensions (`Scale`, `Reliability`, `Security`, `Velocity`, `Low Latency`). Microservices excel at horizontal scale and team velocity, whereas the Monolith achieves lower in-process call latency.
  3. **`ScatterChart` (Bottom)**: Plots continuous X-Y benchmark measurements comparing an **Async Rust Runtime** (`circle` markers) against a **Thread-Pool Worker** (`square` markers), plus a standalone labeled SLO ceiling marker (`chart.add(...)`).
:::
