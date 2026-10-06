# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""High-level SmartArts and quantitative Charts showcase on a single canvas."""

from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Colors, Styles

setup(width=120, height=68, dpi=200, color=Colors.Canvas)

# Top section: ChevronProcess Pipeline (bottom-left anchor)
pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.5),
    description_style=Styles.Muted.patch(text_size=7.5),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.append(
    "1. Author",
    description="Python & Markdown",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=7.5),
)
pipeline.append("2. Validate", description="dcli code-check", style=Styles.Neutral)
pipeline.append("3. Render", description="drawlib build", style=Styles.SecondaryNeutral)
pipeline.append("4. Publish", description="HTML / PDF / Slide", style=Styles.SuccessNeutral)
pipeline.draw(xy=(6, 48), width=108, height=15)

# Bottom-Left section: Declarative BarChart (bottom-left anchor)
chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=8.5),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=7.5),
    width=50,
    height=36,
    title="Throughput (req/s)",
    title_style=Styles.DarkBold.patch(text_size=10.5),
)
chart.add_series("v0.3 Engine", [65.0, 92.0, 128.0, 164.0], style=Styles.PrimaryFlat)
chart.add_series("Baseline", [45.0, 52.0, 58.0, 62.0], style=Styles.SecondaryFlat)
chart.configure_y_axis(show_grid=True)
chart.draw(xy=(6.0, 5.0))

# Bottom-Right section: SmartArt Table (top-left anchor)
table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=8.5),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=9.0),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=Colors.White,
    even_text_style=Styles.Dark.patch(text_size=8.5),
    odd_color=Colors.Gray1,
    odd_text_style=Styles.Dark.patch(text_size=8.5),
)
table.draw(
    xy=(62, 41),
    width=52,
    height=34,
    data=[
        ["Module", "Category", "Output"],
        ["drawlib.graph", "Auto-Layout DAG", "PNG / SVG"],
        ["drawlib.diagrams", "Cloud / UML / ER", "PNG / SVG"],
        ["drawlib.smartarts", "Process / Tree", "PNG / SVG"],
        ["drawlib.charts", "Bar / Line / Gantt", "PNG / SVG"],
        ["drawlib.slide", "16:9 Deck Builder", "HTML / PDF"],
    ],
)

save()
