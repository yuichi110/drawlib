::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Quantitative Chart Growth (`.draw_ratio` & `.draw_direction`)
:::

::: block (80, 140) (740, 840) font:20px
## Spatial Interpolation with Locked Axes

All 7 chart types in `drawlib.charts` return mutable `Series`, `Slice`, or `Task` objects supporting **`.draw_ratio`** (`0.0` → `1.0`) and **`.draw_direction`**.

```python
bar_s = bar_chart.add_series(
    "Throughput", [42, 68, 95, 128],
    style=Styles.PrimaryFlat,
    draw_direction="bottom_to_top",
)
line_s = line_chart.add_series(
    "P99 Latency", [38, 29, 19, 12],
    style=Styles.AccentFlat,
    draw_direction="left_to_right",
)

for ratio in [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]:
    bar_s.draw_ratio = ratio
    line_s.draw_ratio = ratio
    with anim.frame(duration=2.0 if ratio == 1.0 else 0.12):
        bar_chart.draw(xy=(8, 44))
        line_chart.draw(xy=(8, 6))
```

### Dual Direction Modes across Chart Families
- **`"bottom_to_top"`**: Bars grow vertically from baseline; `RadarChart` polygons expand radially outward; `PieChart` wedges grow from inner hole to outer radius.
- **`"left_to_right"`**: `LineChart` & `AreaChart` sweep continuously along arc length; `GanttChart` tasks extend across timeline; `PieChart` sweeps angularly.
:::

::: block (860, 140) (980, 840)
```drawlib file:chart_growth_anim.png anim:auto
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.charts.bar import BarChart
from drawlib.charts.line import LineChart
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)
anim = Animation(fps=8.0, loop=0)

quarters = ["Q1 '25", "Q2 '25", "Q3 '25", "Q4 '25", "Q1 '26"]

# Top Chart: BarChart (bottom_to_top vertical growth)
bar_chart = BarChart(
    axis_line_style=Styles.Dark,
    categories=quarters,
    width=82.0,
    height=32.0,
    title="API Gateway Throughput (k RPS) — draw_direction='bottom_to_top'",
    title_style=Styles.DarkBold.patch(text_size=9.5),
    bar_r=0.8,
    bar_width_ratio=0.62,
    axis_text_style=Styles.Muted.patch(text_size=8.0),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.PrimaryBold.patch(text_size=8.0),
    value_format="{:.0f}k",
)
bar_chart.configure_y_axis(min_value=0, max_value=150, tick_step=50)
s_bar = bar_chart.add_series(
    "Throughput",
    [45.0, 68.0, 92.0, 118.0, 142.0],
    style=Styles.PrimaryFlat,
    draw_direction="bottom_to_top",
)

# Bottom Chart: LineChart (left_to_right arc sweep)
line_chart = LineChart(
    axis_line_style=Styles.Dark,
    categories=quarters,
    width=82.0,
    height=32.0,
    title="P99 Tail Latency (ms) — draw_direction='left_to_right'",
    title_style=Styles.DarkBold.patch(text_size=9.5),
    smooth=True,
    show_points=True,
    point_size=0.9,
    axis_text_style=Styles.Muted.patch(text_size=8.0),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.DarkBold.patch(text_size=8.0),
)
line_chart.configure_y_axis(min_value=0, max_value=60, tick_step=20, unit="ms")
s_line = line_chart.add_series(
    "P99 Latency",
    [52.0, 41.0, 29.0, 18.0, 11.0],
    style=Styles.AccentFlat,
    line_width=2.5,
    draw_direction="left_to_right",
)

ratios = [0.15, 0.28, 0.42, 0.56, 0.70, 0.84, 0.94, 1.0]
for idx, r in enumerate(ratios):
    is_last = idx == len(ratios) - 1
    s_bar.draw_ratio = r
    s_line.draw_ratio = r
    with anim.frame(duration=2.2 if is_last else 0.13):
        rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
        rectangle(
            (84, 76),
            width=18,
            height=4.5,
            style=Styles.PrimaryNeutral.patch(shape_r=1.0),
            text=f"ratio = {r:.2f}",
            text_style=Styles.PrimaryBold.patch(text_size=8.0),
        )
        bar_chart.draw(xy=(8.0, 44.0))
        line_chart.draw(xy=(8.0, 6.0))

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 5: Multi-Frame Animations — Quantitative Chart Growth (.draw_ratio)*
:::

::: note
- Notice how both the `BarChart` (`0` to `150k`) and `LineChart` (`0` to `60ms`) keep their Y-axis ticks, gridlines, and category labels completely stationary while `.draw_ratio` interpolates from `0.15` to `1.00`.
- `BarChart` grows upward (`bottom_to_top`), while `LineChart` sweeps smoothly from left to right (`left_to_right`), revealing vertex markers and value labels as the curve reaches each category.
:::
