# Technical Diagrams Overview & Universal Routing Engine

Drawlib's `drawlib.diagrams` module provides a declarative, pure-Python visualization suite for technical architectures, workflow flowcharts, interaction sequence diagrams, state machines, UML class hierarchies, and relational database schemas.

Unlike external diagramming tools that depend on Graphviz, PlantUML, or opaque automatic layout solvers that scramble diagrams when text changes, Drawlib diagrams offer:
- **Deterministic coordinate control**: You position elements with precision while Drawlib automatically handles boundary clipping, line offsets, and arrow alignments.
- **Universal `Connectable` interface**: Nodes, entities, classes, boundaries, and junctions implement a common protocol for flexible orthogonal, direct, and curved connections.
- **Rich vector and cloud icons**: Built-in access to 259 official Google Cloud Platform (`GcpIcon`) icons and 1,531 Phosphor (`PhosphorIcon`) icons.
- **Native theming integration**: All diagrams use standard `Styles`, `Colors`, and `Font` models.

---

## 1. Diagram Taxonomy

| Diagram Category | Class Name | Module Import | Primary Use Case |
|---|---|---|---|
| **Cloud & Architecture** | `ArchitectureDiagram` | `drawlib.diagrams.architecture` | Microservices, VPC boundaries, cloud topologies |
| **Workflow & Processes** | `FlowDiagram` | `drawlib.diagrams.flow` | ISO 5807 flowcharts, cross-functional swimlanes |
| **API Sequences & Protocols** | `SequenceDiagram` | `drawlib.diagrams.sequence` | Chronological message lifelines, condition blocks |
| **Object-Oriented Structure** | `ClassDiagram` | `drawlib.diagrams.class_diagram` | UML 2.0 class cards, 6 standard relationships |
| **Relational Schemas** | `ERDiagram` | `drawlib.diagrams.er` | Crow's foot physical schemas, column-level anchors |
| **Statecharts & Automata** | `StateDiagram` | `drawlib.diagrams.state_diagram` | Finite state machines, curved arc transitions |

---

## 2. Universal Connection Engine

All diagram elements (nodes, entities, classes, boundaries, and junctions) implement the `Connectable` protocol:

```text
       Orthogonal Z-Bend                 Direct Straight                  Curved Arc (bend)
    ┌─────┐        ┌─────┐           ┌─────┐         ┌─────┐          ┌─────┐  . - ~ - .  ┌─────┐
    │  A  ├──┐     │  B  │           │  A  │────────►│  B  │          │  A  ├'           '┤  B  │
    └─────┘  └───►─┴─────┘           └─────┘         └─────┘          └─────┘             └─────┘
```

### Connection Routing Strategies
1. **`routing="orthogonal"`** *(Default for Architecture, Flow, Class, and ER)*:
   Computes clean right-angled Z-bends and L-bends. Avoids overlapping node bounding boxes when possible.
2. **`routing="direct"`**:
   Draws a straight Euclidean line between source and target anchor points, clipping cleanly at each entity's outer boundary.
3. **`bend=float`** *(Widely used in State Diagrams)*:
   Generates a quadratic Bezier or arc curve between nodes. A positive bend curves to the left/top, while a negative bend curves to the right/bottom, allowing elegant bidirectional transitions.

### Attachment Sides and Edge Padding
- **`start_side` / `end_side`**: Set explicitly to `"left"`, `"right"`, `"top"`, `"bottom"`, or `"auto"` (resolved by nearest Euclidean distance).
- **`padding`**:
  - `padding=2.0`: Adds a 2.0-unit gap between the edge endpoint and the node perimeter.
  - `padding=(1.0, 3.0)`: Configures asymmetric padding (1.0 at start, 3.0 at end).

---

## 3. Waypoints & Bus Lines with `Junction`

A `Junction` represents a zero-dimension coordinate `(x, y)` on the canvas. It allows you to:
- **Fork Bus Lines**: Split a single wire into multiple downstream connections.
- **Merge Paths**: Combine multiple upstream error or completion paths into a single successor node.
- **Dynamic Insertion**: Calling `edge.add_point(xy)` converts an intermediate edge coordinate into a reusable `Junction`.

---

## 4. Chapter Navigation

Explore each dedicated diagram guide:
- [Cloud & Architecture Diagrams](./architecture.md): Microservices, VPC boundaries, and cloud icon topologies.
- [Flowcharts & Swimlanes](./flow.md): ISO 5807 flowchart symbols with multi-lane workflows.
- [Sequence Diagrams](./sequence.md): Chronological API interactions, message styles, and condition blocks.
- [UML Class Diagrams](./class_diagram.md): 3-compartment class cards with the 6 standard UML relationships.
- [Database ER Diagrams](./er.md): Relational schemas with Information Engineering (Crow's Foot) notation.
- [State Machines & Automata](./state_diagram.md): UML statecharts, action compartments, and curved transitions.
