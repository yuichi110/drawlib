# 4. Drawing Primitives: Shapes, Lines & Math

While high-level engines (`ArchitectureDiagram`, `SmartArts`, and `Charts`) automate full multi-node layouts, `drawlib.shapes`, `drawlib.lines`, and `drawlib.math` give you surgical vector control over custom badges, callouts, container geometry, and interpolated connector routes.

```drawlib align=center code=fold file=shapes_gallery.png caption="Figure 4.1: Representative Primitives Across Drawlib's 43 Geometric Shapes"
from drawlib.canvas import save, setup
from drawlib.shapes import (
    bubblespeech,
    chevron,
    circle,
    cloud,
    cylinder,
    document,
    rectangle,
    regularpolygon,
)
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=144, height=68)

xs = [21.0, 55.0, 89.0, 123.0]
ys = [49.5, 18.5]
slot_style = Styles.White.patch(
    shape_r=2.0,
    shape_line_color=Colors.Gray3,
    shape_line_width=1.0,
)

for ry in ys:
    for cx in xs:
        rectangle((cx, ry), width=31.0, height=26.5, style=slot_style)

label_style = Styles.DarkBold.patch(text_size=10.0)
body_dark = Styles.DarkBold.patch(text_size=10.8)

# Row 1: Basic, Ring Cutout, Polygon, Block Arrow
rectangle(
    (xs[0], 52.8),
    width=23.0,
    height=12.0,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text="Focal Card",
    text_style=Styles.WhiteBold.patch(text_size=10.8),
)
text((xs[0], 40.2), "rectangle (shape_r)", style=label_style)

circle(
    (xs[1], 52.8),
    radius=6.8,
    hole_ratio=0.48,
    style=Styles.PrimaryNeutral,
)
text((xs[1], 40.2), "circle (hole_ratio)", style=label_style)

regularpolygon(
    (xs[2], 52.8),
    6,
    7.2,
    style=Styles.SecondaryNeutral.patch(shape_r=0.9),
    text="6-gon",
    text_style=body_dark,
)
text((xs[2], 40.2), "regularpolygon", style=label_style)

chevron(
    (xs[3], 52.8),
    width=20.5,
    height=11.0,
    corner_angle=48,
    style=Styles.Neutral,
    text="Stage 1",
    text_style=body_dark,
)
text((xs[3], 40.2), "chevron", style=label_style)

# Row 2: 3D Container, Cloud, Speech Callout, Stacked Document
cylinder(
    (xs[0], 22.0),
    width=18.5,
    height=13.0,
    disks=1,
    style=Styles.PrimaryNeutral,
    text="Storage",
    text_style=Styles.DarkBold.patch(text_size=10.2, xy_abs_shift=(0, -1.5)),
)
text((xs[0], 9.2), "cylinder", style=label_style)

cloud(
    (xs[1], 22.0),
    width=23.5,
    height=13.5,
    style=Styles.Neutral,
    text="VPC Edge",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
text((xs[1], 9.2), "cloud", style=label_style)

bubblespeech(
    (xs[2] - 10.5, 19.2),
    width=21.0,
    height=9.5,
    tail_edge="bottom",
    tail_start_ratio=0.32,
    tail_vertex_xy=(85.0, 14.5),
    tail_end_ratio=0.55,
    style=Styles.SecondaryNeutral,
    text="SLA < 5ms",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
text((xs[2], 9.2), "bubblespeech", style=label_style)

document(
    (xs[3], 22.0),
    width=19.5,
    height=13.0,
    stacked=2,
    style=Styles.Neutral,
    text="RFC Spec",
    text_style=Styles.DarkBold.patch(text_size=10.2, xy_abs_shift=(0, 0.8)),
)
text((xs[3], 9.2), "document", style=label_style)

save()
```

---

## 4.1 The 43 Shapes of `drawlib.shapes`

`drawlib.shapes` organizes **43 pure-Python vector primitives** into 6 domain families. Every shape function enforces a keyword-only `*, style: Style` contract so geometry and visual tokens never mix.

