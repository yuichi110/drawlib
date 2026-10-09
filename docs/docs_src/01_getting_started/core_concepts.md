# Core Visual Concepts

To create clean, professional illustrations with Drawlib, it is important to understand its underlying geometry and visual design principles.

---

## 1. Cartesian Coordinate Space & Anchor Categories

Drawlib uses a standard **mathematical Cartesian coordinate system**:

- **Origin `(0, 0)` is at the Bottom-Left**:
  - `x` increases horizontally to the right.
  - `y` increases vertically upwards.
  *(This differs from traditional computer graphics/HTML canvas where `(0, 0)` is at the top-left).*

### The 4 Coordinate Anchor Categories

Across Drawlib's components, coordinates follow four consistent anchoring models depending on the component's natural layout geometry:

1. **Center-Anchored (`(x, y)` = center)**:  
   Most closed shapes (`rectangle`, `circle`, `ellipse`, `donuts`, `triangle`, `regularpolygon`, `star`, `cylinder`, `face`), icons, text, `Cycle`, and `MindMapNode`. *(On shapes, icons, and text, the anchor is configurable via `style.halign` and `style.valign`).*
2. **Bottom-Left Anchored (`(x, y)` = bottom-left)**:  
   `bubblespeech`, `ChevronProcess`, `GridLayout`, `Pyramid`, `BoxList`, `GeoMap`, all `Charts`, and `d.draw(xy=...)` on `Diagrams` and `Graph`.
3. **Top-Left Anchored (`(x, y)` = top-left)**:  
   `Table`, `TreeNode`, `BulletPoints`, and `SourceCode` (components that grow downward as rows/lines are added).
4. **Vertex / Endpoint Coordinates**:  
   `polygon(xys)`, `arrow(xy1, xy2)`, `arrow_polyline(xys)`, `line(xy1, xy2)`, and `lines(xys)`.

```drawlib fold-code 650px center file:core_concepts_four_anchor_categories.png caption:"The Four Coordinate Anchor Conventions in Drawlib"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import arrow, circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=74)

# Panel 1 (Top-Left): Center-Anchored (cx, cy)
rectangle((36, 54.5), width=58, height=30, style=Styles.Neutral.patch(shape_r=2))
text((36, 65.5), "1. Center-Anchored (cx, cy)", style=Styles.DarkBold.patch(text_size=8.8))
rectangle((36, 54), width=26, height=11, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
circle((36, 54), radius=1.2, style=Styles.DangerFlat)
text((36, 50.5), "(cx, cy)", style=Styles.DangerBold.patch(text_size=7.8))
text((36, 43), "shapes, text, icons, Cycle, MindMapNode", style=Styles.Muted.patch(text_size=7.2))

# Panel 2 (Top-Right): Bottom-Left Anchored (x, y)
rectangle((100, 54.5), width=58, height=30, style=Styles.Neutral.patch(shape_r=2))
text((100, 65.5), "2. Bottom-Left Anchored (x, y)", style=Styles.DarkBold.patch(text_size=8.8))
rectangle((101, 54.5), width=24, height=10, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
line((89, 49.5), (117, 49.5), arrow_head="->", style=Styles.DarkBold)
text((120.5, 49.5), "+x", style=Styles.DarkBold.patch(text_size=7.5))
line((89, 49.5), (89, 61.5), arrow_head="->", style=Styles.DarkBold)
text((85.5, 60.5), "+y", style=Styles.DarkBold.patch(text_size=7.5))
circle((89, 49.5), radius=1.2, style=Styles.DangerFlat)
text((82.5, 49.5), "(x, y)", style=Styles.DangerBold.patch(text_size=7.8))
text((100, 43), "ChevronProcess, GridLayout, Charts, Diagrams.draw()", style=Styles.Muted.patch(text_size=7.2))

# Panel 3 (Bottom-Left): Top-Left Anchored (x, y)
rectangle((36, 19.5), width=58, height=30, style=Styles.Neutral.patch(shape_r=2))
text((36, 30.5), "3. Top-Left Anchored (x, y)", style=Styles.DarkBold.patch(text_size=8.8))
rectangle((37, 19), width=24, height=10, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
line((25, 24), (53, 24), arrow_head="->", style=Styles.DarkBold)
text((56.5, 24), "+x", style=Styles.DarkBold.patch(text_size=7.5))
line((25, 24), (25, 12), arrow_head="->", style=Styles.DarkBold)
text((21.5, 13), "-y", style=Styles.DarkBold.patch(text_size=7.5))
circle((25, 24), radius=1.2, style=Styles.DangerFlat)
text((18.5, 24), "(x, y)", style=Styles.DangerBold.patch(text_size=7.8))
text((36, 8), "Table, TreeNode, BulletPoints, SourceCode", style=Styles.Muted.patch(text_size=7.2))

# Panel 4 (Bottom-Right): Vertex / Endpoint (xys)
rectangle((100, 19.5), width=58, height=30, style=Styles.Neutral.patch(shape_r=2))
text((100, 30.5), "4. Vertex / Endpoint (xys)", style=Styles.DarkBold.patch(text_size=8.8))
arrow((86, 16.5), (114, 22.5), tail_width=3.5, head_width=8.5, head_length=6.5, style=Styles.PrimaryFlat)
circle((86, 16.5), radius=1.2, style=Styles.DangerFlat)
text((80, 16.5), "xy1", style=Styles.DangerBold.patch(text_size=7.8))
circle((114, 22.5), radius=1.2, style=Styles.DangerFlat)
text((120, 22.5), "xy2", style=Styles.DangerBold.patch(text_size=7.8))
text((100, 8), "line, lines, arrow, arrow_polyline, polygon", style=Styles.Muted.patch(text_size=7.2))

save()
```

