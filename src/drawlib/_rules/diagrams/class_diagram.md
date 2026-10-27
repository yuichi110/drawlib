# Drawlib ClassDiagram Guidelines (`lib-diagrams-class`)

`drawlib.diagrams.class_diagram` models object-oriented software designs according to UML 2.0 specifications, rendering 3-compartment class boxes (`ClassNode`: header with stereotype/name, attributes compartment, and methods compartment) connected by the 6 canonical UML relationship types (`inheritance`, `realization`, `composition`, `aggregation`, `dependency`, `association`).

```text
  ┌──────────────────────────────┐          ┌──────────────────────────────┐
  │         <<interface>>        │          │          OrderItem           │
  │          Repository          │          ├──────────────────────────────┤
  ├──────────────────────────────┤          │ - sku: str                   │
  ├──────────────────────────────┤          │ - quantity: int = 1          │
  │ + find_by_id(id: UUID): T    │          ├──────────────────────────────┤
  │ + save(entity: T): None      │          │ + subtotal(): Decimal        │
  └──────────────▲───────────────┘          └──────────────▲───────────────┘
                 │                                         │
                 │ cd.connect(..., "realization")          │ cd.connect(..., "composition")
                 │ (dashed line, hollow triangle)          ◆ (solid diamond at Order)
  ┌──────────────┴───────────────┐          ┌──────────────┴───────────────┐
  │      SqlOrderRepository      │─────────►│            Order             │
  └──────────────────────────────┘          └──────────────────────────────┘
```

---

## 1. Public Exports & Imports

```python
from drawlib.diagrams.class_diagram import (
    AttributeInfo,
    ClassDiagram,
    ClassNode,
    ClassRelationship,
    MethodInfo,
    RelationshipType,
    RoutingType,
    Side,
)
```

*(Note on type & model names: In internal `drawlib._diagrams.class_diagram._models` or conceptual descriptions, `AttributeInfo`, `MethodInfo`, `ClassRelationship`, and the visibility literal `"+" | "-" | "#" | "~"` are also referred to as `Attribute`, `Method`, `Relationship`, and `Visibility`. Always import `AttributeInfo`, `MethodInfo`, and `ClassRelationship` from `drawlib.diagrams.class_diagram`.)*

---

## 2. Core Classes & Constructor Parameters

### 2.1 `ClassDiagram`

