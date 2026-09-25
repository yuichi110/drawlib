# Drawlib Diagrams Guidelines

`drawlib.diagrams` provides a declarative, pure-Python visualization suite for software architectures, workflow flowcharts, interaction sequence diagrams, state machines, UML class hierarchies, and relational database schemas.  
Unlike external diagramming engines that depend on Graphviz, PlantUML, or opaque automatic layout solvers, Drawlib diagrams offer deterministic coordinate control, native vector drawing primitives, seamless icon library integration, and direct styling via Drawlib's `Style`, `Colors`, and `Font` systems.

---

## 1. Overview & Architecture

### 1.1 Philosophy: Illustration-as-Code for Technical Systems
Drawlib diagrams are designed for engineers and architects who require exact visual presentation:
1. **Explicit, Deterministic Layout**: Rather than fighting heuristic layout algorithms that rearrange diagrams when text changes, Drawlib gives you precise coordinate control while automatically handling boundary clipping, line offsets, and arrow alignments.
2. **First-Class Connectables**: Nodes, entities, classes, boundaries, and junctions implement a unified `Connectable` interface, enabling effortless connections between any diagram components.
3. **Rich Icon Ecosystem**: Built-in support for 259 official Google Cloud Platform (`GcpIcon`) icons, 1,531 Phosphor (`PhosphorIcon`) icons, and custom images (`CustomIcon`).
4. **Context-Aware Routing**: Smart orthogonal routing (with L-bends and Z-bends), direct straight lines with boundary clipping, and curved transition arcs.

### 1.2 Module Structure & Imports
Domain diagram modules are organized under `drawlib.diagrams`:

```python
from drawlib.diagrams import (
    ArchitectureDiagram,
    ClassDiagram,
    ERDiagram,
    FlowDiagram,
    SequenceDiagram,
    StateDiagram,
    architecture,
    class_diagram,
    er,
    flow,
    sequence,
    state_diagram,
)
```

### 1.3 Diagram Family Taxonomy

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            drawlib.diagrams Taxonomy                             │
├──────────────────────────┬────────────────────────────┬──────────────────────────┤
│ System & Architecture    │ Behavior & Process         │ Structural & Data Models │
├──────────────────────────┼────────────────────────────┼──────────────────────────┤
│ • ArchitectureDiagram    │ • FlowDiagram              │ • ClassDiagram           │
│   - Microservices        │   - ISO 5807 Flowcharts    │   - UML 2.0 Classes      │
│   - Cloud VPCs & Subnets │   - Cross-Lane Swimlanes   │   - 6 UML Relationships  │
│   - Waypoints & Bus Lines│ • SequenceDiagram          │ • ERDiagram              │
│                          │   - Synchronous / Async    │   - IE / Crow's Foot     │
│                          │   - Condition Blocks (with)│   - Table Columns (PK/FK)│
│                          │ • StateDiagram             │   - Column Anchoring     │
│                          │   - FSM / Statecharts      │                          │
│                          │   - Arcs & Pseudo-States   │                          │
└──────────────────────────┴────────────────────────────┴──────────────────────────┘
```

---

## 2. The Universal Connection & Routing Engine

### 2.1 The `Connectable` Contract
All diagram vertices, tables, containers, and waypoints derive from or implement the `Connectable` protocol:
- **Boundary Rectangles**: Every connectable defines an outer boundary bounding box.
- **Edge Anchor Calculation**: When two connectables are linked, the line intersection points are computed dynamically based on the requested side (`left`, `right`, `top`, `bottom`) or automatically (`auto`).
- **Boundary Padding**: Connection endpoints can be offset from boundaries using `padding=float` or `padding=(start_pad, end_pad)` to create clean visual gaps before arrowheads.

```text
       Source Node                                Target Node
    ┌──────────────┐      Orthogonal Edge      ┌──────────────┐
    │              ├───────────┐               │              │
    │  (cx1, cy1)  │           └──────────────►│  (cx2, cy2)  │
    │              │  padding                  │              │
    └──────────────┘                           └──────────────┘
```

### 2.2 Routing Strategies & Visual Geometries
1. **`routing="orthogonal"`** (Default for Architecture, Flow, Class, and ER):
   Computes clean right-angled Z-bends and L-bends. Avoids overlapping node bounding boxes when possible.
2. **`routing="direct"`**:
   Draws a straight Euclidean line between source and target anchor points, clipping cleanly at each entity's outer boundary.
3. **`bend=float`** (Used extensively in `StateDiagram`):
   Generates a quadratic Bezier or arc curve between nodes. A positive bend curves to the left/top, while a negative bend curves to the right/bottom, allowing elegant bidirectional transitions.

```text
       Orthogonal Z-Bend                 Direct Straight                  Curved Arc (bend)
    ┌─────┐        ┌─────┐           ┌─────┐         ┌─────┐          ┌─────┐  . - ~ - .  ┌─────┐
    │  A  ├──┐     │  B  │           │  A  │────────►│  B  │          │  A  ├'           '┤  B  │
    └─────┘  └───►─┴─────┘           └─────┘         └─────┘          └─────┘             └─────┘
