# ArchitectureGraph: Cloud Topologies & Nested Containers

`ArchitectureGraph` is a declarative **two-level macro/micro layout solver** purpose-built for cloud infrastructure, VPC topologies, and multi-zone microservice architectures.

Unlike generic DAG solvers that flatten nested groups or scramble boundary boxes, `ArchitectureGraph` solves layouts in two hierarchical phases:
1. **Micro Layout**: Packs internal nodes inside each leaf cluster (`g.cluster(...)`), and recursively packs child clusters inside parent containers (`parent="vpc"`, `order=1, 2, ...`).
2. **Macro Layout**: Arranges top-level containers across a **5-zone compass** (`pos="left" | "center" | "right" | "top" | "bottom"`) or along the primary flow axis (`direction="LR" | "TB"`), then routes orthogonal Manhattan highway edges with evenly distributed port offsets.

---

## 1. Constructor & Container Methods

```python
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

g = ArchitectureGraph(
    direction="LR",                  # "LR" (Left-to-Right) or "TB" (Top-to-Bottom)
    container_sep=None,              # Gap between top-level containers (auto-scales if None)
    edge_routing="orthogonal",       # "orthogonal" or "straight"
    default_node_style=Styles.Neutral,
    default_node_text_style=None,
    default_edge_style=Styles.DarkBold,
    default_container_style=Styles.MutedDashed,
    default_node_width=24.0,
    default_node_height=12.0,
)
```

### Parameter Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | Primary macro flow axis (`"LR"` left-to-right or `"TB"` top-to-bottom). |
| `container_sep` | `float \| None` | `None` | Fixed separation between top-level containers (auto-scales to fit canvas if `None`). |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Edge path routing strategy (`"orthogonal"` right-angled highway routing or `"straight"`). |
| `default_node_style` | `Style \| None` | `None` | Default style applied to nodes without an explicit `style` (defaults to `Styles.PrimaryFlat`). |
| `default_node_text_style` | `Style \| None` | `None` | Default typography style for node labels. |
| `default_edge_style` | `Style \| None` | `None` | Default line style for edges (defaults to `Styles.DarkBold`). |
| `default_edge_text_style` | `Style \| None` | `None` | Default text style for edge labels. |
| `default_container_style` | `Style \| None` | `None` | Default boundary box style for clusters and groups (defaults to `Styles.MutedDashed`). |
| `default_node_width` | `float` | `24.0` | Default node width in canvas units. |
| `default_node_height` | `float` | `12.0` | Default node height in canvas units. |

### Nested Clusters & 5-Zone Compass Placement

You can organize nodes into single-level or nested two-level containers using `g.group()` and `g.cluster()`, or by passing `group="..."` and `subgroup="..."` directly on `g.node()`:

- **`g.group(id, label=None, *, nodes=None, style=None, text_style=None, padding=4.0, parent=None, order=None, pos=None, show=True) -> Cluster`**:
  Creates a top-level or parent container (such as a Cloud VPC) that can hold child clusters (`parent=id`).
- **`g.cluster(id, nodes, label=None, *, style=None, text_style=None, padding=4.0, parent=None, order=None, pos=None, show=True) -> Cluster`**:
  Encloses a list of `nodes` inside a labeled boundary rectangle.
  - **`parent`**: ID of the enclosing parent group (e.g. `parent="vpc"`).
  - **`order`**: Integer rank (`1`, `2`, ...) controlling the sequence of sibling tiers inside a parent container.
  - **`pos`**: Compass zone (`"left"`, `"center"`, `"right"`, `"top"`, `"bottom"`) for macro placement on the canvas.
- **Inline Node Membership (`g.node(..., group="...", subgroup="...")`)**:
  During `calc()`, `ArchitectureGraph` inspects each node's `group` and `subgroup` attributes. Any referenced cluster ID that has not been explicitly created via `g.group()` or `g.cluster()` is **automatically registered** (using its ID as the label and `default_container_style`), the node is appended to the innermost container, and if both `group` and `subgroup` are provided, `subgroup.parent` is automatically linked to `group` (`subgroup.parent = node.group`). You can still call `g.group()` or `g.cluster()` before or after `g.node()` to customize labels, `pos`, `order`, or `padding`.

