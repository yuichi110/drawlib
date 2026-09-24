# Class Diagrams

`drawlib.diagrams.class_diagram` provides a declarative, pure-Python UML Class diagramming framework.
It supports standard UML 2.0 notations including three-compartment class cards (name, attributes, methods), stereotypes, abstract classes, and all 6 standard UML relationship types with intuitive verb-based connection methods.

---

## 1. Core Concepts

| Component | Class | Description |
|---|---|---|
| **Container** | `ClassDiagram` | Top-level container managing classes, relationships, canvas sizing, and rendering. |
| **Class Node** | `ClassNode` | Represents a class, abstract class, or interface. `(x, y)` sets the **center** of the card. |
| **Relationship** | `ClassRelationship` | An edge connecting two classes with UML markers (triangles, diamonds, arrows). |

---

## 2. Quick Start

Below is a domain model illustrating an e-commerce payment and order flow:

```drawlib show-code 650px center caption:"E-Commerce Domain Class Diagram"
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode

canvas.initialize()

cd = ClassDiagram(title="E-Commerce Domain Model")

# 1. Define Class Nodes
user = cd.add(ClassNode(name="User", width=28.0), xy=(22.0, 60.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("name", type="str", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", params="password: str", return_type="bool")
user.add_method("logout", return_type="void")

customer = cd.add(ClassNode(name="Customer", width=28.0), xy=(22.0, 20.0))
customer.add_attribute("address", type="str")
customer.add_attribute("phone", type="str")
customer.add_method("checkout", return_type="Order")

order = cd.add(ClassNode(name="Order", width=28.0), xy=(75.0, 20.0))
order.add_attribute("order_id", type="str")
order.add_attribute("total", type="float")
order.add_method("calculate_tax", return_type="float")
order.add_method("pay", return_type="bool")

payment_service = cd.add(
    ClassNode(name="PaymentService", stereotype="interface", width=30.0),
    xy=(75.0, 60.0),
)
payment_service.add_method("process_payment", params="amount: float", return_type="bool")

# 2. Connect with Intuitive Verb Methods
# Customer inherits User (Generalization)
customer.inherit(user, start_side="top", end_side="bottom")

# Customer composes Order (Whole to Part)
customer.composite(
    order,
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="places",
)

# Order depends on PaymentService (Dependency)
order.depend(payment_service, start_side="top", end_side="bottom", label="uses")

cd.draw(xy=(0.0, 0.0))
```

---

## 3. ClassNode Configuration

### 3.1 Adding Attributes

Attributes can be added individually via `add_attribute()` or in batch using `add_attributes()`.
By default, `is_public=True` prepends `+`, while `is_public=False` prepends `-`. Explicit symbols (`+`, `-`, `#`, `~`) can also be specified:

```python
class_node = ClassNode(name="Account")

# Individual addition (fluent API)
class_node.add_attribute("id", type="int", is_public=True)        # "+ id: int"
class_node.add_attribute("balance", type="float", is_public=False)  # "- balance: float"
class_node.add_attribute("token", visibility="#")                 # "# token"
class_node.add_attribute("count", type="int", is_static=True, default_value="0") # "+ count: int = 0 {static}"

# Batch addition
class_node.add_attributes([
    ("email", "str", True),
    ("secret_key", "str", False),
])
```

### 3.2 Adding Methods

Methods can be added individually via `add_method()` or in batch using `add_methods()`:

```python
class_node = ClassNode(name="OrderService")

class_node.add_method("create", params="cart: Cart", return_type="Order")
class_node.add_method("validate", params="order: Order", return_type="bool", is_public=False)
class_node.add_method("get_instance", return_type="OrderService", is_static=True)
class_node.add_method("process", return_type="void", is_abstract=True)
```

### 3.3 Stereotypes and Abstract Classes

- **Stereotype**: Pass `stereotype="interface"` or `stereotype="enumeration"` to display `«stereotype»` above the class name.
- **Abstract Class**: Pass `is_abstract=True` to indicate an abstract class (displays `«abstract»` in the header).

```python
interface_node = ClassNode(name="Repository", stereotype="interface")
abstract_node = ClassNode(name="BaseEntity", is_abstract=True)
```

---

## 4. Relationship Types and Verb Methods

Drawlib provides intuitive verb methods on `ClassNode` to create UML relationships directly:

