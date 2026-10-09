# ERDiagram: Relational Schemas & Crow's Foot Notations

`ERDiagram` visualizes relational database architectures adhering strictly to **Information Engineering (IE) / Crow's Foot notation**—the industry standard for physical database schema modeling.

---

## 1. Overview & Crow's Foot Notation

```drawlib fold-code 650px center file:er_overview_anatomy.png caption:"Entity-Relationship Tables with Row-Anchored Crow's Foot Notation"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import ERDiagram, Entity
from drawlib.styles import Styles

setup(width=106, height=44)

er = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
)

users = er.add(Entity(name="users", width=32.0), xy=(21.0, 22.0))
users.add_column("id", type="INT", pk=True)
users.add_column("email", type="VARCHAR(255)", nullable=False)
users.add_column("name", type="VARCHAR(100)")

orders = er.add(Entity(name="orders", width=32.0, style=Styles.PrimaryNeutral), xy=(85.0, 22.0))
orders.add_column("id", type="INT", pk=True)
orders.add_column("user_id", type="INT", fk=True)
orders.add_column("total", type="DECIMAL(10,2)", nullable=False)

users.connect(
    orders,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="user_id",
    label="places",
)

er.draw(xy=(0.0, 0.0))
save()
```

- **Information Engineering (IE) Standard**: Uses standard Crow's Foot vector markers (double vertical bar for exactly one, circle + crow's foot for zero or many, bar + crow's foot for one or many, and circle + bar for zero or one).
- **Column-Level Anchoring**: Rather than connecting to arbitrary points on the table perimeter, Drawlib allows you to anchor lines directly to the specific primary key and foreign key table rows (`start_column="id"`, `end_column="user_id"`).
- **Key Badges**: Automatically renders `[PK]` and `[FK]` tags next to column definitions with syntax highlighting.

---

## 2. Constructor & Entity Definition

```drawlib show-code 550px center file:er_basic_entity.png caption:"Basic Entity Table"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import ERDiagram, Entity
from drawlib.styles import Styles

setup(width=50, height=45)

er = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="User Schema",
)

# Create entity table
users = er.add(Entity(name="users", width=30.0), xy=(25.0, 18.0))
users.add_column("id", type="INT", pk=True)
users.add_column("email", type="VARCHAR(255)", nullable=False)
users.add_column("created_at", type="TIMESTAMP")

er.draw(xy=(0.0, 0.0))
save()
```

### Parameter Reference Tables

#### `ERDiagram` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `node_style` | `Style` | *(Required)* | Base `Style` object for entity table cards in the diagram. |
| `edge_style` | `Style` | *(Required)* | Base `Style` object for relationship lines and Crow's Foot markers. |
| `edge_text_style` | `Style` | *(Required)* | Base `Style` object for relationship labels. |
| `title` | `str` | `""` | Optional banner title displayed above the diagram. |
| `title_style` | `Style \| None` | `None` | Optional `Style` object for the diagram title. |
| `width` | `float \| None` | `None` | Optional fixed width of the diagram (auto-fit if `None`). |
| `height` | `float \| None` | `None` | Optional fixed height of the diagram (auto-fit if `None`). |
| `style` | `Style \| None` | `None` | Optional `Style` object for the diagram background card. |
| `header_style` | `Style \| None` | `None` | Optional `Style` overriding entity card header bands across the diagram. |

#### `Entity` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | *(Required)* | Table / entity name displayed in the header band. |
| `width` | `float` | `25.0` | Table bounding box width in canvas units. |
| `height` | `float \| None` | `None` | Optional minimum height override (auto-expands to fit all columns if `None` or smaller). |
| `size` | `tuple[float, float] \| None` | `None` | Optional `(width, height)` shorthand tuple overriding `width` and `height`. |
| `header_height` | `float` | `4.0` | Height of the entity title header compartment. |
| `row_height` | `float` | `3.2` | Vertical height of each column row. |
| `style` | `Style \| None` | `None` | Optional `Style` for the main entity box and border. |
| `header_style` | `Style \| None` | `None` | Optional `Style` for this entity's header background and text. |
| `show` | `bool` | `True` | Visibility flag (connected `Relationship` lines auto-hide when `False`). |

#### Column Declaration (`add_column`, `add_columns` & `ColumnInfo`)
| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | *(Required)* | Column field name. |
| `type` | `str` | `""` | SQL data type string (e.g. `"INT"`, `"VARCHAR(255)"`). |
| `pk` | `bool` | `False` | When `True`, displays the `[PK]` primary key badge. |
| `fk` | `bool` | `False` | When `True`, displays the `[FK]` foreign key badge. |
| `nullable` | `bool` | `True` | Whether the column allows `NULL` values. |

