# Drawlib GridLayout SmartArt Guidelines (`lib-smartarts-grid-layout`)

`GridLayout` positions cards and rectangles across a uniform or flexible column/row matrix, supporting multi-column and multi-row cell spanning (`GridItem`), custom corner radii, and optional outer container frames.

---

## 1. Coordinate & Indexing Rules

- **Anchor (`align`)**: Coordinate `xy=(x, y)` marks the **bottom-left corner** (`align="bottom_left"`, default) or **center** (`align="center"`) of the entire grid.
- **Row Indexing (`0` = Bottom)**: `row_start=0` is the **bottom-most row**. Rows increment upward (`+y`) toward `num_row - 1` (the top-most row).
- **Column Indexing (`0` = Left)**: `column_start=0` is the **left-most column**. Columns increment rightward (`+x`) toward `num_column - 1`.
- **Cell Spanning**: A cell registered at `position=(column_start, row_start)` spans `width` columns (`column_start .. column_start + width - 1`) and `height` rows (`row_start .. row_start + height - 1`).

---

## 2. Constructor, `GridItem` & Methods

```python
from drawlib.smartarts import GridItem, GridLayout

grid = GridLayout(
    *,
    num_column: int,
    num_row: int,
    style: Style,
    text_style: Style,
)
```

### Item Model (`GridItem`) & `.items` Property

- `grid.items -> list[GridItem]`: Returns the list of registered `GridItem` instances.
- `GridItem` attributes (mutable before or between `draw()` calls):
  - `position: tuple[int, int]` (`(column_start, row_start)`)
  - `width: int` (number of columns spanned)
  - `height: int` (number of rows spanned)
  - `style: Style`
  - `text: str`
  - `text_style: Style`
  - `show: bool = True`

### Adding Cells & Drawing Modes

```python
item = grid.add(
    position: tuple[int, int],  # (column_start, row_start)
    width: int,                 # Number of columns spanned (>= 1)
    height: int,                # Number of rows spanned (>= 1)
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
    show: bool = True,
) -> GridItem

grid.draw(
    xy: tuple[float, float],
    width: float,
    height: float,
    margin: float,
    outer_style: Style | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self

grid.draw_flexible(
    xy: tuple[float, float],
    column_widths: list[float],
    column_margins: list[float],
    row_heights: list[float],
    row_margins: list[float],
    outer_style: Style | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

- `draw(...) -> Self`: Computes uniform column widths and row heights with `margin` gutters between cells (and around the perimeter when `outer_style` is provided).
- `draw_flexible(...) -> Self`: Uses explicit `column_widths` (length `num_column`), `column_margins` (length `num_column + 1`, including left and right outer margins), `row_heights` (length `num_row`), and `row_margins` (length `num_row + 1`, including bottom and top outer margins).

---

## 3. Production Example: Multi-Tier Cloud Software Architecture

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=110, height=75)

grid = GridLayout(
    num_column=4,
    num_row=4,
    style=Styles.Neutral.patch(shape_r=1.5),
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

# Row 3 (Top): Client & CDN Ingress (Hero layer)
grid.add(
    position=(0, 3),
    width=4,
    height=1,
    text="Edge Ingress: Cloudflare CDN & WAF Gateway",
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
# Row 2: Microservice Layer
grid.add(position=(0, 2), width=2, height=1, text="Order & Cart API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 2), width=1, height=1, text="Auth API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(3, 2), width=1, height=1, text="Notify", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
# Row 1: Persistence Tier
grid.add(position=(0, 1), width=1, height=1, text="Postgres", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(1, 1), width=1, height=1, text="Mongo", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 1), width=2, height=1, text="Redis Replication Cluster", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
# Row 0 (Bottom): Cloud Infrastructure
grid.add(
    position=(0, 0),
    width=4,
    height=1,
    text="Kubernetes Core Platform (AWS EKS Multi-AZ)",
    style=Styles.Neutral.patch(shape_r=1.5),
)

grid.draw(
    xy=(10, 10),
    width=90,
    height=55,
    margin=1.5,
    outer_style=Styles.MutedDashed.patch(shape_r=2.0),
)
save()
```
