# Drawlib Table SmartArt Guidelines (`lib-smartarts-table`)

`Table` renders 2D tabular data with fine-grained styling control over outer/inner borders, header cells, row headers, alternating even/odd rows, and individual cell ranges.

---

## 1. Architecture & Coordinate Mechanics

- **Anchor (`align`)**: Top-Left coordinate `xy=(x, y)` by default (`align="top_left"`), or `"bottom_left"` / `"center"`. Row `0` starts at the top edge of the table and subsequent rows step downward (`y - row_height`).
- **Data Shape**: 2D list of any serializable values (`list[list[Any]]`). Every value is converted via `str(val)`.
- **Sizing Modes** (both return `Self` for method chaining):
  - `draw(xy, width, height, data, align="top_left", scale=1.0) -> Self`: Uniform column widths (`width / num_cols`) and uniform row heights (`height / num_rows`), with optional proportional scaling around `xy`.
  - `draw_flexible(xy, column_widths, row_heights, data, align="top_left", scale=1.0) -> Self`: Explicit per-column widths (`list[float]`) and per-row heights (`list[float]`), with optional proportional scaling around `xy`.

---

## 2. Constructor & Style Methods

```python
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Primary,
    header_cell_style=Styles.PrimaryThin,
    header_text_style=Styles.PrimaryBold,
    border_style=Styles.MutedThin,
    has_header=True,
)
```

### Constructor Signature

```python
Table(
    *,
    cell_style: Style,
    text_style: Style,
    header_cell_style: Style,
    header_text_style: Style,
    border_style: Style,
    has_header: bool = True,
)
```

- `cell_style`: Default cell style (uses `cell_style.shape_fill_color` for cell backgrounds).
- `text_style`: Default text style for data cell contents.
- `header_cell_style`: Default style for header cells (`row 0` when `has_header=True`, using `header_cell_style.shape_fill_color`).
- `header_text_style`: Default text style for header cell contents (`row 0` when `has_header=True`).
- `border_style`: Default line style applied to all outer and inner borders upon initialization.
- `has_header`: Whether `row 0` is initialized with `header_cell_style` and `header_text_style`. Defaults to `True`.
- `reset_styles() -> None`: Resets all cell and border style overrides back to the initial constructor settings.

### Cell Styling Methods & Ordering Rule

Cell styles are evaluated in the exact sequential order they were registered:

- `set_style_cell_evenodd(even_color: ColorType, even_text_style: Style, odd_color: ColorType, odd_text_style: Style) -> None`:
  Applies alternating background colors and text styles to even (`0, 2, 4, ...`) and odd (`1, 3, 5, ...`) rows.
- `set_style_cell_header(background_color: ColorType, text_style: Style) -> None`:
  Applies background color and text style exclusively to column headers (`rows=[0]`).
- `set_style_cell_rowheader(background_color: ColorType, text_style: Style) -> None`:
  Applies background color and text style exclusively to row headers (`columns=[0]`).
- `set_style_cell_headers(background_color: ColorType, text_style: Style) -> None`:
  Applies background color and text style to both `column 0` and `row 0`.
- `set_style_cell(background_color: ColorType, text_style: Style, rows: list[int] | None = None, columns: list[int] | None = None) -> None`:
  Targets specific 0-indexed `rows` and/or `columns` (if `rows=None`, applies to all rows; if `columns=None`, applies to all columns).

> **Important — `set_style_cell_evenodd()` vs. `set_style_cell_header()` Ordering**:
> Because `Table` applies cell style rules in registration order and `0` is an even index, calling `set_style_cell_evenodd(...)` **overwrites `row 0`** with `even_color` and `even_text_style`. Always call `set_style_cell_header(...)` (or `set_style_cell(..., rows=[0])`) **after** `set_style_cell_evenodd(...)` so the header row retains its header styling!

### Border Styling Method

```python
table.set_style_border(
    top: Style | None = None,
    top2: Style | None = None,
    bottom: Style | None = None,
    left: Style | None = None,
    left2: Style | None = None,
    right: Style | None = None,
    between_columns: Style | None = None,
    between_rows: Style | None = None,
) -> None
```

- `top`, `bottom`, `left`, `right`: Perimeter border lines.
- `top2`: Horizontal divider line directly beneath the header row (between `row 0` and `row 1`).
- `left2`: Vertical divider line directly to the right of the row header column (between `col 0` and `col 1`).
- `between_columns`: Vertical separator lines between inner columns.
- `between_rows`: Horizontal separator lines between inner rows.
- *(Note: Calling `set_style_border(...)` replaces all border slots; pass explicit `Style` objects for each border you want drawn, and `None` to hide specific grid lines.)*

### Drawing Signatures

```python
table.draw(
    xy: tuple[float, float],
    width: float,
    height: float,
    data: list[list[Any]],
    align: Literal["top_left", "bottom_left", "center"] = "top_left",
    scale: float = 1.0,
) -> Self

table.draw_flexible(
    xy: tuple[float, float],
    column_widths: list[float],
    row_heights: list[float],
    data: list[list[Any]],
    align: Literal["top_left", "bottom_left", "center"] = "top_left",
    scale: float = 1.0,
) -> Self
```

*(Note: `align` and `scale` are positional-or-keyword parameters in `Table.draw()` and `Table.draw_flexible()`—there is no `*` separator before `align`.)*

---

## 3. Production Example: Microservice SLA & Availability Table

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

setup(width=120, height=65)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Primary.patch(text_color=Colors.Dark, text_size=10.0),
    header_cell_style=Styles.Primary.patch(shape_fill_color=Colors.Dark),
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.5),
)

# 1. Apply alternating row colors first
table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Primary.patch(text_color=Colors.Dark, text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Primary.patch(text_color=Colors.Dark, text_size=10.0),
)

# 2. Re-apply header row style AFTER set_style_cell_evenodd so row 0 is not overwritten
table.set_style_cell_header(
    background_color=Colors.Dark,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

# 3. Highlight specific SLA cell (Row 2, Column 3)
table.set_style_cell(
    background_color=CssColors.PaleGreen,
    text_style=Styles.Primary.patch(text_color=CssColors.ForestGreen, text_size=10.0),
    rows=[2],
    columns=[3],
)

table.set_style_border(
    top=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.5),
    top2=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.0),
    bottom=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.5),
    between_rows=Styles.Primary.patch(line_color=CssColors.LightGray, line_width=0.5),
)

sla_data = [
    ["Service Name", "Protocol", "P99 Latency", "Availability", "Tier"],
    ["Auth Gateway", "gRPC / HTTPS", "18 ms", "99.99 %", "Tier 0"],
    ["Order Engine", "gRPC", "8 ms", "99.999 %", "Tier 0"],
    ["Notification", "Async Kafka", "120 ms", "99.9 %", "Tier 2"],
    ["Analytics", "Batch REST", "450 ms", "99.5 %", "Tier 3"],
]
table.draw_flexible(
    xy=(10, 55),
    column_widths=[30, 22, 20, 18, 10],
    row_heights=[8, 8, 8, 8, 8],
    data=sla_data,
    align="top_left",
)
save()
```
