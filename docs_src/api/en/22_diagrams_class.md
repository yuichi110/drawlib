# drawlib.diagrams.class_diagram

UML 2.0 object-oriented class diagrams featuring 3-compartment class and interface cards, member visibility prefixes, and canonical UML relationship markers. Canonical import: `from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode, ClassRelationship`.

```drawlib align=center code=fold file=22_diagrams_class_hero.png caption="UML 2.0 Class Diagram with Interface Realization, Dependency, and Composition"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Colors, Styles

setup(width=120, height=64)

cd = ClassDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(
        text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0, shape_line_color=Styles.Neutral.shape_line_color
    ),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    margin=4.0,
)

repo_iface = cd.add(
    ClassNode(
        "Repository",
        stereotype="interface",
        width=40,
        row_height=3.8,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Colors.White, text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0
        ),
    ).add_method("save", "order: Order", "None"),
    xy=(25.0, 49.0),
)

sql_repo = cd.add(
    ClassNode("SqlRepository", width=40, row_height=3.8)
    .add_attribute("dsn", "str", visibility="-")
    .add_method("save", "order: Order", "None"),
    xy=(25.0, 17.0),
)

order = cd.add(
    ClassNode(
        "Order",
        width=40,
        row_height=3.8,
        header_style=Styles.SecondaryNeutral.patch(
            text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0, shape_line_color=Styles.Neutral.shape_line_color
        ),
    )
    .add_attribute("id", "UUID", visibility="+")
    .add_method("total", "", "Decimal"),
    xy=(95.0, 49.0),
)

item = cd.add(
    ClassNode("OrderItem", width=40, row_height=3.8)
    .add_attribute("sku", "str", visibility="+")
    .add_attribute("qty", "int", default_value="1", visibility="+"),
    xy=(95.0, 17.0),
)

cd.connect(sql_repo, repo_iface, "realization", start_side="top", end_side="bottom")
cd.connect(repo_iface, order, "dependency", label="«persists»", start_side="right", end_side="left")
cd.connect(
    order,
    item,
    "composition",
    start_multiplicity="1",
    end_multiplicity="1..*",
    directed=True,
    start_side="bottom",
    end_side="top",
)

cd.draw(xy=(60.0, 32.0), align="center")
save()
```

---

## `class` AttributeInfo

