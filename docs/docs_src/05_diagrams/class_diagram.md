# ClassDiagram: UML 2.0 Class Hierarchies & Relationships

`ClassDiagram` implements standard UML 2.0 Object-Oriented structural modeling. It features three-compartment class cards (class name, attributes, methods), stereotypes, abstract classes, and all 6 standard UML relationships.

---

## 1. Overview & Three-Compartment Cards

```drawlib fold-code 650px center file:class_diagram_overview_anatomy.png caption:"Three-Compartment UML Class Cards with Realization and Composition"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=112, height=64)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
)

payment_svc = cd.add(
    ClassNode(name="PaymentService", stereotype="interface", width=30.0, style=Styles.PrimaryNeutral),
    xy=(24.0, 48.0),
)
payment_svc.add_method("pay", params="amount", return_type="bool")

stripe_svc = cd.add(
    ClassNode(name="StripeService", width=30.0, style=Styles.Neutral),
    xy=(24.0, 16.0),
)
stripe_svc.add_attribute("api_key", type="str", is_public=False)
stripe_svc.add_method("pay", params="amount", return_type="bool")

tx = cd.add(
    ClassNode(name="Transaction", width=28.0, style=Styles.SecondaryNeutral),
    xy=(86.0, 16.0),
)
tx.add_attribute("id", type="UUID", is_public=True)
tx.add_attribute("amount", type="Decimal", is_public=True)

cd.connect(
    stripe_svc,
    payment_svc,
    relationship_type="realization",
    start_side="top",
    end_side="bottom",
    label="realizes",
)
cd.connect(
    stripe_svc,
    tx,
    relationship_type="composition",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="records",
)

cd.draw(xy=(2.0, 2.0))
save()
```

- **Three Compartments**: Class cards automatically separate the class title/stereotype header, attribute declarations, and method signatures into distinct compartments with divider lines.
- **Access Modifiers**: Supports standard UML visibility prefixes: `+` (public), `-` (private), `#` (protected), `~` (package).
- **Dynamic Sizing**: The card height automatically expands (`node.effective_height`) to accommodate all attributes and methods.

---

## 2. Constructor, `ClassNode` & Member Declarations

```drawlib show-code 550px center file:class_diagram_basic_node.png caption:"Basic Class and Interface Nodes"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=90, height=45)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Domain Model",
)

# Class with attributes and methods
user = cd.add(ClassNode(name="User", width=26.0), xy=(25.0, 18.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", params="password: str", return_type="bool")

# Interface with stereotype
gateway = cd.add(ClassNode(name="PaymentGateway", stereotype="interface", width=28.0, style=Styles.PrimaryNeutral), xy=(65.0, 18.0))
gateway.add_method("charge", params="amount: float", return_type="bool")

cd.draw(xy=(0.0, 0.0))
save()
```

### Parameter Reference Tables

#### `ClassDiagram` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `node_style` | `Style` | *(Required)* | Base `Style` object for class cards in the diagram. |
| `edge_style` | `Style` | *(Required)* | Base `Style` object for relationship lines and UML markers. |
| `edge_text_style` | `Style` | *(Required)* | Base `Style` object for relationship labels, roles, and multiplicities. |
| `title` | `str` | `""` | Optional title displayed above the diagram. |
| `title_style` | `Style \| None` | `None` | Optional `Style` object for the diagram title. |
| `style` | `Style \| None` | `None` | Optional `Style` overriding the overall diagram background. |
| `width` | `float \| None` | `None` | Optional fixed canvas width (auto-calculated from content if `None`). |
| `height` | `float \| None` | `None` | Optional fixed canvas height (auto-calculated from content if `None`). |
| `margin` | `float` | `5.0` | Outer margin padding surrounding all classes when auto-calculating size. |
| `header_style` | `Style \| None` | `None` | Optional `Style` overriding class card header compartments across the diagram. |

