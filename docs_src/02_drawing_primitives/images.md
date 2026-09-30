# Images & Dimage

Drawlib allows embedding external bitmap and vector images directly into your illustrations.  
You can combine raster graphics (company logos, cloud service icons, application screenshots) with vector shapes and annotations, or manipulate graphics programmatically using the in-memory `Dimage` model.

---

## 1. Overview of Image Placement

```drawlib 650px center caption:"Embedding External Assets and In-Memory Dimages"
from drawlib.canvas import setup
from drawlib.images import image, Dimage
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.styles import Styles

setup(width=120, height=50)

# Card 1: Local image file
rectangle((35, 25), width=45, height=36, r=3, style=Styles.primary_dashed)
image((35, 28), width=18, image="../_assets/linux.png")
text((35, 12), "Linux Logo", style=Styles.bold)

# Card 2: Memory Dimage
rectangle((85, 25), width=45, height=36, r=3, style=Styles.secondary_dashed)
dimg = Dimage("../_assets/python.png")
image((85, 28), width=18, image=dimg)
text((85, 12), "Python Dimage", style=Styles.bold)
```

---

## 2. Placing Images (`image`)

The `image()` function places an image on the canvas at coordinate `xy`, automatically preserving its original aspect ratio.

```python
image(
    xy: tuple[float, float],
    width: float,
    image: str | Image.Image | Dimage,
    angle: float = 0.0,
    style: Style | None = None,
)
```

### Parameter Reference:
- **`xy`**: Center coordinate anchor point `(x, y)`.
- **`width`**: Width of the image in canvas units. The height scales proportionally.
- **`image`**: File path (`.png`, `.jpg`, `.svg`), PIL `Image` instance, or `Dimage` object.
- **`angle`**: Counter-clockwise rotation angle around `xy`.
- **`style`**: Optional styling controlling opacity (`image_alpha`) or alignment.

### Changing Anchor Alignment
By default, `(x, y)` anchors the center of the image. To position an image by its bottom-left corner:

```python
from drawlib.styles import Styles

bottom_left_style = Styles.bold.patch(text_halign="left", text_valign="bottom")
image((10, 10), width=25, image="logo.png", style=bottom_left_style)
```

---

## 3. In-Memory Image Manipulation (`Dimage`)

The `Dimage` class wraps a PIL Image object with Drawlib transformation utilities:

```python
from drawlib.images import Dimage

# 1. Load from file
dimg = Dimage("assets/screenshot.png")

# 2. Inspect dimensions
width, height = dimg.get_image_size()

# 3. Apply color tinting
# Replaces non-transparent pixels with an RGB tint
tinted_dimg = dimg.fill((52, 152, 219))

# 4. Clone instance
copy_dimg = dimg.copy()
```

---

## 4. Dynamic In-Memory Rendering (`get_dimage_from_code`)

Drawlib can execute a snippet of Drawlib drawing code dynamically and return the rendered result directly as an in-memory `Dimage`.  
This enables recursive nesting and reusable sub-diagram templates:

```python
from drawlib.images import get_dimage_from_code, image
from drawlib.canvas import setup

# Render a sub-component in-memory
sub_code = """
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles

setup(width=40, height=40)
circle((20, 20), radius=15, style=Styles.accent_flat, text="Pod")
"""

sub_diagram = get_dimage_from_code(sub_code)

# Embed the sub-diagram onto the primary canvas
setup(width=100, height=50)
image((50, 25), width=25, image=sub_diagram)
```
