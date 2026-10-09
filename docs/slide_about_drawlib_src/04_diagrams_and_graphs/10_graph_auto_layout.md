::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Declarative Auto-Layout + Fine-Tuning (`drawlib.graph`)
:::

::: block (80, 140) (660, 840) compact
## Bridging Auto-Layout and Manual Control

Manual `(x, y)` coordinates give total precision, but when a graph topology changes frequently, you want automatic layout—**without getting trapped in a rigid black box like Graphviz**.

### The 3 Progressive Workflows of `drawlib.graph`
1. **Workflow 1 — Direct Declarative (`g.draw()`)**:
   - Declare `.node()`, `.edge()`, and `.cluster()`, then call `g.draw()` to compute coordinates and render in one step.
2. **Workflow 2 — Calculate, Tweak & Overlay (`g.calc()`)**:
   - Call `layout = g.calc()` to obtain a mutable `GraphLayout` (`layout.nodes`, `layout.edges`, `layout.clusters`).
   - Nudge specific nodes or clusters with `layout.offset("db", dy=-5.0)`.
   - Read exact computed coordinates (`layout.nodes["api"].x`) to attach custom `bubblespeech` callouts or charts!
3. **Workflow 3 — Export Standalone Code (`g.export_code()`)**:
   - Generates clean, self-contained `drawlib.shapes` + `drawlib.lines` Python code with all computed coordinates baked in.
:::

::: block (780, 140) (1060, 840)
```drawlib file:graph_workflow.svg
from drawlib.canvas import clear, save, setup
from drawlib.graph import LayerGraph
from drawlib.shapes import bubblespeech, rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=106, height=84)

# Top Panel: Live LayerGraph rendered via Workflow 2 (calc -> offset -> draw + overlay)
rectangle((53, 61), width=102, height=42, style=Styles.MutedOutline.patch(shape_r=2.0))
text(
    (5, 78.5),
    "Workflow 2 Live Output: layout = g.calc() -> layout.offset() -> layout.draw()",
    style=Styles.DarkBold.patch(text_size=8.8, halign="left"),
)

g = LayerGraph(direction="LR", rank_sep=11.0, default_node_width=20.0, default_node_height=9.5)
g.node("git", "Git Push", style=Styles.Neutral)
g.node("lint", "Lint & Type", style=Styles.PrimaryNeutral)
g.node("test", "Unit Tests", style=Styles.PrimaryNeutral)
g.node("canary", "Canary Gate", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("prod", "Prod Fleet", style=Styles.SecondaryNeutral)

g.tier("ci", ["lint", "test"], layer=1)
g.cluster("ci_cluster", ["lint", "test"], label="CI Stage", padding=4.0)

g.edge("git", "lint")
g.edge("git", "test")
g.edge("lint", "canary")
g.edge("test", "canary")
g.edge("canary", "prod", "Promote")

# Compute layout inside top panel, nudge 'canary', and render at xy=(3, 40)
layout = g.calc(width=100, height=35, margin=6.0)
layout.offset("canary", dy=-2.5)
layout.draw(xy=(3.0, 40.0))

# Attach a custom primitive callout to the exact computed node coordinate!
canary_node = layout.nodes["canary"]
cx = 3.0 + canary_node.x
cy = 40.0 + canary_node.y
bubblespeech(
    (cx - 14.0, cy + 8.5),
    width=28.0,
    height=7.5,
    tail_edge="bottom",
    tail_start_ratio=0.42,
    tail_end_ratio=0.58,
    tail_vertex_xy=(cx, cy + canary_node.height / 2.0 + 0.5),
    style=Styles.WarningNeutral,
    text=" Tweaked dy=-2.5 + Callout!",
    text_style=Styles.DarkBold.patch(text_size=6.8),
)

# Bottom Panel: The 3 Progressive Code Workflows Side-by-Side
text(
    (5, 35.5),
    "3 Progressive Workflows — From 1-Line Auto-Layout to Exported Primitives",
    style=Styles.DarkBold.patch(text_size=8.8, halign="left"),
)

code_w12 = """# 1. Direct Auto-Layout:
g.draw(margin=10)

# 2. Calc, Tweak & Overlay:
layout = g.calc(margin=10)
layout.offset("canary", dy=-2.5)
layout.draw()
c = layout.nodes["canary"]
bubblespeech((c.x - 14, c.y + 8), ...)"""

code_w3 = """# 3. Export Editable Primitive Code:
print(g.export_code(width=160, height=90))
# Outputs standalone Python script:
# setup(width=160, height=90)
# rectangle((24.0, 45.0), width=20.0,
#           height=9.5, text="Git Push")
# line((34.0, 45.0), (58.0, 62.0), ...)"""

cs = SourceCodeStyles.get("dark", font_lang="en", text_size=6.8)
SourceCode.draw(xy=(4, 32.5), width=47, code=code_w12, styles=cs, code_lang="python")
SourceCode.draw(xy=(55, 32.5), width=47, code=code_w3, styles=cs, code_lang="python")

save()
```
:::

::: note
- What if you want automatic graph layout without giving up pixel-level adjustments or custom Drawlib overlays?
- `drawlib.graph` solves this with **three progressive workflows**:
  1. **Direct rendering (`g.draw()`)**: Declare nodes, clusters, and edges and render immediately.
  2. **Calculate, Tweak & Overlay (`layout = g.calc()`)**: As shown in the top panel, we run the Sugiyama `LayerGraph` solver, call `layout.offset("canary", dy=-2.5)` to nudge a specific node, call `layout.draw()`, and then inspect `layout.nodes["canary"].x, .y` to attach a `bubblespeech` callout right above the computed node!
  3. **Export standalone code (`g.export_code()`)**: Ejects the solved graph into a pure `drawlib.shapes` + `drawlib.lines` Python script with rounded numeric coordinates when you want 100% manual ownership.
:::