```drawlib fold-code 650px center file:cartesian_coordinate_system.png caption:"Drawlib Cartesian Coordinate System"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle, circle
from drawlib.lines import line
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=60, grid=True)

# Origin marker
circle((0, 0), radius=2, style=Styles.DangerFlat)
text((8, 5), "(0, 0) Bottom-Left Origin", style=Styles.DangerBold)

# Center-based element
rectangle((55, 32), width=44, height=20, style=Styles.PrimaryFlat, text="Centered at (55, 32)", text_style=Styles.WhiteBold)
circle((55, 32), radius=1.5, style=Styles.AccentFlat)

# Y-axis
line((4, 8), (4, 52), arrow_head="->", style=Styles.DarkBold)
text((8, 50), "+Y (Upwards)", style=Styles.DarkBold)

# X-axis
line((8, 4), (45, 4), arrow_head="->", style=Styles.DarkBold)
text((32, 7), "+X (Rightwards)", style=Styles.DarkBold)
save()
```

---

## 2. Canvas Sizing & Virtual Units

Canvas dimensions specified in `setup(width=..., height=...)` represent **arbitrary virtual coordinate units**, not physical pixels. 
Drawlib maps these coordinate units to high-resolution display pixels automatically.

### Recommended Canvas Dimensions
Choose dimensions that match the natural aspect ratio of your diagram:
- **Wide Schemas (16:9 / Landscape)**: `width=120`, `height=50` or `width=140`, `height=60`
- **Balanced Cards (4:3)**: `width=100`, `height=75`
- **Square / Symmetrical**: `width=100`, `height=100`

---

## 3. Perimeter Margins, Z-Order Layering & Geometry Helpers

A common mistake when generating diagrams is placing elements too close to the canvas edges or drawing elements out of z-order:

- **Keep 5%–10% Perimeter Margin**: Leave breathing room around all four borders. For a canvas with `width=100` and `height=60`, avoid placing text or shape boundaries below `x=5`, above `x=95`, below `y=5`, or above `y=55`.
- **4-Layer Painter's Algorithm Z-Order**: Drawlib renders elements in the exact order they are called (back-to-front). Follow this 4-layer drawing sequence so lines never cut across node labels and backgrounds never obscure foreground nodes:
  1. **Layer 1 — Background Zones**: VPCs, subnets, and boundary containers (e.g. `rectangle(..., style=Styles.MutedDashed)`).
  2. **Layer 2 — Connectors / Lines**: Inter-service arrows and communication links (`line`, `line_curved`, `lines`).
  3. **Layer 3 — Primary Nodes / Shapes**: Service cards, databases, icons, and actors (`rectangle`, `circle`, `cylinder`).
  4. **Layer 4 — Callouts / Badges**: Floating protocol badges, status indicators, and speech callouts (`bubblespeech`, `text`).
- **Dynamic Bounding Boxes with `drawlib.math.get_center_and_size()`**: Instead of manually calculating container centers and dimensions around a group of nodes, pass their coordinate list to `get_center_and_size(points)` to obtain `((center_x, center_y), (width, height))` automatically.

