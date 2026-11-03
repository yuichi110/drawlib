# drawlib.graph

`drawlib.graph` provides five declarative graph layout solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`) that compute overlap-free node coordinates, nested container bounding boxes, and orthogonal or straight edge paths via `get_layout()`. Pair the returned `GraphLayout` geometry with `drawlib.diagrams` or `drawlib.shapes` and `drawlib.lines` in a clean two-step layout-and-render workflow.

```drawlib align=center code=fold file=25_graph_hero.png caption="Two-Step Graph Layout Workflow: LayerGraph.get_layout() Solving Node, Cluster, and Edge Coordinates"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.icons import phosphor
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.smartarts import BoxList
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=132, height=74)

rectangle(
    (66, 37),
    width=122,
    height=64,
    style=Styles.Neutral.patch(shape_fill_color=Colors.Transparent, line_style="dashed", shape_r=2.5),
)
text(
    (66, 64.5),
    "Step 1: layout = g.get_layout()   ->   Step 2: Render ClusterLayout, EdgeLayout & NodeLayout",
    style=Styles.DarkBold.patch(text_size=11.5),
)

g = LayerGraph(direction="LR", rank_sep=15.0, node_sep=5.0, default_node_width=26.0, default_node_height=10.5)
g.node("ingest")
g.node("validate")
g.node("enrich")
g.node("warehouse")
g.tier("stage", ["validate", "enrich"], layer=1)
g.cluster("etl_cluster", ["validate", "enrich"], padding=3.0, header_height=4.0)
g.edge("ingest", "validate")
g.edge("ingest", "enrich")
g.edge("validate", "warehouse")
g.edge("enrich", "warehouse")

raw = g.get_layout(width=116, height=38, margin=2.0)
cl = raw.clusters["etl_cluster"]
dy = 38.0 - cl.cy

rectangle(
    (cl.cx + 8.0, cl.cy + dy),
    width=cl.width,
    height=cl.height,
    style=Styles.PrimaryNeutral.patch(line_style="dashed", shape_r=2.0),
)
text(
    (cl.cx + 8.0, cl.top + dy - 2.3),
    "ClusterLayout ('etl_cluster')",
    style=Styles.PrimaryBold.patch(text_size=10.0),
)

for edge in raw.edges:
    pts = [(px + 8.0, py + dy) for px, py in edge.points]
    lines(pts, arrow_head="->", style=Styles.DarkBold)

node_specs = [
    ("ingest", "Ingest API", Styles.Neutral, Styles.DarkBold, Styles.PrimaryBold, phosphor.globe),
    ("validate", "Validate", Styles.Neutral, Styles.DarkBold, Styles.PrimaryBold, phosphor.check_circle),
    ("enrich", "DAG Solver", Styles.PrimaryFlat, Styles.WhiteBold, Styles.WhiteBold, phosphor.git_branch),
    ("warehouse", "Analytics DB", Styles.SecondaryNeutral, Styles.DarkBold, Styles.SecondaryBold, phosphor.database),
]
for nid, label, card_st, txt_st, ico_st, icon_fn in node_specs:
    n = raw.nodes[nid]
    cx, cy = n.x + 8.0, n.y + dy
    rectangle((cx, cy), width=n.width, height=n.height, style=card_st.patch(shape_r=1.8))
    icon_fn((cx - 8.5, cy), width=4.4, style=ico_st)
    text((cx + 2.2, cy), label, style=txt_st.patch(text_size=10.5))

solvers = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
solvers.add("ArchitectureGraph")
solvers.add("LayerGraph", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.0))
solvers.add("TreeGraph")
solvers.add("RadialGraph")
solvers.add("GridGraph", style=Styles.SecondaryNeutral)
solvers.draw(xy=(9.0, 8.0), box_width=22.8, box_height=7.0, direction="left")