```

### 2.3 Attachment Sides & Padding Configuration
Sides can be specified explicitly or resolved automatically:
- **`start_side` / `end_side`**: `"left"`, `"right"`, `"top"`, `"bottom"`, or `"auto"` (default).
- **`padding`**:
  - `padding=2.0`: Symmetric 2.0-unit gap at both ends.
  - `padding=(1.0, 3.0)`: Asymmetric padding (1.0 at start, 3.0 at target).

### 2.4 Waypoints & Branching with `Junction`
A `Junction` represents a zero-dimension connectable coordinate `(x, y)` on the canvas. It enables:
- **T-Junctions**: Splitting a single bus line into multiple downstream connections.
- **Merge Points**: Combining multiple upstream error or completion paths into a common successor node.
- **Dynamic Insertion**: Calling `edge.add_point(xy)` converts an intermediate edge coordinate into a reusable `Junction`.

```python
# Create a primary data stream connection
main_edge = d.connect(producer, consumer_1, label="Raw Events", padding=2.0)

# Dynamically tap into the edge at coordinate (50.0, 50.0)
tap_junction = main_edge.add_point((50.0, 50.0))

# Branch off to an audit logger or archive pipeline
tap_junction.connect(consumer_2, label="Audit Stream", routing="orthogonal", padding=1.5)
```

---

## 3. ArchitectureDiagram: Microservices, Cloud Nodes, and Boundaries

### 3.1 Conceptual Overview
`ArchitectureDiagram` visualizes distributed systems, cloud networks, microservices topologies, and infrastructure boundaries. It pairs icon-centric nodes with automatic hierarchical boundary boxes (`NodeGroup`) and multi-way branch routing.

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

### 3.2 Constructor Parameters & Signatures

```python
from drawlib.diagrams.architecture import ArchitectureDiagram, Edge, Junction, Node, NodeGroup
from drawlib.diagrams.architecture import CustomIcon, GcpIcon, PhosphorIcon
```

#### `ArchitectureDiagram` Class:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `""` | Diagram title text rendered at top. |
| `width` / `height` | `float \| None` | `None` | Optional canvas bounding dimensions override. |
| `style` | `Style \| None` | `None` | Optional Style for container background card. |

- `d.add(item, xy) -> Node | NodeGroup`: Places a node or group.
- `d.connect(source, target, label="", routing="orthogonal", padding=0.0) -> Edge`: Creates connection edge.
- `d.draw(xy=(0.0, 0.0))`: Renders diagram at bottom-left coordinate `xy`.

#### `Node` Class:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `""` | Node label text (supports `\n`). |
| `icon` | `IconType \| None` | `None` | PhosphorIcon, GcpIcon, or CustomIcon. |
| `icon_size` | `float` | `8.0` | Outer width and height of the icon square. |
| `text_position` | `"bottom"` \| `"top"` \| `"left"` \| `"right"` | `"bottom"` | Label placement relative to icon center. |
| `style` | `Style \| None` | `None` | Optional typography or node background style. |

- **Icon-Centric Coordinates**: The coordinate `xy` passed to `d.add(node, xy)` **strictly defines the center of the icon**. The text label is positioned relative to the icon according to `text_position` without shifting the icon's position. This ensures perfectly straight wire routing between aligned icons.
- `node.fork(targets, at_x=None, at_y=None, padding=0.0)`: Creates a 1-to-N bus fan-out via an automatic intermediate junction.

#### `NodeGroup` Class:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `""` | Group banner title (e.g. `"VPC Network (10.0.0.0/16)"`). |
| `padding` | `float` | `6.0` | Inner margin around enclosed child nodes. |
| `style` | `Style \| None` | `None` | Style for group background fill and boundary border. |

- **Auto-Bounding**: Automatically computes its bounding box to enclose all child nodes and nested groups with configurable padding.
- **Group as Connectable**: You can connect directly to or from a group's boundary box.

#### Built-in Icons:
- `GcpIcon`: 259 official Google Cloud icons (`GcpIcon.COMPUTE_ENGINE`, `GcpIcon.CLOUD_RUN`, `GcpIcon.CLOUD_SQL`, `GcpIcon.BIGQUERY`, etc.).
- `PhosphorIcon`: 1,531 modern interface icons (`PhosphorIcon.USER`, `PhosphorIcon.DATABASE`, `PhosphorIcon.BROWSER`, etc.).
- `CustomIcon(image)`: Wraps file paths, PIL Images, or `Dimage` instances.

### 3.3 Production Examples

#### Example 3.3.1: Multi-Tier Cloud VPC Network
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon

canvas.initialize()
canvas.config(width=115, height=95)

d = ArchitectureDiagram(title="Production Multi-Tier Cloud VPC")

# Outer VPC Network boundary
vpc = d.add(NodeGroup(title="VPC Network (10.0.0.0/16)", padding=7.0), xy=(10.0, 8.0))

# Public Subnet with Load Balancer
public_subnet = vpc.add(NodeGroup(title="Public Subnet (10.0.1.0/24)", padding=5.0), xy=(5.0, 5.0))
lb = public_subnet.add(Node("Cloud Load Balancer", icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=8.0), xy=(15.0, 35.0))

# Private Subnet with Application Pods
private_subnet = vpc.add(NodeGroup(title="Private Subnet (10.0.2.0/24)", padding=5.0), xy=(38.0, 5.0))
gke1 = private_subnet.add(Node("API Pod 1", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0), xy=(15.0, 48.0))
gke2 = private_subnet.add(Node("API Pod 2", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0), xy=(15.0, 20.0))

# External Actor and Managed Services
user = d.add(Node("Client User", icon=PhosphorIcon.USER, icon_size=8.0), xy=(5.0, 42.0))
db = d.add(Node("Cloud SQL\n(PostgreSQL)", icon=GcpIcon.CLOUD_SQL, icon_size=8.0), xy=(85.0, 45.0))
storage = d.add(Node("Cloud Storage\n(Assets)", icon=GcpIcon.CLOUD_STORAGE, icon_size=8.0), xy=(85.0, 18.0))

# Connections
d.connect(user, lb, label="HTTPS (443)", padding=2.0)
lb.fork([gke1, gke2], at_x=42.0, padding=2.0)
d.connect(gke1, db, label="SQL Query", padding=2.0)
d.connect(gke2, db, label="SQL Query", padding=2.0)
d.connect(gke1, storage, label="Uploads", padding=2.0)

d.draw(xy=(5.0, 5.0))
```

