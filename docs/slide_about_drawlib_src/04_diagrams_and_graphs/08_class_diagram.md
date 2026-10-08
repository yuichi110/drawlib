::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# UML 2.0 Object-Oriented Models (`ClassDiagram`)
:::

::: block (80, 140) (640, 840) compact
## Three-Compartment Classes & 6 UML Connectors

`ClassDiagram` models object-oriented domain architectures, design patterns, and SDK type hierarchies in standard UML 2.0 notation:

### `ClassNode` Structure
- **Header Compartment**: Supports `stereotype="interface"` (`«interface»`) and `is_abstract=True` (`«abstract»`).
- **Attributes (`add_attribute`)**: Automatic visibility prefixes (`+` public, `-` private) and static underlines.
- **Methods (`add_method`)**: Parameter signatures, return types, and abstract method styling.

### All 6 Standard UML Relationship Types
| `relationship_type` | Line & Marker | Semantics |
| :--- | :--- | :--- |
| `"inheritance"` | Solid + Hollow Triangle | Subclass generalizes superclass |
| `"realization"` | Dashed + Hollow Triangle | Concrete class implements interface |
| `"composition"` | Solid + Filled Diamond | Strong lifecycle ownership (`1..*`) |
| `"aggregation"` | Solid + Hollow Diamond | Shared collection reference |
| `"association"` | Solid Line / Arrow | Structural field link |
| `"dependency"` | Dashed + Open Arrow | Method/parameter dependency |
:::

::: block (760, 140) (1080, 840)
```drawlib file:class_uml.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

clear()
setup(width=108, height=84)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=7.0),
    title="Payment & Order Domain Model (UML 2.0 ClassDiagram)",
    title_style=Styles.DarkBold.patch(text_size=9.5),
)

# 1. Top-Left: Abstract Base Entity (Inheritance target)
base_entity = cd.add(
    ClassNode(
        name="AuditableEntity",
        is_abstract=True,
        width=30.0,
        style=Styles.Neutral,
    ),
    xy=(21.0, 58.0),
)
base_entity.add_attribute("id", type="UUID", is_public=True)
base_entity.add_attribute("created_at", type="datetime", is_public=True)
base_entity.add_method("validate", return_type="bool", is_abstract=True)

# 2. Bottom-Left: Order Aggregate Root (Inherits AuditableEntity)
order = cd.add(
    ClassNode(
        name="Order",
        width=30.0,
        style=Styles.PrimaryNeutral,
    ),
    xy=(21.0, 20.0),
)
order.add_attribute("customer_id", type="UUID", is_public=True)
order.add_attribute("status", type="OrderStatus", is_public=False)
order.add_method("total_amount", return_type="Decimal")
order.add_method("checkout", params="gw: PaymentGateway", return_type="Receipt")

# 3. Bottom-Right: LineItem (Composed by Order 1 -> 1..*)
line_item = cd.add(
    ClassNode(
        name="LineItem",
        width=30.0,
        style=Styles.SecondaryNeutral,
    ),
    xy=(82.0, 20.0),
)
line_item.add_attribute("sku", type="str", is_public=True)
line_item.add_attribute("qty", type="int", is_public=True)
line_item.add_attribute("unit_price", type="Decimal", is_public=True)
line_item.add_method("subtotal", return_type="Decimal")

# 4. Top-Center: PaymentGateway Interface
gateway_iface = cd.add(
    ClassNode(
        name="PaymentGateway",
        stereotype="interface",
        width=30.0,
        style=Styles.BlueNeutral,
    ),
    xy=(54.0, 58.0),
)
gateway_iface.add_method("authorize", params="amt: Decimal", return_type="TxToken")
gateway_iface.add_method("capture", params="token: TxToken", return_type="Receipt")

# 5. Top-Right: Concrete StripeGateway (Realizes PaymentGateway)
stripe_gw = cd.add(
    ClassNode(
        name="StripeGateway",
        width=28.0,
        style=Styles.TealNeutral,
    ),
    xy=(90.0, 58.0),
)
stripe_gw.add_attribute("api_secret", type="str", is_public=False)
stripe_gw.add_method("authorize", params="amt: Decimal", return_type="TxToken")

# UML Relationships: inheritance, realization, composition, dependency
cd.connect(order, base_entity, "inheritance", start_side="top", end_side="bottom")
cd.connect(stripe_gw, gateway_iface, "realization", start_side="left", end_side="right")
cd.connect(
    order,
    line_item,
    "composition",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="1..*",
    label="contains",
)
cd.connect(
    order,
    gateway_iface,
    "dependency",
    start_side="right",
    end_side="bottom",
    label="uses",
)

cd.draw(xy=(0.0, 0.0))

save()
```
:::

::: note
- Slide 8 demonstrates `ClassDiagram` modeling an object-oriented Payment & Order domain.
- Notice how four core UML 2.0 relationships are rendered with exact marker geometries:
  1. **`"inheritance"`**: `Order` extends the abstract class `AuditableEntity` (`«abstract»`) via a solid line and hollow triangle.
  2. **`"realization"`**: `StripeGateway` implements `PaymentGateway` (`«interface»`) via a dashed line and hollow triangle.
  3. **`"composition"`**: `Order` owns `1..*` `LineItem` instances via a filled diamond marker at the `Order` source port.
  4. **`"dependency"`**: `Order.checkout(gw: PaymentGateway)` depends on `PaymentGateway` via a dashed open-arrow connector.
:::
