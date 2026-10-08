# Architecture Diagrams: Cloud Topologies, Microservices & VPC Boundaries

`ArchitectureDiagram` visualizes distributed systems, cloud networks, microservices topologies, and infrastructure boundaries. It pairs icon-centric nodes with automatic hierarchical boundary boxes (`NodeGroup`) and multi-way branch routing.

---

## 1. Overview & Key Concepts

```text
 ┌──────────────────────────────────────────────────────────────┐
 │ VPC Network (NodeGroup)                                      │
 │   ┌────────────────────────┐    ┌────────────────────────┐   │
 │   │ Public Subnet          │    │ Private Subnet         │   │
 │   │      ┌──────┐          │    │      ┌──────┐          │   │
 │   │      │ [LB] │──────────┼────┼─────►│[App1]│          │   │
 │   │      └──────┘          │    │      └──────┘          │   │
 │   └────────────────────────┘    └────────────────────────┘   │
 └──────────────────────────────────────────────────────────────┘
```

- **Card-Centric Coordinates**: When placing a node via `d.add(node, xy=(x, y))`, the coordinate defines the **center of the node card** `card_size=(width, height)`. When both `icon` and `text` are present, the icon is positioned in the upper middle and the text label in the lower portion (adjustable via `text_style=Styles.DarkBold.patch(xy_shift=...)`). If neither `node_card_style` nor `card_style` is provided, the card background is transparent.
- **Hierarchical Auto-Bounding (`NodeGroup`)**: Groups automatically compute their outer boundary boxes to enclose all enclosed nodes and nested sub-groups with configurable padding.
- **Connectable Boundaries**: You can connect edges directly to or from a group's perimeter box as well as individual nodes.
- **1-to-N Fan-Out (`fork`)**: Easily split a single connection line into multiple downstream destinations using an automatic intermediate bus line.

---

## 2. Constructor & Core Classes

```python
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Production Multi-Tier Cloud VPC",
)
```

### Parameter Reference

#### `ArchitectureDiagram` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `node_style` | `Style` | *(Required)* | Default style for node icons and images. |
| `node_text_style` | `Style` | *(Required)* | Default style for node text labels. |
| `edge_style` | `Style` | *(Required)* | Default style for connection lines and arrowheads. |
| `edge_text_style` | `Style` | *(Required)* | Default style for connection text labels. |
| `node_card_style` | `Style \| None` | `None` | Default style for node card backgrounds (transparent if `None`). |
| `title` | `str` | `""` | Optional banner title for the diagram. |
| `title_style` | `Style \| None` | `None` | Optional style for diagram title. |
| `width` | `float \| None` | `None` | Explicit diagram canvas width, or `None` for auto-fit. |
| `height` | `float \| None` | `None` | Explicit diagram canvas height, or `None` for auto-fit. |
| `margin` | `float` | `5.0` | Outer margin around all elements. |
| `style` | `Style \| None` | `None` | Overall diagram background and border style. |

#### `Node` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `card_size` | `tuple[float, float]` | *(Required)* | Card bounding box `(width, height)` in canvas units. |
| `text` | `str` | `""` | Node label text (supports `\n`). |
| `icon` | `IconType` | `None` | `PhosphorIcon`, `GcpIcon`, icon callable, `CustomIcon`, `Dimage`, `PIL.Image`, or path. |
| `icon_size` | `float` | `8.0` | Outer width and height of the icon/image. |
| `style` | `Style \| None` | `None` | Optional style override for the icon or image. |
| `text_style` | `Style \| None` | `None` | Optional style override for the label text (supports `xy_shift`, `angle`). |
| `card_style` | `Style \| None` | `None` | Optional style override for the card background/border (transparent if `None` and `node_card_style` is `None`). |
| `show` | `bool` | `True` | Visibility flag (connected edges auto-hide when `False`). |

#### `NodeGroup` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `""` | Group banner title (e.g. `"VPC Network (10.0.0.0/16)"`). |
| `padding` | `float` | `6.0` | Inner margin around enclosed child nodes. |
| `style` | `Style \| None` | `None` | Style for group background fill and boundary border. |
| `show` | `bool` | `True` | Visibility flag (hides group box, child nodes, and connected edges when `False`, while preserving outer auto-bounds). |

#### Registration, Connection & Rendering Methods
- `d.add(item, xy=(x, y), *, show: bool = True) -> Node | NodeGroup | Junction` (also available on `group.add(...)`)
- `d.connect(src, dst, label="", ..., show: bool = True) -> Edge` (or `node.connect(dst, ..., show: bool = True) -> Edge`)
- `node.fork(targets, at_x=None, at_y=None, ..., show: bool = True) -> list[Edge]`
- `d.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`

