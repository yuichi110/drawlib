# Table Component

The `Table` component renders 2D tabular data, comparison matrices, and database schemas with fine-grained styling control over borders, headers, alternating even/odd row backgrounds, and specific cell highlights.

---

## 1. Quick Example: Service SLA & Status Matrix

```drawlib 650px center caption:"Service Status Matrix with Table"
from drawlib.canvas import setup
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles

setup(width=120, height=60)

table = Table(
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold,
    default_cell_style=Styles.White,
    default_text_style=Styles.PrimaryBold,
    border_style=Styles.PrimaryBold,
)

# Custom even/odd row styling using semantic tokens
table.set_style_cell_evenodd(
    even_color=Colors.Muted1,
    even_textstyle=Styles.PrimaryBold,
    odd_color=Colors.White,
    odd_textstyle=Styles.PrimaryBold,
)

# SLA highlight on HEALTHY rows using Success tint
table.set_style_cell(
    background_color=Colors.Success1,
    textstyle=Styles.SuccessBold,
    rows=[1, 2],
    columns=[3],
)

# SLA highlight on DEGRADED row using Danger tint
table.set_style_cell(
    background_color=Colors.Danger1,
    textstyle=Styles.DangerBold,
    rows=[3],
    columns=[3],
)

data = [
    ["Service Name", "Protocol", "P99 Latency", "Status"],
    ["Auth Gateway", "gRPC / HTTPS", "12 ms", "HEALTHY"],
    ["Order Service", "gRPC", "8 ms", "HEALTHY"],
    ["Payment Broker", "HTTPS", "45 ms", "DEGRADED"],
]

table.draw(xy=(10, 52), width=100, height=40, data=data)
```

---

## 2. Geometry & Coordinate Mechanics

- **Top-Left Anchor `(x, y)`**: The coordinate passed to `draw(xy=...)` specifies the **top-left corner** of the first table cell.
- **Downward Flow**: Rows move downward (`y - row_height`), while columns extend to the right (`x + col_width`).
- **Sizing Modes**:
  - `draw(xy, width, height, data)`: Distributes `width` and `height` equally across all columns and rows.
  - `draw_flexible(xy, column_widths, row_heights, data)`: Provides custom widths per column (e.g. `column_widths=[30, 20, 25, 25]`).

---

## 3. Styling API Reference

### Cell Styling Methods
- **`set_style_cell_header(background_color, textstyle)`**: Applies style exclusively to the header row (row 0).
- **`set_style_cell_rowheader(background_color, textstyle)`**: Applies style exclusively to the row header column (column 0).
- **`set_style_cell_evenodd(even_color, even_textstyle, odd_color, odd_textstyle)`**: Alternating zebra-stripe styles for even and odd data rows.
- **`set_style_cell(background_color, textstyle, rows=None, columns=None)`**: Applies styling to specific rows or columns.

### Border Styling Methods
- **`set_style_border(top=None, top2=None, bottom=None, left=None, right=None, between_columns=None, between_rows=None)`**:
  - `top`, `bottom`, `left`, `right`: Outer perimeter border lines.
  - `top2`: Sub-header horizontal divider line beneath row 0.
  - `between_rows`, `between_columns`: Inner grid divider lines.
