# Graph Engine Overview (`drawlib.graph`)

`drawlib.graph` provides a declarative **auto-layout graph engine** powered by five specialized layout solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`).

Instead of manually computing `(x, y)` coordinates for every vertex and container when drafting a complex topology, you declare **structural relationships**—nodes, edges, and clusters—and let Drawlib's pure-Python layout algorithms calculate clean coordinates, container bounding boxes, and orthogonal or radial edge routes automatically.

```drawlib show-code 720px center file:graph_overview_workflow.png caption:"Declarative Cloud Architecture Layout Computed Automatically by ArchitectureGraph"
from drawlib.canvas import save, setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=185, height=110)

g = ArchitectureGraph(direction="LR", default_node_width=26.0)

# External client zone pinned to the left
g.cluster("clients", ["client"], label="External", pos="left", padding=5.0)
g.node("client", "Client App", style=Styles.Neutral)

# Cloud VPC container with nested Compute and Data tiers in the center
g.group("vpc", "Production VPC", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], label="Compute Tier", parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db", "cache"], label="Data Tier", parent="vpc", order=2, padding=5.0)

# 50%+ Neutral baseline with a single PrimaryFlat focal node
g.node("api", "API Gateway", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("worker", "Worker", style=Styles.PrimaryNeutral)
g.node("db", "Primary DB", style=Styles.SecondaryNeutral)
g.node("cache", "Redis Cache", style=Styles.SecondaryNeutral)

# Observability cluster pinned to the bottom
g.cluster("obs", ["metrics"], label="Observability", pos="bottom", padding=5.0)
g.node("metrics", "Prometheus", style=Styles.Neutral)

g.edge("client", "api", "HTTPS")
g.edge("api", "worker", "Queue")
g.edge("api", "cache", "Read")
g.edge("worker", "db", "Write")
g.edge("worker", "metrics", style=Styles.MutedDashed)

g.draw(margin=10.0)
save()
```

---

## 1. When to Use `drawlib.graph` vs. `drawlib.diagrams`

Drawlib offers two complementary approaches to technical diagramming:

| Dimension | `drawlib.graph` (Auto-Layout Graphs) | [`drawlib.diagrams`](../05_diagrams/overview.md) (Coordinate Diagrams) |
| :--- | :--- | :--- |
| **Coordinate Placement** | **Automatic**: Solvers calculate `(x, y)` coordinates from topology (`node`, `edge`, `cluster`). | **Deterministic**: You specify exact `(x, y)` coordinates (`d.add(node, xy=(x, y))`). |
| **Primary Strength** | Solving the **Cold-Start Problem**; rapid topology prototyping, large DAGs, trees, and matrices. | Domain-specific notations and rich icon cards (`GcpIcon`, `PhosphorIcon`), UML compartments, Crow's Foot ER tables, and chronological lifelines. |
| **Fine-Tuning** | Post-layout nudging via `layout.offset(id, dx, dy)` or scaffolding to primitive code via `g.export_code()`. | Direct coordinate control, explicit attachment sides (`start_side`, `end_side`), and `Junction` bus lines. |
| **Animation Support** | Full visibility (`show=False`) and `scale` support on nodes, edges, clusters, and `GraphLayout` ([Animating Graphs](../07_animations/graphs.md)). | Full visibility (`show=False`) and `scale` support ([Animating Diagrams](../07_animations/diagrams.md)). |

---

## 2. The Five Specialized Layout Solvers

Rather than forcing every graph through a single generic force-directed or Sugiyama heuristic, `drawlib.graph` provides five purpose-built solvers tailored to distinct topological structures:

| Solver Class | Layout Algorithm | Primary Use Cases | Key Helper Methods | Guide Link |
| :--- | :--- | :--- | :--- | :--- |
| **[`ArchitectureGraph`](./architecture_graph.md)** | 2-Level Macro/Micro Packing + 5-Zone Compass | Cloud VPCs, nested subnets, multi-zone microservices | `.group()`, `.cluster(parent=..., pos=...)` | [ArchitectureGraph](./architecture_graph.md) |
| **[`LayerGraph`](./layer_graph.md)** | Sugiyama Hierarchical DAG (Cycle removal, Barycenter ordering) | CI/CD pipelines, ETL dataflows, layered dependency DAGs | `.tier(name, nodes, layer=...)`, `node(..., layer=...)` | [LayerGraph](./layer_graph.md) |
| **[`TreeGraph`](./tree_graph.md)** | Reingold-Tilford / Buchheim Compact Tree | Org charts, ASTs, decision trees, call hierarchies | `.child(parent, child_id, ...)` | [TreeGraph](./tree_graph.md) |
| **[`RadialGraph`](./radial_graph.md)** | Concentric BFS Rings & Angular Sector Allocation | Hub-and-spoke meshes, Pub/Sub topologies, dependency radars | `.spoke(parent, spoke_id, ring=...)`, `draw_ring_guides=True` | [RadialGraph](./radial_graph.md) |
| **[`GridGraph`](./grid_graph.md)** | 2D Matrix Assignment & Smart Channel Routing | Service catalogs, state matrices, tabular component grids | `.cell(id, row, col)`, `.cluster_row()`, `.cluster_column()` | [GridGraph](./grid_graph.md) |

---

## 3. Shared Architecture (`BaseGraph`)

All five solvers inherit from `BaseGraph` and share a unified API for building topologies, calculating layouts, rendering to the canvas, and exporting standalone code:

```python
from drawlib.graph import (
    ArchitectureGraph,
    BaseGraph,
    Cluster,
    ClusterLayout,
    Edge,
    EdgeLayout,
    GraphLayout,
    GridGraph,
    LayerGraph,
    Node,
    NodeLayout,
    RadialGraph,
    TreeGraph,
)
```

### 3.1. Building Topologies (`node`, `edge`, `cluster`, `group`)

#### `g.node(...) -> Node`
Registers a node in the graph and returns a mutable `Node` dataclass instance.
- **Signature**:
  ```python
  g.node(
      id: str,
      label: str | None = None,
      *,
      style: Style | None = None,
      text_style: Style | None = None,
      shape: Literal["rectangle", "circle"] = "rectangle",
      width: float | None = None,
      height: float | None = None,
      ring: int | None = None,
      row: int | None = None,
      col: int | None = None,
      layer: int | None = None,
      group: str | None = None,
      subgroup: str | None = None,
      show: bool = True,
  ) -> Node
  ```
- **Note**: `drawlib.graph` nodes are geometric shapes (`"rectangle"` or `"circle"`, with corner rounding controlled via `style.shape_r`) and do not take an `icon` parameter. For icon-centric architecture cards (`GcpIcon`, `PhosphorIcon`), use [`ArchitectureDiagram`](../05_diagrams/architecture.md) or overlay icons at computed `layout.nodes[id].xy` coordinates.

#### `g.edge(...) -> Edge`
Registers a directed or undirected edge between `src` and `dst` (automatically creating undeclared endpoint nodes with default styling).
- **Signature**:
  ```python
  g.edge(
      src: str,
      dst: str,
      label: str | None = None,
      *,
      style: Style | None = None,
      text_style: Style | None = None,
      arrow_head: Literal["->", "<-", "<->", "-"] = "->",
      line_style: Literal["solid", "dashed", "dotted"] | None = None,
      show: bool = True,
  ) -> Edge
  ```

#### `g.cluster(...) -> Cluster` and `g.group(...) -> Cluster`
Groups a list of nodes inside a labeled boundary rectangle (defaulting to `Styles.MutedDashed`).
- **Signatures**:
  ```python
  g.cluster(
      id: str,
      nodes: list[str],
      label: str | None = None,
      *,
      style: Style | None = None,
      text_style: Style | None = None,
      padding: float = 4.0,
      parent: str | None = None,
      order: int | None = None,
      pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
      show: bool = True,
  ) -> Cluster

  g.group(
      id: str,
      label: str | None = None,
      *,
      nodes: list[str] | None = None,
      style: Style | None = None,
      text_style: Style | None = None,
      padding: float = 4.0,
      parent: str | None = None,
      order: int | None = None,
      pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
      show: bool = True,
  ) -> Cluster
  ```

---

### 3.2. Layout Lifecycle (`calc`, `offset`, `draw`, `export_code`)

`drawlib.graph` supports a progressive three-stage workflow:

```drawlib fold-code 650px center file:graph_overview_lifecycle_stages.png caption:"Three Progressive Workflows in drawlib.graph: Auto-Draw, Calculate & Offset, and Export Standalone Code"
from drawlib.canvas import save, setup
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=186, height=74)

