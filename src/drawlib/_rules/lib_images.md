# Drawlib Images Guidelines

Drawlib allows embedding external raster (bitmap) images directly into canvases.  
You can combine raster graphics (company logos, cloud badges, screenshots in PNG, JPEG, WebP, etc.) with vector shapes, lines, and text annotations, or manipulate raster graphics programmatically using the `Dimage` model (which wraps `PIL.Image.Image`).

---

## 1. Imports & Core Architecture

All public image functions and types are imported from `drawlib.images`:

```python
from drawlib.images import (
    image,  # Primary function to draw raster images onto the canvas
    Dimage,  # Image manipulation model (wraps PIL.Image.Image)
    get_dimage_from_code,  # Render Drawlib Python code in-memory to a Dimage
)
```

---

## 2. Core Function: `image()`

`image()` places a raster image at a target coordinate, preserving its aspect ratio automatically.

```python
image(
    xy: tuple[float, float],
    width: float,
    image: str | Image.Image | Dimage,
    *,
    style: Style | None = None,
) -> None
```

### Parameter Breakdown:
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | Required | Coordinate of the image anchor point `(x, y)`. |
| `width` | `float` | Required | Width of the image in canvas units. Height is calculated automatically from the image aspect ratio. |
| `image` | `str \| Image.Image \| Dimage`| Required | Filesystem path to a raster image file (`.png`, `.jpg`, `.jpeg`, `.webp`, etc.), a PIL `Image.Image`, or a `Dimage`. |
| `style` | `Style \| None` | `None` | Style controlling rotation (`angle`), alignment (`halign`, `valign`), offset (`xy_shift`, `xy_abs_shift`), transparency (`alpha`), background fill (`image_tint_color`), or border (`image_border_width`, `image_border_color`, `image_border_style`). |

### Anchor Alignment
By default (`halign="center"`, `valign="center"`), `(x, y)` corresponds to the **geometric center** of the image in canvas coordinates.

### Image Styling via `Style`
Unlike geometric shapes (which use `shape_line_*` and `shape_fill_color`), `image()` uses dedicated `image_*` attributes on `Style`:
- **`image_border_width`** (`float | None`): Border stroke width around the image frame (`0` or `None` disables the border).
- **`image_border_color`** (`ColorType | None`): Border stroke color.
- **`image_border_style`** (`LineStyle | None`): Border stroke pattern (`"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`).
- **`image_tint_color`** (`ColorType | None`): Calls `Dimage.fill(image_tint_color)` to fill transparent background pixels (`alpha == 0`) with the specified color.

### Asset Paths & Portability (Relative Paths Only)
When referencing image files in `image(..., image="...")` or `Dimage("...")`:
- **Always use relative paths** (e.g. `_assets/logo.png` or `../_assets/icon.png`). Relative paths are resolved relative to the caller Python script directory.
- In Drawlib projects (`site`, `doc`, `slide`, `images`), static assets are placed under `_assets/` within the source directory and copied to the build output.
- **Never use machine-specific absolute paths** (`/usr/...`, `/home/...`, `/Users/...`, `C:\...`) or `file://` URLs. Absolute paths break portability across environments, CI/CD runners, and team collaboration.

---

## 3. The `Dimage` Model

`Dimage` wraps a Python Imaging Library (`PIL.Image.Image`) object with non-destructive, immutable drawing transformations (every transformation method returns a new `Dimage` while leaving the original unchanged):

### 3.1. Constructor & Core Inspection / IO Methods

```python
Dimage(
    image: str | os.PathLike | Dimage | Image.Image,
    copy: bool = False,
)
```

| Method | Signature | Return Type | Description |
| :--- | :--- | :--- | :--- |
| **`__init__`** | `Dimage(image, copy=False)` | `Dimage` | Initialize from a raster file path, `PIL.Image.Image`, or existing `Dimage`. |
| **`get_image_size`** | `get_image_size()` | `tuple[int, int]` | Return pixel dimensions `(width, height)`. |
| **`get_pil_image`** | `get_pil_image()` | `Image.Image` | Return a defensive copy of the underlying `PIL.Image.Image`. |
| **`copy`** | `copy()` | `Dimage` | Return a copied `Dimage` instance. |
| **`save`** | `save(file, quality=95)` | `None` | Save the image to `file` (creating parent directories if needed) with `quality` (`0`–`100`). |

