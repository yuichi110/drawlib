# Drawlib Diagrams Guidelines

`drawlib.diagrams` provides a declarative, pure-Python visualization suite for software architectures, workflow flowcharts, interaction sequence diagrams, state machines, UML class hierarchies, and relational database schemas.  
Unlike external diagramming engines that depend on Graphviz, PlantUML, or opaque automatic layout solvers, Drawlib diagrams offer deterministic coordinate control, native vector drawing primitives, seamless icon library integration, and direct styling via Drawlib's `Style`, `Colors`, and `Font` systems.

---

## 1. Overview & Architecture

### 1.1 Philosophy: Illustration-as-Code for Technical Systems
Drawlib diagrams are designed for engineers and architects who require exact visual presentation:
1. **Explicit, Deterministic Layout**: Rather than fighting heuristic layout algorithms that rearrange diagrams when text changes, Drawlib gives you precise coordinate control while automatically handling boundary clipping, line offsets, and arrow alignments.
2. **First-Class Connectables**: Nodes, entities, classes, boundaries, and junctions implement a unified `Connectable` interface, enabling effortless connections between any diagram components.
3. **Rich Icon Ecosystem**: Built-in support for official Google Cloud Platform (`GcpIcon`) icons, Phosphor (`PhosphorIcon`) icons, and custom images (`CustomIcon`) in `drawlib.diagrams.architecture` and `drawlib.diagrams.sequence`.
4. **Context-Aware Routing**: Smart orthogonal routing (with L-bends and Z-bends), direct straight lines with boundary clipping, and curved transition arcs.

### 1.2 Module Structure & Imports
Domain diagram modules are organized under `drawlib.diagrams`:

