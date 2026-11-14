# 9. Cloud & System Architecture Diagrams

Distributed systems are defined by trust boundaries, network topologies, and service dependencies. `drawlib.diagrams.architecture` turns cloud infrastructure blueprints into clean, version-controlled Python code—combining hierarchical `NodeGroup` containers, 33 built-in vendor & vector icon enums (`GcpIcon`, `AwsIcon`, `AzureIcon`, `PhosphorIcon`), smart boundary edge routing, and spaghetti-free `junction()` buses.

```drawlib align=center code=fold file=cloud_vpc_architecture.png caption="Figure 9.1: Production Cloud VPC Topology with External Client, Focal API Gateway, Junction Fan-Out, and Data Tier"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.styles import Styles

setup(width=160, height=74)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.White,
)

# External actor stays OUTSIDE the Cloud Region / VPC boundary
client = d.add(
    Node(
        "Web & Mobile\nClients",
        width=25.0,
        height=18.5,
        icon=PhosphorIcon.DEVICES,
        icon_size=6.0,
        card_style=Styles.Neutral.patch(shape_r=2.0),
    ),
    xy=(14.5, 30.0),
)

# Cloud Region / VPC boundary (Bottom-Left at (41, 2) in diagram coordinates)
vpc = d.add(
    NodeGroup(
        title="Google Cloud Region — Production VPC (us-central1)",
        width=109.0,
        height=62.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.4),
        text_style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
    ),
    xy=(41.0, 2.0),
)

# Focal Ingress Gateway (local center relative to vpc bottom-left)
gateway = vpc.add(
    Node(
        "API Gateway\n(Ingress)",
        width=23.0,
        height=19.0,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=6.0,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.0),
    ),
    xy=(16.5, 28.0),
)

# Application Services inside VPC (White cards + official GcpIcon)
auth_svc = vpc.add(
    Node(
        "Auth Service\n(Cloud Run)",
        width=24.0,
        height=16.5,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(52.5, 40.5),
)
order_svc = vpc.add(
    Node(
        "Order API\n(Cloud Run)",
        width=24.0,
        height=16.5,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(52.5, 15.5),
)

# Nested Data Tier NodeGroup (local bottom-left inside vpc)
data_tier = vpc.add(
    NodeGroup(
        title="Data Tier (Private)",
        width=34.0,
        height=52.5,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    ),
    xy=(71.0, 3.5),
)
sql_db = data_tier.add(
    Node(
        "Cloud SQL\n(Primary DB)",
        width=26.0,
        height=16.5,
        icon=GcpIcon.CLOUD_SQL,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(17.0, 37.0),
)
cache_db = data_tier.add(
    Node(
        "Memorystore\n(Redis Cache)",
        width=26.0,
        height=16.5,
        icon=GcpIcon.MEMORYSTORE,
        icon_size=6.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(17.0, 12.0),
)

# External HTTPS ingress + clean Junction fan-out bus
d.connect(
    client,
    gateway,
    label="HTTPS",
    routing="direct",
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_shift=(-2.0, 2.6)),
)

j_mid = d.junction((75.0, 30.0))
j_top = d.junction((75.0, 42.5))
j_bot = d.junction((75.0, 17.5))
d.connect(gateway, j_mid, arrow="-", routing="direct", padding=(1.0, 0.0))
d.connect(j_mid, j_top, arrow="-", routing="direct")
d.connect(j_mid, j_bot, arrow="-", routing="direct")
d.connect(j_top, auth_svc, arrow="->", routing="direct", padding=(0.0, 1.0))
d.connect(j_bot, order_svc, arrow="->", routing="direct", padding=(0.0, 1.0))

d.connect(auth_svc, sql_db, arrow="->", routing="direct", padding=1.0)
d.connect(order_svc, cache_db, arrow="<->", routing="direct", padding=1.0)

d.draw(xy=(4.0, 4.0))
save()
```

## 9.1 `ArchitectureDiagram`, `Node` & Coordinate Semantics

`ArchitectureDiagram` acts as the top-level container and establishes a **three-tier style cascade** (*Element Override -> Diagram Default -> Built-in Fallback*). Its four required keyword-only defaults—`node_style`, `node_text_style`, `edge_style`, and `edge_text_style`—plus optional `node_card_style` keep typography and stroke weights uniform across dozens of microservices without repeating style kwargs on every node.

Understanding how `d.add(..., xy=...)` and `group.add(..., xy=...)` interpret `xy` prevents off-by-half-width placement bugs:

