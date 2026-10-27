# Drawlib LayerGraph Guidelines (`lib-graph-layer`)

`LayerGraph` (`from drawlib.graph import LayerGraph`) is a declarative **Sugiyama-style hierarchical DAG coordinate solver** (cycle breaking, longest-path layering, barycenter crossing reduction, and orthogonal/straight port routing). It is ideal for CI/CD pipelines, ETL/data lineage DAGs, workflow stages, and dependency graphs.

```text
   Layer 0             Layer 1 (tier="ci")            Layer 2           Layer 3
 ┌──────────┐        ┌──────────────────────┐       ┌──────────┐      ┌──────────┐
 │          │───────►│  [Lint & Typecheck]  ├──────►│          │      │          │
 │ Git Push │        │                      │       │  Build   ├─────►│  Deploy  │
 │          │───────►│    [Unit Tests]      ├──────►│  Image   │      │   Prod   │
 └──────────┘        └──────────────────────┘       └──────────┘      └──────────┘
```

---

## 1. Imports & Constructor Signature

```python
from drawlib.graph import Cluster, ClusterLayout, Edge, EdgeLayout, GraphLayout, LayerGraph, Node, NodeLayout

g = LayerGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    rank_sep: float | None = None,
    node_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | Flow progression axis (`"LR"` Left-to-Right or `"TB"` Top-to-Bottom). |
| `rank_sep` | `float \| None` | `None` | Fixed distance between successive layers/ranks (auto-scales to canvas if `None`). |
| `node_sep` | `float \| None` | `None` | Fixed minimum distance between parallel nodes in the same layer (auto-scales if `None`). |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Edge path algorithm (`"orthogonal"` Manhattan right-angles or `"straight"` direct ports). |
| `default_node_width` | `float` | `22.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |

---

## 2. Layer Assignment, `.tier()`, & Cluster Boundaries

### 2.1 Automatic Longest-Path Layering vs. Explicit `.tier()` Pinning
- By default, `LayerGraph` assigns each node to a layer index (`0, 1, 2, ...`) based on topological longest-path depth from source nodes (automatically breaking any cycles via DFS).
- **Explicit Layer Pinning (`g.tier()` or `g.node(..., layer=...)`)**:
  ```python
  g.tier(
      name: str,
      nodes: list[str],
      *,
      layer: int | None = None,
  ) -> None
  ```
  Registers all node IDs in `nodes` (if not already present) and pins them to the explicit integer rank `layer` (`0, 1, 2, ...`).
- **Stage Grouping (`g.cluster()`)**:
  Call `g.cluster("ci_stage", ["lint", "unit"], padding=6.0, header_height=3.5)` to compute an enclosing `ClusterLayout` (`layout["ci_stage"]`) around nodes in a pipeline stage.

### 2.2 Computing the Layout (`g.get_layout()`)
```python
layout = g.get_layout(
    *,
    width: float | None = None,
    height: float | None = None,
    margin: float = 10.0,
) -> GraphLayout
```
- When `width`/`height` are omitted, uses active `canvas` dimensions (or fallback `120.0 x 70.0` for `"LR"` / `120.0 x 90.0` for `"TB"`).
- Feed `layout[id].xy` into `FlowDiagram` (`flow.add(Process(...), xy=layout[id].xy)`), `ArchitectureDiagram`, or `shapes.rectangle(layout[id].xy, ...)` + `lines.lines(edge.points, arrow_head="->")`.

---

## 3. Production Examples

### Example 3.1: CI/CD Pipeline DAG (`LayerGraph` + `FlowDiagram` + Stage Cluster)
```drawlib align=center code=fold file=graph_layer_cicd_flow.png caption="Step 1: LayerGraph.get_layout() -> Step 2: FlowDiagram & Stage Boundary Rendering"
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.graph import LayerGraph
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=185, height=90)

# Step 1: Compute layered DAG coordinates with LayerGraph
g = LayerGraph(direction="LR", rank_sep=14.0, default_node_width=26.0, default_node_height=12.0)
g.node("git")
g.node("lint")
g.node("unit")
g.node("build")
g.node("prod")

g.tier("ci", ["lint", "unit"], layer=1)
g.cluster("ci_box", ["lint", "unit"], padding=6.0)

g.edge("git", "lint")
g.edge("git", "unit")
g.edge("lint", "build")
g.edge("unit", "build")
g.edge("build", "prod")

layout = g.get_layout(margin=12.0)

# Step 2: Draw cluster boundary and render workflow with FlowDiagram
ci_box = layout["ci_box"]
rectangle(ci_box.xy, width=ci_box.width, height=ci_box.height, style=Styles.MutedDashed.patch(shape_r=2.0))
text((ci_box.left + 2.0, ci_box.top - 2.5), "CI Checks", style=Styles.DarkBold.patch(halign="left", text_size=10.0))

flow = FlowDiagram(node_style=Styles.Neutral, edge_style=Styles.DarkBold, edge_text_style=Styles.Dark)
git = flow.add(Start("Git Push", width=26, height=12), xy=layout["git"].xy)
lint = flow.add(Process("Lint & Type", width=26, height=12, style=Styles.PrimaryNeutral), xy=layout["lint"].xy)
unit = flow.add(Process("Unit Tests", width=26, height=12, style=Styles.PrimaryNeutral), xy=layout["unit"].xy)
build = flow.add(Process("Build Image", width=26, height=12, style=Styles.SecondaryNeutral), xy=layout["build"].xy)
prod = flow.add(End("Production", width=26, height=12, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=layout["prod"].xy)

flow.connect(git, lint, start_side="right", end_side="left")
flow.connect(git, unit, start_side="right", end_side="left")
flow.connect(lint, build, start_side="right", end_side="left")
flow.connect(unit, build, start_side="right", end_side="left")
flow.connect(build, prod, label="Deploy")

flow.draw()
save()
```