| Verb Method | UML Relationship | Line Style | Marker | Description |
|---|---|---|---|---|
| `child.inherit(parent)` | **Inheritance** (Generalization) | Solid | Hollow Triangle (at parent) | Superclass / Subclass relationship |
| `impl.realize(iface)` | **Realization** (Implementation) | Dashed | Hollow Triangle (at interface) | Interface realization |
| `whole.composite(part)` | **Composition** | Solid | Filled Diamond (at whole) | Strong ownership; part dies with whole |
| `whole.aggregate(part)` | **Aggregation** | Solid | Hollow Diamond (at whole) | Shared ownership / part-whole |
| `c1.associate(c2)` | **Association** | Solid | None (or Open Arrow if `directed=True`) | Structural relationship |
| `client.depend(supplier)` | **Dependency** | Dashed | Open Arrow (at supplier) | Client uses / depends on supplier |

```drawlib show-code 650px center caption:"All 6 UML Relationship Types"
from drawlib import canvas
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode, RelationshipType

canvas.initialize()

types: list[RelationshipType] = [
    "inheritance",
    "realization",
    "composition",
    "aggregation",
    "association",
    "dependency",
]

cd = ClassDiagram(title="UML Relationship Types Gallery")

for idx, rel_type in enumerate(types):
    y = 78.0 - idx * 12.0
    src = cd.add(ClassNode(name=f"Source_{idx}", width=22.0, height=7.0), xy=(25.0, y))
    tgt = cd.add(ClassNode(name=f"Target_{idx}", width=22.0, height=7.0), xy=(75.0, y))

    src.connect(
        tgt,
        relationship_type=rel_type,
        start_side="right",
        end_side="left",
        label=rel_type,
        start_multiplicity="1" if rel_type in {"composition", "aggregation"} else "",
        end_multiplicity="*" if rel_type in {"composition", "aggregation"} else "",
    )

cd.draw()
```

---

## 5. Multiplicities, Roles, and Labels

Relationships support UML multiplicity strings, role names, and central labels:

- `start_multiplicity`: e.g. `"1"`, `"0..1"`
- `end_multiplicity`: e.g. `"*"`, `"1..*"`, `"0..*"`
- `start_role`: e.g. `"+owner"`, `"publisher"`
- `end_role`: e.g. `"+subscribers"`, `"listener"`
- `label`: Text badge displayed centered along the connection line

```python
publisher.associate(
    subscriber,
    start_multiplicity="1",
    end_multiplicity="*",
    start_role="pub",
    end_role="+subs",
    label="notifies",
    directed=True,
)
```

---

## 6. Routing and Anchoring

### 6.1 Orthogonal vs Direct Routing

- `routing="orthogonal"` (default): Smart right-angled routing with clean right-angle bends.
- `routing="direct"`: Draws straight lines directly connecting classes. The line endpoints are automatically clipped at the exact outer boundary of each class card.

### 6.2 Attachment Sides

Sides can be explicitly set with `start_side` and `end_side`:
- `"left"`, `"right"`, `"top"`, `"bottom"`, or `"auto"` (default).

When `"auto"` is used, Drawlib automatically chooses the nearest complementary sides based on relative coordinates.

---

## 7. Custom Styling

Classes and relationships fully integrate with Drawlib's `Style` class:

```drawlib show-code 650px center caption:"Styled UML Class Diagram"
from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode

canvas.initialize()

cd = ClassDiagram(
    title="Custom Styled Payment Architecture",
    style=Style(fill_color=Colors.White),
)

processor = cd.add(
    ClassNode(
        name="PaymentProcessor",
        stereotype="interface",
        width=30.0,
        header_style=Style(fill_color=Colors.Teal, text_color=Colors.White),
    ),
    xy=(50.0, 65.0),
)
processor.add_method("process_payment", params="amount: float", return_type="bool")

stripe = cd.add(
    ClassNode(
        name="StripeService",
        width=26.0,
        header_style=Style(fill_color=Colors.Navy, text_color=Colors.White),
    ),
    xy=(25.0, 22.0),
)
stripe.add_attribute("api_key", type="str", is_public=False)
stripe.add_method("process_payment", params="amount: float", return_type="bool")

paypal = cd.add(
    ClassNode(
        name="PayPalService",
        width=26.0,
        header_style=Style(fill_color=Colors.Blue, text_color=Colors.White),
    ),
    xy=(75.0, 22.0),
)
paypal.add_attribute("client_id", type="str", is_public=False)
paypal.add_method("process_payment", params="amount: float", return_type="bool")

stripe.realize(
    processor,
    routing="direct",
    style=Style(line_color=Colors.Navy, line_width=2.0),
    padding=1.0,
)
paypal.realize(
    processor,
    routing="direct",
    style=Style(line_color=Colors.Blue, line_width=2.0),
    padding=1.0,
)

cd.draw()
```
