# Block Arrows

In addition to line connectors (`drawlib.lines`), Drawlib provides six **directed block arrow primitives** in `drawlib.shapes`. 
Block arrows are closed 2D polygons with customizable tail widths, arrowhead dimensions, and corner rounding. They are widely used for data pipelines, architectural flows, and process stages.

---

## 1. Overview of Block Arrow Functions

```drawlib 650px center file:arrow_overview.png caption:"Overview of Drawlib Block Arrow Primitives"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, arrow_arc, arrow_l, arrow_u, chevron
from drawlib.styles import Styles

setup(width=120, height=60)

# 1. Straight Block Arrow
arrow((15, 45), (45, 45), tail_width=4, head_width=10, head_length=8, style=Styles.PrimaryFlat, text="arrow", text_style=Styles.WhiteBold)

# 2. Chevron
chevron((75, 45), width=24, height=14, corner_angle=60, style=Styles.AccentFlat, text="chevron", text_style=Styles.WhiteBold)

# 3. Arrow Arc (Circular flow)
arrow_arc((105, 45), width=20, height=20, angle_start=180, angle_end=0, tail_width=3, head_width=8, style=Styles.SuccessFlat)

# 4. L-shaped Arrow
arrow_l((30, 20), width=25, height=20, tail_width=3, head_width=8, head_length=6, style=Styles.SecondaryFlat)

# 5. U-turn Arrow
arrow_u((75, 20), width=25, height=22, tail_width=3, head_width=8, head_length=6, style=Styles.DangerFlat)

save()
```

---

## 2. Straight Block Arrow (`arrow`)

Draws a directed block arrow between two arbitrary coordinates `xy1` and `xy2`.

```drawlib show-code 600px center file:arrow_straight.png caption:"Straight Block Arrow with Centered Label"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow
from drawlib.styles import Styles

setup(width=100, height=40)
arrow(
    (15, 20),
    (85, 20),
    tail_width=5,
    head_width=13,
    head_length=10,
    head="->",  # "->", "<-", or "<->"
    style=Styles.PrimaryFlat,
    text="Data Ingestion",
    text_style=Styles.WhiteBold,
)
save()
```

- **`head`**: Supports single forward (`"->"`), backward (`"<-"`), or bidirectional (`"<->"`) arrowheads.
- **`text`**: Automatically centers a label within the arrow shaft.

---

## 3. Process Chevron (`chevron`)

Draws an interlocking arrowhead-shaped block with an indented rear notch, ideal for sequential stage diagrams:

```drawlib show-code 600px center file:arrow_chevron.png caption:"Sequential Process Chevron"
from drawlib.canvas import save, setup
from drawlib.shapes import chevron
from drawlib.styles import Styles

setup(width=100, height=40)
chevron(
    (50, 20),
    width=40,
    height=20,
    corner_angle=60,  # Tip acute angle
    style=Styles.AccentFlat,
    text="Stage 1",
    text_style=Styles.WhiteBold,
)
save()
```

> [!TIP]
> For chained multi-stage chevron pipelines, consider using the high-level **[`ChevronProcess`](../03_smartarts/chevron_process.md)** component, which calculates automatic spacing and themes.

---

## 4. Orthogonal Routed Arrows

### L-Shaped Corner Arrow (`arrow_l`)
Draws a 90-degree right-angled block arrow within a bounding box `(width, height)`.

```drawlib show-code 600px center file:arrow_l.png caption:"Right-Angled Corner Arrow"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_l
from drawlib.styles import Styles

setup(width=100, height=60)
arrow_l(
    (50, 30),
    width=40,
    height=35,
    tail_width=4,
    head_width=11,
    head_length=8,
    r=5,  # Corner rounding radius
    style=Styles.SecondaryFlat,
)
save()
```

### U-Turn Feedback Arrow (`arrow_u`)
Draws a 180-degree turnaround block arrow, typically used for retry mechanisms or feedback loops.

```drawlib show-code 600px center file:arrow_u.png caption:"180-Degree U-Turn Arrow"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_u
from drawlib.styles import Styles

setup(width=100, height=60)
arrow_u(
    (50, 30),
    width=35,
    height=40,
    tail_width=4,
    head_width=11,
    head_length=8,
    r=6,  # Corner rounding radius
    style=Styles.DangerFlat,
)
save()
```

---

## 5. Circular & Multi-Point Arrows

### Circular Arc Arrow (`arrow_arc`)
Draws an elliptical arc block arrow between `angle_start` and `angle_end`.

```drawlib show-code 600px center file:arrow_arc.png caption:"Circular Arc Arrow"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_arc
from drawlib.styles import Styles

setup(width=100, height=35)
arrow_arc(
    (50, 26),
    width=45,
    height=32,
    angle_start=180,
    angle_end=0,
    tail_width=4,
    head_width=11,
    style=Styles.SuccessFlat,
)
save()
```

### Multi-Point Polyline Arrow (`arrow_polyline`)
Draws a complex routed block arrow passing through an arbitrary list of waypoint coordinates `[(x1, y1), (x2, y2), ...]`.

```drawlib show-code 600px center file:arrow_polyline.png caption:"Multi-Point Polyline Arrow"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_polyline
from drawlib.styles import Styles

setup(width=100, height=60)
arrow_polyline(
    [(15, 15), (50, 15), (50, 45), (85, 45)],
    tail_width=4,
    head_width=11,
    head_length=8,
    r=4,
    style=Styles.PrimaryFlat,
)
save()
```
