# Drawlib Graph Guidelines

This document provides the complete technical specification, solver catalog, and programmatic usage patterns for `drawlib.graph`.

---

## Table of Contents

- [1. Module Overview & Architecture](#1-module-overview--architecture)
  - [1.1. Public Exports](#11-public-exports)
  - [1.2. Core Philosophy: Auto-Layout + Fine-Tuning](#12-core-philosophy-auto-layout--fine-tuning)
  - [1.3. Solver Selection Matrix](#13-solver-selection-matrix)
- [2. Common Graph API (`BaseGraph`)](#2-common-graph-api-basegraph)
  - [2.1. Declaring Nodes, Edges, and Clusters](#21-declaring-nodes-edges-and-clusters)
  - [2.2. Layout Calculation, Rendering, and Code Export](#22-layout-calculation-rendering-and-code-export)
  - [2.3. Supported Node Shapes & Icons](#23-supported-node-shapes--icons)
- [3. Specialized Layout Solvers](#3-specialized-layout-solvers)
  - [3.1. `ArchitectureGraph` (Cloud & System Topologies)](#31-architecturegraph-cloud--system-topologies)
  - [3.2. `LayerGraph` (Hierarchical DAGs & Pipelines)](#32-layergraph-hierarchical-dags--pipelines)
  - [3.3. `TreeGraph` (Hierarchies & Taxonomies)](#33-treegraph-hierarchies--taxonomies)
  - [3.4. `RadialGraph` (Hub-and-Spoke & Concentric Rings)](#34-radialgraph-hub-and-spoke--concentric-rings)
  - [3.5. `GridGraph` (Matrix Layouts & Service Catalogs)](#35-gridgraph-matrix-layouts--service-catalogs)
- [4. Layout Models & Post-Calculation Adjustment (`GraphLayout`)](#4-layout-models--post-calculation-adjustment-graphlayout)
  - [4.1. Inspecting & Offsetting Coordinates (`calc()` + `offset()`)](#41-inspecting--offsetting-coordinates-calc--offset)
  - [4.2. Exporting Editable Primitive Code (`export_code()` / `to_code()`)](#42-exporting-editable-primitive-code-export_code--to_code)
- [5. Best Practices & Anti-Patterns](#5-best-practices--anti-patterns)

---

## 1. Module Overview & Architecture

The `drawlib.graph` module provides a declarative **graph layout engine** that automatically computes node coordinates, container bounding boxes, and orthogonal or straight edge routes from topological relationships (nodes, edges, and clusters).

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

### 1.2. Core Philosophy: Auto-Layout + Fine-Tuning

Writing complex diagrams by manually calculating every `(x, y)` coordinate can be tedious when topologies change. Conversely, black-box auto-layout tools (like Graphviz/Mermaid) make it nearly impossible to tweak a single awkward node or edge.

`drawlib.graph` bridges both worlds through three progressive workflows:
1. **Direct Declarative Rendering (`g.draw()`)**: Declare nodes, clusters, and edges, and let the solver compute coordinates and draw directly onto the canvas.
2. **Calculate, Tweak, and Draw (`layout = g.calc()` -> `layout.offset(...)` -> `layout.draw()`)**: Compute the layout first, inspect or shift specific nodes/clusters, and even mix custom `drawlib.shapes` or annotations using exact computed coordinates (`layout.nodes["db"].x`).
3. **Scaffold to Standalone Primitives (`g.export_code()`)**: Generate clean, self-contained Python source code using standard `drawlib.shapes` and `drawlib.lines` with all computed coordinates baked in for 100% manual control.

### 1.3. Solver Selection Matrix

| Solver Class | Algorithm / Strategy | Best Used For | Key Helper Methods |
| :--- | :--- | :--- | :--- |
| **`ArchitectureGraph`** | 2-Level Macro/Micro Container + Compass Packing | Cloud architectures, VPCs/subnets, multi-zone microservices | `.group()`, `.cluster(parent=..., pos=...)` |
| **`LayerGraph`** | Sugiyama Hierarchical DAG (Cycle removal, Barycenter ordering) | CI/CD pipelines, dataflows, layered dependency graphs | `.tier(name, nodes, layer=...)` |
| **`TreeGraph`** | Reingold-Tilford / Buchheim Compact Tree | Org charts, ASTs, decision trees, taxonomies | `.child(parent, child_id, ...)` |
| **`RadialGraph`** | Concentric BFS Rings & Angular Sector Allocation | Hub-and-spoke networks, ecosystem maps, dependency rings | `.spoke(parent, spoke_id, ring=...)` |
| **`GridGraph`** | 2D Matrix Assignment & Channel Edge Routing | Service catalogs, state matrices, periodic/tabular networks | `.cell()`, `.cluster_row()`, `.cluster_col()` |

---

## 2. Common Graph API (`BaseGraph`)

All five solvers inherit from `BaseGraph` and share a unified fluent builder interface.

### 2.1. Declaring Nodes, Edges, and Clusters

#### `g.node(...) -> Self`
Registers or updates a node in the graph.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Unique identifier for the node. |
| `label` | `str \| None` | `None` | Display text inside the node (defaults to `id` when `None`). |
| `style` | `Style \| str \| None` | `None` | Visual style for the node shape (defaults to solver's `default_node_style`, typically `Styles.Primary`). |
| `text_style` | `Style \| str \| None` | `None` | Optional explicit style override for the node label. |
| `shape` | `str` | `"rectangle"` | Shape primitive name (`"rectangle"`, `"circle"`, `"cylinder"`, `"diamond"`, `"hexagon"`, `"ellipse"`, `"trapezoid"`, `"parallelogram"`). |
| `icon` | `str \| Dimage \| None` | `None` | Optional Phosphor icon name (e.g., `"database"`, `"cloud"`, `"cpu"`, `"globe"`) or `Dimage` instance rendered above the label. |
| `width` | `float \| None` | `None` | Explicit node width in canvas units (auto-sized from label length if `None`). |
| `height` | `float \| None` | `None` | Explicit node height in canvas units (auto-sized from label line count and icon if `None`). |
| `layer` | `int \| None` | `None` | Explicit rank/layer index for `LayerGraph` (`0` = first rank). |
| `ring` | `int \| None` | `None` | Explicit concentric ring index for `RadialGraph` (`0` = center hub). |
| `row`, `col` | `int \| None` | `None` | Explicit 0-based grid coordinates for `GridGraph`. |
| `group`, `subgroup` | `str \| None` | `None` | Optional logical grouping tags. |

#### `g.edge(...) -> Self`
Registers a directed or undirected connection between two nodes. If `src` or `dst` has not been declared via `.node()`, it is automatically created with default styling.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `src` | `str` | *(required)* | Source node ID. |
| `dst` | `str` | *(required)* | Destination node ID. |
| `label` | `str \| None` | `None` | Optional text label placed along the edge midpoint. |
| `style` | `Style \| str \| None` | `None` | Line style (defaults to `Styles.DarkBold`). |
| `text_style` | `Style \| str \| None` | `None` | Text style for edge label (defaults to `Styles.Dark`). |
| `arrow_head` | `TypeArrowHead` | `"->"` | Arrowhead direction (`"->"`, `"<-"`, `"<->"`, `"-"`). |
| `line_style` | `Literal["straight", "curved", " elbow"] \| None` | `None` | Optional per-edge routing override. |

#### `g.cluster(...) -> Self` and `g.group(...) -> Self`
Groups nodes inside a visual boundary container (such as a VPC, subnet, or stage box).

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Unique cluster identifier. |
| `nodes` | `Sequence[str]` | *(required in `cluster`)* | List of node IDs contained in this cluster. |
| `label` | `str \| None` | `None` | Header title rendered at the top-left of the container box. |
| `style` | `Style \| str \| None` | `None` | Container box style (defaults to `Styles.SecondaryLight`). |
| `text_style` | `Style \| str \| None` | `None` | Container title text style (defaults to `Styles.SecondaryBold`). |
| `padding` | `float` | `4.0` | Internal margin between the cluster border and enclosed nodes. |
| `parent` | `str \| None` | `None` | Parent cluster ID for nested containers (e.g., Subnet inside a VPC). |
| `order` | `int \| None` | `None` | Explicit sorting priority among sibling clusters (`ArchitectureGraph`). |
| `pos` | `Literal["left", "right", "top", "bottom", "center"] \| None` | `None` | Compass zone placement relative to the canvas or parent cluster (`ArchitectureGraph`). |

### 2.2. Layout Calculation, Rendering, and Code Export

Every graph solver provides three terminal execution methods:

- **`g.calc(width=None, height=None, *, margin=10.0) -> GraphLayout`**:
  Computes all node positions, cluster bounds, and edge waypoints, returning a `GraphLayout` object without drawing anything. If `setup()` was already called on `drawlib.canvas`, `width` and `height` automatically default to the active canvas dimensions; otherwise they default to `160 x 100`.
- **`g.draw(width=None, height=None, *, margin=10.0) -> GraphLayout`**:
  Computes the layout via `calc()`, automatically initializes the canvas (`setup()`) if not yet active, renders all clusters, edges, and nodes in proper z-order, and returns the `GraphLayout`.
- **`g.export_code(width=None, height=None, *, margin=10.0) -> str`**:
  Computes the layout and returns a complete, formatted Python script using `drawlib.shapes`, `drawlib.lines`, and `drawlib.text` with exact numeric coordinates.

### 2.3. Supported Node Shapes & Icons

Nodes support built-in shape dispatch (`shape=...`) and Phosphor icon integration (`icon=...`):
- **Shapes**: `"rectangle"` (default rounded box), `"cylinder"` (database/storage cylinder), `"diamond"` (decision gate), `"hexagon"` (microservice/worker), `"circle"`, `"ellipse"`, `"trapezoid"`, `"parallelogram"`.
- **Icons**: Pass any common Phosphor icon name as a string (such as `"database"`, `"cloud"`, `"server"`, `"cpu"`, `"globe"`, `"lock"`, `" shield"`, `"user"`, `"users"`, `"gear"`, `" HardDrive"`, `"chart_bar"`, `"warning"`, `"check_circle"`) or any `Dimage` returned by `drawlib.icons.phosphor.*`.

---

## 3. Specialized Layout Solvers

### 3.1. `ArchitectureGraph` (Cloud & System Topologies)

`ArchitectureGraph` is purpose-built for cloud infrastructure and system architecture diagrams. It uses a **two-level hierarchical layout algorithm**:
1. **Micro Layout**: Packs nodes inside each leaf cluster (and recursively packs child clusters inside parent clusters).
2. **Macro Layout**: Arranges top-level clusters and standalone nodes across a 5-zone compass (`pos="left" | "center" | "right" | "top" | "bottom"`) or along the primary flow axis (`direction="LR" | "TB"`), then routes orthogonal edges with evenly distributed port offsets.

```python
ArchitectureGraph(
    direction: Literal["LR", "TB"] = "LR",
    *,
    container_sep: float | None = None,
    node_sep: float | None = None,
    rank_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_style: Style | str | None = None,
    default_edge_style: Style | str | None = None,
    default_cluster_style: Style | str | None = None,
)
```

```drawlib show-code 750px center file:lib_graph_architecture.png caption:"ArchitectureGraph with Nested Clusters and Compass Zones"
from drawlib.canvas import save, setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=160, height=95)

g = ArchitectureGraph(direction="LR")

# External client on the left
g.node("client", "Client App", icon="globe", style=Styles.AccentFlat, text_style=Styles.WhiteBold)

# Cloud VPC container with nested App & Data tiers
g.group("vpc", "Production VPC", style=Styles.MutedLight, text_style=Styles.DarkBold, pos="center")
g.cluster("app_tier", ["api", "worker"], label="Compute Tier", parent="vpc", order=1, style=Styles.PrimaryLight)
g.cluster("data_tier", ["db", "cache"], label="Data Tier", parent="vpc", order=2, style=Styles.SecondaryLight)

g.node("api", "API Gateway", icon="cloud", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("worker", "Async Worker", shape="hexagon", style=Styles.Primary)
g.node("db", "Primary DB", shape="cylinder", style=Styles.SecondaryFlat, text_style=Styles.WhiteBold)
g.node("cache", "Redis Cache", shape="cylinder", style=Styles.Secondary)

# External observability at the bottom
g.cluster("obs", ["metrics"], label="Observability", pos="bottom", style=Styles.SuccessLight)
g.node("metrics", "Prometheus", icon="chart_bar", style=Styles.Success)

g.edge("client", "api", "HTTPS")
g.edge("api", "worker", "Queue")
g.edge("api", "cache", "Read")
g.edge("worker", "db", "Write")
g.edge("api", "metrics", style=Styles.MutedDashed)

g.draw(margin=8)
save()
```

### 3.2. `LayerGraph` (Hierarchical DAGs & Pipelines)

`LayerGraph` implements a **Sugiyama-style layered DAG algorithm** (cycle removal via DFS, longest-path rank assignment with explicit `layer` pinning, barycenter crossing minimization, and orthogonal or straight routing). Use `.tier(name, nodes, layer=...)` to pin multiple nodes to the same stage and automatically wrap them in a labeled stage container.

```python
LayerGraph(
    direction: Literal["LR", "TB"] = "LR",
    *,
    rank_sep: float | None = None,
    node_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_style: Style | str | None = None,
    default_edge_style: Style | str | None = None,
    default_cluster_style: Style | str | None = None,
)
```

```drawlib show-code 750px center file:lib_graph_layer.png caption:"LayerGraph Directed Acyclic Pipeline with Tiers"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.styles import Styles

setup(width=160, height=85)

g = LayerGraph(direction="LR")

g.node("git", "Git Push", style=Styles.AccentFlat, text_style=Styles.WhiteBold)
g.node("lint", "Lint & Type", style=Styles.Primary)
g.node("unit", "Unit Tests", style=Styles.Primary)
g.node("build", "Build Image", style=Styles.SecondaryFlat, text_style=Styles.WhiteBold)
g.node("staging", "Staging Env", style=Styles.Success)
g.node("prod", "Production", style=Styles.SuccessFlat, text_style=Styles.WhiteBold)

g.tier("ci", ["lint", "unit"], layer=1)
g.cluster("cd", ["staging", "prod"], label="Deployment", style=Styles.SuccessLight)

g.edge("git", "lint")
g.edge("git", "unit")
g.edge("lint", "build")
g.edge("unit", "build")
g.edge("build", "staging")
g.edge("staging", "prod", "Approve")

g.draw(margin=10)
save()
```

### 3.3. `TreeGraph` (Hierarchies & Taxonomies)

`TreeGraph` computes proportional subtree widths (Reingold-Tilford / Buchheim contour algorithm) so sibling subtrees never overlap while keeping parents centered over their children. Use `.child(parent_id, child_id, label, ...)` for concise tree construction.

```python
TreeGraph(
    root: str | None = None,
    direction: Literal["TB", "LR"] = "TB",
    *,
    level_sep: float | None = None,
    sibling_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_style: Style | str | None = None,
    default_edge_style: Style | str | None = None,
    default_cluster_style: Style | str | None = None,
)
```

```drawlib show-code 700px center file:lib_graph_tree.png caption:"TreeGraph Hierarchy with Orthogonal Routing"
from drawlib.canvas import save, setup
from drawlib.graph import TreeGraph
from drawlib.styles import Styles

setup(width=150, height=80)

g = TreeGraph(root="vp", direction="TB")
g.node("vp", "VP of Engineering", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)

g.child("vp", "plat", "Platform Team", style=Styles.SecondaryFlat, text_style=Styles.WhiteBold)
g.child("vp", "prod", "Product Team", style=Styles.AccentFlat, text_style=Styles.WhiteBold)

g.child("plat", "infra", "Cloud Infra", style=Styles.Secondary)
g.child("plat", "sec", "Security", style=Styles.Secondary)
g.child("prod", "web", "Web Frontend", style=Styles.Accent)
g.child("prod", "mob", "Mobile Apps", style=Styles.Accent)

g.draw(margin=10)
save()
```

### 3.4. `RadialGraph` (Hub-and-Spoke & Concentric Rings)

`RadialGraph` places a central hub at `ring=0` and arranges connected nodes on concentric circles (`ring=1, 2, ...`), allocating angular sectors proportionally to subtree leaf counts to avoid edge crossings. Setting `draw_ring_guides=True` draws subtle dashed guide circles for each ring.

```python
RadialGraph(
    hub: str | None = None,
    *,
    center: tuple[float, float] | None = None,
    radius_step: float | None = None,
    start_angle: float = 0.0,
    angle_range: float = 360.0,
    draw_ring_guides: bool = False,
    ring_guide_style: Style | str | None = None,
    default_node_style: Style | str | None = None,
    default_edge_style: Style | str | None = None,
    default_cluster_style: Style | str | None = None,
)
```

```drawlib show-code 650px center file:lib_graph_radial.png caption:"RadialGraph Hub-and-Spoke Topology with Ring Guides"
from drawlib.canvas import save, setup
from drawlib.graph import RadialGraph
from drawlib.styles import Styles

setup(width=140, height=110)

g = RadialGraph(hub="core", draw_ring_guides=True)
g.node("core", "Event Mesh", shape="circle", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)

g.spoke("core", "auth", "Auth Service", style=Styles.Secondary)
g.spoke("core", "billing", "Billing", style=Styles.Secondary)
g.spoke("core", "orders", "Order Engine", style=Styles.Accent)
g.spoke("core", "notify", "Notification", style=Styles.Success)

g.spoke("orders", "inv", "Inventory DB", ring=2, shape="cylinder", style=Styles.Warning)
g.spoke("orders", "ship", "Shipping API", ring=2, style=Styles.Warning)

g.draw(margin=12)
save()
```

### 3.5. `GridGraph` (Matrix Layouts & Service Catalogs)

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
    default_node_style: Style | str | None = None,
    default_edge_style: Style | str | None = None,
    default_cluster_style: Style | str | None = None,
)
```

```drawlib show-code 700px center file:lib_graph_grid.png caption:"GridGraph Matrix with Row Clusters and Smart Channel Routing"
from drawlib.canvas import save, setup
from drawlib.graph import GridGraph
from drawlib.styles import Styles

setup(width=150, height=90)

g = GridGraph(columns=3)

g.cell("fe_web", row=0, col=0, label="Web UI", style=Styles.Primary)
g.cell("fe_mob", row=0, col=1, label="Mobile UI", style=Styles.Primary)
g.cell("fe_cli", row=0, col=2, label="CLI Tool", style=Styles.Primary)

g.cell("svc_auth", row=1, col=0, label="Auth API", style=Styles.Secondary)
g.cell("svc_core", row=1, col=1, label="Core API", style=Styles.SecondaryFlat, text_style=Styles.WhiteBold)
g.cell("svc_pay", row=1, col=2, label="Billing API", style=Styles.Secondary)

g.cluster_row(0, "row_fe", label="Client Interfaces", style=Styles.PrimaryLight)
g.cluster_row(1, "row_be", label="Backend Services", style=Styles.SecondaryLight)

g.edge("fe_web", "svc_core")
g.edge("fe_mob", "svc_core")
g.edge("fe_cli", "svc_auth")
g.edge("svc_core", "svc_pay")

g.draw(margin=10)
save()
```

---

## 4. Layout Models & Post-Calculation Adjustment (`GraphLayout`)

Calling `layout = g.calc()` returns a mutable `GraphLayout` container holding computed geometries:
- `layout.nodes`: `dict[str, NodeLayout]` — each `NodeLayout` has `.id`, `.x`, `.y`, `.width`, `.height`, `.label`, `.shape`, `.icon`, `.style`, `.text_style`.
- `layout.edges`: `list[EdgeLayout]` — each `EdgeLayout` has `.src`, `.dst`, `.points` (`list[tuple[float, float]]`), `.label`, `.style`, `.text_style`, `.arrow_head`, `.line_style`.
- `layout.clusters`: `dict[str, ClusterLayout]` — each `ClusterLayout` has `.id`, `.x`, `.y`, `.width`, `.height`, `.label`, `.style`, `.text_style`.

### 4.1. Inspecting & Offsetting Coordinates (`calc()` + `offset()`)

Use `layout.offset(id, dx=..., dy=...)` to shift a node or an entire cluster (along with its enclosed nodes and attached edge endpoints) before calling `layout.draw()`. You can also read `layout.nodes[id].x` and `.y` to attach custom callouts or primitives.

```drawlib show-code 700px center file:lib_graph_offset.png caption:"Fine-Tuning Computed Layout with offset() and Custom Annotations"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.shapes import bubblespeech
from drawlib.styles import Styles

setup(width=150, height=70)

g = LayerGraph(direction="LR")
g.node("ingest", "Ingest", style=Styles.Primary)
g.node("process", "Stream Engine", style=Styles.AccentFlat, text_style=Styles.WhiteBold)
g.node("store", "Data Lake", shape="cylinder", style=Styles.Secondary)

g.edge("ingest", "process")
g.edge("process", "store")

# 1. Calculate layout without drawing
layout = g.calc(margin=12)

# 2. Nudge the middle node downward and render
layout.offset("process", dy=-6.0)
layout.draw()

# 3. Use computed node coordinates for custom primitive overlay
proc = layout.nodes["process"]
bubblespeech(
    (proc.x, proc.y + 18),
    width=36,
    height=11,
    tail_edge="bottom",
    tail_start_ratio=0.4,
    tail_end_ratio=0.6,
    tail_vertex_xy=(proc.x, proc.y + proc.height / 2 + 1),
    style=Styles.WarningLight,
    text="Auto-scaled x8",
    text_style=Styles.WarningBold,
)

save()
```

### 4.2. Exporting Editable Primitive Code (`export_code()` / `to_code()`)

When you want to use `drawlib.graph` as an initial layout generator and then take full manual ownership of every shape and line in your script:

```python
code_str = g.export_code(width=160, height=90)
print(code_str)
```

This outputs clean, human-readable Python code (`setup(...)`, `rectangle(...)`, `cylinder(...)`, `line(...)`, `save()`) with every computed coordinate rounded to `.1f`.

---

## 5. Best Practices & Anti-Patterns

1. **Choose the Right Solver for the Topology**:
   - Use `ArchitectureGraph` when you have nested containers (`parent=...`) or multi-zone boundaries (`pos="left"|"center"|"right"|"bottom"`).
   - Use `LayerGraph` for left-to-right or top-to-bottom directed pipelines where rank alignment matters.
   - Use `TreeGraph` for strict parent-child hierarchies so subtrees are balanced symmetrically.
2. **Use `shape="cylinder"` for Databases & Storage**:
   - Instead of generic rectangles for every node, set `shape="cylinder"` on databases/queues and `shape="diamond"` on decision nodes to improve visual scannability.
3. **Avoid Overcrowding Single Clusters**:
   - Keep leaf clusters focused (2–6 nodes per cluster) and group related sub-clusters inside a parent cluster (`parent="vpc"`) for clean hierarchical spacing.
