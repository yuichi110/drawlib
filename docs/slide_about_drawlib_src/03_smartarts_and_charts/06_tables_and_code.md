::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Data Matrices & Embedded Code (`Table` & `SourceCode`)
:::

::: block (80, 140) (680, 840) compact
## Tabular Precision & Vector Syntax Highlighting

### 1. `Table` — Fine-Grained Matrix Styling
- **Flexible Sizing**: `draw(xy, width, height, data)` distributes columns evenly, while `draw_flexible(xy, column_widths, row_heights, data)` gives exact per-column and per-row dimensions.
- **Zebra & Cell Highlighting**:
  - `set_style_cell_evenodd(even_color, even_text_style, odd_color, odd_text_style)` applies alternating row stripes.
  - `set_style_cell(background_color, text_style, rows=[...], columns=[...])` highlights specific SLA breaches or target cells.
- **Selective Borders**: `set_style_border(top=..., top2=..., bottom=..., between_rows=...)` controls perimeter and inner rules independently.

### 2. `SourceCode` — Vector Code Containers
- Renders Pygments-tokenized code directly onto the canvas as crisp vector glyphs and rounded containers (`show_linenum=True`).
- Built-in themes (`"dark"`, `"monokai"`, `"default"`, `"google"`, `"monochrome"`) and CJK-aware monospace fonts (`font_lang="en" | "ja"`).
:::

::: block (800, 140) (1040, 840)
```drawlib file:tables_and_code.svg
from drawlib.canvas import clear, save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles, Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

clear()
setup(width=104, height=84)

# 1. Top Panel: Microservice SLA & Availability Table
rectangle((52, 62), width=100, height=40, style=Styles.MutedOutline.patch(shape_r=2.0))
text(
    (6, 78.5),
    "Production Microservice SLA Matrix — Table.draw_flexible()",
    style=Styles.DarkBold.patch(text_size=9.5, halign="left"),
)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=8.2),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=8.5),
    border_style=Styles.MutedThin,
    has_header=True,
)
table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=8.2),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=8.2),
)
# Highlight Tier-0 99.999% SLA cell (Row 2, Column 3)
table.set_style_cell(
    background_color=CssColors.PaleGreen,
    text_style=Styles.DarkBold.patch(text_color=CssColors.ForestGreen, text_size=8.2),
    rows=[2],
    columns=[3],
)
# Highlight latency warning cell (Row 4, Column 2)
table.set_style_cell(
    background_color=CssColors.MistyRose,
    text_style=Styles.DarkBold.patch(text_color=CssColors.FireBrick, text_size=8.2),
    rows=[4],
    columns=[2],
)
table.set_style_border(
    top=Styles.DarkBold.patch(line_width=1.4),
    top2=Styles.DarkBold.patch(line_width=1.0),
    bottom=Styles.DarkBold.patch(line_width=1.4),
    between_rows=Styles.MutedThin,
)

sla_data = [
    ["Service Name", "Protocol", "P99 Latency", "Availability SLA", "Tier"],
    ["Edge Auth Gateway", "gRPC / HTTP3", "12 ms", "99.99 %", "Tier 0"],
    ["Ledger Core Engine", "gRPC (mTLS)", "6 ms", "99.999 %", "Tier 0"],
    ["Event Dispatcher", "Kafka Stream", "45 ms", "99.95 %", "Tier 1"],
    ["Batch Analytics", "REST / Parquet", "380 ms", "99.50 %", "Tier 2"],
]
table.draw_flexible(
    xy=(6, 75),
    column_widths=[26, 20, 16, 18, 12],
    row_heights=[6.0, 5.8, 5.8, 5.8, 5.8],
    data=sla_data,
)

# 2. Bottom Panel: Embedded Vector SourceCode Block
text(
    (6, 37.5),
    "Embedded Vector Code Container — SourceCode.draw(show_linenum=True)",
    style=Styles.DarkBold.patch(text_size=9.5, halign="left"),
)

envoy_snippet = """# Envoy Rate-Limit & Circuit-Breaker Filter Config
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: ledger-core-circuit-breaker
  namespace: prod-mesh
spec:
  workloadSelector:
    labels:
      app: ledger-core
      tier: tier-0
  configPatches:
    - applyTo: CLUSTER
      patch:
        operation: MERGE
        value:
          circuit_breakers:
            thresholds:
              - max_connections: 4096
                max_pending_requests: 1024"""

code_styles = SourceCodeStyles.get("dark", font_lang="en", text_size=7.4)
SourceCode.draw(
    xy=(6, 34),
    width=92,
    code=envoy_snippet,
    styles=code_styles,
    code_lang="yaml",
    show_linenum=True,
)

save()
```
:::

::: note
- Technical presentations frequently need to pair operational data tables with configuration snippets or code blocks right inside a diagram canvas.
- **Top (`Table`)**: Demonstrates `draw_flexible()` with custom column widths (`[26, 20, 16, 18, 12]`), alternating row shading via `set_style_cell_evenodd()`, and targeted cell highlights via `set_style_cell()`—marking the `99.999%` SLA cell in green and the `380 ms` batch latency cell in rose.
- **Bottom (`SourceCode`)**: Renders syntax-highlighted YAML directly into the vector SVG canvas with line numbers (`show_linenum=True`) and dark theme styling (`SourceCodeStyles.get("dark")`).
:::
