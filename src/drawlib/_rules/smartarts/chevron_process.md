# Drawlib ChevronProcess SmartArt Guidelines (`lib-smartarts-chevron-process`)

`ChevronProcess` draws horizontal, sequential process pipelines consisting of interlocking arrowhead blocks (chevrons). It is the primary SmartArt component for CI/CD pipelines, ETL workflows, fulfillment lifecycles, and phased migrations.

---

## 1. Geometry & Anchor Mechanics

- **Anchor (`align`)**: Bottom-Left coordinate `xy=(x, y)` by default (`align="bottom_left"`), or `"center"` of the overall process bounding box.
- **Angle Calculation**: Arrowhead indentation is governed by `corner_angle` (degrees between `10.0` and `80.0`, default `60.0`):
  $$x_{\text{indent}} = \frac{\text{height} / 2}{\tan(\text{corner\_angle})}$$
- **First Chevron (`flat_left_end`)**: Setting `flat_left_end=True` replaces the first chevron's left indent with a clean vertical edge (a flat-backed pentagon).
- **Text Alignment**: Supports primary titles (`text`) and optional secondary supporting descriptions (`description`) centered cleanly within each chevron body.

---

## 2. Constructor, `ChevronItem` & Methods

```python
from drawlib.smartarts import ChevronItem, ChevronProcess

pipeline = ChevronProcess(
    *,
    style: Style,
    text_style: Style,
    description_style: Style,
    corner_angle: float = 60.0,
    spacing: float = 1.5,
    flat_left_end: bool = False,
)
```

### Item Model (`ChevronItem`) & `.items` Property

- `pipeline.items -> list[ChevronItem]`: Returns the list of registered `ChevronItem` instances.
- `ChevronItem` attributes (mutable before or between `draw()` calls):
  - `text: str`
  - `description: str = ""`
  - `style: Style`
  - `text_style: Style`
  - `description_style: Style`
  - `show: bool = True`

### Step Management & Drawing

```python
item = pipeline.add(
    text: str,
    *,
    description: str = "",
    style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    show: bool = True,
) -> ChevronItem

pipeline.draw(
    xy: tuple[float, float],
    width: float = 90.0,
    height: float = 12.0,
    item_width: float | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

- `add(...) -> ChevronItem`: Appends an individual step with optional style overrides and returns the public `ChevronItem` instance. Setting `item.show = False` skips drawing that step while keeping all remaining chevrons at their exact horizontal positions and widths.
- `draw(...) -> Self`:
  - `width`: Total bounding width allocated when `item_width is None`; individual block widths are computed automatically:
    $$\text{item\_width} = \frac{\text{width} - (\text{num\_items} - 1) \cdot \text{spacing} - x_{\text{indent}}}{\text{num\_items}}$$
  - `item_width`: If provided, overrides automatic width distribution (`total_width = num_items * item_width + (num_items - 1) * spacing + x_indent`).
  - `align`: `"bottom_left"` (default) or `"center"`.
  - `scale`: Proportional scale factor around `xy` (`1.0` by default).
  - Returns `Self` for method chaining.

---

## 3. Production Example: Cloud CI/CD Deployment Pipeline

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=130, height=45)

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
pipeline.add("1. Commit", description="Lint / Hooks")
pipeline.add("2. Build", description="Docker Image")
# Active Stage Highlight (returns ChevronItem)
active_stage = pipeline.add(
    text="3. Security",
    description="SAST & CVE",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
    description_style=Styles.White.patch(text_size=9.5),
)
pipeline.add("4. Staging", description="Integration")
pipeline.add("5. Production", description="Canary Deploy", style=Styles.SecondaryNeutral)
pipeline.draw(xy=(10, 15), width=110.0, height=16.0)
save()
```
