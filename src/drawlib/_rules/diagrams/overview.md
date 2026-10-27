# Drawlib Diagrams Overview Guidelines (`lib-diagrams-overview`)

`drawlib.diagrams` provides a declarative, pure-Python visualization suite for software architectures, workflow flowcharts, interaction sequence diagrams, state machines, UML class hierarchies, and relational database schemas.  
Unlike external diagramming engines that depend on Graphviz, PlantUML, or opaque automatic layout solvers, Drawlib diagrams offer deterministic coordinate control, native vector drawing primitives, seamless icon library integration, and direct styling via Drawlib's `Style`, `Colors`, and `Font` systems.

---

## 1. Sub-Topic Routing Table & Decision Matrix

Query the dedicated rule manual for each diagram family using `uv run drawlib rules show <rule-id>`:

| Rule ID | Diagram Class | Module | Primary Use Cases & Key Capabilities |
| :--- | :--- | :--- | :--- |
| **`lib-diagrams-architecture`** | `ArchitectureDiagram` | `drawlib.diagrams.architecture` | Cloud networks, VPC/subnet boundaries (`NodeGroup`), microservices, 33 official & vendor-neutral icon suites (`GcpIcon`, `AwsIcon`, `AzureIcon`, `PhosphorIcon`, etc.), `Junction` fan-out (`node.fork()`). |
| **`lib-diagrams-flow`** | `FlowDiagram` | `drawlib.diagrams.flow` | ISO 5807 / JIS X 0121 flowcharts (`Start`, `End`, `Process`, `Decision`, `Data`), cross-functional vertical or horizontal swimlanes (`Lane`), orthogonal/curved/direct branch routing. |
| **`lib-diagrams-sequence`** | `SequenceDiagram` | `drawlib.diagrams.sequence` | API request/reply lifelines (`Participant`), logical service boundaries (`ParticipantGroup`), sync/async messages (`request()`, `reply()`, `connect()`), timeline notes (`Note`), and interaction frames (`loop`, `alt`, `else_`, `opt`, `par`). |
| **`lib-diagrams-state`** | `StateDiagram` | `drawlib.diagrams.state` | UML 2.x finite state machines (`State`, `InitialState`, `FinalState`, `ChoiceState`, `ForkJoinState`), entry/do/exit internal compartment behaviors, self-loops, and curved `event [guard] / action` transitions. |
| **`lib-diagrams-class`** | `ClassDiagram` | `drawlib.diagrams.class_diagram` | Three-compartment OOP UML 2.0 classes (`ClassNode`), stereotypes (`<<interface>>`), visibility markers (`+`, `-`, `#`, `~`), static/abstract members, and 6 canonical UML relationship types (`inheritance`, `realization`, `composition`, `aggregation`, `dependency`, `association`). |
| **`lib-diagrams-er`** | `ERDiagram` | `drawlib.diagrams.er` | Relational database schemas (`Entity`), PK/FK/NN/UQ column constraints, Crow's Foot / IE cardinality markers (`"1:1"`, `"1:*"`, `"*:1"`, `"*:*"`, `"1:0..1"`, `"1:1..*"`, `"1:0..*"`), and row-level column-to-column anchoring (`start_column`, `end_column`). |

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            drawlib.diagrams Taxonomy                             │
├──────────────────────────┬────────────────────────────┬──────────────────────────┤
│ System & Architecture    │ Behavior & Process         │ Structural & Data Models │
├──────────────────────────┼────────────────────────────┼──────────────────────────┤
│ • ArchitectureDiagram    │ • FlowDiagram              │ • ClassDiagram           │
│   (lib-diagrams-         │   (lib-diagrams-flow)      │   (lib-diagrams-class)   │
│    architecture)         │   - ISO 5807 Flowcharts    │   - UML 2.0 Classes      │
│   - Microservices        │   - Cross-Lane Swimlanes   │   - 6 UML Relationships  │
│   - Cloud VPCs & Subnets │ • SequenceDiagram          │ • ERDiagram              │
│   - Waypoints & Bus Lines│   (lib-diagrams-sequence)  │   (lib-diagrams-er)      │
│                          │   - Synchronous / Async    │   - IE / Crow's Foot     │
│                          │   - Condition Blocks (with)│   - Table Columns (PK/FK)│
│                          │ • StateDiagram             │   - Column Anchoring     │
│                          │   (lib-diagrams-state)     │                          │
│                          │   - FSM / Statecharts      │                          │
│                          │   - Arcs & Pseudo-States   │                          │
└──────────────────────────┴────────────────────────────┴──────────────────────────┘
```

### Module Structure & Imports

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

---

## 2. Universal Diagram Lifecycle & Local Coordinate System

All six diagram classes (`ArchitectureDiagram`, `FlowDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`) follow a unified 4-phase lifecycle:
**1. Instantiate Diagram -> 2. Register Elements in Local Coordinates -> 3. Mutate State (Optional) -> 4. Measure (`get_size()`) & Render (`draw()`)**

### 2.1 Local Coordinate Space vs. Canvas Placement (`draw()`)
Every diagram maintains its own internal local coordinate system `(0, 0) -> (width, height)` where `(0, 0)` is the diagram's bottom-left origin:

```text
  Canvas Global Space
  ▲ Y
  │      ┌─────────────────────────────────────────────────────┐
  │      │ Diagram Container: d.get_size() -> (width, height)  │
  │      │                                                     │
  │      │    ┌────────────────┐          ┌────────────────┐   │
  │      │    │ Node A         │─────────►│ Node B         │   │
  │      │    │ xy=(cx1, cy1)  │          │ xy=(cx2, cy2)  │   │
  │      │    └────────────────┘          └────────────────┘   │
  │      │                                                     │
  │      ●─────────────────────────────────────────────────────┘
  │   xy=(x0, y0)  <-- d.draw(xy=(x0, y0), align="bottom_left", scale=1.0)
  └─────────────────────────────────────────────────────────────────────────► X
