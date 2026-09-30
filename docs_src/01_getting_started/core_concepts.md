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

```drawlib 650px center caption:"Drawlib Cartesian Coordinate System"
from drawlib.canvas import setup
from drawlib.shapes import rectangle, circle
from drawlib.lines import line
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=60, grid=True)

# Origin marker
circle((0, 0), radius=2, style=Styles.danger_flat)
text((8, 5), "(0, 0) Bottom-Left Origin", style=Styles.danger_bold)

# Center-based element
rectangle((55, 32), width=44, height=20, style=Styles.primary_flat, text="Centered at (55, 32)", textstyle=Styles.white_bold)
circle((55, 32), radius=1.5, style=Styles.accent_flat)

# Y-axis
line((4, 8), (4, 52), arrowhead="->", style=Styles.bold)
text((8, 50), "+Y (Upwards)", style=Styles.bold)

# X-axis
line((8, 4), (45, 4), arrowhead="->", style=Styles.bold)
text((32, 7), "+X (Rightwards)", style=Styles.bold)
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
- **Containers Before Components**: Draw boundary containers (e.g. `rectangle(..., style=Styles.muted_dashed)`) to establish visual scopes before positioning child components.

---

## 4. The 6-Color Semantic Design System

Professional illustrations maintain visual clarity by structuring colors around Drawlib's 6 core semantic roles, anchoring around `primary` while utilizing the other roles to represent distinct components and states without artificial frequency restrictions:

```drawlib 650px center caption:"The 6-Color Semantic System"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=150, height=35)

# Neutral Foundation / Subnet Boundary (Muted)
rectangle((75, 17.5), width=146, height=30, style=Styles.muted_dashed)

# Primary Anchor (Core Microservice)
rectangle((18, 17.5), width=22, height=18, style=Styles.primary_flat, text="Primary\n(Core)", textstyle=Styles.white_bold)

# Secondary (Database / Auxiliary)
rectangle((44, 17.5), width=22, height=18, style=Styles.secondary_flat, text="Secondary\n(Service)", textstyle=Styles.white_bold)

# Accent (Events / Gateway)
rectangle((70, 17.5), width=22, height=18, style=Styles.accent_flat, text="Accent\n(Trigger)", textstyle=Styles.white_bold)

# Danger (Alert / Error Path)
rectangle((96, 17.5), width=22, height=18, style=Styles.danger_flat, text="Danger\n(Alert)", textstyle=Styles.white_bold)

# Success (Verified Outcome)
rectangle((122, 17.5), width=22, height=18, style=Styles.success_flat, text="Success\n(Audit)", textstyle=Styles.white_bold)
```

1. **Primary Anchor (`Styles.primary`)**:
   Central workflow spine, core microservices, and primary subject matter.
2. **Functional Semantics (`Styles.secondary`, `Styles.accent`, `Styles.danger`, `Styles.success`)**:
   Auxiliary services, events, databases, alerts, and verified deliverables. Used actively across the diagram according to their functional intent without artificial percentage caps.
3. **Muted Structural Base (`Styles.muted`)**:
   Neutral containers, group boundaries, subnets, and grouping boxes (`Styles.muted_flat`, `Styles.muted_dashed`).

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
