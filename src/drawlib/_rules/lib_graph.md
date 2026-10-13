# Drawlib Graph Guidelines

This document provides the complete technical specification, solver catalog, and 2-step programmatic workflow for `drawlib.graph`.

---

## Table of Contents

- [1. Module Overview & Architecture](#1-module-overview--architecture)
  - [1.1. Public Exports](#11-public-exports)
  - [1.2. Core Philosophy: Pure Coordinate Calculator & 2-Step Workflow](#12-core-philosophy-pure-coordinate-calculator--2-step-workflow)
  - [1.3. Solver Selection Matrix](#13-solver-selection-matrix)
- [2. Common Graph API (`BaseGraph`)](#2-common-graph-api-basegraph)
  - [2.1. Declaring Nodes, Edges, and Clusters](#21-declaring-nodes-edges-and-clusters)
  - [2.2. Computing the Layout (`get_layout()`)](#22-computing-the-layout-get_layout)
- [3. Specialized Layout Solvers & 2-Step Recipes](#3-specialized-layout-solvers--2-step-recipes)
  - [3.1. `ArchitectureGraph` + `ArchitectureDiagram` (Cloud & System Topologies)](#31-architecturegraph--architecturediagram-cloud--system-topologies)
  - [3.2. `LayerGraph` + `FlowDiagram` (Hierarchical DAGs & Pipelines)](#32-layergraph--flowdiagram-hierarchical-dags--pipelines)
  - [3.3. `TreeGraph` + `shapes` / `lines` (Hierarchies & Taxonomies)](#33-treegraph--shapes--lines-hierarchies--taxonomies)
  - [3.4. `RadialGraph` + `shapes` / `lines` (Hub-and-Spoke & Concentric Rings)](#34-radialgraph--shapes--lines-hub-and-spoke--concentric-rings)
  - [3.5. `GridGraph` + `shapes` / `lines` (Matrix Layouts & Service Catalogs)](#35-gridgraph--shapes--lines-matrix-layouts--service-catalogs)
- [4. Layout Models & Post-Calculation Adjustment (`GraphLayout`)](#4-layout-models--post-calculation-adjustment-graphlayout)
  - [4.1. Coordinate Properties Reference (`NodeLayout`, `ClusterLayout`, `EdgeLayout`)](#41-coordinate-properties-reference-nodelayout-clusterlayout-edgelayout)
  - [4.2. Inspecting (`print(layout)`) & Offsetting (`layout.offset()`)](#42-inspecting-printlayout--offsetting-layoutoffset)
- [5. Best Practices & Anti-Patterns](#5-best-practices--anti-patterns)

---

## 1. Module Overview & Architecture

The `drawlib.graph` module is a **pure coordinate and layout calculator** that computes node coordinates, nested container bounding boxes, and orthogonal or straight edge waypoints from topological relationships (nodes, edges, and clusters).

### 1.1. Public Exports

```python
from drawlib.graph import (
    # Specialized Graph Solvers
    ArchitectureGraph,
    LayerGraph,
    TreeGraph,
    RadialGraph,
    GridGraph,
    BaseGraph,
    # Input Declaration Models
    Node,
    Edge,
    Cluster,
    # Computed Layout Models
    GraphLayout,
    NodeLayout,
    EdgeLayout,
    ClusterLayout,
)
```

### 1.2. Core Philosophy: Pure Coordinate Calculator & 2-Step Workflow

Writing complex diagrams from scratch by mentally calculating every `(x, y)` coordinate and container bounding box is error-prone when topologies evolve. Conversely, black-box auto-layout tools that render directly (like Graphviz) make it impossible to customize individual node icons, card styles, or wire ports.

To give you the best of both worlds, **`drawlib.graph` is strictly a pure geometry solver (`get_layout()` only)**:
- It has **no `.draw()` method**, **no `.export_code()` method**, and **no visual styling or label attributes** (`style`, `text_style`, `label`, `shape`, `show` do not exist on `drawlib.graph`).
- Instead, you use `drawlib.graph` in a clean **2-Step Workflow**:

1. **Step 1 — Solve & Inspect Topology (`layout = g.get_layout()`)**:
   - Declare nodes (`g.node("id", width=..., height=...)`), edges (`g.edge("src", "dst")`), and clusters (`g.cluster("id", nodes=[...], padding=..., header_height=...)`).
   - Call `layout = g.get_layout(width=..., height=..., margin=10.0)` to compute the `GraphLayout`.
   - You can either inspect the solved coordinates via `print(layout)` in a one-liner to copy exact numbers into your script, or reference `layout["id"]` (`layout.nodes["id"]`, `layout.clusters["id"]`, `layout.edges`) programmatically.
2. **Step 2 — Render with `drawlib.diagrams` or `drawlib.shapes` / `drawlib.lines`**:
   - Pass the solved coordinates into `ArchitectureDiagram` (`xy=layout["vpc"].bottom_left`, `xy=layout["sub"].local_bottom_left`, `xy=layout["api"].local_xy`), `FlowDiagram` (`xy=layout["step"].xy`), or primitive `rectangle(n.xy, ...)`, `circle(n.xy, ...)`, and `lines(e.points, arrow_head="->")`.

### 1.3. Solver Selection Matrix

| Solver Class | Algorithm / Strategy | Best Used For | Key Helper Methods | Typical Rendering Partner |
| :--- | :--- | :--- | :--- | :--- |
| **`ArchitectureGraph`** | 2-Level Macro/Micro Container + Compass Packing | Cloud architectures, VPCs/subnets, multi-zone microservices | `.group()`, `.cluster(parent=..., pos=...)` | `ArchitectureDiagram` (`NodeGroup`, `Node`, `GcpIcon`, `PhosphorIcon`) |
| **`LayerGraph`** | Sugiyama Hierarchical DAG (Cycle removal, Barycenter ordering) | CI/CD pipelines, dataflows, layered dependency graphs | `.tier(name, nodes, layer=...)` | `FlowDiagram`, `ArchitectureDiagram`, or `shapes`/`lines` |
| **`TreeGraph`** | Reingold-Tilford / Buchheim Compact Tree | Org charts, ASTs, decision trees, taxonomies | `.child(parent, child_id, ...)` | `shapes.rectangle` + `lines.lines` or `FlowDiagram` |
| **`RadialGraph`** | Concentric BFS Rings & Angular Sector Allocation | Hub-and-spoke networks, ecosystem maps, dependency rings | `.spoke(parent, spoke_id, ring=...)` | `shapes.circle` / `rectangle` + `lines.line` (`layout.ring_radii`) |
| **`GridGraph`** | 2D Matrix Assignment & Channel Edge Routing | Service catalogs, state matrices, tabular networks | `.cell()`, `.cluster_row()`, `.cluster_column()` | `shapes.rectangle` + `lines.lines` or `ArchitectureDiagram` |

---

## 2. Common Graph API (`BaseGraph`)

All five solvers inherit from `BaseGraph` and share a unified topology declaration API:

```python
BaseGraph(*, default_node_width: float = 20.0, default_node_height: float = 12.0)
```

### 2.1. Declaring Nodes, Edges, and Clusters

#### `g.node(...) -> Node`
Registers a node in the graph and returns a `Node` geometry declaration object.

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
| `id` | `str` | *(required)* | Unique identifier for the node. |
| `width` | `float \| None` | `None` | Node width in canvas units (defaults to solver's `default_node_width`). |
| `height` | `float \| None` | `None` | Node height in canvas units (defaults to solver's `default_node_height`). |
| `layer` | `int \| None` | `None` | Explicit rank/layer index for `LayerGraph` (`0` = first rank). |
| `ring` | `int \| None` | `None` | Explicit concentric ring index for `RadialGraph` (`0` = center hub). |
| `row`, `col` | `int \| None` | `None` | Explicit 0-based grid coordinates for `GridGraph`. |
| `group`, `subgroup` | `str \| None` | `None` | Optional container/group and nested subgroup IDs for `ArchitectureGraph`. |

#### `g.edge(...) -> Edge`
Registers a directed topological connection between two nodes. If `src` or `dst` has not been declared via `.node()`, it is automatically created with the solver's default node dimensions.

```python
g.edge(src: str, dst: str) -> Edge
```

#### `g.cluster(...) -> Cluster` and `g.group(...) -> Cluster`
Groups nodes inside a hierarchical boundary container (such as a VPC, subnet, or pipeline stage) and reserves padding and header height during layout calculation.

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
| `id` | `str` | *(required)* | Unique cluster identifier. |
| `nodes` | `list[str] \| None` | `None` | List of node IDs contained in this cluster. |
| `padding` | `float` | `4.0` | Internal margin between the cluster border and enclosed nodes/subclusters. |
| `header_height` | `float` | `3.5` | Extra top clearance reserved for the container's title banner. |
| `parent` | `str \| None` | `None` | Parent cluster ID for nested containers (e.g., Subnet inside a VPC). |
| `order` | `int \| None` | `None` | Explicit sorting priority among sibling clusters (`ArchitectureGraph`). |
| `pos` | `Literal["top", "bottom", "left", "right", "center"] \| None` | `None` | Compass zone placement relative to the canvas (`ArchitectureGraph`). |

### 2.2. Computing the Layout (`get_layout()`)

Every graph solver provides `get_layout()` as its sole execution method:

```python
layout = g.get_layout(
    *,
    width: float | None = None,
    height: float | None = None,
    margin: float = 10.0,
) -> GraphLayout
```
Computes all node positions, cluster bounds, local cluster-relative coordinates, and edge waypoints across the full topology, returning a `GraphLayout` object. If `setup(width=..., height=...)` was already called on `drawlib.canvas`, `width` and `height` automatically default to the active canvas dimensions (`100.0 x 100.0` otherwise).

---

## 3. Specialized Layout Solvers & 2-Step Recipes

### 3.1. `ArchitectureGraph` + `ArchitectureDiagram` (Cloud & System Topologies)

`ArchitectureGraph` is purpose-built for cloud infrastructure and microservice architecture diagrams. It uses a **two-level hierarchical layout algorithm**:
1. **Micro Layout**: Packs nodes inside each leaf cluster (and recursively packs child clusters inside parent clusters).
2. **Macro Layout**: Arranges top-level clusters across a 5-zone compass (`pos="left" | "center" | "right" | "top" | "bottom"`) or along the primary flow axis (`direction="LR" | "TB"`), and computes `local_bottom_left` and `local_xy` coordinates that map 1-to-1 to `ArchitectureDiagram`'s `NodeGroup` hierarchy.

```python
ArchitectureGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    container_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 24.0,
    default_node_height: float = 12.0,
)
```

```drawlib code=show align=center file=lib_graph_architecture.png caption="Step 1: ArchitectureGraph.get_layout() -> Step 2: ArchitectureDiagram Rendering"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=215, height=130)

# Step 1: Solve topology coordinates with ArchitectureGraph
g = ArchitectureGraph(direction="LR", container_sep=16.0, default_node_width=24.0, default_node_height=15.0)
g.cluster("clients", ["client"], pos="left", padding=5.0)
g.group("vpc", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db", "cache"], parent="vpc", order=2, padding=5.0)
g.cluster("obs", ["metrics"], pos="bottom", padding=5.0)

g.edge("client", "api")
g.edge("api", "worker")
g.edge("worker", "db")
g.edge("worker", "cache")
g.edge("worker", "metrics")

layout = g.get_layout(margin=10.0)

# Step 2: Render rich cloud topology with ArchitectureDiagram using solved coordinates
d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
    node_card_style=Styles.Neutral,
)

# Top-level NodeGroups use .bottom_left; nested NodeGroups use .local_bottom_left
ext_grp = d.add(NodeGroup(title="External", padding=5.0, style=Styles.MutedDashed), xy=layout["clients"].bottom_left)
vpc_grp = d.add(NodeGroup(title="Production VPC", padding=5.0, style=Styles.MutedDashed), xy=layout["vpc"].bottom_left)
app_grp = vpc_grp.add(NodeGroup(title="Compute Tier", padding=5.0, style=Styles.PrimaryNeutral), xy=layout["app_tier"].local_bottom_left)
data_grp = vpc_grp.add(NodeGroup(title="Data Tier", padding=5.0, style=Styles.SecondaryNeutral), xy=layout["data_tier"].local_bottom_left)
obs_grp = d.add(NodeGroup(title="Observability", padding=5.0, style=Styles.MutedDashed), xy=layout["obs"].bottom_left)

# Nodes inside a NodeGroup use .local_xy
client = ext_grp.add(Node("Client App", width=24, height=15, icon=PhosphorIcon.DEVICES), xy=layout["client"].local_xy)
api = app_grp.add(
    Node("API Gateway", width=24, height=15, icon=GcpIcon.CLOUD_API_GATEWAY, style=Styles.White, card_style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.5)),
    xy=layout["api"].local_xy,
)
worker = app_grp.add(Node("Worker", width=24, height=15, icon=GcpIcon.CLOUD_RUN), xy=layout["worker"].local_xy)
db = data_grp.add(Node("Primary DB", width=24, height=15, icon=GcpIcon.CLOUD_SQL), xy=layout["db"].local_xy)
cache = data_grp.add(Node("Redis Cache", width=24, height=15, icon=GcpIcon.MEMORYSTORE), xy=layout["cache"].local_xy)
metrics = obs_grp.add(Node("Monitoring", width=24, height=15, icon=GcpIcon.CLOUD_MONITORING), xy=layout["metrics"].local_xy)

d.connect(client, api, label="HTTPS")
d.connect(api, worker)
worker.fork([db, cache], at_x=151.0)
d.connect(worker, metrics, style=Styles.MutedDashed)

d.draw()
save()
```

### 3.2. `LayerGraph` + `FlowDiagram` (Hierarchical DAGs & Pipelines)

`LayerGraph` implements a **Sugiyama-style layered DAG algorithm** (cycle removal via DFS, longest-path rank assignment with explicit `layer` pinning, barycenter crossing minimization, and orthogonal or straight routing). Use `.tier(name, nodes, *, layer=None)` to pin multiple nodes to the same stage, then render with `FlowDiagram` or primitives.

```python
LayerGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    rank_sep: float | None = None,
    node_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
)
```

```drawlib code=show align=center file=lib_graph_layer.png caption="Step 1: LayerGraph.get_layout() -> Step 2: FlowDiagram Rendering"
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

### 3.3. `TreeGraph` + `shapes` / `lines` (Hierarchies & Taxonomies)

`TreeGraph` computes proportional subtree widths (Reingold-Tilford / Buchheim contour algorithm) so sibling subtrees never overlap while keeping parents centered over their children. Use `.child(parent_id, child_id, *, width=None, height=None)` for concise tree construction.

```python
TreeGraph(
    *,
    root: str | None = None,
    direction: Literal["TB", "LR"] = "TB",
    level_sep: float | None = None,
    sibling_sep: float | None = None,
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
)
```

```drawlib code=show align=center file=lib_graph_tree.png caption="Step 1: TreeGraph.get_layout() -> Step 2: Primitives Rendering"
from drawlib.canvas import save, setup
from drawlib.graph import TreeGraph
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=160, height=85)

# Step 1: Solve symmetric tree coordinates with TreeGraph
g = TreeGraph(root="vp", direction="TB", default_node_width=28.0, default_node_height=11.0)
g.node("vp")
g.child("vp", "plat")
g.child("vp", "prod")
g.child("plat", "infra")
g.child("plat", "sec")
g.child("prod", "web")
g.child("prod", "mob")

layout = g.get_layout(margin=12.0)

# Step 2: Render orthogonal edges and styled cards using layout coordinates
for edge in layout.edges:
    lines(edge.points, arrow_head="->", style=Styles.DarkBold)

node_specs = [
    ("vp", "VP Engineering", Styles.PrimaryFlat, Styles.WhiteBold),
    ("plat", "Platform Team", Styles.PrimaryNeutral, Styles.DarkBold),
    ("prod", "Product Team", Styles.SecondaryNeutral, Styles.DarkBold),
    ("infra", "Cloud Infra", Styles.Neutral, Styles.Dark),
    ("sec", "Security", Styles.Neutral, Styles.Dark),
    ("web", "Web Frontend", Styles.Neutral, Styles.Dark),
    ("mob", "Mobile Apps", Styles.Neutral, Styles.Dark),
]
for nid, label, style, text_style in node_specs:
    n = layout[nid]
    rectangle(n.xy, width=n.width, height=n.height, style=style.patch(shape_r=1.5), text=label, text_style=text_style)

save()
```

### 3.4. `RadialGraph` + `shapes` / `lines` (Hub-and-Spoke & Concentric Rings)

`RadialGraph` places a central hub at `ring=0` and arranges connected nodes on concentric circles (`ring=1, 2, ...`), allocating angular sectors proportionally to subtree leaf counts to avoid edge crossings. The computed `GraphLayout.ring_radii` dictionary (`dict[int, float]`) provides exact radii for drawing concentric ring guide circles.

```python
RadialGraph(
    hub: str | None = None,
    *,
    center: tuple[float, float] | None = None,
    radius_step: float | None = None,
    start_angle: float = 0.0,
    angle_range: float = 360.0,
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
)
```

```drawlib code=show align=center file=lib_graph_radial.png caption="Step 1: RadialGraph.get_layout() -> Step 2: Ring Guides & Hub-and-Spoke Rendering"
from drawlib.canvas import save, setup
from drawlib.graph import RadialGraph
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

setup(width=170, height=130)

# Step 1: Solve concentric ring coordinates with RadialGraph
g = RadialGraph(hub="core", default_node_width=24.0, default_node_height=10.0)
g.node("core", width=24.0, height=24.0)

g.spoke("core", "auth")
g.spoke("core", "billing")
g.spoke("core", "orders")
g.spoke("core", "notify")

g.spoke("orders", "inv", ring=2)
g.spoke("orders", "ship", ring=2)

layout = g.get_layout(margin=18.0)

# Step 2: Render concentric ring guides, radial edges, and hub/spoke shapes
hub = layout["core"]
for r in layout.ring_radii.values():
    circle(hub.xy, radius=r, style=Styles.MutedDashed)

for edge in layout.edges:
    line(edge.src_port, edge.dst_port, arrow_head="->", style=Styles.DarkBold)

circle(hub.xy, radius=hub.width / 2, style=Styles.PrimaryFlat, text="Event Mesh", text_style=Styles.WhiteBold)

spoke_specs = [
    ("auth", "Auth API", Styles.PrimaryNeutral),
    ("billing", "Billing", Styles.PrimaryNeutral),
    ("orders", "Orders", Styles.SecondaryNeutral),
    ("notify", "Notify", Styles.PrimaryNeutral),
    ("inv", "Inventory", Styles.Neutral),
    ("ship", "Shipping", Styles.Neutral),
]
for nid, label, style in spoke_specs:
    n = layout[nid]
    rectangle(n.xy, width=n.width, height=n.height, style=style.patch(shape_r=1.5), text=label)

save()
```

### 3.5. `GridGraph` + `shapes` / `lines` (Matrix Layouts & Service Catalogs)

`GridGraph` places nodes into a structured 2D matrix `(row, col)`. Nodes without explicit `(row, col)` coordinates are automatically assigned to the next open cell in `"row-major"` or `"column-major"` order. Non-adjacent edges are routed cleanly through inter-row and inter-column channels when `edge_routing="smart"`.

```python
GridGraph(
    columns: int = 3,
    *,
    rows: int | None = None,
    order: Literal["row-major", "column-major"] = "row-major",
    col_sep: float | None = None,
    row_sep: float | None = None,
    edge_routing: Literal["smart", "orthogonal", "straight"] = "smart",
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
)
```

Helper methods on `GridGraph`:
- `g.cell(cell_id: str, row: int | None = None, col: int | None = None, *, width: float | None = None, height: float | None = None) -> Node`
- `g.cluster_row(row: int, cluster_id: str, *, padding: float = 4.0, header_height: float = 3.5) -> Cluster`
- `g.cluster_column(col: int, cluster_id: str, *, padding: float = 4.0, header_height: float = 3.5) -> Cluster`

```drawlib code=show align=center file=lib_graph_grid.png caption="Step 1: GridGraph.get_layout() -> Step 2: Matrix & Row Cluster Rendering"
from drawlib.canvas import save, setup
from drawlib.graph import GridGraph
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=90)

# Step 1: Solve 2x3 matrix and row cluster coordinates with GridGraph
g = GridGraph(columns=3, default_node_width=24.0, default_node_height=12.0)

g.cell("fe_web", row=0, col=0)
g.cell("fe_mob", row=0, col=1)
g.cell("fe_cli", row=0, col=2)

g.cell("svc_auth", row=1, col=0)
g.cell("svc_core", row=1, col=1)
g.cell("svc_pay", row=1, col=2)

g.cluster_row(0, "row_fe")
g.cluster_row(1, "row_be")

g.edge("fe_web", "svc_core")
g.edge("fe_mob", "svc_core")
g.edge("fe_cli", "svc_auth")
g.edge("svc_core", "svc_pay")

layout = g.get_layout(margin=12.0)

# Step 2: Render row clusters, channel-routed edges, and matrix cells
for cid, title in [("row_fe", "Client Interfaces"), ("row_be", "Backend Services")]:
    c = layout[cid]
    rectangle(c.xy, width=c.width, height=c.height, style=Styles.MutedDashed.patch(shape_r=2.0))
    text((c.left + 2.0, c.top - 2.2), title, style=Styles.DarkBold.patch(halign="left", text_size=9.5))

for edge in layout.edges:
    lines(edge.points, arrow_head="->", style=Styles.DarkBold)

cells = [
    ("fe_web", "Web UI", Styles.Neutral, Styles.Dark),
    ("fe_mob", "Mobile UI", Styles.Neutral, Styles.Dark),
    ("fe_cli", "CLI Tool", Styles.Neutral, Styles.Dark),
    ("svc_auth", "Auth API", Styles.SecondaryNeutral, Styles.DarkBold),
    ("svc_core", "Core API", Styles.PrimaryFlat, Styles.WhiteBold),
    ("svc_pay", "Billing API", Styles.SecondaryNeutral, Styles.DarkBold),
]
for nid, label, style, text_style in cells:
    n = layout[nid]
    rectangle(n.xy, width=n.width, height=n.height, style=style.patch(shape_r=1.5), text=label, text_style=text_style)

save()
```

---

## 4. Layout Models & Post-Calculation Adjustment (`GraphLayout`)

### 4.1. Coordinate Properties Reference (`NodeLayout`, `ClusterLayout`, `EdgeLayout`)

Calling `layout = g.get_layout()` returns a `GraphLayout` container with dictionary-style `layout["id"]` lookup across both nodes and clusters:

| Layout Model | Key Properties | Primary Rendering Usage |
| :--- | :--- | :--- |
| **`GraphLayout`** | `.nodes` (`dict[str, NodeLayout]`)<br>`.clusters` (`dict[str, ClusterLayout]`)<br>`.edges` (`list[EdgeLayout]`)<br>`.width`, `.height` (`float`)<br>`.ring_radii` (`dict[int, float]`)<br>`layout[key]`, `layout.offset(id, dx, dy)` | Access solved geometries by ID (`layout["api"]`), shift nodes/clusters with `.offset()`, or print human-readable coordinates via `print(layout)`. |
| **`NodeLayout`** | `.xy` / `.center` (`(cx, cy)`)<br>`.x`, `.y` (`float`)<br>`.bottom_left` (`(left, bottom)`)<br>`.local_xy` (center relative to parent cluster's `bottom_left`)<br>`.local_bottom_left`<br>`.width`, `.height`, `.size`<br>`.left`, `.right`, `.bottom`, `.top`<br>`.parent_id` (`str \| None`) | • Pass `.xy` to `d.add(Node(...), xy=nl.xy)`, `flow.add(..., xy=nl.xy)`, or `rectangle(nl.xy, width=nl.width, height=nl.height)`.<br>• Pass `.local_xy` to `group.add(Node(...), xy=nl.local_xy)` inside an `ArchitectureDiagram` `NodeGroup`. |
| **`ClusterLayout`** | `.bottom_left` (`(left, bottom)`)<br>`.local_bottom_left` (relative to parent cluster's `bottom_left`)<br>`.xy` / `.center` (`(cx, cy)`)<br>`.cx`, `.cy`, `.width`, `.height`, `.size`<br>`.left`, `.right`, `.bottom`, `.top`<br>`.parent_id` (`str \| None`) | • Pass `.bottom_left` to top-level `d.add(NodeGroup(...), xy=cl.bottom_left)`.<br>• Pass `.local_bottom_left` to nested `parent_grp.add(NodeGroup(...), xy=cl.local_bottom_left)`.<br>• Pass `.xy` to `rectangle(cl.xy, width=cl.width, height=cl.height)`. |
| **`EdgeLayout`** | `.src`, `.dst` (`str`)<br>`.src_port`, `.dst_port` (`(x, y)`)<br>`.waypoints` (`list[(x, y)]`)<br>`.points` (`[src_port, *waypoints, dst_port]`)<br>`.mid_xy` (`(mx, my)`) | • Pass `.points` to `lines(edge.points, arrow_head="->", style=...)`.<br>• Pass `.mid_xy` to `text(edge.mid_xy, "Label", ...)`. |

### 4.2. Inspecting (`print(layout)`) & Offsetting (`layout.offset()`)

You can print any `GraphLayout` to inspect all computed coordinates in a clean table:

```python
layout = g.get_layout(width=160, height=80, margin=10.0)
print(layout)
# Output:
# GraphLayout(width=160.0, height=80.0)
# Clusters:
#   ext : bottom_left=(17.0, 27.25), center=(33.0, 40.0), size=(32.0, 25.5)
#   vpc : bottom_left=(65.0, 20.5), center=(104.0, 40.0), size=(78.0, 39.0)
#   app : bottom_left=(70.0, 27.25), center=(104.0, 38.25), size=(68.0, 22.0), parent='vpc', local_bottom_left=(5.0, 6.75)
# Nodes:
#   client : xy=(33.0, 38.25), bottom_left=(21.0, 31.25), size=(24.0, 14.0), parent='ext', local_xy=(16.0, 11.0)
#   api    : xy=(86.0, 38.25), bottom_left=(74.0, 31.25), size=(24.0, 14.0), parent='app', local_xy=(16.0, 11.0)
```

Use `layout.offset(id, dx=..., dy=...)` to shift a specific node or an entire cluster (along with its enclosed child nodes and attached edge ports) before rendering:

```drawlib code=show align=center file=lib_graph_offset.png caption="Fine-Tuning Computed Layout with offset() and Custom Callout Overlay"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.lines import lines
from drawlib.shapes import bubblespeech, rectangle
from drawlib.styles import Styles

setup(width=150, height=75)

# Step 1: Calculate layout and nudge the middle node downward via .offset()
g = LayerGraph(direction="LR", default_node_width=28.0, default_node_height=12.0)
g.node("ingest")
g.node("process")
g.node("store")
g.edge("ingest", "process")
g.edge("process", "store")

layout = g.get_layout(margin=14.0).offset("process", dy=-6.0)

# Step 2: Render edges, nodes, and a custom callout anchored to layout["process"]
for edge in layout.edges:
    lines(edge.points, arrow_head="->", style=Styles.DarkBold)

specs = [
    ("ingest", "Ingest", Styles.Neutral, Styles.Dark),
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

---

## 5. Best Practices & Anti-Patterns

1. **Always Separate Layout Calculation (Step 1) from Visual Rendering (Step 2)**:
   - Never pass `style`, `text_style`, `label`, `shape`, or `show` to `g.node()`, `g.edge()`, or `g.cluster()`, and never call `g.draw()` or `g.export_code()`.
   - Use `layout = g.get_layout()` to solve coordinates, then render with `ArchitectureDiagram`, `FlowDiagram`, or `drawlib.shapes` / `drawlib.lines`.
2. **Match Node Dimensions Between Step 1 and Step 2**:
   - Pass the same `default_node_width` / `default_node_height` (or per-node `width` / `height` and cluster `padding`) to `g` in Step 1 that you pass to `Node(width=..., height=...)` or `rectangle(..., width=n.width, height=n.height)` in Step 2 so edge ports clip cleanly on card boundaries.
3. **Use `.local_xy` and `.local_bottom_left` with `ArchitectureDiagram` `NodeGroup`s**:
   - In `ArchitectureDiagram`, child items added via `group.add(...)` expect coordinates relative to the group's `bottom_left` origin. Always use `layout["child_node"].local_xy` and `layout["nested_cluster"].local_bottom_left`.
4. **Follow the 50%+ Neutral-Grounded Color Rule in Step 2**:
   - Ground **50% or more of rendered nodes in calm neutral or tinted-neutral cards** (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`). Reserve saturated `Styles.PrimaryFlat` (with `text_style=Styles.WhiteBold`) strictly for the 1–2 primary focal nodes.
