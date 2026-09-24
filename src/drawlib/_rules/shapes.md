# Drawlib Shapes Guidelines

Draw 2D geometric shapes onto the canvas. Shapes support built-in centered text labels and alignment controls.

## 1. Imports
```python
from drawlib.shapes import (
    circle,
    donut,
    ellipse,
    polygon,
    rectangle,
    regular_polygon,
    wedge,
)
from drawlib.types import Style
```

## 2. Core Functions
- `rectangle(xy, width, height, r=0, style=None, text="", textstyle=None, angle=0, halign="center", valign="center")`
  - `xy`: Coordinates `(x, y)` representing shape anchor (default center).
  - `r`: Corner radius for rounded corners.
- `circle(xy, radius, style=None, text="", textstyle=None, angle=0, halign="center", valign="center")`
- `ellipse(xy, width, height, style=None, text="", textstyle=None, angle=0, halign="center", valign="center")`
- `wedge(xy, radius, angle1, angle2, style=None, text="", textstyle=None)`
- `polygon(points, style=None, text="", textstyle=None)`
  - `points`: List of vertices `[(x1, y1), (x2, y2), ...]`.
- `regular_polygon(xy, num_vertices, radius, style=None, text="", textstyle=None, angle=0)`
- `donut(xy, radius_outer, radius_inner, style=None, text="", textstyle=None)`

## 3. Style & Alignment
- `style`: Preset style string (e.g. `"blue"`, `"red_flat"`, `"green_solid"`) or `Style(...)` object.
- `text`: Text string centered inside shape (or positioned via shape text alignment).
- `textstyle`: Style for the shape's text (e.g. `"white_bold"`, `"blue_light"`).
- `halign`: Horizontal anchor alignment (`"left"`, `"center"`, `"right"`).
- `valign`: Vertical anchor alignment (`"bottom"`, `"center"`, `"top"`).

## 4. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.shapes import circle, rectangle

config(width=100, height=50)
rectangle((30, 25), width=35, height=20, r=2, style="blue_flat", text="Service", textstyle="white")
circle((75, 25), radius=12, style="green_solid", text="Active", textstyle="green_bold")
save()
```
