# 3. Canvas & Coordinate System

Every Drawlib illustration is rendered on a virtual **Canvas**. Understanding Drawlib's coordinate space is the foundation of creating clear, balanced diagrams.

## Cartesian Coordinate Space

Unlike traditional web or GUI coordinate systems where `(0, 0)` sits at the top-left with a descending Y-axis, Drawlib uses the standard mathematical **Cartesian Coordinate System**:

- **Origin `(0, 0)`**: Located at the **Bottom-Left** corner of the canvas.
- **X-Axis**: Increases from left to right (`0` to `width`).
- **Y-Axis**: Increases from bottom to top (`0` to `height`).

```drawlib 620px center file:canvas_coordinates.png caption:"Figure 3.1: Cartesian Coordinate System & Canvas Anchors"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=55)

# Outer canvas boundary
rectangle(xy=(60, 27.5), width=108, height=45, style=Styles.MutedDashed.patch(shape_r=2))

# Coordinate axes
line((12, 10), (110, 10), arrow_head="->", style=Styles.DarkBold)
text((112, 10), "X", style=Styles.DarkBold.patch(text_size=11))

line((16, 6), (16, 48), arrow_head="->", style=Styles.DarkBold)
text((16, 50), "Y", style=Styles.DarkBold.patch(text_size=11))

# Origin marker
circle((16, 10), radius=1.5, style=Styles.AccentFlat)
text((13, 6), "(0, 0)", style=Styles.AccentBold.patch(text_size=9))

# Center anchor element
circle((60, 28), radius=8, style=Styles.PrimaryFlat)
text((60, 28), "Center\n(60, 28)", style=Styles.WhiteBold.patch(text_size=9))

# Corner coordinate labels
text((18, 45), "Top-Left (0, H)", style=Styles.MutedBold.patch(text_size=8))
text((105, 45), "Top-Right (W, H)", style=Styles.MutedBold.patch(text_size=8))
text((105, 14), "Bottom-Right (W, 0)", style=Styles.MutedBold.patch(text_size=8))
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

## Alignment & Text Anchors (`halign` and `valign`)

Text labels support horizontal (`halign`) and vertical (`valign`) alignment configured via style attributes or `.patch()`:

- **Horizontal Alignment (`halign`)**: `"left"`, `"center"`, `"right"`.
- **Vertical Alignment (`valign`)**: `"bottom"`, `"center"`, `"top"`.

```drawlib 620px center file:canvas_text_alignment.png caption:"Figure 3.2: Text Alignment Anchors with halign"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

anchors = [
    (24, "left", "Left Aligned\n(starts at X)", Styles.Primary),
    (60, "center", "Center Aligned\n(centered at X)", Styles.Secondary),
    (96, "right", "Right Aligned\n(ends at X)", Styles.Accent),
]

for x, align_mode, label, st in anchors:
    # Reference vertical alignment line
    line((x, 10), (x, 38), style=Styles.MutedDashed)
    # Red anchor dot
    circle((x, 24), radius=1.5, style=Styles.DangerFlat)
    text((x, 24), label, style=Styles.PrimaryBold.patch(halign=align_mode, text_size=8.5))
    text((x, 6), f"halign='{align_mode}'", style=st.patch(text_size=8.5))
```
