# 3. Canvas & Coordinate System

Every Drawlib illustration is rendered on a virtual **Canvas**. Understanding Drawlib's coordinate space is the foundation of creating clear, balanced diagrams.

## Cartesian Coordinate Space

Unlike traditional web or GUI coordinate systems where `(0, 0)` sits at the top-left with a descending Y-axis, Drawlib uses the standard mathematical **Cartesian Coordinate System**:

- **Origin `(0, 0)`**: Located at the **Bottom-Left** corner of the canvas.
- **X-Axis**: Increases from left to right (`0` to `width`).
- **Y-Axis**: Increases from bottom to top (`0` to `height`).

```drawlib 620px center caption:"Figure 3.1: Cartesian Coordinate System & Canvas Anchors"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=55)

# Outer canvas boundary
rectangle(xy=(60, 27.5), width=108, height=45, r=2, style=Styles.muted_dashed)

# Coordinate axes
line((12, 10), (110, 10), arrowhead="->", style=Styles.primary_bold)
text((112, 10), "X", style=Styles.primary_bold, size=11)

line((16, 6), (16, 48), arrowhead="->", style=Styles.primary_bold)
text((16, 50), "Y", style=Styles.primary_bold, size=11)

# Origin marker
circle((16, 10), radius=1.5, style=Styles.accent_flat)
text((13, 6), "(0, 0)", style=Styles.accent_bold, size=9)

# Center anchor element
circle((60, 28), radius=8, style=Styles.primary_flat)
text((60, 28), "Center\n(60, 28)", style=Styles.white_bold, size=9)

# Corner coordinate labels
text((18, 45), "Top-Left (0, H)", style=Styles.muted_bold, size=8)
text((105, 45), "Top-Right (W, H)", style=Styles.muted_bold, size=8)
text((105, 14), "Bottom-Right (W, 0)", style=Styles.muted_bold, size=8)
```

## Configuring the Canvas with `setup()`

Call `setup()` at the beginning of a drawing script or Markdown block to define canvas dimensions:

```python
from drawlib.canvas import setup

# 120 x 60 coordinate units, high-resolution 150 DPI, visual coordinate grid enabled
setup(width=120, height=60, dpi=150, grid=True)
```

- **`width` / `height`**: Logical coordinate space (defaults to `100.0` x `100.0`). Choosing an aspect ratio tailored to your content (e.g. `120 x 60` for horizontal architectures) prevents letterboxing.
- **`dpi`**: Dots per inch (default `100`). At `100` DPI, a canvas of `100` units renders at `1000px` width.
- **`grid=True`**: Overlays grid lines every 10 units and coordinate numbers every 20 units. Extremely useful during rapid development to inspect exact alignment.

## Alignment & Text Anchors (`text_halign` and `text_valign`)

Text labels support horizontal (`text_halign`) and vertical (`text_valign`) alignment configured via style attributes or `.patch()`:

- **Horizontal Alignment (`text_halign`)**: `"left"`, `"center"`, `"right"`.
- **Vertical Alignment (`text_valign`)**: `"bottom"`, `"center"`, `"top"`.

```drawlib 620px center caption:"Figure 3.2: Text Alignment Anchors with text_halign"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

anchors = [
    (24, "left", "Left Aligned\n(starts at X)", Styles.primary),
    (60, "center", "Center Aligned\n(centered at X)", Styles.secondary),
    (96, "right", "Right Aligned\n(ends at X)", Styles.accent),
]

for x, align_mode, label, st in anchors:
    # Reference vertical alignment line
    line((x, 10), (x, 38), style=Styles.muted_dashed)
    # Red anchor dot
    circle((x, 24), radius=1.5, style=Styles.danger_flat)
    text((x, 24), label, style=Styles.bold.patch(text_halign=align_mode), size=8.5)
    text((x, 6), f"text_halign='{align_mode}'", style=st, size=8.5)
```