```python
# Import diagram classes from their respective submodules:
from drawlib.diagrams.architecture import ArchitectureDiagram
from drawlib.diagrams.class_diagram import ClassDiagram
from drawlib.diagrams.er import ERDiagram
from drawlib.diagrams.flow import FlowDiagram
from drawlib.diagrams.sequence import SequenceDiagram
from drawlib.diagrams.state import StateDiagram

# Or import submodules from drawlib.diagrams:
from drawlib.diagrams import (
    architecture,
    class_diagram,
    er,
    flow,
    sequence,
    state,
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

### 2.5 Unified Component Lifecycle (`show`, Mutable Elements, and `scale`)
All six diagram classes (`ArchitectureDiagram`, `FlowDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`) follow a unified 4-phase lifecycle (**1. Instantiate -> 2. Register Elements -> 3. Mutate State -> 4. Render via `draw()`**):

1. **Element Visibility (`show: bool = True`) & Layout Stability**:
   - Every element constructor (`Node`, `NodeGroup`, `Junction`, `Edge`, `Start`/`Process`/`Decision`/`Data`/`End`, `Lane`, `Participant`, `ParticipantGroup`, `Message`, `Note`, `Block`, `State`/`InitialState`/`FinalState`/`ChoiceState`/`ForkJoinState`, `StateTransition`, `ClassNode`, `ClassRelationship`, `Entity`, `Relationship`) and registration method (`add()`, `connect()`, `fork()`, `junction()`, `add_lane()`, `request()`, `reply()`, `note()`, `loop()`/`alt()`/`opt()`/`par()`) accepts `show: bool = True` and returns the mutable element instance.
   - Setting `elem.show = False` skips rendering that element while **keeping the diagram's total bounding box (`get_size()`), node coordinates, `NodeGroup` auto-bounds, `FlowDiagram` swimlanes, and `SequenceDiagram` vertical message timelines completely unchanged**.
2. **Automatic Connected Edge & Dangling `Junction` Hiding**:
   - When a node, group, participant, state, class, or entity has `show = False`, any edge, message, transition, or relationship connected to it (`start.show == False` or `end.show == False`) is automatically hidden during `draw()`.
   - For `Junction` fan-out / merge topologies (such as `node.fork([t1, t2])`), if all outgoing branches from a `Junction` (or all incoming stems into a `Junction`) are hidden, the dangling pass-through stem is automatically hidden as well.
3. **In-Place Property Mutation**:
   - Returned element objects expose mutable `.show`, `.style`, `.text_style`, `.text` / `.name` / `.title`, and `.label` attributes that are evaluated dynamically on each `draw()` call.
4. **Proportional Scaling (`scale: float = 1.0`)**:
   - Every diagram's `draw(xy=(0.0, 0.0), *, scale: float = 1.0)` method applies a uniform canvas transformation anchored at `xy`, proportionally scaling all coordinates, shapes, stroke widths, arrowheads, icons, and font sizes.

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
| `node_style` | `Style` | *(Required)* | Default style for node icons and images. |
| `node_text_style` | `Style` | *(Required)* | Default typography style for node labels. |
| `edge_style` | `Style` | *(Required)* | Default style for connection lines and arrowheads. |
| `edge_text_style` | `Style` | *(Required)* | Default typography style for connection edge labels. |
| `node_card_style` | `Style \| None` | `None` | Default style for node card backgrounds (transparent if `None`). |
| `title` | `str` | `""` | Diagram title text rendered at top. |
| `title_style` | `Style \| None` | `None` | Optional typography style for diagram title. |
| `width` / `height` | `float \| None` | `None` | Optional canvas bounding dimensions override. |
| `margin` | `float` | `5.0` | Outer margin around all elements. |
| `style` | `Style \| None` | `None` | Optional Style for container background card. |

- `d.add(item, xy, *, show=None) -> Node | NodeGroup | Junction`: Places a node, group, or junction (optionally overriding `item.show`).
- `d.connect(source, target, label="", arrow="->", routing="orthogonal", style=None, text_style=None, padding=0.0, show=True) -> Edge`: Creates and registers a connection edge.
- `d.junction(xy, *, show=True) -> Junction`: Creates and registers a branching waypoint junction.
- `d.draw(xy=(0.0, 0.0), *, scale=1.0)`: Renders diagram at bottom-left coordinate `xy` with optional proportional `scale`.

#### `Node` Class:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `""` | Node label text (supports `\n`). |
| `width` | `float` | `20.0` | Card bounding box width in canvas units. |
| `height` | `float` | `16.0` | Card bounding box height in canvas units. |
| `icon` | `IconType` | `None` | `PhosphorIcon`, `GcpIcon`, icon callable, `CustomIcon`, `Dimage`, `PIL.Image`, or path. |
| `icon_size` | `float` | `8.0` | Outer width and height of the icon/image. |
| `style` | `Style \| None` | `None` | Optional style override for the icon or image. |
| `text_style` | `Style \| None` | `None` | Optional explicit style override for the label text (supports `xy_shift`, `angle`). |
| `card_style` | `Style \| None` | `None` | Optional style override for the card background/border (transparent if `None` and `node_card_style` is `None`). |
| `show` | `bool` | `True` | Whether to render this node (and its connected edges). |

- **Card-Centric Coordinates**: The coordinate `xy` passed to `d.add(node, xy)` defines the **center of the node card** `(width, height)`. When both `icon` and `text` are provided, the icon is placed in the upper middle of the card and the label in the lower portion (adjustable via `text_style=Styles.DarkBold.patch(xy_shift=...)`).
- `node.connect(target, label="", arrow="->", routing="orthogonal", style=None, text_style=None, padding=0.0, show=True) -> Edge`: Connects this node to `target`.
- `node.fork(targets, at_x=None, at_y=None, style=None, padding=0.0, show=True) -> list[Edge]`: Creates a 1-to-N bus fan-out via an automatic intermediate junction.

#### `NodeGroup` Class:
| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | `""` | Group banner title (e.g. `"VPC Network (10.0.0.0/16)"`). |
| `padding` | `float` | `6.0` | Inner margin around enclosed child nodes. |
| `style` | `Style \| None` | `None` | Style for group background fill and boundary border. |
| `text_style` | `Style \| None` | `None` | Optional style override for the group title. |
| `show` | `bool` | `True` | Whether to render the group boundary box and title. |

- **Auto-Bounding**: Automatically computes its bounding box to enclose all child nodes and nested groups with configurable padding (even when child nodes have `show=False`).
- **Group as Connectable**: You can connect directly to or from a group's boundary box.

#### Built-in Icons & Images:
- `GcpIcon`: 259 official Google Cloud icons (`GcpIcon.COMPUTE_ENGINE`, `GcpIcon.CLOUD_RUN`, `GcpIcon.CLOUD_SQL`, `GcpIcon.BIGQUERY`, etc.).
- `PhosphorIcon`: 1,531 modern interface icons (`PhosphorIcon.USER`, `PhosphorIcon.DATABASE`, `PhosphorIcon.BROWSER`, etc.).
- Direct callables/images: `phosphor.*` or `gcp.*` functions, `Dimage`, `PIL.Image.Image`, file paths (`str` / `Path`), or `CustomIcon(image)`.

### 3.3 Production Examples

#### Example 3.3.1: Multi-Tier Cloud VPC Network
```drawlib show-code
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