#### Example 3.3.2: Event-Driven Kafka Streaming Mesh
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon

canvas.initialize()
canvas.config(width=105, height=75)

d = ArchitectureDiagram(title="Event-Driven Message Streaming Topology")

cluster = d.add(NodeGroup(title="Streaming Event Mesh", padding=6.0), xy=(15.0, 10.0))
broker1 = cluster.add(Node("Kafka Broker 1", icon=PhosphorIcon.STACK, icon_size=7.0), xy=(20.0, 45.0))
broker2 = cluster.add(Node("Kafka Broker 2", icon=PhosphorIcon.STACK, icon_size=7.0), xy=(20.0, 20.0))

pub = d.add(Node("Event Ingest\nProducer", icon=PhosphorIcon.BROADCAST, icon_size=7.5), xy=(5.0, 32.5))
analytics = d.add(Node("Realtime Analytics\nConsumer", icon=PhosphorIcon.CHART_BAR, icon_size=7.5), xy=(85.0, 45.0))
archiver = d.add(Node("Parquet Lakehouse\nArchiver", icon=PhosphorIcon.HARD_DRIVES, icon_size=7.5), xy=(85.0, 20.0))

pub.fork([broker1, broker2], at_x=22.0, padding=1.5)
d.connect(broker1, analytics, label="Consumer Group A", padding=1.5)
d.connect(broker2, archiver, label="Consumer Group B", padding=1.5)

d.draw(xy=(5.0, 5.0))
```

---

## 4. FlowDiagram: Standard Flowcharts and Cross-Functional Swimlanes

### 4.1 Conceptual Overview
`FlowDiagram` implements standard flowchart symbols according to ISO 5807 and JIS X 0121 standards, with support for cross-functional swimlane layouts (columns or rows) sharing a unified coordinate plane.

```text
  Lane: Customer                Lane: Gateway              Lane: Warehouse
 ┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
 │   (Start)                 │                           │                           │
 │      │                    │                           │                           │
 │      ▼                    │                           │                           │
 │ [Submit Order]───────────►│ <Payment Valid?>          │                           │
 │                           │    │           │ (No)     │                           │
 │                           │    ▼ (Yes)     ▼          │                           │
 │                           │    │        [Show Error]  │                           │
 │                           │    ▼                      │                           │
 │                           │    └─────────────────────►│ [Pack & Ship]             │
 └───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

### 4.2 Standard Symbols & Geometries
| Class | Symbol / Geometry | Shape Type | Default Size (W x H) | Standard Usage |
|---|---|---|---|---|
| `Start` | Stadium / Pill (`r=5.0`) | `"start"` | `20.0 x 10.0` | Initial entry point of the flow |
| `End` | Stadium / Pill (`r=5.0`) | `"end"` | `20.0 x 10.0` | Terminal termination point |
| `Process` | Rectangle | `"process"` | `24.0 x 12.0` | Task, execution step, or operation |
| `Decision` | Rhombus / Diamond | `"decision"`| `22.0 x 14.0` | Conditional branch (Yes/No, True/False) |
| `Data` | Parallelogram | `"data"` | `24.0 x 12.0` | Data input, output, or file I/O |
| `Junction` | Zero-Size Coordinate | `"junction"`| `0.0 x 0.0` | Wire tap, waypoint, or merge junction |
| `Lane` | Boundary Band | `"lane"` | Dynamic | Department, role, or microservice boundary |

### 4.3 Node Arguments & Geometric Styling
All flow nodes inherit from `FlowNode` and accept standard geometric customization arguments:
- `text`: Label centered inside shape (multiline supported via `\n`).
- `width` / `height`: Boundary dimensions in canvas units.
- `r`: Corner rounding radius.
- `style`: Fill color, border stroke color, line width, and line style.
- `textstyle`: Typography style for the centered text.
- `textsize`: Direct font size shortcut.

### 4.4 Swimlane Architecture & Global Coordinates
In `FlowDiagram`, swimlanes provide a structured visual background and column/row headers without trapping nodes inside isolated local coordinates.  
**All nodes share a single global canvas coordinate system.** This allows corresponding steps in different lanes to be effortlessly aligned along the exact same horizontal $Y$ coordinate:
- **Vertical Swimlanes**: `flow.add_lane(name, width=...)` stacks columns left-to-right.
- **Horizontal Swimlanes**: `flow = FlowDiagram(..., lane_orientation="horizontal")`, then `flow.add_lane(name, height=...)` stacks rows top-to-bottom.

