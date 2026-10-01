# Chapter 7: Drawing Primitives

Drawlib's primitive drawing layers (`shapes`, `lines`, `text`, `icons`) give you the power to construct custom geometric layouts and specialized diagrams.

## 7.1 Canvas Coordinate System

Drawlib uses a standard **Cartesian coordinate space**:
- **Origin `(0, 0)`**: Located at the **bottom-left** corner of the canvas.
- **Canvas Dimensions**: Defined explicitly using `setup(width=W, height=H)`.

## 7.2 Shapes, Lines, and Vector Icons

Over 22 shape primitives (rectangles, circles, ellipses, wedges, donuts, block arrows, stars) are built-in:

```drawlib 600px center file:fig_basic_drawing.png caption:"Figure 7.1: Service Architecture Built with Shapes, Lines, and Icons"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=105, height=42)

# Client Node
rectangle((20, 21), width=24, height=18, r=1.5, style=Styles.secondary_flat, text="Client App", textstyle=Styles.white_bold)
phosphor.device_mobile(xy=(20, 34), width=6, style=Styles.secondary)

# API Gateway Node
rectangle((55, 21), width=26, height=20, r=1.5, style=Styles.primary_flat, text="API Gateway", textstyle=Styles.white_bold)
phosphor.cloud(xy=(55, 35), width=6, style=Styles.primary)

# Database Cluster Node
circle((88, 21), radius=9, style=Styles.accent_flat, text="DB Cluster", textstyle=Styles.white_bold)
phosphor.database(xy=(88, 34), width=6, style=Styles.accent)

# Connections and Arrows
line((32, 21), (42, 21), arrowhead="->", style=Styles.bold)
text((37, 24), "HTTPS", style=Styles.primary, size=9)

line((68, 21), (79, 21), arrowhead="->", style=Styles.bold)
text((73.5, 24), "SQL", style=Styles.accent, size=9)
```

## 7.3 Essential Drawing Functions

- **`rectangle(xy, width, height, r=0, style=...)`**: Rectangle with optional rounded corners.
- **`circle(xy, radius, style=...)`**: Circle.
- **`line(start_xy, end_xy, arrowhead="->", style=...)`**: Straight line with arrowheads.
- **`line_curved(start_xy, end_xy, bend=0.2, ...)`**: Smooth bezier curves.
- **`text(xy, text="...", style=..., size=12)`**: Styled typography.
- **`phosphor.<icon_name>(xy, width, style=...)`**: Phosphor vector icons.