| Family | Count | Functions in `drawlib.shapes` | Typical Engineering Use Cases |
| :--- | :---: | :--- | :--- |
| **Basic Shapes** | 6 | `rectangle`, `circle`, `ellipse`, `arc`, `fan`, `wedge` | Service cards (`rectangle` + `shape_r`), nodes, donut/ring gauges (`circle` with `hole_ratio` or `wedge` with `width`), radial sectors |
| **Polygons & Custom Paths** | 9 | `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `regularpolygon`, `star`, `plaque`, `polygon`, `shape` | Flowchart decisions (`rhombus`) & I/O (`parallelogram`), pentagons/hexagons/octagons (`regularpolygon(xy, n, r)`), arbitrary cutouts (`polygon` + `holes`) |
| **Arrows & Chevrons** | 6 | `arrow`, `arrow_polyline`, `arrow_arc`, `arrow_l`, `arrow_u`, `chevron` | Prominent phase banners (`chevron`), 1-way or 2-way block arrows (`arrow(..., head="<->")`), orthogonal L/U turn blocks |
| **Containers & Cylinders** | 6 | `cylinder`, `cube`, `document`, `funnel`, `cloud`, `brace` | Persistent databases (`cylinder` with `disks=2`), 3D nodes (`cube`), wave/folded specs (`document`), cloud boundaries, curly `brace` groupings |
| **Badges & Callouts** | 8 | `bubblespeech`, `ribbon`, `shield`, `tag`, `pin`, `checkmark`, `forbidden`, `explosion` | Inline speech callouts (`bubblespeech`), security/IAM badges (`shield`), release tags (`tag`, `ribbon`), geo markers (`pin`), pass/block indicators |
| **Symbols & Flowchart Operators** | 8 | `clock`, `face`, `gear`, `heart`, `lightning`, `math_symbol`, `moon`, `sun` | Cron/latency timers (`clock`), worker daemons (`gear`), cross/plus/arithmetic operators (`math_symbol`), event triggers (`lightning`) |

When building standard software flowcharts, standard ISO symbols map directly to these primitives (`rhombus` for branching decisions, `parallelogram` for data I/O, `document` for artifacts, `cylinder` for storage, and `rectangle` with `shape_r` for process steps)—or can be automated end-to-end with `drawlib.diagrams.flow.FlowDiagram`.

---

## 4.2 Center Anchors `(cx, cy)`, Inline Text, Corner Radius & Rotation

Unlike top-left DOM boxes or bottom-left chart frames, **planar shapes in `drawlib.shapes` anchor at their exact geometric center `xy = (cx, cy)`** (with explicit-vertex exceptions `arrow(xy1, xy2, ...)`, `arrow_polyline(xys, ...)`, `polygon(xys, ...)`, and `bubblespeech(xy, ...)` whose body box starts at bottom-left `(x0, y0)`). This center-first convention makes aligning circles, hexagons, cylinders, and cards along a shared row `y = 20` effortless without subtracting half-widths.

Three ergonomic features keep primitive code compact and declarative:

- **Built-in Inline Labels (`text` & `text_style`)**: 39 of the 43 shapes render centered text directly via `text="..."` and `text_style=...` (eliminating extra `text()` calls). Use `text_style=Styles.DarkBold.patch(xy_abs_shift=(0, -12))` to place captions cleanly underneath compact badges like `pin` or `gear`.
- **Smooth Corner Rounding (`shape_r`)**: Patch `shape_r=2.5` onto `style` to round polygon corners with quadratic Bézier fillets on `rectangle`, `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `regularpolygon`, `star`, and `polygon`.
- **Counter-Clockwise Rotation (`angle`) & Hollow Cutouts (`hole_ratio`)**: Patch `angle=30` onto `style` to rotate a shape CCW around `(cx, cy)` (pass `angle=0` on `text_style` to keep its label horizontal), or pass `hole_ratio=0.5` to cut a true transparent compound ring.

```python
from drawlib.canvas import save, setup
from drawlib.shapes import circle, rectangle, regularpolygon
from drawlib.styles import Styles

setup(width=120, height=40)

# Center-anchored at y=20 with inline text, corner radius, and rotation
rectangle(
    (25, 20),
    width=30,
    height=16,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text="Ingress",
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)
regularpolygon(
    (65, 20),
    6,
    10.0,
    style=Styles.PrimaryNeutral.patch(angle=15, shape_r=1.0),
    text="Router",
    text_style=Styles.DarkBold.patch(text_size=10.5, angle=0),
)
circle(
    (100, 20),
    radius=9.5,
    hole_ratio=0.5,
    style=Styles.Neutral,
    text="50%",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

save()
```

---

## 4.3 Vector Connectors (`drawlib.lines`) & Geometry Helpers (`drawlib.math`)

To wire shapes together cleanly, `drawlib.lines` provides 1D stroke connectors while `drawlib.math` supplies pure-Python vector and interpolation math so you never have to hardcode fragile trigonometry.

- **Straight & Polylines (`line`, `lines`, `lines_curved`)**: `line(xy1, xy2, *, style, arrow_head="->")` draws a direct segment, `lines(xys, ...)` draws sharp orthogonal Manhattan routes, and `lines_curved(xys, r=3.5, ...)` rounds every interior polyline corner with fillet radius `r` (keep $r < \frac{1}{2}\min \|P_{i+1} - P_i\|$). Every line function accepts `arrow_head` values `""`, `"-"`, `"->"`, `"<-"`, and `"<->"`.
- **Arcs & Bézier Curves (`line_curved`, `line_bezier1`, `line_bezier2`, `lines_bezier`, `line_arc`)**: `line_curved(xy1, xy2, bend=0.22, ...)` bulges smoothly left (`bend > 0`) or right (`bend < 0`) of the travel vector—ideal for request/response pairs—while `lines_bezier(xy, path_points, ...)` chains straight `(x, y)`, quadratic `(cp, end)`, and cubic `(cp1, cp2, end)` segments in a single path.
- **Coordinate & Trajectory Math (`drawlib.math`)**:
  - `get_intermediate_point(xy1, xy2)` & `get_intermediate_points(xy1, xy2, num=3)`: Sample evenly spaced waypoints along a segment (plus `get_intermediate_path_points(xys, num=...)` along multi-corner polylines).
  - `rotate_point(xy, angle, center)` & `get_point_on_ellipse(center, width, height, angle)`: Compute exact radial node positions and boundary anchor points without manual `sin`/`cos` boilerplate.
  - `get_angle(xy1, xy2)`, `get_distance(xy1, xy2)`, `get_center_and_size(xys)`, & `compute_orthogonal_path(...)`: Measure slopes, auto-fit cluster bounding boxes, and synthesize L/Z-shaped orthogonal routes.

