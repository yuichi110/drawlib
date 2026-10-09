# Canvas & Coordinates

The `canvas` is the foundational drawing surface of Drawlib.  
Under the "Illustration as Code" paradigm, canvas dimensions, resolution, background coloring, coordinate grids, and export formats are managed entirely through declarative Python function calls.

---

## 1. Imports & Core Lifecycle

Canvas lifecycle functions and the singleton `canvas` instance are imported from `drawlib.canvas`:

```python
from drawlib.canvas import (
    canvas,       # Active singleton Canvas instance (provides canvas.transform())
    clear,        # Reset canvas state and configuration between drawings
    get_dimage,   # Render canvas in-memory and return a Dimage object
    save,         # Save drawing to disk (PNG, WebP, JPG, SVG, PDF)
    setup,        # Configure dimensions, grid, background color, and DPI
    show,         # Display canvas in an interactive GUI window
)
```

### The Canvas Lifecycle Model

Drawlib maintains an active canvas singleton. Drawing functions (`rectangle()`, `line()`, `text()`, etc.) register visual elements to this active canvas before it is saved or rendered:



<figure class="drawlib-image" style="text-align: center;">
  <img src="canvas_images/canvas_lifecycle_model.png" alt="canvas_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">The Drawlib Canvas Lifecycle Model</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.lines import line, lines_curved
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=130, height=48)

# 3-Step Lifecycle Cards (50%+ Neutral baseline with PrimaryFlat hero on Step 2)
rectangle(
    (24, 31),
    width=32,
    height=18,
    style=Styles.Neutral.patch(shape_r=2),
    text="1. Configure Canvas\nsetup(width, height)\nSet size, grid, bg",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)