```python
from drawlib.diagrams.er import ColumnInfo

# Single column & batch column registration
entity.add_column(name: str, type: str = "", pk: bool = False, fk: bool = False, nullable: bool = True) -> Entity
entity.add_columns(
    columns: Sequence[Sequence[Any] | ColumnInfo],
    # Each item is a ColumnInfo or tuple (name, [type, pk, fk, nullable])
) -> Entity
```

#### `Relationship` (`entity.connect` & `er.connect`)
| Parameter | Type | Default | Description |
|---|---|---|---|
| `start` / `target` | `Entity` | *(Required)* | Source and target `Entity` tables (`entity.connect(target, ...)` or `er.connect(start, end, ...)`). |
| `cardinality` | `Cardinality` | `"1:*"` | Crow's Foot multiplicity (`"1:*"`, `"1:1"`, `"1:1..*"`, `"1:0..1"`, `"0..1:1"`, `"0..1:*"`, `"*:*"`). |
| `start_side` | `Literal["left", "right", "top", "bottom", "auto"]` | `"auto"` | Attachment side on the source entity perimeter. |
| `end_side` | `Literal["left", "right", "top", "bottom", "auto"]` | `"auto"` | Attachment side on the target entity perimeter. |
| `start_column` | `str \| None` | `None` | Optional column name in `start` entity to anchor the wire directly to that row. |
| `end_column` | `str \| None` | `None` | Optional column name in `end` entity to anchor the wire directly to that row. |
| `label` | `str` | `""` | Optional relationship text label along the connection line. |
| `style` | `Style \| None` | `None` | Optional `Style` override for the relationship line and Crow's Foot markers. |
| `text_style` | `Style \| None` | `None` | Optional `Style` override for the relationship label text. |
| `routing` | `Literal["orthogonal", "direct"]` | `"orthogonal"` | Line routing strategy (`"orthogonal"` Z-bends or `"direct"` straight line). |
| `padding` | `float \| tuple[float, float]` | `0.0` | Gap distance between entity borders and line endpoints. |
| `show` | `bool` | `True` | Visibility flag for the relationship line. |

#### Registration, Sizing & Rendering Methods
- **`er.add(entity, xy=(cx, cy), show: bool | None = None) -> Entity`**: Places an entity table centered at `(cx, cy)` and returns the mutable `Entity`.
- **`entity.connect(target, cardinality="1:*", ..., show=True) -> Relationship`** or **`er.connect(start, end, cardinality="1:*", ..., show=True) -> Relationship`** (and `er.add_relationship(rel) -> Relationship`): Connects two entities with Crow's Foot notation and returns a mutable `Relationship` (`rel.show`, `rel.style`, `rel.text_style`).
- **`er.get_size() -> tuple[float, float]`**: Returns the overall `(width, height)` of the diagram.
- **`er.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: Renders the ER diagram anchored at bottom-left `xy`, proportionally scaling table geometry, Crow's Foot markers, and font sizes by `scale`.

---

## 3. Supported Cardinality Notations

| Cardinality String | Parent Marker | Child Marker | Standard Semantics |
|---|---|---|---|
| `"1:*"` | One (double vertical bar) | Zero or Many (circle + crow's foot) | One-to-Many (Default) |
| `"1:1"` | One (double vertical bar) | One (double vertical bar) | One-to-One |
| `"1:1..*"` | One (double vertical bar) | One or Many (bar + crow's foot) | Mandatory Child One-to-Many |
| `"1:0..1"` | One (double vertical bar) | Zero or One (circle + bar) | Optional Child One-to-One |
| `"0..1:1"` | Zero or One (circle + bar) | One (double vertical bar) | Optional Parent One-to-One |
| `"0..1:*"` | Zero or One (circle + bar) | Zero or Many (circle + crow's foot) | Optional Parent One-to-Many |
| `"*:*"` | Zero or Many (circle + crow's foot) | Zero or Many (circle + crow's foot) | Many-to-Many |

```drawlib show-code 650px center file:er_cardinality_notations.png caption:"All Seven Crow's Foot Cardinality Notations in ERDiagram"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import ERDiagram, Entity
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=158, height=112)

er = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
)