Validated Pydantic data model representing a single class field or attribute row inside a [`ClassNode`](#classnode)'s attributes compartment. Typically created via `node.add_attribute(...)` or passed to `node.add_attributes([...])`.

```python
AttributeInfo(
    *,
    name: str,
    type: str = "",
    is_public: bool = True,
    visibility: str | None = None,
    default_value: str = "",
    is_static: bool = False,
) -> None
```

- **Coordinate Anchor**: Rendered left-aligned as an ordered row inside the middle compartment of [`ClassNode`](#classnode).

### Constructor Parameters & Fields

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Attribute or field identifier (keyword-only). |
| `type` | `str` | `""` | Type annotation string (e.g., `"UUID"`, `"list[Item]"`). |
| `is_public` | `bool` | `True` | Resolves visibility prefix to `"+"` when `True` or `"-"` when `False` unless `visibility` is specified. |
| `visibility` | `str \| None` | `None` | Explicit UML visibility prefix (`"+"` public, `"-"` private, `"#"` protected, `"~"` package); overrides `is_public`. |
| `default_value` | `str` | `""` | Optional default literal rendered as `= <default_value>`. |
| `is_static` | `bool` | `False` | Marks the attribute as class-level static (rendered underlined in UML). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `display_text` | `property` | `-> str` | Formatted UML attribute string (`"{symbol} {name}: {type} = {default_value}"`). |
| `symbol` | `property` | `-> str` | Resolved single-character UML visibility prefix (`"+"`, `"-"`, `"#"`, or `"~"`). |
| `model_copy` | `method` | `(self, *, update: Mapping[str, Any] \| None = None, deep: bool = False) -> Self` | Create a shallow or deep copy with optional field updates (`pydantic.BaseModel`). |
| `model_dump` | `method` | `(self, *, mode: str = "python", ...) -> dict[str, Any]` | Serialize fields to a Python dictionary (`pydantic.BaseModel`). |
| `model_dump_json` | `method` | `(self, *, indent: int \| None = None, ...) -> str` | Serialize fields to a JSON string (`pydantic.BaseModel`). |
| `model_validate` | `classmethod` | `(obj: Any, *, strict: bool \| None = None, ...) -> Self` | Validate an arbitrary mapping or object into `AttributeInfo`. |
| `model_validate_json` | `classmethod` | `(json_data: str \| bytes \| bytearray, ...) -> Self` | Parse and validate JSON input into `AttributeInfo`. |
| `model_validate_strings` | `classmethod` | `(obj: Any, ...) -> Self` | Validate string-typed input dictionary into `AttributeInfo`. |
| `model_construct` | `classmethod` | `(_fields_set: set[str] \| None = None, **values: Any) -> Self` | Construct an unvalidated instance directly from field values. |
| `model_json_schema` | `classmethod` | `(by_alias: bool = True, ...) -> dict[str, Any]` | Generate a JSON Schema dictionary for `AttributeInfo`. |

*(Also inherits standard `pydantic.BaseModel` lifecycle/compatibility members: `model_extra`, `model_fields_set`, `model_parametrized_name`, `model_post_init`, `model_rebuild`, `construct`, `copy`, `dict`, `from_orm`, `json`, `parse_file`, `parse_obj`, `parse_raw`, `schema`, `schema_json`, `update_forward_refs`, and `validate`.)*

---

## `class` ClassDiagram

Top-level container managing [`ClassNode`](#classnode) cards, [`ClassRelationship`](#classrelationship) connectors, and bounding-box layout for UML 2.0 class diagrams.

```python
ClassDiagram(
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
) -> None
```

- **Coordinate Anchor**: `draw(xy=(0.0, 0.0), align="bottom_left")` shifts local coordinates by `xy` (or centers the computed bounding box of all classes at `xy` when `align="center"`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base style for class card bodies, compartment dividers, and member text (keyword-only). |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base stroke and marker style for [`ClassRelationship`](#classrelationship) lines (keyword-only). |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style for relationship labels, multiplicities, and role names (keyword-only). |
| `title` | `str` | `""` | Optional diagram title rendered centered above the top border. |
| `title_style` | `Style \| None` | `None` | Optional typography style override for `title`. |
| `style` | `Style \| None` | `None` | Optional outer background/border style for the diagram container. |
| `width` | `float \| None` | `None` | Optional fixed diagram width override (`None` auto-computes from `get_bounds()` + `margin`). |
| `height` | `float \| None` | `None` | Optional fixed diagram height override (`None` auto-computes from `get_bounds()` + `margin`). |
| `margin` | `float` | `5.0` | Outer margin padding surrounding all registered classes. |
| `header_style` | `Style \| None` | `None` | Optional default style applied to top class header compartments unless overridden per node. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, class_node: ClassNode, xy: tuple[float, float] = (0.0, 0.0), show: bool \| None = None) -> ClassNode` | Register a [`ClassNode`](#classnode) centered at local coordinate `xy` and return it. |
| `add_relationship` | `method` | `(self, rel: ClassRelationship) -> ClassRelationship` | Register a pre-constructed [`ClassRelationship`](#classrelationship) with this diagram. |
| `connect` | `method` | `(self, source: ClassNode, target: ClassNode, relationship_type: RelationshipType = "association", *, type: RelationshipType \| None = None, label: str = "", start_side: Side = "auto", end_side: Side = "auto", start_multiplicity: str = "", end_multiplicity: str = "", start_role: str = "", end_role: str = "", directed: bool = False, style: Style \| None = None, text_style: Style \| None = None, routing: RoutingType = "orthogonal", padding: PaddingType = 0.0, show: bool = True) -> ClassRelationship` | Create and register a UML [`ClassRelationship`](#classrelationship) between `source` and `target`. |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | Render the complete class diagram onto the active canvas anchored at `xy`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Compute enclosing `(min_x, min_y, max_x, max_y)` of all registered class cards. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Compute overall `(width, height)` of the diagram including `margin`. |

---

## `class` ClassNode

UML 2.0 3-compartment box representing a concrete class, abstract class, interface, enum, or dataclass.

```python
ClassNode(
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
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `cd.add(node, xy=(cx, cy))`. When using saturated header fills such as `Styles.PrimaryFlat`, pass `header_style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=11.0)` for crisp contrast.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Class or interface name displayed in the top header compartment. |
| `stereotype` | `str` | `""` | Optional UML stereotype (auto-formatted as `<<stereotype>>` if unbracketed, e.g., `"interface"`). |
| `is_abstract` | `bool` | `False` | Marks the class as abstract (displays `<<abstract>>` when `stereotype` is empty). |
| `width` | `float` | `28.0` | Class card width in local diagram units. |
| `height` | `float \| None` | `None` | Optional fixed total height override (`None` auto-expands from header + member rows). |
| `header_height` | `float \| None` | `None` | Optional fixed header height (`None` defaults to `5.2`, or `6.5` with stereotype/abstract tag). |
| `row_height` | `float` | `3.2` | Vertical height per attribute or method row. |
| `style` | `Style \| None` | `None` | Optional body fill, border, and member text style override (falls back to `cd.node_style`). |
| `header_style` | `Style \| None` | `None` | Optional header compartment fill/border/text style override (falls back to `cd.header_style`). |
| `show` | `bool` | `True` | Visibility flag (`False` hides this class card and its relationships). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add_attribute` | `method` | `(self, name: str, type: str = "", is_public: bool = True, visibility: str \| None = None, default_value: str = "", is_static: bool = False) -> ClassNode` | Append a field row ([`AttributeInfo`](#attributeinfo)) to the attributes compartment and return `self`. |
| `add_attributes` | `method` | `(self, attributes: Sequence[Sequence[Any] \| AttributeInfo]) -> ClassNode` | Append multiple attributes from `(name, type, ...)` tuples or `AttributeInfo` objects and return `self`. |
| `add_method` | `method` | `(self, name: str, params: str = "", return_type: str = "", is_public: bool = True, visibility: str \| None = None, is_static: bool = False, is_abstract: bool = False) -> ClassNode` | Append an operation row ([`MethodInfo`](#methodinfo)) to the methods compartment and return `self`. |
| `add_methods` | `method` | `(self, methods: Sequence[Sequence[Any] \| MethodInfo]) -> ClassNode` | Append multiple methods from `(name, params, return_type, ...)` tuples or `MethodInfo` objects and return `self`. |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the class card. |
| `effective_height` | `property` | `-> float` | Computed total rendered height of the class card across all compartments. |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return boundary midpoint coordinate on `side` (`"left"`, `"right"`, `"top"`, `"bottom"`, `"auto"`). |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-width/2, -effective_height/2, width/2, effective_height/2)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)` of the class card. |

---

## `class` ClassRelationship

UML 2.0 relationship edge connecting two [`ClassNode`](#classnode) boxes with hollow triangles, solid/hollow diamonds, open arrowheads, multiplicities, and role labels.

```python
ClassRelationship(
    start: ClassNode,
    end: ClassNode,
    relationship_type: RelationshipType = "association",
    start_side: Side = "auto",
    end_side: Side = "auto",
    label: str = "",
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
) -> None
```

- **Coordinate Anchor**: Connects `start_side` boundary port on `start` to `end_side` boundary port on `end`. Register via `cd.connect(...)` or `cd.add_relationship(rel)`.

### Constructor Parameters & Attributes

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start` | [`ClassNode`](#classnode) | *(Required)* | Source class (subclass for inheritance/realization; whole/owner for composition/aggregation). |
| `end` | [`ClassNode`](#classnode) | *(Required)* | Target class (superclass/interface for inheritance/realization; part/member for composition/aggregation). |
| `relationship_type` | [`RelationshipType`](#relationshiptype) | `"association"` | UML relationship kind controlling stroke dash and endpoint markers. |
| `start_side` | [`Side`](#side) | `"auto"` | Attachment side on `start` (`"left"`, `"right"`, `"top"`, `"bottom"`, `"auto"`). |
| `end_side` | [`Side`](#side) | `"auto"` | Attachment side on `end` (`"left"`, `"right"`, `"top"`, `"bottom"`, `"auto"`). |
| `label` | `str` | `""` | Midpoint stereotype or verb phrase label (e.g., `"<<creates>>"`). |
| `start_multiplicity` | `str` | `""` | Multiplicity string rendered near the `start` anchor (e.g., `"1"`, `"0..1"`). |
| `end_multiplicity` | `str` | `""` | Multiplicity string rendered near the `end` anchor (e.g., `"*"`, `"1..*"`). |
| `start_role` | `str` | `""` | Role name rendered near the `start` anchor. |
| `end_role` | `str` | `""` | Role name rendered near the `end` anchor. |
| `directed` | `bool` | `False` | Draws a navigable open V-arrow at `end` on `"association"`, `"aggregation"`, or `"composition"`. |
| `style` | `Style \| None` | `None` | Optional stroke style override (falls back to `cd.edge_style`). |
| `text_style` | `Style \| None` | `None` | Optional typography style override for labels/multiplicities (falls back to `cd.edge_text_style`). |
| `routing` | [`RoutingType`](#routingtype) | `"orthogonal"` | Path routing strategy (`"orthogonal"` or `"direct"`). |
| `padding` | `float \| tuple[float, float]` | `0.0` | Clearance gap between class borders and line endpoints. |
| `show` | `bool` | `True` | Whether to render this relationship edge. |

---

## `class` MethodInfo

Validated Pydantic data model representing a single class method or operation row inside a [`ClassNode`](#classnode)'s methods compartment. Typically created via `node.add_method(...)` or passed to `node.add_methods([...])`.

```python
MethodInfo(
    *,
    name: str,
    params: str = "",
    return_type: str = "",
    is_public: bool = True,
    visibility: str | None = None,
    is_static: bool = False,
    is_abstract: bool = False,
) -> None
```

- **Coordinate Anchor**: Rendered left-aligned as an ordered row inside the bottom compartment of [`ClassNode`](#classnode).

### Constructor Parameters & Fields

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Method name with or without parentheses (keyword-only). |
| `params` | `str` | `""` | Parameter list signature string (e.g., `"order_id: UUID"`). |
| `return_type` | `str` | `""` | Return type annotation string (e.g., `"Order \| None"`). |
| `is_public` | `bool` | `True` | Resolves visibility prefix to `"+"` when `True` or `"-"` when `False` unless `visibility` is specified. |
| `visibility` | `str \| None` | `None` | Explicit UML visibility prefix (`"+"`, `"-"`, `"#"`, `"~"`); overrides `is_public`. |
| `is_static` | `bool` | `False` | Marks the method as static (`@staticmethod` / `@classmethod`, rendered underlined). |
| `is_abstract` | `bool` | `False` | Marks the method as abstract (`{abstract}` suffix / italic semantics). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `display_text` | `property` | `-> str` | Formatted UML operation string (`"{symbol} {name}({params}): {return_type}"`). |
| `symbol` | `property` | `-> str` | Resolved single-character UML visibility prefix (`"+"`, `"-"`, `"#"`, or `"~"`). |
| `model_copy` | `method` | `(self, *, update: Mapping[str, Any] \| None = None, deep: bool = False) -> Self` | Create a shallow or deep copy with optional field updates (`pydantic.BaseModel`). |
| `model_dump` | `method` | `(self, *, mode: str = "python", ...) -> dict[str, Any]` | Serialize fields to a Python dictionary (`pydantic.BaseModel`). |
| `model_dump_json` | `method` | `(self, *, indent: int \| None = None, ...) -> str` | Serialize fields to a JSON string (`pydantic.BaseModel`). |
| `model_validate` | `classmethod` | `(obj: Any, *, strict: bool \| None = None, ...) -> Self` | Validate an arbitrary mapping or object into `MethodInfo`. |
| `model_validate_json` | `classmethod` | `(json_data: str \| bytes \| bytearray, ...) -> Self` | Parse and validate JSON input into `MethodInfo`. |
| `model_validate_strings` | `classmethod` | `(obj: Any, ...) -> Self` | Validate string-typed input dictionary into `MethodInfo`. |
| `model_construct` | `classmethod` | `(_fields_set: set[str] \| None = None, **values: Any) -> Self` | Construct an unvalidated instance directly from field values. |
| `model_json_schema` | `classmethod` | `(by_alias: bool = True, ...) -> dict[str, Any]` | Generate a JSON Schema dictionary for `MethodInfo`. |

*(Also inherits standard `pydantic.BaseModel` lifecycle/compatibility members: `model_extra`, `model_fields_set`, `model_parametrized_name`, `model_post_init`, `model_rebuild`, `construct`, `copy`, `dict`, `from_orm`, `json`, `parse_file`, `parse_obj`, `parse_raw`, `schema`, `schema_json`, `update_forward_refs`, and `validate`.)*

---

## `type` RelationshipType

Literal union specifying the 6 canonical UML 2.0 class relationship kinds (plus concise verb aliases) accepted by `ClassDiagram.connect()` and [`ClassRelationship`](#classrelationship).

```python
RelationshipType = Literal[
    "inheritance",
    "realization",
    "composition",
    "aggregation",
    "association",
    "dependency",
    "inherit",
    "realize",
    "composite",
    "aggregate",
    "associate",
    "depend",
]
```

- **Coordinate Anchor**: Determines marker geometry at `start` (diamonds) and `end` (hollow triangles or open V-arrows).

| Canonical Value | Short Alias | Stroke | `start` Marker | `end` Marker | UML Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `"inheritance"` | `"inherit"` | Solid | None | Hollow triangle (`▷`) | `start` subclass extends `end` superclass. |
| `"realization"` | `"realize"` | Dashed | None | Hollow triangle (`▷`) | `start` class implements `end` interface. |
| `"composition"` | `"composite"` | Solid | Solid diamond (`◆`) | Open arrow if `directed=True` | `start` strongly owns lifecycle of `end`. |
| `"aggregation"` | `"aggregate"` | Solid | Hollow diamond (`◇`) | Open arrow if `directed=True` | `start` references shared `end` instance. |
| `"association"` | `"associate"` | Solid | None | Open arrow if `directed=True` | Structural association between `start` and `end`. |
| `"dependency"` | `"depend"` | Dashed | None | Open V-arrow (`>`) | `start` transiently depends on `end`. |

---

## `type` RoutingType

Literal type controlling path routing for [`ClassRelationship`](#classrelationship) connectors.

```python
RoutingType = Literal["orthogonal", "direct"]
```

- **Coordinate Anchor**: Governs connector routing between resolved `start` and `end` class boundary ports.

| Literal Value | Path Geometry |
| :--- | :--- |
| `"orthogonal"` | Right-angled horizontal and vertical Manhattan segments (default). |
| `"direct"` | Straight Euclidean segment connecting the resolved ports. |

---

## `type` Side

Literal type selecting the attachment edge on a [`ClassNode`](#classnode) box.

```python
Side = Literal["left", "right", "top", "bottom", "auto"]
```

- **Coordinate Anchor**: `"left"`, `"right"`, `"top"`, and `"bottom"` attach to the midpoint of that class card edge; `"auto"` chooses the nearest facing side automatically.
