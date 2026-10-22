# Chapter 10: Technical Diagrams (Architecture & System Design)

`drawlib.diagrams` is the top-level module for rendering distributed architectures, microservices, and network topologies using engineering-standard notations.

## 10.1 Cloud Architecture Diagrams (`ArchitectureDiagram`)

Easily define boundary groups (`NodeGroup`), cloud service nodes (`Node`), and orthogonal routing connections:

```drawlib align=center file=fig_architecture_diagram.png caption="Figure 10.1: Cloud Microservices Architecture Topology"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=145, height=72)

diag = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Cloud Microservices Architecture",
    title_style=Styles.DarkBold.patch(text_size=12.0, halign="left", valign="bottom"),
)

# VPC Boundary Group
vpc = diag.add(
    NodeGroup(
        title="Production Cloud VPC (us-central1)",
        padding=5.5,
        style=Styles.MutedDashed,
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="top"),
    ),
    xy=(39.0, 5.0),
)

# Services Inside VPC (vpc.add)
gw = vpc.add(
    Node(
        "API Gateway",
        width=22,
        height=16,
        icon=PhosphorIcon.CLOUD_CHECK,
        icon_size=7.0,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=10.0),
    ),
    xy=(14.0, 23.0),
)
auth = vpc.add(
    Node("Auth Service", width=23, height=16, icon=GcpIcon.SECURITY_COMMAND_CENTER, icon_size=7.0, card_style=Styles.PrimaryNeutral),
    xy=(45.0, 34.0),
)
order = vpc.add(
    Node("Order Service", width=23, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.0, card_style=Styles.PrimaryNeutral),
    xy=(45.0, 12.0),
)
db = vpc.add(
    Node("Cloud SQL\n(PostgreSQL)", width=25, height=17, icon=GcpIcon.CLOUD_SQL, icon_size=7.0, card_style=Styles.SecondaryNeutral),
    xy=(82.0, 23.0),
)

# External Client Node (diag.add)
client = diag.add(
    Node("Client User\n(Web/Mobile)", width=21, height=17, icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.0, card_style=Styles.Neutral),
    xy=(11.0, 28.0),
)

# Inter-Service Connections
diag.connect(client, gw, label="HTTPS (443)", padding=1.5)
gw.fork([auth, order], at_x=68.0, padding=1.5)
diag.connect(order, db, label="SQL Query", padding=1.5)

diag.draw(xy=(2.0, 2.0))
save()
```

## 10.2 Auto-Layout Graph Engine (`drawlib.graph`)

When drafting complex architectures or data workflows from scratch, calculating pixel coordinates `(x, y)` for every node and boundary can strain cognitive working memory for both engineers and AI agents—a challenge known as the **Cold-Start Problem**.

Drawlib's `drawlib.graph` is a Pure-Python **coordinate and layout calculator (`get_layout()`)** with zero external binary dependencies (no Graphviz required). Rather than coupling layout calculation to a rigid renderer, it powers a clean **2-Step Workflow**: solve coordinates in Step 1 (`layout = g.get_layout()`), then render with `drawlib.diagrams` or `drawlib.shapes` in Step 2:

```drawlib align=center file=fig_architecture_graph.png caption="Figure 10.2: 2-Step Auto-Layout with ArchitectureGraph.get_layout() and ArchitectureDiagram"
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

setup(width=192, height=84)

# Step 1: Solve cluster bounds and node coordinates with ArchitectureGraph
g = ArchitectureGraph(direction="LR", container_sep=14.0, default_node_width=24.0, default_node_height=15.0)
g.cluster("external", ["client"], pos="left", padding=4.5)
g.group("vpc", pos="center", padding=4.5)
g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1, padding=4.5)
g.cluster("data_tier", ["db", "cache"], parent="vpc", order=2, padding=4.5)

g.edge("client", "api")
g.edge("api", "worker")
g.edge("worker", "db")
g.edge("worker", "cache")

layout = g.get_layout(margin=6.0)

# Step 2: Pass solved coordinates (bottom_left, local_bottom_left, local_xy) to ArchitectureDiagram
d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

group_title_style = Styles.DarkBold.patch(text_size=10.5, halign="left", valign="top")
ext = d.add(
    NodeGroup(title="External Client", padding=4.5, style=Styles.MutedDashed, text_style=group_title_style),
    xy=layout["external"].bottom_left,
)
vpc = d.add(
    NodeGroup(title="Cloud VPC (us-central1)", padding=4.5, style=Styles.MutedDashed, text_style=group_title_style),
    xy=layout["vpc"].bottom_left,
)
app = vpc.add(
    NodeGroup(title="Application Tier", padding=4.5, style=Styles.PrimaryNeutral, text_style=group_title_style),
    xy=layout["app_tier"].local_bottom_left,
)
data = vpc.add(
    NodeGroup(title="Data Tier", padding=4.5, style=Styles.SecondaryNeutral, text_style=group_title_style),
    xy=layout["data_tier"].local_bottom_left,
)

client = ext.add(Node("Web / Mobile", width=24, height=15, icon=PhosphorIcon.DEVICES), xy=layout["client"].local_xy)
api = app.add(
    Node(
        "API Gateway",
        width=24,
        height=15,
        icon=PhosphorIcon.CLOUD_CHECK,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
    ),
    xy=layout["api"].local_xy,
)
worker = app.add(Node("Async Worker", width=24, height=15, icon=GcpIcon.CLOUD_RUN), xy=layout["worker"].local_xy)
db = data.add(Node("Primary DB", width=24, height=15, icon=GcpIcon.CLOUD_SQL), xy=layout["db"].local_xy)
cache = data.add(Node("Redis Cache", width=24, height=15, icon=GcpIcon.MEMORYSTORE), xy=layout["cache"].local_xy)

d.connect(client, api, label="HTTPS")
d.connect(api, worker)
worker.fork([db, cache], at_x=136.0)

d.draw()
save()
```

### The 2-Step Workflow (`get_layout()` & `print(layout)`)
- **Step 1 — Solve & Inspect (`layout = g.get_layout()`)**: Computes node centers (`.xy`, `.local_xy`), cluster bounds (`.bottom_left`, `.local_bottom_left`, `.size`), and edge waypoints (`.points`). Call `print(layout)` to inspect the coordinate table for manual scripts, or call `layout.offset("api", dy=-4.0)` to fine-tune positions.
- **Step 2 — Render with Rich Components (`drawlib.diagrams` / `drawlib.shapes`)**: Pass the solved coordinates into `ArchitectureDiagram`, `FlowDiagram`, or `drawlib.shapes` / `drawlib.lines` for full control over icons, styles, and connectors.

### 5 Specialized Layout Solvers
- **`ArchitectureGraph`**: Multi-tier architecture, VPC/subnet boundary nesting, and 5-zone compass positioning (`left`, `right`, `top`, `bottom`, `center`).
- **`LayerGraph`**: Sugiyama-style hierarchical DAGs for pipelines, dataflows, and dependency graphs (`.tier()`).
- **`TreeGraph`**: Reingold-Tilford symmetrical tree layout for org charts, taxonomies, and ASTs (`.child()`).
- **`RadialGraph`**: Concentric ring layouts for hub-and-spoke and event-driven architectures (`.spoke()`, `layout.ring_radii`).
- **`GridGraph`**: 2D matrix grids with orthogonal channel routing for service catalogs (`.cell()`, `.cluster_row()`).

## 10.3 Other Domain Diagrams

- **`FlowDiagram`**: ISO-compliant flowcharts with decision diamonds and swimlanes.
- **`SequenceDiagram`**: Lifelines, synchronous/async messages, and `with d.loop()` condition frames.
- **`ERDiagram`**: Relational schemas with PK/FK indicators and Crow's Foot cardinalities.
- **`ClassDiagram`**: Object-oriented UML class diagrams with inheritance and composition.
- **`StateDiagram`**: Finite state machines with transition triggers and activity compartments.