```

- **Element Registration Anchors (`d.add(element, xy=...)`)**:
  - **Node-like Elements (`Node`, `FlowNode`, `StateNodeBase`, `ClassNode`, `Entity`, `Junction`)**: `xy=(cx, cy)` specifies the **center** coordinate of the element inside the diagram's local coordinate system.
  - **Container Groups (`NodeGroup` in `ArchitectureDiagram`)**: `xy=(x0, y0)` specifies the **bottom-left** origin of the group container relative to its parent (`ArchitectureDiagram` or outer `NodeGroup`). Child elements added via `group.add(child, xy=...)` use coordinates local to that group's bottom-left `(0, 0)`.
  - **Participants (`Participant` in `SequenceDiagram`)**: Added horizontally via `d.add(participant, x=None)` (auto-spaced by `col_width=20.0` or pinned to an explicit horizontal `x` coordinate).
- **Measuring Diagram Dimensions (`d.get_size()`)**:
  - `d.get_size() -> tuple[float, float]`: Returns `(width, height)` of the diagram in unscaled local units (either the explicit `width`/`height` passed to the constructor or the auto-calculated bounding box enclosing all registered elements).
  - `StateDiagram` and `ClassDiagram` also expose `d.get_bounds() -> tuple[float, float, float, float]` returning `(min_x, min_y, max_x, max_y)`.
- **Rendering onto the Canvas (`d.draw()`)**:
  ```python
  d.draw(
      xy: tuple[float, float] = (0.0, 0.0),
      *,
      align: Literal["bottom_left", "center"] = "bottom_left",
      scale: float = 1.0,
  ) -> None
  ```
  - `xy`: Target canvas coordinate `(x, y)`.
  - `align`: Anchor alignment mode (`"bottom_left"` by default places the diagram's bottom-left corner at `xy`; `"center"` centers the diagram's bounding box at `xy`).
  - `scale`: Uniform scaling multiplier (`scale > 0.0`). Proportionally scales all coordinates, shapes, stroke widths, arrowheads, icons, and font sizes around the anchor point.

### 2.2 Element Visibility (`show: bool = True`) & Layout Stability
1. **Registration & Property Mutation**:
   - Every element constructor (`Node`, `NodeGroup`, `Junction`, `Edge`, `Start`/`Process`/`Decision`/`Data`/`End`, `Lane`, `FlowEdge`, `Participant`, `ParticipantGroup`, `Message`, `Note`, `Block`, `State`/`InitialState`/`FinalState`/`ChoiceState`/`ForkJoinState`, `StateTransition`, `ClassNode`, `ClassRelationship`, `Entity`, `Relationship`) and registration method (`add()`, `add_edge()`, `connect()`, `fork()`, `junction()`, `add_lane()`, `request()`, `reply()`, `note()`, `loop()`/`alt()`/`else_()`/`opt()`/`par()`) accepts `show: bool = True` and returns the mutable element instance.
   - Setting `elem.show = False` skips rendering that element while **keeping the diagram's total bounding box (`get_size()`), node coordinates, `NodeGroup` auto-bounds, `FlowDiagram` swimlanes, and `SequenceDiagram` vertical message timelines completely unchanged**.
2. **Automatic Connected Edge & Dangling `Junction` Hiding**:
   - When a node, group, participant, state, class, or entity has `show = False`, any edge, message, transition, or relationship connected to it (`start.show == False` or `end.show == False`) is automatically hidden during `draw()`.
   - For `Junction` fan-out / merge topologies (such as `node.fork([t1, t2])`), if all outgoing branches from a `Junction` (or all incoming stems into a `Junction`) are hidden, the dangling pass-through stem is automatically hidden as well.
3. **In-Place Property Mutation for Step-by-Step Animations**:
   - Returned element objects expose mutable `.show`, `.style`, `.text_style`, `.text` / `.name` / `.title`, and `.label` attributes that are evaluated dynamically on each `draw()` call.

---

## 3. Universal Connection & Routing Engine

### 3.1 The `Connectable` Contract & `Side` / `PaddingType`
All diagram vertices, tables, containers, and waypoints implement the `Connectable` contract:
- **Boundary Rectangles**: Every connectable defines an outer bounding box (`get_bounds() -> (min_x, min_y, max_x, max_y)`).
- **Attachment Sides (`Side = Literal["left", "right", "top", "bottom", "auto"]`)**:
  - Connections resolve attachment points dynamically via `start_side="auto"` / `end_side="auto"` or pin to an explicit side (`"left"`, `"right"`, `"top"`, `"bottom"`).
- **Boundary Padding (`PaddingType = float | tuple[float, float]`)**:
  - `padding=1.5`: Symmetric 1.5-unit gap at both source and target boundaries.
  - `padding=(1.0, 2.5)`: Asymmetric gap (`1.0` at start, `2.5` at target) before arrowheads.

```text
       Source Node                                Target Node
    ┌──────────────┐      Orthogonal Edge      ┌──────────────┐
    │              ├───────────┐               │              │
    │  (cx1, cy1)  │           └──────────────►│  (cx2, cy2)  │
    │              │  padding                  │              │
    └──────────────┘                           └──────────────┘