#### `ClassNode` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | *(Required)* | Class or interface name. |
| `stereotype` | `str` | `""` | Optional UML stereotype rendered as `«stereotype»` (e.g. `"interface"`, `"abstract"`, `"enumeration"`). |
| `is_abstract` | `bool` | `False` | When `True`, renders the class name in italic font. |
| `width` | `float` | `28.0` | Width of the class card in canvas units. |
| `height` | `float \| None` | `None` | Optional minimum height override (auto-expands to fit attributes/methods if `None` or smaller). |
| `size` | `tuple[float, float] \| None` | `None` | Optional `(width, height)` shorthand tuple overriding `width` and `height`. |
| `header_height` | `float \| None` | `None` | Height of the header compartment (`6.5` when `stereotype` is set, otherwise `5.2`). |
| `row_height` | `float` | `3.2` | Vertical height of each attribute and method line. |
| `style` | `Style \| None` | `None` | Optional `Style` override for the card border and body fill. |
| `header_style` | `Style \| None` | `None` | Optional `Style` override for this card's header compartment background and text. |
| `show` | `bool` | `True` | Visibility flag (connected `ClassRelationship` edges auto-hide when `False`). |

### Attribute & Method Declaration API (`AttributeInfo` & `MethodInfo`)

```python
from drawlib.diagrams.class_diagram import AttributeInfo, MethodInfo

# Single attribute & batch attributes
node.add_attribute(
    name: str,
    type: str = "",
    is_public: bool = True,
    visibility: str | None = None,      # "+", "-", "#", or "~" (overrides is_public if set)
    default_value: str = "",            # Rendered as " = <default_value>"
    is_static: bool = False,
) -> ClassNode

node.add_attributes(
    attributes: Sequence[Sequence[Any] | AttributeInfo],
    # Each tuple is (name, [type, is_public, visibility, default_value]) or an AttributeInfo instance
) -> ClassNode

# Single method & batch methods
node.add_method(
    name: str,
    params: str = "",
    return_type: str = "",
    is_public: bool = True,
    visibility: str | None = None,      # "+", "-", "#", or "~" (overrides is_public if set)
    is_static: bool = False,
    is_abstract: bool = False,
) -> ClassNode

node.add_methods(
    methods: Sequence[Sequence[Any] | MethodInfo],
    # Each tuple is (name, [return_type, params, is_public, visibility]) or a MethodInfo instance
) -> ClassNode
```

---

## 3. The 6 UML Relationship Types (`ClassRelationship`)

Relationships between classes are registered at the diagram level via `cd.connect(source, target, relationship_type=...)` (or `cd.add_relationship(rel: ClassRelationship) -> ClassRelationship`):

| `relationship_type` | Shorthand Alias | Relationship | Line Stroke | Marker | Semantic Meaning |
|---|---|---|---|---|---|
| `"inheritance"` | `"inherit"` | **Inheritance** | Solid | Hollow Triangle (at `target`) | Superclass generalization |
| `"realization"` | `"realize"` | **Realization** | Dashed | Hollow Triangle (at `target`) | Interface implementation |
| `"composition"` | `"composite"` | **Composition** | Solid | Filled Diamond (at `source`) | Strong lifecycle ownership |
| `"aggregation"` | `"aggregate"` | **Aggregation** | Solid | Hollow Diamond (at `source`) | Shared lifecycle / part-whole |
| `"association"` | `"associate"` | **Association** | Solid | None (or Open Arrow if `directed=True`) | Structural reference |
| `"dependency"` | `"depend"` | **Dependency** | Dashed | Open Arrow (at `target`) | Uses-a dependency |

```drawlib show-code 650px center file:class_diagram_relationship_types.png caption:"All Six UML Relationship Types and Marker Styles in ClassDiagram"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=156, height=96)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
)

# 2x3 Grid of the 6 UML Relationship Types
specs = [
    # Left column (x_src=18, x_dst=60)
    ("1. Inheritance (solid + hollow triangle)", "inheritance", False, 18.0, 60.0, 74.0, "SubClass", "SuperClass"),
    ("3. Composition (solid + filled diamond)", "composition", False, 18.0, 60.0, 44.0, "Order", "LineItem"),
    ("5. Association (directed=True)", "association", True, 18.0, 60.0, 14.0, "Customer", "Cart"),
    # Right column (x_src=96, x_dst=138)
    ("2. Realization (dashed + hollow triangle)", "realization", False, 96.0, 138.0, 74.0, "Impl", "Interface"),
    ("4. Aggregation (solid + hollow diamond)", "aggregation", False, 96.0, 138.0, 44.0, "Team", "Member"),
    ("6. Dependency (dashed + open arrow)", "dependency", False, 96.0, 138.0, 14.0, "Client", "Service"),
]

lbl_style = Styles.DarkBold.patch(text_size=9.5, text_color=Colors.Primary5)

for title_str, rel_type, is_dir, x1, x2, y, src_name, dst_name in specs:
    n_src = cd.add(ClassNode(name=src_name, width=18.0, style=Styles.PrimaryNeutral), xy=(x1, y))
    n_dst = cd.add(ClassNode(name=dst_name, width=18.0, style=Styles.Neutral), xy=(x2, y))
    cd.connect(
        n_src,
        n_dst,
        relationship_type=rel_type,
        directed=is_dir,
        start_side="right",
        end_side="left",
    )

cd.draw(xy=(0.0, 0.0))

for title_str, _rel_type, _is_dir, x1, x2, y, _src_name, _dst_name in specs:
    text(((x1 + x2) / 2.0, y + 8.5), title_str, style=lbl_style)

save()
```