rectangle(
    (65, 31),
    width=34,
    height=18,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="2. Draw Elements\nshapes, lines, text,\nsmartarts, diagrams",
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)
rectangle(
    (106, 31),
    width=32,
    height=18,
    style=Styles.Neutral.patch(shape_r=2),
    text="3. Output Result\nsave() / show()\nExport to file or view",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

# Forward transitions
line((40, 31), (48, 31), arrow_head="->", style=Styles.DarkBold)
line((82, 31), (90, 31), arrow_head="->", style=Styles.DarkBold)

# Return loop from Step 3 back to Step 1
lines_curved(
    [(106, 22), (106, 12), (24, 12), (24, 22)],
    r=3.5,
    arrow_head="->",
    style=Styles.MutedDashed.patch(line_width=1.8),
)
text((65, 6.5), "clear() — Reset canvas state for next image", style=Styles.DarkBold.patch(text_size=8.5))
save()
```

</details>



> [!IMPORTANT]
> **Sequential Scripts & Multi-Image Generation**:  
> If you generate multiple illustrations in a single Python script, always call `clear()` between images. Otherwise, elements from earlier drawings will bleed onto subsequent canvases.

---

## 2. Cartesian Coordinate Space

Drawlib uses a mathematical Cartesian coordinate system:

- **Origin `(0, 0)`**: Fixed at the **bottom-left corner** of the canvas.
- **X-Axis**: Increases horizontally to the right (`0` to `width`).
- **Y-Axis**: Increases vertically upwards (`0` to `height`).
- **Center-Based Anchoring**: Coordinates `(x, y)` for shapes, text, and icons refer to their **exact geometric center** by default.



```python
from drawlib.canvas import save, setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles

# Custom background color (Muted tone 1) and coordinate grid
setup(width=100, height=50, background_color=Colors.Muted1, grid=True)

rectangle((50, 25), width=60, height=25, style=Styles.PrimaryFlat, text="Custom Canvas Setup", text_style=Styles.WhiteBold)
circle((20, 25), radius=8, style=Styles.Neutral)
circle((80, 25), radius=8, style=Styles.SecondaryNeutral)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="canvas_images/canvas_configuration_grid.png" alt="canvas_2" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Custom Canvas Configuration with Grid</figcaption>
</figure>



---

## 3. Function & Method Reference

### 3.1. `setup()`
Configures canvas geometry, resolution, coordinate grids, and background appearance. Must be called before drawing elements.

```python
setup(
    width: int | None = None,
    height: int | None = None,
    dpi: int | None = None,
    color: Color | tuple[int, int, int] | tuple[int, int, int, float] | str | None = None,
    alpha: float | None = None,
    background_color: Color | tuple[int, int, int] | tuple[int, int, int, float] | str | None = None,
    background_alpha: float | None = None,
    grid: bool | None = None,
    grid_only: bool | None = None,
    grid_style: Style | None = None,
    grid_centerstyle: Style | None = None,
    grid_xpitch: int | None = None,
    grid_ypitch: int | None = None,
)
```

#### Parameter Reference:
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `int` | `100` | Canvas width in virtual coordinate units (`> 0`). |
| `height` | `int` | `100` | Canvas height in virtual coordinate units (`> 0`). |
| `dpi` | `int` | `100` | Dots per inch (resolution and raster sharpness). |
| `background_color` / `color` | `Color \| tuple \| str` | `(255, 255, 255)` | Canvas background color as a `Color` instance, RGB/RGBA tuple, hex string (`"#f8fafc"`), or CSS color name (`color` is a shorthand alias for `background_color`). |
| `background_alpha` / `alpha` | `float` | `1.0` | Background opacity in `[0.0, 1.0]` (`0.0` = fully transparent, `1.0` = opaque; `alpha` is a shorthand alias for `background_alpha`). |
| `grid` | `bool` | `False` | Overlays coordinate grid lines for layout alignment. |
| `grid_only` | `bool` | `False` | Renders the coordinate grid overlay without saving a separate non-grid image. |
| `grid_style` | `Style` | Gray dashed | Custom line style for regular grid lines (automatically enables `grid=True`). |
| `grid_centerstyle`| `Style` | Bold gray dashed | Custom line style for center axes (`x = width / 2`, `y = height / 2`). |
| `grid_xpitch` | `int` | `width / 10` | Spacing between vertical grid lines. |
| `grid_ypitch` | `int` | `height / 10` | Spacing between horizontal grid lines. |

---

### 3.2. `save()`
Exports the active canvas to an image file on disk.

```python
save(
    file: str | None = None,
    format: Literal["png", "webp", "jpg", "pdf", "svg"] | None = None,
)
```

- **`file`**: Target file path. If omitted, defaults to `<script_name>.png` in the directory of the running script.
- **`format`**: Output image format (`"png"`, `"webp"`, `"jpg"`/`"jpeg"`, `"svg"`, `"pdf"`). If omitted, inferred from the filename extension or defaults to `"png"`.
- **Grid Export Behavior (`setup(..., grid=True)`)**:
  - When `grid=True` and `grid_only=False` (default), calling `save("out.png")` writes **two files**: the clean illustration (`out.png`) and a companion grid-overlaid image (`out_grid.png`).
  - When `grid_only=True`, calling `save("out.png")` writes **only a single file** (`out.png`) with the coordinate grid overlaid directly on the drawing.

> [!NOTE]
> **Handling `save()` in Markdown Blocks**:
> In Markdown embedded code blocks (` ```drawlib `), calling `save()` is optional because the Document Builder captures the canvas automatically. If `save()` is called within an embedded block, the engine treats it safely as a no-op to prevent duplicate writes or collisions. However, explicitly including `save()` (without arguments) in complete examples is recommended for 100% copy-paste compatibility with standalone `.py` scripts.

---

### 3.3. `show()`
Opens a local interactive desktop window displaying the illustration. In headless environments (CI/CD, Docker, remote servers), use `save()` or CLI `drawlib show -o <path>` instead.

### 3.4. `clear()`
Resets canvas geometry, clears registered artists, and restores default styles and configuration parameters.

### 3.5. `get_dimage()`
Renders the canvas in-memory and returns a `Dimage` object, allowing programmatic image transformations, cropping, and chaining without writing temporary files to disk.

---

### 3.6. Local Coordinate Scaling & Translation (`canvas.transform()`)

The `canvas.transform()` context manager applies a similarity transformation (proportional scaling around an anchor `origin` plus an `(dx, dy)` translation offset) to all shapes, lines, icons, and text drawn within its `with` block. Transforms can also be nested.

```python
with canvas.transform(
    origin: tuple[float, float] = (0.0, 0.0),
    scale: float = 1.0,
    translate: tuple[float, float] = (0.0, 0.0),
):
    ...
```

- **`origin`**: Anchor coordinate `(ox, oy)` around which scaling is performed (defaults to `(0.0, 0.0)`).
- **`scale`**: Positive proportional scale factor (`> 0`, defaults to `1.0`). Scales geometry, stroke widths, arrowheads, and font sizes together.
- **`translate`**: Additional `(dx, dy)` translation offset applied in canvas units (defaults to `(0.0, 0.0)`).



```python
from drawlib.canvas import canvas, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=125, height=48, grid=True, grid_xpitch=25, grid_ypitch=12)

def draw_service_pod(title: str, is_hero: bool = False) -> None:
    """Reusable pod component authored in local coordinates around (28, 21)."""
    card_style = Styles.PrimaryFlat if is_hero else Styles.Neutral
    label_style = Styles.WhiteBold if is_hero else Styles.DarkBold
    rectangle((28, 21), width=36, height=24, style=Styles.MutedDashed.patch(shape_r=3))
    rectangle((28, 25), width=28, height=10, style=card_style.patch(shape_r=2), text=title, text_style=label_style)
    circle((20, 13), radius=3.5, style=Styles.SecondaryNeutral, text="1")
    circle((36, 13), radius=3.5, style=Styles.SecondaryNeutral, text="2")
    line((23.5, 13), (32.5, 13), arrow_head="<->", style=Styles.DarkBold)

# 1. Original 1.0x pod at (28, 21)
draw_service_pod("Primary Pod (1.0x)", is_hero=True)

# 2. Scaled (0.78x) and translated (+44, 0) replica pod
with canvas.transform(origin=(28, 21), scale=0.78, translate=(44, 0)):
    draw_service_pod("Replica (0.78x)")

# 3. Scaled (0.58x) and translated (+80, 0) standby pod
with canvas.transform(origin=(28, 21), scale=0.58, translate=(80, 0)):
    draw_service_pod("Standby (0.58x)")

text((90, 38), "Scaled & Translated via canvas.transform()", style=Styles.DarkBold.patch(text_size=9.5))
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="canvas_images/canvas_transform_context.png" alt="canvas_3" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Local Coordinate Scaling and Translation with canvas.transform()</figcaption>
</figure>



