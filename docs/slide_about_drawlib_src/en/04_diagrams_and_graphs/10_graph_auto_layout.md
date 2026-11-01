::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
import utils

utils.draw_page_number()
```
:::

::: block xy=(80, 40) width=1760 height=60
# 2-Step Auto-Layout Engine (`drawlib.graph` -> `get_layout()`)
:::

::: block xy=(80, 140) width=660 height=840 compact=true
## Pure Coordinate Solver + Rich Rendering

Manual `(x, y)` coordinates give total precision, while black-box tools like Graphviz lock you out of custom icons and styles. `drawlib.graph` bridges both worlds as a **pure coordinate calculator (`get_layout()` only)**:

### The 2-Step Workflow of `drawlib.graph`
1. **Step 1 — Solve & Inspect (`layout = g.get_layout()`)**:
   - Declare topology via `.node(id, width=..., height=...)`, `.edge(src, dst)`, and `.cluster(id, nodes=[...])`.
   - Call `layout = g.get_layout(width=..., height=..., margin=...)` to compute a `GraphLayout`.
   - Inspect all solved coordinates via `print(layout)` or fine-tune positions with `layout.offset("canary", dy=-2.5)`.
2. **Step 2 — Render with `diagrams` or `shapes`**:
   - Pass `layout["id"].xy`, `.local_xy`, `.bottom_left`, `.local_bottom_left`, or `edge.points` directly into `ArchitectureDiagram`, `FlowDiagram`, or `drawlib.shapes` / `drawlib.lines`.
   - Attach custom callouts (`bubblespeech`) or charts to exact solved coordinates!
:::

::: block xy=(780, 140) width=1060 height=840
```drawlib file=graph_workflow.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.graph import LayerGraph
from drawlib.shapes import bubblespeech, rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=106, height=84)

# Top Panel: Live LayerGraph solved in Step 1 and rendered with FlowDiagram in Step 2
rectangle((53, 61), width=102, height=42, style=Styles.MutedOutline.patch(shape_r=2.0))
text(
    (5, 78.5),
    "2-Step Live Output: Step 1 g.get_layout().offset() -> Step 2 FlowDiagram + Callout",
    style=Styles.DarkBold.patch(text_size=8.6, halign="left"),
)

# Step 1: Solve layered DAG coordinates and nudge 'canary'
g = LayerGraph(direction="LR", rank_sep=8.5, default_node_width=16.5, default_node_height=8.5)
g.node("git")
g.node("lint")
g.node("test")
g.node("canary")
g.node("prod")

g.tier("ci", ["lint", "test"], layer=1)
g.cluster("ci_cluster", ["lint", "test"], padding=3.5)

g.edge("git", "lint")
g.edge("git", "test")
g.edge("lint", "canary")
g.edge("test", "canary")
g.edge("canary", "prod")

layout = g.get_layout(width=100, height=35, margin=6.0).offset("canary", dy=-2.5)

# Step 2: Render cluster box, FlowDiagram nodes/edges, and bubblespeech callout
ox, oy = 3.0, 40.0
ci_box = layout["ci_cluster"]
rectangle(
    (ox + ci_box.cx, oy + ci_box.cy),
    width=ci_box.width,
    height=ci_box.height,
    style=Styles.MutedDashed.patch(shape_r=1.5),
)
text(
    (ox + ci_box.left + 1.5, oy + ci_box.top - 2.0),
    "CI Stage",
    style=Styles.DarkBold.patch(text_size=7.0, halign="left"),
)