```drawlib fold-code 650px center file:core_concepts_z_order_and_margins.png caption:"5%–10% Perimeter Margin Safe Zone and 4-Layer Back-to-Front Z-Order"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=64)

# Outer canvas boundary frame & inner 5%-10% Safe Margin Zone
rectangle((68, 32), width=132, height=60, style=Styles.MutedOutline)
rectangle((68, 30), width=114, height=46, style=Styles.DangerDashed.patch(shape_r=2))
text((68, 56.5), "5%–10% Perimeter Margin Safe Zone (Keep Elements Inside)", style=Styles.DangerBold.patch(text_size=8.5))
line((2, 30), (11, 30), arrow_head="<->", style=Styles.DangerBold)
line((125, 30), (134, 30), arrow_head="<->", style=Styles.DangerBold)

# Z-Layer 1: Background Zone
rectangle((68, 28), width=102, height=34, style=Styles.MutedDashed.patch(shape_r=2))
text((68, 41), "Z-Layer 1: Background Zone (Styles.MutedDashed)", style=Styles.DarkBold.patch(text_size=8.5))

# Z-Layer 2: Connectors (drawn before or between nodes)
line((35, 26), (101, 26), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.5))
text((68, 15), "Z-Layer 2: Connectors (drawn before or between nodes)", style=Styles.DarkBold.patch(text_size=8.2))
line((51, 17.5), (51, 25), arrow_head="->", style=Styles.MutedDashed)
line((85, 17.5), (85, 25), arrow_head="->", style=Styles.MutedDashed)

# Z-Layer 3: Primary Nodes
rectangle(
    (35, 26),
    width=26,
    height=13,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Z-Layer 3:\nPrimary Nodes",
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)
rectangle(
    (101, 26),
    width=26,
    height=13,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="Z-Layer 3:\nPrimary Nodes",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

# Z-Layer 4: Badges & Callouts (drawn last on top of connectors)
rectangle(
    (68, 26),
    width=28,
    height=6.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="Z-Layer 4: Badges & Callouts",
    text_style=Styles.DarkBold.patch(text_size=7.5),
)

save()
```

---

## 4. The Semantic Design System & Color Discipline

Professional illustrations maintain visual clarity by structuring colors around Drawlib's core semantic roles and following the **50%+ Neutral-Grounded Architecture** discipline:

> [!IMPORTANT]
> **Avoid Rainbow Chaos (50%+ Neutral-Grounded Architecture)**:
> Never color every box with saturated fills (`PrimaryFlat`, `AccentFlat`, `SuccessFlat`, `WarningFlat`). Overly colorful diagrams look amateurish and cause visual fatigue.
> - **Ground 50% or more of nodes in calm neutral or tinted-neutral cards**: `Styles.Neutral`, `Styles.NeutralFlat`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`.
> - **Reserve saturated hero fills (`Styles.PrimaryFlat`, `Styles.AccentFlat` with `text_style=Styles.WhiteBold`)** strictly for 1–2 primary focal points.
> - **Use `Styles.MutedDashed` or `Styles.Muted`** for boundary containers, VPCs, and clusters.
> - **Use `Styles.DarkBold` or `Styles.DarkFlat`** for clean, neutral connection lines.

```drawlib fold-code 650px center file:seven_color_semantic_system.png caption:"The Semantic Color System"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=170, height=35)

# Neutral Foundation / Subnet Boundary (Muted)
rectangle((85, 17.5), width=166, height=30, style=Styles.MutedDashed)

# 1. Primary Hero Anchor
rectangle((18, 17.5), width=20, height=18, style=Styles.PrimaryFlat, text="Primary\n(Core Hero)", text_style=Styles.WhiteBold)

# 2. Neutral Supporting Card (50%+ Grounding)
rectangle((40, 17.5), width=20, height=18, style=Styles.Neutral, text="Neutral\n(Card)")

# 3. Secondary Tinted Neutral
rectangle((62, 17.5), width=20, height=18, style=Styles.SecondaryNeutral, text="Secondary\n(Storage)")

# 4. Accent (Trigger / Client)
rectangle((84, 17.5), width=20, height=18, style=Styles.AccentFlat, text="Accent\n(Trigger)", text_style=Styles.WhiteBold)

# 5. Warning (Caution / Review)
rectangle((106, 17.5), width=20, height=18, style=Styles.WarningNeutral, text="Warning\n(Caution)")

# 6. Danger (Alert / Error Path)
rectangle((128, 17.5), width=20, height=18, style=Styles.DangerFlat, text="Danger\n(Alert)", text_style=Styles.WhiteBold)

# 7. Success (Verified Outcome)
rectangle((150, 17.5), width=20, height=18, style=Styles.SuccessNeutral, text="Success\n(Audit)")
save()
```

1. **Primary Anchor (`Styles.PrimaryFlat`)**:
   Central workflow spine, core microservices, and primary subject matter (reserved for 1–2 hero elements).
2. **Neutral Grounding (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`)**:
   General worker nodes, supporting services, and calm card surfaces that provide breathing room for the eye.
3. **Functional Semantics (`Styles.Accent`, `Styles.Warning`, `Styles.Danger`, `Styles.Success`)**:
   Auxiliary events, warnings, alerts, and verified deliverables used purposefully where their functional meaning applies.
4. **Muted Structural Base (`Styles.Muted`)**:
   Neutral containers, group boundaries, subnets, and grouping boxes (`Styles.MutedFlat`, `Styles.MutedDashed`).

---

## 5. Development Overlay: Coordinate Grids

While prototyping, enable the coordinate grid to verify alignments:

```python
# In code:
setup(width=100, height=60, grid=True)
```

Or via CLI flag without changing code:

```bash
$ uv run drawlib show my_diagram.py -g -o test_grid.png
```
