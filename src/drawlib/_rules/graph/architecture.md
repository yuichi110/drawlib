# Drawlib ArchitectureGraph Guidelines (`lib-graph-architecture`)

`ArchitectureGraph` (`from drawlib.graph import ArchitectureGraph`) is a declarative **2-level macro/micro architecture coordinate solver** designed for cloud topologies, VPC/subnet boundaries, and multi-zone microservice architectures. It pairs seamlessly with `ArchitectureDiagram` (`lib-diagrams-architecture`).

```text
  ┌──────────────────┐    ┌───────────────────────────────────────────────────┐
  │ pos="left"       │    │ pos="center": Production VPC (parent=None)        │
  │ [Client Zone]    │    │   ┌────────────────────┐   ┌────────────────────┐ │
  │   ┌──────────┐   │    │   │ Compute (order=1)  │   │ Data (order=2)     │ │
  │   │  Client  ├───┼───►│   │  ┌─────┐  ┌─────┐  │   │  ┌─────┐  ┌─────┐  │ │
  │   └──────────┘   │    │   │  │ API ├─►│ App │──┼──►│  │ SQL │  │Cache│  │ │
  └──────────────────┘    │   │  └─────┘  └─────┘  │   │  └─────┘  └─────┘  │ │
                          │   └────────────────────┘   └────────────────────┘ │
                          └───────────────────────────────────────────────────┘
```

---

## 1. Imports & Constructor Signature

```python
from drawlib.graph import ArchitectureGraph, Cluster, ClusterLayout, Edge, EdgeLayout, GraphLayout, Node, NodeLayout

g = ArchitectureGraph(
    *,
    direction: Literal["LR", "TB"] = "LR",
    container_sep: float | None = None,
    edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    default_node_width: float = 24.0,
    default_node_height: float = 12.0,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `direction` | `Literal["LR", "TB"]` | `"LR"` | Primary macro flow axis (`"LR"` Left-to-Right or `"TB"` Top-to-Bottom). |
| `container_sep` | `float \| None` | `None` | Fixed spacing between adjacent top-level containers (auto-scales to fit canvas if `None`). |
| `edge_routing` | `Literal["orthogonal", "straight"]` | `"orthogonal"` | Edge path algorithm (`"orthogonal"` Manhattan right-angles or `"straight"` direct ports). |
| `default_node_width` | `float` | `24.0` | Default width for nodes when `width` is omitted in `g.node()`. |
| `default_node_height` | `float` | `12.0` | Default height for nodes when `height` is omitted in `g.node()`. |

---

## 2. Topology Declaration & 2-Level Container Hierarchy

### 2.1 Declaring Containers (`g.group()`, `g.cluster()`) & Nodes (`g.node()`)

`ArchitectureGraph` supports two complementary ways to assign nodes to top-level groups and nested subgroups:

1. **Cluster-First Declaration (`g.group()` / `g.cluster()`)**:
   ```python
   g.group("vpc", pos="center", padding=5.0, header_height=3.5)
   g.cluster("app_subnet", ["api", "worker"], parent="vpc", order=1, padding=5.0)
   g.cluster("data_subnet", ["db", "redis"], parent="vpc", order=2, padding=5.0)
   ```
2. **Node-First Declaration (`group=...`, `subgroup=...` on `g.node()`)**:
   ```python
   g.node("api", group="vpc", subgroup="app_subnet", width=24.0, height=15.0)
   g.node("db", group="vpc", subgroup="data_subnet", width=24.0, height=15.0)
   ```
   *(Any referenced `group`, `subgroup`, or `cluster.nodes` entry is automatically registered during `get_layout()`.)*

### 2.2 Macro Compass Placement (`pos`) & Sibling Ordering (`order`)
- **Compass Zone Pinning (`pos: Literal["top", "bottom", "left", "right", "center"] | None = None`)**:
  Places top-level containers into dedicated spatial zones around the central architecture (e.g. `pos="left"` for external clients, `pos="center"` for the core VPC, `pos="right"` for data warehouse/analytics, `pos="bottom"` for observability/CI-CD, `pos="top"` for IAM/DNS).
- **Sibling Container Ordering (`order: int | None = None`)**:
  Controls the sequential tier order (`order=1`, `order=2`, ...) of child subnets inside a parent VPC or peer containers along `direction`.

### 2.3 Mapping `GraphLayout` Coordinates to `ArchitectureDiagram`

When feeding `layout = g.get_layout(width=..., height=..., margin=10.0)` into `ArchitectureDiagram`:
- **Top-Level `NodeGroup` (`parent_id is None`)**: Pass `xy=layout["vpc"].bottom_left` to `d.add(NodeGroup(...), xy=...)`.
- **Nested `NodeGroup` (`parent_id is not None`)**: Pass `xy=layout["app_subnet"].local_bottom_left` to `vpc_grp.add(NodeGroup(...), xy=...)`.
- **Node Inside a `NodeGroup`**: Pass `xy=layout["api"].local_xy` to `subnet_grp.add(Node(...), xy=...)`.
- **Standalone Node Outside All Groups**: Pass `xy=layout["user"].xy` to `d.add(Node(...), xy=...)`.
- **Match `padding` and `(width, height)`**: Always pass the same `padding` to `NodeGroup(padding=5.0)` and the same `(width, height)` to `Node(width=24, height=15)` that you configured in `ArchitectureGraph`.

---

## 3. Production Examples

### Example 3.1: 5-Zone Compass Cloud Architecture (`ArchitectureGraph` + `ArchitectureDiagram`)
```drawlib align=center code=fold file=graph_arch_compass_vpc.png caption="Step 1: ArchitectureGraph.get_layout() -> Step 2: ArchitectureDiagram Rendering"
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

# Step 2: Render cloud topology with ArchitectureDiagram using solved coordinates
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
app_grp = vpc_grp.add(
    NodeGroup(title="Compute Tier", padding=5.0, style=Styles.PrimaryNeutral),
    xy=layout["app_tier"].local_bottom_left,
)
data_grp = vpc_grp.add(
    NodeGroup(title="Data Tier", padding=5.0, style=Styles.SecondaryNeutral),
    xy=layout["data_tier"].local_bottom_left,
)
obs_grp = d.add(NodeGroup(title="Observability", padding=5.0, style=Styles.MutedDashed), xy=layout["obs"].bottom_left)

# Nodes inside a NodeGroup use .local_xy
client = ext_grp.add(Node("Client App", width=24, height=15, icon=PhosphorIcon.DEVICES), xy=layout["client"].local_xy)
api = app_grp.add(
    Node(
        "API Gateway",
        width=24,
        height=15,
        icon=GcpIcon.CLOUD_API_GATEWAY,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
    ),
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