```python
cd = ClassDiagram(
    *,
    node_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    title: str = "",
    title_style: Style | None = None,
    style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    margin: float = 5.0,
    header_style: Style | None = None,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | `Style` | *(Required)* | Mandatory base `Style` object for `ClassNode` boxes and member typography in the diagram. |
| `edge_style` | `Style` | *(Required)* | Mandatory base `Style` object for relationship lines and UML marker heads. |
| `edge_text_style` | `Style` | *(Required)* | Mandatory base `Style` object for relationship labels, multiplicities, and role names. |
| `title` | `str` | `""` | Optional diagram title rendered at the top center. |
| `title_style` | `Style \| None` | `None` | Optional typography style for the diagram title. |
| `style` | `Style \| None` | `None` | Optional outer background card style for the diagram container. |
| `width` / `height` | `float \| None` | `None` | Optional explicit diagram dimensions override. |
| `margin` | `float` | `5.0` | Outer margin padding surrounding all classes. |
| `header_style` | `Style \| None` | `None` | Optional default `Style` overriding the top class header compartment. |

#### Diagram Registration & Sizing Methods:
- **`cd.add(class_node, xy=(0.0, 0.0), show=None) -> ClassNode`**:
  Registers a `ClassNode` centered at `xy=(cx, cy)`.
- **`cd.connect(source, target, relationship_type="association", *, type=None, label="", start_side="auto", end_side="auto", start_multiplicity="", end_multiplicity="", start_role="", end_role="", directed=False, style=None, text_style=None, routing="orthogonal", padding=0.0, show=True) -> ClassRelationship`**:
  Creates and registers a UML `ClassRelationship` between `source` and `target`.
- **`cd.add_relationship(rel) -> ClassRelationship`**:
  Registers a pre-constructed `ClassRelationship` instance.
- **`cd.get_bounds() -> tuple[float, float, float, float]`**:
  Returns `(min_x, min_y, max_x, max_y)` of the class diagram in local coordinates.
- **`cd.get_size() -> tuple[float, float]`**:
  Returns the total `(width, height)` of the class diagram in unscaled local units.
- **`cd.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0) -> None`**:
  Renders the class diagram onto the active canvas anchored at `xy` (`align: Literal["bottom_left", "center"] = "bottom_left"`, `scale: float = 1.0`).

---

### 2.2 `ClassNode` & Member Registration (`add_attribute`, `add_method`)

```python
node = ClassNode(
    name: str,
    stereotype: str = "",
    is_abstract: bool = False,
    width: float = 28.0,
    height: float | None = None,
    header_height: float | None = None,
    row_height: float = 3.2,
    style: Style | None = None,
    header_style: Style | None = None,
    show: bool = True,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Class or interface name (rendered in the top header compartment). |
| `stereotype` | `str` | `""` | Optional UML stereotype name (automatically wrapped as `<<{stereotype}>>` if not already bracketed, e.g. `"interface"`, `"dataclass"`, `"enum"`). |
| `is_abstract` | `bool` | `False` | Marks the class as abstract (adds `<<abstract>>` header tag if `stereotype` is empty). |
| `width` | `float` | `28.0` | Class box width in local units. Increase to `32.0`–`42.0` for long method signatures. |
| `height` | `float \| None` | `None` | Optional fixed height override. If `None`, auto-calculates height from header + attribute rows + method rows. |
| `header_height` | `float \| None` | `None` | Optional fixed header height override (`5.2` default, or `6.5` when a stereotype/abstract tag is shown). |
| `row_height` | `float` | `3.2` | Vertical height per attribute or method row. |
| `style` | `Style \| None` | `None` | Optional background/border style override for the class body. |
| `header_style` | `Style \| None` | `None` | Optional background/border style override for the class header compartment. |
| `show` | `bool` | `True` | Visibility flag for this class box (and its connected relationships). |

#### Fluent Member Builders & Visibility (`Visibility = Literal["+", "-", "#", "~"]`):

```python
# Add an attribute row (returns self for chaining):
node.add_attribute(
    name: str,
    type: str = "",
    is_public: bool = True,
    visibility: str | None = None,
    default_value: str = "",
    is_static: bool = False,
) -> ClassNode

# Add a method row (returns self for chaining):
node.add_method(
    name: str,
    params: str = "",
    return_type: str = "",
    is_public: bool = True,
    visibility: str | None = None,
    is_static: bool = False,
    is_abstract: bool = False,
) -> ClassNode
```

- **Visibility Resolution (`visibility: str | None = None`)**:
  - When `visibility` is explicitly passed (`"+"` public, `"-"` private, `"#"` protected, `"~"` package/internal), it takes precedence over `is_public`.
  - Otherwise, `is_public=True` resolves to `"+"` and `is_public=False` resolves to `"-"`.
- **Formatted UML Strings**:
  - Attributes render as `"{vis} {name}: {type} = {default_value}"` (underlined if `is_static=True`).
  - Methods render as `"{vis} {name}({params}): {return_type} {abstract}"` (underlined if `is_static=True`).

---

### 2.3 UML Relationships (`cd.connect()` & `RelationshipType`)

`ClassDiagram` supports all 6 canonical UML 2.0 `RelationshipType` values via `cd.connect(source, target, relationship_type=..., ...)`:

```python
rel = cd.connect(
    source: ClassNode,
    target: ClassNode,
    relationship_type: RelationshipType = "association",
    *,
    type: RelationshipType | None = None,  # Keyword alias for relationship_type
    label: str = "",
    start_side: Side = "auto",
    end_side: Side = "auto",
    start_multiplicity: str = "",
    end_multiplicity: str = "",
    start_role: str = "",
    end_role: str = "",
    directed: bool = False,
    style: Style | None = None,
    text_style: Style | None = None,
    routing: RoutingType = "orthogonal",
    padding: PaddingType = 0.0,
    show: bool = True,
) -> ClassRelationship
```

| `RelationshipType` | Line Stroke | Source Marker (`source`) | Target Marker (`target`) | Semantic Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **`"inheritance"`** | Solid | None | Hollow closed triangle (`▷`) | Subclass (`source`) extends superclass (`target`). |
| **`"realization"`** | Dashed | None | Hollow closed triangle (`▷`) | Concrete class (`source`) implements interface (`target`). |
| **`"composition"`** | Solid | Filled solid diamond (`◆`) | Open arrow (if `directed=True`) | Whole (`source`) strongly owns lifecycle of part (`target`). |
| **`"aggregation"`** | Solid | Hollow diamond (`◇`) | Open arrow (if `directed=True`) | Whole (`source`) references shared part (`target`). |
| **`"dependency"`** | Dashed | None | Open V-arrow (`>`) | Client (`source`) transiently depends on supplier (`target`). |
| **`"association"`** | Solid | None | Open V-arrow (if `directed=True`) | Structural link between `source` and `target`. |

- **Routing & Waypoints on `ClassRelationship`**:
  - `routing`: `"orthogonal"` (default) or `"direct"`.
  - `rel.points(waypoints: list[tuple[float, float]]) -> Self`, `rel.via(*waypoints: tuple[float, float]) -> Self`, `rel.set_label(label: str) -> Self`, `rel.set_style(style: Style) -> Self`, `rel.set_text_style(text_style: Style) -> Self`, `rel.set_padding(padding: PaddingType) -> Self`.

---

## 3. Production Examples

### Example 3.1: Domain Model with Interface Realization, Inheritance, Composition & Aggregation
```drawlib align=center code=fold file=class_domain_model.png caption="UML 2.0 Domain Model with Realization, Inheritance, Composition, and Aggregation"
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=156, height=96)

cd = ClassDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=9.5),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="E-Commerce Order & Repository Class Hierarchy",
)

# 1. Interface (Top-Left)
repo_iface = cd.add(
    ClassNode("OrderRepository", stereotype="interface", width=42, header_style=Styles.SecondaryNeutral)
    .add_method("find_by_id", "order_id: UUID", "Order | None")
    .add_method("save", "order: Order", "None"),
    xy=(30, 72),
)

# 2. Concrete Repository Implementing Interface (Bottom-Left)
sql_repo = cd.add(
    ClassNode("PostgresOrderRepository", width=42)
    .add_attribute("pool", "ConnectionPool", visibility="-")
    .add_method("find_by_id", "order_id: UUID", "Order | None")
    .add_method("save", "order: Order", "None"),
    xy=(30, 26),
)

# 3. Aggregate Root Entity (Top-Right)
order = cd.add(
    ClassNode("Order", width=38, header_style=Styles.PrimaryFlat)
    .add_attribute("id", "UUID", visibility="+")
    .add_attribute("status", "OrderStatus", visibility="#")
    .add_method("add_item", "sku: str, qty: int", "None")
    .add_method("total", "", "Decimal"),
    xy=(112, 72),
)

# 4. Value Object / Part Entity (Bottom-Right)
line_item = cd.add(
    ClassNode("OrderLineItem", width=38)
    .add_attribute("sku", "str", visibility="+")
    .add_attribute("qty", "int", default_value="1", visibility="+")
    .add_attribute("unit_price", "Decimal", visibility="-")
    .add_method("subtotal", "", "Decimal"),
    xy=(112, 26),
)

# UML Relationships via cd.connect()
cd.connect(sql_repo, repo_iface, "realization", start_side="top", end_side="bottom")
cd.connect(sql_repo, order, "dependency", label="<<creates>>", start_side="right", end_side="left")
cd.connect(
    order,
    line_item,
    "composition",
    start_multiplicity="1",
    end_multiplicity="1..*",
    end_role="items",
    directed=True,
    start_side="bottom",
    end_side="top",
)

cd.draw(xy=(4.0, 4.0))
canvas.save()
```
