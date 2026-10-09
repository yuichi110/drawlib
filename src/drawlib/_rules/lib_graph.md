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
| **`GridGraph`** | 2D Matrix Assignment & Channel Edge Routing | Service catalogs, state matrices, periodic/tabular networks | `.cell()`, `.cluster_row()`, `.cluster_column()` |

---

## 2. Common Graph API (`BaseGraph`)

All five solvers inherit from `BaseGraph` and share a unified fluent builder interface.

### 2.1. Declaring Nodes, Edges, and Clusters

#### `g.node(...) -> Node`
Registers a node in the graph and returns a mutable `Node` declaration object (`node.show`, `node.style`, `node.text_style`, `node.label`).

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Unique identifier for the node. |
| `label` | `str \| None` | `None` | Display text inside the node (defaults to `id` when `None`). |
| `style` | `Style \| None` | `None` | Visual style for the node shape (defaults to solver's `default_node_style`, typically `Styles.PrimaryFlat`). |
| `text_style` | `Style \| None` | `None` | Optional explicit style override for the node label. |
| `shape` | `Literal["rectangle", "circle"]` | `"rectangle"` | Shape geometry (`"rectangle"`, `"circle"`; corner rounding controlled via `style.shape_r`). |
| `width` | `float \| None` | `None` | Explicit node width in canvas units (defaults to solver's `default_node_width`). |
| `height` | `float \| None` | `None` | Explicit node height in canvas units (defaults to solver's `default_node_height`). |
| `layer` | `int \| None` | `None` | Explicit rank/layer index for `LayerGraph` (`0` = first rank). |
| `ring` | `int \| None` | `None` | Explicit concentric ring index for `RadialGraph` (`0` = center hub). |
| `row`, `col` | `int \| None` | `None` | Explicit 0-based grid coordinates for `GridGraph`. |
| `group`, `subgroup` | `str \| None` | `None` | Optional container/group and nested subgroup IDs for `ArchitectureGraph`. |
| `show` | `bool` | `True` | Visibility flag. Hidden nodes (`show=False`) keep their layout slot during `calc()`, but are skipped during rendering along with any connected edges. |

*(Solver-specific convenience methods `.child(..., show=True)`, `.spoke(..., show=True)`, and `.cell(..., show=True)` also accept `show: bool = True`.)*

#### `g.edge(...) -> Edge`
Registers a directed or undirected connection between two nodes and returns a mutable `Edge` declaration object (`edge.show`, `edge.style`, `edge.text_style`, `edge.label`). If `src` or `dst` has not been declared via `.node()`, it is automatically created with default styling.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `src` | `str` | *(required)* | Source node ID. |
| `dst` | `str` | *(required)* | Destination node ID. |
| `label` | `str \| None` | `None` | Optional text label placed along the edge midpoint. |
| `style` | `Style \| None` | `None` | Line style (defaults to `Styles.DarkBold`). |
| `text_style` | `Style \| None` | `None` | Text style for edge label. |
| `arrow_head` | `Literal["->", "<-", "<->", "-"]` | `"->"` | Arrowhead direction (`"->"`, `"<-"`, `"<->"`, `"-"`). |
| `line_style` | `Literal["solid", "dashed", "dotted"] \| None` | `None` | Optional per-edge stroke style override. |
| `show` | `bool` | `True` | Visibility flag. Also automatically skipped during rendering if either endpoint node has `show=False`. |

#### `g.cluster(...) -> Cluster` and `g.group(...) -> Cluster`
Groups nodes inside a visual boundary container (such as a VPC, subnet, or stage box) and returns a mutable `Cluster` declaration object (`cluster.show`, `cluster.style`, `cluster.text_style`, `cluster.label`).

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Unique cluster identifier. |
| `nodes` | `list[str]` | *(required in `cluster`)* | List of node IDs contained in this cluster. |
| `label` | `str \| None` | `None` | Header title rendered at the top-left of the container box. |
| `style` | `Style \| None` | `None` | Container box style (defaults to `Styles.MutedDashed`). |
| `text_style` | `Style \| None` | `None` | Container title text style. |
| `padding` | `float` | `4.0` | Internal margin between the cluster border and enclosed nodes. |
| `parent` | `str \| None` | `None` | Parent cluster ID for nested containers (e.g., Subnet inside a VPC). |
| `order` | `int \| None` | `None` | Explicit sorting priority among sibling clusters (`ArchitectureGraph`). |
| `pos` | `Literal["top", "bottom", "left", "right", "center"] \| None` | `None` | Compass zone placement relative to the canvas (`ArchitectureGraph`). |
| `show` | `bool` | `True` | Visibility flag for the container box (`cluster_row(..., show=True)` and `cluster_column(..., show=True)` in `GridGraph` also accept `show`). |

### 2.2. Layout Calculation, Rendering, and Code Export

Every graph solver provides three terminal execution methods:

- **`g.calc(*, width=None, height=None, margin=10.0) -> GraphLayout`**:
  Computes all node positions, cluster bounds, and edge waypoints across the full topology (regardless of `show=False`), returning a `GraphLayout` object without drawing anything. If `setup()` was already called on `drawlib.canvas`, `width` and `height` automatically default to the active canvas dimensions.
- **`g.draw(xy=(0.0, 0.0), *, width=None, height=None, margin=10.0, scale: float = 1.0) -> GraphLayout`**:
  Computes the layout via `calc()`, renders all visible (`show=True`) clusters, edges, and nodes in proper z-order onto the active canvas (translated by `xy` and scaled by `scale`), and returns the `GraphLayout`.
- **`g.export_code(*, width=None, height=None, margin=10.0) -> str`**:
  Computes the layout and returns a complete, formatted Python script using `drawlib.shapes`, `drawlib.lines`, and `drawlib.text` with exact numeric coordinates.

---

## 3. Specialized Layout Solvers

### 3.1. `ArchitectureGraph` (Cloud & System Topologies)

`ArchitectureGraph` is purpose-built for cloud infrastructure and system architecture diagrams. It uses a **two-level hierarchical layout algorithm**:
1. **Micro Layout**: Packs nodes inside each leaf cluster (and recursively packs child clusters inside parent clusters).
2. **Macro Layout**: Arranges top-level clusters across a 5-zone compass (`pos="left" | "center" | "right" | "top" | "bottom"`) or along the primary flow axis (`direction="LR" | "TB"`), then routes orthogonal edges with evenly distributed port offsets.

```python
ArchitectureGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    container_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_style: Style | None = None,
    default_node_text_style: Style | None = None,
    default_edge_style: Style | None = None,
    default_edge_text_style: Style | None = None,
    default_container_style: Style | None = None,
    default_node_width: float = 24.0,
    default_node_height: float = 12.0,
)
```

```drawlib show-code center file:lib_graph_architecture.png caption:"ArchitectureGraph with Nested Clusters and Compass Zones"
from drawlib.canvas import save, setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=205, height=115)

g = ArchitectureGraph(direction="LR", default_node_width=28.0)

# External client zone on the left (calm Neutral card)
g.cluster("clients", ["client"], label="External", pos="left", padding=5.0)
g.node("client", "Client App", style=Styles.Neutral)

# Cloud VPC container with nested Compute & Data tiers in the center
g.group("vpc", "Production VPC", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], label="Compute Tier", parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db", "cache"], label="Data Tier", parent="vpc", order=2, padding=5.0)

# Hero focal node in PrimaryFlat; supporting nodes in calm Neutral / Tinted-Neutral cards
g.node("api", "API Gateway", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("worker", "Worker", style=Styles.PrimaryNeutral)
g.node("db", "Primary DB", style=Styles.SecondaryNeutral)
g.node("cache", "Redis Cache", style=Styles.SecondaryNeutral)

# Observability cluster at the bottom
g.cluster("obs", ["metrics"], label="Observability", pos="bottom", padding=5.0)
g.node("metrics", "Prometheus", style=Styles.Neutral)

g.edge("client", "api", "HTTPS")
g.edge("api", "worker", "Queue")
g.edge("api", "cache", "Read")
g.edge("worker", "db", "Write")
g.edge("worker", "metrics", style=Styles.MutedDashed)

g.draw(margin=10)
save()
```

### 3.2. `LayerGraph` (Hierarchical DAGs & Pipelines)

`LayerGraph` implements a **Sugiyama-style layered DAG algorithm** (cycle removal via DFS, longest-path rank assignment with explicit `layer` pinning, barycenter crossing minimization, and orthogonal or straight routing). Use `.tier(name, nodes, layer=...)` to pin multiple nodes to the same stage.

```python
LayerGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    rank_sep: float | None = None,
    node_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_style: Style | None = None,
    default_node_text_style: Style | None = None,
    default_edge_style: Style | None = None,
    default_edge_text_style: Style | None = None,
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
)
```

```drawlib show-code center file:lib_graph_layer.png caption:"LayerGraph Directed Acyclic Pipeline with Tiers"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.styles import Styles

setup(width=185, height=90)

g = LayerGraph(direction="LR", rank_sep=14.0, default_node_width=26.0)

g.node("git", "Git Push", style=Styles.Neutral)
g.node("lint", "Lint & Type", style=Styles.PrimaryNeutral)
g.node("unit", "Unit Tests", style=Styles.PrimaryNeutral)
g.node("build", "Build Image", style=Styles.SecondaryNeutral)
g.node("prod", "Production", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)

g.tier("ci", ["lint", "unit"], layer=1)
g.cluster("ci_box", ["lint", "unit"], label="CI Checks", padding=6.0)

g.edge("git", "lint")
g.edge("git", "unit")
g.edge("lint", "build")
g.edge("unit", "build")
g.edge("build", "prod", "Deploy")

g.draw(margin=12)
save()
```

### 3.3. `TreeGraph` (Hierarchies & Taxonomies)

`TreeGraph` computes proportional subtree widths (Reingold-Tilford / Buchheim contour algorithm) so sibling subtrees never overlap while keeping parents centered over their children. Use `.child(parent_id, child_id, label, ...)` for concise tree construction.

```python
TreeGraph(
    *,
    direction: Literal["TB", "LR"] = "TB",
    root: str | None = None,
    level_sep: float | None = None,
    sibling_sep: float | None = None,
    subtree_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_style: Style | None = None,
    default_node_text_style: Style | None = None,
    default_edge_style: Style | None = None,
    default_edge_text_style: Style | None = None,
    default_node_width: float = 20.0,
    default_node_height: float = 10.0,
)
```

```drawlib show-code center file:lib_graph_tree.png caption:"TreeGraph Hierarchy with Orthogonal Routing"
from drawlib.canvas import save, setup
from drawlib.graph import TreeGraph
from drawlib.styles import Styles

setup(width=160, height=85)

g = TreeGraph(root="vp", direction="TB", default_node_width=28.0)
g.node("vp", "VP Engineering", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)

g.child("vp", "plat", "Platform Team", style=Styles.PrimaryNeutral)
g.child("vp", "prod", "Product Team", style=Styles.SecondaryNeutral)

g.child("plat", "infra", "Cloud Infra", style=Styles.Neutral)
g.child("plat", "sec", "Security", style=Styles.Neutral)
g.child("prod", "web", "Web Frontend", style=Styles.Neutral)
g.child("prod", "mob", "Mobile Apps", style=Styles.Neutral)

g.draw(margin=12)
save()
```

### 3.4. `RadialGraph` (Hub-and-Spoke & Concentric Rings)

`RadialGraph` places a central hub at `ring=0` and arranges connected nodes on concentric circles (`ring=1, 2, ...`), allocating angular sectors proportionally to subtree leaf counts to avoid edge crossings. Setting `draw_ring_guides=True` draws subtle dashed guide circles for each ring.

```python
RadialGraph(
    *,
    hub: str | None = None,
    center: tuple[float, float] | None = None,
    radius_step: float | None = None,
    start_angle: float = 0.0,
    angle_range: float = 360.0,
    draw_ring_guides: bool = False,
    ring_guide_style: Style | None = None,
    default_node_style: Style | None = None,
    default_node_text_style: Style | None = None,
    default_edge_style: Style | None = None,
    default_edge_text_style: Style | None = None,
    default_node_width: float = 18.0,
    default_node_height: float = 10.0,
)
```

```drawlib show-code center file:lib_graph_radial.png caption:"RadialGraph Hub-and-Spoke Topology with Ring Guides"
from drawlib.canvas import save, setup
from drawlib.graph import RadialGraph
from drawlib.styles import Styles

setup(width=170, height=130)

g = RadialGraph(hub="core", draw_ring_guides=True, default_node_width=24.0)
g.node("core", "Event Mesh", shape="circle", width=24.0, height=24.0, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)

g.spoke("core", "auth", "Auth API", style=Styles.PrimaryNeutral)
g.spoke("core", "billing", "Billing", style=Styles.PrimaryNeutral)
g.spoke("core", "orders", "Orders", style=Styles.SecondaryNeutral)
g.spoke("core", "notify", "Notify", style=Styles.PrimaryNeutral)

g.spoke("orders", "inv", "Inventory", ring=2, style=Styles.Neutral)
g.spoke("orders", "ship", "Shipping", ring=2, style=Styles.Neutral)

g.draw(margin=18)
save()
```

### 3.5. `GridGraph` (Matrix Layouts & Service Catalogs)

`GridGraph` places nodes into a structured 2D matrix `(row, col)`. Nodes without explicit `(row, col)` coordinates are automatically assigned to the next open cell in `"row-major"` or `"column-major"` order. Non-adjacent edges are routed cleanly through inter-row and inter-column channels when `edge_routing="smart"`.

```python
GridGraph(
    *,
    columns: int = 3,
    rows: int | None = None,
    order: Literal["row-major", "column-major"] = "row-major",
    col_sep: float | None = None,
    row_sep: float | None = None,
    edge_routing: Literal["smart", "orthogonal", "straight"] = "smart",
    default_node_style: Style | None = None,
    default_node_text_style: Style | None = None,
    default_edge_style: Style | None = None,
    default_edge_text_style: Style | None = None,
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
)
```

```drawlib show-code center file:lib_graph_grid.png caption:"GridGraph Matrix with Row Clusters and Smart Channel Routing"
from drawlib.canvas import save, setup
from drawlib.graph import GridGraph
from drawlib.styles import Styles

setup(width=150, height=90)

g = GridGraph(columns=3)

g.cell("fe_web", row=0, col=0, label="Web UI", style=Styles.Neutral)
g.cell("fe_mob", row=0, col=1, label="Mobile UI", style=Styles.Neutral)
g.cell("fe_cli", row=0, col=2, label="CLI Tool", style=Styles.Neutral)

g.cell("svc_auth", row=1, col=0, label="Auth API", style=Styles.SecondaryNeutral)
g.cell("svc_core", row=1, col=1, label="Core API", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.cell("svc_pay", row=1, col=2, label="Billing API", style=Styles.SecondaryNeutral)

g.cluster_row(0, "row_fe", label="Client Interfaces")
g.cluster_row(1, "row_be", label="Backend Services")

g.edge("fe_web", "svc_core")
g.edge("fe_mob", "svc_core")
g.edge("fe_cli", "svc_auth")
g.edge("svc_core", "svc_pay")

g.draw(margin=12)
save()
```

---

## 4. Layout Models & Post-Calculation Adjustment (`GraphLayout`)

Calling `layout = g.calc()` returns a mutable `GraphLayout` container holding computed geometries:
- `layout.nodes`: `dict[str, NodeLayout]` — each `NodeLayout` has `.id`, `.x`, `.y`, `.width`, `.height`, `.label`, `.shape`, `.style`, `.text_style`, `.show`.
- `layout.edges`: `list[EdgeLayout]` — each `EdgeLayout` has `.src`, `.dst`, `.points` (`list[tuple[float, float]]`), `.label`, `.style`, `.text_style`, `.arrow_head`, `.line_style`, `.show`.
- `layout.clusters`: `dict[str, ClusterLayout]` — each `ClusterLayout` has `.id`, `.cx`, `.cy`, `.width`, `.height`, `.label`, `.style`, `.text_style`, `.show`.
- `layout.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`: Renders the computed layout onto the active canvas, translating by `xy`, scaling by `scale`, and skipping any elements where `.show=False` (including edges connected to hidden endpoint nodes).

### 4.1. Inspecting & Offsetting Coordinates (`calc()` + `offset()`)

Use `layout.offset(id, dx=..., dy=...)` to shift a node or an entire cluster (along with its enclosed nodes and attached edge endpoints) before calling `layout.draw()`. You can also read `layout.nodes[id].x` and `.y` to attach custom callouts or primitives, or mutate `layout.nodes[id].show` / `.style` across frames without re-running the layout solver.

```drawlib show-code center file:lib_graph_offset.png caption:"Fine-Tuning Computed Layout with offset() and Custom Annotations"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.shapes import bubblespeech
from drawlib.styles import Styles

setup(width=150, height=75)

g = LayerGraph(direction="LR", default_node_width=26.0)
g.node("ingest", "Ingest", style=Styles.Neutral)
g.node("process", "Stream Engine", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("store", "Data Lake", style=Styles.SecondaryNeutral)

g.edge("ingest", "process")
g.edge("process", "store")

# 1. Calculate layout without drawing
layout = g.calc(margin=14)

# 2. Nudge the middle node downward and render
layout.offset("process", dy=-6.0)
layout.draw()

# 3. Use computed node coordinates for custom primitive overlay
proc = layout.nodes["process"]
bubblespeech(
    (proc.x - 18, proc.y + 14),
    width=36,
    height=12,
    tail_edge="bottom",
    tail_start_ratio=0.4,
    tail_end_ratio=0.6,
    tail_vertex_xy=(proc.x, proc.y + proc.height / 2 + 1),
    style=Styles.WarningNeutral,
    text="Auto-scaled x8",
)

save()
```

### 4.2. Exporting Editable Primitive Code (`export_code()` / `to_code()`)

When you want to use `drawlib.graph` as an initial layout generator and then take full manual ownership of every shape and line in your script:

```python
code_str = g.export_code(width=160, height=90)
print(code_str)
```

This outputs clean, human-readable Python code (`setup(...)`, `rectangle(...)`, `circle(...)`, `line(...)`, `save()`) with every computed coordinate rounded to `.1f`.

---

## 5. Best Practices & Anti-Patterns

1. **Follow the 50%+ Neutral-Grounded Color Rule**:
   - Avoid "Rainbow Color Chaos" (giving every node a saturated fill like `PrimaryFlat`, `AccentFlat`, `SuccessFlat`, `WarningFlat`).
   - Ground **50% or more of nodes in calm neutral or tinted-neutral cards** (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`). Reserve saturated `Styles.PrimaryFlat` (with `text_style=Styles.WhiteBold`) strictly for the 1–2 primary focal nodes in the graph.
2. **Choose the Right Solver for the Topology**:
   - Use `ArchitectureGraph` when you have nested containers (`parent=...`) or multi-zone boundaries (`pos="left"|"center"|"right"|"bottom"`).
   - Use `LayerGraph` for left-to-right or top-to-bottom directed pipelines where rank alignment matters.
   - Use `TreeGraph` for strict parent-child hierarchies so subtrees are balanced symmetrically.
3. **Keep Cluster Styles Subtle**:
   - Rely on the default `Styles.MutedDashed` container style on `g.cluster()` / `g.group()` so foreground nodes stand out with high contrast.
4. **Size `default_node_width` for Long Labels**:
   - When nodes have longer titles (e.g. `"VP Engineering"`), pass `default_node_width=28.0` to the solver or `width=28.0` to `g.node()` so labels have generous horizontal padding.

