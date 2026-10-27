# Drawlib Graph Overview Guidelines (`lib-graph-overview`)

`drawlib.graph` is a **pure coordinate and layout calculator** (`get_layout()`) that computes node centers/corners, nested container bounding boxes, and orthogonal or straight edge waypoints from topological declarations (`Node`, `Edge`, `Cluster`).

---

## 1. Sub-Topic Routing Table & Solver Selection Matrix

Query the dedicated rule manual for each graph solver using `uv run drawlib rules show <rule-id>`:

| Rule ID | Solver Class | Algorithm / Strategy | Primary Use Cases & Key Helper Methods | Typical Rendering Partner |
| :--- | :--- | :--- | :--- | :--- |
| **`lib-graph-architecture`** | `ArchitectureGraph` | 2-Level Macro/Micro Container + 5-Zone Compass Packing | Cloud infrastructure, VPCs/subnets, multi-zone microservices (`.group()`, `.cluster(parent=..., pos=..., order=...)`) | `ArchitectureDiagram` (`NodeGroup`, `Node`, `GcpIcon`, `PhosphorIcon`) |
| **`lib-graph-layer`** | `LayerGraph` | Sugiyama Hierarchical DAG (Cycle removal, Barycenter crossing reduction) | CI/CD pipelines, dataflows, ETL/Airflow DAGs, layered dependency graphs (`.tier(name, nodes, layer=...)`) | `FlowDiagram`, `ArchitectureDiagram`, or `shapes` / `lines` |
| **`lib-graph-tree`** | `TreeGraph` | Reingold-Tilford / Buchheim Compact Tree | Org charts, ASTs, decision trees, taxonomies (`.child(parent, child_id, ...)`) | `shapes.rectangle` + `lines.lines` or `FlowDiagram` |
| **`lib-graph-radial`** | `RadialGraph` | Concentric BFS Rings & Angular Sector Allocation | Hub-and-spoke networks, Pub/Sub meshes, ecosystem rings (`.spoke(parent, spoke_id, ring=...)`, `layout.ring_radii`) | `shapes.circle` / `rectangle` + `lines.line` |
| **`lib-graph-grid`** | `GridGraph` | 2D Matrix Slot Assignment & Inter-Cell Channel Routing | Service catalogs, state matrices, tabular networks (`.cell()`, `.cluster_row()`, `.cluster_column()`) | `shapes.rectangle` + `lines.lines` or `ArchitectureDiagram` |

### Public Exports (`drawlib.graph`)

```python
from drawlib.graph import (
    # Specialized Graph Solvers
    ArchitectureGraph,
    BaseGraph,
    GridGraph,
    LayerGraph,
    RadialGraph,
    TreeGraph,
    # Input Declaration Models
    Cluster,
    Edge,
    Node,
    # Computed Layout Models
    ClusterLayout,
    EdgeLayout,
    GraphLayout,
    NodeLayout,
)
```

---

## 2. Core Philosophy: Pure Coordinate Calculator & 2-Step Workflow

Manually calculating every `(x, y)` coordinate and container bounding box is tedious when topologies evolve, while black-box auto-layout tools that render directly (like Graphviz) make it impossible to customize individual node icons, card styles, or wire ports.

**`drawlib.graph` is strictly a pure geometry solver (`get_layout()` only)**:
- It has **no `.draw()` method** and **no visual styling or label attributes** (`style`, `text_style`, `label`, `shape`, `show` do not exist on `drawlib.graph`).
- Instead, use `drawlib.graph` in a deterministic **2-Step Workflow**:

1. **Step 1 — Declare Topology & Compute Layout (`layout = g.get_layout()`)**:
   - Declare nodes (`g.node("id", width=..., height=...)`), edges (`g.edge("src", "dst")`), and clusters (`g.cluster("id", nodes=[...], padding=..., header_height=...)`).
   - Call `layout = g.get_layout(width=..., height=..., margin=10.0)` to compute the `GraphLayout`.
   - Inspect solved coordinates via `print(layout)` (`str(layout)`) to copy literal coordinates into standalone drawing code (replacing legacy `.to_code()` / `.export_code()` workflows), or reference `layout["id"]` (`layout.nodes["id"]`, `layout.clusters["id"]`, `layout.edges`) directly in Step 2.
