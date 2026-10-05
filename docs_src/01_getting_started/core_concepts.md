# Core Visual Concepts

To create clean, professional illustrations with Drawlib, it is important to understand its underlying geometry and visual design principles.

---

## 1. Cartesian Coordinate Space

Drawlib uses a standard **mathematical Cartesian coordinate system**:

- **Origin `(0, 0)` is at the Bottom-Left**:
  - `x` increases horizontally to the right.
  - `y` increases vertically upwards.
  *(This differs from traditional computer graphics/HTML canvas where `(0, 0)` is at the top-left).*
- **Center-Based Anchoring**:
  - By default, all closed shapes (`rectangle`, `circle`, `donuts`, `polygon`) and icons are anchored at their exact **geometric center `(x, y)`**.

```drawlib 650px center file:cartesian_coordinate_system.png caption:"Drawlib Cartesian Coordinate System"
from drawlib.canvas import setup
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

## 3. Perimeter Margins and Breathing Room

A common mistake when generating diagrams is placing elements too close to the canvas edges.

- **Keep 5%–10% Margin**: Leave breathing room around all four borders. For a canvas with `width=100` and `height=60`, avoid placing text or shape boundaries below `x=5`, above `x=95`, below `y=5`, or above `y=55`.
- **Containers Before Components**: Draw boundary containers (e.g. `rectangle(..., style=Styles.MutedDashed)`) to establish visual scopes before positioning child components.

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

```drawlib 650px center file:seven_color_semantic_system.png caption:"The Semantic Color System"
from drawlib.canvas import setup
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
