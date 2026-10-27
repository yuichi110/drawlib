# Drawlib GridGraph Guidelines (`lib-graph-grid`)

`GridGraph` (`from drawlib.graph import GridGraph`) is a declarative **2D matrix grid coordinate solver** that tiles nodes across `(row, col)` matrix slots, automatically groups entire rows or columns into `ClusterLayout` bands (`.cluster_row()`, `.cluster_column()`), and routes non-adjacent edges cleanly through inter-row and inter-column corridors (`edge_routing="smart"`).

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │ Row 0 Cluster ("row_fe"): Client Interfaces                         │
  │   ┌───────────────┐       ┌───────────────┐       ┌───────────────┐ │
  │   │  (0, 0) Web   │       │  (0, 1) Mob   │       │  (0, 2) CLI   │ │
  │   └───────┬───────┘       └───────┬───────┘       └───────┬───────┘ │
  └───────────┼───────────────────────┼───────────────────────┼─────────┘
              └───────────────┐       │                       │
  ┌───────────────────────────┼───────┼───────────────────────┼─────────┐
  │ Row 1 Cluster ("row_be")  ▼       ▼                       ▼         │
  │   ┌───────────────┐       ┌───────────────┐       ┌───────────────┐ │
  │   │  (1, 0) Auth  │       │  (1, 1) Core  ├──────►│  (1, 2) Pay   │ │
  │   └───────────────┘       └───────────────┘       └───────────────┘ │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Imports & Constructor Signature

```python
from drawlib.graph import Cluster, ClusterLayout, Edge, EdgeLayout, GraphLayout, GridGraph, Node, NodeLayout

g = GridGraph(
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

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `columns` | `int` | `3` | Number of matrix columns (`>= 1`). |
| `rows` | `int \| None` | `None` | Optional fixed number of rows (used primarily when `order="column-major"`). |
| `order` | `Literal["row-major", "column-major"]` | `"row-major"` | Automatic slot-filling sequence for nodes without explicit `(row, col)` coordinates. |
| `col_sep` | `float \| None` | `None` | Fixed horizontal gap between columns (auto-scales to fit canvas if `None`). |
| `row_sep` | `float \| None` | `None` | Fixed vertical gap between rows (auto-scales to fit canvas if `None`). |
| `edge_routing` | `Literal["smart", "orthogonal", "straight"]` | `"smart"` | `"smart"` routes non-adjacent cells through inter-row/inter-column channels to avoid crossing intermediate cells; `"orthogonal"` uses standard L/Z-bends; `"straight"` uses direct ports. |
| `default_node_width` | `float` | `20.0` | Default cell node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default cell node height in canvas units. |

---

## 2. Matrix Cell Pinning & Row/Column Cluster Helpers

### 2.1 `g.cell(...) -> Node`
Registers a node with optional 0-based `(row, col)` matrix coordinates (`row=0` is the top row; `col=0` is the leftmost column):

```python
g.cell(
    cell_id: str,
    row: int | None = None,
    col: int | None = None,
    *,
    width: float | None = None,
    height: float | None = None,
) -> Node
```
*(Nodes where `row` or `col` is `None` are automatically placed into the next unoccupied slot according to `order="row-major"` or `"column-major"`.)*

### 2.2 `g.cluster_row(...)` & `g.cluster_column(...)`
Automatically encloses all nodes assigned to a specific row or column inside a `ClusterLayout` boundary during `get_layout()`:

```python
g.cluster_row(
    row: int,
    cluster_id: str,
    *,
    padding: float = 4.0,
    header_height: float = 3.5,
) -> Cluster

g.cluster_column(
    col: int,
    cluster_id: str,
    *,
    padding: float = 4.0,
    header_height: float = 3.5,
) -> Cluster
```

---

## 3. Production Examples

### Example 3.1: 2x3 Tiered Service Matrix (`GridGraph` + `cluster_row()`)
```drawlib align=center code=fold file=graph_grid_service_matrix.png caption="Step 1: GridGraph.get_layout() -> Step 2: Matrix Cells & Row Cluster Rendering"
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