```drawlib fold-code 650px center file:graph_arch_compass_zones.png caption:"ArchitectureGraph 5-Zone Compass Layout (top, left, center, right, bottom) and Nested Sub-Clusters"
from drawlib.canvas import save, setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=218, height=132)

g = ArchitectureGraph(
    direction="LR",
    container_sep=9.0,
    default_node_text_style=Styles.Dark.patch(text_size=8.5),
    default_node_width=24.0,
    default_node_height=11.0,
)

# 1. Top Zone (pos="top")
g.cluster("top_zone", ["iam"], label="Control Plane (pos='top')", pos="top", padding=4.5)
g.node("iam", "IAM & Config", style=Styles.Neutral)

# 2. Left Zone (pos="left")
g.cluster("left_zone", ["waf"], label="Ingress Zone (pos='left')", pos="left", padding=4.5)
g.node("waf", "Edge WAF", style=Styles.Neutral)

# 3. Center Zone (pos="center") with two nested sub-clusters (parent="core", order=1 & 2)
g.group("core", "Core VPC (pos='center')", pos="center", padding=5.5)
g.cluster("tier1", ["api"], label="App Tier (order=1)", parent="core", order=1, padding=5.5)
g.cluster("tier2", ["worker"], label="Worker Tier (order=2)", parent="core", order=2, padding=5.5)
g.node("api", "API Gateway", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=8.5))
g.node("worker", "Task Worker", style=Styles.PrimaryNeutral)

# 4. Right Zone (pos="right")
g.cluster("right_zone", ["dr_replica"], label="Egress / DR (pos='right')", pos="right", padding=4.5)
g.node("dr_replica", "DR Replica", style=Styles.SecondaryNeutral)

# 5. Bottom Zone (pos="bottom")
g.cluster("bottom_zone", ["obs"], label="Observability & Storage (pos='bottom')", pos="bottom", padding=4.5)
g.node("obs", "Metrics & Logs", style=Styles.Neutral)

# Connect across all 5 compass zones
g.edge("waf", "api")
g.edge("api", "worker")
g.edge("worker", "dr_replica")
g.edge("iam", "api", style=Styles.MutedDashed)
g.edge("worker", "obs", style=Styles.MutedDashed)

g.draw(margin=10.0)
save()
```

---

## 2. Multi-VPC / Multi-Tier Cloud Topology with Nested Clusters

The following example builds a complete cloud architecture featuring an external client zone (`pos="left"`), a central production VPC (`pos="center"`) with nested Ingress, Compute, and Data tiers (`parent="vpc"`, `order=1, 2, 3`), and an observability zone (`pos="bottom"`):