# Outer VPC Network boundary
vpc = d.add(NodeGroup(title="VPC Network (10.0.0.0/16)", padding=7.0), xy=(32.0, 8.0))

# Public Subnet with Load Balancer (local coordinates inside vpc)
public_subnet = vpc.add(NodeGroup(title="Public Subnet (10.0.1.0/24)", padding=5.0), xy=(6.0, 6.0))
lb = public_subnet.add(Node("Cloud Load Balancer", width=26, height=17, icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=8.0), xy=(16.0, 30.0))

# Private Subnet with Application Pods (local coordinates inside vpc)
private_subnet = vpc.add(NodeGroup(title="Private Subnet (10.0.2.0/24)", padding=5.0), xy=(48.0, 6.0))
gke1 = private_subnet.add(Node("API Pod 1", width=20, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0), xy=(14.0, 44.0))
gke2 = private_subnet.add(Node("API Pod 2", width=20, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0), xy=(14.0, 16.0))

# External Actor and Managed Services (global diagram coordinates outside vpc)
user = d.add(Node("Client User", width=18, height=16, icon=PhosphorIcon.USER, icon_size=8.0), xy=(9.0, 44.0))
db = d.add(Node("Cloud SQL\n(PostgreSQL)", width=24, height=18, icon=GcpIcon.CLOUD_SQL, icon_size=8.0), xy=(140.0, 58.0))
storage = d.add(Node("Cloud Storage\n(Assets)", width=24, height=18, icon=GcpIcon.CLOUD_STORAGE, icon_size=8.0), xy=(140.0, 30.0))

# Connections
d.connect(user, lb, label="HTTPS (443)", padding=1.5)
lb.fork([gke1, gke2], at_x=73.0, padding=1.5)
d.connect(gke1, db, label="SQL Query", padding=1.5)
d.connect(gke2, storage, label="Asset Sync", padding=1.5)