save()
```

## `class` ArchitectureGraph

Declarative 2-level macro/micro architecture graph layout solver. `ArchitectureGraph` arranges top-level architectural containers (VPCs, clusters, client zones, external SaaS boundaries) across compass zones or along the primary macro flow axis while automatically ordering internal services, subnets, and databases inside their respective boundaries.

```python
from drawlib.graph import ArchitectureGraph

ArchitectureGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    container_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 24.0,
    default_node_height: float = 12.0,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | Primary macro layout flow axis (`"LR"` left-to-right or `"TB"` top-to-bottom). |
| `container_sep` | `float \| None` | `None` | Fixed spacing between top-level containers in canvas units; auto-scales when `None`. |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Edge path routing strategy (`"orthogonal"` right-angle segments or `"straight"` direct ports). |
| `default_node_width` | `float` | `24.0` | Default width assigned to registered nodes when `width` is omitted. |
| `default_node_height` | `float` | `12.0` | Default height assigned to registered nodes when `height` is omitted. |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | Register a node in the topology with optional `group` and `subgroup` container assignments. |
| `edge` | `(src, dst)` | [`Edge`](#edge) | Register a directed connection from `src` to `dst` (auto-registers missing node IDs on solve). |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register a grouping boundary with optional `parent` nesting, sibling `order`, and 5-zone compass `pos` (`"top"`, `"bottom"`, `"left"`, `"right"`, `"center"`). |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Keyword-only `nodes` alias for `cluster()` suited for VPCs, zones, and subnets. |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | Compute compound macro/micro coordinates without rendering (defaults to active canvas size). |

## `class` BaseGraph

Abstract base class inherited by all five declarative graph coordinate solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`). Provides shared node, edge, and cluster registration methods and the uniform `get_layout()` calculation interface.

```python
from drawlib.graph import BaseGraph

BaseGraph(
    *,
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `default_node_width` | `float` | `20.0` | Fallback node width in canvas units when `width` is not passed to `node()`. |
| `default_node_height` | `float` | `12.0` | Fallback node height in canvas units when `height` is not passed to `node()`. |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | Register a node in the graph topology. |
| `edge` | `(src, dst)` | [`Edge`](#edge) | Register a directed connection between two node IDs. |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register a grouping boundary surrounding a subset of nodes. |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register an architectural container or group boundary. |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | Compute node, edge, and cluster geometries without drawing onto the canvas. |

## `class` Cluster

Dataclass representing a user-registered grouping boundary returned by `g.cluster()` or `g.group()`.

```python
from drawlib.graph import Cluster

Cluster(
    id: str,
    nodes: list[str] = ...,
    padding: float = 4.0,
    header_height: float = 3.5,
    parent: str | None = None,
    order: int | None = None,
    pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Unique cluster or container identifier. |
| `nodes` | `list[str]` | `[]` | Member node IDs enclosed directly within this boundary. |
| `padding` | `float` | `4.0` | Inner clearance margin around enclosed nodes and child clusters. |
| `header_height` | `float` | `3.5` | Extra top clearance reserved for a container title banner. |
| `parent` | `str \| None` | `None` | Optional parent cluster ID for nested hierarchies (e.g., subnet inside VPC). |
| `order` | `int \| None` | `None` | Explicit ordering index among sibling containers. |
| `pos` | `Literal["top", "bottom", "left", "right", "center"] \| None` | `None` | Macro compass zone placement hint used by `ArchitectureGraph`. |

## `class` ClusterLayout

Calculated bounding box and hierarchy coordinates for a solved cluster container in `GraphLayout.clusters`. Provides both bottom-left corners (for `ArchitectureDiagram` `NodeGroup`) and center coordinates (for primitive shapes).

```python
from drawlib.graph import ClusterLayout

ClusterLayout(
    id: str,
    bbox: tuple[float, float, float, float],
    parent_id: str | None = None,
    local_bottom_left: tuple[float, float] = (0.0, 0.0),
) -> None
```

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Cluster identifier matching the registered `Cluster.id`. |
| `bbox` | `tuple[float, float, float, float]` | *(required)* | Global bounding box tuple `(left, bottom, right, top)` in canvas coordinates. |
| `parent_id` | `str \| None` | `None` | Parent cluster ID when nested inside an outer container, or `None` for top-level clusters. |
| `local_bottom_left` | `tuple[float, float]` | `(0.0, 0.0)` | Bottom-left `(x, y)` relative to the parent cluster's bottom-left origin. |

### Properties

| Property | Type | Description |
| :--- | :--- | :--- |
| `bottom` | `float` | Bottom edge Y coordinate (`bbox[1]`). |
| `bottom_left` | `tuple[float, float]` | Global bottom-left `(left, bottom)` coordinate (pass to top-level `NodeGroup`). |
| `center` | `tuple[float, float]` | Global cluster center `(cx, cy)` coordinate. |
| `cx` | `float` | Global cluster center X coordinate. |
| `cy` | `float` | Global cluster center Y coordinate. |
| `height` | `float` | Total cluster height (`top - bottom`). |
| `left` | `float` | Left edge X coordinate (`bbox[0]`). |
| `right` | `float` | Right edge X coordinate (`bbox[2]`). |
| `size` | `tuple[float, float]` | Cluster `(width, height)` dimensions. |
| `top` | `float` | Top edge Y coordinate (`bbox[3]`). |
| `width` | `float` | Total cluster width (`right - left`). |
| `xy` | `tuple[float, float]` | Alias for `center` (`(cx, cy)`), suited for center-anchored `rectangle()`. |

## `class` Edge

Dataclass representing a directed topological connection between two nodes returned by `g.edge(src, dst)`.

```python
from drawlib.graph import Edge

Edge(
    src: str,
    dst: str,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `src` | `str` | *(required)* | Source node ID where the directed edge originates. |
| `dst` | `str` | *(required)* | Destination node ID where the directed edge terminates. |

## `class` EdgeLayout

Calculated port coordinates and intermediate routing waypoints for a solved edge in `GraphLayout.edges`.

```python
from drawlib.graph import EdgeLayout

EdgeLayout(
    src: str,
    dst: str,
    src_port: tuple[float, float],
    dst_port: tuple[float, float],
    waypoints: list[tuple[float, float]] = ...,
) -> None
```

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `src` | `str` | *(required)* | Source node identifier. |
| `dst` | `str` | *(required)* | Destination node identifier. |
| `src_port` | `tuple[float, float]` | *(required)* | Boundary attachment point `(x, y)` on the source node perimeter. |
| `dst_port` | `tuple[float, float]` | *(required)* | Boundary attachment point `(x, y)` on the destination node perimeter. |
| `waypoints` | `list[tuple[float, float]]` | `[]` | Intermediate bend points `(x, y)` between `src_port` and `dst_port`. |

### Properties

| Property | Type | Description |
| :--- | :--- | :--- |
| `points` | `list[tuple[float, float]]` | Complete polyline sequence `[src_port, *waypoints, dst_port]` ready for `lines(edge.points, arrow_head="->")`. |
| `mid_xy` | `tuple[float, float]` | Geometric midpoint `(mx, my)` along the routed path for placing edge labels. |

## `class` GraphLayout

Complete geometrical result returned by `get_layout()` on any graph solver. Supports dictionary-style `layout[key]` lookup across both `nodes` and `clusters`, human-readable coordinate dumps via `print(layout)`, and post-solve node nudging via `.offset()`.

```python
from drawlib.graph import GraphLayout

GraphLayout(
    nodes: dict[str, NodeLayout] = ...,
    edges: list[EdgeLayout] = ...,
    clusters: dict[str, ClusterLayout] = ...,
    width: float = 100.0,
    height: float = 100.0,
    ring_radii: dict[int, float] = ...,
) -> None
```

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `nodes` | `dict[str, NodeLayout]` | `{}` | Mapping from node ID to solved [`NodeLayout`](#nodelayout). |
| `edges` | `list[EdgeLayout]` | `[]` | Ordered list of solved [`EdgeLayout`](#edgelayout) paths. |
| `clusters` | `dict[str, ClusterLayout]` | `{}` | Mapping from cluster ID to solved [`ClusterLayout`](#clusterlayout). |
| `width` | `float` | `100.0` | Target layout width in canvas units. |
| `height` | `float` | `100.0` | Target layout height in canvas units. |
| `ring_radii` | `dict[int, float]` | `{}` | Concentric ring index-to-radius mapping populated by [`RadialGraph`](#radialgraph). |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `offset` | `(node_id: str, dx: float = 0.0, dy: float = 0.0)` | `Self` | Shift `nodes[node_id]` by `(dx, dy)` (updating `.xy`, `.local_xy`, and incident edge ports) and return `self` for chaining. |

## `class` GridGraph

Declarative 2D matrix grid graph layout solver. Tiles nodes into regular rows and columns with configurable ordering (`"row-major"` or `"column-major"`), explicit `(row, col)` cell pinning, and inter-cell channel routing.

```python
from drawlib.graph import GridGraph

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
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `columns` | `int` | `3` | Number of grid columns (`>= 1`). |
| `rows` | `int \| None` | `None` | Optional explicit row count (computed automatically from node count when `None`). |
| `order` | `Literal["row-major", "column-major"]` | `"row-major"` | Automatic slot filling order for unpinned nodes. |
| `col_sep` | `float \| None` | `None` | Fixed horizontal gap between columns; auto-scales to canvas width when `None`. |
| `row_sep` | `float \| None` | `None` | Fixed vertical gap between rows; auto-scales to canvas height when `None`. |
| `edge_routing` | `Literal["smart", "orthogonal", "straight"]` | `"smart"` | Edge routing mode (`"smart"` routes non-adjacent links cleanly through grid channels). |
| `default_node_width` | `float` | `20.0` | Default cell node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default cell node height in canvas units. |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `cell` | `(cell_id, row=None, col=None, *, width=None, height=None)` | [`Node`](#node) | Convenience helper to register a grid cell node at an optional 0-based `(row, col)` slot. |
| `cluster_row` | `(row, cluster_id, *, padding=4.0, header_height=3.5)` | [`Cluster`](#cluster) | Group all nodes placed in 0-based `row` into a single cluster boundary. |
| `cluster_column` | `(col, cluster_id, *, padding=4.0, header_height=3.5)` | [`Cluster`](#cluster) | Group all nodes placed in 0-based `col` into a single cluster boundary. |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | Register a node in the matrix topology. |
| `edge` | `(src, dst)` | [`Edge`](#edge) | Register a connection between two grid nodes. |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register a custom cluster surrounding arbitrary grid cells. |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Keyword-only `nodes` alias for `cluster()`. |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | Compute matrix grid coordinates and routed edge paths without rendering. |

## `class` LayerGraph

Declarative Sugiyama-style layered hierarchical DAG layout solver (cycle breaking, longest-path rank assignment, and barycenter edge-crossing minimization). Ideal for CI/CD pipelines, ETL/Airflow data lineage, task DAGs, and module dependency graphs.

```python
from drawlib.graph import LayerGraph

LayerGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    rank_sep: float | None = None,
    node_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | Rank progression axis (`"LR"` left-to-right or `"TB"` top-to-bottom). |
| `rank_sep` | `float \| None` | `None` | Fixed spacing between consecutive ranks/layers; auto-scales when `None`. |
| `node_sep` | `float \| None` | `None` | Fixed spacing between sibling nodes within the same rank; auto-scales when `None`. |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Edge path routing mode (`"orthogonal"` Manhattan segments or `"straight"` direct ports). |
| `default_node_width` | `float` | `22.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `tier` | `(name, nodes, *, layer=None)` | `None` | Explicitly pin multiple node IDs to the same layer/rank index (`0, 1, ...`). |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | Register a node with an optional explicit `layer` rank. |
| `edge` | `(src, dst)` | [`Edge`](#edge) | Register a directed dependency edge from `src` to `dst`. |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register a stage boundary surrounding a subset of nodes. |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Keyword-only `nodes` alias for `cluster()`. |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | Compute hierarchical layered coordinates without rendering. |

## `class` Node

Dataclass representing a user-registered node in a graph topology returned by `g.node()`, `g.cell()`, `g.spoke()`, or `g.child()`.

```python
from drawlib.graph import Node

Node(
    id: str,
    width: float | None = None,
    height: float | None = None,
    ring: int | None = None,
    row: int | None = None,
    col: int | None = None,
    layer: int | None = None,
    group: str | None = None,
    subgroup: str | None = None,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Unique node identifier string. |
| `width` | `float \| None` | `None` | Node width override (`None` inherits solver's `default_node_width`). |
| `height` | `float \| None` | `None` | Node height override (`None` inherits solver's `default_node_height`). |
| `ring` | `int \| None` | `None` | Concentric ring index for `RadialGraph` (`0` = central hub). |
| `row` | `int \| None` | `None` | Explicit 0-based row index for `GridGraph`. |
| `col` | `int \| None` | `None` | Explicit 0-based column index for `GridGraph`. |
| `layer` | `int \| None` | `None` | Explicit 0-based rank/layer index for `LayerGraph`. |
| `group` | `str \| None` | `None` | Top-level container ID for `ArchitectureGraph`. |
| `subgroup` | `str \| None` | `None` | Nested child container ID inside `group` for `ArchitectureGraph`. |

## `class` NodeLayout

Calculated global and cluster-relative coordinates and dimensions for a solved node in `GraphLayout.nodes`.

```python
from drawlib.graph import NodeLayout

NodeLayout(
    id: str,
    xy: tuple[float, float],
    width: float,
    height: float,
    parent_id: str | None = None,
    local_xy: tuple[float, float] = (0.0, 0.0),
) -> None
```

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | *(required)* | Node identifier matching `Node.id`. |
| `xy` | `tuple[float, float]` | *(required)* | Global center `(cx, cy)` coordinate on the canvas. |
| `width` | `float` | *(required)* | Solved node width in canvas units. |
| `height` | `float` | *(required)* | Solved node height in canvas units. |
| `parent_id` | `str \| None` | `None` | Enclosing cluster ID when the node belongs to a cluster, else `None`. |
| `local_xy` | `tuple[float, float]` | `(0.0, 0.0)` | Center `(cx, cy)` relative to the enclosing cluster's `bottom_left` origin (for `NodeGroup.add()`). |

### Properties

| Property | Type | Description |
| :--- | :--- | :--- |
| `bottom` | `float` | Bottom edge Y coordinate (`y - height / 2`). |
| `bottom_left` | `tuple[float, float]` | Global bottom-left `(left, bottom)` corner coordinate. |
| `center` | `tuple[float, float]` | Alias for `xy` (`(x, y)` global center). |
| `left` | `float` | Left edge X coordinate (`x - width / 2`). |
| `local_bottom_left` | `tuple[float, float]` | Bottom-left corner relative to the parent cluster's `bottom_left` origin. |
| `right` | `float` | Right edge X coordinate (`x + width / 2`). |
| `size` | `tuple[float, float]` | Node dimensions `(width, height)`. |
| `top` | `float` | Top edge Y coordinate (`y + height / 2`). |
| `x` | `float` | Global center X coordinate (`xy[0]`). |
| `y` | `float` | Global center Y coordinate (`xy[1]`). |

## `class` RadialGraph

Declarative radial and concentric-ring graph layout solver. Places a central hub node at `center` and distributes connected spoke nodes across concentric orbital rings with even angular spacing (`GraphLayout.ring_radii` exposes each ring's radius for drawing background orbit circles).

```python
from drawlib.graph import RadialGraph

RadialGraph(
    hub: str | None = None,
    *,
    center: tuple[float, float] | None = None,
    radius_step: float | None = None,
    start_angle: float = 0.0,
    angle_range: float = 360.0,
    default_node_width: float = 20.0,
    default_node_height: float = 12.0,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `hub` | `str \| None` | `None` | Optional central hub node ID placed at ring `0` (inferred from topology if `None`). |
| `center` | `tuple[float, float] \| None` | `None` | Explicit `(cx, cy)` hub center coordinate; defaults to canvas center when `None`. |
| `radius_step` | `float \| None` | `None` | Radial distance increment per concentric ring; auto-scales to fit canvas when `None`. |
| `start_angle` | `float` | `0.0` | Starting angle in degrees (`0.0` = +X axis, counter-clockwise). |
| `angle_range` | `float` | `360.0` | Total angular sweep in degrees (`360.0` full circle, `180.0` fan/semicircle). |
| `default_node_width` | `float` | `20.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `spoke` | `(parent, spoke_id, *, ring=None, width=None, height=None)` | [`Node`](#node) | Convenience helper that registers `spoke_id` (optionally on `ring`) and connects an edge from `parent`. |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | Register a node with an optional concentric `ring` index. |
| `edge` | `(src, dst)` | [`Edge`](#edge) | Register a radial or cross-spoke connection. |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register a grouping boundary around a subset of nodes. |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Keyword-only `nodes` alias for `cluster()`. |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | Compute radial node coordinates, edge ports, and `ring_radii` without rendering. |

## `class` TreeGraph

Declarative tree layout solver using the Reingold-Tilford / Buchheim compact tree algorithm. Centers parent nodes cleanly above (`"TB"`) or beside (`"LR"`) their child subtrees without horizontal or vertical subtree overlap.

```python
from drawlib.graph import TreeGraph

TreeGraph(
    *,
    root: str | None = None,
    direction: Literal["TB", "LR"] = "TB",
    level_sep: float | None = None,
    sibling_sep: float | None = None,
    default_node_width: float = 22.0,
    default_node_height: float = 12.0,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `root` | `str \| None` | `None` | Explicit root node ID (auto-detected from zero-indegree node when `None`). |
| `direction` | `Literal["TB", "LR"]` | `"TB"` | Tree expansion direction (`"TB"` top-to-bottom or `"LR"` left-to-right). |
| `level_sep` | `float \| None` | `None` | Fixed distance between tree depth levels; auto-scales when `None`. |
| `sibling_sep` | `float \| None` | `None` | Minimum gap between adjacent sibling nodes/subtrees; auto-scales when `None`. |
| `default_node_width` | `float` | `22.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Parent-to-child connector routing style (`"orthogonal"` elbow fork or `"straight"`). |

### Public Methods

| Method | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `child` | `(parent, child_id, *, width=None, height=None)` | [`Node`](#node) | Convenience helper that registers `child_id` (and `parent` if needed) and adds edge `parent -> child_id`. |
| `node` | `(id, *, width=None, height=None, ring=None, row=None, col=None, layer=None, group=None, subgroup=None)` | [`Node`](#node) | Register a tree node. |
| `edge` | `(src, dst)` | [`Edge`](#edge) | Register a parent-to-child tree edge. |
| `cluster` | `(id, nodes=None, *, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Register a subtree or level grouping boundary. |
| `group` | `(id, *, nodes=None, padding=4.0, header_height=3.5, parent=None, order=None, pos=None)` | [`Cluster`](#cluster) | Keyword-only `nodes` alias for `cluster()`. |
| `get_layout` | `(*, width=None, height=None, margin=10.0)` | [`GraphLayout`](#graphlayout) | Compute tidy tree coordinates and routed connectors without rendering. |