### 3.2. Geometry, Color & Filter Transformation Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| **`resize`** | `resize(width, height, resample="lanczos")` | Resize to `(width, height)` in pixels (`resample`: `"nearest"`, `"box"`, `"bilinear"`, `"hamming"`, `"bicubic"`, `"lanczos"`). |
| **`crop`** | `crop(x, y, width, height)` | Crop a rectangular region of `(width, height)` pixels where **`(0, 0)` is the bottom-left corner** of the image. |
| **`flip`** | `flip()` | Flip the image vertically (top-to-bottom). |
| **`mirror`** | `mirror()` | Mirror the image horizontally (left-to-right). |
| **`fill`** | `fill(color)` | Fill transparent background pixels (`alpha == 0`) with `color` (blending semi-transparent pixels) while leaving opaque pixels unchanged. |
| **`alpha`** | `alpha(alpha)` | Cap pixel opacity at `alpha` (`0.0` to `1.0`), preserving pixels that are already more transparent. |
| **`invert`** | `invert()` | Invert RGB channels while preserving the original alpha channel. |
| **`grayscale`** | `grayscale()` | Convert the image to grayscale (`LA` mode, preserving alpha). |
| **`brightness`** | `brightness(brightness=0.5)` | Scale image brightness (`1.0` = original, `< 1.0` = darker, `> 1.0` = brighter). |
| **`sepia`** | `sepia()` | Apply a warm sepia tone filter while preserving alpha. |
| **`colorize`** | `colorize(from_black_to, from_white_to, from_mid_to=None)` | Map grayscale luminance from black -> `from_black_to`, white -> `from_white_to` (and optional mid-tones -> `from_mid_to`), preserving alpha. Use this to recolor/tint monochrome icons or assets. |
| **`posterize`** | `posterize(num_colors=4)` | Reduce the number of bits/levels per color channel (`num_colors`), preserving alpha. |
| **`mosaic`** | `mosaic(block_size=8)` | Pixelate the image into average-colored square blocks of `block_size` pixels. |
| **`blur`** | `blur()` | Apply a Gaussian/box blur filter (`ImageFilter.BLUR`). |
| **`line_extraction`** | `line_extraction()` | Extract dark contour outlines on a white background from the image. |
| **`trim`** | `trim(color="auto", tolerance=0)` | Automatically crop surrounding solid or transparent margins (`"auto"` detects corner background color/transparency; `None` trims transparent margins). |
| **`make_transparent`**| `make_transparent(color="auto", tolerance=0)` | Convert a solid background color (`"auto"` detects from corners, or pass a specific `Color`/hex/tuple) into transparent RGBA pixels within `tolerance` (`0`–`255`). |

```python
from drawlib.images import Dimage
from drawlib.styles import Colors

# Load from file, strip white background, trim margins, and recolor
dimg = (
    Dimage("_assets/logo.png")
    .make_transparent(color="auto", tolerance=15)
    .trim(color=None)
    .colorize(from_black_to=Colors.Primary, from_white_to=Colors.White)
)

# Inspect pixel dimensions
w, h = dimg.get_image_size()

# Fill transparent background pixels with a soft neutral card color
filled_dimg = dimg.fill(Colors.Neutral)
```

---

## 4. In-Memory Composition: `get_dimage_from_code()`

Drawlib allows executing a snippet of Drawlib Python code in an isolated child process and capturing the resulting canvas in-memory as a `Dimage` (ignoring any `save()` calls inside the snippet).  
This enables nested composite diagrams and recursive visual pipelining without affecting the parent canvas state:

```python
get_dimage_from_code(
    code: str,
    timeout: float | None = None,
) -> Dimage
```

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
sub_image = get_dimage_from_code(sub_code, timeout=10.0)

# Embed the generated sub-diagram onto the main canvas
image((40, 30), width=25, image=sub_image)
```

---

## 5. Practical Code Examples

### 5.1. Architectural Schema with In-Memory Embedded Diagrams

```drawlib code=fold align=center caption="Architecture Schema with Embedded Diagram Images"
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
rectangle((35, 30), width=36, height=36, style=Styles.MutedDashed.patch(shape_r=3))
rectangle((105, 30), width=36, height=36, style=Styles.MutedDashed.patch(shape_r=3))

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

### 5.2. Image Borders, Background Fill & Opacity Blending

```drawlib code=fold align=center caption="Styling Images with Transparency, Border, and Background Fill"
from drawlib.canvas import save, setup
from drawlib.images import get_dimage_from_code, image
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.styles import Colors, Styles

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
rectangle((50, 25), width=80, height=36, style=Styles.MutedDashed.patch(shape_r=4))

# Place image with alpha transparency and image_border_* attributes
image_style = Styles.Primary.patch(
    alpha=0.85,
    image_border_width=1.5,
    image_border_color=Colors.Primary,
    image_border_style="solid",
)
image((50, 25), width=20, image=badge_img, style=image_style)
text((50, 10), "Framed & Styled Badge", style=Styles.DarkBold)
save()
```

---

## 6. Related Rules
- Icons Catalog (34 Icon Suites — Phosphor, GCP, AWS, Azure, Domain Suites): `uv run drawlib rules show lib-icons-overview`
- Canvas Coordinate Space: `uv run drawlib rules show lib-canvas`
- Shapes Drawing Primitives: `uv run drawlib rules show lib-shapes-overview`
