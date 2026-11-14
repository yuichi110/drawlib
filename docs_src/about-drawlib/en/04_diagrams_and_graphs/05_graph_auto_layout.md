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
# Declarative Graph Layout (drawlib.graph)
:::

::: block xy=(80, 145) width=680 height=790
## Hybrid Algorithmic + Manual Control

- **Auto-Solve Topology**: Crossing-free `(x, y)` via `get_layout()`
- **Manual Fine-Tuning**: Nudge nodes with `offset(dx, dy)` anytime
- **No Black-Box Lock-In**: Inspect & freeze code via `print(layout)`

```python
g = LayerGraph(direction="LR")
g.edge("ingest", "validate")
g.edge("validate", "serve")
layout = g.get_layout(margin=8.0)
layout.offset("serve", dy=-4.0)
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=graph_hybrid_workflow.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.graph import LayerGraph
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

panel = Panel(
    "LayerGraph.get_layout() + offset()",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    icon=phosphor.graph,
    icon_style=Styles.PrimaryBold,
    header_height=9.0,
)
panel.draw((2.0, 2.0), width=100.0, height=76.0)

# Step 1: Solve crossing-minimized DAG coordinates via LayerGraph
g = LayerGraph(direction="LR", default_node_width=21.0, default_node_height=12.0)
g.tier("src", ["ingest"], layer=0)
g.tier("etl", ["validate", "enrich"], layer=1)
g.tier("out", ["serve"], layer=2)
g.cluster("stage", ["validate", "enrich"], padding=4.5, header_height=4.5)

g.edge("ingest", "validate")
g.edge("ingest", "enrich")
g.edge("validate", "serve")
g.edge("enrich", "serve")

layout = g.get_layout(width=94.0, height=58.0, margin=5.0).offset("serve", dy=-4.0)
ox, oy = 5.0, 5.0


def pt(xy: tuple[float, float]) -> tuple[float, float]:
    return (xy[0] + ox, xy[1] + oy)


# Step 2: Render stage cluster, FlowDiagram nodes, and offset() callout badge
stg = layout["stage"]
rectangle(pt(stg.xy), width=stg.width, height=stg.height, style=Styles.MutedDashed.patch(shape_r=2.0))
text(
    (stg.left + ox + 2.0, stg.top + oy - 2.6),
    "ETL Stage",
    style=Styles.DarkBold.patch(text_size=13.5, halign="left"),
)

flow = FlowDiagram(
    node_style=Styles.Neutral.patch(text_size=13.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=13.5),
)
n_in = flow.add(
    Start("Ingest", width=21, height=11, style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=14.0)),
    xy=pt(layout["ingest"].xy),
)
n_val = flow.add(
    Process("Validate", width=21, height=12, style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=14.0)),
    xy=pt(layout["validate"].xy),
)
n_enr = flow.add(
    Process("Enrich", width=21, height=12, style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=14.0)),
    xy=pt(layout["enrich"].xy),
)
n_srv = flow.add(
    End("Serve API", width=22, height=12, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=14.0)),
    xy=pt(layout["serve"].xy),
)

flow.connect(n_in, n_val, start_side="right", end_side="left", padding=0.8)
flow.connect(n_in, n_enr, start_side="right", end_side="left", padding=0.8)
flow.connect(n_val, n_srv, start_side="right", end_side="left", padding=0.8)
flow.connect(n_enr, n_srv, start_side="right", end_side="left", padding=0.8)
flow.draw()

srv_xy = pt(layout["serve"].xy)
rectangle(
    (srv_xy[0], srv_xy[1] + 12.5),
    width=23.0,
    height=6.8,
    style=Styles.WarningNeutral.patch(shape_r=1.8),
    text="offset(dy=-4)",
    text_style=Styles.DarkBold.patch(text_size=13.5),
)
save()
```
:::

::: note
**Declarative Coordinate Solving with `drawlib.graph`**:
- Traditional auto-layout tools like Graphviz or Mermaid act as black boxes: if one node lands slightly in the wrong spot, you cannot nudge it by 4 units without rewriting opaque rank hacks. Conversely, calculating every `(x, y)` coordinate manually becomes tedious for large DAGs and trees.
- **`drawlib.graph` gives you the best of both worlds** via a clean 2-step workflow:
  1. **Step 1 (`get_layout()`)**: Declare nodes, edges, and clusters (`LayerGraph`, `ArchitectureGraph`, `TreeGraph`, `RadialGraph`, or `GridGraph`). `get_layout()` computes overlap-free node centers (`layout[id].xy`), cluster bounds (`layout[cid].bottom_left`), and orthogonal edge ports (`edge.points`) with zero rendering side effects.
  2. **Step 2 (`offset()` + Render)**: Optionally nudge any node via `layout.offset("serve", dy=-4.0)` (which automatically updates incident ports) or inspect/copy exact solved coordinates via `print(layout)`, then render using full-power `FlowDiagram`, `ArchitectureDiagram`, or `shapes` primitives.
:::
