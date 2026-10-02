# Cycle Component

The `Cycle` component draws circular, repeating process diagrams and continuous feedback loops. 
It is ideally suited for Agile/Scrum iterations, PDCA DevOps lifecycles, incident response loops, and token refresh mechanisms.

---

## 1. Quick Example: Agile Development Cycle

```drawlib 600px center caption:"Continuous Agile Lifecycle with Cycle"
from drawlib.canvas import setup
from drawlib.smartarts import Cycle
from drawlib.styles import Styles

setup(width=100, height=90)

cycle = Cycle(
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=7.5,
    arrow_type="arc",
    arrow_width=1.5,
    arrow_head_width=4.0,
    arrow_color_mode="match_source",
    default_textstyle=Styles.WhiteBold.patch(text_size=9),
    default_description_style=Styles.White.patch(text_size=7),
    default_arrow_style=Styles.PrimarySolid,
    description_placement="inside",
)
cycle.append("1. Plan", description="Sprint Goal", style=Styles.PrimaryFlat)
cycle.append("2. Do", description="Build Feature", style=Styles.AccentFlat)
cycle.append("3. Check", description="Code Review", style=Styles.SecondaryFlat)
cycle.append("4. Act", description="Retro & Deploy", style=Styles.SuccessFlat)

cycle.set_center(
    text="Agile",
    description="Loop",
    radius=10.0,
    style=Styles.MutedFlat,
    textstyle=Styles.PrimaryBold.patch(text_size=10),
)

cycle.draw(xy=(50, 45), radius=28.0)
```

---

## 2. Geometry & Coordinate Mechanics

- **Center Anchor `(cx, cy)`**: The coordinate passed to `draw(xy=(cx, cy), radius=R)` specifies the **center hub of the orbit circle**.
- **Equi-Angular Distribution**: Steps are automatically spaced evenly along the orbit circumference:
  $$\theta_i = \text{start\_angle} \mp \left(i \cdot \frac{360^\circ}{N}\right)$$
- **Circular Arc Connectors**: Steps are connected by curved block arrows (`arrow_type="arc"`), direct lines (`"line"`), or no connectors (`"none"`).
- **Arrow Color Mode**:
  - `"match_source"` *(default)*: Each connector arrow adopts the theme color of its originating step.
  - `"match_target"`: Connectors match the destination step color.
  - `"monochrome"`: Connectors use a uniform line style (`default_arrow_style`).

---

## 3. Class API Reference

### Constructor
```python
Cycle(
    clockwise: bool = True,
    start_angle: float = 90.0,
    node_shape: Literal["circle", "rectangle", "none"] = "circle",
    node_radius: float = 8.0,
    node_size: tuple[float, float] = (18.0, 10.0),
    description_placement: Literal["inside", "outside"] = "inside",
    arrow_type: Literal["arc", "line", "none"] = "arc",
    arrow_width: float = 2.0,
    arrow_head_width: float = 4.5,
    arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
    arrow_gap: float = 2.5,
    default_textstyle: Style | None = None,
    default_description_style: Style | None = None,
    default_arrow_style: Style | None = None,
    center_text: str = "",
    center_description: str = "",
    center_radius: float = 10.0,
    center_style: Style | None = None,
    center_textstyle: Style | None = None,
    center_description_style: Style | None = None,
)
```

### Adding Steps and Center Hub
- **`append(text, style, description="", textstyle=None, description_style=None, arrow_style=None)`**:  
  Appends a step with its mandatory `style` to the circular perimeter.
- **`extend(texts, styles, descriptions=None)`**:  
  Appends multiple steps with a single shared `Style` or a list of `Style` objects matching `texts`.
- **`set_center(text, style=None, description="", radius=None, textstyle=None, description_style=None)`**:  
  Adds an optional central focal node to create a radial cycle.

### Drawing
- **`draw(xy, radius=28.0)`**:  
  Renders the circular cycle centered at `xy` with orbit radius `radius`.