| Registration Call | Anchor Point of `xy` | Coordinate Frame | Global Diagram Position Formula |
| :--- | :--- | :--- | :--- |
| **`d.add(Node(...), xy=(cx, cy))`** | **Center** `(cx, cy)` | Global diagram space | `(cx, cy)` |
| **`d.add(NodeGroup(...), xy=(x0, y0))`** | **Bottom-Left** `(x0, y0)` | Global diagram space | Bottom-Left at `(x0, y0)` |
| **`group.add(Node(...), xy=(lx, ly))`** | **Center** `(lx, ly)` | **Local** to `group` `(0, 0)` | `(x0 + lx, y0 + ly)` |
| **`group.add(NodeGroup(...), xy=(lx0, ly0))`** | **Bottom-Left** `(lx0, ly0)` | **Local** to `group` `(0, 0)` | Bottom-Left at `(x0 + lx0, y0 + ly0)` |
| **`d.junction((jx, jy))`** | **Exact Point** `(jx, jy)` | Global diagram space | `(jx, jy)` |

### 9.1.1 Pairing Official Cloud & Monochrome Icons with Card Contrast

- **Multi-Color Cloud & Domain Icons (`GcpIcon`, `AwsIcon`, `AzureIcon`, `DataIcon`, `CnativeIcon`, etc.)**: Render `512x512` official RGBA artwork. Place them on `Styles.White` or light `Styles.Neutral` cards (`card_style=Styles.White.patch(shape_r=1.8)`) so brand colors stay crisp and legible.
- **Focal Hero Nodes (`Styles.PrimaryFlat` / `Styles.AccentFlat`)**: Reserve saturated card fills for 1–2 architectural focal points (such as an Ingress Gateway or Event Router), and pair them with monochrome `PhosphorIcon` glyphs tinted via `style=Styles.WhiteBold` and `text_style=Styles.WhiteBold`.

## 9.2 Network Boundaries with `NodeGroup` & External Actor Rule

`NodeGroup` models hierarchical boundaries—Cloud Regions, VPCs, Availability Zones, Kubernetes Clusters, Public/Private Subnets, and Data Tiers. Groups can either **auto-size** around their children via `padding: float = 5.0` (when `width=None, height=None`) or lock to explicit `width` and `height` dimensions for crisp multi-tier grid alignment.

> **Architectural Boundary Rule — Keep External Actors Outside the Cloud `NodeGroup`**: Never place end users, mobile apps, browsers, or third-party SaaS webhooks *inside* your Cloud Region or VPC `NodeGroup`. Register external actors in global diagram space via `d.add(Node(...), xy=...)` on the left or top perimeter, and route them across the `NodeGroup` border into an explicit edge/ingress node (CDN, Load Balancer, or API Gateway).

## 9.3 Edge Routing, Bidirectional Arrows & `junction()` Fan-Out Buses

`d.connect(start, end, ...)` (as well as `node.connect(...)` and `Edge(...)`) connects any `Node`, `NodeGroup`, or `Junction` while automatically clipping arrows cleanly at outer bounding boxes:

- **Three Routing Modes (`routing`)**:
  - `"orthogonal"` *(default)*: Right-angled Manhattan L-bends and Z-bends between service tiers.
  - `"direct"`: Straight Euclidean segments for aligned horizontal/vertical flows or bus trunks.
  - `"curved"`: Smooth curved arcs/splines (steerable via `.via((x, y))`) ideal for async callbacks or replication paths.
- **Boundary Attachment, Padding & Arrows**: Endpoints automatically select the closest boundary side toward the target or first `.via((x, y))` waypoint. Use `padding=1.0` (or asymmetric `padding=(1.0, 0.0)`) for crisp breathing room, `arrow="<->"` for bidirectional read/write cache links, and `xy_shift=(dx, dy)` on `edge_text_style` so labels never collide with line strokes.
- **Spaghetti-Free Fan-Out Buses (`d.junction(xy)`, `node.fork()`, `edge.add_point()`)**: Instead of drawing N diagonal lines from a gateway to N downstream workers, route a single `"direct"` trunk (`arrow="-"`) into shared `d.junction((x, y))` waypoints (or call `gateway.fork([svc1, svc2], at_x=...)`).

