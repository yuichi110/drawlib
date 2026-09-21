# Architecture & Implementation Plan: Flow Diagram (`drawlib.diagrams.flow`)

## 1. Overview & Goals
- **Purpose**: Provide a declarative, pure-Python flowchart and business workflow diagramming module within `drawlib`.
- **Target Notations**: Standard flowchart notation (ISO 5807 / JIS X 0121) and cross-functional swimlane diagrams.
- **Key Design Principles**:
  - **Shape-Centric Nodes**: Text rendered centered inside geometric shapes (Rectangle for Process, Rhombus for Decision, Rounded Stadium for Start/End, Parallelogram for Data).
  - **Direct Shape Arguments**: Inherits Drawlib's standard shape parameters (`width`, `height`, `r`, `style`, `textstyle`, `textsize`).
  - **Decoupled Architecture**: Built entirely on Drawlib `_core` drawing primitives (`rectangle`, `rhombus`, `parallelogram`, `line`, `lines`, `text`).
  - **First-Class Junction Support**: Seamless branching (Yes/No from decision points or intermediate wire taps via `flow.junction()`, `edge.add_point()`, and `node.fork()`).
  - **Declarative Swimlanes**: Flat global coordinate system where lanes serve as a background layer, allowing effortless alignment across lanes.

---

## 2. Public API Specification

### 2.1. Basic Flowchart with Decision & Loopback Example

```python
from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.flow import (
    FlowDiagram,
    Process,
    Decision,
    Start,
    End,
)

canvas.initialize()

flow = FlowDiagram(title="User Registration Flow")

# 1. Add nodes (coordinates specify shape center)
start = flow.add(Start("Start"), xy=(50.0, 90.0))
input_email = flow.add(Process("Enter Email"), xy=(50.0, 75.0))
check_exist = flow.add(Decision("Already\nRegistered?"), xy=(50.0, 55.0))
send_mail = flow.add(Process("Send Confirmation"), xy=(50.0, 35.0))
show_error = flow.add(Process("Show Error"), xy=(80.0, 55.0))
end = flow.add(End("End"), xy=(50.0, 15.0))

# 2. Connect
start.connect(input_email)
input_email.connect(check_exist)

# Decision branching
check_exist.connect(send_mail, label="No", start_side="bottom")
check_exist.connect(show_error, label="Yes", start_side="right")
show_error.connect(input_email, start_side="top", end_side="right")  # Loopback

send_mail.connect(end)

flow.draw()
```

### 2.2. Cross-Functional Swimlane Diagram with Junction Example

```python
from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.flow import (
    FlowDiagram,
    Process,
    Decision,
    Start,
    End,
)

canvas.initialize()

flow = FlowDiagram(title="Order & Payment Approval Workflow")

# 1. Define Swimlanes (column boundaries with header)
flow.add_lane("Customer", width=30.0)
flow.add_lane("Order Service", width=35.0)
flow.add_lane("Payment Gateway", width=35.0)

# 2. Add Nodes (global coordinates keep steps aligned horizontally across lanes)
submit = flow.add(Start("Submit Order"), xy=(15.0, 80.0))
validate = flow.add(Process("Validate Cart"), xy=(47.5, 80.0))
check_amt = flow.add(Decision("Amount > $1000?"), xy=(47.5, 60.0))

# T-junction branching
j = flow.junction(xy=(47.5, 45.0))
check_amt.connect(j)

auto_pay = flow.add(Process("Auto Charge"), xy=(47.5, 25.0))
manual_review = flow.add(Process("Manual Review"), xy=(82.5, 45.0))

j.connect(auto_pay, label="No", routing="orthogonal")
j.connect(manual_review, label="Yes", routing="orthogonal")

submit.connect(validate)
validate.connect(check_amt)

flow.draw()
```

---

## 3. Class & Component Design

### 3.1. Node Hierarchy (`_node.py`, `_nodes.py`)
- `FlowNode`: Base class representing any flow shape with centered text.
  - **Attributes**:
    - `text: str`: Display text
    - `width: float`: Shape width
    - `height: float`: Shape height
    - `r: float`: Corner radius (for rounded rectangle / stadium)
    - `style: Style | str | None`: Stroke/fill style
    - `textstyle: Style | str | None`: Typography style
    - `textsize: float | None`: Font size shortcut
    - `shape_type: Literal["process", "decision", "start", "end", "data"]`: Shape geometry type
    - `_local_xy: tuple[float, float]`: Center coordinate `(cx, cy)`
    - `_diagram: FlowDiagram | None`: Owning diagram
  - **Anchor Methods**:
    - `get_bounds()`: Visual bounding box relative to center.
    - `top`, `bottom`, `left`, `right`: Edge anchor coordinates taking shape geometry into account (e.g. Rhombus anchors are exact diamond vertices).
    - `get_anchor(side: Side)`: Generic anchor dispatcher.
    - `connect(target, label="", arrow="->", routing="orthogonal", style=None, padding=0.0)`
    - `fork(targets, at_x=None, at_y=None, ...)`

