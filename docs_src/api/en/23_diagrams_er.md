# drawlib.diagrams.er

Relational database Entity-Relationship (ER) schema diagrams using Information Engineering (Crow's Foot) notation and row-accurate foreign key column anchoring. Canonical import: `from drawlib.diagrams.er import Entity, ERDiagram, Relationship`.

```drawlib align=center code=fold file=23_diagrams_er_hero.png caption="Crow's Foot ER Schema with Column-Level Foreign Key Anchoring"
from drawlib.canvas import save, setup
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

users = erd.add(
    Entity("users", width=42, header_height=4.8, row_height=4.0)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("email", "VARCHAR", nullable=False)
    .add_column("created_at", "TIMESTAMP", nullable=False),
    xy=(27.0, 43.0),
)

products = erd.add(
    Entity(
        "products",
        width=42,
        header_height=4.8,
        row_height=4.0,
        header_style=Styles.SecondaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0),
    )
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("sku", "VARCHAR", nullable=False)
    .add_column("price", "INT", nullable=False),
    xy=(27.0, 15.0),
)

order_items = erd.add(
    Entity(
        "order_items",
        width=44,
        header_height=4.8,
        row_height=4.0,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Colors.White, text_font=FontRoboto.ROBOTO_BOLD, text_size=11.0
        ),
    )
    .add_column("id", "BIGINT", pk=True, nullable=False)
    .add_column("user_id", "UUID", fk=True, nullable=False)
    .add_column("product_id", "UUID", fk=True, nullable=False)
    .add_column("qty", "INT", nullable=False),
    xy=(92.0, 29.0),
)

users.connect(
    order_items,
    cardinality="1:*",
    start_column="id",
    end_column="user_id",
    start_side="right",
    end_side="left",
)
products.connect(
    order_items,
    cardinality="1:*",
    start_column="id",
    end_column="product_id",
    start_side="right",
    end_side="left",
)

erd.draw(xy=(0.0, 0.0))
save()
```

---

## `type` Cardinality

Literal union specifying Information Engineering (Crow's Foot) multiplicity markers at the `start` and `end` endpoints of a [`Relationship`](#relationship).

```python
Cardinality = Literal["1:*", "1:1", "1:1..*", "1:0..1", "0..1:1", "0..1:*", "*:*"]
```

- **Coordinate Anchor**: Drawn immediately outside the resolved `start` and `end` entity border or column-row anchor points.

| Literal Value | `start` Marker | `end` Marker | Relational Semantics |
| :--- | :--- | :--- | :--- |
| `"1:*"` | Mandatory One (`\|\|`) | Zero-or-Many (`o<` / `\|<`) | Standard 1-to-Many foreign key relationship (default). |
| `"1:1"` | Mandatory One (`\|\|`) | Mandatory One (`\|\|`) | Strict 1-to-1 relationship. |
| `"1:1..*"` | Mandatory One (`\|\|`) | Mandatory One-or-Many (`\|<`) | 1-to-Many requiring at least one child row. |
| `"1:0..1"` | Mandatory One (`\|\|`) | Optional Zero-or-One (`o\|`) | Mandatory source to optional target row. |
| `"0..1:1"` | Optional Zero-or-One (`o\|`) | Mandatory One (`\|\|`) | Optional source to mandatory target row. |
| `"0..1:*"` | Optional Zero-or-One (`o\|`) | Many (`\|<`) | Nullable foreign key 1-to-Many relationship. |
| `"*:*"` | Many (`>\|`) | Many (`\|<`) | Many-to-Many association. |

---

## `class` ColumnInfo

Validated Pydantic data model representing a single database table column row inside an [`Entity`](#entity). Typically created via `entity.add_column(...)` or passed to `entity.add_columns([...])`.

```python
ColumnInfo(
    *,
    name: str,
    type: str = "",
    pk: bool = False,
    fk: bool = False,
    nullable: bool = True,
) -> None
```

- **Coordinate Anchor**: Rendered as a 3-slot aligned row (`PK`/`FK` badge | `name` | `type (NN)`) inside [`Entity`](#entity), addressable by `name` in `start_column` / `end_column` relationship anchors.

### Constructor Parameters & Fields

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Database column identifier (keyword-only). |
| `type` | `str` | `""` | SQL data type label (e.g., `"UUID"`, `"VARCHAR(255)"`, `"BIGINT"`). |
| `pk` | `bool` | `False` | Marks the column as a Primary Key (renders `"PK"` badge and bold name). |
| `fk` | `bool` | `False` | Marks the column as a Foreign Key (renders `"FK"` or `"PK,FK"` badge). |
| `nullable` | `bool` | `True` | When `False`, appends `(NN)` (`NOT NULL`) beside `type`. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `model_copy` | `method` | `(self, *, update: Mapping[str, Any] \| None = None, deep: bool = False) -> Self` | Create a shallow or deep copy with optional field updates (`pydantic.BaseModel`). |
| `model_dump` | `method` | `(self, *, mode: str = "python", ...) -> dict[str, Any]` | Serialize column metadata to a Python dictionary (`pydantic.BaseModel`). |
| `model_dump_json` | `method` | `(self, *, indent: int \| None = None, ...) -> str` | Serialize column metadata to a JSON string (`pydantic.BaseModel`). |
| `model_validate` | `classmethod` | `(obj: Any, *, strict: bool \| None = None, ...) -> Self` | Validate an arbitrary mapping or object into `ColumnInfo`. |
| `model_validate_json` | `classmethod` | `(json_data: str \| bytes \| bytearray, ...) -> Self` | Parse and validate JSON input into `ColumnInfo`. |
| `model_validate_strings` | `classmethod` | `(obj: Any, ...) -> Self` | Validate string-typed input dictionary into `ColumnInfo`. |
| `model_construct` | `classmethod` | `(_fields_set: set[str] \| None = None, **values: Any) -> Self` | Construct an unvalidated instance directly from field values. |
| `model_json_schema` | `classmethod` | `(by_alias: bool = True, ...) -> dict[str, Any]` | Generate a JSON Schema dictionary for `ColumnInfo`. |

*(Also inherits standard `pydantic.BaseModel` lifecycle/compatibility members: `model_extra`, `model_fields_set`, `model_parametrized_name`, `model_post_init`, `model_rebuild`, `construct`, `copy`, `dict`, `from_orm`, `json`, `parse_file`, `parse_obj`, `parse_raw`, `schema`, `schema_json`, `update_forward_refs`, and `validate`.)*

---

## `class` ERDiagram

Top-level container for Entity-Relationship (ER) database schema diagrams managing [`Entity`](#entity) table cards and Crow's Foot [`Relationship`](#relationship) lines.

```python
ERDiagram(
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
) -> None
```

- **Coordinate Anchor**: `draw(xy=(0.0, 0.0), align="bottom_left")` places the diagram's local `(0.0, 0.0)` origin at canvas coordinate `xy` (or centers `get_size()` around `xy` when `align="center"`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base style for [`Entity`](#entity) table cards, borders, and column text (keyword-only). |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base stroke style for [`Relationship`](#relationship) lines and Crow's Foot markers (keyword-only). |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style for relationship labels (keyword-only). |
| `title` | `str` | `""` | Optional diagram title rendered centered above the schema. |
| `title_style` | `Style \| None` | `None` | Optional typography style override for `title`. |
| `width` | `float \| None` | `None` | Optional fixed diagram width in local units. |
| `height` | `float \| None` | `None` | Optional fixed diagram height in local units. |
| `style` | `Style \| None` | `None` | Optional outer background/border style for the diagram container. |
| `header_style` | `Style \| None` | `None` | Optional default style applied to top entity header banners unless overridden per `Entity`. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, entity: Entity, xy: tuple[float, float], show: bool \| None = None) -> Entity` | Register an [`Entity`](#entity) table centered at local coordinate `xy` and return it. |
| `add_relationship` | `method` | `(self, relationship: Relationship) -> Relationship` | Register a pre-constructed [`Relationship`](#relationship) instance with this diagram. |
| `connect` | `method` | `(self, start: Entity, end: Entity, cardinality: Cardinality = "1:*", start_side: Side = "auto", end_side: Side = "auto", start_column: str \| None = None, end_column: str \| None = None, label: str = "", style: Style \| None = None, text_style: Style \| None = None, routing: RoutingType = "orthogonal", padding: PaddingType = 0.0, show: bool = True) -> Relationship` | Create and register a Crow's Foot [`Relationship`](#relationship) between `start` and `end`. |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | Render the complete ER diagram onto the active canvas anchored at `xy`. |
| `entities` | `property` | `-> list[Entity]` | Return the list of [`Entity`](#entity) tables registered in the diagram. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Return the overall `(width, height)` of the diagram in unscaled local units. |
| `relationships` | `property` | `-> list[Relationship]` | Return the list of [`Relationship`](#relationship) edges registered in the diagram. |

---

## `class` Entity

Database table card displaying a header banner and 3-subcolumn schema rows (`PK`/`FK` badge, column name, and SQL type + nullability).

```python
Entity(
    name: str,
    width: float = 25.0,
    height: float | None = None,
    header_height: float = 4.0,
    row_height: float = 3.2,
    style: Style | None = None,
    header_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `erd.add(entity, xy=(cx, cy))`. When highlighting a focal table header with `Styles.PrimaryFlat`, pass `header_style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=11.0)` so the table name renders in crisp white text.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | Table or entity name displayed in the top header banner. |
| `width` | `float` | `25.0` | Table card width in local units (use `36.0`–`44.0` when showing SQL types with `(NN)`). |
| `height` | `float \| None` | `None` | Optional fixed table height override (`None` auto-computes `header_height + max(len(columns), 1) * row_height`). |
| `header_height` | `float` | `4.0` | Vertical height of the top table name banner. |
| `row_height` | `float` | `3.2` | Vertical height per column row. |
| `style` | `Style \| None` | `None` | Optional body fill, border, and column text style override (falls back to `erd.node_style`). |
| `header_style` | `Style \| None` | `None` | Optional header banner fill/border/text style override (falls back to `erd.header_style`). |
| `show` | `bool` | `True` | Visibility flag (`False` hides this entity card and connected relationships). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add_column` | `method` | `(self, name: str, type: str = "", pk: bool = False, fk: bool = False, nullable: bool = True) -> Entity` | Append a [`ColumnInfo`](#columninfo) row to this entity and return `self` for method chaining. |
| `add_columns` | `method` | `(self, columns: Sequence[Sequence[Any] \| ColumnInfo]) -> Entity` | Append multiple columns in batch from `(name, type, ...)` tuples or `ColumnInfo` instances and return `self`. |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the entity card. |
| `connect` | `method` | `(self, target: Entity, cardinality: Cardinality = "1:*", start_side: Side = "auto", end_side: Side = "auto", start_column: str \| None = None, end_column: str \| None = None, label: str = "", style: Style \| None = None, text_style: Style \| None = None, routing: RoutingType = "orthogonal", padding: PaddingType = 0.0, show: bool = True) -> Relationship` | Connect this registered entity to `target` and register the [`Relationship`](#relationship) on the parent `ERDiagram`. |
| `effective_height` | `property` | `-> float` | Actual rendered height of the entity card in local units. |
| `get_anchor` | `method` | `(self, side: Side, column_name: str \| None = None) -> tuple[float, float]` | Return boundary coordinate on `side`, optionally aligned to the exact row Y of `column_name`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-width/2, -effective_height/2, width/2, effective_height/2)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)` of the entity card. |

---

## `class` Relationship

Crow's Foot connector linking two [`Entity`](#entity) tables at either card midpoints or exact foreign-key column rows (`start_column`, `end_column`).

```python
Relationship(
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
) -> None
```

- **Coordinate Anchor**: Attaches to `start.get_anchor(start_side, start_column)` and `end.get_anchor(end_side, end_column)`. Register via `erd.connect(...)`, `entity.connect(...)`, or `erd.add_relationship(rel)`.

### Constructor Parameters & Attributes

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start` | [`Entity`](#entity) | *(Required)* | Source database entity. |
| `end` | [`Entity`](#entity) | *(Required)* | Target database entity. |
| `cardinality` | [`Cardinality`](#cardinality) | `"1:*"` | Crow's Foot multiplicity notation (`"1:*"`, `"1:1"`, `"1:1..*"`, `"1:0..1"`, `"0..1:1"`, `"0..1:*"`, `"*:*"`). |
| `start_side` | [`Side`](#side) | `"auto"` | Attachment side on `start` (`"left"`, `"right"`, `"top"`, `"bottom"`, `"auto"`). |
| `end_side` | [`Side`](#side) | `"auto"` | Attachment side on `end` (`"left"`, `"right"`, `"top"`, `"bottom"`, `"auto"`). |
| `start_column` | `str \| None` | `None` | Optional column name in `start` to snap the departure anchor directly to that row's Y coordinate (on `"left"`/`"right"` sides). |
| `end_column` | `str \| None` | `None` | Optional column name in `end` to snap the arrival anchor directly to that row's Y coordinate (on `"left"`/`"right"` sides). |
| `label` | `str` | `""` | Optional relationship verb or constraint label along the connector. |
| `style` | `Style \| None` | `None` | Optional line stroke style override (falls back to `erd.edge_style`). |
| `text_style` | `Style \| None` | `None` | Optional label typography style override (falls back to `erd.edge_text_style`). |
| `routing` | [`RoutingType`](#routingtype) | `"orthogonal"` | Path routing strategy (`"orthogonal"` or `"direct"`). |
| `padding` | `float \| tuple[float, float]` | `0.0` | Clearance gap between entity borders and Crow's Foot endpoints. |
| `show` | `bool` | `True` | Whether to render this relationship. |

---

## `type` RoutingType

Literal type controlling connector geometry for [`Relationship`](#relationship) edges.

```python
RoutingType = Literal["orthogonal", "direct"]
```

- **Coordinate Anchor**: Governs path segments between resolved `start` and `end` entity/column anchors.

| Literal Value | Path Geometry |
| :--- | :--- |
| `"orthogonal"` | Right-angled horizontal and vertical Manhattan segments (default; recommended for `start_column`/`end_column`). |
| `"direct"` | Straight Euclidean segment connecting the resolved anchors. |

---

## `type` Side

Literal type specifying the attachment side on an [`Entity`](#entity) card.

```python
Side = Literal["left", "right", "top", "bottom", "auto"]
```

- **Coordinate Anchor**: `"left"` and `"right"` support row-level Y snapping when paired with `start_column` / `end_column`; `"auto"` selects the nearest facing side automatically.
