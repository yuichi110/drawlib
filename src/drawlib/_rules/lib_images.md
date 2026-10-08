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
    *,
    style: Style | None = None,
)
```

### Parameter Breakdown:
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | Required | Coordinate of the image center anchor point `(x, y)`. |
| `width` | `float` | Required | Width of the image in canvas units. Height is calculated automatically from the image aspect ratio. |
| `image` | `str \| Image \| Dimage`| Required | Filesystem path to an image file (`.png`, `.jpg`, `.webp`), a PIL `Image`, or a `Dimage`. |
| `angle` | `float` | `0.0` | Counter-clockwise rotation angle in degrees around the anchor point. |
| `style` | `Style \| None` | `None` | Style controlling transparency (`alpha`), tint color (`image_tint_color`), or border (`image_border_width`, `image_border_color`). |

### Anchor Alignment
By default, `(x, y)` corresponds to the **geometric center** of the image in canvas coordinates.

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
from drawlib.styles import Styles
from drawlib.shapes import circle
setup(width=50, height=50)
circle((25, 25), radius=20, style=Styles.PrimaryFlat, text="Pod")
"""
sub_image = get_dimage_from_code(sub_code)

# Embed the generated sub-diagram onto the main canvas
image((40, 30), width=25, image=sub_image)
```

---

## 5. Practical Code Examples

### 5.1. Architectural Schema with In-Memory Embedded Diagrams

```drawlib fold-code 600px center caption:"Architecture Schema with Embedded Diagram Images"
from drawlib.canvas import save, setup
from drawlib.images import get_dimage_from_code, image
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.styles import Styles

setup(width=140, height=60)

# Generate sub-diagram components dynamically
frontend_code = """
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles
setup(width=40, height=40)
circle((20, 20), radius=16, style=Styles.SecondaryNeutral, text="UI")
"""
api_code = """
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles
setup(width=40, height=40)
circle((20, 20), radius=16, style=Styles.PrimaryFlat, text="API", text_style=Styles.WhiteBold)
"""

img_frontend = get_dimage_from_code(frontend_code)
img_api = get_dimage_from_code(api_code)

# Service container cards
rectangle((35, 30), width=36, height=36, r=3, style=Styles.MutedDashed)
rectangle((105, 30), width=36, height=36, r=3, style=Styles.MutedDashed)

# Embed sub-diagram images
image((35, 30), width=22, image=img_frontend)
image((105, 30), width=22, image=img_api)

# Card titles
text((35, 52), "Client Application", style=Styles.DarkBold)
text((105, 52), "Microservice API", style=Styles.DarkBold)

# Connecting arrow with payload label
line((53, 30), (87, 30), arrow_head="->", style=Styles.DarkBold)
text((70, 35), "JSON / HTTPS", style=Styles.Muted)
save()
```

### 5.2. Image Tinting & Opacity Blending

```drawlib fold-code 500px center caption:"Styling Images with Transparency and Tint"
from drawlib.canvas import save, setup
from drawlib.images import get_dimage_from_code, image
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=50)

# Generate a base icon image
badge_code = """
from drawlib.canvas import setup
from drawlib.shapes import star
from drawlib.styles import Styles
setup(width=30, height=30)
star((15, 15), num_vertex=5, radius_ext=12, radius_int=6, style=Styles.PrimaryFlat)
"""
badge_img = get_dimage_from_code(badge_code)

# Solid border backdrop
rectangle((50, 25), width=80, height=36, r=4, style=Styles.MutedDashed)

# Place image with alpha transparency
image_style = Styles.Primary.patch(alpha=0.6)
image((50, 25), width=20, image=badge_img, style=image_style)
text((50, 12), "Watermarked Badge", style=Styles.DarkBold)
save()
```

---

## 6. Related Rules
- Icons Catalog (Phosphor, FontAwesome, GCP): `uv run drawlib rules show lib-icons`
- Canvas Coordinate Space: `uv run drawlib rules show lib-canvas`
- Shapes Drawing Primitives: `uv run drawlib rules show lib-shapes`