### 4.5 Production Examples

#### Example 4.5.1: Cross-Functional Expense Approval Flow
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start

canvas.initialize()
canvas.config(width=110, height=95)

flow = FlowDiagram(title="Expense Reimbursement Approval Workflow", width=100.0, height=90.0)

# 1. Define vertical department lanes (columns from left to right)
flow.add_lane("Employee", width=30.0)
flow.add_lane("Line Manager", width=35.0)
flow.add_lane("Finance Dept", width=35.0)

# 2. Add nodes (Y coordinates align corresponding steps horizontally)
submit = flow.add(Start("Submit Claim"), xy=(15.0, 78.0))
receipt = flow.add(Data("Attach Receipt"), xy=(15.0, 62.0))
review = flow.add(Process("Review Details"), xy=(47.5, 62.0))
decision = flow.add(Decision("Amount < $500?"), xy=(47.5, 42.0))

j = flow.junction(xy=(47.5, 25.0))
auto_pay = flow.add(Process("Disburse Payment"), xy=(82.5, 25.0))
audit = flow.add(Process("Compliance Audit"), xy=(82.5, 42.0))
end = flow.add(End("Claim Closed"), xy=(15.0, 25.0))

# 3. Connect steps
submit.connect(receipt)
receipt.connect(review)
review.connect(decision)

# Decision routing
decision.connect(audit, label="No", start_side="right", end_side="left")
decision.connect(j, label="Yes", start_side="bottom", end_side="top")
j.connect(auto_pay, routing="orthogonal")
audit.connect(auto_pay, start_side="bottom", end_side="top")
auto_pay.connect(end, label="Notice Sent")

flow.draw(xy=(5.0, 5.0))
```

#### Example 4.5.2: Horizontal Warehouse Order Processing
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start

canvas.initialize()
canvas.config(width=130, height=80)

flow = FlowDiagram(title="Fulfillment Logistics Pipeline", lane_orientation="horizontal", width=115.0, height=65.0)

flow.add_lane("Sales Platform", height=32.5, header_size=22.0)
flow.add_lane("Distribution Center", height=32.5, header_size=22.0)

order = flow.add(Start("New Purchase"), xy=(36.0, 48.0))
validate = flow.add(Decision("In Stock?"), xy=(62.0, 48.0))
cancel = flow.add(End("Cancel & Refund"), xy=(92.0, 48.0))
pack = flow.add(Process("Pick & Pack"), xy=(62.0, 16.0))
dispatch = flow.add(End("Ship Carrier"), xy=(92.0, 16.0))

order.connect(validate)
validate.connect(cancel, label="No", start_side="right", end_side="left")
validate.connect(pack, label="Yes", start_side="bottom", end_side="top")
pack.connect(dispatch)

flow.draw(xy=(8.0, 5.0))
```

---

## 5. SequenceDiagram: Lifelines, Synchronous Calls, and Structured Frames

### 5.1 Conceptual Overview
`SequenceDiagram` models chronological interactions and protocols between collaborating participants over time. Time progresses strictly downwards along vertical lifelines, with horizontal arrows representing messages.

```text
    Client               API Server            Database
      │                      │                    │
      │ ──POST /login───────►│                    │
      │                      │ ──SELECT user─────►│
      │                      │                    │ █ (Activation)
      │                      │ ◄──User Record─────│
      │ ◄──200 OK (JWT)──────│                    │
      │                      │                    │
```

### 5.2 Key Classes & Message Semantics

```python
from drawlib.diagrams.sequence import Block, Message, Note, Participant, ParticipantGroup, SequenceDiagram
```

#### Constructor & Participant Management:
- `SequenceDiagram(title="", width=None, height=None, autonumber=False, style=None)`
- `d.add(Participant(name, icon=None, icon_size=8.0, style=None)) -> Participant`
- `d.add_group(ParticipantGroup(title="", padding=4.0, style=None)) -> ParticipantGroup`

#### Message Verbs:
- **`a.request(b, label, is_async=False)`**: Synchronous call rendered as a solid line with a filled arrowhead (`―▶`). If `is_async=True`, renders an open stick arrowhead (`―>`).
- **`b.reply(a, label, is_async=False)`**: Response or return value rendered as a dashed line with a filled arrowhead (`---▶`). If `is_async=True`, renders an open stick arrowhead (`--->`).
- **`a.connect(b, label, arrow="<->")`**: Bidirectional persistent communication (e.g. WebSocket connection or gRPC streaming channel).
- **`p.request(p, label)`**: Self-call loop rendered as a 3-segment orthogonal loop returning to the caller's lifeline.

#### Execution Controls:
- **Activation Boxes**: `p.activate()` and `p.deactivate()` render execution rectangles along the participant's vertical lifeline.
- **Autonumbering**: Setting `SequenceDiagram(..., autonumber=True)` automatically prepends chronological sequential numbers (`1.`, `2.`, `3.`, ...) to message labels.
- **Sticky Notes**:
  - `p.note(text, pos="left"|"right")`: Annotates a single participant's lifeline.
  - `d.note(text, over=[p1, p2])`: Spans centered across multiple lifelines.

