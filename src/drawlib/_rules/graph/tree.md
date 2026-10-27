# Drawlib TreeGraph Guidelines (`lib-graph-tree`)

`TreeGraph` (`from drawlib.graph import TreeGraph`) is a declarative **Reingold-Tilford / Buchheim tree coordinate solver** that arranges hierarchical trees into compact, symmetrical subtrees where parents are centered over (or beside) their children and sibling subtrees are guaranteed never to overlap.

```text
                       ┌────────────────┐
                       │ VP Engineering │
                       └───────┬────────┘
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
         ┌───────────────┐           ┌───────────────┐
         │ Platform Team │           │ Product Team  │
         └───────┬───────┘           └───────┬───────┘
           ┌─────┴─────┐               ┌─────┴─────┐
           ▼           ▼               ▼           ▼
       ┌───────┐   ┌───────┐       ┌───────┐   ┌───────┐
       │ Infra │   │  Sec  │       │  Web  │   │  Mob  │
       └───────┘   └───────┘       └───────┘   └───────┘
```

---

## 1. Imports & Constructor Signature

```python
from drawlib.graph import Cluster, ClusterLayout, Edge, EdgeLayout, GraphLayout, Node, NodeLayout, TreeGraph

g = TreeGraph(
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

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `root` | `str \| None` | `None` | Optional explicit root node ID. If `None`, automatically detects nodes with in-degree `0`. |
| `direction` | `Literal["TB", "LR"]` | `"TB"` | Tree growth axis (`"TB"` Top-to-Bottom or `"LR"` Left-to-Right). |
| `level_sep` | `float \| None` | `None` | Fixed gap between generational levels (auto-scales to fit canvas if `None`). |
| `sibling_sep` | `float \| None` | `None` | Fixed minimum gap between sibling nodes (auto-scales to fit canvas if `None`). |
| `default_node_width` | `float` | `22.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Edge path algorithm (`"orthogonal"` Manhattan step bends or `"straight"` direct ports). |

---

## 2. Tree Declaration, `.child()`, & Strict Tree Validation

### 2.1 Declaring Parent-Child Relationships (`g.child()`)

In addition to `g.node()` and `g.edge(parent, child)`, `TreeGraph` provides the `.child()` convenience method that registers a child node (auto-registering `parent` if needed) and creates the directed parent-to-child edge in a single call:

```python
g.child(
    parent: str,
    child_id: str,
    *,
    width: float | None = None,
    height: float | None = None,
) -> Node
```

### 2.2 Strict Acyclic Single-Parent Validation
- `TreeGraph` enforces a strict tree topology during `get_layout()`:
  - **Single Parent**: Every node may have at most one incoming parent edge. If a node has multiple parents (a diamond DAG), `TreeGraph` raises a `ValueError` recommending `LayerGraph` or `ArchitectureGraph`.
  - **Acyclic**: Directed cycles raise a `ValueError`.
- Multiple roots (forests of disjoint trees) are supported automatically when `root=None`.

### 2.3 Computing the Layout (`g.get_layout()`)
```python
layout = g.get_layout(
    *,
    width: float | None = None,
    height: float | None = None,
    margin: float = 10.0,
) -> GraphLayout
```
- Defaults `width` and `height` to active `canvas` dimensions (or `120.0 x 60.0` fallback).
- Render the solved layout using `lines(edge.points, arrow_head="->")` and `rectangle(n.xy, width=n.width, height=n.height, ...)` or `FlowDiagram`.

---

## 3. Production Examples

### Example 3.1: Symmetrical Organization & System Taxonomy (`TreeGraph` + `shapes`/`lines`)
```drawlib align=center code=fold file=graph_tree_org_hierarchy.png caption="Step 1: TreeGraph.get_layout() -> Step 2: Orthogonal Tree Rendering"
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
