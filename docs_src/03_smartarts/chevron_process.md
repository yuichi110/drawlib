# ChevronProcess Component

The `ChevronProcess` component draws horizontal, sequential process pipelines consisting of interlocking arrowhead blocks (chevrons). 
It is the premier component for CI/CD delivery pipelines, phased development milestones, fulfillment lifecycles, and multi-step workflows.

---

## 1. Quick Example: CI/CD Pipeline

```drawlib 650px center caption:"Continuous Delivery Pipeline with ChevronProcess"
from drawlib.canvas import setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=130, height=45)

pipeline = ChevronProcess(
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
    default_textstyle=Styles.WhiteBold.patch(text_size=10),
    default_description_style=Styles.White.patch(text_size=7.5),
)
pipeline.append("1. Commit", description="Lint & Tests", style=Styles.PrimaryFlat)
pipeline.append("2. Build", description="Docker Image", style=Styles.PrimaryFlat)
pipeline.append("3. Security", description="Vulnerability Scan", style=Styles.AccentFlat)
pipeline.append("4. Staging", description="E2E Validation", style=Styles.PrimaryFlat)
pipeline.append("5. Production", description="Canary Release", style=Styles.SuccessFlat)

pipeline.draw(xy=(10, 15), width=110.0, height=16.0)
```

---

## 2. Geometry & Coordinate Anchor

- **Bottom-Left Anchor `(x, y)`**: The coordinate passed to `draw(xy=...)` represents the **bottom-left corner** of the entire process bounding box.
- **`flat_left_end`**: When set to `True`, the first chevron has a clean vertical left border instead of an indented notch, creating a polished start.
- **`corner_angle`**: Sets the sharpness of the chevron arrowhead tip (typically between `45.0` and `60.0` degrees).
- **`spacing`**: The horizontal gap between adjacent chevrons.

---

## 3. Class API Reference

### Constructor
```python
ChevronProcess(
    corner_angle: float = 60.0,
    spacing: float = 1.5,
    flat_left_end: bool = False,
    default_style: str | Style | None = None,
    default_textstyle: str | Style | None = None,
    default_description_style: str | Style | None = None,
    palette: Sequence[tuple[int, int, int]] | None = None,
)
```

### Adding Steps
- **`append(text, description="", style=None, textstyle=None, description_style=None)`**:  
  Adds a new process stage. If `style` is omitted, Drawlib assigns colors automatically from `palette`.
- **`extend(texts, descriptions=None)`**:  
  Appends multiple stage titles at once.
- **`insert(index, text, description="", ...)`**:  
  Inserts a stage at a specified index.

### Drawing
- **`draw(xy, width=90.0, height=12.0, item_width=None)`**:  
  Renders the pipeline onto the active canvas. If `item_width` is omitted, Drawlib divides `width` equally among all stages.
