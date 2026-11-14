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
# Tooling Landscape Comparison
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=comparison_table.svg
from drawlib.canvas import clear, save, setup
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

clear()
setup(width=176, height=82)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=12.6),
    header_cell_style=Styles.DarkFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=13.8),
    border_style=Styles.MutedThin,
    has_header=True,
)

table.set_style_cell_evenodd(
    even_color=Colors.Neutral,
    even_text_style=Styles.Dark.patch(text_size=12.6),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=12.6),
)

table.set_style_cell_rowheader(
    background_color=Colors.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.5),
)

table.set_style_cell(
    background_color=Colors.PrimaryNeutral,
    text_style=Styles.PrimaryBold.patch(text_size=12.8),
    rows=[1, 2, 3, 4, 5, 6],
    columns=[4],
)

table.set_style_cell_header(
    background_color=Colors.Dark,
    text_style=Styles.WhiteBold.patch(text_size=13.8),
)

table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=14.5),
    rows=[0],
    columns=[4],
)

table.set_style_border(
    top=Styles.DarkBold.patch(line_width=1.8),
    top2=Styles.DarkBold.patch(line_width=1.4),
    bottom=Styles.DarkBold.patch(line_width=1.8),
    left2=Styles.Muted.patch(line_width=1.0),
    between_columns=Styles.MutedThin.patch(line_color=Colors.Gray3, line_width=0.7),
    between_rows=Styles.MutedThin.patch(line_color=Colors.Gray3, line_width=0.7),
)

data = [
    ["Capability", "GUI Whiteboards", "Text DSLs", "Plotting Libs", "Drawlib"],
    ["Git Diff & PR Review", "× Binary Blob", "✓ Text Syntax", "✓ Python Code", "✓ Clean Python"],
    ["Spatial Coordinate Control", "✓ Manual Drag", "× Rigid Auto", "△ Axes Only", "✓ Exact + Auto"],
    ["Cloud & UML Diagrams", "✓ Manual Icons", "△ Basic Boxes", "× Unsupported", "✓ 6 Engines + Icons"],
    ["Charts & Infographics", "△ Manual Shapes", "× Very Limited", "✓ Plots Only", "✓ Charts & SmartArts"],
    ["Site / Catalog / Slide / Office", "× Image Export", "× Snippet Only", "× Image Only", "✓ 5 Archetypes"],
    ["AI Visual Self-Healing (-g)", "× GUI Locked", "× Blind Text", "△ Ad-Hoc Scripts", "✓ Built-In -g CLI"],
]

table.draw_flexible(
    xy=(3.0, 77.5),
    column_widths=[46.0, 28.5, 28.5, 28.5, 38.5],
    row_heights=[11.0, 10.4, 10.4, 10.4, 10.4, 10.4, 10.4],
    data=data,
    align="top_left",
)
save()
```
:::

::: note
This comparison matrix summarizes where Drawlib sits across six critical engineering dimensions.
GUI whiteboards excel at freeform dragging, yet fail Git PR review, multi-target document compilation, and AI automation.
Text DSLs like Mermaid pass Git review, but forfeit spatial coordinate control, rich infographics, and full document/slide publishing.
Plotting libraries like Matplotlib give Python control over numeric charts, yet cannot express cloud topologies, UML diagrams, or multi-target documentation sites and slides.
Drawlib combines clean Python Git diffs, exact `(x, y)` coordinates paired with optional graph layout solvers, 6 diagram engines with 34 icon suites, 27 SmartArts and charts, 5 publishing archetypes, and a built-in `-g` visual grid CLI designed from day one for AI self-healing.
:::