# 7 supported Crow's Foot cardinality strings arranged in a clean 2-column catalog
specs = [
    # Left column (x_src=16, x_dst=58)
    ('"1:*"  (One-to-Many)', "1:*", 16.0, 58.0, 92.0, "Parent", "Child"),
    ('"1:1"  (One-to-One)', "1:1", 16.0, 58.0, 66.0, "Parent", "Child"),
    ('"1:1..*"  (Mandatory Child)', "1:1..*", 16.0, 58.0, 40.0, "Parent", "Child"),
    ('"1:0..1"  (Optional Child)', "1:0..1", 16.0, 58.0, 14.0, "Parent", "Child"),
    # Right column (x_src=96, x_dst=138)
    ('"0..1:1"  (Optional Parent 1:1)', "0..1:1", 96.0, 138.0, 92.0, "Parent", "Child"),
    ('"0..1:*"  (Optional Parent 1:N)', "0..1:*", 96.0, 138.0, 66.0, "Parent", "Child"),
    ('"*:*"  (Many-to-Many)', "*:*", 96.0, 138.0, 40.0, "Left", "Right"),
]

lbl_style = Styles.DarkBold.patch(text_size=9.0, text_color=Colors.Primary5)

for _title_str, card, x1, x2, y, src_name, dst_name in specs:
    e_src = er.add(Entity(name=src_name, width=16.0, style=Styles.PrimaryNeutral), xy=(x1, y))
    e_dst = er.add(Entity(name=dst_name, width=16.0, style=Styles.Neutral), xy=(x2, y))
    e_src.connect(e_dst, cardinality=card, start_side="right", end_side="left")

er.draw(xy=(0.0, 0.0))

for title_str, _card, x1, x2, y, _src_name, _dst_name in specs:
    text(((x1 + x2) / 2.0, y + 6.5), title_str, style=lbl_style)

save()
```

---

## 4. E-Commerce Relational Schema with Column Anchors

The following four-table schema (`users`, `orders`, `order_items`, and `products`) anchors every relationship directly to its primary and foreign key rows:

```drawlib show-code 650px center file:er_ecommerce_schema.png caption:"E-Commerce Relational Database Schema"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import ERDiagram, Entity
from drawlib.styles import Styles

setup(width=128, height=96)

er = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="E-Commerce Relational Database Schema",
)

# Top row: users (left) -> orders (right)
users = er.add(Entity(name="users", width=34.0), xy=(26.0, 66.0))
users.add_column("id", type="INT", pk=True)
users.add_column("email", type="VARCHAR(255)", nullable=False)
users.add_column("name", type="VARCHAR(100)")
users.add_column("created_at", type="TIMESTAMP")

orders = er.add(Entity(name="orders", width=34.0, style=Styles.PrimaryNeutral), xy=(100.0, 66.0))
orders.add_column("id", type="INT", pk=True)
orders.add_column("user_id", type="INT", fk=True)
orders.add_column("total_cents", type="INT", nullable=False)
orders.add_column("status", type="VARCHAR(32)")

# Bottom row: products (left) -> order_items (right)
products = er.add(Entity(name="products", width=34.0), xy=(26.0, 22.0))
products.add_column("id", type="INT", pk=True)
products.add_column("sku", type="VARCHAR(64)", nullable=False)
products.add_column("title", type="VARCHAR(200)")
products.add_column("price_cents", type="INT", nullable=False)

order_items = er.add(Entity(name="order_items", width=34.0, style=Styles.SecondaryNeutral), xy=(100.0, 22.0))
order_items.add_column("id", type="INT", pk=True)
order_items.add_column("order_id", type="INT", fk=True)
order_items.add_column("product_id", type="INT", fk=True)
order_items.add_column("quantity", type="INT", nullable=False)

# Row-anchored relationships
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
    order_items,
    cardinality="1:1..*",
    start_side="bottom",
    end_side="top",
    label="contains",
)
products.connect(
    order_items,
    cardinality="1:*",
    start_side="right",
    end_side="left",
    start_column="id",
    end_column="product_id",
    label="referenced by",
)

er.draw(xy=(0.0, 0.0))
save()
```

---

## 5. Best Practices & Guidelines

1. **Always Use Column Anchoring**: Supplying `start_column` and `end_column` visually connects the specific foreign key attribute to its referenced primary key, making schemas intuitive and professional.
2. **Width Budgeting**: Tables with long data types (e.g., `VARCHAR(255)`) look best with a `width` of `28.0` to `34.0` canvas units.
3. **Cardinality Strings**: Always use explicit cardinality strings (`"1:*"`, `"1:1"`, etc.) rather than manual arrow heads.
