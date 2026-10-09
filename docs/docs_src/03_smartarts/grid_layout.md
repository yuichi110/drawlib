# GridLayout

The `GridLayout` component positions cards and rectangular blocks across a uniform or flexible column/row matrix. It supports multi-column and multi-row cell spanning, outer container borders, and proportional scaling—making it ideal for layered system architectures, service matrices, and executive dashboard layouts.

---

## 1. Multi-Span Architecture & Dashboard Layout (`draw`)

In standard mode (`grid.draw(...)`), `GridLayout` divides the total `width` and `height` evenly across `num_column` columns and `num_row` rows with a uniform `margin` gutter between cells. If `outer_style` is provided, an outer container frame is drawn with an inner margin around the perimeter.

```drawlib show-code 650px center file:smartarts_gridlayout_architecture.png caption:"Multi-Tier Cloud Architecture with GridLayout Cell Spanning"
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=115, height=75)

grid = GridLayout(
    num_column=4,
    num_row=4,
    style=Styles.Neutral.patch(shape_r=1.5),
    text_style=Styles.DarkBold.patch(text_size=9.5),
)

# Row 3 (Top): Edge Ingress spanning all 4 columns (Hero focal layer)
grid.add(
    position=(0, 3),
    width=4,
    height=1,
    text="Edge Ingress: CDN & WAF Gateway",
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

# Row 2: Application Services Layer
grid.add(position=(0, 2), width=2, height=1, text="Order & Checkout API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 2), width=1, height=1, text="Auth API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(3, 2), width=1, height=1, text="Worker", style=Styles.PrimaryNeutral.patch(shape_r=1.5))

# Row 1: Persistence & Caching Tier
grid.add(position=(0, 1), width=1, height=1, text="PostgreSQL", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(1, 1), width=1, height=1, text="OpenSearch", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 1), width=2, height=1, text="Redis Cluster (Multi-AZ)", style=Styles.SecondaryNeutral.patch(shape_r=1.5))

# Row 0 (Bottom): Shared Infrastructure Foundation
grid.add(
    position=(0, 0),
    width=4,
    height=1,
    text="Kubernetes Platform Foundation (Multi-Region)",
    style=Styles.Neutral.patch(shape_r=1.5),
)

grid.draw(
    xy=(10, 10),
    width=95,
    height=55,
    margin=1.8,
    outer_style=Styles.MutedDashed.patch(shape_r=2.0),
)
save()
```

---

## 2. Flexible Grid Sizing & Custom Cell Overlays (`draw_flexible`)

When columns or rows require asymmetric proportions (such as a narrow sidebar next to a wide content area, or a compact header row), use `grid.draw_flexible(...)` with explicit `column_widths`, `column_margins`, `row_heights`, and `row_margins`. Because the cell positions are deterministic from `xy`, you can also overlay standard icons and shapes inside any cell.

```drawlib show-code 650px center file:smartarts_gridlayout_flexible_icons.png caption:"Flexible Dashboard Grid with Custom Column/Row Proportions and Icon Overlays"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=115, height=70)

grid = GridLayout(
    num_column=3,
    num_row=3,
    style=Styles.Neutral.patch(shape_r=1.5),
    text_style=Styles.DarkBold.patch(text_size=9.5),
)

# Top Header (Row 2, spanning 3 columns)
grid.add(
    position=(0, 2),
    width=3,
    height=1,
    text="Observability Control Plane",
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

# Left Navigation Sidebar (Column 0, spanning Rows 0..1)
grid.add(
    position=(0, 0),
    width=1,
    height=2,
    text="Routing\n&\n Policies",
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)

# Main Content Cards (Columns 1..2, Rows 0..1)
grid.add(position=(1, 1), width=1, height=1, text="      Metrics Store", style=Styles.Neutral.patch(shape_r=1.5))
grid.add(position=(2, 1), width=1, height=1, text="      Trace Collector", style=Styles.Neutral.patch(shape_r=1.5))
grid.add(
    position=(1, 0),
    width=2,
    height=1,
    text="      Alerting & Incident Automation Engine",
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
)

# Render with custom column widths [22, 33, 33] and row heights [16, 16, 11]
grid.draw_flexible(
    xy=(10, 10),
    column_widths=[22.0, 33.0, 33.0],
    column_margins=[2.0, 2.0, 2.0, 2.0],
    row_heights=[16.0, 16.0, 11.0],
    row_margins=[2.0, 2.0, 2.0, 2.0],
    outer_style=Styles.MutedDashed.patch(shape_r=2.0),
)

# Overlay Phosphor icons inside the metric/trace/alert cells using deterministic coordinates
phosphor.chart_bar(xy=(40, 38), width=4.0, style=Styles.PrimaryFlat)
phosphor.activity(xy=(75, 38), width=4.0, style=Styles.PrimaryFlat)
phosphor.bell_ringing(xy=(45, 20), width=4.0, style=Styles.DarkBold)
save()
```