#### Structured Condition Frames (`Block` via Python `with`):
Indented Python `with` statements naturally structure condition frames in the diagram:
- `with d.loop("Condition"):` (Loop / repeat frame)
- `with d.alt("Condition A"):` and `with d.else_("Condition B"):` (Alternative branch frame)
- `with d.opt("Condition"):` (Optional execution frame)
- `with d.par("Description"):` (Concurrent parallel steps)

### 5.3 Production Examples

#### Example 5.3.1: Microservices Order Processing Pipeline
```drawlib show-code
from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram

canvas.initialize()
canvas.config(width=115, height=135)

d = SequenceDiagram(title="Microservices Distributed Transaction Pipeline", autonumber=True)

# Participant boundary group for internal cluster
backend = d.add_group(
    ParticipantGroup(
        title="Google Cloud VPC",
        padding=4.0,
        style=Style(fill_color=(242, 246, 255, 0.4), line_color=Colors.Gray, line_style="dashed"),
    )
)
api = backend.add(Participant("Cloud Run\n(Gateway)", icon=GcpIcon.CLOUD_RUN, icon_size=8.0))
worker = backend.add(Participant("GKE Pod\n(Worker)", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0))
db = backend.add(Participant("Cloud SQL\n(Database)", icon=GcpIcon.CLOUD_SQL, icon_size=8.0))

client = d.add(Participant("Web Browser", icon=PhosphorIcon.BROWSER, icon_size=8.0))

# 1. User initiates request
client.request(api, "POST /api/v1/checkout")
api.activate()

# 2. Validation & Database query
api.request(db, "Check Inventory")
db.reply(api, "Stock Available")

# 3. Sticky Note annotation
api.note("Dispatching background fulfillment job", pos="right")

# 4. Asynchronous worker dispatch
api.request(worker, "Enqueue Job (Pub/Sub)", is_async=True)
worker.reply(api, "Ack", is_async=True)

# 5. Immediate response to client
api.reply(client, "202 Accepted (Order ID)")
api.deactivate()

# 6. Worker background processing within loop
with d.loop("Retry up to 3 times on DB lock"):
    worker.request(db, "Deduct Inventory Rows")
    db.reply(worker, "Rows Committed")

d.draw(xy=(5.0, 5.0))
```

#### Example 5.3.2: Bidirectional WebSocket Protocol Stream
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram

canvas.initialize()
canvas.config(width=65, height=80)

d = SequenceDiagram(title="WebSocket Real-Time Live Sync")

app = d.add(Participant("Mobile App", icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5))
gateway = d.add(Participant("WS Gateway", icon=PhosphorIcon.CLOUD, icon_size=7.5))

app.request(gateway, "GET /ws HTTP/1.1 (Upgrade: websocket)")
gateway.reply(app, "101 Switching Protocols")

# Bidirectional streaming channel
app.connect(gateway, "Full-Duplex JSON Telemetry Stream", arrow="<->")

with d.loop("Every 500ms Ping Interval"):
    gateway.request(app, "PING", is_async=True)
    app.reply(gateway, "PONG", is_async=True)

d.draw(xy=(5.0, 5.0))
```

---

## 6. StateDiagram: Statecharts, Finite State Automata, and Transitions

### 6.1 Conceptual Overview
`StateDiagram` models behavioral state transitions, Finite State Machines (FSM), and UML 2.0 Statecharts. It provides dedicated pseudo-states, internal action compartments (`entry`, `do`, `exit`), and curved arc transitions.

```text
    (Initial)
        │
        ▼
   ┌─────────┐      event [guard] / action
   │  Idle   ├─────────────────────────────────►┌──────────────┐
   └────▲────┘                                  │  Processing  │
        │           failure (bend=0.25)         ├──────────────┤
        └───────────────────────────────────────┤ entry/timer  │
                                                │ do/calculate │
                                                └──────────────┘
```

### 6.2 Node Shapes and Pseudo-States
`State` supports 5 distinct geometric representations via `shape`:
1. `"box"` (Default): UML rounded card with action compartment headers.
2. `"oval"`: Pill / capsule shape for high-level workflow states.
3. `"circle"`: Automaton / DFA / NFA states with transparent backgrounds.
4. `"double_circle"`: Automaton accepting or terminal states.
5. `"text_only"`: Minimalist borderless text state.

#### UML Pseudo-States:
- **`InitialState()`**: Solid filled black circle marking entry.
- **`FinalState()`**: Bullseye target (solid black dot enclosed by an outer circle).
- **`ChoiceState(name)`**: Diamond shape representing dynamic conditional branching.
- **`ForkJoinState(orientation="horizontal"|"vertical", length=20.0)`**: Solid synchronization bar for concurrent state splits and joins.

### 6.3 Action Compartments & Transition Syntax
- **Internal Actions**: Pass `entry="..."`, `do="..."`, or `exit="..."` during `State` creation, or chain with `state.add_action("custom", "...")`.
- **Transitions with `node.to(...)`**:
  ```python
  s1.to(
      s2,
      event="submit",
      guard="is_valid",
      action="save()",
      bend=0.25,  # Curved arc
  )
  ```
  Automatically formats formal UML labels: `event [guard] / action`.
- **Self-Transitions**: Call `state.loop(side="top", event="tick")` or `state.to(state, ...)`.

### 6.4 Production Examples

#### Example 6.4.1: Session Lifecycle State Machine
```python
from drawlib import canvas
from drawlib.diagrams.state_diagram import ChoiceState, FinalState, InitialState, State, StateDiagram