d.draw(xy=(4.0, 4.0))
```

#### Example 3.3.2: Event-Driven Kafka Streaming Mesh
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=132, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Event-Driven Message Streaming Topology",
)

cluster = d.add(NodeGroup(title="Streaming Event Mesh", padding=6.0), xy=(30.0, 10.0))
broker1 = cluster.add(Node("Kafka Broker 1", width=22, height=16, icon=PhosphorIcon.STACK, icon_size=7.0), xy=(17.0, 40.0))
broker2 = cluster.add(Node("Kafka Broker 2", width=22, height=16, icon=PhosphorIcon.STACK, icon_size=7.0), xy=(17.0, 14.0))

pub = d.add(Node("Event Ingest\nProducer", width=20, height=17, icon=PhosphorIcon.BROADCAST, icon_size=7.5), xy=(9.0, 37.0))
analytics = d.add(Node("Realtime Analytics\nConsumer", width=26, height=17, icon=PhosphorIcon.CHART_BAR, icon_size=7.5), xy=(104.0, 50.0))
archiver = d.add(Node("Parquet Lakehouse\nArchiver", width=26, height=17, icon=PhosphorIcon.HARD_DRIVES, icon_size=7.5), xy=(104.0, 24.0))

pub.fork([broker1, broker2], at_x=25.0, padding=1.5)
d.connect(broker1, analytics, label="Consumer Group A", padding=1.5)
d.connect(broker2, archiver, label="Consumer Group B", padding=1.5)

d.draw(xy=(4.0, 4.0))
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
| `Start` | Stadium / Pill (`shape_r=5.0`) | `"start"` | `20.0 x 10.0` | Initial entry point of the flow |
| `End` | Stadium / Pill (`shape_r=5.0`) | `"end"` | `20.0 x 10.0` | Terminal termination point |
| `Process` | Rectangle | `"process"` | `24.0 x 12.0` | Task, execution step, or operation |
| `Decision` | Rhombus / Diamond | `"decision"`| `22.0 x 14.0` | Conditional branch (Yes/No, True/False) |
| `Data` | Parallelogram | `"data"` | `24.0 x 12.0` | Data input, output, or file I/O |
| `Junction` | Zero-Size Coordinate | `"junction"`| `0.0 x 0.0` | Wire tap, waypoint, or merge junction |
| `Lane` | Boundary Band | `"lane"` | Dynamic | Department, role, or microservice boundary |

### 4.3 Node Arguments, Registration & Rendering
All flow nodes inherit from `FlowNode` and accept standard geometric customization arguments:
- `text`: Label centered inside shape (multiline supported via `\n`).
- `width` / `height`: Boundary dimensions in canvas units.
- `style`: Fill color, border stroke color, line width, line style, and corner rounding radius (`style.shape_r`).
- `text_style`: Typography style for the centered text.
- `show`: `bool = True` (initial visibility flag; can also be overridden in `flow.add(..., show=...)` or mutated via `node.show = ...`).

#### Registration, Connections & Rendering:
- `flow.add(node, xy=(x, y), *, show: bool = True) -> FlowNode`
- `flow.add_lane(name, width=..., height=..., header_size=..., *, show: bool = True) -> Lane`
- `node.connect(other, label="", start_side=None, end_side=None, routing="orthogonal", arrow="->", style=None, text_style=None, bend=0.25, show: bool = True) -> Edge`
- `flow.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`

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
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=110, height=95)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Expense Reimbursement Approval Workflow",
    width=100.0,
    height=90.0,
)

# 1. Define vertical department lanes (columns from left to right)
flow.add_lane("Employee", width=30.0)
flow.add_lane("Line Manager", width=35.0)
flow.add_lane("Finance Dept", width=35.0)

# 2. Add nodes (Y coordinates align corresponding steps horizontally)
submit = flow.add(Start("Submit Claim"), xy=(15.0, 78.0))
receipt = flow.add(Data("Attach Receipt"), xy=(15.0, 62.0))
review = flow.add(
    Process("Review Details", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold),
    xy=(47.5, 62.0),
)
decision = flow.add(Decision("Amount < $500?", style=Styles.SecondaryNeutral), xy=(47.5, 42.0))

audit = flow.add(Process("Compliance Audit"), xy=(82.5, 42.0))
auto_pay = flow.add(Process("Disburse Payment", style=Styles.PrimaryNeutral), xy=(82.5, 20.0))
end = flow.add(End("Claim Closed"), xy=(15.0, 20.0))

# 3. Connect steps
submit.connect(receipt)
receipt.connect(review)
review.connect(decision)

# Decision routing (separate vertical levels avoid label collisions)
decision.connect(audit, label="No", start_side="right", end_side="left")
decision.connect(auto_pay, label="Yes", start_side="bottom", end_side="left")
audit.connect(auto_pay, start_side="bottom", end_side="top")
auto_pay.connect(end, label="Notice Sent", start_side="left", end_side="right")

flow.draw(xy=(5.0, 5.0))
```

#### Example 4.5.2: Horizontal Warehouse Order Processing
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=145, height=80)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Fulfillment Logistics Pipeline",
    lane_orientation="horizontal",
    width=130.0,
    height=65.0,
)

flow.add_lane("Sales Platform", height=32.5, header_size=22.0)
flow.add_lane("Distribution Center", height=32.5, header_size=22.0)

