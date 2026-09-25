# 3. Canvas, Coordinates & Shapes

Every Drawlib illustration takes place on a coordinate **Canvas**. By default, the canvas spans `width=100` and `height=100` coordinate units with the origin `(0, 0)` at the bottom-left corner.

## Configuring the Canvas

Use `config()` from `drawlib.canvas` to customize the coordinate dimensions, resolution (`dpi`), or alignment grid (`grid=True`):

```python
from drawlib.canvas import config

config(width=100, height=50, dpi=200, grid=True)
```

- **`width` / `height`**: Logical coordinate space (default: `100` x `100`).
- **`dpi`**: Dots per inch resolution (default: `100`, where 10 inches x 100 DPI = 1000px width).
- **`grid`**: Overlays a coordinate grid and center axes to assist with precise placement.

## Drawing Fundamental Primitives

Drawlib provides intuitive functions for lines, circles, rectangles, polygons, arrows, and text:

```drawlib 580px center caption:"Figure 3.1: Fundamental Shapes and Coordinate Grid"
from drawlib.canvas import config
from drawlib.lines import line
from drawlib.shapes import arrow, circle, rectangle
from drawlib.text import text

config(width=100, height=50, grid=True)

# Circle at (20, 28)
circle(xy=(20, 28), radius=12, style=styles.blue)
text(xy=(20, 8), text="circle((20, 28))", style=styles.primary, size=10)

# Rectangle at (50, 28)
rectangle(xy=(50, 28), width=22, height=20, r=2, style=styles.green)
text(xy=(50, 8), text="rectangle((50, 28))", style=styles.primary, size=10)

# Arrow and Line at (80, 28)
arrow((70, 28), (90, 28), tail_width=4, head_width=10, head_length=6, style=styles.red)
line((70, 18), (90, 18), arrowhead="<->", style=styles.black)
text(xy=(80, 8), text="arrow & line", style=styles.primary, size=10)
```

## Coordinate Alignment (`halign` and `valign`)

All shapes and text elements support horizontal (`left`, `center`, `right`) and vertical (`bottom`, `center`, `top`) alignment via `Style(halign=..., valign=...)`, making it effortless to align labels and boxes around any anchor point `(x, y)`.