### `cd.connect(...)` Signature
```python
cd.connect(
    source: ClassNode,
    target: ClassNode,
    relationship_type: RelationshipType = "association",
    *,
    type: RelationshipType | None = None,              # Keyword alias for relationship_type
    label: str = "",
    start_side: Literal["left", "right", "top", "bottom", "auto"] = "auto",
    end_side: Literal["left", "right", "top", "bottom", "auto"] = "auto",
    start_multiplicity: str = "",                      # e.g. "1", "0..1"
    end_multiplicity: str = "",                        # e.g. "*", "1..*"
    start_role: str = "",
    end_role: str = "",
    directed: bool = False,                            # Draws open navigability arrow at target
    style: Style | None = None,
    text_style: Style | None = None,
    routing: Literal["orthogonal", "direct"] = "orthogonal",
    padding: float | tuple[float, float] = 0.0,
    show: bool = True,
) -> ClassRelationship
```

### Registration, Sizing & Rendering Lifecycle
- **`cd.add(class_node, xy=(cx, cy), show: bool | None = None) -> ClassNode`**: Registers a class card centered at `(cx, cy)` and returns the mutable `ClassNode` (`node.show`, `node.style`, `node.header_style`). Hiding a class (`show=False`) also automatically hides all `ClassRelationship` edges connected to it while keeping diagram bounds fixed.
- **`cd.get_bounds() -> tuple[float, float, float, float]`**: Returns `(min_x, min_y, max_x, max_y)` enclosing all registered classes.
- **`cd.get_size() -> tuple[float, float]`**: Returns `(width, height)` of the diagram (including `margin`).
- **`cd.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: Renders the class diagram anchored at bottom-left `xy`, proportionally scaling card widths, compartment heights, UML markers, and typography by `scale`.

---

## 4. E-Commerce Domain Model

The following example combines inheritance, composition, and interface dependency:

```drawlib show-code 650px center file:class_diagram_ecommerce_domain.png caption:"E-Commerce Domain Class Hierarchy"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=110, height=85)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="E-Commerce Domain Class Model",
)

# 1. Define classes
user = cd.add(ClassNode(name="User", width=26.0), xy=(22.0, 60.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("email", type="str", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", return_type="bool")

customer = cd.add(ClassNode(name="Customer", width=26.0, style=Styles.SecondaryNeutral), xy=(22.0, 20.0))
customer.add_attribute("shipping_address", type="str")
customer.add_method("checkout", return_type="Order")

order = cd.add(ClassNode(name="Order", width=28.0, style=Styles.PrimaryNeutral), xy=(75.0, 20.0))
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

```drawlib show-code 650px center file:class_diagram_observer_pattern.png caption:"UML Observer Design Pattern"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=105, height=80)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="UML Observer Design Pattern",
)

subj_iface = cd.add(
    ClassNode(name="Subject", stereotype="interface", width=28.0, style=Styles.PrimaryNeutral),
    xy=(25.0, 58.0),
)
subj_iface.add_method("attach", params="o: Observer", return_type="void")
subj_iface.add_method("notify", return_type="void")

obs_iface = cd.add(
    ClassNode(name="Observer", stereotype="interface", width=28.0, style=Styles.SecondaryNeutral),
    xy=(75.0, 58.0),
)
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
