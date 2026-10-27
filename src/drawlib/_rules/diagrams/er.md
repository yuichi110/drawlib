# Drawlib ERDiagram Guidelines (`lib-diagrams-er`)

`drawlib.diagrams.er` models relational database schemas and data models using Information Engineering (IE / Crow's Foot) notation. It renders multi-column table cards (`Entity`) with automatic `PK` / `FK` / `NN` / `UQ` constraint alignment and supports row-accurate column-to-column foreign key routing (`start_column`, `end_column`).

```text
  ┌──────────────────────────────────┐            ┌──────────────────────────────────┐
  │              users               │            │              orders              │
  ├───────┬──────────────┬───────────┤            ├───────┬──────────────┬───────────┤
  │ PK    │ id           │ UUID (NN) ├──────┐     │ PK    │ id           │ UUID (NN) │
  │ UQ    │ email        │ VARCHAR   │   1  │     │ FK    │ user_id      │ UUID (NN) │
  │       │ created_at   │ TIMESTAMP │      └────<│       │ total_cents  │ INT (NN)  │
  └───────┴──────────────┴───────────┘       0..* └───────┴──────────────┴───────────┘
```

---

## 1. Public Exports & Imports

```python
from drawlib.diagrams.er import (
    Cardinality,
    ColumnInfo,
    Entity,
    ERDiagram,
    Relationship,
    RoutingType,
    Side,
)
```

*(Note on model naming: In conceptual specs, `ColumnInfo` is sometimes referred to as `Column`. Always import `ColumnInfo` from `drawlib.diagrams.er` or register columns via `entity.add_column(...)`.)*

---

## 2. Core Classes & Constructor Parameters

### 2.1 `ERDiagram`

```python
erd = ERDiagram(
    *,
    node_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    title: str = "",
    title_style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    header_style: Style | None = None,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | `Style` | *(Required)* | Mandatory base `Style` object for `Entity` table cards and column typography. |
| `edge_style` | `Style` | *(Required)* | Mandatory base `Style` object for relationship lines and Crow's Foot markers. |
| `edge_text_style` | `Style` | *(Required)* | Mandatory base `Style` object for relationship labels. |
| `title` | `str` | `""` | Optional diagram title rendered at the top center. |
| `title_style` | `Style \| None` | `None` | Optional typography style for the diagram title. |
| `width` / `height` | `float \| None` | `None` | Optional explicit diagram dimensions override. |
| `style` | `Style \| None` | `None` | Optional outer background card style for the diagram container. |
| `header_style` | `Style \| None` | `None` | Optional default `Style` overriding entity card header banners. |

#### Diagram Registration & Sizing Methods:
- **`erd.add(entity, xy, show=None) -> Entity`**:
  Registers an `Entity` table centered at `xy=(cx, cy)`.
- **`erd.connect(start, end, cardinality="1:*", start_side="auto", end_side="auto", start_column=None, end_column=None, label="", style=None, text_style=None, routing="orthogonal", padding=0.0, show=True) -> Relationship`**:
  Creates and registers a Crow's Foot `Relationship` between `start` and `end`.
- **`erd.add_relationship(relationship) -> Relationship`**:
  Registers a pre-constructed `Relationship` instance.
- **`erd.get_size() -> tuple[float, float]`**:
  Returns the total `(width, height)` of the ER diagram in unscaled local units.
- **`erd.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0) -> None`**:
  Renders the ER diagram onto the active canvas anchored at `xy` (`align: Literal["bottom_left", "center"] = "bottom_left"`, `scale: float = 1.0`).

---

### 2.2 `Entity` & Column Registration (`add_column`, `add_columns`)

```python
entity = Entity(
    name: str,
    width: float = 25.0,
    height: float | None = None,
    header_height: float = 4.0,
    row_height: float = 3.2,
    style: Style | None = None,
    header_style: Style | None = None,
    show: bool = True,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Database table / entity name rendered in the top header banner. |
| `width` | `float` | `25.0` | Table box width in local units. Increase to `28.0`–`38.0` when displaying SQL types and constraints. |
| `height` | `float \| None` | `None` | Optional fixed table height override. If `None`, auto-calculates height as `header_height + max(len(columns), 1) * row_height`. |
| `header_height` | `float` | `4.0` | Height of the top table title banner. |
| `row_height` | `float` | `3.2` | Vertical height per column row. |
| `style` | `Style \| None` | `None` | Optional background/border style override for the table body. |
| `header_style` | `Style \| None` | `None` | Optional background/border style override for the table header banner. |
| `show` | `bool` | `True` | Visibility flag for this table (and its connected relationships). |

#### Fluent Column Builder (`entity.add_column` & `entity.add_columns`):

```python
entity.add_column(
    name: str,
    type: str = "",
    pk: bool = False,
    fk: bool = False,
    nullable: bool = True,
) -> Entity

entity.add_columns(
    columns: Sequence[Sequence[Any] | ColumnInfo],
) -> Entity
```

- **3-Subcolumn Table Alignment**:
  - **Left badge slot**: Displays `"PK"`, `"FK"`, or `"PK,FK"`.
  - **Middle name slot**: Displays the column `name` (in bold when `pk=True`).
  - **Right type slot**: Displays `{type}` with `(NN)` when `nullable=False`.

---

### 2.3 Crow's Foot Relationships (`erd.connect()`, `entity.connect()`, `Cardinality`)

Relationships can be created via `erd.connect(start, end, ...)` or directly on a registered `Entity` via `entity.connect(target, ...)`:

```python
# Via ERDiagram:
rel = erd.connect(
    start: Entity,
    end: Entity,
    cardinality: Cardinality = "1:*",
    start_side: Side = "auto",
    end_side: Side = "auto",
    start_column: str | None = None,
    end_column: str | None = None,
    label: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    routing: RoutingType = "orthogonal",
    padding: PaddingType = 0.0,
    show: bool = True,
) -> Relationship

# Via Entity (requires entity or target to be registered on erd via erd.add(entity, xy)):
rel = entity.connect(
    target: Entity,
    cardinality: Cardinality = "1:*",
    start_side: Side = "auto",
    end_side: Side = "auto",
    start_column: str | None = None,
    end_column: str | None = None,
    label: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    routing: RoutingType = "orthogonal",
    padding: PaddingType = 0.0,
    show: bool = True,
) -> Relationship
```

#### Supported `Cardinality` Values:
`Cardinality = Literal["1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*"]`

| `Cardinality` | Source Marker (`start`) | Target Marker (`end`) | Relational Meaning |
| :--- | :--- | :--- | :--- |
| **`"1:1"`** | Mandatory One (`\|\|`) | Mandatory One (`\|\|`) | Strict 1-to-1 relationship |
| **`"1:0..1"`** / **`"0..1:1"`** | Mandatory One (`\|\|`) | Optional Zero-or-One (`o\|`) | Nullable 1-to-1 relationship |
| **`"1:*"`** | Mandatory One (`\|\|`) | Many (`\|<`) | Standard 1-to-Many foreign key |
| **`"1:1..*"`** | Mandatory One (`\|\|`) | Mandatory One-or-Many (`\|<`) | 1-to-Many (at least one child row) |
| **`"0..1:*"`** | Optional Zero-or-One (`o\|`) | Many (`\|<`) | Optional parent to many child rows |
| **`"*:*"`** | Many (`>\|`) | Many (`\|<`) | Many-to-Many relationship |

- **Column-Level Row Anchoring (`start_column`, `end_column`)**:
  Pass a column name (`str`, e.g. `start_column="id"`, `end_column="user_id"`) to anchor the Crow's Foot connector directly to the exact vertical `Y` coordinate of that column row on the left or right edge of the table!
- **`Relationship` Fluent Methods**:
  - `rel.points(waypoints: list[tuple[float, float]]) -> Self`, `rel.via(*waypoints: tuple[float, float]) -> Self`, `rel.set_label(label: str) -> Self`, `rel.set_style(style: Style) -> Self`, `rel.set_text_style(text_style: Style) -> Self`, `rel.set_padding(padding: PaddingType) -> Self`.

---

## 3. Production Examples

### Example 3.1: E-Commerce Relational Schema with Column-Level Foreign Key Anchoring
```drawlib align=center code=fold file=er_ecommerce_schema.png caption="Relational Database Schema with Crow's Foot Notation and Column-Level Anchoring"
from drawlib import canvas
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=158, height=92)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=9.5),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="E-Commerce Relational Schema (Crow's Foot & Column Anchoring)",
)

users = erd.add(
    Entity("users", width=36)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("email", "VARCHAR(255)", nullable=False)
    .add_column("full_name", "VARCHAR(120)", nullable=False)
    .add_column("created_at", "TIMESTAMPTZ", nullable=False),
    xy=(26, 62),
)

orders = erd.add(
    Entity("orders", width=38, header_style=Styles.PrimaryFlat)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("user_id", "UUID", fk=True, nullable=False)
    .add_column("status", "VARCHAR(32)", nullable=False)
    .add_column("total_cents", "BIGINT", nullable=False)
    .add_column("placed_at", "TIMESTAMPTZ", nullable=False),
    xy=(79, 62),
)

order_items = erd.add(
    Entity("order_items", width=38)
    .add_column("id", "BIGSERIAL", pk=True, nullable=False)
    .add_column("order_id", "UUID", fk=True, nullable=False)
    .add_column("product_id", "UUID", fk=True, nullable=False)
    .add_column("quantity", "INT", nullable=False)
    .add_column("unit_cents", "BIGINT", nullable=False),
    xy=(132, 62),
)

products = erd.add(
    Entity("products", width=38, header_style=Styles.SecondaryNeutral)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("sku", "VARCHAR(64)", nullable=False)
    .add_column("title", "VARCHAR(200)", nullable=False)
    .add_column("price_cents", "BIGINT", nullable=False),
    xy=(79, 20),
)

# Column-to-column anchored Crow's Foot relationships
users.connect(
    orders,
    cardinality="1:*",
    start_column="id",
    end_column="user_id",
    start_side="right",
    end_side="left",
)
orders.connect(
    order_items,
    cardinality="1:1..*",
    start_column="id",
    end_column="order_id",
    start_side="right",
    end_side="left",
)
erd.connect(
    products,
    order_items,
    cardinality="1:*",
    start_column="id",
    end_column="product_id",
    start_side="right",
    end_side="left",
)

erd.draw(xy=(4.0, 4.0))
canvas.save()
```