```drawlib align=center code=fold file=routing_and_junctions.png caption="Figure 9.2: Clean Connection Patterns — Direct, Orthogonal, Curved Edges, and a Junction Fan-Out Bus"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.styles import Styles

setup(width=160, height=70)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.2),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.White,
)

# Left Panel: 3 Edge Routing Modes
left = d.add(
    NodeGroup(
        title="Edge Routing Modes (direct / orthogonal / curved)",
        width=72.0,
        height=58.0,
        style=Styles.Neutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(2.0, 2.0),
)
a1 = left.add(Node("Edge LB", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(13.5, 43.0))
b1 = left.add(Node("Auth Pod", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(58.5, 43.0))
d.connect(
    a1,
    b1,
    label='direct ("<->")',
    arrow="<->",
    routing="direct",
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, text_bg_fill_color=None, xy_shift=(0.0, 2.8)),
)

a2 = left.add(Node("API Pod", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(13.5, 28.5))
b2 = left.add(Node("SQL Read", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(58.5, 22.5))
d.connect(
    a2,
    b2,
    label="orthogonal",
    arrow="->",
    routing="orthogonal",
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, text_bg_fill_color=None, xy_shift=(6.5, 5.8)),
)

a3 = left.add(Node("Producer", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(13.5, 10.5))
b3 = left.add(Node("Consumer", width=19.0, height=10.5, card_style=Styles.White.patch(shape_r=1.6)), xy=(58.5, 10.5))
e_curved = d.connect(
    a3,
    b3,
    label="curved (async)",
    arrow="->",
    routing="curved",
    style=Styles.SecondaryBold.patch(line_style="dashed"),
    padding=1.0,
    text_style=Styles.DarkBold.patch(text_size=10.0, text_bg_fill_color=None, xy_shift=(2.5, 5.2)),
)
e_curved.via((28.0, 10.4), (33.0, 8.6), (38.0, 7.8), (43.0, 8.6), (48.0, 10.4))

# Right Panel: Junction 1-to-3 Fan-Out Bus
right = d.add(
    NodeGroup(
        title="Spaghetti-Free Bus Fan-Out via junction()",
        width=72.0,
        height=58.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(78.0, 2.0),
)
router = right.add(
    Node(
        "Event\nRouter",
        width=21.0,
        height=17.0,
        icon=PhosphorIcon.GIT_BRANCH,
        icon_size=5.6,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=1.8),
    ),
    xy=(14.5, 26.5),
)
w1 = right.add(
    Node("Billing Worker", width=25.0, height=11.5, card_style=Styles.White.patch(shape_r=1.6)),
    xy=(55.0, 42.5),
)
w2 = right.add(
    Node("Search Indexer", width=25.0, height=11.5, card_style=Styles.White.patch(shape_r=1.6)),
    xy=(55.0, 26.5),
)
w3 = right.add(
    Node("Audit Archive", width=25.0, height=11.5, card_style=Styles.SecondaryNeutral.patch(shape_r=1.6)),
    xy=(55.0, 10.5),
)

jb_mid = d.junction((112.0, 28.5))
jb_top = d.junction((112.0, 44.5))
jb_bot = d.junction((112.0, 12.5))
d.connect(router, jb_mid, arrow="-", routing="direct", padding=(1.0, 0.0))
d.connect(jb_mid, jb_top, arrow="-", routing="direct")
d.connect(jb_mid, jb_bot, arrow="-", routing="direct")
d.connect(jb_top, w1, arrow="->", routing="direct", padding=(0.0, 1.0))
d.connect(jb_mid, w2, arrow="->", routing="direct", padding=(0.0, 1.0))
d.connect(jb_bot, w3, arrow="->", routing="direct", padding=(0.0, 1.0))

d.draw(xy=(4.0, 4.0))
save()
```

For standard 1-to-N orthogonal fan-outs or dead-letter stream taps, `node.fork(targets, at_x=...)` and `edge.add_point((x, y))` create and wire `Junction` waypoints in a single method call:

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, PhosphorIcon
from drawlib.styles import Styles

setup(width=124, height=54)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.2),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

lb = d.add(
    Node(
        "Ingress LB",
        width=24.0,
        height=16.0,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=5.8,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=1.8),
    ),
    xy=(20.0, 25.0),
)
pod_a = d.add(Node("Worker A", width=24.0, height=15.0, icon=GcpIcon.CLOUD_RUN, icon_size=5.8), xy=(84.0, 36.0))
pod_b = d.add(Node("Worker B", width=24.0, height=15.0, icon=GcpIcon.CLOUD_RUN, icon_size=5.8), xy=(84.0, 14.0))

# Auto-creates a shared Junction at x=52.0 and fans out cleanly to both pods
lb.fork([pod_a, pod_b], at_x=52.0, padding=1.2)

d.draw(xy=(6.0, 2.0))
save()
```

Explore all 33 architecture icon enums and advanced waypoint APIs via `uv run drawlib rules show lib-diagrams-architecture` and `uv run drawlib rules show lib-icons-overview`.