# Top Header / Input Node
rectangle(
    (93, 62),
    width=142,
    height=13,
    style=Styles.PrimaryNeutral.patch(shape_r=2.5),
)
text((93, 64.5), "Declarative Graph Topology", style=Styles.DarkBold.patch(text_size=10.5))
text((93, 59.0), "g.node()   ·   g.edge()   ·   g.cluster()   ·   g.group()", style=Styles.Dark.patch(text_size=8.5))

# Orthogonal fan-out lines from top header into the 3 workflow cards
line((93, 55.5), (93, 39.5), arrow_head="->", style=Styles.DarkBold)
lines([(93, 47.5), (33, 47.5), (33, 39.5)], arrow_head="->", style=Styles.DarkBold)
lines([(93, 47.5), (153, 47.5), (153, 39.5)], arrow_head="->", style=Styles.DarkBold)

# Card 1: Direct Auto-Draw (Neutral)
rectangle((33, 22), width=54, height=35, style=Styles.Neutral.patch(shape_r=2.5))
text((33, 33.5), "1. Direct Auto-Draw", style=Styles.DarkBold.patch(text_size=9.5))
rectangle((33, 23.5), width=46, height=9.5, style=Styles.White.patch(shape_r=1.5))
text((33, 23.5), "g.draw(margin=10.0)", style=Styles.PrimaryBold.patch(text_size=8.5))
text((33, 11.5), "One-step layout\n& canvas render", style=Styles.Dark.patch(text_size=8.0))