```drawlib align=center code=fold file=lines_and_math.png caption="Figure 4.2: Vector Connectors (line, lines_curved, line_curved, lines_bezier) and Math Waypoint Helpers"
from drawlib.canvas import save, setup
from drawlib.lines import line, line_curved, lines_bezier, lines_curved
from drawlib.math import get_intermediate_points, rotate_point
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=68)

hdr = Styles.DarkBold.patch(text_size=10.5, halign="left")
note = Styles.Dark.patch(text_size=10.0)
node_light = Styles.White.patch(shape_r=1.8)
node_sec = Styles.SecondaryNeutral.patch(shape_r=1.8)
lbl_dark = Styles.DarkBold.patch(text_size=10.2)

# 4 spacious neutral quadrant panels
rectangle((37.5, 49.5), width=64.0, height=26.5, style=Styles.PrimaryNeutral.patch(shape_r=2.2))
rectangle((106.5, 49.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((37.5, 18.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((106.5, 18.5), width=64.0, height=26.5, style=Styles.SecondaryNeutral.patch(shape_r=2.2))

# Panel 1: Straight "<->" + get_intermediate_points()
text((9.0, 59.0), '1. line("<->") + get_intermediate_points()', style=hdr)
rectangle(
    (16.0, 48.0),
    width=12.5,
    height=8.2,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    text="Src",
    text_style=Styles.WhiteBold.patch(text_size=10.2),
)
rectangle((59.0, 48.0), width=12.5, height=8.2, style=node_light, text="Dst", text_style=lbl_dark)
line((22.5, 48.0), (52.5, 48.0), arrow_head="<->", style=Styles.DarkBold)
for pt in get_intermediate_points((22.5, 48.0), (52.5, 48.0), num=3):
    circle(pt, radius=1.3, style=Styles.AccentFlat)
text((37.5, 39.8), "num=3 interpolated waypoints", style=note)

# Panel 2: Rounded orthogonal routing with lines_curved(r=3.5)
text((78.0, 59.0), '2. lines_curved(xys, r=3.5, arrow_head="->")', style=hdr)
rectangle((85.5, 51.8), width=14.0, height=7.8, style=node_light, text="Ingress", text_style=lbl_dark)
rectangle((127.5, 42.2), width=14.0, height=7.8, style=node_sec, text="Worker", text_style=lbl_dark)
route = [(92.5, 51.8), (106.5, 51.8), (106.5, 42.2), (120.5, 42.2)]
lines_curved(route, r=3.5, arrow_head="->", style=Styles.DarkBold)
text((91.5, 41.2), "r=3.5 corner fillet", style=note)

# Panel 3: Bidirectional arc splines with line_curved(bend=...)
text((9.0, 28.0), "3. line_curved(bend=-0.22) Request / Reply", style=hdr)
rectangle((16.0, 16.0), width=13.0, height=8.2, style=node_light, text="Client", text_style=lbl_dark)
rectangle((59.0, 16.0), width=13.0, height=8.2, style=node_sec, text="Cache", text_style=lbl_dark)
line_curved((22.8, 18.2), (52.2, 18.2), bend=-0.22, arrow_head="->", style=Styles.PrimaryBold)
line_curved((52.2, 13.8), (22.8, 13.8), bend=-0.22, arrow_head="->", style=Styles.DarkBold)
text((37.5, 16.0), "bend = -0.22", style=note)

# Panel 4: Cubic S-curve (lines_bezier) + radial satellite (rotate_point)
text((78.0, 28.0), "4. lines_bezier() + rotate_point()", style=hdr)
rectangle((85.5, 20.8), width=13.5, height=7.6, style=node_light, text="Stream", text_style=lbl_dark)
hub = (125.5, 16.0)
circle(hub, radius=4.8, style=Styles.White, text="Hub", text_style=lbl_dark)
for deg in [35, 145, 270]:
    sat = rotate_point((hub[0] + 7.2, hub[1]), deg, center=hub)
    circle(sat, radius=1.2, style=Styles.PrimaryFlat)
lines_bezier(
    (92.5, 20.8),
    [((107.0, 20.8), (106.0, 16.0), (120.4, 16.0))],
    arrow_head="->",
    style=Styles.DarkBold,
)
text((92.0, 10.2), "Cubic Bezier S-curve", style=note)

save()
```