order = flow.add(Start("New Purchase", width=22.0), xy=(36.0, 48.0))
validate = flow.add(Decision("In Stock?", style=Styles.SecondaryNeutral), xy=(68.0, 48.0))
cancel = flow.add(End("Cancel & Refund", width=26.0), xy=(112.0, 48.0))
pack = flow.add(Process("Pick & Pack", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=(68.0, 16.0))
dispatch = flow.add(End("Ship Carrier", width=24.0), xy=(112.0, 16.0))

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

#### Constructor, Participant Management & Rendering:
- `SequenceDiagram(node_style, node_text_style, edge_style, edge_text_style, node_card_style=None, title="", width=None, height=None, margin=5.0, autonumber=False, style=None, title_style=None)`
- `d.add(Participant(text="", width=20.0, height=16.0, icon=None, icon_size=8.0, style=None, text_style=None, card_style=None, lifeline_style=None, show=True), *, show: bool = True) -> Participant`
- `d.add(ParticipantGroup(title="", padding=4.0, style=None, show=True), *, show: bool = True) -> ParticipantGroup`
- `group.add(Participant(...), *, show: bool = True) -> Participant`
- `d.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`

#### Message Verbs (all return a mutable `Message` instance):
- **`a.request(b, label, is_async=False, show=True) -> Message`**: Synchronous call rendered as a solid line with a filled arrowhead (`―▶`). If `is_async=True`, renders an open stick arrowhead (`―>`).
- **`b.reply(a, label, is_async=False, show=True) -> Message`**: Response or return value rendered as a dashed line with a filled arrowhead (`---▶`). If `is_async=True`, renders an open stick arrowhead (`--->`).
- **`a.connect(b, label, arrow="<->", show=True) -> Message`**: Bidirectional persistent communication (e.g. WebSocket connection or gRPC streaming channel).
- **`p.request(p, label, show=True) -> Message`**: Self-call loop rendered as a 3-segment orthogonal loop returning to the caller's lifeline.

#### Execution Controls:
- **Activation Boxes**: `p.activate()` and `p.deactivate()` render execution rectangles along the participant's vertical lifeline.
- **Autonumbering**: Setting `SequenceDiagram(..., autonumber=True)` automatically prepends chronological sequential numbers (`1.`, `2.`, `3.`, ...) to message labels.
- **Sticky Notes** (return a mutable `Note` instance):
  - `p.note(text, pos="left"|"right", show=True) -> Note`: Annotates a single participant's lifeline.
  - `d.note(text, over=[p1, p2], show=True) -> Note`: Spans centered across multiple lifelines.

#### Structured Condition Frames (`Block` via Python `with`):
Indented Python `with` statements naturally structure condition frames in the diagram and yield a mutable `Block` instance:
- `with d.loop("Condition", show=True) as blk:` (Loop / repeat frame)
- `with d.alt("Condition A", show=True) as blk:` and `with d.else_("Condition B"):` (Alternative branch frame)
- `with d.opt("Condition", show=True) as blk:` (Optional execution frame)
- `with d.par("Description", show=True) as blk:` (Concurrent parallel steps)

### 5.3 Production Examples

#### Example 5.3.1: Microservices Order Processing Pipeline
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=165, height=140)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Microservices Distributed Transaction Pipeline",
    autonumber=True,
    col_width=38.0,
    step_y=10.0,
)

# 1. Participants: Client on the left, Backend services in VPC group on the right
client = d.add(Participant("Web Browser", width=22, height=16, icon=PhosphorIcon.BROWSER, icon_size=7.5))

backend = d.add(
    ParticipantGroup(
        title="Google Cloud VPC",
        padding=3.5,
        style=Styles.MutedDashed,
    )
)
api = backend.add(
    Participant("Cloud Run\n(Gateway)", width=22, height=16, icon=GcpIcon.CLOUD_RUN, icon_size=7.5, card_style=Styles.PrimaryNeutral)
)
worker = backend.add(Participant("GKE Pod\n(Worker)", width=22, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=7.5))
db = backend.add(Participant("Cloud SQL\n(Database)", width=22, height=16, icon=GcpIcon.CLOUD_SQL, icon_size=7.5))

# 2. Interactions
client.request(api, "POST /api/v1/checkout")
api.activate()

api.request(db, "Check Inventory")
db.reply(api, "Stock Available")

api.request(worker, "Enqueue Job (Pub/Sub)", is_async=True)
worker.reply(api, "Ack", is_async=True)

api.reply(client, "202 Accepted (Order ID)")
api.deactivate()

with d.loop("Retry up to 3 times on DB lock"):
    worker.request(db, "Deduct Inventory Rows")
    db.reply(worker, "Rows Committed")

