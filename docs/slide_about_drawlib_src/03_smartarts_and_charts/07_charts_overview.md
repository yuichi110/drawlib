::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Quantitative Charts Overview (`drawlib.charts`)
:::

::: block (80, 140) (680, 840) compact
## Why Built-In Vector Charts Beat External Plotting Tools

Traditional workflows force you to plot charts in Matplotlib/Excel, export PNGs, and paste them next to architecture diagrams—resulting in mismatched fonts, blurry raster scaling, and broken visual alignment.

### 4 Pillars of `drawlib.charts`
1. **First-Class Canvas Coexistence**: Charts render directly onto the Drawlib canvas at any `(x, y)` coordinate. You can draw connector arrows directly from an architecture microservice node to a live telemetry `BarChart` or `PieChart`.
2. **Deterministic Bounding Layout**: Explicit `width`, `height`, and `radius` parameters guarantee predictable margins without layout drift.
3. **Nice Numbers & Logarithmic Axes**: `Axis(scale="linear" | "log")` automatically computes human-readable tick steps ($1, 2, 5 \times 10^k$) or base-10 powers ($10^k$) with custom formatters (`format="{:.1f}M"`, `unit="ms"`).
4. **Animation-Ready (`show` & `draw_ratio`)**: Toggle `series.show = False` without rescaling axes, or animate `draw_ratio` (`0.0 -> 1.0`) along `"bottom_to_top"` or `"left_to_right"`.
:::

::: block (800, 140) (1040, 840)
```drawlib file:charts_coexistence.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.bar import BarChart
from drawlib.charts.pie import PieChart
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=84)

# Outer container framing the composite canvas
rectangle((52, 42), width=100, height=80, style=Styles.MutedOutline.patch(shape_r=2.0))
text(
    (6, 78),
    "Single-Canvas Coexistence: Architecture Nodes + Live Telemetry Charts",
    style=Styles.DarkBold.patch(text_size=9.5, halign="left"),
)

# 1. Left Side: Architecture Topology Nodes on the Same Canvas
rectangle((18, 60), width=24, height=11, style=Styles.Neutral.patch(shape_r=1.5), text="Edge Ingress\n(Cloud CDN)")
rectangle(
    (18, 41),
    width=24,
    height=12,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="API Gateway\n(Telemetry Source)",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)
rectangle((18, 21), width=24, height=11, style=Styles.SecondaryNeutral.patch(shape_r=1.5), text="Worker Pool\n(GKE Autoscaler)")

line((18, 54.5), (18, 47.0), arrow_head="->", style=Styles.DarkBold)
line((18, 35.0), (18, 26.5), arrow_head="->", style=Styles.DarkBold)

# Direct connectors from Architecture Node to Charts on the right!
line((30, 44), (40, 56), arrow_head="->", style=Styles.PrimaryBold)
line((30, 38), (40, 24), arrow_head="->", style=Styles.SecondaryBold)

# 2. Top-Right: Live Latency BarChart
bar = BarChart(
    axis_line_style=Styles.Dark,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=56.0,
    height=33.0,
    title="Gateway Throughput (RPS)",
    title_style=Styles.DarkBold.patch(text_size=9.0),
    bar_mode="group",
    bar_width_ratio=0.7,
    bar_r=0.6,
    axis_text_style=Styles.Muted.patch(text_size=7.5),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.DarkBold.patch(text_size=7.0),
    value_format="{:.0f}k",
    background_style=Styles.NeutralFlat,
)
bar.add_series("HTTP/3", [42.0, 58.0, 74.0, 92.0], style=Styles.PrimaryFlat)
bar.add_series("gRPC", [28.0, 39.0, 51.0, 68.0], style=Styles.SecondaryFlat)
bar.configure_y_axis(min_value=0, max_value=100, tick_step=25, unit="k")
bar.draw(xy=(42.0, 41.0))
bar.draw_legend(xy=(50.0, 74.5), text_style=Styles.Dark.patch(text_size=7.5), orientation="horizontal")

# 3. Bottom-Right: Traffic Split Donut PieChart
pie = PieChart(
    radius=12.5,
    hole_ratio=0.58,
    center_text="99.98%\nSuccess",
    center_text_style=Styles.DarkBold.patch(text_size=7.2),
    title="Response Status Distribution",
    title_style=Styles.DarkBold.patch(text_size=9.0),
    value_text_style=Styles.WhiteBold.patch(text_size=7.0),
    background_style=Styles.NeutralFlat,
)
pie.add_slice("200 OK (Cached)", 64.0, style=Styles.PrimaryFlat)
pie.add_slice("200 OK (Origin)", 28.0, style=Styles.SecondaryFlat)
pie.add_slice("304 Not Modified", 8.0, style=Styles.AccentFlat)
pie.draw(xy=(42.0, 5.5), width=56.0, height=32.0)
pie.draw_legend(xy=(74.0, 24.0), text_style=Styles.Dark.patch(text_size=7.2), orientation="vertical")

save()
```
:::

::: note
- Why did we build a dedicated charting engine (`drawlib.charts`) when libraries like Matplotlib and Seaborn already exist?
- Look at the right-hand canvas: we have an architecture topology on the left (`Edge Ingress -> API Gateway -> Worker Pool`) and **live vector `BarChart` and `PieChart` instances drawn on the exact same coordinate plane**, connected by arrows directly from the `API Gateway` node!
- Every chart uses the exact same `Styles`, `Colors`, and bundled `Font` tokens as the surrounding diagram, eliminating font mismatches and raster pixelation.
- Furthermore, all 7 chart classes support `series.show = False` (which hides a series while locking the 100% axis scale so axes never jump during slide transitions) and `draw_ratio` (`0.0 -> 1.0`) for smooth bar/line/wedge growth animations.
:::
