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



```python
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=90, height=45)

cd = ClassDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
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

<figure class="drawlib-image" style="text-align: center;">
  <img src="class_diagram_images/class_diagram_basic_node.png" alt="class_diagram_1" style="width: 550px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Basic Class and Interface Nodes</figcaption>
</figure>



---

## 3. The 6 UML Relationship Verbs

Drawlib provides dedicated semantic methods for the 6 core UML relationships instead of generic line drawing:

| Verb Method | Relationship | Line Stroke | End Marker | Semantic Meaning |
|---|---|---|---|---|
| `child.inherit(parent)` | **Inheritance** | Solid | Hollow Triangle (at parent) | Superclass generalization |
| `impl.realize(iface)` | **Realization** | Dashed | Hollow Triangle (at iface) | Interface implementation |
| `whole.composite(part)` | **Composition** | Solid | Filled Diamond (at whole) | Strong lifecycle ownership |
| `whole.aggregate(part)` | **Aggregation** | Solid | Hollow Diamond (at whole) | Shared lifecycle / part-whole |
| `c1.associate(c2)` | **Association** | Solid | None (or Open Arrow) | Structural reference |
| `client.depend(supplier)` | **Dependency** | Dashed | Open Arrow (at supplier) | Uses-a dependency |

All relationship methods accept `start_side`, `end_side`, `start_multiplicity` (`"1"`, `"0..1"`), `end_multiplicity` (`"*"`, `"1..*"`), `start_role`, `end_role`, and `label`.

---

## 4. E-Commerce Domain Model

The following example combines inheritance, composition, and interface dependency:



<figure class="drawlib-image" style="text-align: center;">
  <img src="class_diagram_images/class_diagram_ecommerce_domain.png" alt="class_diagram_2" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">E-Commerce Domain Class Hierarchy</figcaption>
</figure>



---

## 5. Design Pattern Modeling: Observer Pattern

Class diagrams excel at illustrating software design patterns such as the Observer pattern:



<figure class="drawlib-image" style="text-align: center;">
  <img src="class_diagram_images/class_diagram_observer_pattern.png" alt="class_diagram_3" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">UML Observer Design Pattern</figcaption>
</figure>



---

## 6. Best Practices & Guidelines

1. **Card Width Sizing**: Choose a consistent card width (`26.0` to `30.0` units) across horizontally aligned classes to maintain visual balance.
2. **Explicit Connection Sides**: Specifying `start_side` and `end_side` ensures orthogonal lines route cleanly around cards without cutting through text compartments.