d.draw(xy=(5.0, 3.0))
```

#### Example 5.3.2: Bidirectional WebSocket Protocol Stream
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=85, height=80)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="WebSocket Real-Time Live Sync",
)

app = d.add(Participant("Mobile App", width=22, height=15, icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5))
gateway = d.add(Participant("WS Gateway", width=22, height=15, icon=PhosphorIcon.CLOUD, icon_size=7.5, card_style=Styles.PrimaryNeutral))

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

### 6.3 Action Compartments, Registration & Transition Syntax
- **Registration & Rendering**:
  - `sd.add(state_or_note, xy=(x, y), *, show: bool = True) -> StateNode | StateNote`
  - `sd.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`
- **Internal Actions**: Pass `entry="..."`, `do="..."`, or `exit="..."` during `State` creation, or chain with `state.add_action("custom", "...")`.
- **Transitions with `sd.connect(...) -> Transition`**:
  ```python
  tr = sd.connect(
      s1,
      s2,
      event="submit",
      guard="is_valid",
      action="save()",
      bend=0.25,  # Curved arc
      show=True,
  )
  ```
  Automatically formats formal UML labels: `event [guard] / action`, and returns a mutable `Transition` object (`tr.show`, `tr.style`, `tr.text_style`, `tr.event`, `tr.guard`, `tr.action`).
- **Self-Transitions**: Call `sd.connect(state, state, side="top", event="tick")`.

### 6.4 Production Examples

#### Example 6.4.1: Session Lifecycle State Machine
```drawlib show-code file:diagram_state_lifecycle.png
from drawlib import canvas
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=142, height=75)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="User Session Lifecycle State Machine",
)

# 1. Pseudo-states and state nodes
init = sd.add(InitialState(), xy=(12.0, 38.0))
idle = sd.add(
    State("Idle", shape="box", entry="reset()", do="listen()", width=22.0),
    xy=(38.0, 38.0),
)
valid_check = sd.add(ChoiceState(name="Valid?", style=Styles.SecondaryNeutral), xy=(72.0, 38.0))
active = sd.add(
    State(
        "Active",
        shape="box",
        entry="start()",
        do="handle()",
        exit="flush()",
        style=Styles.PrimaryNeutral,
        width=22.0,
    ),
    xy=(105.0, 38.0),
)
final = sd.add(FinalState(), xy=(132.0, 38.0))

# 2. Connect transitions
sd.connect(init, idle)
sd.connect(idle, valid_check, event="login")

# Choice branches (success vs failure)
sd.connect(valid_check, active, guard="valid")
sd.connect(
    valid_check,
    idle,
    guard="invalid",
    bend=-0.35,
    start_side="bottom",
    end_side="bottom",
    text_style=Styles.Dark.patch(valign="top"),
)

# Self-transition heartbeat loop
sd.connect(active, active, side="top", event="ping", action="extend()")

# Termination
sd.connect(active, final, event="logout")

sd.draw(xy=(0.0, 0.0))
```

#### Example 6.4.2: Concurrent Task Synchronization with Fork and Join
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.state import FinalState, ForkJoinState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=115, height=75)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Concurrent Task Fork and Join",
)

init = sd.add(InitialState(), xy=(10.0, 37.5))
fork = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(25.0, 37.5))
job_a = sd.add(State("Compute Analytics", shape="box", width=28.0, style=Styles.PrimaryNeutral), xy=(55.0, 50.0))
job_b = sd.add(State("Index Search", shape="box", width=28.0, style=Styles.SecondaryNeutral), xy=(55.0, 25.0))
join = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(85.0, 37.5))
final = sd.add(FinalState(), xy=(105.0, 37.5))

sd.connect(init, fork)
sd.connect(fork, job_a)
sd.connect(fork, job_b)
sd.connect(job_a, join)
sd.connect(job_b, join)
sd.connect(join, final)

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

### 7.2 ClassNode Configuration, Registration & Rendering
- **Registration & Rendering**:
  - `cd.add(node, xy=(x, y), *, show: bool = True) -> ClassNode`
  - `cd.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`
- **Attributes**: `node.add_attribute(name, type, is_public=True, is_static=False, default_value="")`.
  - Symbols: `+` (public), `-` (private), `#` (protected), `~` (package).
  - Batch: `node.add_attributes([("id", "int", True), ("secret", "str", False)])`.
