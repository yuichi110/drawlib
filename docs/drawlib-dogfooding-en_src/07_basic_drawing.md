# Chapter 7: Drawing Primitives

Drawlib's primitive drawing layers (`shapes`, `lines`, `text`, `icons`) give you the power to construct custom geometric layouts and specialized diagrams.

## 7.1 Canvas Coordinate System & Anchor Rules

Drawlib uses a standard **Cartesian coordinate space**:
- **Origin `(0, 0)`**: Located at the **bottom-left** corner of the canvas (unlike top-left screen coordinates).
- **Canvas Dimensions**: Defined explicitly using `setup(width=W, height=H)`, and finalized by calling `save()`.
- **Center Coordinate Anchor `(cx, cy)`**: All primitive drawing elements (`shapes`, `text`, `icons`, `images`) are anchored by their **center coordinate `(cx, cy)`** (in contrast to high-level modules `smartarts`, `charts`, and `diagrams`, which anchor at the bottom-left `(x0, y0)`).

## 7.2 Shapes, Lines, and Vector Icons

**43 shape primitives** (`rectangle`, `circle`, `ellipse`, `polygon`, `star`, `donuts`, `fan`, `bubblespeech`, `cylinder`, `parallelogram`, `trapezoid`, `chevron`, and block arrows `arrow_polyline`, `arrow_l`, `arrow_u`, `arrow_arc`, etc.) are built-in:

```drawlib align=center file=fig_basic_drawing.png caption="Figure 7.1: Service Architecture Built with Shapes, Lines, and Icons"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=105, height=44)

# Client Node (Neutral baseline)
rectangle(
    (20, 20),
    width=24,
    height=18,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="Client App",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
phosphor.device_mobile(xy=(20, 34), width=6, style=Styles.Secondary)

# API Gateway Node (PrimaryFlat focal highlight)
rectangle(
    (54, 20),
    width=26,
    height=20,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="API Gateway",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
phosphor.cloud(xy=(54, 35), width=6, style=Styles.Primary)

# Database Cluster Node (SecondaryNeutral baseline)
circle(
    (87, 20),
    radius=10,
    style=Styles.SecondaryNeutral,
    text="DB Cluster",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
phosphor.database(xy=(87, 35), width=6, style=Styles.Secondary)

# Connections and Arrows
line((32, 20), (41, 20), arrow_head="->", style=Styles.DarkBold)
text((36.5, 23.5), "HTTPS", style=Styles.DarkBold.patch(text_size=10.5))

line((67, 20), (77, 20), arrow_head="->", style=Styles.DarkBold)
text((72, 23.5), "SQL", style=Styles.DarkBold.patch(text_size=10.5))

save()
```

## 7.3 Essential Drawing Functions

- **`rectangle(xy, width, height, style=...)`**: Rectangle (supports rounded corners via `style.shape_r`).
- **`circle(xy, radius, style=...)`**: Circle.
- **`line(start_xy, end_xy, arrow_head="->", style=...)`**: Straight line with arrowheads.
- **`line_curved(start_xy, end_xy, bend=0.2, ...)`**: Smooth bezier curves.
- **`text(xy, text="...", style=...)`**: Styled typography.
- **`phosphor.<icon_name>(xy, width, style=...)`**: Phosphor vector icons (`drawlib.icons.phosphor`).
- **`fontawesome.<icon_name>(xy, width, style=...)`**: FontAwesome icons (`drawlib.icons.fontawesome`).
- **`gcp.<icon_name>(xy, width, ...)`**: Official Google Cloud architecture icons (`drawlib.icons.gcp`).
