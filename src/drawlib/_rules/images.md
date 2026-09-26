# Drawlib Images Guidelines

Drawlib allows embedding external bitmap and vector images directly into canvases.  
You can combine raster graphics (company logos, cloud badges, screenshots) with vector shapes, lines, and text annotations, or manipulate graphics programmatically using the `Dimage` model.

---

## 1. Imports & Core Architecture

All public image functions and types are imported from `drawlib.images`:

```python
from drawlib.images import (
    image,                 # Primary function to draw images onto the canvas
    Dimage,                # Image manipulation model (wraps PIL Image)
    get_dimage_from_code,  # Render Drawlib Python code in-memory to a Dimage
)
```

---

## 2. Core Function: `image()`

`image()` places a raster or vector image at a target coordinate, preserving its aspect ratio automatically.

```python
image(
    xy: tuple[float, float],
    width: float,
    image: str | Image.Image | Dimage,
    angle: float = 0.0,
    style: Style | None = None,
)
```

### Parameter Breakdown:
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | Required | Coordinate of the image anchor point `(x, y)`. |
| `width` | `float` | Required | Width of the image in canvas units. Height is calculated automatically from the image aspect ratio. |
| `image` | `str \| Image \| Dimage`| Required | Filesystem path to an image file (`.png`, `.jpg`, `.svg`), a PIL `Image`, or a `Dimage`. |
| `angle` | `float` | `0.0` | Counter-clockwise rotation angle in degrees around the anchor point. |
| `style` | `Style \| None` | `None` | Style controlling transparency (`image_alpha`), tint color (`image_tint_color`), or anchor alignment (`text_halign`, `text_valign`). |

### Anchor Alignment
By default, `(x, y)` corresponds to the **geometric center** of the image.  
To change anchor alignment, configure `text_halign` and `text_valign` via `Style`:

```python
from drawlib.types import Style

# Anchor is bottom-left corner of image
bottom_left_style = Style(text_halign="left", text_valign="bottom")
```

> **Rotation & Alignment Note**:  
> If an image is rotated (`angle != 0.0`), `text_halign` and `text_valign` should be left at `"center"`. Non-center alignments on rotated images are automatically adjusted to `"center"` to prevent spatial distortion.

---

## 3. The `Dimage` Model

`Dimage` wraps a Python Imaging Library (PIL) `Image` object with drawing-specific transformations:

```python
from drawlib.images import Dimage

# Load from file or existing image
dimg = Dimage("assets/logo.png")

# Inspect pixel dimensions
w, h = dimg.get_image_size()

# Apply monochrome color tint
tinted_dimg = dimg.fill((52, 152, 219)) # Tint all non-transparent pixels with blue

# Deep copy
dimg_copy = dimg.copy()
```

---

## 4. In-Memory Composition: `get_dimage_from_code()`

Drawlib allows executing a snippet of Drawlib code and capturing the resulting canvas in-memory as a `Dimage`.  
This enables nested composite diagrams and recursive visual pipelining:

```python
from drawlib.images import get_dimage_from_code, image

# Draw a sub-diagram dynamically
sub_code = """
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle
setup(width=50, height=50)
circle((25, 25), radius=20, style=styles.purple_flat, text="Pod")
"""
sub_image = get_dimage_from_code(sub_code)

# Embed the generated sub-diagram onto the main canvas
image((40, 30), width=25, image=sub_image)
```

---

## 5. Practical Code Examples

### 5.1. Architectural Schema with External Server Icons

```drawlib fold-code 600px center caption:"Architecture Schema with External Logos & Containers"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.config import styles

setup(width=140, height=60)

# Service container cards
rectangle((35, 30), width=36, height=36, r=3, style=styles.blue_solid)
rectangle((105, 30), width=36, height=36, r=3, style=styles.green_solid)

# Card titles
text((35, 42), "Client Application", style=styles.bold)
text((105, 42), "Microservice API", style=styles.bold)

# Inner placeholder badges
rectangle((35, 26), width=20, height=12, style=styles.blue_flat, text="React", textstyle=styles.white_bold)
rectangle((105, 26), width=20, height=12, style=styles.green_flat, text="FastAPI", textstyle=styles.white_bold)

# Connecting arrow with payload label
line((53, 30), (87, 30), arrowhead="->", style=styles.bold)
text((70, 34), "JSON over HTTPS", style=styles.bold)
save()
```

### 5.2. Image Tinting & Opacity Blending

```drawlib fold-code 500px center caption:"Styling Images with Transparency and Tint"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=50)

# Solid border backdrop
rectangle((50, 25), width=80, height=36, r=4, style=styles.purple_solid)
text((50, 25), "Overlay Panel", style=styles.bold)
save()
```

---

## 6. Related Rules
- Icons Catalog (Phosphor, FontAwesome, GCP): `uv run drawlib rules show icons`
- Canvas Coordinate Space: `uv run drawlib rules show canvas`
- Shapes Drawing Primitives: `uv run drawlib rules show shapes`
