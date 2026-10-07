# Lists & Grids

Drawlib includes four specialized layout components for structuring collections of elements:
- **`GridLayout`**: Positions cards across a matrix of rows and columns with cell spanning.
- **`Pyramid`**: Hierarchical trapezoidal stacks (testing pyramids, security tiers).
- **`BoxList`**: Linear card sequences flowing horizontally or vertically.
- **`BulletPoints`**: Formatted bulleted text lists with customizable indentation levels and icons.

---

## 1. Quick Example: Grid Architecture & Pyramid Stacks



<figure class="drawlib-image" style="text-align: center;">
  <img src="lists_and_grids_images/smartarts_grid_and_pyramid.png" alt="lists_and_grids_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Matrix Grid Layers and Tiered Pyramid Stacks</figcaption>
</figure>



---

## 2. GridLayout (Matrix Architecture)

`GridLayout` organizes cards across a grid of `num_column` columns and `num_row` rows:
- **Anchor**: Bottom-Left `(x, y)`. Row 0 is the bottom row; Column 0 is the left column.
- **Cell Spanning**: A card at `position=(col, row)` can span `width` columns and `height` rows.



```python
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=110, height=75)
grid = GridLayout(num_column=3, num_row=3, style=Styles.Neutral, text_style=Styles.DarkBold, r=2.0)
grid.add(position=(0, 2), width=3, height=1, text="Top Header Span", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
grid.add(position=(0, 0), width=1, height=2, text="Sidebar", style=Styles.SecondaryNeutral)
grid.add(position=(1, 0), width=2, height=2, text="Main Content")
grid.draw(xy=(10, 10), width=90, height=55, margin=1.5)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="lists_and_grids_images/smartarts_gridlayout.png" alt="lists_and_grids_2" style="width: 550px; max-width: 100%;" />
  <figcaption class="drawlib-caption">GridLayout Spanning</figcaption>
</figure>



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



```python
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

<figure class="drawlib-image" style="text-align: center;">
  <img src="lists_and_grids_images/smartarts_boxlist.png" alt="lists_and_grids_3" style="width: 550px; max-width: 100%;" />
  <figcaption class="drawlib-caption">BoxList Sequence</figcaption>
</figure>



---

## 5. BulletPoints (Formatted Text Lists)

`BulletPoints` renders nested lists starting from a top-left coordinate `(x, y)`:



```python
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

<figure class="drawlib-image" style="text-align: center;">
  <img src="lists_and_grids_images/smartarts_bulletpoints.png" alt="lists_and_grids_4" style="width: 550px; max-width: 100%;" />
  <figcaption class="drawlib-caption">BulletPoints List</figcaption>
</figure>