ts_body = Styles.DarkBold.patch(text_size=7.2)
ts_hero = Styles.WhiteBold.patch(text_size=7.2)
flow = FlowDiagram(node_style=Styles.Neutral, edge_style=Styles.DarkBold, edge_text_style=Styles.Dark.patch(text_size=6.8))
git = flow.add(Start("Git Push", width=16.5, height=8.5, text_style=ts_body), xy=layout["git"].xy)
lint = flow.add(Process("Lint & Type", width=16.5, height=8.5, style=Styles.PrimaryNeutral, text_style=ts_body), xy=layout["lint"].xy)
test = flow.add(Process("Unit Tests", width=16.5, height=8.5, style=Styles.PrimaryNeutral, text_style=ts_body), xy=layout["test"].xy)
canary = flow.add(Process("Canary Gate", width=16.5, height=8.5, style=Styles.PrimaryFlat, text_style=ts_hero), xy=layout["canary"].xy)
prod = flow.add(End("Prod Fleet", width=16.5, height=8.5, style=Styles.SecondaryNeutral, text_style=ts_body), xy=layout["prod"].xy)

flow.connect(git, lint, start_side="right", end_side="left")
flow.connect(git, test, start_side="right", end_side="left")
flow.connect(lint, canary, start_side="right", end_side="left")
flow.connect(test, canary, start_side="right", end_side="left")
flow.connect(canary, prod, label="Promote")
flow.draw(xy=(ox, oy))

# Attach a custom primitive callout to the exact computed node coordinate!
canary_node = layout["canary"]
cx = ox + canary_node.x
cy = oy + canary_node.y
bubblespeech(
    (cx, cy + 10.5),
    width=29.0,
    height=7.2,
    tail_edge="bottom",
    tail_start_ratio=0.42,
    tail_end_ratio=0.58,
    tail_vertex_xy=(cx, cy + canary_node.height / 2.0 + 0.5),
    style=Styles.WarningNeutral,
    text="Tweaked dy=-2.5 + Callout!",
    text_style=Styles.DarkBold.patch(text_size=6.8),
)

# Bottom Panel: The 2-Step Workflow Side-by-Side
text(
    (5, 35.5),
    "The 2-Step Workflow — Pure Layout Calculation (Step 1) + Rich Diagram Rendering (Step 2)",
    style=Styles.DarkBold.patch(text_size=8.6, halign="left"),
)

code_step1 = """# Step 1: Solve & Inspect Topology
g = LayerGraph(direction="LR", default_node_width=19)
g.tier("ci", ["lint", "test"], layer=1)
g.cluster("ci_cluster", ["lint", "test"])
g.edge("git", "lint"); g.edge("lint", "canary")
layout = g.get_layout(width=100, height=35)
layout.offset("canary", dy=-2.5)
print(layout)  # Inspect xy, local_xy, bottom_left"""

code_step2 = """# Step 2: Render with Diagrams or Shapes
flow = FlowDiagram(node_style=Styles.Neutral, ...)
git = flow.add(Start("Git Push"), xy=layout["git"].xy)
can = flow.add(Process("Canary"), xy=layout["canary"].xy)
flow.connect(git, can); flow.draw()
# Or attach callouts to layout["canary"]:
c = layout["canary"]
bubblespeech((c.x, c.y + 10.5), ...)"""

cs = SourceCodeStyles.get("dark", font_lang="en", text_size=6.8)
SourceCode.draw(xy=(4, 32.5), width=47, code=code_step1, styles=cs, code_lang="python")
SourceCode.draw(xy=(55, 32.5), width=47, code=code_step2, styles=cs, code_lang="python")

save()
```
:::

::: note
- What if you want automatic graph layout without giving up `ArchitectureDiagram` icons, `FlowDiagram` shapes, or pixel-level adjustments?
- `drawlib.graph` achieves this by acting strictly as a **pure coordinate calculator (`get_layout()` only)** in a **2-Step Workflow**:
  1. **Step 1 — Solve & Inspect (`layout = g.get_layout()`)**: Declare nodes, clusters, and edges and compute a `GraphLayout`. You can run `print(layout)` to inspect the coordinate table or call `layout.offset("canary", dy=-2.5)` to nudge a node or cluster.
  2. **Step 2 — Render with `drawlib.diagrams` or `drawlib.shapes`**: As shown in the top panel, we pass `layout[id].xy` directly into `FlowDiagram` (`Start`, `Process`, `End`) and use `layout["canary"].x, .y` to attach a `bubblespeech` callout right above the computed node!
:::
