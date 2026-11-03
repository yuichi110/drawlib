# drawlib.smartarts (Flows, Trees & Maps)

High-level SmartArt components (`from drawlib.smartarts import ...`) for interlocking chevron pipelines, radial cycles, tiered pyramids, milestone roadmaps, directory trees, multi-directional mind maps, geographical GeoJSON maps, and day/week/month schedule calendars. For box lists, bullet lists, feature cards, panels, KPI cards, matrix grids, vector source code, and tables, see [drawlib.smartarts (Lists, Cards & Tables)](09_smartarts_lists_cards.md).

```drawlib align=center code=fold file=10_smartarts_flows_trees_maps_hero.png caption="SmartArts Part 2 — ChevronProcess, TreeNode & Radial Cycle"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.smartarts import ChevronProcess, Cycle, TreeNode
from drawlib.styles import Colors, Styles

setup(width=120, height=56)

# Left Top: Sequential ChevronProcess Pipeline (Bottom-Left at (5, 38))
pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.add("1. Plan", description="RFC")
pipeline.add("2. Build", description="Verify", style=Styles.PrimaryNeutral)
pipeline.add(
    "3. Ship",
    description="Canary",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
pipeline.draw(xy=(5.0, 38.0), width=59.0, height=13.0, align="bottom_left")

# Left Bottom: TreeNode Hierarchy with Phosphor Icons (Top-Left at (6, 31))
TreeNode.register_drawing_item(
    name="hero_dir",
    location="before",
    padding_width=4.2,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 2.8},
)
TreeNode.register_drawing_item(
    name="hero_py",
    location="before",
    padding_width=4.2,
    function=phosphor.file_py,
    style=Styles.Dark,
    args={"width": 2.8},
)

root = TreeNode(
    "drawlib-service/",
    text_style=Styles.DarkBold.patch(text_size=10.5),
    line_style=Styles.Muted.patch(line_width=1.1),
    line_horizontal_margin=2.8,
    line_horizontal_length=2.8,
    line_vertical_margin=6.0,
    children=[
        TreeNode(
            "src/api/",
            text_style=Styles.DarkBold.patch(text_size=10.2),
            children=[
                TreeNode("router.py", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("hero_py"),
                TreeNode("worker.py", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("hero_py"),
            ],
        ).set_drawing_item("hero_dir"),
        TreeNode("deploy.py", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("hero_py"),
    ],
).set_drawing_item("hero_dir")
root.draw(xy=(6.0, 31.0))

line((67.5, 6.0), (67.5, 50.0), style=Styles.MutedDashed)

# Right: Radial Cycle with Central Hub (Center anchored at (93, 28))
cycle = Cycle(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    arrow_style=Styles.DarkFlat,
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=6.6,
    arrow_type="arc",
    arrow_width=1.4,
    arrow_head_width=3.6,
    arrow_color_mode="monochrome",
    arrow_gap=2.2,
)
cycle.add("Plan", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.5))
cycle.add("Code", style=Styles.PrimaryNeutral)
cycle.add("Test", style=Styles.SecondaryNeutral)
cycle.add("Ops", style=Styles.Neutral)
cycle.set_center(
    "PDCA",
    radius=6.8,
    style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
cycle.draw(xy=(93.0, 28.0), radius=15.2, align="center")

save()
```

## `class` ChevronProcess

Renders horizontal sequential process pipelines composed of interlocking arrowhead blocks (chevrons), supporting optional secondary descriptions, flat left-end start blocks, and per-step highlight styling.

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or **Center** `(cx, cy)` (`align="center"`).

```python
ChevronProcess(
    *,
    style: Style,
    text_style: Style,
    description_style: Style,
    corner_angle: Angle90 = 60.0,
    spacing: PosFloat = 1.5,
    flat_left_end: bool = False,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *Required* | Default polygon fill and border style for chevron steps. |
| `text_style` | `Style` | *Required* | Default text style for primary step titles. |
| `description_style` | `Style` | *Required* | Default text style for supporting step descriptions. |
| `corner_angle` | `Angle90` | `60.0` | Arrowhead tip angle in degrees (`10.0`–`80.0`), controlling horizontal tip indentation. |
| `spacing` | `PosFloat` | `1.5` | Horizontal gap in canvas units between adjacent chevrons. |
| `flat_left_end` | `bool` | `False` | When `True`, renders the first chevron with a flat vertical left edge instead of an inward notch. |

### Methods & Properties

```python
pipeline.items -> list[ChevronItem]