- **Methods**: `node.add_method(name, params="", return_type="", is_public=True, is_abstract=False, is_static=False)`.
  - Batch: `node.add_methods([("execute", "task: Task", "bool")])`.
- **Stereotypes**: `ClassNode(name="Service", stereotype="interface")` renders `«interface»`.
- **Abstract Classes**: `ClassNode(name="Entity", is_abstract=True)` renders `«abstract»`.

### 7.3 The 6 UML Relationship Types
Relationships between classes are registered cleanly at the diagram level via `cd.connect(source, target, relationship_type=..., ..., show: bool = True) -> Relationship`:

| `relationship_type` | UML Relationship | Line Stroke | End Marker | Description |
|---|---|---|---|---|
| `"inheritance"` | **Inheritance** | Solid | Hollow Triangle (at target) | Superclass / Subclass Generalization |
| `"realization"` | **Realization** | Dashed | Hollow Triangle (at target) | Interface Implementation |
| `"composition"` | **Composition** | Solid | Filled Diamond (at source) | Strong ownership; part dies with whole |
| `"aggregation"` | **Aggregation** | Solid | Hollow Diamond (at source) | Shared ownership / part-whole |
| `"association"` | **Association** | Solid | None (or Open Arrow) | Structural reference |
| `"dependency"` | **Dependency** | Dashed | Open Arrow (at target) | Client depends on supplier |

`cd.connect(...)` supports `start_side`, `end_side`, `start_multiplicity` (`"1"`, `"0..1"`), `end_multiplicity` (`"*"`, `"1..*"`), `start_role`, `end_role`, `label`, and `show: bool = True`, returning a mutable `Relationship` instance (`rel.show`, `rel.style`, `rel.text_style`, `rel.label`).

### 7.4 Production Examples

#### Example 7.4.1: E-Commerce Domain Model
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=110, height=85)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="E-Commerce Domain Class Model",
)

# 1. Define classes
user = cd.add(ClassNode(name="User", width=26.0), xy=(22.0, 60.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("email", type="str", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", return_type="bool")

customer = cd.add(ClassNode(name="Customer", width=26.0, style=Styles.SecondaryNeutral), xy=(22.0, 20.0))
customer.add_attribute("shipping_address", type="str")
customer.add_method("checkout", return_type="Order")

order = cd.add(ClassNode(name="Order", width=28.0, style=Styles.PrimaryNeutral), xy=(75.0, 20.0))
order.add_attribute("order_id", type="str")
order.add_attribute("total", type="float")
order.add_method("calculate_tax", return_type="float")

iface = cd.add(ClassNode(name="PaymentGateway", stereotype="interface", width=30.0), xy=(75.0, 60.0))
iface.add_method("process_charge", params="amount: float", return_type="bool")

# 2. Connect relationships using diagram.connect
cd.connect(customer, user, "inheritance", start_side="top", end_side="bottom")
cd.connect(
    customer,
    order,
    "composition",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="places",
)
cd.connect(order, iface, "dependency", start_side="top", end_side="bottom", label="uses")

cd.draw(xy=(0.0, 0.0))
```

#### Example 7.4.2: Observer Design Pattern Implementation
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=105, height=80)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="UML Observer Design Pattern",
)

subj_iface = cd.add(
    ClassNode(name="Subject", stereotype="interface", width=28.0, style=Styles.PrimaryNeutral),
    xy=(25.0, 58.0),
)
subj_iface.add_method("attach", params="o: Observer", return_type="void")
subj_iface.add_method("notify", return_type="void")

obs_iface = cd.add(
    ClassNode(name="Observer", stereotype="interface", width=28.0, style=Styles.SecondaryNeutral),
    xy=(75.0, 58.0),
)
obs_iface.add_method("update", return_type="void")

concrete_subj = cd.add(ClassNode(name="NewsPublisher", width=28.0), xy=(25.0, 20.0))
concrete_subj.add_attribute("state", type="str", is_public=False)
concrete_subj.add_method("get_state", return_type="str")

concrete_obs = cd.add(ClassNode(name="EmailSubscriber", width=28.0), xy=(75.0, 20.0))
concrete_obs.add_method("update", return_type="void")

cd.connect(concrete_subj, subj_iface, "realization", start_side="top", end_side="bottom")
cd.connect(concrete_obs, obs_iface, "realization", start_side="top", end_side="bottom")
cd.connect(
    subj_iface,
    obs_iface,
    "aggregation",
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

### 8.2 Entity Configuration, Registration & Column Modeling
- **Registration & Rendering**:
  - `er.add(entity, xy=(x, y), *, show: bool = True) -> Entity`
  - `er.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`
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
By passing `start_column="col_a"` and `end_column="col_b"`, connection lines align vertically with the exact table rows of foreign and primary keys (`entity.connect(...)` returns a mutable `Relationship` instance and accepts `show: bool = True`):

```python
rel = users.connect(
    orders,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",       # Anchors to 'id' row in users
    end_column="user_id",    # Anchors to 'user_id' row in orders
    label="places",
    show=True,
)
```

### 8.5 Production Examples

#### Example 8.5.1: Core E-Commerce Relational Schema
```drawlib show-code
from drawlib import canvas
from drawlib.diagrams.er import ERDiagram, Entity
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=158, height=85)

erd = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="E-Commerce Relational Database Schema",
)

# 1. Define entities with adequate width for column names and types
users = erd.add(Entity(name="users", width=28.0), xy=(22.0, 50.0))
users.add_column("id", type="INT", pk=True)
users.add_column("email", type="VARCHAR", nullable=False)
users.add_column("name", type="VARCHAR")

orders = erd.add(Entity(name="orders", width=32.0, style=Styles.PrimaryNeutral), xy=(76.0, 50.0))
orders.add_column("id", type="INT", pk=True)
orders.add_column("user_id", type="INT", fk=True)
orders.add_column("total_amount", type="DECIMAL")

items = erd.add(Entity(name="order_items", width=34.0), xy=(130.0, 50.0))
items.add_column("id", type="INT", pk=True)
items.add_column("order_id", type="INT", fk=True)
items.add_column("product_name", type="VARCHAR")
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
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=145, height=80)

