# Drawlib ArchitectureDiagram Guidelines (`lib-diagrams-architecture`)

`drawlib.diagrams.architecture` visualizes distributed systems, cloud infrastructure, microservices topologies, and hierarchical network boundaries (`NodeGroup`). It pairs icon-centric service cards (`Node`) with nested boundary containers, multi-way bus branching (`Junction`, `node.fork()`), and flexible edge routing.

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

---

## 1. Public Exports & Imports

```python
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    CustomIcon,
    Edge,
    Junction,
    Node,
    NodeGroup,
    icons,
    # 33 Built-in Icon Enums:
    AiIcon,
    AwsIcon,
    AzureIcon,
    BusinessIcon,
    ClientIcon,
    CloudIcon,
    CnativeIcon,
    CodeIcon,
    DataIcon,
    DevopsIcon,
    FacilityIcon,
    GcpIcon,
    ItserviceIcon,
    NetworkIcon,
    OriginalAiIcon,
    OriginalBusinessIcon,
    OriginalClientIcon,
    OriginalCloudIcon,
    OriginalCnativeIcon,
    OriginalCodeIcon,
    OriginalDataIcon,
    OriginalDevopsIcon,
    OriginalFacilityIcon,
    OriginalItserviceIcon,
    OriginalNetworkIcon,
    OriginalSecurityIcon,
    OriginalServerIcon,
    OriginalSocialIcon,
    OriginalWorkspaceIcon,
    PhosphorIcon,
    SecurityIcon,
    ServerIcon,
    SocialIcon,
    WorkspaceIcon,
)
```

---

## 2. Core Classes & Constructor Parameters

### 2.1 `ArchitectureDiagram`