2. **Step 2 — Render with `drawlib.diagrams` or `drawlib.shapes` / `drawlib.lines`**:
   - Pass the solved coordinates into `ArchitectureDiagram` (`xy=layout["vpc"].bottom_left`, `xy=layout["sub"].local_bottom_left`, `xy=layout["api"].local_xy`), `FlowDiagram` (`xy=layout["step"].xy`), or primitive `rectangle(n.xy, ...)`, `circle(n.xy, ...)`, and `lines(e.points, arrow_head="->")`.

```drawlib align=center code=fold file=graph_overview_two_step.png caption="2-Step Workflow: Step 1 (LayerGraph.get_layout()) -> Step 2 (Render with Shapes & Lines)"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.lines import lines
from drawlib.shapes import circle
from drawlib.styles import Styles

setup(width=100, height=52)

# Step 1: Declare topology & solve coordinates with get_layout()
g = LayerGraph(direction="LR", default_node_width=16.0, default_node_height=16.0)
g.edge("A", "B")
g.edge("A", "C")
g.edge("B", "D")
g.edge("C", "D")

layout = g.get_layout(margin=8.0)

# Step 2: Render edges and nodes using solved coordinates
for e in layout.edges:
    lines(e.points, arrow_head="->", style=Styles.DarkBold)

circle(layout["A"].xy, radius=8.0, style=Styles.PrimaryFlat, text="A\n(16, 26)", text_style=Styles.WhiteBold.patch(text_size=10.0))
circle(layout["B"].xy, radius=8.0, style=Styles.PrimaryNeutral, text="B\n(50, 36)", text_style=Styles.DarkBold.patch(text_size=10.0))
circle(layout["C"].xy, radius=8.0, style=Styles.PrimaryNeutral, text="C\n(50, 16)", text_style=Styles.DarkBold.patch(text_size=10.0))
circle(layout["D"].xy, radius=8.0, style=Styles.SecondaryNeutral, text="D\n(84, 26)", text_style=Styles.DarkBold.patch(text_size=10.0))

save()
```

---

## 3. Common Graph API (`BaseGraph`) & Input Models (`Node`, `Edge`, `Cluster`)

All five solvers inherit from `BaseGraph`:

```python
BaseGraph(*, default_node_width: float = 20.0, default_node_height: float = 12.0)
```

### 3.1 `g.node(...) -> Node`
Registers a node in the graph and returns a `Node` dataclass instance:

```python
g.node(
    id: str,
    *,
    width: float | None = None,
    height: float | None = None,
    ring: int | None = None,
    row: int | None = None,
    col: int | None = None,
    layer: int | None = None,
    group: str | None = None,
    subgroup: str | None = None,
) -> Node
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(Required)* | Unique node identifier string. |
| `width` | `float \| None` | `None` | Custom node width (defaults to solver's `default_node_width`). |
| `height` | `float \| None` | `None` | Custom node height (defaults to solver's `default_node_height`). |
| `layer` | `int \| None` | `None` | Explicit rank/layer index for `LayerGraph` (`0` = first rank). |
| `ring` | `int \| None` | `None` | Explicit concentric ring index for `RadialGraph` (`0` = center hub). |
| `row`, `col` | `int \| None` | `None` | Explicit 0-based matrix coordinates for `GridGraph`. |
| `group`, `subgroup` | `str \| None` | `None` | Container/group and nested subgroup IDs for `ArchitectureGraph`. |

### 3.2 `g.edge(src, dst) -> Edge`
Registers a directed topological connection (`Edge(src, dst)`). Any node ID referenced in `src` or `dst` that has not been explicitly registered via `g.node()` is auto-registered with the solver's default dimensions during `get_layout()`.

### 3.3 `g.cluster(...) -> Cluster` & `g.group(...) -> Cluster`
Registers a grouping boundary container (`Cluster`) around a subset of nodes:

```python
g.cluster(
    id: str,
    nodes: list[str] | None = None,
    *,
    padding: float = 4.0,
    header_height: float = 3.5,
    parent: str | None = None,
    order: int | None = None,
    pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
) -> Cluster