```

### 3.2 Routing Strategies (`RoutingType`)
`RoutingType = Literal["orthogonal", "direct", "curved"]`:
1. **`routing="orthogonal"`** (Default for `ArchitectureDiagram`, `FlowDiagram`, `ClassDiagram`, and `ERDiagram`):
   Computes clean right-angled Manhattan L-bends and Z-bends between source and target boundaries.
2. **`routing="direct"`**:
   Draws a straight Euclidean line between source and target anchor points, clipping cleanly at each entity's outer boundary.
3. **`routing="curved"`** (Default for `StateDiagram`; supported across `ArchitectureDiagram`, `FlowDiagram`, `StateDiagram`, `ClassDiagram`, and `ERDiagram`):
   Draws a smooth curved transition path or spline between source and target boundaries. In `StateDiagram`, `bend: float` controls the arc deflection for bidirectional transitions.

```text
       Orthogonal Z-Bend                 Direct Straight                   Curved Spline
    ┌─────┐        ┌─────┐           ┌─────┐         ┌─────┐          ┌─────┐  . - ~ - .  ┌─────┐
    │  A  ├──┐     │  B  │           │  A  │────────►│  B  │          │  A  ├'           '┤  B  │
    └─────┘  └───►─┴─────┘           └─────┘         └─────┘          └─────┘             └─────┘
```

### 3.3 Waypoints & Branching with `Junction`
Available in `ArchitectureDiagram` and `FlowDiagram`, a `Junction` represents a zero-dimension connectable coordinate `(x, y)` on the diagram:
- **T-Junctions & Fan-Out (`node.fork()`)**: Split a single trunk line into multiple downstream targets aligned at `at_x` or `at_y`.
- **Merge Points (`d.junction(xy)`)**: Combine multiple upstream paths into a single shared waypoint before entering a successor node.
- **Dynamic Edge Tap (`edge.add_point(xy) -> Junction`)**: Insert a waypoint along an existing edge and return a connectable `Junction` for branching.

---

## 4. Styling Inheritance & Typography Hierarchy

### 4.1 3-Tier Style Resolution Cascade
Every diagram enforces a strict 3-tier style cascade (**Element Override -> Diagram Default -> Built-in Fallback**):
1. **Diagram-Level Defaults**: Passed at diagram construction (`node_style`, `node_text_style`, `edge_style`, `edge_text_style`, `node_card_style`, `header_style`, `title_style`, `style`).
2. **Element-Level Overrides**: Passed to individual nodes, containers, or edges (`style=...`, `text_style=...`, `card_style=...`, `header_style=...`) or mutated via `elem.style = ...`.
3. **Immutable Patching (`.patch()`)**: Always derive custom styles from `Styles.*` presets using `.patch(...)`:

```python
from drawlib.fonts import Font, FontMonoSpace, FontRoboto, FontSourceCode
from drawlib.styles import Colors, Styles