pipeline.add(
    text: str,
    *,
    description: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> ChevronItem

pipeline.draw(
    xy: Coordinate,
    width: PosFloat = 90.0,
    height: PosFloat = 12.0,
    item_width: PosFloat | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `ChevronItem` instances (`list[ChevronItem]`). |
| `add(text, *, description="", style=None, text_style=None, description_style=None, show=True)` | `method` | Append a process step with optional style overrides and return `ChevronItem`. Setting `show=False` hides the step while preserving sibling widths and positions. |
| `draw(xy, width=90.0, height=12.0, item_width=None, align="bottom_left", scale=1.0)` | `method` | Render the chevron pipeline at `xy` (`width` distributes block widths evenly when `item_width=None`), returning `self`. |

## `class` ChevronItem

Mutable Pydantic item model storing step labels, styles, and visibility for a single chevron in `ChevronProcess`.

- **Coordinate Anchor:** Positioned automatically along the horizontal axis of the parent `ChevronProcess`.

```python
ChevronItem(
    *,
    text: str,
    style: Style,
    text_style: Style,
    description_style: Style,
    description: str = "",
    show: bool = True,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Primary step title centered inside the chevron. |
| `style` | `Style` | *Required* | Chevron polygon fill and border style. |
| `text_style` | `Style` | *Required* | Text style for `text`. |
| `description_style` | `Style` | *Required* | Text style for `description`. |
| `description` | `str` | `""` | Optional secondary subtitle rendered beneath `text`. |
| `show` | `bool` | `True` | Visibility toggle; when `False`, skips drawing this chevron while preserving pipeline geometry. |

### Methods & Properties

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | Return a copy of the chevron item model with optional field updates (`pydantic.BaseModel`). |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Standard Pydantic serialization and validation methods (`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`). |

## `class` Cycle

Renders circular and cyclical process diagrams (PDCA loops, SRE incident lifecycles, token refresh cycles) with circular, rectangular, or borderless orbit nodes, curved block-arc or line-arc arrows, and an optional central hub (`CycleCenter`).

- **Coordinate Anchor:** **Center** `(cx, cy)` by default (`align="center"`), or **Bottom-Left** `(x, y)` (`align="bottom_left"`).

```python
Cycle(
    *,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    clockwise: bool = True,
    start_angle: Angle = 90.0,
    node_shape: Literal["circle", "rectangle", "none"] = "circle",
    node_radius: PosFloat = 8.0,
    node_width: PosFloat = 18.0,
    node_height: PosFloat = 10.0,
    description_placement: Literal["inside", "outside"] = "inside",
    arrow_type: Literal["arc", "line", "none"] = "arc",
    arrow_width: PosFloat = 2.0,
    arrow_head_width: PosFloat = 4.5,
    arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
    arrow_gap: PosFloat = 2.5,
    center_text: str = "",
    center_description: str = "",
    center_radius: PosFloat = 10.0,
    center_style: Style | None = None,
    center_text_style: Style | None = None,
    center_description_style: Style | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *Required* | Default fill and border style for orbit nodes. |
| `text_style` | `Style` | *Required* | Default text style for orbit node titles. |
| `description_style` | `Style \| None` | `None` | Default text style for orbit node descriptions. |
| `arrow_style` | `Style \| None` | `None` | Default arrow style (required when `arrow_color_mode="monochrome"` and `arrow_type != "none"`). |
| `clockwise` | `bool` | `True` | When `True`, steps advance clockwise from `start_angle`; otherwise counter-clockwise. |
| `start_angle` | `Angle` | `90.0` | Polar angle in degrees for `items[0]` (`90.0` places the first step at 12 o'clock). |
| `node_shape` | `Literal["circle", "rectangle", "none"]` | `"circle"` | Orbit node geometry (`"none"` renders text-only nodes). |
| `node_radius` | `PosFloat` | `8.0` | Radius of each orbit node when `node_shape="circle"`. |
| `node_width` | `PosFloat` | `18.0` | Width of each orbit node when `node_shape="rectangle"`. |
| `node_height` | `PosFloat` | `10.0` | Height of each orbit node when `node_shape="rectangle"`. |
| `description_placement` | `Literal["inside", "outside"]` | `"inside"` | Place `description` inside each node beneath `text` or radiating outward beyond the orbit. |
| `arrow_type` | `Literal["arc", "line", "none"]` | `"arc"` | Connector style along the orbit (`"arc"` curved block arrow, `"line"` curved stroke arrow, or `"none"`). |
| `arrow_width` | `PosFloat` | `2.0` | Body thickness of curved block arrows (`arrow_type="arc"`). |
| `arrow_head_width` | `PosFloat` | `4.5` | Arrowhead width for curved block arrows (`arrow_type="arc"`). |
| `arrow_color_mode` | `Literal["monochrome", "match_source", "match_target"]` | `"match_source"` | Color derivation mode for orbit arrows. |
| `arrow_gap` | `PosFloat` | `2.5` | Angular clearance in canvas units between node boundaries and arrow endpoints. |
| `center_text` | `str` | `""` | Optional label for a central hub circle (can also be configured via `set_center()`). |
| `center_description` | `str` | `""` | Optional secondary description inside the central hub. |
| `center_radius` | `PosFloat` | `10.0` | Radius of the central hub circle. |
| `center_style` | `Style \| None` | `None` | Shape style for the central hub circle. |
| `center_text_style` | `Style \| None` | `None` | Text style for `center_text`. |
| `center_description_style` | `Style \| None` | `None` | Text style for `center_description`. |

### Methods & Properties

```python
cycle.items -> list[CycleItem]
cycle.center -> CycleCenter

cycle.add(
    text: str,
    *,
    style: Style | None = None,
    description: str = "",
    text_style: Style | None = None,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    show: bool = True,
) -> CycleItem

cycle.set_center(
    text: str,
    *,
    style: Style | None = None,
    description: str = "",
    radius: PosFloat | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CycleCenter

cycle.draw(
    xy: Coordinate,
    radius: PosFloat = 35.0,
    align: Literal["center", "bottom_left"] = "center",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `CycleItem` models (`list[CycleItem]`). |
| `center` | `property` | Return the mutable `CycleCenter` hub model. |
| `add(text, *, style=None, description="", text_style=None, description_style=None, arrow_style=None, show=True)` | `method` | Append an orbit node and return `CycleItem`. |
| `set_center(text, *, style=None, description="", radius=None, text_style=None, description_style=None, show=True)` | `method` | Configure and enable the optional central hub node, returning `CycleCenter`. |
| `draw(xy, radius=35.0, align="center", scale=1.0)` | `method` | Render the cycle diagram with orbit `radius` anchored at `xy` (`"center"` or `"bottom_left"`), returning `self`. |

## `class` CycleCenter

Mutable Pydantic model representing the central hub node of a radial `Cycle` (accessed via `cycle.center` or returned by `cycle.set_center()`).

- **Coordinate Anchor:** Centered at the orbit origin `(cx, cy)` of the parent `Cycle`.

```python
CycleCenter(
    *,
    text: str,
    description: str = "",
    radius: float = 10.0,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Primary hub title text (empty `""` disables central hub rendering unless `set_center()` is called). |
| `description` | `str` | `""` | Optional secondary subtitle rendered below `text` inside the hub. |
| `radius` | `float` | `10.0` | Radius of the central hub circle in canvas units. |
| `style` | `Style \| None` | `None` | Circle fill and border style for the hub. |
| `text_style` | `Style \| None` | `None` | Text style for `text`. |
| `description_style` | `Style \| None` | `None` | Text style for `description`. |
| `show` | `bool` | `True` | Visibility flag for the central hub node. |

### Methods & Properties

```python
center.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
center.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | Return a copy of the center hub model with optional field updates (`pydantic.BaseModel`). |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Standard Pydantic serialization and validation methods (`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`). |

## `class` CycleItem

Mutable Pydantic item model representing a single orbit node and its outgoing connector style in `Cycle`.

- **Coordinate Anchor:** Placed along polar orbit angle $\theta_i = \text{start\_angle} \mp i \cdot (360^\circ / N)$ at distance `radius` from `Cycle` center.

```python
CycleItem(
    *,
    text: str,
    style: Style,
    description: str = "",
    text_style: Style | None = None,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    show: bool = True,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Primary step label rendered inside the orbit node. |
| `style` | `Style` | *Required* | Shape fill and border style for this orbit node. |
| `description` | `str` | `""` | Optional supporting description (placed `"inside"` or `"outside"` per `Cycle` config). |
| `text_style` | `Style \| None` | `None` | Per-item override for `text` style. |
| `description_style` | `Style \| None` | `None` | Per-item override for `description` style. |
| `arrow_style` | `Style \| None` | `None` | Per-item override for the outgoing connector arrow from this step. |
| `show` | `bool` | `True` | Visibility toggle; when `False`, hides the node and adjacent arrow while keeping remaining nodes at fixed orbit angles. |

### Methods & Properties

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | Return a copy of the cycle item model with optional field updates (`pydantic.BaseModel`). |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Standard Pydantic serialization and validation methods (`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`). |

## `class` Pyramid

Renders hierarchical tiered pyramids composed of an apex triangle and progressively widening trapezoid slices in four orientations (`"bottom"`, `"top"`, `"left"`, `"right"`), supporting both uniform (`draw`) and custom per-tier (`draw_flexible`) heights.

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or **Center** `(cx, cy)` (`align="center"`).

```python
Pyramid(
    *,
    style: Style,
    text_style: Style,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *Required* | Default polygon fill and border style for pyramid tiers. |
| `text_style` | `Style` | *Required* | Default text style for tier labels. |

### Methods & Properties

```python
pyramid.items -> list[PyramidItem]

pyramid.add(
    text: str,
    *,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> PyramidItem

pyramid.draw(
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    margin: PosFloat,
    direction: Literal["bottom", "top", "left", "right"] = "bottom",
    order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self

pyramid.draw_flexible(
    xy: Coordinate,
    width: PosFloat,
    item_heights: list[PosFloat],
    margins: list[PosFloat],
    direction: Literal["bottom", "top", "left", "right"] = "bottom",
    order: Literal["vertex_to_base", "base_to_vertex"] = "vertex_to_base",
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `PyramidItem` instances (`list[PyramidItem]`). |
| `add(text, *, style=None, text_style=None, show=True)` | `method` | Append a pyramid tier and return `PyramidItem`. |
| `draw(xy, width, height, margin, direction="bottom", order="vertex_to_base", align="bottom_left", scale=1.0)` | `method` | Render uniform-height tiers (`direction` sets where the wide base sits; `order` controls whether `items[0]` is at the vertex or base), returning `self`. |
| `draw_flexible(xy, width, item_heights, margins, direction="bottom", order="vertex_to_base", align="bottom_left", scale=1.0)` | `method` | Render tiers with explicit `item_heights` (length `N`) and inter-tier `margins` (length `N - 1`), returning `self`. |

## `class` PyramidItem

Mutable Pydantic item model storing label text, polygon style, text style, and visibility for a single tier in `Pyramid`.

- **Coordinate Anchor:** Positioned automatically within the parent `Pyramid` bounding box.

```python
PyramidItem(
    *,
    style: Style,
    text: str,
    text_style: Style,
    show: bool = True,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *Required* | Polygon fill and border style for this tier. |
| `text` | `str` | *Required* | Label centered inside the triangle/trapezoid slice. |
| `text_style` | `Style` | *Required* | Text style for `text`. |
| `show` | `bool` | `True` | Visibility toggle; when `False`, hides this slice while keeping all sibling tier geometries intact. |

### Methods & Properties

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | Return a copy of the pyramid item model with optional field updates (`pydantic.BaseModel`). |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Standard Pydantic serialization and validation methods (`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`). |

## `class` Roadmap

Renders chronological milestone timelines, release roadmaps, and incident chronicles along a straight or quadratic-Bezier curved vertical spine (`direction="vertical"`) or a single-row / alternating horizontal spine (`direction="horizontal"`), pairing numbered/labeled spine badges with rounded-rectangle or pill milestone cards.

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or **Center** `(cx, cy)` (`align="center"`).

```python
Roadmap(
    *,
    style: Style,
    text_style: Style,
    spine_style: Style,
    badge_style: Style,
    badge_text_style: Style,
    description_style: Style | None = None,
    icon_style: Style | None = None,
    direction: Literal["vertical", "horizontal"] = "vertical",
    curve_bend: float = 0.0,
    card_shape: Literal["pill", "rounded_rect"] = "rounded_rect",
    alternating: bool = False,
    spacing: PosFloat = 2.5,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `style` | `Style` | *Required* | Default style for milestone card containers. |
| `text_style` | `Style` | *Required* | Default text style for milestone titles. |
| `spine_style` | `Style` | *Required* | Line style for the timeline spine arrow and card connector ticks. |
| `badge_style` | `Style` | *Required* | Default shape style for milestone badges mounted on the spine. |
| `badge_text_style` | `Style` | *Required* | Default text style for spine badge labels (`badge_text`). |
| `description_style` | `Style \| None` | `None` | Default text style for milestone descriptions (required when `description` is non-empty). |
| `icon_style` | `Style \| None` | `None` | Default style passed to milestone card `icon` callables (required when `icon` is provided). |
| `direction` | `Literal["vertical", "horizontal"]` | `"vertical"` | Spine orientation (`"vertical"` top-to-bottom or `"horizontal"` left-to-right). |
| `curve_bend` | `float` | `0.0` | Quadratic Bezier curvature (`-0.5` to `0.5`) applied when `direction="vertical"` (`0.0` draws a straight spine). |
| `card_shape` | `Literal["pill", "rounded_rect"]` | `"rounded_rect"` | Milestone card container shape. |
| `alternating` | `bool` | `False` | When `True` with `direction="horizontal"`, alternates milestone cards above and below a centered horizontal spine. |
| `spacing` | `PosFloat` | `2.5` | Gap between adjacent milestone cards in canvas units. |

### Methods & Properties

```python
rm.items -> list[RoadmapItem]

rm.add(
    text: str,
    description: str = "",
    *,
    badge_text: str | None = None,
    icon: Callable[..., Any] | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    icon_style: Style | None = None,
    show: bool = True,
) -> RoadmapItem

rm.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `RoadmapItem` models (`list[RoadmapItem]`). |
| `add(text, description="", *, badge_text=None, icon=None, ...)` | `method` | Append a milestone (auto-assigning 1-based `"1"`, `"2"`, ... when `badge_text=None`) and return `RoadmapItem`. |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Render the spine, badges, connectors, and milestone cards inside `(width, height)` anchored at `xy`, returning `self`. |

## `class` RoadmapItem

Mutable Pydantic item model representing a single milestone node and card in `Roadmap`.

- **Coordinate Anchor:** Positioned automatically along the vertical or horizontal spine of the parent `Roadmap`.

```python
RoadmapItem(
    *,
    text: str,
    description: str = "",
    badge_text: str | None = None,
    icon: Callable[..., Any] | None = None,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    badge_style: Style,
    badge_text_style: Style,
    icon_style: Style | None = None,
    show: bool = True,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Primary milestone or phase title text. |
| `description` | `str` | `""` | Optional supporting subtitle or detail text. |
| `badge_text` | `str \| None` | `None` | Short label displayed on the spine badge (e.g. `"1"`, `"Q1"`, `"T+0m"`). |
| `icon` | `Callable[..., Any] \| None` | `None` | Optional icon callable rendered inside the milestone card. |
| `style` | `Style` | *Required* | Milestone card container style. |
| `text_style` | `Style` | *Required* | Text style for `text`. |
| `description_style` | `Style \| None` | `None` | Optional text style for `description`. |
| `badge_style` | `Style` | *Required* | Shape style for the milestone badge on the spine. |
| `badge_text_style` | `Style` | *Required* | Text style for `badge_text`. |
| `icon_style` | `Style \| None` | `None` | Optional style passed to `icon`. |
| `show` | `bool` | `True` | Visibility toggle; when `False`, hides this milestone's badge, tick, and card while preserving spine geometry. |

### Methods & Properties

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | Return a copy of the roadmap item model with optional field updates (`pydantic.BaseModel`). |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Standard Pydantic serialization and validation methods (`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`). |

## `class` TreeNode

Renders hierarchical file-system and directory trees with orthogonal L-shaped connector lines, downward style/spacing cascading from the root node, and named prepended/appended icon items (`register_drawing_item` + `set_drawing_item`).

- **Coordinate Anchor:** **Fixed Top-Left** `(x, y)` — the root label is placed at `xy` and descendant rows step downward (`-line_vertical_margin`). The root node must specify `text_style`, `line_style`, `line_horizontal_margin`, `line_horizontal_length`, and `line_vertical_margin`.

```python
TreeNode(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: PosFloat | None = None,
    line_horizontal_length: PosFloat | None = None,
    line_vertical_margin: PosFloat | None = None,
    children: list[TreeNode] | None = None,
    show: bool = True,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Node text label (e.g. `"src/"`, `"main.py"`). |
| `text_style` | `Style \| None` | `None` | Text style for this node (required on root; inherited by children when `None`). |
| `line_style` | `Style \| None` | `None` | Orthogonal connector line style (required on root; inherited by children when `None`). |
| `line_horizontal_margin` | `PosFloat \| None` | `None` | Horizontal indent before the vertical branch stem (required on root; cascades to children). |
| `line_horizontal_length` | `PosFloat \| None` | `None` | Horizontal tick length from branch stem to child label (required on root; cascades to children). |
| `line_vertical_margin` | `PosFloat \| None` | `None` | Vertical row step between consecutive tree rows (required on root; cascades to children). |
| `children` | `list[TreeNode] \| None` | `None` | Optional list of pre-constructed child `TreeNode` instances. |
| `show` | `bool` | `True` | Visibility flag; setting `show=False` hides the node and its tick while preserving vertical row slots. |

### Methods & Properties

```python
node.text -> str
node.text_style -> Style | None
node.line_style -> Style | None
node.children -> list[TreeNode]

node.add(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: PosFloat | None = None,
    line_horizontal_length: PosFloat | None = None,
    line_vertical_margin: PosFloat | None = None,
    show: bool = True,
) -> Self

TreeNode.register_drawing_item(
    name: str,
    location: Literal["before", "after"],
    padding_width: float,
    function: Callable[..., Any],
    style: Style,
    args: dict[str, Any],
) -> None

node.set_drawing_item(name: str) -> Self

node.draw(
    xy: Coordinate,
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `text` | `property` | Get or set the node text label (`str`). |
| `text_style` | `property` | Get or set the node text style (`Style \| None`). |
| `line_style` | `property` | Get or set the node connector line style (`Style \| None`). |
| `children` | `property` | Return the list of child `TreeNode` instances (`list[TreeNode]`). |
| `add(text, *, ...)` | `method` | Construct and append a child `TreeNode` from `text: str` (pass pre-built `TreeNode` objects via `children=[...]` instead), returning the newly created child node. |
| `register_drawing_item(name, location, padding_width, function, style, args)` | `classmethod` | Register a reusable icon/shape callable (`location="before"` or `"after"`) that nodes can attach by `name`. |
| `set_drawing_item(name)` | `method` | Attach a previously registered drawing item (`name`) to this node and return `self` for chaining. |
| `draw(xy, scale=1.0)` | `method` | Render the tree rooted at top-left `xy` with proportional `scale`, returning `self`. |

## `class` MindMapNode

Renders hierarchical trees, organization charts, and 4-way radial mind maps (`branch="bottom" | "top" | "left" | "right"`) with automatic two-pass subtree bounding measurement and right-angled orthogonal fork routing.

- **Coordinate Anchor:** **Fixed Root Center** `(cx, cy)` — `draw(xy)` places the center of the root node at `xy`. The root node must specify `style`, `text_style`, and `line_style`.

```python
MindMapNode(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "ellipse", "none"] | None = None,
    width: PosFloat | None = None,
    height: PosFloat | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: PosFloat | None = None,
    vertical_margin: PosFloat | None = None,
    line_length: PosFloat | None = None,
    xy_shift: Coordinate | None = None,
    children: list[MindMapNode] | None = None,
    show: bool = True,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Node text label. |
| `branch` | `Literal["bottom", "top", "left", "right"] \| None` | `None` | Expansion direction for this node/subtree (assign distinct directions on direct root children for a 4-way radial mind map). |
| `shape` | `Literal["rectangle", "ellipse", "none"] \| None` | `None` | Node body shape (`"rectangle"` default on root; `"none"` renders a borderless text node). |
| `width` | `PosFloat \| None` | `None` | Explicit node width in canvas units (cascades downward unless overridden). |
| `height` | `PosFloat \| None` | `None` | Explicit node height in canvas units (cascades downward unless overridden). |
| `style` | `Style \| None` | `None` | Node fill/border style (required on root; cascades to children). |
| `text_style` | `Style \| None` | `None` | Node text style (required on root; cascades to children). |
| `line_style` | `Style \| None` | `None` | Orthogonal fork connector line style (required on root; cascades to children). |
| `horizontal_margin` | `PosFloat \| None` | `None` | Horizontal sibling spacing in canvas units. |
| `vertical_margin` | `PosFloat \| None` | `None` | Vertical sibling spacing in canvas units. |
| `line_length` | `PosFloat \| None` | `None` | Distance along the branch axis between parent and child tiers. |
| `xy_shift` | `Coordinate \| None` | `None` | Optional `(dx, dy)` post-layout offset applied to fine-tune node placement. |
| `children` | `list[MindMapNode] \| None` | `None` | Optional list of pre-constructed child `MindMapNode` instances. |
| `show` | `bool` | `True` | Visibility toggle; when `False`, hides the node and incoming branch while keeping sibling layout fixed. |

### Methods & Properties

```python
node.text -> str
node.branch -> Literal["bottom", "top", "left", "right"] | None
node.shape -> Literal["rectangle", "ellipse", "none"] | None
node.width -> float | None
node.height -> float | None
node.style -> Style | None
node.text_style -> Style | None
node.line_style -> Style | None
node.children -> list[MindMapNode]

node.add(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "ellipse", "none"] | None = None,
    width: PosFloat | None = None,
    height: PosFloat | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: PosFloat | None = None,
    vertical_margin: PosFloat | None = None,
    line_length: PosFloat | None = None,
    xy_shift: Coordinate | None = None,
    show: bool = True,
) -> Self

node.draw(
    xy: Coordinate,
    branch: Literal["bottom", "top", "left", "right"] = "bottom",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `text`, `branch`, `shape`, `width`, `height`, `style`, `text_style`, `line_style` | `property` | Read/write properties for inspecting or mutating node geometry and styles between frames. |
| `children` | `property` | Return the list of child `MindMapNode` instances (`list[MindMapNode]`). |
| `add(text, *, ...)` | `method` | Construct and append a child `MindMapNode` from `text: str`, returning the created child node. |
| `draw(xy, branch="bottom", scale=1.0)` | `method` | Compute two-pass layout and render the mind map centered at root `xy` (`branch` sets fallback direction), returning `self`. |

## `class` GeoMap

Renders vector geographical maps onto the canvas without external GIS dependencies, supporting built-in world/regional presets (`GeoMap.World.*` such as `All`, `Asia`, `Europe`, `NorthAmerica`), 215 country/territory maps (`GeoMap.Countries.*`), 16 metropolitan city maps (`GeoMap.Cities.*`), and custom `.geojson` file paths or dictionaries.

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or **Center** `(cx, cy)` (`align="center"`). At least one of `width` or `height` must be supplied to `draw()`.

```python
GeoMap(
    target: World | type[World] | Countries | Cities | str | Path | dict[str, Any],
    *,
    area_style: Style | None = None,
    background_style: Style | None = None,
    id_key: str | None = None,
    name_key: str | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `target` | `World \| type[World] \| Countries \| Cities \| str \| Path \| dict[str, Any]` | *Required* | Preset map target (`GeoMap.World.Asia`, `GeoMap.Countries.Japan`, `GeoMap.Cities.Japan_Tokyo`) or custom GeoJSON file path / `dict`. |
| `area_style` | `Style \| None` | `None` | Default polygon fill/stroke style for map regions (defaults internally to `Styles.Neutral` when `None`). |
| `background_style` | `Style \| None` | `None` | Optional ocean/frame background rectangle style drawn behind the map polygons. |
| `id_key` | `str \| None` | `None` | Custom GeoJSON feature `properties` key used to extract region identifiers. |
| `name_key` | `str \| None` | `None` | Custom GeoJSON feature `properties` key used to extract human-readable region names. |

### Methods & Properties

```python
m.data -> GeoData

m.get_areas() -> list[str]

m.set_area_styles(
    areas: list[str],
    style: Style,
) -> Self

m.draw(
    xy: tuple[float, float] = (0.0, 0.0),
    width: float | None = None,
    height: float | None = None,
    *,
    lon_range: tuple[float, float] | None = None,
    lat_range: tuple[float, float] | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self

m.get_area_xy(area: str) -> tuple[float, float]

m.lonlat_to_xy(lon: float, lat: float) -> tuple[float, float]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `data` | `property` | Return the normalized `GeoData` model containing map polygons, bounding boxes, and viewport metadata. |
| `get_areas()` | `method` | Return the ordered list of canonical region names in this map (callable before or after `draw()`). |
| `set_area_styles(areas, style)` | `method` | Assign `style` to regions matching canonical names, ISO codes (`"JP"`, `"JPN"`), or Japanese names (`"日本"`), returning `self`. |
| `draw(xy=(0.0, 0.0), width=None, height=None, *, lon_range=None, lat_range=None, align="bottom_left", scale=1.0)` | `method` | Render the map onto the canvas (pass `width` or `height` alone for cosine-corrected natural aspect fit, or both with `lon_range`/`lat_range`), returning `self`. |
| `get_area_xy(area)` | `method` | Return the representative canvas `(x, y)` coordinate of a named region (**must be called after `draw()`**). |
| `lonlat_to_xy(lon, lat)` | `method` | Project a `(lon, lat)` decimal-degree coordinate to canvas `(x, y)` on the last drawn map (**must be called after `draw()`**). |

## `class` DayCalendar

Renders a single-day schedule in either `direction="vertical"` (top-to-bottom hourly axis with automatic X-axis parallel lane splitting) or `direction="horizontal"` (left-to-right hourly axis with Y-axis lane splitting), plus an optional `"All-day"` (`"全日"`) banner. Accepts strict ISO 8601 `"YYYY-MM-DD"` and `"YYYY-MM-DD HH:MM"` strings (does **not** take `sunday_text_style` / `saturday_text_style`).

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or `"center"` / `"top_left"`.

```python
DayCalendar(
    *,
    date: str = "2026-10-13",
    direction: Literal["vertical", "horizontal"] = "vertical",
    start_hour: int = 9,
    end_hour: int = 18,
    hour_step: PosInt = 1,
    show_all_day: bool | None = None,
    all_day_label: str | None = None,
    title: str | None = None,
    lang: Literal["en", "ja"] = "en",
    cell_style: Style,
    text_style: Style,
    header_style: Style,
    header_text_style: Style,
    border_style: Style,
    event_style: Style | None = None,
    event_text_style: Style | None = None,
    title_style: Style | None = None,
    title_text_style: Style | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `date` | `str` | `"2026-10-13"` | Target calendar date in strict `"YYYY-MM-DD"` format. |
| `direction` | `Literal["vertical", "horizontal"]` | `"vertical"` | Time-axis orientation (`"vertical"` top-to-bottom or `"horizontal"` left-to-right). |
| `start_hour` | `int` | `9` | Starting hour of the displayed time grid (`0`–`23`). |
| `end_hour` | `int` | `18` | Ending hour of the displayed time grid (`> start_hour`, up to `24`). |
| `hour_step` | `PosInt` | `1` | Hour interval between grid tick labels (`>= 1`). |
| `show_all_day` | `bool \| None` | `None` | `None` auto-displays the All-Day track when `>= 1` all-day item is added; `True`/`False` forces visibility. |
| `all_day_label` | `str \| None` | `None` | Custom label for the All-Day track (defaults to `"All-day"` for `"en"` or `"全日"` for `"ja"`). |
| `title` | `str \| None` | `None` | Header title (`None` auto-formats date + weekday; `""` hides the title bar). |
| `lang` | `Literal["en", "ja"]` | `"en"` | Localization language for auto-generated weekday and all-day labels. |
| `cell_style` | `Style` | *Required* | Background style for time-grid cells. |
| `text_style` | `Style` | *Required* | Text style for hour axis labels. |
| `header_style` | `Style` | *Required* | Background style for axis/column headers. |
| `header_text_style` | `Style` | *Required* | Text style for header labels. |
| `border_style` | `Style` | *Required* | Grid and frame border line style. |
| `event_style` | `Style \| None` | `None` | Default box style for added events. |
| `event_text_style` | `Style \| None` | `None` | Default text style for event titles. |
| `title_style` | `Style \| None` | `None` | Optional background style override for the top title bar. |
| `title_text_style` | `Style \| None` | `None` | Optional text style override for the top title bar. |

### Methods & Properties

```python
dcal.items -> list[CalendarItem]

dcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    all_day: bool | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

dcal.get_time_xy(
    dt: str,
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> tuple[float, float]

dcal.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `CalendarItem` models (`list[CalendarItem]`). |
| `add(start, end=None, text="", *, description="", all_day=None, style=None, text_style=None, description_style=None, show=True)` | `method` | Register a timed block (`"YYYY-MM-DD HH:MM"`) or all-day banner (`"YYYY-MM-DD"`) and return `CalendarItem`. |
| `get_time_xy(dt, xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Return canvas center `(cx, cy)` corresponding to `"YYYY-MM-DD"` (all-day slot) or `"YYYY-MM-DD HH:MM"` (timed slot). |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Render the day schedule onto the canvas and return `self`. |

## `class` WeekCalendar

Renders multi-day hourly time-grid calendars (7-day week, 5-day workweek, or custom `start_date`..`end_date` / `columns` range) with a top All-Day spanning banner and three multi-day timed rendering modes (`span_mode="columns" | "box" | "all_day"`).

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or `"center"` / `"top_left"`.

```python
WeekCalendar(
    *,
    start_date: str = "2026-10-11",
    end_date: str | None = None,
    num_days: PosInt = 7,
    columns: list[str] | None = None,
    start_hour: int = 9,
    end_hour: int = 18,
    hour_step: PosInt = 1,
    show_all_day: bool | None = None,
    all_day_label: str | None = None,
    title: str | None = None,
    lang: Literal["en", "ja"] = "en",
    cell_style: Style,
    text_style: Style,
    header_style: Style,
    header_text_style: Style,
    border_style: Style,
    event_style: Style | None = None,
    event_text_style: Style | None = None,
    sunday_text_style: Style | None = None,
    saturday_text_style: Style | None = None,
    title_style: Style | None = None,
    title_text_style: Style | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start_date` | `str` | `"2026-10-11"` | First displayed date in strict `"YYYY-MM-DD"` format. |
| `end_date` | `str \| None` | `None` | Optional inclusive end date (`"YYYY-MM-DD"`); overrides `num_days` when provided. |
| `num_days` | `PosInt` | `7` | Number of day columns when `end_date=None`. |
| `columns` | `list[str] \| None` | `None` | Optional custom column header labels matching the displayed day count. |
| `start_hour` | `int` | `9` | Top hour of the vertical time grid (`0`–`23`). |
| `end_hour` | `int` | `18` | Bottom hour of the vertical time grid (`> start_hour`, up to `24`). |
| `hour_step` | `PosInt` | `1` | Hour interval between time-gutter labels. |
| `show_all_day` | `bool \| None` | `None` | `None` auto-shows the top All-Day band when all-day events exist; `True`/`False` forces visibility. |
| `all_day_label` | `str \| None` | `None` | Custom label for the All-Day gutter (`"All-day"` / `"全日"` by default). |
| `title` | `str \| None` | `None` | Top title bar text (`None` auto-generates range title; `""` hides title bar). |
| `lang` | `Literal["en", "ja"]` | `"en"` | Localization language for weekday headers and default labels. |
| `cell_style` | `Style` | *Required* | Time-slot cell background style. |
| `text_style` | `Style` | *Required* | Time-gutter and weekday text style. |
| `header_style` | `Style` | *Required* | Day column header background style. |
| `header_text_style` | `Style` | *Required* | Day column header text style. |
| `border_style` | `Style` | *Required* | Grid line style. |
| `event_style` | `Style \| None` | `None` | Default event block/bar style. |
| `event_text_style` | `Style \| None` | `None` | Default event title text style. |
| `sunday_text_style` | `Style \| None` | `None` | Optional header text style override for Sunday columns. |
| `saturday_text_style` | `Style \| None` | `None` | Optional header text style override for Saturday columns. |
| `title_style` | `Style \| None` | `None` | Optional background style override for the top title bar. |
| `title_text_style` | `Style \| None` | `None` | Optional text style override for the top title bar. |

### Methods & Properties

```python
wcal.items -> list[CalendarItem]

wcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    all_day: bool | None = None,
    span_mode: Literal["columns", "box", "all_day"] = "columns",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

wcal.get_slot_xy(
    dt: str,
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> tuple[float, float]

wcal.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `CalendarItem` models (`list[CalendarItem]`). |
| `add(start, end=None, text="", *, description="", all_day=None, span_mode="columns", ...)` | `method` | Register an all-day X-axis bar or timed event (`span_mode="columns"`, `"box"`, or `"all_day"`) and return `CalendarItem`. |
| `get_slot_xy(dt, xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Return canvas `(cx, cy)` for `"YYYY-MM-DD"` (all-day header cell) or `"YYYY-MM-DD HH:MM"` (hourly grid slot). |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Render the week calendar onto the canvas and return `self`. |

## `class` MonthCalendar

Renders Outlook / Google Calendar-style 7-column monthly (`end_date=None`) or multi-week cross-month (`end_date="YYYY-MM-DD"`) grid calendars with automatic cross-week event wrapping (`←` / `→`) and vertical lane stacking (`max_tracks`).

- **Coordinate Anchor:** **Bottom-Left** `(x, y)` by default (`align="bottom_left"`), or `"center"` / `"top_left"`.

```python
MonthCalendar(
    *,
    start_date: str = "2026-10-01",
    end_date: str | None = None,
    first_weekday: Literal["sun", "mon"] = "sun",
    title: str | None = None,
    lang: Literal["en", "ja"] = "en",
    max_tracks: PosInt = 3,
    cell_style: Style,
    text_style: Style,
    header_style: Style,
    header_text_style: Style,
    border_style: Style,
    event_style: Style | None = None,
    event_text_style: Style | None = None,
    sunday_text_style: Style | None = None,
    saturday_text_style: Style | None = None,
    title_style: Style | None = None,
    title_text_style: Style | None = None,
) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start_date` | `str` | `"2026-10-01"` | Target month date (or start date of a multi-week span when `end_date` is set) in `"YYYY-MM-DD"` format. |
| `end_date` | `str \| None` | `None` | Optional inclusive end date (`"YYYY-MM-DD"`) for multi-week / cross-month grids; `None` renders the full month of `start_date`. |
| `first_weekday` | `Literal["sun", "mon"]` | `"sun"` | Left-most weekday column (`"sun"` or `"mon"`). |
| `title` | `str \| None` | `None` | Top title bar text (`None` auto-generates month/year title; `""` hides title bar). |
| `lang` | `Literal["en", "ja"]` | `"en"` | Localization language for month title and weekday headers. |
| `max_tracks` | `PosInt` | `3` | Maximum stacked horizontal event bar lanes per week row (`>= 1`). |
| `cell_style` | `Style` | *Required* | Date cell background style. |
| `text_style` | `Style` | *Required* | Date number text style. |
| `header_style` | `Style` | *Required* | Weekday header row background style. |
| `header_text_style` | `Style` | *Required* | Weekday header text style. |
| `border_style` | `Style` | *Required* | Calendar cell grid line style. |
| `event_style` | `Style \| None` | `None` | Default style for spanning event bars. |
| `event_text_style` | `Style \| None` | `None` | Default text style for event bar labels. |
| `sunday_text_style` | `Style \| None` | `None` | Optional date/header text style override for Sundays. |
| `saturday_text_style` | `Style \| None` | `None` | Optional date/header text style override for Saturdays. |
| `title_style` | `Style \| None` | `None` | Optional background style override for the top title bar. |
| `title_text_style` | `Style \| None` | `None` | Optional text style override for the top title bar. |

### Methods & Properties

```python
mcal.items -> list[CalendarItem]

mcal.add(
    start: str,
    end: str | None = None,
    text: str = "",
    *,
    description: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CalendarItem

mcal.get_date_xy(
    date: str,
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> tuple[float, float]

mcal.draw(
    xy: Coordinate,
    width: PosFloat = 100.0,
    height: PosFloat = 60.0,
    *,
    align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
    scale: PosFloat = 1.0,
) -> Self
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `items` | `property` | Return the ordered list of registered `CalendarItem` models (`list[CalendarItem]`). |
| `add(start, end=None, text="", *, description="", style=None, text_style=None, description_style=None, show=True)` | `method` | Register a single-day or multi-day spanning event bar and return `CalendarItem`. |
| `get_date_xy(date, xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Return canvas center `(cx, cy)` of the cell matching `"YYYY-MM-DD"`. |
| `draw(xy, width=100.0, height=60.0, *, align="bottom_left", scale=1.0)` | `method` | Render the month/multi-week grid calendar onto the canvas and return `self`. |

## `class` CalendarItem

Mutable Pydantic item model representing an event block or all-day spanning bar shared across `DayCalendar`, `WeekCalendar`, and `MonthCalendar`.

- **Coordinate Anchor:** Mapped automatically from ISO 8601 `start` / `end` timestamps onto the parent calendar's date/time grid.

```python
CalendarItem(
    *,
    start: str,
    end: str | None = None,
    text: str = "",
    description: str = "",
    all_day: bool | None = None,
    span_mode: Literal["columns", "box", "all_day"] = "columns",
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    show: bool = True,
) -> None
```

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start` | `str` | *Required* | Start date (`"YYYY-MM-DD"`) or datetime (`"YYYY-MM-DD HH:MM"`). |
| `end` | `str \| None` | `None` | Optional end date or datetime (defaults to `start` when `None` for single-day events). |
| `text` | `str` | `""` | Primary event title rendered inside the bar or time block. |
| `description` | `str` | `""` | Optional secondary subtitle or time note. |
| `all_day` | `bool \| None` | `None` | Explicit All-Day override (`None` infers `True` for `"YYYY-MM-DD"` and `False` for `"YYYY-MM-DD HH:MM"`). |
| `span_mode` | `Literal["columns", "box", "all_day"]` | `"columns"` | Multi-day timed rendering mode in `WeekCalendar` (`"columns"` per-day segments, `"box"` unified rectangle, or `"all_day"` top banner). |
| `style` | `Style` | *Required* | Event bar/box fill and border style. |
| `text_style` | `Style` | *Required* | Text style for `text`. |
| `description_style` | `Style \| None` | `None` | Optional text style for `description`. |
| `show` | `bool` | `True` | Visibility toggle; when `False`, hides this event while preserving calendar track/lane geometry. |

### Methods & Properties

```python
item.model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
item.model_dump(*, mode: Literal["json", "python"] | str = "python", **kwargs: Any) -> dict[str, Any]
```

| Member | Kind | Description |
| :--- | :--- | :--- |
| `model_copy(*, update=None, deep=False)` | `method` | Return a copy of the calendar item model with optional field updates (`pydantic.BaseModel`). |
| `model_dump(**kwargs)` / `model_validate(obj)` | `method` | Standard Pydantic serialization and validation methods (`model_dump_json`, `model_validate_json`, `model_json_schema`, `model_fields_set`, `model_extra`). |