canvas.initialize()
canvas.config(width=135, height=75)

sd = StateDiagram(title="User Session Lifecycle State Machine")

# 1. Pseudo-states and state nodes
init = sd.add(InitialState(), xy=(12.0, 38.0))
idle = sd.add(
    State("Idle", shape="box", entry="reset_timeout()", do="listen_events()"),
    xy=(35.0, 38.0),
)
valid_check = sd.add(ChoiceState(name="Valid?"), xy=(70.0, 38.0))
active = sd.add(
    State("Active", shape="box", entry="start_heartbeat()", do="handle_requests()", exit="flush()"),
    xy=(102.0, 38.0),
)
final = sd.add(FinalState(), xy=(126.0, 38.0))

# 2. Connect transitions
init.to(idle)
idle.to(valid_check, event="login", guard="token_present")

# Choice branches (success vs failure)
valid_check.to(active, guard="token_valid")
valid_check.to(idle, guard="token_invalid", bend=0.3)

# Self-transition heartbeat loop
active.loop(side="top", event="ping", action="extend_lease()")

# Termination
active.to(final, event="logout")

sd.draw(xy=(0.0, 0.0))
```

#### Example 6.4.2: Concurrent Task Synchronization with Fork and Join
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.state_diagram import FinalState, ForkJoinState, InitialState, State, StateDiagram

canvas.initialize()
canvas.config(width=115, height=75)

sd = StateDiagram(title="Concurrent Task Fork and Join")

init = sd.add(InitialState(), xy=(10.0, 37.5))
fork = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(25.0, 37.5))
job_a = sd.add(State("Compute Analytics", shape="box"), xy=(55.0, 50.0))
job_b = sd.add(State("Index Search", shape="box"), xy=(55.0, 25.0))
join = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(85.0, 37.5))
final = sd.add(FinalState(), xy=(105.0, 37.5))

init.to(fork)
fork.to(job_a)
fork.to(job_b)
job_a.to(join)
job_b.to(join)
join.to(final)

sd.draw(xy=(0.0, 0.0))
```

---

## 7. ClassDiagram: UML 2.0 Class Hierarchies and Relationships

### 7.1 Conceptual Overview
`ClassDiagram` implements standard UML 2.0 Object-Oriented structural modeling. It features three-compartment class cards (name, attributes, methods), stereotypes, abstract classes, and all 6 standard UML relationships via intuitive verb methods.

```text
   ┌──────────────────────────┐
   │       «interface»        │
   │      PaymentService      │
   ├──────────────────────────┤
   │ + pay(amount): bool      │
   └─────────────▲────────────┘
                 ┆ (Realization: .realize())
   ┌─────────────┴────────────┐            1            * ┌──────────────────────────┐
   │      StripeService       │◆─────────────────────────►│        Transaction       │
   ├──────────────────────────┤   (Composition:           ├──────────────────────────┤
   │ - api_key: str           │    .composite())          │ - id: str                │
   ├──────────────────────────┤                           │ - amount: float          │
   │ + pay(amount): bool      │                           └──────────────────────────┘
   └──────────────────────────┘
```

### 7.2 ClassNode Configuration
- **Attributes**: `node.add_attribute(name, type, is_public=True, is_static=False, default_value="")`.
  - Symbols: `+` (public), `-` (private), `#` (protected), `~` (package).
  - Batch: `node.add_attributes([("id", "int", True), ("secret", "str", False)])`.
- **Methods**: `node.add_method(name, params="", return_type="", is_public=True, is_abstract=False, is_static=False)`.
  - Batch: `node.add_methods([("execute", "task: Task", "bool")])`.
- **Stereotypes**: `ClassNode(name="Service", stereotype="interface")` renders `«interface»`.
- **Abstract Classes**: `ClassNode(name="Entity", is_abstract=True)` renders `«abstract»`.

### 7.3 The 6 UML Relationship Verb Methods
| Verb Method | UML Relationship | Line Stroke | End Marker | Description |
|---|---|---|---|---|
| `child.inherit(parent)` | **Inheritance** | Solid | Hollow Triangle (at parent) | Superclass / Subclass Generalization |
| `impl.realize(iface)` | **Realization** | Dashed | Hollow Triangle (at iface) | Interface Implementation |
| `whole.composite(part)` | **Composition** | Solid | Filled Diamond (at whole) | Strong ownership; part dies with whole |
| `whole.aggregate(part)` | **Aggregation** | Solid | Hollow Diamond (at whole) | Shared ownership / part-whole |
| `c1.associate(c2)` | **Association** | Solid | None (or Open Arrow) | Structural reference |
| `client.depend(supplier)`| **Dependency** | Dashed | Open Arrow (at supplier) | Client depends on supplier |

All relationship methods support `start_multiplicity` (`"1"`, `"0..1"`), `end_multiplicity` (`"*"`, `"1..*"`), `start_role`, `end_role`, and `label`.