erd = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Multi-Tenant RBAC Authorization Schema",
)

tenants = erd.add(Entity(name="tenants", width=28.0), xy=(22.0, 48.0))
tenants.add_column("id", type="UUID", pk=True)
tenants.add_column("slug", type="VARCHAR", nullable=False)

accounts = erd.add(Entity(name="accounts", width=28.0, style=Styles.PrimaryNeutral), xy=(72.0, 48.0))
accounts.add_column("id", type="UUID", pk=True)
accounts.add_column("tenant_id", type="UUID", fk=True)
accounts.add_column("email", type="VARCHAR")

roles = erd.add(Entity(name="roles", width=28.0), xy=(122.0, 48.0))
roles.add_column("id", type="UUID", pk=True)
roles.add_column("account_id", type="UUID", fk=True)
roles.add_column("role_name", type="VARCHAR")

tenants.connect(
    accounts,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="tenant_id",
    routing="orthogonal",
)
accounts.connect(
    roles,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="account_id",
    routing="orthogonal",
)

erd.draw(xy=(0.0, 0.0))
```

---

## 9. Cross-Cutting Design Principles & Best Practices

### 9.1 Canvas Budgeting & Coordinate Planning
- **Center vs Corner Origin**: In `ArchitectureDiagram`, `ClassDiagram`, `ERDiagram`, and `FlowDiagram`, the `(x, y)` coordinate passed to `d.add(entity, xy=...)` defines the **geometric center** of the card or icon. In contrast, `d.draw(xy=(0, 0))` anchors the bottom-left corner of the overall diagram bounding frame.
- **Coordinate Spacing**: Allocate 25–35 coordinate units between related nodes to leave ample space for orthogonal bends, edge labels, and multiplicity badges.

### 9.2 Visual Hierarchy & Styling
- **Header Contrast**: For `ClassNode` and `Entity`, set prominent dark header styles with white text (`Style(shape_fill_color=Colors.Navy, text_color=Colors.White)`) to emphasize domain entity titles.
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
- **CLI Export**: `drawlib show my_diagram.md 1 -g -o preview.png`
- **Canvas Overlay**: Call `canvas.show_grid()` during initial drafting to visually inspect `(x, y)` coordinates, then remove it for publication.
