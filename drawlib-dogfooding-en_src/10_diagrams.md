# Chapter 10: Technical Diagrams (Architecture & System Design)

`drawlib.diagrams` is the top-level module for rendering distributed architectures, microservices, and network topologies using engineering-standard notations.

## 10.1 Cloud Architecture Diagrams (`ArchitectureDiagram`)

Easily define boundary groups (`NodeGroup`), cloud service nodes (`Node`), and orthogonal routing connections:

```drawlib 640px center file:fig_architecture_diagram.png caption:"Figure 10.1: Cloud Microservices Architecture Topology"
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=115, height=65)

diag = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.DarkBold,
    title="Cloud Microservices Architecture",
)

# VPC Boundary Group
vpc = diag.add(
    NodeGroup(
        title="Production Cloud VPC (us-central1)",
        padding=6.0,
    ),
    xy=(32.0, 6.0),
)

# Services Inside VPC (vpc.add)
gw = vpc.add(Node("API Gateway", icon=GcpIcon.APIGEE, icon_size=7.5), xy=(12.0, 24.0))
auth = vpc.add(Node("Auth Service", icon=GcpIcon.SECURITY_COMMAND_CENTER, icon_size=7.5), xy=(38.0, 36.0))
order = vpc.add(Node("Order Service", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.5), xy=(38.0, 12.0))
db = vpc.add(Node("Cloud SQL\n(PostgreSQL)", icon=GcpIcon.CLOUD_SQL, icon_size=7.5), xy=(64.0, 24.0))

# External Client Node (diag.add)
client = diag.add(Node("Client User\n(Web/Mobile)", icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5), xy=(12.0, 30.0))

# Inter-Service Connections
diag.connect(client, gw, label="HTTPS (443)", padding=2.0)
diag.connect(gw, auth, label="gRPC", padding=2.0)
diag.connect(gw, order, label="gRPC", padding=2.0)
diag.connect(order, db, label="SQL Query", padding=2.0)

diag.draw(xy=(5.0, 4.0))
```

## 10.2 Other Domain Diagrams

- **`FlowDiagram`**: ISO-compliant flowcharts with decision diamonds and swimlanes.
- **`SequenceDiagram`**: Lifelines, synchronous/async messages, and `with d.loop()` condition frames.
- **`ERDiagram`**: Relational schemas with PK/FK indicators and Crow's Foot cardinalities.
- **`ClassDiagram`**: Object-oriented UML class diagrams with inheritance and composition.
- **`StateDiagram`**: Finite state machines with transition triggers and activity compartments.