### 7.4 Production Examples

#### Example 7.4.1: E-Commerce Domain Model
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode

canvas.initialize()
canvas.config(width=110, height=85)

cd = ClassDiagram(title="E-Commerce Domain Class Model")

# 1. Define classes
user = cd.add(ClassNode(name="User", width=26.0), xy=(22.0, 60.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("email", type="str", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", return_type="bool")

customer = cd.add(ClassNode(name="Customer", width=26.0), xy=(22.0, 20.0))
customer.add_attribute("shipping_address", type="str")
customer.add_method("checkout", return_type="Order")

order = cd.add(ClassNode(name="Order", width=28.0), xy=(75.0, 20.0))
order.add_attribute("order_id", type="str")
order.add_attribute("total", type="float")
order.add_method("calculate_tax", return_type="float")

iface = cd.add(ClassNode(name="PaymentGateway", stereotype="interface", width=30.0), xy=(75.0, 60.0))
iface.add_method("process_charge", params="amount: float", return_type="bool")

# 2. Connect relationships using intuitive verbs
customer.inherit(user, start_side="top", end_side="bottom")
customer.composite(
    order,
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="places",
)
order.depend(iface, start_side="top", end_side="bottom", label="uses")

cd.draw(xy=(0.0, 0.0))
```

#### Example 7.4.2: Observer Design Pattern Implementation
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode

canvas.initialize()
canvas.config(width=105, height=80)

cd = ClassDiagram(title="UML Observer Design Pattern")

subj_iface = cd.add(ClassNode(name="Subject", stereotype="interface", width=28.0), xy=(25.0, 58.0))
subj_iface.add_method("attach", params="o: Observer", return_type="void")
subj_iface.add_method("notify", return_type="void")

obs_iface = cd.add(ClassNode(name="Observer", stereotype="interface", width=28.0), xy=(75.0, 58.0))
obs_iface.add_method("update", return_type="void")

concrete_subj = cd.add(ClassNode(name="NewsPublisher", width=28.0), xy=(25.0, 20.0))
concrete_subj.add_attribute("state", type="str", is_public=False)
concrete_subj.add_method("get_state", return_type="str")

concrete_obs = cd.add(ClassNode(name="EmailSubscriber", width=28.0), xy=(75.0, 20.0))
concrete_obs.add_method("update", return_type="void")

concrete_subj.realize(subj_iface, start_side="top", end_side="bottom")
concrete_obs.realize(obs_iface, start_side="top", end_side="bottom")
subj_iface.aggregate(
    obs_iface,
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    start_role="subject",
    end_role="observers",
)

cd.draw(xy=(0.0, 0.0))
```

---

## 8. ERDiagram: Relational Database Schemas and Crow's Foot Notations

### 8.1 Conceptual Overview
`ERDiagram` visualizes relational database architectures adhering strictly to **Information Engineering (IE) / Crow's Foot notation**—the industry standard for physical database schema modeling.

```text
     users                               orders
  ┌──────────────────────┐            ┌──────────────────────┐
  │ id          INT [PK] │──||────o<──│ id          INT [PK] │
  │ email   VARCHAR(255) │            │ user_id     INT [FK] │
  │ name    VARCHAR(100) │            │ total  DECIMAL(10,2) │
  └──────────────────────┘            └──────────────────────┘
```

### 8.2 Entity Configuration & Column Modeling
- **Primary & Foreign Keys**: `entity.add_column("id", type="INT", pk=True)` displays `[PK]`. `fk=True` displays `[FK]`.
- **Nullable**: `nullable=False` marks mandatory fields.
- **Batch Additions**:
  ```python
  entity.add_columns([
      ("user_id", "INT", False, True, False),  # (name, type, pk, fk, nullable)
      ("created_at", "TIMESTAMP"),
  ])
  ```
- **Dynamic vs Fixed Sizing**: Entities automatically calculate their height from column counts. If an explicit `height` is passed that exceeds content, the extra space is kept as a clean, blank background margin.

### 8.3 Supported Crow's Foot Cardinality Notations
| Cardinality | Parent Marker | Child Marker | Standard Semantics |
|---|---|---|---|
| `"1:*"` | Exactly 1 (`||`) | Zero or more (`o<`) | Standard One-to-Many (Default) |
| `"1:1"` | Exactly 1 (`||`) | Exactly 1 (`||`) | One-to-One |
| `"1:1..*"` | Exactly 1 (`||`) | One or more (`|<`) | Mandatory Child One-to-Many |
| `"1:0..1"` | Exactly 1 (`||`) | Zero or one (`o|`) | Optional Child One-to-One |
| `"0..1:1"` | Zero or one (`o|`) | Exactly 1 (`||`) | Optional Parent One-to-One |
| `"0..1:*"` | Zero or one (`o|`) | Zero or more (`o<`) | Optional Parent One-to-Many |
| `"*:*"` | Zero or more (`o<`) | Zero or more (`o<`) | Many-to-Many |

### 8.4 Column-Level Anchoring
By passing `start_column="col_a"` and `end_column="col_b"`, connection lines align vertically with the exact table rows of foreign and primary keys:

```python
users.connect(
    orders,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",       # Anchors to 'id' row in users
    end_column="user_id",    # Anchors to 'user_id' row in orders
    label="places",
)
```

### 8.5 Production Examples

#### Example 8.5.1: Core E-Commerce Relational Schema
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.er import ERDiagram, Entity

canvas.initialize()
canvas.config(width=115, height=85)

erd = ERDiagram(title="E-Commerce Relational Database Schema")

# 1. Define entities
users = erd.add(Entity(name="users", width=26.0), xy=(20.0, 50.0))
users.add_column("id", type="INT", pk=True)
users.add_column("email", type="VARCHAR(255)", nullable=False)
users.add_column("name", type="VARCHAR(100)")

orders = erd.add(Entity(name="orders", width=26.0), xy=(55.0, 50.0))
orders.add_column("id", type="INT", pk=True)
orders.add_column("user_id", type="INT", fk=True)
orders.add_column("total_amount", type="DECIMAL(10,2)")

items = erd.add(Entity(name="order_items", width=26.0), xy=(90.0, 50.0))
items.add_column("id", type="INT", pk=True)
items.add_column("order_id", type="INT", fk=True)
items.add_column("product_name", type="VARCHAR(100)")
items.add_column("quantity", type="INT")

# 2. Connect relationships with column anchoring
users.connect(
    orders,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="user_id",
    label="places",
)
orders.connect(
    items,
    cardinality="1:1..*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="order_id",
    label="contains",
)

erd.draw(xy=(0.0, 0.0))
```

#### Example 8.5.2: Multi-Tenant RBAC Security Schema
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.er import ERDiagram, Entity

canvas.initialize()
canvas.config(width=110, height=80)

erd = ERDiagram(title="Multi-Tenant RBAC Authorization Schema")

tenants = erd.add(Entity(name="tenants", width=24.0), xy=(20.0, 48.0))
tenants.add_column("id", type="UUID", pk=True)
tenants.add_column("slug", type="VARCHAR(64)", nullable=False)

accounts = erd.add(Entity(name="accounts", width=24.0), xy=(55.0, 48.0))
accounts.add_column("id", type="UUID", pk=True)
accounts.add_column("tenant_id", type="UUID", fk=True)
accounts.add_column("email", type="VARCHAR(128)")

roles = erd.add(Entity(name="roles", width=24.0), xy=(90.0, 48.0))
roles.add_column("id", type="UUID", pk=True)
roles.add_column("account_id", type="UUID", fk=True)
roles.add_column("role_name", type="VARCHAR(32)")

tenants.connect(
    accounts,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="tenant_id",
)
accounts.connect(
    roles,
    cardinality="1:1..*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="account_id",
)

erd.draw(xy=(0.0, 0.0))
```

---

## 9. Cross-Cutting Design Principles & Best Practices

### 9.1 Canvas Budgeting & Coordinate Planning
- **Center vs Corner Origin**: In `ArchitectureDiagram`, `ClassDiagram`, `ERDiagram`, and `FlowDiagram`, the `(x, y)` coordinate passed to `d.add(entity, xy=...)` defines the **geometric center** of the card or icon. In contrast, `d.draw(xy=(0, 0))` anchors the bottom-left corner of the overall diagram bounding frame.
- **Coordinate Spacing**: Allocate 25–35 coordinate units between related nodes to leave ample space for orthogonal bends, edge labels, and multiplicity badges.

### 9.2 Visual Hierarchy & Styling
- **Header Contrast**: For `ClassNode` and `Entity`, set prominent dark header styles with white text (`Style(fill_color=Colors.Navy, text_color=Colors.White)`) to emphasize domain entity titles.
- **Boundary Differentiation**: Use dashed or semi-transparent styles for `NodeGroup` and `ParticipantGroup` to clearly distinguish network boundaries from concrete computational nodes.
- **Edge Padding**: Always configure `padding=1.5` to `2.5` on architecture edges when connecting to icons to prevent arrowheads from touching icon glyphs.

### 9.3 Orthogonal Routing Guidelines
- **Side Selection**: When connecting horizontally adjacent nodes, use `start_side="right", end_side="left"`. When connecting vertically stacked nodes, use `start_side="bottom", end_side="top"`.
- **Avoiding Wire Crossings**: Use intermediate `Junction` waypoints or offset parallel paths to keep diagrams readable.

### 9.4 Typography and Font Pairing
- **Diagram Titles**: Use bold sans-serif fonts at size 18–20 for diagram headers (`FontRoboto.Bold`, `FontSansSerif.Bold`).
- **Node Labels**: Use medium sans-serif fonts at size 12–14 for entity cards and icons (`FontRoboto.Regular`).
- **Edge Badges**: Use light or regular fonts at size 9–10 with subtle background badges to preserve readability across intersecting grid lines.
- **Code & SQL**: Use monospaced fonts (`FontMonoSpace.Regular` or `FontSourceCode.Regular`) for attribute types, database column names, and method signatures.

### 9.5 Rapid Iteration with Coordinate Grids
During development, aligning nodes and fine-tuning orthogonal routing is accelerated by enabling canvas coordinate overlays:
- **CLI Export**: `drawlib export my_diagram.md 1 -g -o preview.png`
- **Canvas Overlay**: Call `canvas.show_grid()` during initial drafting to visually inspect `(x, y)` coordinates, then remove it for publication.
