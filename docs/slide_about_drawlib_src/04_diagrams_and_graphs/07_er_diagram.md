::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Relational Schemas & Crow's Foot (`ERDiagram`)
:::

::: block (80, 140) (640, 840) compact
## Information Engineering (IE) Database Modeling

`ERDiagram` visualizes physical and logical relational database schemas with strict Crow's Foot cardinality markers and row-aligned foreign key connectors:

### Entity & Column Capabilities
- **Auto-Height Tables**: `Entity(name="users", width=28.0)` automatically scales its vertical height based on registered columns.
- **Constraint Badges**: `entity.add_column(name, type="...", pk=True, fk=False, nullable=False)` renders `[PK]`, `[FK]`, and mandatory field indicators cleanly aligned in the right column.
- **7 Crow's Foot Cardinalities**:
  - `"1:*"` (One-to-Zero-or-More `|| ── o<`)
  - `"1:1..*"` (One-to-One-or-More `|| ── |<`)
  - `"1:1"`, `"1:0..1"`, `"0..1:1"`, `"0..1:*"`, `"*:*"`
- **Row-Exact Foreign Key Anchoring**:
  - Passing `start_column="id", end_column="user_id"` attaches the relationship wire directly to the vertical Y-center of those specific table rows!
:::

::: block (760, 140) (1080, 840)
```drawlib file:er_schema.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.styles import Styles

clear()
setup(width=108, height=84)

erd = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=7.2),
    title="Multi-Tenant E-Commerce Relational Schema (Crow's Foot)",
    title_style=Styles.DarkBold.patch(text_size=9.5),
)

# 1. Users Table (Top-Left)
users = erd.add(
    Entity(name="users", width=29.0, style=Styles.PrimaryNeutral),
    xy=(20.0, 56.0),
)
users.add_column("id", type="UUID", pk=True, nullable=False)
users.add_column("email", type="VARCHAR", nullable=False)
users.add_column("full_name", type="VARCHAR")
users.add_column("created_at", type="TIMESTAMP", nullable=False)

# 2. Orders Table (Center Hero Table)
orders = erd.add(
    Entity(name="orders", width=31.0, style=Styles.SecondaryNeutral),
    xy=(55.0, 56.0),
)
orders.add_column("id", type="UUID", pk=True, nullable=False)
orders.add_column("user_id", type="UUID", fk=True, nullable=False)
orders.add_column("status", type="VARCHAR", nullable=False)
orders.add_column("total_cents", type="BIGINT", nullable=False)

# 3. Order Items Table (Top-Right)
items = erd.add(
    Entity(name="order_items", width=31.0, style=Styles.Neutral),
    xy=(90.0, 56.0),
)
items.add_column("id", type="UUID", pk=True, nullable=False)
items.add_column("order_id", type="UUID", fk=True, nullable=False)
items.add_column("product_id", type="UUID", fk=True, nullable=False)
items.add_column("quantity", type="INT", nullable=False)

# 4. Products Table (Bottom-Right)
products = erd.add(
    Entity(name="products", width=31.0, style=Styles.BlueNeutral),
    xy=(90.0, 20.0),
)
products.add_column("id", type="UUID", pk=True, nullable=False)
products.add_column("sku", type="VARCHAR", nullable=False)
products.add_column("unit_price", type="BIGINT", nullable=False)

# 5. Payments Audit Table (Bottom-Center)
payments = erd.add(
    Entity(name="payments", width=31.0, style=Styles.TealNeutral),
    xy=(55.0, 20.0),
)
payments.add_column("id", type="UUID", pk=True, nullable=False)
payments.add_column("order_id", type="UUID", fk=True, nullable=False)
payments.add_column("stripe_tx", type="VARCHAR", nullable=False)

# Row-anchored Crow's Foot Relationships
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
products.connect(
    items,
    cardinality="1:*",
    start_side="top",
    end_side="bottom",
    label="catalog",
)
orders.connect(
    payments,
    cardinality="1:0..1",
    start_side="bottom",
    end_side="top",
    label="settled_by",
)

erd.draw(xy=(0.0, 0.0))

save()
```
:::

::: note
- Slide 7 demonstrates `ERDiagram` for relational database modeling.
- Look closely at the horizontal connections between `users -> orders` and `orders -> order_items`:
  - By specifying `start_column="id"` and `end_column="user_id"`, the orthogonal connector starts at the exact vertical height of the `id [PK]` row in `users`, steps down cleanly, and terminates with a Crow's Foot (`o<`) right at the `user_id [FK]` row in `orders`.
  - Different Crow's Foot cardinalities are shown on the same canvas: `"1:*"` (one-to-zero-or-many), `"1:1..*"` (mandatory child one-to-many), and `"1:0..1"` (optional one-to-one payment settlement).
:::
