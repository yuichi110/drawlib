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
grid = GridLayout(num_column=2, num_row=2, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold, r=1.5)
grid.add(position=(0, 1), width=2, height=1, text="API Gateway Layer", style=Styles.PrimaryFlat)
grid.add(position=(0, 0), width=1, height=1, text="Auth Service", style=Styles.AccentFlat)
grid.add(position=(1, 0), width=1, height=1, text="Order Service", style=Styles.SecondaryFlat)
grid.draw(xy=(10, 10), width=50, height=40, margin=1.5)

# 2. Pyramid: Software Testing Pyramid
pyramid = Pyramid(style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=9))
pyramid.add("E2E UI (10%)", style=Styles.DangerFlat)
pyramid.add("Integration (30%)", style=Styles.AccentFlat)
pyramid.add("Unit Tests (60%)", style=Styles.SuccessFlat)
pyramid.draw(xy=(75, 10), width=45, height=40, margin=1.5, order="vertex_to_base")
save()
```

---

## 2. GridLayout (Matrix Architecture)

`GridLayout` organizes cards across a grid of `num_column` columns and `num_row` rows:
- **Anchor**: Bottom-Left `(x, y)`. Row 0 is the bottom row; Column 0 is the left column.
- **Cell Spanning**: A card at `position=(col, row)` can span `width` columns and `height` rows.

```drawlib show-code 550px center file:smartarts_gridlayout.png caption:"GridLayout Spanning"
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=110, height=75)
grid = GridLayout(num_column=3, num_row=3, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold, r=2.0)
grid.add(position=(0, 2), width=3, height=1, text="Top Header Span", style=Styles.PrimaryFlat)
grid.add(position=(0, 0), width=1, height=2, text="Sidebar", style=Styles.SecondaryFlat)
grid.add(position=(1, 0), width=2, height=2, text="Main Content", style=Styles.AccentFlat)
grid.draw(xy=(10, 10), width=90, height=55, margin=1.5)
save()
```

---

## 3. Pyramid (Tiered Stacks)

`Pyramid` renders hierarchical trapezoids crowned by an apex triangle:
- **Anchor**: Bottom-Left `(x, y)`.
- **`order`**:
  - `"vertex_to_base"`: First added item is positioned at the apex; subsequent items widen toward the base.
  - `"base_to_vertex"`: First added item starts at the wide base.
- **`align`**: `"bottom"` (standard upright pyramid), `"top"` (inverted funnel), `"left"`, `"right"`.

---

## 4. BoxList (Linear Card Sequences)

`BoxList` sequences cards along one axis (`align="left"`, `"right"`, `"top"`, or `"bottom"`):

```drawlib show-code 550px center file:smartarts_boxlist.png caption:"BoxList Sequence"
from drawlib.canvas import save, setup
from drawlib.smartarts import BoxList
from drawlib.styles import Styles

setup(width=110, height=35)
bl = BoxList(style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
bl.append("Step 1")
bl.append("Step 2", style=Styles.AccentFlat)  # Highlighted step
bl.append("Step 3")
bl.draw(xy=(17, 10), box_width=25, box_height=15, align="left")
save()
```

---

## 5. BulletPoints (Formatted Text Lists)

`BulletPoints` renders nested lists starting from a top-left coordinate `(x, y)`:

```drawlib show-code 550px center file:smartarts_bulletpoints.png caption:"BulletPoints List"
from drawlib.canvas import save, setup
from drawlib.smartarts import BulletPoints
from drawlib.styles import Styles

setup(width=100, height=45)
bp = BulletPoints(text_style=Styles.PrimaryBold, vertical_margin=8.0, indent_width=5.0)
bp.set_indent(1)
bp.add("First architectural requirement")
bp.add("Second architectural requirement")
bp.set_indent(2)
bp.add("Nested implementation detail")
bp.draw(xy=(10, 35))
save()
```