- **Specialized Concrete Node Classes**:
  - `Process(text, width=24.0, height=12.0, r=0.0, ...)`: Standard rectangular action.
  - `Decision(text, width=22.0, height=14.0, ...)`: Rhombus (diamond) for conditionals.
  - `Start(text="Start", width=20.0, height=10.0, r=5.0, ...)`: Stadium/pill terminal.
  - `End(text="End", width=20.0, height=10.0, r=5.0, ...)`: Stadium/pill terminal.
  - `Data(text, width=24.0, height=12.0, ...)`: Parallelogram for I/O.

### 3.2. Junction (`_junction.py`)
- Zero-size waypoint `(0, 0)` connectable element identical to `ArchitectureDiagram.Junction`.
- Supports branching, joins, and wire routing waypoints.

### 3.3. Swimlane (`_lane.py`)
- Represents a vertical (or horizontal) lane.
- **Attributes**:
  - `title: str`: Header label
  - `size: float`: Width (vertical mode) or Height (horizontal mode)
  - `style: Style | None`: Background fill and boundary line style
  - `textstyle: Style | None`: Header title text style
  - `header_size: float`: Height of header card (default: 6.0)

### 3.4. FlowEdge (`_edge.py`)
- Connection line connecting any `Connectable` (`FlowNode`, `Junction`).
- Supports orthogonal and direct routing, arrowheads (`->`, `<-`, `<->`, `-`), labels, and padding.

### 3.5. FlowDiagram (`_diagram.py`)
- Top-level diagram container.
- Manages nodes, lanes, edges, and junctions.
- Computes overall canvas bounds and executes renderer.

---

## 4. Rendering Engine (`_renderer.py`)

1. **Layer 0: Canvas Background** (if `diagram.style` provided)
2. **Layer 1: Swimlanes**
   - Background fills (alternating or custom)
   - Divider lines between lanes
   - Header boxes and rotated/centered title text
3. **Layer 2: Flow Edges**
   - Orthogonal pathing with Z-bends, L-bends, and loopbacks
   - Padding application
   - Arrowhead rendering
   - Edge labels with subtle background card
4. **Layer 3: Flow Nodes**
   - Shape rendering via `_core` (`rectangle`, `rhombus`, `parallelogram`)
   - Centered text rendering with multiline support
5. **Layer 4: Diagram Title**

---

## 5. Directory & Module Structure

```text
src/drawlib/
├── _diagrams/
│   └── flow/
│       ├── __init__.py        # Internal package export
│       ├── _types.py          # Side, ArrowType, ShapeType, etc.
│       ├── _node.py           # FlowNode base class & anchors
│       ├── _nodes.py          # Process, Decision, Start, End, Data
│       ├── _junction.py       # Junction class
│       ├── _edge.py           # FlowEdge connection class
│       ├── _lane.py           # Lane class
│       ├── _diagram.py        # FlowDiagram container
│       └── _renderer.py       # Complete rendering pipeline
└── diagrams/
    └── flow/
        └── __init__.py        # Public API facade
```

---

## 6. Implementation Roadmap

- [ ] **Phase 1: Foundation Models & Types**
  - Implement `_types.py`, `_node.py`, `_nodes.py`, `_junction.py`, `_edge.py`, `_lane.py`, `_diagram.py`.
  - Expose in `drawlib.diagrams.flow` and `drawlib.diagrams`.
- [ ] **Phase 2: Rendering Pipeline**
  - Implement node shape rendering (Rectangle, Rhombus, Stadium, Parallelogram).
  - Implement orthogonal edge routing and arrowheads.
  - Implement swimlane rendering (vertical and horizontal).
- [ ] **Phase 3: Unit & Integration Tests**
  - Create `tests/test_flow_diagrams.py`.
  - Verify node properties, anchors, junction branching, swimlanes, and PNG export.
  - Validate with `./dcli check all` and pytest.
- [ ] **Phase 4: Documentation & Guide**
  - Create `docs_src/diagrams/flow.md`.
  - Build docs via `./dcli docs build` and verify generated images.
  - Update `docs_src/index.md` and release notes.
