# Lists & Grids

Drawlib includes four specialized layout components for structuring collections of elements:
- **`GridLayout`**: Positions cards across a matrix of rows and columns with cell spanning.
- **`Pyramid`**: Hierarchical trapezoidal stacks (testing pyramids, security tiers).
- **`BoxList`**: Linear card sequences flowing horizontally or vertically.
- **`BulletPoints`**: Formatted bulleted text lists with customizable indentation levels and icons.

---

## 1. Quick Example: Grid Architecture & Pyramid Stacks

```drawlib 650px center file:smartarts_grid_and_pyramid.png caption:"Matrix Grid Layers and Tiered Pyramid Stacks"
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout, Pyramid
from drawlib.styles import Styles

setup(width=130, height=60)

# 1. GridLayout: Cloud Architecture Layers
grid = GridLayout(num_column=2, num_row=2, style=Styles.Neutral.patch(shape_r=1.5), text_style=Styles.DarkBold)
grid.add(position=(0, 1), width=2, height=1, text="API Gateway Layer", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
grid.add(position=(0, 0), width=1, height=1, text="Auth Service")
grid.add(position=(1, 0), width=1, height=1, text="Order Service", style=Styles.SecondaryNeutral)
grid.draw(xy=(10, 10), width=50, height=40, margin=1.5)

# 2. Pyramid: Software Testing Pyramid
pyramid = Pyramid(style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=9))
pyramid.add("E2E UI (10%)", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=9))
pyramid.add("Integration (30%)", style=Styles.SecondaryNeutral)
pyramid.add("Unit Tests (60%)", style=Styles.Neutral)
pyramid.draw(xy=(75, 10), width=45, height=40, margin=1.5, order="vertex_to_base")
save()
```

---

## 2. GridLayout (Matrix Architecture)

`GridLayout` organizes cards across a grid of `num_column` columns and `num_row` rows:
- **Anchor**: Bottom-Left `(x, y)`. Row 0 is the bottom row; Column 0 is the left column.
- **Cell Spanning**: `grid.add(position=(col, row), width=1, height=1, text="", style=None, text_style=None, show: bool = True)` spans `width` columns and `height` rows. Setting `show=False` hides the cell card while preserving the matrix grid.
- **Rendering**: `grid.draw(xy, width, height, margin, outer_margin=0.0, *, scale: float = 1.0)` renders all visible cells and proportionally scales geometry and typography by `scale`.

```drawlib show-code 550px center file:smartarts_gridlayout.png caption:"GridLayout Spanning"
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=110, height=75)
grid = GridLayout(num_column=3, num_row=3, style=Styles.Neutral.patch(shape_r=2.0), text_style=Styles.DarkBold)
grid.add(position=(0, 2), width=3, height=1, text="Top Header Span", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
grid.add(position=(0, 0), width=1, height=2, text="Sidebar", style=Styles.SecondaryNeutral)
grid.add(position=(1, 0), width=2, height=2, text="Main Content")
grid.draw(xy=(10, 10), width=90, height=55, margin=1.5)
save()
```

---

## 3. Pyramid (Tiered Stacks)

`Pyramid` renders hierarchical trapezoids crowned by an apex triangle:
- **Anchor**: Bottom-Left `(x, y)`.
- **`pyramid.add(text="", style=None, text_style=None, show: bool = True)`**: Appends a tier. Hidden tiers (`show=False`) keep their trapezoid slice reserved so remaining tiers stay in their exact positions.
- **`pyramid.draw(xy, width, height, margin, align="bottom", order="vertex_to_base", *, scale: float = 1.0)`**:
  - **`order`**: `"vertex_to_base"` (first item at apex) or `"base_to_vertex"` (first item at wide base).
  - **`align`**: `"bottom"` (standard upright pyramid), `"top"` (inverted funnel), `"left"`, `"right"`.
  - **`scale`**: Proportionally scales dimensions, margins, and font sizes relative to `xy`.

---

## 4. BoxList (Linear Card Sequences)

`BoxList` sequences cards along one axis (`align="left"`, `"right"`, `"top"`, or `"bottom"`):
- **`bl.add(text, *, style=None, text_style=None, show: bool = True)`**: Adds a box to the sequence (`show=False` reserves the box slot and spacing without drawing the box).
- **`bl.draw(xy, box_width, box_height, box_margin=2.0, align="left", *, scale: float = 1.0)`**: Renders the sequence anchored at `xy` with proportional scaling via `scale`.

```drawlib show-code 550px center file:smartarts_boxlist.png caption:"BoxList Sequence"
from drawlib.canvas import save, setup
from drawlib.smartarts import BoxList
from drawlib.styles import Styles

setup(width=110, height=35)
bl = BoxList(style=Styles.Neutral, text_style=Styles.DarkBold)
bl.add("Step 1")
bl.add("Step 2", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)  # Highlighted hero step
bl.add("Step 3")
bl.draw(xy=(17, 10), box_width=25, box_height=15, align="left")
save()
```

---

## 5. BulletPoints (Formatted Text Lists)

`BulletPoints` renders nested lists starting from a top-left coordinate `(x, y)`:
- **`bp.add(text, style=None, text_style=None, show: bool = True)`**: Appends a bullet item at the current indent level (`show=False` keeps vertical spacing fixed for subsequent items).
- **`bp.draw(xy, *, scale: float = 1.0)`**: Renders all visible bullet points anchored at `xy`, scaling indent width, vertical margin, icon size, and font size by `scale`.

```drawlib show-code 550px center file:smartarts_bulletpoints.png caption:"BulletPoints List"
from drawlib.canvas import save, setup
from drawlib.smartarts import BulletPoints
from drawlib.styles import Styles

setup(width=100, height=45)
bp = BulletPoints(text_style=Styles.DarkBold, vertical_margin=8.0, indent_width=5.0)
bp.set_indent(1)
bp.add("First architectural requirement")
bp.add("Second architectural requirement")
bp.set_indent(2)
bp.add("Nested implementation detail")
bp.draw(xy=(10, 35))
save()
```