---

## 3. Production Cloud VPC Architecture

The following complete example demonstrates public and private subnets, load balancing, GKE pods, Cloud SQL, and external users:

```drawlib 650px center file:architecture_cloud_vpc_topology.png caption:"Production Multi-Tier Cloud VPC Topology"
from drawlib import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=165, height=102)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Production Multi-Tier Cloud VPC",
)

# 1. Outer VPC Network Boundary
vpc = d.add(NodeGroup(title="VPC Network (10.0.0.0/16)", padding=7.0), xy=(35.0, 8.0))

# 2. Public Subnet with Load Balancer (local coordinates inside vpc)
public_subnet = vpc.add(NodeGroup(title="Public Subnet (10.0.1.0/24)", padding=5.0), xy=(6.0, 6.0))
lb = public_subnet.add(Node((26, 18), "Cloud Load\nBalancer", icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=8.0), xy=(16.0, 30.0))

# 3. Private Subnet with Application Pods (local coordinates inside vpc)
private_subnet = vpc.add(NodeGroup(title="Private Subnet (10.0.2.0/24)", padding=5.0), xy=(48.0, 6.0))
gke1 = private_subnet.add(Node((20, 16), "API Pod 1", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0), xy=(14.0, 44.0))
gke2 = private_subnet.add(Node((20, 16), "API Pod 2", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0), xy=(14.0, 16.0))

# 4. External Actor and Managed Services (global diagram coordinates outside vpc)
user = d.add(Node((22, 16), "Client User", icon=PhosphorIcon.USER, icon_size=8.0), xy=(11.0, 44.0))
db = d.add(Node((26, 18), "Cloud SQL\n(PostgreSQL)", icon=GcpIcon.CLOUD_SQL, icon_size=8.0), xy=(143.0, 58.0))
storage = d.add(Node((26, 18), "Cloud Storage\n(Assets)", icon=GcpIcon.CLOUD_STORAGE, icon_size=8.0), xy=(143.0, 30.0))

# 5. Connections
d.connect(user, lb, label="HTTPS (443)", padding=1.5)
lb.fork([gke1, gke2], at_x=76.0, padding=1.5)
d.connect(gke1, db, label="SQL Query", padding=1.5)
d.connect(gke2, storage, label="Asset Sync", padding=1.5)

d.draw(xy=(4.0, 4.0))
```

---

## 4. Event-Driven Streaming Mesh

You can also use general architecture icons from `PhosphorIcon` to model messaging queues, Kafka clusters, and analytics engines:

```drawlib 650px center file:architecture_event_message_streaming.png caption:"Event-Driven Message Streaming Topology"
from drawlib import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=136, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Event-Driven Message Streaming Topology",
)

cluster = d.add(NodeGroup(title="Streaming Event Mesh", padding=6.0), xy=(32.0, 10.0))
broker1 = cluster.add(Node((24, 16), "Kafka Broker 1", icon=PhosphorIcon.STACK, icon_size=7.0), xy=(18.0, 40.0))
broker2 = cluster.add(Node((24, 16), "Kafka Broker 2", icon=PhosphorIcon.STACK, icon_size=7.0), xy=(18.0, 14.0))

pub = d.add(Node((22, 18), "Event Ingest\nProducer", icon=PhosphorIcon.BROADCAST, icon_size=7.5), xy=(11.0, 37.0))
analytics = d.add(Node((30, 18), "Realtime Analytics\nConsumer", icon=PhosphorIcon.CHART_BAR, icon_size=7.5), xy=(108.0, 50.0))
archiver = d.add(Node((30, 18), "Parquet Lakehouse\nArchiver", icon=PhosphorIcon.HARD_DRIVES, icon_size=7.5), xy=(108.0, 24.0))

pub.fork([broker1, broker2], at_x=27.0, padding=1.5)
d.connect(broker1, analytics, label="Consumer Group A", padding=1.5)
d.connect(broker2, archiver, label="Consumer Group B", padding=1.5)

d.draw(xy=(4.0, 4.0))
```

---

## 5. Best Practices & Guidelines

1. **Align Node Centers**: When aligning multiple nodes in a row or column, give them the exact same X or Y coordinate so horizontal and vertical connections stay straight.
2. **Use `fork` for Fan-Out**: Avoid drawing multiple crossing lines from a single node. Use `node.fork([n1, n2, ...], at_x=...)` to create clean right-angle bus routes.
3. **Padded Boundaries**: Always set `padding` on `NodeGroup` (typically `5.0` to `7.0`) to give enclosed components breathing room from the border lines.
