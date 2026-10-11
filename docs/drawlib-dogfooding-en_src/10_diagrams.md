# Chapter 10: Technical Diagrams (Architecture & System Design)

`drawlib.diagrams` is the top-level module for rendering distributed architectures, microservices, and network topologies using engineering-standard notations.

## 10.1 Cloud Architecture Diagrams (`ArchitectureDiagram`)

Easily define boundary groups (`NodeGroup`), cloud service nodes (`Node`), and orthogonal routing connections:

```drawlib 640px center file:fig_architecture_diagram.png caption:"Figure 10.1: Cloud Microservices Architecture Topology"
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=155, height=78)

diag = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    node_text_style=Styles.Black,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Black,
    node_card_style=Styles.Neutral,
    title="Cloud Microservices Architecture",
)

# VPC Boundary Group
vpc = diag.add(
    NodeGroup(
        title="Production Cloud VPC (us-central1)",
        padding=6.0,
    ),
    xy=(40.0, 6.0),
)

# Services Inside VPC (vpc.add)
gw = vpc.add(Node("API Gateway", width=22, height=16, icon=GcpIcon.APIGEE, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(15.0, 26.0))
auth = vpc.add(Node("Auth Service", width=24, height=16, icon=GcpIcon.SECURITY_COMMAND_CENTER, icon_size=7.5), xy=(48.0, 38.0))
order = vpc.add(Node("Order Service", width=24, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.5), xy=(48.0, 14.0))
db = vpc.add(Node("Cloud SQL\n(PostgreSQL)", width=26, height=17, icon=GcpIcon.CLOUD_SQL, icon_size=7.5), xy=(90.0, 26.0))

# External Client Node (diag.add)
client = diag.add(Node("Client User\n(Web/Mobile)", width=22, height=17, icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5), xy=(13.0, 32.0))

# Inter-Service Connections
diag.connect(client, gw, label="HTTPS (443)", padding=1.5)
gw.fork([auth, order], at_x=71.0, padding=1.5)
diag.connect(order, db, label="SQL Query", padding=1.5)

diag.draw(xy=(3.0, 3.0))
```

## 10.2 Auto-Layout Graph Engine (`drawlib.graph`)

When drafting complex architectures or data workflows from scratch, calculating pixel coordinates `(x, y)` for every node and boundary can strain cognitive working memory for both engineers and AI agents—a challenge known as the **Cold-Start Problem**.

Drawlib provides a Pure-Python declarative graph layout engine via `drawlib.graph`. Without requiring external binaries (like Graphviz), it computes tidy orthogonal routes and nested cluster bounds automatically:

```drawlib 640px center file:fig_architecture_graph.png caption:"Figure 10.2: Auto-Layout and Cluster Packing with ArchitectureGraph"
from drawlib.canvas import setup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=195, height=80)

g = ArchitectureGraph(direction="LR", default_node_width=26.0, default_node_height=13.0)

ts_hero = Styles.WhiteBold.patch(text_size=9.5)
ts_body = Styles.Dark.patch(text_size=9.0)

# External client (pinned to the left compass zone)
g.cluster("external", ["client"], label="External Client", pos="left", padding=4.0)
g.node("client", "Web / Mobile\nClient", style=Styles.Neutral, text_style=ts_body)

# Cloud VPC (central group container)
g.group("vpc", "Cloud VPC (us-central1)", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], label="Application Tier", parent="vpc", order=1, padding=4.0)
g.cluster("data_tier", ["db", "cache"], label="Data Tier", parent="vpc", order=2, padding=4.0)

g.node("api", "API Gateway", style=Styles.PrimaryFlat, text_style=ts_hero)
g.node("worker", "Async Worker", style=Styles.SecondaryNeutral, text_style=ts_body)
g.node("db", "Primary DB", style=Styles.Neutral, text_style=ts_body)
g.node("cache", "Redis Cache", style=Styles.Neutral, text_style=ts_body)

# Edge connections (orthogonal routing)
g.edge("client", "api", label="HTTPS")
g.edge("api", "worker", label="Queue")
g.edge("api", "cache", label="Get/Set")
g.edge("worker", "db", label="Write")

g.draw(margin=8)
```

### From Draft to Finished Illustration (`export_code()`)
- `g.draw()`: Immediately computes coordinates and draws the topology to canvas.
- `g.export_code()`: Generates self-contained Drawlib Python code with calculated coordinates baked in as semantic variables (e.g., `api_xy = (72.0, 42.0)`). This enables an ideal **two-stage workflow**: *draft rapidly with auto-layout, then fine-tune critical elements with absolute coordinates*.

### 5 Specialized Layout Solvers
- **`ArchitectureGraph`**: Multi-tier architecture, VPC/subnet boundary nesting, and 5-zone compass positioning (`left`, `right`, `top`, `bottom`, `center`).
- **`LayerGraph`**: Sugiyama-style hierarchical DAGs for pipelines, dataflows, and dependency graphs.
- **`TreeGraph`**: Reingold-Tilford symmetrical tree layout for org charts, taxonomies, and ASTs.
- **`RadialGraph`**: Concentric ring layouts for hub-and-spoke and event-driven architectures.
- **`GridGraph`**: 2D matrix grids with orthogonal channel routing for service catalogs.

## 10.3 Other Domain Diagrams

- **`FlowDiagram`**: ISO-compliant flowcharts with decision diamonds and swimlanes.
- **`SequenceDiagram`**: Lifelines, synchronous/async messages, and `with d.loop()` condition frames.
- **`ERDiagram`**: Relational schemas with PK/FK indicators and Crow's Foot cardinalities.
- **`ClassDiagram`**: Object-oriented UML class diagrams with inheritance and composition.
- **`StateDiagram`**: Finite state machines with transition triggers and activity compartments.
