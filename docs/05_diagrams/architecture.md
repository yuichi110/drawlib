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

- **Icon-Centric Coordinates**: When placing a node via `d.add(node, xy=(x, y))`, the coordinate strictly defines the **center of the icon**. The text label is offset according to `text_position` (`"bottom"`, `"top"`, `"left"`, `"right"`), ensuring that horizontally or vertically aligned icons maintain perfectly straight wire connections.
- **Hierarchical Auto-Bounding (`NodeGroup`)**: Groups automatically compute their outer boundary boxes to enclose all enclosed nodes and nested sub-groups with configurable padding.
- **Connectable Boundaries**: You can connect edges directly to or from a group's perimeter box as well as individual nodes.
- **1-to-N Fan-Out (`fork`)**: Easily split a single connection line into multiple downstream destinations using an automatic intermediate bus line.

---

## 2. Constructor & Core Classes

```python
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

d = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    title="Production Multi-Tier Cloud VPC",
)
```

### Parameter Reference

#### `ArchitectureDiagram` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `node_style` | `Style` | *(Required)* | Default style for nodes and card backgrounds. |
| `edge_style` | `Style` | *(Required)* | Default style for connection lines and arrowheads. |
| `title` | `str` | `""` | Optional banner title for the diagram. |
| `width` | `float \| None` | `None` | Explicit diagram canvas width, or `None` for auto-fit. |
| `height` | `float \| None` | `None` | Explicit diagram canvas height, or `None` for auto-fit. |
| `margin` | `float` | `5.0` | Outer margin around all elements. |
| `style` | `Style \| None` | `None` | Overall diagram background and border style. |

#### `Node` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `""` | Node label text (supports `\n`). |
| `icon` | `IconType \| None` | `None` | `PhosphorIcon`, `GcpIcon`, or `CustomIcon`. |
| `icon_size` | `float` | `8.0` | Outer width and height of the icon square. |
| `text_position` | `"bottom"` \| `"top"` \| `"left"` \| `"right"` | `"bottom"` | Label placement relative to icon center. |
| `style` | `Style \| None` | `None` | Optional typography or node background style. |

#### `NodeGroup` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `""` | Group banner title (e.g. `"VPC Network (10.0.0.0/16)"`). |
| `padding` | `float` | `6.0` | Inner margin around enclosed child nodes. |
| `style` | `Style \| None` | `None` | Style for group background fill and boundary border. |

---

## 3. Production Cloud VPC Architecture

The following complete example demonstrates public and private subnets, load balancing, GKE pods, Cloud SQL, and external users:



<figure class="drawlib-image" style="text-align: center;">
  <img src="architecture_images/1.png" alt="architecture_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Production Multi-Tier Cloud VPC Topology</figcaption>
</figure>



---

## 4. Event-Driven Streaming Mesh

You can also use general architecture icons from `PhosphorIcon` to model messaging queues, Kafka clusters, and analytics engines:



<figure class="drawlib-image" style="text-align: center;">
  <img src="architecture_images/2.png" alt="architecture_2" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Event-Driven Message Streaming Topology</figcaption>
</figure>



---

## 5. Best Practices & Guidelines

1. **Keep Coordinates Icon-Centric**: When aligning multiple nodes in a row or column, give them the exact same X or Y coordinate. The text labels will not alter the position of the icon or connections.
2. **Use `fork` for Fan-Out**: Avoid drawing multiple crossing lines from a single node. Use `node.fork([n1, n2, ...], at_x=...)` to create clean right-angle bus routes.
3. **Padded Boundaries**: Always set `padding` on `NodeGroup` (typically `5.0` to `7.0`) to give enclosed components breathing room from the border lines.
