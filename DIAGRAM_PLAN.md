# Architecture Design Document: `drawlib.diagrams`

This document specifies the technical design, object model, API contracts, and implementation plan for `drawlib.diagrams`, with a specific focus on its first sub-module: `drawlib.diagrams.architecture`.

---

## 1. Overview and Objectives

### 1.1. Motivation & Multi-Diagram Vision
Drawlib aims to provide a comprehensive, declarative diagramming framework ("Diagram as Code") without relying on external binary runtimes like Graphviz (`dot`).

To accommodate different diagram types cleanly under a unified namespace, `drawlib.diagrams` is structured into domain-specific submodules:

```text
drawlib.diagrams
├── architecture    # Architecture & infrastructure graphs (Node, Edge, NodeGroup, Junction)
└── sequence        # Future: Sequence diagrams (Lifeline, Message, Activation)
```

### 1.2. Core Principles for `drawlib.diagrams.architecture`
- **Pure Python**: Zero external binary dependencies (runs directly on Drawlib's matplotlib canvas engine).
- **Hierarchical Layout Control**: Relative coordinates for components (`node_group.add(..., xy=(x, y))`) combined with canvas placement (`diagram.draw(xy=(x, y))`).
- **Standard Pythonic API**: Explicit method-based graph connections (`A.connect(B)`), eliminating operator overloading quirks and enabling fluent chaining (`edge.points([...]).set_label(...)`).
- **Branching & Forking Support**: First-class `Junction` (waypoint/branch) objects allowing recursive splits (`edge.add_point(...) -> junction -> junction.connect(...)`).
- **Strict Style Objects**: Only accepts Drawlib's `Style` objects for styling (no string-based style names).
- **Type-Safe Icon Ecosystem**: Integrates GCP PNG icons (`GcpIcon`) and Phosphor font icons (`PhosphorIcon`) via `EnumStr`, alongside arbitrary custom image file paths.

---

## 2. Package Architecture

Following Drawlib's single-package architecture (Pattern A):

```text
src/drawlib/
├── diagrams/                          # Public namespace package
│   ├── __init__.py                    # Exports architecture and future sequence modules
│   └── architecture/                  # Public architecture diagrams module
│       ├── __init__.py                # Exports Diagram, Node, NodeGroup, Edge, Junction, GcpIcon, PhosphorIcon
│       └── icons.py                   # Re-exports GcpIcon, PhosphorIcon
└── _diagrams/                         # Internal implementation package
    ├── __init__.py
    └── architecture/
        ├── __init__.py
        ├── _diagram.py                # Diagram container class
        ├── _node.py                   # Node vertex component
        ├── _group.py                  # NodeGroup (cluster/boundary)
        ├── _junction.py               # Junction (branch/split point)
        ├── _edge.py                   # Edge connection
        ├── _icons.py                  # GcpIcon & PhosphorIcon EnumStr definitions
        └── _renderer.py               # Coordinate resolution and canvas rendering engine
```

### 2.1. Import Contracts

```python
# Primary recommended import
from drawlib.diagrams.architecture import Diagram, Edge, Junction, Node, NodeGroup
from drawlib.diagrams.architecture import GcpIcon, PhosphorIcon

# Or importing icons from dedicated sub-module
from drawlib.diagrams.architecture.icons import GcpIcon, PhosphorIcon

# Top-level namespace access
import drawlib.diagrams.architecture as da
```

---

## 3. Core Concepts & Class Specifications

### 3.1. `Diagram` (Top-Level Container)

The root manager of nodes, groups, junctions, and connections within an architecture diagram.

#### Constructor
```python
class Diagram:
    def __init__(
        self,
        title: str = "",
        width: float | None = None,
        height: float | None = None,
        style: Style | None = None,
    ) -> None: ...
```

#### Public Methods
- `add(item: Node | NodeGroup | Junction, xy: tuple[float, float]) -> Node | NodeGroup | Junction`
  - Adds a top-level node, group, or junction at diagram-local relative coordinates `xy = (x, y)`.
  - Returns `item` for assignment or chaining.
- `connect(start: Connectable, end: Connectable, label: str = "", arrow: str = "->", routing: str = "orthogonal", style: Style | None = None) -> Edge`
  - Creates and registers an `Edge` between two connectables directly from the diagram instance.
- `junction(xy: tuple[float, float]) -> Junction`
  - Convenience helper to create, register, and return an independent `Junction` at `xy`.
- `draw(xy: tuple[float, float] = (0.0, 0.0)) -> None`
  - Resolves hierarchical coordinates, auto-bounding boxes, and anchor intersections, then renders everything to the canvas at offset `xy`.
- `get_size() -> tuple[float, float]`
  - Returns the bounding dimensions `(width, height)` of the entire diagram.

---

### 3.2. `Node` (Vertex Component)

Represents an entity (server, database, user, client, microservice) within the architecture diagram.
Crucially, **the node's `xy` coordinate defines the center of the icon/image**. The text label is offset relative to the icon and does not affect the icon's coordinate, guaranteeing reliable horizontal/vertical grid alignment and straight connection lines regardless of label content.

#### Constructor
```python
class Node:
    def __init__(
        self,
        text: str = "",
        icon: GcpIcon | PhosphorIcon | str | Callable | None = None,
        icon_size: float = 8.0,
        icon_style: Style | None = None,
        style: Style | None = None,
        # Text positioning and formatting
        text_position: Literal["bottom", "top", "left", "right"] = "bottom",
        text_margin: float = 1.5,
        text_angle: float = 0.0,
        text_size: float | None = None,
        textstyle: Style | None = None,
    ) -> None: ...
```

#### Public Methods & Properties
- `connect(target: Connectable, label: str = "", arrow: str = "->", routing: str = "orthogonal", style: Style | None = None) -> Edge`
  - Connects this node to another target (`Node`, `NodeGroup`, or `Junction`).
  - Automatically registers the created `Edge` with the diagram and returns it.
- `fork(targets: list[Connectable], at_x: float | None = None, at_y: float | None = None, style: Style | None = None) -> list[Edge]`
  - 1-to-N branching shortcut. Spawns an internal `Junction` at `at_x` or `at_y` and returns the generated edges.
- Anchors (`top`, `bottom`, `left`, `right`, `center`):
  - `left` / `right`: Located at `(x ± icon_size/2, y)` along the icon's horizontal axis, ensuring straight horizontal connections between aligned nodes.
  - `top` / `bottom`: Positioned on the outer boundary of the node (avoiding collision with text when text is positioned above or below the icon).
- `get_size() -> tuple[float, float]`
  - Returns overall visual width and height (icon + label bounding box).

---

### 3.3. `NodeGroup` (Containers / Boundaries)

A visual boundary grouping multiple `Node`s and/or nested `NodeGroup`s (e.g. VPC, Subnet, Cluster, Region).

#### Constructor
```python
class NodeGroup:
    def __init__(
        self,
        title: str = "",
        width: float | None = None,  # None -> Auto-computed from members + padding
        height: float | None = None,
        padding: float = 5.0,
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None: ...
```

#### Public Methods & Properties
- `add(item: Node | NodeGroup | Junction, xy: tuple[float, float]) -> Node | NodeGroup | Junction`
  - Adds a child element positioned at `xy` relative to this group's origin.
- `connect(target: Connectable, ...) -> Edge`
  - Connects the group's boundary to another connectable (e.g. VPC peering).
- `get_size() -> tuple[float, float]`
  - Returns `(width, height)`. If explicit, returns given dimensions; if `None`, computes the bounding box enclosing all members plus `padding` and header margin.
- Anchors (`top`, `bottom`, `left`, `right`, `center`):
  - Boundary connection anchors.

---

### 3.4. `Junction` (Branch Points / Waypoints)

A lightweight connectable point `(x, y)` without icon or text, used for splitting, joining, and complex bus topologies.

#### Constructor
```python
class Junction:
    def __init__(self, xy: tuple[float, float]) -> None: ...
```

#### Public Methods
- `connect(target: Connectable, label: str = "", arrow: str = "->", routing: str = "orthogonal", style: Style | None = None) -> Edge`
  - Connects this junction to any target (`Node`, `NodeGroup`, or another `Junction`).
  - **Returns a fully manipulable `Edge` instance.**

---

### 3.5. `Edge` (Connections)

Represents lines and relationships between connectables.

#### Constructor
```python
class Edge:
    def __init__(
        self,
        start: Connectable,
        end: Connectable,
        label: str = "",
        arrow: str = "->",
        routing: Literal["orthogonal", "direct", "curved"] = "orthogonal",
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None: ...
```

#### Public Methods (Fluent Chaining)
- `points(waypoints: list[tuple[float, float]]) -> Edge`
  - Sets explicit routing waypoints (relative to the diagram). Returns `self`.
- `via(*waypoints: tuple[float, float]) -> Edge`
  - Convenience unpacked alias for `points()`. Returns `self`.
- `add_point(xy: tuple[float, float]) -> Junction`
  - Inserts a branch point at `xy` on this edge and returns a `Junction`. Calling `junction.connect(target)` creates a branching connection.
- `set_label(text: str, pos: float = 0.5) -> Edge`
  - Sets the text label and fractional position along the line (`0.0`=start, `1.0`=end).
- `set_arrow(arrow: str) -> Edge`
  - Sets arrowhead style (`"->"`, `"<-"`, `"<->"`, `"-"`).
- `set_style(style: Style) -> Edge`
  - Overwrites the line style (color, line width, dash style).

---

### 3.6. `GcpIcon` and `PhosphorIcon` (EnumStr)

Type-safe string enumerations inheriting from `str, Enum` for IDE auto-completion and static analysis:

```python
class GcpIcon(str, Enum):
    COMPUTE_ENGINE = "compute_engine"
    CLOUD_STORAGE = "cloud_storage"
    CLOUD_SQL = "cloud_sql"
    CLOUD_LOAD_BALANCING = "cloud_load_balancing"
    KUBERNETES_ENGINE = "kubernetes_engine"
    # ... derived from drawlib._icons.png_icons.gcp


class PhosphorIcon(str, Enum):
    USER = "user"
    USERS = "users"
    DATABASE = "database"
    SERVER = "server"
    GLOBE = "globe"
    # ... derived from drawlib._icons.font_icons.phosphor
```

---

## 4. Coordinate Transformation, Alignment & 2-Pass Rendering

### 4.1. Coordinate Alignment & Origin Conventions (Fixed / Non-Configurable)

To minimize user cognitive load, ensure flawless visual alignment, and eliminate anchor calculation discrepancies, **coordinate alignment is strictly standardized and non-configurable** across all elements:

| Component | Alignment / Origin | Description & Rationale |
| :--- | :--- | :--- |
| **`Node`** | **`center` of icon (Fixed)** | The `xy` coordinate specifies the **exact center of the icon/image**, completely independent of label text length or line count. <br>• **Why icon-centric**: When placing nodes along the same Y-coordinate (e.g., `y=50`), all icons align along the line with zero vertical drift regardless of whether a label has 1 line or 3 lines. Horizontal connections between nodes remain straight without jogs.<br>• Text is offset based on `text_position` and `text_margin`. |
| **`NodeGroup`** | **`left_bottom` (Fixed)** | The group's `xy` coordinate represents its **bottom-left corner**, and child elements inside the group are positioned relative to this `(0, 0)` origin.<br>• **Why fixed**: Allows intuitive placement of child nodes using exclusively positive offsets (`x >= 0, y >= 0`). |
| **`Junction`** | **`center` (Fixed)** | The `xy` coordinate specifies the point itself. |
| **`Diagram`** | **`left_bottom` (Fixed)** | The `xy` argument in `diagram.draw(xy=(x, y))` places the bottom-left of the entire diagram at the specified canvas coordinate. |

*Note: Following the **YAGNI (You Aren't Gonna Need It)** principle, no `align` parameter is exposed in the public API. Internal engines use `align="center"` for nodes and `align="left_bottom"` for groups.*

### 4.2. 2-Pass Rendering Pipeline

Diagram rendering uses a **2-pass model**:

```text
[Pass 1: Definition]
Nodes, Groups, Junctions added -> Local relative coordinates recorded

[Pass 2: Resolution & Drawing (diagram.draw(xy=(bx, by)))]
1. Hierarchical coordinate tree resolution:
   Canvas (x, y) = Base(bx, by) + DiagramOffset + GroupOffset + ItemOffset
2. Group auto-size computation:
   BoundingBox = [min_x - padding, min_y - padding, max_x + padding, max_y + padding + title_margin]
3. Anchor computation:
   Calculate exact boundary intersection for Edge starts/ends based on node center & visual bounds.
4. Render order (back-to-front):
   Layer 0: Group backgrounds & borders
   Layer 1: Edges (lines, arrows, labels)
   Layer 2: Nodes & Junctions (icons, labels, cards)
```

---

## 5. Usage Scenarios & Code Examples

### Scenario A: Standard GCP Architecture
```python
from drawlib.canvas import config, save
from drawlib.diagrams.architecture import Diagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.types import Colors, Style

config(width=120, height=80)

diagram = Diagram()

# External User
client = diagram.add(
    Node(icon=PhosphorIcon.USER, text="Client"),
    xy=(15, 40),
)

# VPC Network with dashed style
vpc_style = Style(line_style="dashed", line_color=Colors.Gray, line_width=1.5)
vpc = NodeGroup("VPC Network", padding=6.0, style=vpc_style)

lb = vpc.add(Node(icon=GcpIcon.CLOUD_LOAD_BALANCING, text="Cloud LB"), xy=(15, 25))
vm1 = vpc.add(Node(icon=GcpIcon.COMPUTE_ENGINE, text="App Server 1"), xy=(40, 35))
vm2 = vpc.add(Node(icon=GcpIcon.COMPUTE_ENGINE, text="App Server 2"), xy=(40, 15))
db = vpc.add(Node(icon=GcpIcon.CLOUD_SQL, text="Cloud SQL"), xy=(65, 25))

diagram.add(vpc, xy=(35, 15))

# Connections
client.connect(lb, label="HTTPS")
lb.connect(vm1)
lb.connect(vm2)
vm1.connect(db)
vm2.connect(db)

# Render to canvas at (5, 5)
diagram.draw(xy=(5, 5))
save("gcp_architecture.png")
```

---

### Scenario B: Branching Tree with Custom Edge Formatting
```python
from drawlib.canvas import config, save
from drawlib.diagrams.architecture import Diagram, Node, PhosphorIcon
from drawlib.types import Colors, Style

config(width=100, height=80)

diagram = Diagram()

source = diagram.add(Node(icon=PhosphorIcon.SERVER, text="Ingress"), xy=(20, 40))
target_a = diagram.add(Node(icon=PhosphorIcon.DATABASE, text="Replica A"), xy=(80, 60))
target_b = diagram.add(Node(icon=PhosphorIcon.DATABASE, text="Replica B"), xy=(80, 20))

# 1. Main line with junction at (50, 40)
main_edge = source.connect(target_a)
p = main_edge.add_point((50, 40))

# 2. Branch line from junction p to target_b, customized independently
branch_edge = p.connect(target_b)
branch_edge.points([(50, 20)])
branch_edge.set_style(Style(line_style="dashed", line_color=Colors.Red))
branch_edge.set_label("Repl Sync")

diagram.draw(xy=(10, 10))
save("branching_diagram.png")
```

---

## 6. Implementation Roadmap

| Phase | Tasks |
| :--- | :--- |
| **Phase 1: Enums & Assets** | - Implement `GcpIcon` and `PhosphorIcon` EnumStr definitions under `src/drawlib/_diagrams/architecture/_icons.py`.<br>- Expose public module `drawlib.diagrams.architecture.icons` and re-export in `drawlib.diagrams.architecture`. |
| **Phase 2: Core Data Models** | - Implement `Node`, `NodeGroup`, `Junction`, `Edge`, and `Diagram` in `src/drawlib/_diagrams/architecture/`.<br>- Implement parent registration, anchor calculations, `Style` object enforcement, and fluent chaining. |
| **Phase 3: Layout & Rendering Engine** | - Implement hierarchical coordinate translation.<br>- Implement auto-bounding box calculations for `NodeGroup`.<br>- Implement orthogonal / direct line drawing and label placement in `_renderer.py`. |
| **Phase 4: Public Facade** | - Create `src/drawlib/diagrams/architecture/__init__.py` and re-export public API symbols.<br>- Setup `src/drawlib/diagrams/__init__.py`.<br>- Verify import paths and IDE autocompletion. |
| **Phase 5: Verification & Testing** | - Unit tests for coordinate math, bounding boxes, and junction trees (`tests/test_architecture_diagrams.py`).<br>- Visual drawing integration tests with image comparisons.<br>- Linting and type checking via `./dcli check all`. |
| **Phase 6: Documentation** | - Create comprehensive user documentation in `docs_src/diagrams/architecture/`.<br>- Rebuild docs via `./dcli docs build`. |
