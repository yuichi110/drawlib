::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Declarative Bar, Line & Area Charts
:::

::: block xy=(80, 140) width=620 height=800
```drawlib file=chart_kpis.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=62, height=80)
utils.draw_kpi_cards(
    [
        ("10", "Built-In Chart Types", "Bar, Box, Line, Area, Pie,\nRadar, Scatter, Gantt, Heatmap"),
        ("100%", "Theme-Synchronized", "Matches Default, Google &\nMonochrome palettes"),
        ("Auto", "Nice-Number Axes", "Clean ticks, legends &\nprogressive draw_ratio"),
    ],
    width=62,
    height=80,
)
save()
```
:::

::: block xy=(740, 140) width=1100 height=800
```drawlib file=bar_line_showcase.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.area import AreaChart
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=110, height=80)

# 1. Top Panel: Grouped BarChart (Throughput across Q1-Q4)
p_top = Panel(
    "BarChart — Quarterly Render Throughput (k/hr)",
    "Grouped Mode",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.8),
    description_style=Styles.Muted.patch(text_size=12.0),
    icon=phosphor.chart_bar,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_top.draw((1.5, 41.5), width=107.0, height=37.0)

bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=100.0,
    height=26.5,
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.68,
    bar_r=0.9,
    axis_text_style=Styles.Dark.patch(text_size=13.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=12.5),
    value_format="{:.0f}k",
)
bar.add_series("v1 Single-Thread", [18.0, 21.0, 24.0, 27.0], style=Styles.SecondaryNeutral)
bar.add_series("v2 Cached Worker", [34.0, 46.0, 61.0, 76.0], style=Styles.PrimaryFlat)
bar.configure_y_axis(min_value=0.0, max_value=100.0, tick_step=25.0, unit="k")
bar.draw(xy=(4.5, 43.2))
bar.draw_legend(
    xy=(54.0, 68.8),
    text_style=Styles.DarkBold.patch(text_size=12.5),
    orientation="horizontal",
    item_gap=4.5,
)

# 2. Bottom Panel: Smooth Multi-Series AreaChart (Latency p50 / p99 Trend)
p_bot = Panel(
    "AreaChart — Build Pipeline Latency (p50 vs p99)",
    "Smooth Spline",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.8),
    description_style=Styles.Muted.patch(text_size=12.0),
    icon=phosphor.chart_line_up,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_bot.draw((1.5, 1.5), width=107.0, height=37.0)

area = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["v1.0", "v1.2", "v1.4", "v1.6", "v2.0"],
    width=100.0,
    height=26.5,
    mode="overlap",
    fill_alpha=0.24,
    smooth=True,
    show_points=True,
    point_shape="circle",
    point_size=0.75,
    axis_text_style=Styles.Dark.patch(text_size=13.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=12.5),
)
area.add_series(
    "p99 Tail Latency",
    [50.0, 42.0, 34.0, 28.0, 23.0],
    style=Styles.PrimaryFlat,
    line_width=2.2,
)
area.add_series(
    "p50 Median",
    [19.0, 15.0, 12.0, 9.0, 6.0],
    style=Styles.SecondaryFlat,
    line_width=2.0,
    line_style="dashed",
    point_shape="square",
)
area.configure_y_axis(min_value=0.0, max_value=60.0, tick_step=20.0, unit="ms")
area.draw(xy=(4.5, 3.2))
area.draw_legend(
    xy=(54.0, 28.8),
    text_style=Styles.DarkBold.patch(text_size=12.5),
    orientation="horizontal",
    item_gap=4.5,
)

save()
```
:::

::: note
Drawlib's `drawlib.charts` package renders statistical plots directly into the vector canvas without external plotting libraries or raster image exports:
- On the left, `KpiCards` summarizes the three core pillars: 10 built-in chart classes, 100% theme synchronization across `Default`, `Google`, and `Monochrome` palettes, and automatic Nice-Number axis scaling (`1, 2, 5 × 10^k`) with `draw_ratio` animation support.
- On the right, a grouped `BarChart` compares quarterly throughput side-by-side with rounded outer tips (`bar_r=0.9`), while a smooth spline `AreaChart` tracks p50 median and p99 tail latency reductions across releases.
:::