# Keyword-only nodes alias on BaseGraph:
g.group(
    id: str,
    *,
    nodes: list[str] | None = None,
    padding: float = 4.0,
    header_height: float = 3.5,
    parent: str | None = None,
    order: int | None = None,
    pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
) -> Cluster
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(Required)* | Unique cluster/group identifier string. |
| `nodes` | `list[str] \| None` | `None` | List of member node IDs enclosed by this cluster. |
| `padding` | `float` | `4.0` | Internal margin between the cluster border and enclosed nodes/subclusters. |
| `header_height` | `float` | `3.5` | Extra top clearance reserved for the container's title banner. |
| `parent` | `str \| None` | `None` | Parent cluster ID for nested boundaries (e.g. Subnet inside VPC). |
| `order` | `int \| None` | `None` | Explicit ordering rank among sibling containers (`ArchitectureGraph`). |
| `pos` | `Literal["top", "bottom", "left", "right", "center"] \| None` | `None` | 2D macro compass placement (`ArchitectureGraph`). |

### 3.4 `g.get_layout(...) -> GraphLayout`

```python
layout = g.get_layout(
    *,
    width: float | None = None,
    height: float | None = None,
    margin: float = 10.0,
) -> GraphLayout
```
Computes all node positions, cluster bounding boxes, local cluster-relative coordinates, and edge waypoints without rendering. Defaults `width` and `height` to the active `drawlib.canvas` dimensions when `setup()` has been called.

---

## 4. Computed Layout Models (`GraphLayout`, `NodeLayout`, `ClusterLayout`, `EdgeLayout`)

### 4.1 Coordinate Anchor Reference Table

`layout[key]` looks up either a `NodeLayout` (in `layout.nodes`) or a `ClusterLayout` (in `layout.clusters`):

