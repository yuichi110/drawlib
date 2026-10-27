# Drawlib RadialGraph Guidelines (`lib-graph-radial`)

`RadialGraph` (`from drawlib.graph import RadialGraph`) is a declarative **concentric-ring and hub-and-spoke coordinate solver**. It places a central hub at `ring=0` and distributes connected spoke nodes across orbital rings (`ring=1, 2, ...`) with subtree-weighted angular sector allocation and boundary-clipped radial edge ports.

```text
                    [Ring 2 Spoke]
                          ▲
              . - ~ ~ ~ - │ - ~ ~ ~ - .
          . '       ┌─────┴─────┐       ' .
        .           │  Ring 1   │           .
       .            └─────▲─────┘            .
      │                   │                   │
      │  ┌────────┐   ┌───┴────┐   ┌────────┐ │
      │  │ Ring 1 │◄──┤  HUB   ├──►│ Ring 1 │ │
      │  └────────┘   └───┬────┘   └────────┘ │
       .                  │                  .
        .           ┌─────▼─────┐           .
          . '       │  Ring 1   │       ' .
              ' - . └───────────┘ . - '
```

---

## 1. Imports & Constructor Signature

```python
from drawlib.graph import Cluster, ClusterLayout, Edge, EdgeLayout, GraphLayout, Node, NodeLayout, RadialGraph

g = RadialGraph(
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

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `hub` | `str \| None` | `None` | Optional central hub node ID (`ring=0`). If `None`, automatically selects the highest-degree node. |
| `center` | `tuple[float, float] \| None` | `None` | Explicit `(cx, cy)` origin of the concentric rings (defaults to `(width / 2, height / 2)`). |
| `radius_step` | `float \| None` | `None` | Fixed radial distance between successive concentric rings (auto-scales to fit canvas if `None`). |
| `start_angle` | `float` | `0.0` | Starting angle in degrees (`0.0` = East/Right, `90.0` = North/Top). |
| `angle_range` | `float` | `360.0` | Total angular sweep in degrees (`360.0` for full circle, `180.0` for semicircular fan). |
| `default_node_width` | `float` | `20.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |

---

## 2. Spoke Registration (`.spoke()`), Concentric Rings, & `layout.ring_radii`

### 2.1 Registering Hub & Spokes (`g.spoke()`)
In addition to `g.node(id, ring=...)` and `g.edge(src, dst)`, `RadialGraph` provides `.spoke()` to register a spoke node and connect it from its parent/hub in one call:

```python
g.spoke(
    parent: str,
    spoke_id: str,
    *,
    ring: int | None = None,
    width: float | None = None,
    height: float | None = None,
) -> Node
```
- If `ring` is omitted, `RadialGraph` automatically assigns rings via BFS distance from `hub` (`hub` at `ring=0`, direct neighbors at `ring=1`, second-hop neighbors at `ring=2`, etc.).

### 2.2 Drawing Orbital Guide Circles with `layout.ring_radii`
Calling `layout = g.get_layout(width=..., height=..., margin=10.0)` populates `layout.ring_radii: dict[int, float]` mapping each ring index (`1, 2, ...`) to its solved radius around `layout[hub].xy`:

```python
hub = layout["core"]
for r in layout.ring_radii.values():
    circle(hub.xy, radius=r, style=Styles.MutedDashed)
```

---

## 3. Production Examples

### Example 3.1: Multi-Ring Event Mesh (`RadialGraph` + Orbital Ring Guides)
```drawlib align=center code=fold file=graph_radial_event_mesh.png caption="Step 1: RadialGraph.get_layout() -> Step 2: Orbital Ring Guides & Hub-and-Spoke Rendering"
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
