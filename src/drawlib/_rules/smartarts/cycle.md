# Drawlib Cycle SmartArt Guidelines (`lib-smartarts-cycle`)

`Cycle` renders cyclical workflows, feedback loops, and radial hubs—such as DevOps PDCA iterations, token refresh flows, SRE incident lifecycles, and distributed consensus rounds.

---

## 1. Architecture & Circular Geometry

- **Anchor (`align`)**: Coordinate `xy=(x, y)`. Default `align="center"` anchors the circular orbit center `(cx, cy)`. If `align="bottom_left"`, `xy` anchors the bottom-left corner of the overall bounding box.
- **Node Placements**: Steps are distributed evenly along orbit radius $R$:
  $$\theta_i = \text{start\_angle} \mp \left(i \cdot \frac{360^\circ}{N}\right)$$
- **Curved Connectors (`arrow_type`)**: Steps are connected along the orbit circle by curved block arrows (`arrow_type="arc"`), curved line arrows (`"line"`), or no arrows (`"none"`).
- **Center Hub (`set_center` / `.center`)**: Optional central hub node (`CycleCenter`) transforms the diagram into a Radial Cycle.

---

## 2. Constructor, `CycleItem`, `CycleCenter` & Methods

```python
from drawlib.smartarts import Cycle, CycleCenter, CycleItem

cycle = Cycle(
    *,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    clockwise: bool = True,
    start_angle: float = 90.0,
    node_shape: Literal["circle", "rectangle", "none"] = "circle",
    node_radius: float = 8.0,
    node_width: float = 18.0,
    node_height: float = 10.0,
    description_placement: Literal["inside", "outside"] = "inside",
    arrow_type: Literal["arc", "line", "none"] = "arc",
    arrow_width: float = 2.0,
    arrow_head_width: float = 4.5,
    arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
    arrow_gap: float = 2.5,
    center_text: str = "",
    center_description: str = "",
    center_radius: float = 10.0,
    center_style: Style | None = None,
    center_text_style: Style | None = None,
    center_description_style: Style | None = None,
)
```

### Public Models (`CycleItem`, `CycleCenter`) & Properties

- `cycle.items -> list[CycleItem]`: Returns the list of registered `CycleItem` instances.
  - `CycleItem` attributes: `text: str`, `style: Style`, `description: str = ""`, `text_style: Style | None = None`, `description_style: Style | None = None`, `arrow_style: Style | None = None`, `show: bool = True`.
- `cycle.center -> CycleCenter`: Returns the central hub model (`CycleCenter`).
  - `CycleCenter` attributes: `text: str`, `description: str = ""`, `radius: float = 10.0`, `style: Style | None = None`, `text_style: Style | None = None`, `description_style: Style | None = None`, `show: bool = True`.

### Methods

```python
item = cycle.add(
    text: str,
    *,
    style: Style | None = None,
    description: str = "",
    text_style: Style | None = None,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    show: bool = True,
) -> CycleItem

center = cycle.set_center(
    text: str,
    *,
    style: Style | None = None,
    description: str = "",
    radius: float | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> CycleCenter

cycle.draw(
    xy: tuple[float, float],
    radius: float = 35.0,
    align: Literal["center", "bottom_left"] = "center",
    scale: float = 1.0,
) -> Self
```

- `arrow_color_mode`:
  - `"match_source"` *(default)*: Arrow color automatically matches the preceding node's fill/line color.
  - `"match_target"`: Arrow color automatically matches the succeeding node's fill/line color.
  - `"monochrome"`: Uses `arrow_style` (requires `arrow_style` on `Cycle` or per item when `arrow_type != "none"`).
- `description_placement`: `"inside"` (renders `description` below `text` inside the node body) or `"outside"` (radiates `description` outward beyond the orbit).
- **Layout Tip**: For 5-node pentagonal `Cycle` diagrams with `node_shape="rectangle"`, keep `node_width <= 0.9 * radius` so the bottom two nodes maintain a clean horizontal gap for their connecting arrow.

---

## 3. Production Example: SRE Incident Response Lifecycle

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.smartarts import Cycle
from drawlib.styles import Styles

setup(width=100, height=90)

incident_cycle = Cycle(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.5),
    description_style=Styles.Muted.patch(text_size=9.5),
    arrow_style=Styles.DarkBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=9.0,
    arrow_type="arc",
    arrow_width=1.5,
    arrow_head_width=4.0,
    arrow_color_mode="monochrome",
    description_placement="inside",
)
incident_cycle.add(
    "1. Detect",
    description="Alert",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=9.5),
)
incident_cycle.add("2. Triage", description="Scope", style=Styles.PrimaryNeutral)
incident_cycle.add("3. Mitigate", description="Failover", style=Styles.SecondaryNeutral)
incident_cycle.add("4. Resolve", description="Root Fix", style=Styles.Neutral)
incident_cycle.add("5. Learn", description="Postmortem", style=Styles.Neutral)

incident_cycle.set_center(
    text="SRE",
    description="Command",
    radius=11.5,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.0),
    description_style=Styles.White.patch(text_color=CssColors.LightGray, text_size=9.5),
)
incident_cycle.draw(xy=(50, 45), radius=32.0, align="center")
save()
```