# Card 2: Calculate, Offset & Overlay (PrimaryFlat focal card)
rectangle((93, 22), width=56, height=35, style=Styles.PrimaryFlat.patch(shape_r=2.5))
text((93, 33.5), "2. Calculate, Offset & Overlay", style=Styles.WhiteBold.patch(text_size=9.0))
rectangle((93, 23.5), width=48, height=11.0, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
text((93, 23.5), "layout = g.calc()\nlayout.offset() -> layout.draw()", style=Styles.DarkBold.patch(text_size=7.8))
text((93, 11.0), "Inspect layout.nodes[id].x, y\n& overlay custom callouts", style=Styles.White.patch(text_size=7.8))

# Card 3: Export Standalone Code (SecondaryNeutral)
rectangle((153, 22), width=54, height=35, style=Styles.SecondaryNeutral.patch(shape_r=2.5))
text((153, 33.5), "3. Export Standalone Code", style=Styles.DarkBold.patch(text_size=9.0))
rectangle((153, 23.5), width=46, height=9.5, style=Styles.White.patch(shape_r=1.5))
text((153, 23.5), "code = g.export_code()", style=Styles.DarkBold.patch(text_size=8.2))
text((153, 11.5), "Emit editable setup(),\nrectangle(), line(), save() script", style=Styles.Dark.patch(text_size=7.8))

save()
```

1. **Compute Layout (`layout = g.calc(*, width=None, height=None, margin=10.0) -> GraphLayout`)**:
   - Solves all coordinates without drawing onto the canvas.
   - Returns a `GraphLayout` instance containing:
     - `layout.nodes`: `dict[str, NodeLayout]` — each `NodeLayout` exposes `.id`, `.xy`, `.x`, `.y`, `.width`, `.height`, `.left`, `.right`, `.top`, `.bottom`, `.style`, `.text_style`, `.label`, `.shape`, and `.show`.
     - `layout.edges`: `list[EdgeLayout]` — each `EdgeLayout` exposes `.src`, `.dst`, `.src_port`, `.dst_port`, `.waypoints`, `.points`, `.label`, `.style`, `.text_style`, `.arrow_head`, and `.show`.
     - `layout.clusters`: `dict[str, ClusterLayout]` — each `ClusterLayout` exposes `.id`, `.label`, `.bbox`, `.cx`, `.cy`, `.width`, `.height`, `.left`, `.right`, `.top`, `.bottom`, `.style`, `.text_style`, `.shape`, and `.show`.
     - `layout.width`, `layout.height`: Target canvas dimensions.
2. **Post-Layout Fine-Tuning (`layout.offset(node_id, dx=0.0, dy=0.0) -> None`)**:
   - Shifts a specific node by `(dx, dy)` and automatically updates the attachment ports of all incident edges.
   - You can also inspect `layout.nodes[id].x` and `.y` to attach custom primitives from [`drawlib.shapes`](../02_drawing_primitives/shapes_basic.md) or [`drawlib.icons`](../02_drawing_primitives/icons_phosphor.md).
3. **Render to Canvas (`g.draw(*, xy=(0.0, 0.0), width=None, height=None, margin=10.0, scale=1.0) -> GraphLayout` or `layout.draw(*, xy=(0.0, 0.0), scale=1.0) -> None`)**:
   - Renders visible clusters, edges, and nodes in proper z-order onto the active canvas, translated by `xy` and proportionally scaled by `scale`.
   - **Fixed-Layout Visibility (`show=False`)**: Setting `show=False` on any node, edge, or cluster preserves its slot during `calc()` so remaining elements never jump, while skipping hidden elements (and edges attached to hidden endpoint nodes) during `draw()`.
4. **Export Editable Primitive Code (`g.export_code(*, width=None, height=None, margin=10.0) -> str` or `layout.to_code() -> str`)**:
   - Generates a complete, self-contained Drawlib Python script using `setup()`, `rectangle()`, `circle()`, `line()`, and `save()` with all solved coordinates baked in as semantic variables (`api_xy = (85.0, 62.0)`).

```drawlib show-code 680px center file:graph_overview_offset_overlay.png caption:"Calculating Layout with calc(), Shifting a Node with offset(), and Attaching a Speech Callout"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.shapes import bubblespeech
from drawlib.styles import Styles

setup(width=155, height=78)

g = LayerGraph(direction="LR", default_node_width=26.0)
g.node("ingest", "Ingest", style=Styles.Neutral)
g.node("process", "Stream Engine", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("store", "Data Lake", style=Styles.SecondaryNeutral)

g.edge("ingest", "process")
g.edge("process", "store")

# 1. Calculate layout without rendering
layout = g.calc(margin=14.0)

# 2. Fine-tune the middle node position and draw the graph
layout.offset("process", dy=-6.0)
layout.draw()

# 3. Overlay a custom primitive anchored to the computed node coordinates
proc = layout.nodes["process"]
bubblespeech(
    (proc.x - 18.0, proc.y + 14.0),
    width=36.0,
    height=12.0,
    tail_edge="bottom",
    tail_start_ratio=0.4,
    tail_end_ratio=0.6,
    tail_vertex_xy=(proc.x, proc.y + proc.height / 2.0 + 1.0),
    style=Styles.WarningNeutral,
    text="Auto-scaled x8",
)

save()
```

---

## 4. Best Practices & 50%+ Neutral Baseline

1. **Override `default_node_style=Styles.Neutral` for the 50%+ Neutral Baseline**:
   - By default, `BaseGraph` initializes `default_node_style=Styles.PrimaryFlat` if none is supplied. In multi-node graphs, leaving every node in `Styles.PrimaryFlat` creates a visually heavy, over-saturated diagram.
   - Pass `default_node_style=Styles.Neutral` in the graph constructor (or style supporting nodes in `Styles.Neutral`, `Styles.PrimaryNeutral`, and `Styles.SecondaryNeutral`), and explicitly pass `style=Styles.PrimaryFlat, text_style=Styles.WhiteBold` on only **1–2 primary focal nodes**.
2. **Use `calc()` + `offset()` Before Exporting Code**:
   - Start with `g.draw()` to iterate rapidly on your topology. If a specific node or edge needs slight adjustment, switch to `layout = g.calc()` and `layout.offset(id, dx=..., dy=...)`—or call `g.export_code()` once the structure stabilizes to customize individual primitives freely.

---

## 5. Chapter Navigation

Explore each of the five graph solvers in detail:
- **[ArchitectureGraph](./architecture_graph.md)**: Multi-tier cloud topologies, nested VPC/subnet clusters, and 5-zone compass placement.
- **[LayerGraph](./layer_graph.md)**: Sugiyama hierarchical DAGs, CI/CD pipelines, and explicit rank/tier pinning.
- **[TreeGraph](./tree_graph.md)**: Balanced parent-child trees (`TB` and `LR`) using the Reingold-Tilford / Buchheim algorithm.
- **[RadialGraph](./radial_graph.md)**: Hub-and-spoke networks and multi-ring concentric dependency radars.
- **[GridGraph](./grid_graph.md)**: 2D `(row, col)` matrix placement, row/column clusters, and smart channel routing.