```drawlib show-code 740px center file:graph_arch_multi_tier_vpc.png caption:"Multi-Tier Cloud VPC Topology with Nested Clusters and 5-Zone Compass Placement"
from drawlib.canvas import save, setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=200, height=118)

g = ArchitectureGraph(direction="LR", default_node_width=26.0, default_node_height=12.0)

# 1. External client zone pinned to the left
g.cluster("ext_zone", ["web_client", "mobile_client"], label="External Clients", pos="left", padding=5.0)
g.node("web_client", "Web App", style=Styles.Neutral)
g.node("mobile_client", "Mobile App", style=Styles.Neutral)

# 2. Central Production VPC with nested Compute and Data tiers
g.group("prod_vpc", "Production Cloud VPC (10.0.0.0/16)", pos="center", padding=5.5)
g.cluster(
    "compute_subnet",
    ["api_gw", "auth_svc", "order_svc"],
    label="Compute Subnet",
    parent="prod_vpc",
    order=1,
    padding=5.0,
)
g.cluster(
    "data_subnet",
    ["orders_db", "redis_cache"],
    label="Data Subnet",
    parent="prod_vpc",
    order=2,
    padding=5.0,
)

# 50%+ Neutral baseline; single PrimaryFlat hero node for the API Gateway
g.node("api_gw", "API Gateway", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("auth_svc", "Auth Service", style=Styles.PrimaryNeutral)
g.node("order_svc", "Order Worker", style=Styles.PrimaryNeutral)
g.node("orders_db", "Primary SQL", style=Styles.SecondaryNeutral)
g.node("redis_cache", "Redis Cache", style=Styles.SecondaryNeutral)

# 3. Shared observability platform pinned to the bottom
g.cluster("obs_zone", ["prometheus"], label="Observability VPC Peering", pos="bottom", padding=4.5)
g.node("prometheus", "Metrics & Logs", style=Styles.Neutral)

# 4. Orthogonal highway edges
g.edge("web_client", "api_gw", "HTTPS")
g.edge("mobile_client", "api_gw", "gRPC")
g.edge("api_gw", "auth_svc", "Verify")
g.edge("api_gw", "order_svc", "Dispatch")
g.edge("auth_svc", "redis_cache", "Session")
g.edge("order_svc", "orders_db", "Write")
g.edge("order_svc", "prometheus", style=Styles.MutedDashed)

g.draw(margin=10.0)
save()
```

---

## 3. Post-Layout Fine-Tuning with `calc()` and `offset()`

When an automatically calculated topology needs a subtle visual adjustment—or when you want to attach custom [`drawlib.shapes`](../02_drawing_primitives/shapes_basic.md) badges at exact node coordinates—call `layout = g.calc()`, apply `layout.offset(node_id, dx=..., dy=...)`, and then render via `layout.draw()`:

```drawlib show-code 700px center file:graph_arch_calc_offset.png caption:"Fine-Tuning ArchitectureGraph Coordinates with calc() and layout.offset()"
from drawlib.canvas import save, setup
from drawlib.graph import ArchitectureGraph
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=175, height=95)

g = ArchitectureGraph(direction="LR", default_node_width=26.0)

# Declare node membership directly via group / subgroup parameters
g.node("edge_lb", "Edge Router", group="dmz", style=Styles.Neutral)
g.node("core_api", "Core API", group="vpc", subgroup="app", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
g.node("worker", "Async Worker", group="vpc", subgroup="app", style=Styles.PrimaryNeutral)
g.node("AnalyticsDB", "Analytics DB", group="vpc", subgroup="storage", style=Styles.SecondaryNeutral)

g.edge("edge_lb", "core_api", "TLS 1.3")
g.edge("core_api", "worker", "Events")
g.edge("worker", "AnalyticsDB", "Batch")

# 1. Compute layout geometry without drawing
layout = g.calc(margin=12.0)

# 2. Nudge the Core API node slightly upward and re-align its incident edge ports
layout.offset("core_api", dx=0.0, dy=4.0)
layout.draw()

# 3. Overlay a SLA status badge right above the Core API node using computed coordinates
api_box = layout.nodes["core_api"]
rectangle(
    (api_box.x, api_box.top + 4.5),
    width=22.0,
    height=6.0,
    style=Styles.SuccessNeutral,
    text="SLA: 99.99%",
)

save()
```

---

## 4. Best Practices

1. **Use `pos` for Peripheral Zones**: Keep the main request pipeline in `pos="center"` (or `pos="left"` -> `pos="center"` -> `pos="right"`) and place cross-cutting concerns like CI/CD, IAM, or Observability in `pos="bottom"` or `pos="top"`.
2. **Ground Containers in Subtle Dashed Borders**: Leave container styles at their default `Styles.MutedDashed` (or a very light tint) so foreground service cards maintain crisp contrast.
3. **When You Need Cloud Icons**: If your diagram requires official `GcpIcon` or `PhosphorIcon` inside every node card, use [`ArchitectureDiagram`](../05_diagrams/architecture.md) in Chapter 5, or use `g.calc()` to compute node positions and place icons at `layout.nodes[id].xy`.
