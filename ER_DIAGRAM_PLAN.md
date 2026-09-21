# Architecture & Implementation Plan: ER Diagram (`drawlib.diagrams.er`)

## 1. Overview & Goals
- **Purpose**: Provide a built-in ER (Entity-Relationship) diagram drawing capability following the "Illustration as Code" philosophy of `drawlib`.
- **Target Notation**: **IE Notation (Information Engineering / Crow's Foot)** — the undisputed global de-facto standard for modern database modeling.
- **Design Principles**:
  - **Decoupled Architecture**: Zero dependencies on `smartarts.Table` or other high-level modules; built directly on top of `_core` drawing primitives (`rectangle`, `line`, `text`).
  - **Intuitive Object-Oriented Ergonomics**: Define entities independently, place them on the diagram (`diagram.add(entity, xy=...)`), and connect them (`entity.connect(target, ...)` or `diagram.connect(...)`).
  - **Strict Type Hints with `Literal`**: Use explicit `Literal` types for cardinality and side constraints to enable rich IDE auto-completion and static verification (no loose string parsing).

---

## 2. Public API Specification

### 2.1. Basic Usage Example

```python
from drawlib.diagrams.er import ERDiagram, Entity

erd = ERDiagram(title="E-Commerce Core Schema")

# 1. Define Entities (width and optional height; excess space is left blank)
users = Entity(name="users", width=26, height=22)
users.add_column("id", type="INT", pk=True)
users.add_column("email", type="VARCHAR(255)", nullable=False)
users.add_column("created_at", type="TIMESTAMP")

orders = Entity(name="orders", size=(26, 25))
orders.add_column("id", type="INT", pk=True)
orders.add_column("user_id", type="INT", fk=True)
orders.add_column("order_date", type="DATE")
orders.add_column("total_amount", type="DECIMAL(10,2)")

# 2. Place on Diagram (xy represents center coordinate)
erd.add(users, xy=(25, 60))
erd.add(orders, xy=(75, 60))

# 3. Connect Relationships (IE / Crow's Foot)
# users (1) to orders (0 or more)
users.connect(
    orders,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="user_id",
    label="places",
)

# 4. Render
erd.draw()
```

---

## 3. Type Definitions (`_types.py`)

### 3.1. Cardinality (`Cardinality`)
Strict `Literal` defining supported relationship multiplicities:

```python
from typing import Literal

Cardinality = Literal[
    "1:*",      # Exactly 1 to 0 or more (standard one-to-many)
    "1:1",      # Exactly 1 to Exactly 1
    "1:1..*",   # Exactly 1 to 1 or more (mandatory child)
    "1:0..1",   # Exactly 1 to 0 or 1
    "0..1:1",   # 0 or 1 to Exactly 1
    "0..1:*",   # 0 or 1 to 0 or more
    "*:*",      # 0 or more to 0 or more (many-to-many)
]
```

### 3.2. Side / Edge Attachment (`Side`)

```python
Side = Literal["left", "right", "top", "bottom", "auto"]
```

---

## 4. Class Design

### 4.1. `Entity` (`_entity.py`)
Represents a database table / entity box.

- **Layout & Sizing**:
  - Rendered sequentially from **top-left** downward:
    1. Header row (table name) at the top.
    2. Column rows sequentially below the header.
    3. If `height` or `width` is larger than the content, the extra space remains as a clean **blank background area** inside the entity box.
- **Attributes**:
  - `name: str`: Table name
  - `width: float`: Entity box width (default: 25.0)
  - `height: float | None`: Entity box height (default: `None`; if specified, fixed height is used and extra vertical space is left blank; if `None`, height auto-adjusts to fit all columns)
  - `header_height: float`: Header row height (default: 4.0)
  - `row_height: float`: Column row height (default: 3.2)
  - `columns: list[_ColumnInfo]`: Internal list of columns
  - `_local_xy: tuple[float, float] | None`: Assigned center coordinate (cx, cy) when added to a diagram
  - `_diagram: ERDiagram | None`: Owning diagram reference
- **Constructor Options**:
  - `Entity(name: str, width: float = 25.0, height: float | None = None, ...)`
  - Accepts `size: tuple[float, float]` as an optional shorthand for `(width, height)`.
- **Methods**:
  - `add_column(name: str, type: str = "", pk: bool = False, fk: bool = False, nullable: bool = True) -> Entity`:
    Add a column and return `self` for chaining.
  - `add_columns(columns: list[tuple]) -> Entity`:
    Batch helper accepting tuples `(name, type, pk, fk, nullable)`.
  - `connect(target: Entity, cardinality: Cardinality = "1:*", start_side: Side = "auto", end_side: Side = "auto", start_column: str | None = None, end_column: str | None = None, label: str = "", style: Style | None = None) -> Relationship`:
    Convenience method forwarding to `diagram.connect()`.
  - `get_bounds() -> tuple[float, float, float, float]`:
    Returns `(x_min, y_min, x_max, y_max)` bounding box based on center `_local_xy` and effective width/height.
  - `get_anchor(side: Side, column_name: str | None = None) -> tuple[float, float]`:
    Calculates exact anchor coordinate on entity border or column row.

### 4.2. `Relationship` (`_relationship.py`)
Represents an edge connecting two entities with Crow's Foot markers.

- **Attributes**:
  - `start: Entity`: Source entity
  - `end: Entity`: Target entity
  - `cardinality: Cardinality`: Multiplicity ("1:*", etc.)
  - `start_side: Side`: Attachment side on source
  - `end_side: Side`: Attachment side on target
  - `start_column: str | None`: Optional source column anchor
  - `end_column: str | None`: Optional target column anchor
  - `label: str`: Optional relationship text
  - `style: Style | None`: Custom line style
  - `routing: Literal["orthogonal", "direct"]`: Line path routing (default: "orthogonal")

### 4.3. `ERDiagram` (`_diagram.py`)
Top-level container for entities and relationships.

- **Attributes**:
  - `title: str`: Optional diagram title
  - `width: float | None`, `height: float | None`: Fixed or auto canvas size
  - `style: Style | None`: Optional background style
  - `_entities: list[tuple[Entity, tuple[float, float]]]`: Registered entities with positions
  - `_relationships: list[Relationship]`: Registered relationships
- **Methods**:
  - `add(entity: Entity, xy: tuple[float, float]) -> Entity`:
    Place an entity on the diagram at center coordinate `xy` (cx, cy).
  - `connect(...) -> Relationship`:
    Create and register a relationship between two entities.
  - `draw(xy: tuple[float, float] = (0.0, 0.0)) -> None`:
    Render all entities, borders, routing lines, and Crow's Foot markers onto canvas.

---

## 5. Rendering Engine (`_renderer.py`)

Composed purely using `_core` drawing primitives (`rectangle`, `line`, `text`):

1. **Entity Box Rendering**:
   - **Header**: Background rectangle (accent color / theme fill), bold centered table name.
   - **Column Rows**: Alternating / solid background rectangle.
   - **Row Columns Grid Layout**:
     - Key column (left, width ~15%): "PK" / "FK" label in bold.
     - Name column (center, width ~50%): Left-aligned column name (bold if PK).
     - Type column (right, width ~35%): Right-aligned data type in muted text style.
   - **Separators**: Horizontal line below header and between rows; outer border.
2. **Relationship Path Routing (Orthogonal)**:
   - Calculate start anchor point and end anchor point based on `start_side` / `end_side` (or auto-calculated nearest sides).
   - Compute right-angled waypoint path (Z-bend or L-bend) avoiding direct overlaps.
3. **Crow's Foot (IE) Endpoint Markers**:
   - Each endpoint decomposed into 2 parts:
     - **Inner marker** (min cardinality): `0` (circle) or `1` (perpendicular tick line).
     - **Outer marker** (max cardinality): `1` (perpendicular tick line) or `*` (three-pronged crow's foot forks).
   - Parametric vector drawing relative to line orientation vector `(dx, dy)`.

---

## 6. Directory & Module Structure

```text
src/drawlib/
├── _diagrams/
│   └── er/
│       ├── __init__.py        # Internal package export
│       ├── _types.py          # Cardinality, Side, ColumnInfo
│       ├── _entity.py         # Entity class & column registration
│       ├── _relationship.py   # Relationship connection model
│       ├── _diagram.py        # ERDiagram container
│       └── _renderer.py       # Core rendering & Crow's foot geometry
└── diagrams/
    └── er/
        └── __init__.py        # Public API facade (ERDiagram, Entity, Relationship, Cardinality, Side)
```

---

## 7. Implementation Roadmap

- [x] **Phase 1: Foundation Models**
  - Implement `_types.py`, `_entity.py`, `_relationship.py`, and `_diagram.py`.
  - Expose public symbols in `drawlib.diagrams.er`.
- [x] **Phase 2: Rendering Engine**
  - Implement entity drawing (header, columns, key badges, lines).
  - Implement orthogonal path routing.
  - Implement Crow's Foot marker geometry (tick, circle, crows-foot forks).
- [x] **Phase 3: Unit & Visual Tests**
  - Create `tests/test_er_diagrams.py` (model tests, connection tests, edge cases).
  - Add visual image match regression tests and verified with pytest.
- [x] **Phase 4: Documentation & Guide**
  - Create `docs_src/diagrams/er.md` with complete usage examples.
  - Build docs via `./dcli docs build`.
  - Update release notes for v0.3.0.