---

## 3. Coordinate & Indexing Rules

- **Bottom-Left Anchor `(x, y)`**: The `xy` coordinate passed to `draw()` or `draw_flexible()` specifies the **bottom-left corner** of the overall grid.
- **Zero-Indexed Bottom-Up Rows**:
  - `column_start = 0` is the **left-most column**, increasing rightward (`0` to `num_column - 1`).
  - `row_start = 0` is the **bottom-most row**, increasing upward (`0` to `num_row - 1`).
- **Cell Spanning**: `grid.add(position=(col, row), width=w, height=h)` spans `w` columns rightward (`col` through `col + w - 1`) and `h` rows upward (`row` through `row + h - 1`).

```drawlib fold-code 650px center file:smartarts_gridlayout_indexing_geometry.png caption:"GridLayout Bottom-Up (col, row) Matrix Indexing and Multi-Cell Spanning"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles
from drawlib.text import text

setup(width=125, height=58)

grid = GridLayout(
    num_column=3,
    num_row=3,
    style=Styles.Neutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

# Row 0 (Bottom Row)
grid.add(position=(0, 0), width=1, height=1, text="pos=(0, 0)\nw=1, h=1", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
grid.add(position=(1, 0), width=1, height=1, text="pos=(1, 0)\nw=1, h=1")
grid.add(position=(2, 0), width=1, height=1, text="pos=(2, 0)\nw=1, h=1")

# Row 1 (Middle Row) & Spanned Cell across Columns 1..2, Rows 1..2
grid.add(position=(0, 1), width=1, height=1, text="pos=(0, 1)\nw=1, h=1")
grid.add(
    position=(1, 1),
    width=2,
    height=2,
    text="Spanned Cell: position=(1, 1), width=2, height=2\n(Covers cols 1..2, rows 1..2)",
    style=Styles.PrimaryFlat.patch(shape_r=1.2),
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)

# Row 2 (Top Row, Column 0)
grid.add(position=(0, 2), width=1, height=1, text="pos=(0, 2)\nw=1, h=1", style=Styles.SecondaryNeutral.patch(shape_r=1.2))

grid.draw(
    xy=(22.0, 10.0),
    width=90.0,
    height=40.0,
    margin=1.8,
    outer_style=Styles.MutedDashed.patch(shape_r=1.8),
)

# Axis arrows and anchor dot at bottom-left xy=(22, 10)
line((38.0, 5.5), (112.0, 5.5), arrow_head="->", style=Styles.PrimaryBold)
text((75.0, 2.5), "Column Index (col = 0 → 2, +x Rightward)", style=Styles.PrimaryBold.patch(text_size=8.0))

line((16.5, 10.0), (16.5, 50.0), arrow_head="->", style=Styles.PrimaryBold)
text((8.5, 30.0), "Row Index\n(row = 0 → 2)\n+y Upward", style=Styles.PrimaryBold.patch(text_size=7.5))

circle((22.0, 10.0), radius=1.2, style=Styles.DangerFlat)
text((22.0, 5.5), "xy=(22, 10)", style=Styles.DangerBold.patch(text_size=8.0))
text((67.0, 53.5), "3×3 GridLayout Matrix (Bottom-Up Indexing & Multi-Cell Spanning)", style=Styles.BlackBold.patch(text_size=9.5))

save()
```

---

## 4. API Reference

### Constructor
```python
GridLayout(
    *,
    num_column: int,
    num_row: int,
    style: Style,
    text_style: Style,
)
```

### Methods & Properties
- **`add(position: tuple[int, int], width: int, height: int, *, style: Style | None = None, text: str = "", text_style: Style | None = None, show: bool = True) -> GridItem`**:
  Registers a grid card at `position=(column_start, row_start)` spanning `width` columns and `height` rows. Returns a mutable `GridItem` (`position`, `width`, `height`, `style`, `text`, `text_style`, `show`). Setting `show=False` hides the cell while keeping the matrix layout intact.
- **`grid.items -> list[GridItem]`**:
  Returns the list of all registered `GridItem` instances (`position: tuple[int, int]`, `width: int`, `height: int`, `style: Style`, `text: str`, `text_style: Style`, `show: bool`), allowing deferred mutation before or between `draw()` calls.
- **`draw(xy: tuple[float, float], width: float, height: float, margin: float, outer_style: Style | None = None, scale: float = 1.0) -> None`**:
  Renders the grid with equal column widths and equal row heights separated by `margin`. If `outer_style` is provided, draws an outer container rectangle and adds `margin` padding around the outer perimeter.
- **`draw_flexible(xy: tuple[float, float], column_widths: list[float], column_margins: list[float], row_heights: list[float], row_margins: list[float], outer_style: Style | None = None, scale: float = 1.0) -> None`**:
  Renders the grid using explicit column widths (`len == num_column`), column margins (`len == num_column + 1`), row heights (`len == num_row`), and row margins (`len == num_row + 1`).

