# 4. Drawing Primitives: Shapes, Lines & Math

Drawlib provides a rich suite of 2D geometric primitives, flexible line connecting algorithms, styled text labels, and geometric math utilities.

## Shape Primitives (`drawlib.shapes`)

Drawlib includes over 20 shape primitives. Every shape supports direct text embedding, corner radius rounding (`style.shape_r`), rotation (`style.angle`), and full alignment controls (`style.halign`, `style.valign`):

```drawlib 620px center file:shapes_primitives.png caption:"Figure 4.1: Selection of Drawlib Vector Shapes"
from drawlib.canvas import setup
from drawlib.shapes import chevron, circle, donuts, polygon, rectangle, rhombus
from drawlib.styles import Styles

setup(width=120, height=45)

# 1. Rounded Rectangle
rectangle((15, 23), width=20, height=22, style=Styles.PrimaryFlat.patch(shape_r=2), text="Rounded\nBox", text_style=Styles.WhiteBold)

# 2. Circle
circle((38, 23), radius=10, style=Styles.SecondaryFlat, text="Circle", text_style=Styles.WhiteBold)

# 3. Donut Ring
donuts((60, 23), radius=10, width=4, style=Styles.AccentFlat, text="Ring", text_style=Styles.WhiteBold)

# 4. Rhombus / Decision Diamond
rhombus((80, 23), width=18, height=20, style=Styles.DangerFlat, text="Decision", text_style=Styles.WhiteBold)

# 5. Process Chevron
chevron((102, 23), width=18, height=18, corner_angle=60, style=Styles.SuccessFlat, text="Stage", text_style=Styles.WhiteBold)
```

### Direct Text Integration in Shapes

In traditional plotting tools, placing a centered label inside a box requires calculating coordinates and issuing separate text calls. In Drawlib, shapes accept `text` and `text_style` directly:

```python
from drawlib.shapes import rectangle
from drawlib.styles import Styles

rectangle(
    xy=(50, 30),
    width=32,
    height=18,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="Worker Node\n(Active)",
    text_style=Styles.WhiteBold,
)
```

## Connecting Lines & Arrowheads (`drawlib.lines`)

Drawlib provides straight, curved, bezier, and multi-segment chained lines with customizable arrowheads:

- **Arrowhead Styles**: `"->"` (end), `"<-"` (start), `"<->"` (both ends), `"-"` (none).
- **Line Functions**:
  - `line(xy1, xy2, arrow_head="->", style=...)`: Straight connection.
  - `line_curved(xy1, xy2, bend=0.25, arrow_head="->", style=...)`: Smooth arc with defined bend curve.
  - `line_bezier1(xy1, xy2, cp, ...)` / `line_bezier2`: Bezier paths with control points.
  - `lines(xys=[(x1, y1), (x2, y2), ...], ...)`: Polyline connecting arbitrary waypoints.

> [!TIP]
> **Neutral Connectors Principle**: Always use `Styles.DarkBold` (or `Styles.LightBold` on dark backgrounds) for standard sequential lines and arrows. Reserve colors (`Styles.Primary`, `Styles.Accent`, `Styles.Danger`) strictly for meaningful distinctions, such as primary data flows or error rollbacks.

```drawlib 620px center file:lines_connections.png caption:"Figure 4.2: Connecting Lines, Curvature, and Arrowheads"
from drawlib.canvas import setup
from drawlib.lines import line, line_curved, lines
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=45)

# Nodes
circle((20, 23), radius=8, style=Styles.PrimaryFlat, text="A", text_style=Styles.WhiteBold)
circle((60, 35), radius=8, style=Styles.SecondaryFlat, text="B", text_style=Styles.WhiteBold)
circle((100, 23), radius=8, style=Styles.AccentFlat, text="C", text_style=Styles.WhiteBold)

# 1. Straight Line A -> B
line((28, 25), (52, 33), arrow_head="->", style=Styles.DarkBold)
text((38, 33), "Direct", style=Styles.DarkBold.patch(text_size=8.5))

# 2. Curved Arc B -> C
line_curved((68, 35), (92, 25), bend=0.25, arrow_head="->", style=Styles.DarkBold)
text((84, 35), "Curved Arc", style=Styles.DarkBold.patch(text_size=8.5))

# 3. Chained Orthogonal Path A -> C
lines([(20, 15), (20, 8), (100, 8), (100, 15)], arrow_head="->", style=Styles.MutedDashedBold)
text((60, 5), "Multi-Point Orthogonal Route", style=Styles.MutedBold.patch(text_size=8))
```

## Geometric Math Utilities (`drawlib.math`)

When computing dynamic layouts or connecting rotated components, use `drawlib.math`:

- **`get_distance(p1, p2)`**: Euclidean distance between two points.
- **`get_angle(p1, p2)`**: Angle in degrees from `p1` to `p2` relative to the X-axis.
- **`get_center_and_size(points)`**: Bounding box center coordinate `(cx, cy)` and `(width, height)` enclosing a collection of coordinates.
