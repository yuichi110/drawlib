::: block (80, 50) (1760, 120)
# Landscape Comparison Matrix
How Drawlib bridges the gap between GUI canvases, text DSLs, and low-level plotting libraries.
:::

::: block (80, 180) (1760, 780)
```drawlib file:comparison_table.svg
from drawlib.canvas import clear, save, setup
from drawlib.preset_colors import CssColors
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

clear()
setup(width=176, height=78)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.5),
    header_cell_style=Styles.DarkFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=11.0),
    border_style=Styles.MutedThin,
    has_header=True,
)

table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)

# Highlight Column 0 (Criteria) and Column 4 (Drawlib)
table.set_style_cell_rowheader(
    background_color=CssColors.WhiteSmoke,
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
table.set_style_cell(
    background_color=CssColors.AliceBlue,
    text_style=Styles.PrimaryBold.patch(text_size=10.5),
    rows=[1, 2, 3, 4, 5, 6],
    columns=[4],
)
table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=11.5),
    rows=[0],
    columns=[4],
)

table.set_style_border(
    top=Styles.DarkBold.patch(line_width=1.8),
    top2=Styles.DarkBold.patch(line_width=1.2),
    bottom=Styles.DarkBold.patch(line_width=1.8),
    between_rows=Styles.MutedThin.patch(line_width=0.6),
    between_columns=Styles.MutedThin.patch(line_width=0.6),
)

data = [
    [
        "Evaluation Criteria",
        "GUI Tools\n(Visio / Draw.io / Figma)",
        "Text DSLs\n(Mermaid / PlantUML)",
        "Raw Plotting\n(Matplotlib / Raw SVG)",
        "Drawlib\n(Illustration as Code)",
    ],
    [
        "Git Diffability & PR Review",
        "✗ Opaque XML / Binary",
        "✓ Clean Text Diffs",
        "△ Verbose Code Diffs",
        "✓ Concise Python + Markdown",
    ],
    [
        "Layout Control",
        "✓ Manual Pixel Dragging",
        "✗ Rigid Black-Box Heuristics",
        "△ Manual Math Only",
        "✓ Exact Coords + 5 Solvers",
    ],
    [
        "Reusable Python Logic",
        "✗ None (Copy-Paste)",
        "✗ Static DSL Syntax",
        "✓ Full Python",
        "✓ Functions, Loops & styles.py",
    ],
    [
        "Unified Charts + Diagrams",
        "✗ Diagrams Only",
        "△ Limited / Separate",
        "✗ Plots Only (No VPC/UML)",
        "✓ 7 Diagrams + 7 Charts + 23 Shapes",
    ],
    [
        "Multi-Frame Animation",
        "✗ Static Exports",
        "✗ Static Exports",
        "△ Complex FuncAnimation",
        "✓ Native APNG/WebP & Slide Controls",
    ],
    [
        "AI Agent Self-Healing",
        "✗ Requires GUI Mouse",
        "△ Cannot Fix Wire Crossings",
        "✗ Too Verbose for Context",
        "✓ Rules CLI + Grid (-g) Loop",
    ],
]

table.draw_flexible(
    xy=(4, 73),
    column_widths=[36, 33, 33, 33, 33],
    row_heights=[11, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5],
    data=data,
)
save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- This comparison matrix—rendered live using `drawlib.smartarts.Table`—summarizes how Drawlib compares against GUI tools, text DSLs, and raw plotting libraries across six key engineering criteria.
- Notice the rightmost column: Drawlib is the only solution that combines clean Git diffability, both deterministic coordinate control and automatic layout solvers, full Python programmability, unified architecture diagrams + quantitative charts, native multi-frame animations, and an AI agent self-healing workflow.
:::
