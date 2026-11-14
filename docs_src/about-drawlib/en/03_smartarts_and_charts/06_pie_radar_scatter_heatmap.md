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
# Pie, Radar, Scatter & Heatmap Charts
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=pie_radar_scatter_heatmap.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.heatmap import HeatmapChart
from drawlib.charts.pie import PieChart
from drawlib.charts.radar import RadarChart
from drawlib.charts.scatter import ScatterChart
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=176, height=81)

# 1. Top-Left Panel: Donut PieChart (hole_ratio=0.55 + External Legend)
p_tl = Panel(
    "PieChart — Donut Share",
    "hole_ratio=0.55",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.chart_pie_slice,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tl.draw((1.5, 42.2), width=84.5, height=37.5)

pie = PieChart(
    radius=12.0,
    hole_ratio=0.55,
    center_text="100%\nVector",
    center_text_style=Styles.DarkBold.patch(text_size=11.5),
)
pie.add_slice("Slide Decks (42%)", 42.0, style=Styles.PrimaryFlat)
pie.add_slice("Tech Sites (28%)", 28.0, style=Styles.PrimaryNeutral)
pie.add_slice("Whitepapers (18%)", 18.0, style=Styles.SecondaryFlat)
pie.add_slice("CLI Previews (12%)", 12.0, style=Styles.AccentFlat)
pie.draw(xy=(24.0, 57.8), align="center")
pie.draw_legend(
    xy=(44.5, 66.2),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    orientation="vertical",
    item_gap=4.2,
)

# 2. Top-Right Panel: RadarChart (5-Axis Engineering Capability Profile)
p_tr = Panel(
    "RadarChart — 5-Axis Profile",
    "Polygon Web",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.gauge,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tr.draw((90.0, 42.2), width=84.5, height=37.5)

radar = RadarChart(
    categories=["Speed", "Themes", "Git Diff", "Vector", "AI CLI"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.DarkBold.patch(text_size=11.2),
    grid_style=Styles.MutedThin,
    radius=9.8,
    min_value=0.0,
    max_value=100.0,
    levels=4,
    grid_shape="polygon",
)
radar.add_series("Drawlib", [94, 92, 98, 96, 95], style=Styles.PrimaryFlat, fill_alpha=0.28)
radar.add_series(
    "Manual GUI",
    [52, 64, 22, 78, 28],
    style=Styles.SecondaryFlat,
    fill_alpha=0.20,
    line_style="dashed",
    point_shape="square",
)
radar.draw(xy=(121.0, 57.2), align="center")
radar.draw_legend(
    xy=(147.0, 62.2),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    orientation="vertical",
    item_gap=4.5,
)

# 3. Bottom-Left Panel: ScatterChart (2 Bubble/Point Series with Legend)
p_bl = Panel(
    "ScatterChart — Build Scaling",
    "Bubble Series",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.sparkle,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_bl.draw((1.5, 1.5), width=84.5, height=37.5)

scatter = ScatterChart(
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Dark.patch(text_size=11.2),
    grid_style=Styles.MutedThin,
    width=78.0,
    height=25.5,
)
scatter.configure_x_axis(min_value=0.0, max_value=100.0, tick_step=25.0, unit=" figs")
scatter.configure_y_axis(min_value=0.0, max_value=4.0, tick_step=1.0, unit="s")
scatter.add_series(
    "Incremental Cache",
    [(15, 0.2, 0.9), (35, 0.3, 1.2), (60, 0.4, 1.5), (90, 0.5, 1.8)],
    style=Styles.PrimaryFlat,
    shape="circle",
)
scatter.add_series(
    "Cold Full Build",
    [(15, 0.7, 0.9), (35, 1.4, 1.2), (60, 2.3, 1.5), (90, 3.4, 1.8)],
    style=Styles.SecondaryFlat,
    shape="rhombus",
)
scatter.draw(xy=(4.5, 3.0))
scatter.draw_legend(
    xy=(15.5, 29.8),
    text_style=Styles.DarkBold.patch(text_size=11.2),
    orientation="horizontal",
    item_gap=4.5,
)

# 4. Bottom-Right Panel: HeatmapChart (2D Latency/Load Matrix)
p_br = Panel(
    "HeatmapChart — Latency",
    "Auto-Contrast",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.database,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_br.draw((90.0, 1.5), width=84.5, height=37.5)

hm = HeatmapChart(
    styles=[Styles.White, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat],
    x_categories=["00:00", "06:00", "12:00", "18:00", "22:00"],
    axis_line_style=Styles.MutedThin,
    axis_text_style=Styles.DarkBold.patch(text_size=11.0),
    value_text_style=Styles.DarkBold.patch(text_size=11.2),
    width=78.0,
    height=26.5,
    cell_gap=0.7,
    cell_r=0.5,
    auto_contrast_text=True,
    value_format="{:.0f}ms",
)
hm.add_row("US-West", [14, 18, 42, 35, 19])
hm.add_row("EU-West", [16, 29, 54, 38, 21])
hm.add_row("Tokyo", [22, 46, 68, 49, 25])
hm.add_row("Singapore", [18, 34, 51, 41, 22])
hm.draw(xy=(93.0, 3.2))

save()
```
:::

::: note
Beyond Cartesian bars and lines, Drawlib provides proportional, radial, relational, and 2D matrix visualizations:
- **`PieChart`** supports donut rings (`hole_ratio=0.55`) with center KPI callouts, automatic `< 4%` slice label suppression, and external legends so labels never collide.
- **`RadarChart`** compares multi-axis engineering profiles across polygonal or circular concentric webs.
- **`ScatterChart`** plots `(x, y)` points or 3-variable `(x, y, radius)` bubbles across linear or logarithmic axes.
- **`HeatmapChart`** interpolates multi-stop `Style` palettes across 2D categorical grids with automatic dark/light text contrast (`auto_contrast_text=True`).
:::