# Derive domain styles cleanly via .patch()
title_style = Styles.DarkBold.patch(text_size=14.0, text_font=FontRoboto.ROBOTO_BOLD)
node_text = Styles.DarkBold.patch(text_size=10.5, text_font=FontRoboto.ROBOTO_BOLD)
edge_line = Styles.Dark.patch(line_width=1.6)
edge_label = Styles.Dark.patch(text_size=9.5, text_font=FontRoboto.ROBOTO_REGULAR)
code_label = Styles.Dark.patch(text_size=9.5, text_font=FontSourceCode.ROBOTO_MONO)
```

### 4.2 Valid Font Presets (`drawlib.fonts`)
Always use valid enum members from `drawlib.fonts` when overriding `text_font`:
- **Sans-Serif (`Font`, `FontRoboto`, `FontSansSerif`)**:
  - `Font.SANSSERIF_BOLD`, `Font.SANSSERIF_REGULAR`, `Font.SANSSERIF_THIN`
  - `FontRoboto.ROBOTO_BOLD`, `FontRoboto.ROBOTO_REGULAR`, `FontRoboto.ROBOTO_THIN`, `FontRoboto.MONO_REGULAR`
- **Monospace / Code (`FontSourceCode`, `FontMonoSpace`)** (ideal for UML class signatures, ER data types, and API payloads):
  - `FontSourceCode.ROBOTO_MONO`, `FontSourceCode.SOURCECODEPRO`, `FontSourceCode.COURIER`
  - `FontMonoSpace.ROBOTO_MONO_REGULAR`, `FontMonoSpace.ROBOTO_MONO_BOLD`, `FontMonoSpace.SOURCECODEPRO_REGULAR`, `FontMonoSpace.COURIER_REGULAR`

### 4.3 Recommended Typography Sizing (`720pt` Reference Standard)
To ensure rendered diagram labels match `16px` HTML body text across documentation sites and slides:
- **Diagram Title (`title_style`)**: `text_size=13.0` to `15.0` (`FontRoboto.ROBOTO_BOLD`)
- **Group / Swimlane / Table Headers**: `text_size=11.0` to `12.5` (`FontRoboto.ROBOTO_BOLD`)
- **Primary Node / State / Participant Labels**: `text_size=10.0` to `11.5` (`FontRoboto.ROBOTO_BOLD`)
- **Edge Labels / Attributes / Columns / Guards**: `text_size=9.5` to `10.5` (`FontRoboto.ROBOTO_REGULAR` or `FontSourceCode.ROBOTO_MONO`)

---

## 5. Layout & Best Practices Checklist

1. **Maintain the 50%+ Neutral Baseline**:
   - Ground at least 50% of nodes, swimlanes, lifelines, states, classes, and entities in calm neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`).
   - Reserve saturated fills (`Styles.PrimaryFlat`, `Styles.AccentFlat`, `Styles.Danger`) strictly for 1–2 focal nodes, initial/final markers, or critical path highlights.
2. **Coordinate Anchor Awareness**:
   - Remember that `d.add(node, xy=(cx, cy))` places the **center** of a node/state/class/entity, whereas `d.add(NodeGroup(...), xy=(x0, y0))` and `d.draw(xy=(x0, y0))` (with default `align="bottom_left"`) anchor the **bottom-left** corner.
   - To center an entire diagram on a canvas of size `(W, H)`, either call `d.draw(xy=(W / 2, H / 2), align="center")` or compute `w, h = d.get_size()` and call `d.draw(xy=((W - w) / 2, (H - h) / 2))`.
3. **Combine with `drawlib.graph` for Automatic Topology Solving**:
   - When laying out complex DAGs, trees, radial rings, or multi-cluster cloud topologies where manual coordinate math is tedious, compute coordinates first via `drawlib.graph` (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph` — see `lib-graph-overview`) and feed `layout[id].xy` / `layout[cid].bottom_left` directly into `drawlib.diagrams`.