```python
d = ArchitectureDiagram(
    *,
    node_style: Style,
    node_text_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    node_card_style: Style | None = None,
    title: str = "",
    title_style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | `Style` | *(Required)* | Default style for node icons and vector symbols (keyword-only). |
| `node_text_style` | `Style` | *(Required)* | Default typography style for node labels and fallback group titles (keyword-only). |
| `edge_style` | `Style` | *(Required)* | Default stroke style for connection lines and arrowheads (keyword-only). |
| `edge_text_style` | `Style` | *(Required)* | Default typography style for connection edge labels (keyword-only). |
| `node_card_style` | `Style \| None` | `None` | Default style for node card backgrounds and borders (transparent if `None`). |
| `title` | `str` | `""` | Optional diagram title rendered at the top center. |
| `title_style` | `Style \| None` | `None` | Optional typography style for the diagram title. |
| `width` | `float \| None` | `None` | Optional explicit diagram width override (auto-calculated from elements if `None`). |
| `height` | `float \| None` | `None` | Optional explicit diagram height override (auto-calculated from elements if `None`). |
| `style` | `Style \| None` | `None` | Optional background card style for the entire diagram container. |

#### Diagram Methods:
- **`d.add(item, xy=(0.0, 0.0), *, show=None) -> Node | NodeGroup | Junction`**:
  Registers a `Node` (anchored at **center** `xy`), `NodeGroup` (anchored at **bottom-left** `xy`), or `Junction` (at `xy`) in the diagram's coordinate space. Optionally overrides `item.show`.
- **`d.connect(start, end, label="", arrow="->", routing="orthogonal", style=None, text_style=None, padding=0.0, show=True) -> Edge`**:
  Creates and registers an `Edge` between any two connectables (`Node`, `NodeGroup`, or `Junction`).
- **`d.add_edge(edge, *, show=None) -> Edge`**:
  Registers a pre-constructed `Edge` instance with the diagram (optionally overriding `edge.show`).
- **`d.junction(xy, *, show=True) -> Junction`**:
  Creates and registers a zero-size routing waypoint / merge point at `xy`.
- **`d.get_size() -> tuple[float, float]`**:
  Returns the total `(width, height)` of the diagram in unscaled local units.
- **`d.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0) -> None`**:
  Renders the complete diagram onto the active canvas anchored at `xy` (`align: Literal["bottom_left", "center"] = "bottom_left"`, `scale: float = 1.0`).

---

### 2.2 `Node`

```python
node = Node(
    text: str = "",
    width: float = 20.0,
    height: float = 16.0,
    icon: IconType = None,
    icon_size: float = 8.0,
    style: Style | None = None,
    text_style: Style | None = None,
    card_style: Style | None = None,
    show: bool = True,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | Node label text (supports multiline `\n`). |
| `width` | `float` | `20.0` | Card bounding box width in local units. |
| `height` | `float` | `16.0` | Card bounding box height in local units. |
| `icon` | `IconType` | `None` | Any of the 33 icon enums (`PhosphorIcon`, `GcpIcon`, `AwsIcon`, `AzureIcon`, etc.), icon callable (`icons.gcp.*`), `CustomIcon`, `Dimage`, `PIL.Image.Image`, or file path (`str` / `Path`). |
| `icon_size` | `float` | `8.0` | Rendered width/height of the icon or image inside the card. |
| `style` | `Style \| None` | `None` | Optional style override for the icon tint/fill (falls back to `d.node_style`). |
| `text_style` | `Style \| None` | `None` | Optional typography style override for the label (supports `xy_shift`, `angle`). |
| `card_style` | `Style \| None` | `None` | Optional background/border style override for this node card (falls back to `d.node_card_style`). |
| `show` | `bool` | `True` | Visibility flag (when `False`, hides this node and its incident edges while preserving layout). |

- **Center-Anchored Coordinates**: Passing `xy=(cx, cy)` to `d.add(node, xy)` or `group.add(node, xy)` places the **center** of the `(width, height)` node card at `(cx, cy)`. When both `icon` and `text` are present, the icon is positioned in the upper portion and the text label in the lower portion of the card.
- **`node.connect(target, label="", arrow="->", routing="orthogonal", style=None, padding=0.0, show=True) -> Edge`**:
  Connects this node to `target` and registers the edge on the parent diagram.
  *(Note: `node.connect()`, `group.connect()`, and `junction.connect()` do **not** accept `text_style` directly; to customize edge label typography, either use `d.connect(..., text_style=...)`, pass `Edge(..., text_style=...)` to `d.add_edge()`, or chain `.set_text_style(style)` on the returned `Edge`.)*
- **`node.fork(targets, at_x=None, at_y=None, style=None, padding=0.0, show=True) -> list[Edge]`**:
  Creates a 1-to-N orthogonal bus fan-out via an auto-created `Junction` (placed at `at_x` or `at_y`, or midpoint by default) and returns `[trunk_edge, *branch_edges]`.

---

### 2.3 `NodeGroup` (Hierarchical Boundary Container)

```python
group = NodeGroup(
    title: str = "",
    width: float | None = None,
    height: float | None = None,
    padding: float = 5.0,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | `""` | Group banner title rendered at the top-left inside the boundary (e.g. `"VPC Network"`). |
| `width` | `float \| None` | `None` | Optional fixed width override. If `None`, auto-expands to enclose all children plus `padding`. |
| `height` | `float \| None` | `None` | Optional fixed height override. If `None`, auto-expands to enclose all children plus `padding`. |
| `padding` | `float` | `5.0` | Inner margin around enclosed child nodes and nested subgroups. |
| `style` | `Style \| None` | `None` | Boundary box fill and border style (defaults to a dashed border when `None`). |
| `text_style` | `Style \| None` | `None` | Optional typography style override for `title` (falls back to `d.node_text_style`). |
| `show` | `bool` | `True` | Whether to render the group boundary box and title (`False` hides only the boundary box/title and edges attached directly to the group; child nodes remain governed by their own `.show`). |

- **Bottom-Left Local Coordinate Frame**:
  - `d.add(group, xy=(x0, y0))` places the **bottom-left corner** of `group` at `(x0, y0)`.
  - `group.add(child, xy=(lx, ly), *, show=None)` places `child` at `(lx, ly)` **relative to `group`'s bottom-left origin `(0, 0)`**:
    - If `child` is a `Node`, `(lx, ly)` is the node's local center.
    - If `child` is a nested `NodeGroup`, `(lx, ly)` is the subgroup's local bottom-left corner.
- **Connectable Boundary**: `NodeGroup` implements `Connectable` (`group.connect(target, label="", arrow="->", routing="orthogonal", style=None, padding=0.0, show=True) -> Edge` and `group.fork(...)`).

---

### 2.4 `Edge` & `Junction`

```python
edge = Edge(
    start: Connectable,
    end: Connectable,
    label: str = "",
    label_pos: float = 0.5,
    arrow: ArrowType = "->",
    routing: RoutingType = "orthogonal",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    show: bool = True,
)
```

- **Routing & Arrow Options**:
  - `routing`: `"orthogonal"` (default right-angled L/Z-bends), `"direct"` (straight Euclidean line), or `"curved"` (smooth spline).
  - `arrow`: `"->"`, `"<-"`, `"<->"`, or `"-"` (`ArrowType`).
  - `padding`: `float` (symmetric gap at both ends) or `tuple[float, float]` (`(start_pad, end_pad)`).
- **`Edge` Fluent Configuration Methods**:
  - `edge.points(waypoints: list[tuple[float, float]]) -> Self`: Sets intermediate `(x, y)` routing waypoints.
  - `edge.via(*waypoints: tuple[float, float]) -> Self`: Variadic shorthand for `.points(list(waypoints))`.
  - `edge.add_point(xy: tuple[float, float]) -> Junction`: Appends an intermediate `(x, y)` waypoint and returns a connectable `Junction` at `xy` (registered on the diagram) for tapping/branching.
  - `edge.set_label(text: str, pos: float = 0.5) -> Self`: Sets the edge label text and normalized position (`0.0` to `1.0`).
  - `edge.set_arrow(arrow: ArrowType) -> Self`: Updates arrowhead direction (`"->"`, `"<-"`, `"<->"`, `"-"`).
  - `edge.set_style(style: Style) -> Self`: Overrides line stroke style.
  - `edge.set_text_style(text_style: Style) -> Self`: Overrides edge label text style.
  - `edge.set_padding(padding: PaddingType) -> Self`: Updates boundary gap padding.
- **`Junction` Methods**:
  - `j = d.junction(xy=(x, y), *, show=True)`
  - `j.connect(target, label="", arrow="->", routing="orthogonal", style=None, padding=0.0, show=True) -> Edge`
  - `j.fork(targets, at_x=None, at_y=None, style=None, padding=0.0, show=True) -> list[Edge]`

---

## 3. Built-in Icon Catalog (33 Enums + Custom Images)

1. **Cloud Providers**: `GcpIcon` (250 Google Cloud icons), `AwsIcon` (329 AWS icons), `AzureIcon` (250 Azure icons), `CloudIcon` (45 cloud/VPS/PaaS brand logos).
2. **Domain Technology Suites**: `AiIcon` (60 AI/LLM/Agent icons), `CnativeIcon` (73 K8s/CNCF icons), `CodeIcon` (97 language/framework/IDE icons), `DataIcon` (70 database/data platform icons), `DevopsIcon` (58 CI/CD/IaC/Observability icons), `NetworkIcon` (70 CDN/DNS/Cisco topology icons), `SecurityIcon` (74 security vendor/OSS icons), `ServerIcon` (82 OS/hardware/Dell/VMware icons), `FacilityIcon` (49 datacenter/carrier/hardware icons), `BusinessIcon` (48 ERP/CRM/FinTech icons), `ClientIcon` (60 browser/OS/device icons), `ItserviceIcon` (44 GSI/consulting/SIer icons), `SocialIcon` (50 social/community/analytics icons), `WorkspaceIcon` (40 collaboration/office SaaS icons).
3. **Drawlib Vendor-Neutral Pastel Suites (`Original*Icon`)**: `OriginalAiIcon`, `OriginalBusinessIcon`, `OriginalClientIcon`, `OriginalCloudIcon`, `OriginalCnativeIcon`, `OriginalCodeIcon`, `OriginalDataIcon`, `OriginalDevopsIcon`, `OriginalFacilityIcon`, `OriginalItserviceIcon`, `OriginalNetworkIcon`, `OriginalSecurityIcon`, `OriginalServerIcon`, `OriginalSocialIcon`, `OriginalWorkspaceIcon`.
4. **General Vector UI Icons & Custom Images**: `PhosphorIcon` (1,531 monochrome UI icons, tinted by `node.style` / `d.node_style`), `CustomIcon(image)`, `Dimage`, `PIL.Image.Image`, or file path strings.

---

## 4. Production Examples

### Example 4.1: Multi-Tier Cloud VPC Network with Nested Subnets & `fork()`
```drawlib align=center code=fold file=arch_multi_tier_vpc.png caption="Production Multi-Tier Cloud VPC"
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

# Outer VPC Network boundary (bottom-left at (32, 8))
vpc = d.add(NodeGroup(title="VPC Network (10.0.0.0/16)", padding=7.0), xy=(32.0, 8.0))

# Public Subnet with Load Balancer (local coordinates inside vpc)
public_subnet = vpc.add(NodeGroup(title="Public Subnet (10.0.1.0/24)", padding=5.0), xy=(6.0, 6.0))
lb = public_subnet.add(
    Node("Cloud Load Balancer", width=26, height=17, icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=8.0),
    xy=(16.0, 30.0),
)

# Private Subnet with Application Pods (local coordinates inside vpc)
private_subnet = vpc.add(NodeGroup(title="Private Subnet (10.0.2.0/24)", padding=5.0), xy=(48.0, 6.0))
gke1 = private_subnet.add(
    Node("API Pod 1", width=20, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0),
    xy=(14.0, 44.0),
)
gke2 = private_subnet.add(
    Node("API Pod 2", width=20, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0),
    xy=(14.0, 16.0),
)

# External Actor and Managed Services (global diagram coordinates outside vpc)
user = d.add(Node("Client User", width=18, height=16, icon=PhosphorIcon.USER, icon_size=8.0), xy=(9.0, 44.0))
db = d.add(
    Node("Cloud SQL\n(PostgreSQL)", width=24, height=18, icon=GcpIcon.CLOUD_SQL, icon_size=8.0, card_style=Styles.PrimaryNeutral),
    xy=(140.0, 58.0),
)
storage = d.add(
    Node("Cloud Storage\n(Assets)", width=24, height=18, icon=GcpIcon.CLOUD_STORAGE, icon_size=8.0),
    xy=(140.0, 30.0),
)

# Connections & 1-to-N Bus Fan-Out
d.connect(user, lb, label="HTTPS (443)", padding=1.5)
lb.fork([gke1, gke2], at_x=73.0, padding=1.5)
d.connect(gke1, db, label="SQL Query", padding=1.5)
d.connect(gke2, storage, label="Asset Sync", padding=1.5)

d.draw(xy=(4.0, 4.0))
canvas.save()
```

### Example 4.2: Custom Waypoint Routing (`.via()`, `.add_point()`, `set_text_style()`)
```drawlib align=center code=fold file=arch_waypoint_routing.png caption="Event Streaming Topology with Edge Tap & Waypoints"
from drawlib import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, DataIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=136, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Event-Driven Streaming Topology",
)

