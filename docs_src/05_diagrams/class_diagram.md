# ClassDiagram: UML 2.0 Class Hierarchies & Relationships

`ClassDiagram` implements standard UML 2.0 Object-Oriented structural modeling. It features three-compartment class cards (class name, attributes, methods), stereotypes, abstract classes, and all 6 standard UML relationships via intuitive verb methods.

---

## 1. Overview & Three-Compartment Cards

```text
   ┌──────────────────────────┐
   │       «interface»        │
   │      PaymentService      │
   ├──────────────────────────┤
   │ + pay(amount): bool      │
   └─────────────▲────────────┘
                 ┆ (Realization: .realize())
   ┌─────────────┴────────────┐            1            * ┌──────────────────────────┐
   │      StripeService       │◆─────────────────────────►│        Transaction       │
   ├──────────────────────────┤   (Composition:           ├──────────────────────────┤
   │ - api_key: str           │    .composite())          │ - id: str                │
   ├──────────────────────────┤                           │ - amount: float          │
   │ + pay(amount): bool      │                           └──────────────────────────┘
   └──────────────────────────┘
```

- **Three Compartments**: Class cards automatically separate the class title/stereotype header, attribute declarations, and method signatures into distinct compartments with divider lines.
- **Access Modifiers**: Supports standard UML visibility prefixes: `+` (public), `-` (private), `#` (protected), `~` (package).
- **Dynamic Sizing**: The card height automatically expands to accommodate all attributes and methods.

---

## 2. Constructor & Class Definition

```drawlib show-code 550px center file:class_diagram_basic_node.png caption:"Basic Class and Interface Nodes"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=90, height=45)

cd = ClassDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Black,
    title="Domain Model",
)

# Class with attributes and methods
user = cd.add(ClassNode(name="User", width=26.0), xy=(25.0, 18.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", params="password: str", return_type="bool")

# Interface with stereotype
gateway = cd.add(ClassNode(name="PaymentGateway", stereotype="interface", width=28.0), xy=(65.0, 18.0))
gateway.add_method("charge", params="amount: float", return_type="bool")

cd.draw(xy=(0.0, 0.0))
save()
```

---

## 3. The 6 UML Relationship Types

Relationships between classes are registered cleanly at the diagram level via `cd.connect(source, target, relationship_type=...)`:

| `relationship_type` | Relationship | Line Stroke | End Marker | Semantic Meaning |
|---|---|---|---|---|
| `"inheritance"` | **Inheritance** | Solid | Hollow Triangle (at target) | Superclass generalization |
| `"realization"` | **Realization** | Dashed | Hollow Triangle (at target) | Interface implementation |
| `"composition"` | **Composition** | Solid | Filled Diamond (at source) | Strong lifecycle ownership |
| `"aggregation"` | **Aggregation** | Solid | Hollow Diamond (at source) | Shared lifecycle / part-whole |
| `"association"` | **Association** | Solid | None (or Open Arrow) | Structural reference |
| `"dependency"` | **Dependency** | Dashed | Open Arrow (at target) | Uses-a dependency |

`cd.connect(...)` accepts `start_side`, `end_side`, `start_multiplicity` (`"1"`, `"0..1"`), `end_multiplicity` (`"*"`, `"1..*"`), `start_role`, `end_role`, and `label`.

---

## 4. E-Commerce Domain Model

The following example combines inheritance, composition, and interface dependency:

```drawlib 650px center file:class_diagram_ecommerce_domain.png caption:"E-Commerce Domain Class Hierarchy"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=110, height=85)

cd = ClassDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Black,
    title="E-Commerce Domain Class Model",
)

# 1. Define classes
user = cd.add(ClassNode(name="User", width=26.0), xy=(22.0, 60.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("email", type="str", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", return_type="bool")

customer = cd.add(ClassNode(name="Customer", width=26.0), xy=(22.0, 20.0))
customer.add_attribute("shipping_address", type="str")
customer.add_method("checkout", return_type="Order")

order = cd.add(ClassNode(name="Order", width=28.0), xy=(75.0, 20.0))
order.add_attribute("order_id", type="str")
order.add_attribute("total", type="float")
order.add_method("calculate_tax", return_type="float")

iface = cd.add(ClassNode(name="PaymentGateway", stereotype="interface", width=30.0), xy=(75.0, 60.0))
iface.add_method("process_charge", params="amount: float", return_type="bool")

# 2. Connect relationships using diagram.connect
cd.connect(customer, user, "inheritance", start_side="top", end_side="bottom")
cd.connect(
    customer,
    order,
    "composition",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="places",
)
cd.connect(order, iface, "dependency", start_side="top", end_side="bottom", label="uses")

cd.draw(xy=(0.0, 0.0))
save()
```

---

## 5. Design Pattern Modeling: Observer Pattern

Class diagrams excel at illustrating software design patterns such as the Observer pattern:

```drawlib 650px center file:class_diagram_observer_pattern.png caption:"UML Observer Design Pattern"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=105, height=80)

cd = ClassDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Black,
    title="UML Observer Design Pattern",
)

subj_iface = cd.add(ClassNode(name="Subject", stereotype="interface", width=28.0), xy=(25.0, 58.0))
subj_iface.add_method("attach", params="o: Observer", return_type="void")
subj_iface.add_method("notify", return_type="void")

obs_iface = cd.add(ClassNode(name="Observer", stereotype="interface", width=28.0), xy=(75.0, 58.0))
obs_iface.add_method("update", return_type="void")

concrete_subj = cd.add(ClassNode(name="NewsPublisher", width=28.0), xy=(25.0, 20.0))
concrete_subj.add_attribute("state", type="str", is_public=False)
concrete_subj.add_method("get_state", return_type="str")

concrete_obs = cd.add(ClassNode(name="EmailSubscriber", width=28.0), xy=(75.0, 20.0))
concrete_obs.add_method("update", return_type="void")

cd.connect(concrete_subj, subj_iface, "realization", start_side="top", end_side="bottom")
cd.connect(concrete_obs, obs_iface, "realization", start_side="top", end_side="bottom")
cd.connect(
    subj_iface,
    obs_iface,
    "aggregation",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    start_role="subject",
    end_role="observers",
)

cd.draw(xy=(0.0, 0.0))
save()
```

---

## 6. Best Practices & Guidelines

1. **Card Width Sizing**: Choose a consistent card width (`26.0` to `30.0` units) across horizontally aligned classes to maintain visual balance.
2. **Explicit Connection Sides**: Specifying `start_side` and `end_side` ensures orthogonal lines route cleanly around cards without cutting through text compartments.