| Layout Model | Key Properties & Methods | Anchor Semantics & Rendering Usage |
| :--- | :--- | :--- |
| **`GraphLayout`** | • `.nodes: dict[str, NodeLayout]`<br>• `.clusters: dict[str, ClusterLayout]`<br>• `.edges: list[EdgeLayout]`<br>• `.width: float`, `.height: float`<br>• `.ring_radii: dict[int, float]`<br>• `layout[key] -> NodeLayout \| ClusterLayout`<br>• `layout.offset(node_id, dx=0.0, dy=0.0) -> Self`<br>• `str(layout)` / `print(layout)` | • Dictionary lookup `layout["id"]` for nodes and clusters.<br>• `.offset(node_id, dx, dy)` shifts a node and recalculates its incident edge ports.<br>• `print(layout)` outputs a formatted coordinate table for inspection or code generation (replacing `.to_code()`). |
| **`NodeLayout`** | • `.xy` / `.center`: `tuple[float, float]` (**center `(cx, cy)`**)<br>• `.x: float`, `.y: float`<br>• `.bottom_left`: `tuple[float, float]` (**corner `(left, bottom)`**)<br>• `.local_xy`: `tuple[float, float]` (**center relative to parent cluster's `bottom_left`**)<br>• `.local_bottom_left`: `tuple[float, float]` (**corner relative to parent cluster's `bottom_left`**)<br>• `.width: float`, `.height: float`, `.size: (w, h)`<br>• `.left`, `.right`, `.bottom`, `.top`<br>• `.parent_id: str \| None` | • **Global Center (`.xy`)**: Pass to top-level `d.add(Node(...), xy=nl.xy)`, `flow.add(..., xy=nl.xy)`, `rectangle(nl.xy, ...)`, `circle(nl.xy, ...)`.<br>• **Cluster-Local Center (`.local_xy`)**: Pass to `group.add(Node(...), xy=nl.local_xy)` inside an `ArchitectureDiagram` `NodeGroup`.<br>• **Bottom-Left Corner (`.bottom_left` / `.local_bottom_left`)**: Use when placing bottom-left anchored components (`SmartArts`, `Charts`). |
| **`ClusterLayout`** | • `.bottom_left`: `tuple[float, float]` (**corner `(left, bottom)`**)<br>• `.local_bottom_left`: `tuple[float, float]` (**corner relative to parent cluster's `bottom_left`**)<br>• `.xy` / `.center`: `tuple[float, float]` (**center `(cx, cy)`**)<br>• `.cx: float`, `.cy: float`<br>• `.width: float`, `.height: float`, `.size: (w, h)`<br>• `.left`, `.right`, `.bottom`, `.top`<br>• `.parent_id: str \| None` | • **Global Bottom-Left (`.bottom_left`)**: Pass to top-level `d.add(NodeGroup(...), xy=cl.bottom_left)`.<br>• **Parent-Relative Bottom-Left (`.local_bottom_left`)**: Pass to nested `parent_grp.add(NodeGroup(...), xy=cl.local_bottom_left)`.<br>• **Global Center (`.xy`)**: Pass to `rectangle(cl.xy, width=cl.width, height=cl.height)`. |
| **`EdgeLayout`** | • `.src: str`, `.dst: str`<br>• `.src_port: (x, y)`, `.dst_port: (x, y)`<br>• `.waypoints: list[(x, y)]`<br>• `.points: list[(x, y)]` (`[src_port, *waypoints, dst_port]`)<br>• `.mid_xy: (mx, my)` | • Pass `.points` to `lines(edge.points, arrow_head="->", style=...)`.<br>• Pass `.src_port, .dst_port` to `line(edge.src_port, edge.dst_port, arrow_head="->")`.<br>• Pass `.mid_xy` to `text(edge.mid_xy, "Label", ...)`. |

```text
  ClusterLayout ("vpc"):
  ┌─────────────────────────────────────────────────────────────────┐ ▲
  │ Header Title Banner (header_height=3.5)                         │ │
  │   ┌───────────────────────────────┐                             │ │
  │   │ NodeLayout ("api")            │                             │ │ cl.height
  │   │       ● nl.xy (global center) │                             │ │
  │   │         nl.local_xy           │                             │ │
  │   ●───────────────────────────────┘                             │ │
  │   nl.bottom_left / nl.local_bottom_left                         │ ▼
  ●─────────────────────────────────────────────────────────────────┘
  cl.bottom_left (global) / cl.local_bottom_left (inside parent cluster)
  ◄─────────────────────────── cl.width ────────────────────────────►
```

### 4.2 Inspecting Coordinates (`print(layout)`) & Post-Solve Nudging (`layout.offset()`)

- **Inspecting Solved Coordinates (`print(layout)` / `str(layout)`)**:
  Instead of calling a `.to_code()` or `.export_code()` method, pass `layout` directly to `print(layout)` (`GraphLayout.__str__`) to inspect all computed cluster bounds, node centers/corners, local coordinates, and edge waypoints:
  ```python
  layout = g.get_layout(width=160, height=80, margin=10.0)
  print(layout)
  # GraphLayout(width=160.0, height=80.0)
  # Clusters:
  #   vpc : bottom_left=(65.0, 20.5), center=(104.0, 40.0), size=(78.0, 39.0)
  # Nodes:
  #   api : xy=(86.0, 38.25), bottom_left=(74.0, 31.25), size=(24.0, 14.0), parent='vpc', local_xy=(21.0, 17.75)
  ```
- **Fine-Tuning Node Positions (`layout.offset(node_id, dx=0.0, dy=0.0) -> Self`)**:
  Shifts `layout.nodes[node_id]` by `(dx, dy)` (updating both `.xy` and `.local_xy` as well as incident `edge.src_port` / `edge.dst_port` coordinates) and returns `self` for method chaining:

```drawlib align=center code=fold file=graph_overview_offset.png caption="Post-Calculation Coordinate Nudging with GraphLayout.offset()"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.lines import lines
from drawlib.shapes import bubblespeech, rectangle
from drawlib.styles import Styles

setup(width=150, height=75)

g = LayerGraph(direction="LR", default_node_width=28.0, default_node_height=12.0)
g.edge("ingest", "process")
g.edge("process", "store")

# Nudge "process" downward by 6 units to make room for a callout bubble above it
layout = g.get_layout(margin=14.0).offset("process", dy=-6.0)

for edge in layout.edges:
    lines(edge.points, arrow_head="->", style=Styles.DarkBold)

specs = [
    ("ingest", "Ingest", Styles.Neutral, Styles.DarkBold),
    ("process", "Stream Engine", Styles.PrimaryFlat, Styles.WhiteBold),
    ("store", "Data Lake", Styles.SecondaryNeutral, Styles.DarkBold),
]
for nid, label, style, text_style in specs:
    n = layout[nid]
    rectangle(n.xy, width=n.width, height=n.height, style=style.patch(shape_r=1.5), text=label, text_style=text_style)

proc = layout["process"]
bubblespeech(
    (proc.x, proc.y + 18.0),
    width=36.0,
    height=11.0,
    tail_edge="bottom",
    tail_start_ratio=0.4,
    tail_end_ratio=0.6,
    tail_vertex_xy=(proc.x, proc.top + 1.0),
    style=Styles.WarningNeutral,
    text="Auto-scaled x8",
)

save()
```