cluster = d.add(NodeGroup(title="Kafka Streaming Mesh", padding=5.0), xy=(32.0, 10.0))
broker = cluster.add(Node("Kafka Broker", width=22, height=16, icon=DataIcon.KAFKA, icon_size=7.5), xy=(16.0, 28.0))

producer = d.add(Node("Ingest API", width=20, height=16, icon=PhosphorIcon.BROADCAST, icon_size=7.5), xy=(10.0, 38.0))
consumer = d.add(Node("Analytics Worker", width=24, height=16, icon=PhosphorIcon.CHART_BAR, icon_size=7.5), xy=(108.0, 50.0))
dlq = d.add(
    Node("Dead Letter Queue", width=24, height=16, icon=PhosphorIcon.WARNING_CIRCLE, icon_size=7.5, card_style=Styles.DangerNeutral),
    xy=(108.0, 20.0),
)

# Connect producer -> broker and tap into the stream via add_point()
d.connect(producer, broker, label="Produce", padding=1.5)
main_stream = broker.connect(consumer, label="Consume", padding=1.5).set_text_style(Styles.PrimaryBold)
tap = main_stream.add_point((78.0, 38.0))
tap.connect(dlq, label="Failed Retry", style=Styles.Danger, padding=1.5).set_text_style(Styles.Danger)

d.draw(xy=(4.0, 4.0))
canvas.save()
```
