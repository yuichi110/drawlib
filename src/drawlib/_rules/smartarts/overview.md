# Drawlib SmartArts Overview Guidelines (`lib-smartarts-overview`)

The `drawlib.smartarts` module provides high-level graphical components designed for **"Illustration as Code."** These components automate the layout, geometry, text positioning, and styling of structured diagrams—including tabular datasets, directory trees, multi-directional mindmaps, process pipelines, cyclical workflows, matrix grids, tiered pyramids, bulleted lists, syntax-highlighted source code, geographical vector maps, KPI metric cards, feature card lists, milestone roadmaps, titled container panels, and schedule calendars.

---

## 1. Public Exports & Imports (`drawlib.smartarts`)

All **33** SmartArt classes, mutable item/configuration models, and helper function aliases are exported directly from `drawlib.smartarts`:

```python
from drawlib.smartarts import (
    # Primary SmartArt Components (19)
    BoxList,
    BulletPoints,
    CardList,
    ChevronProcess,
    Cycle,
    DayCalendar,
    GeoMap,
    GridLayout,
    KpiCard,
    KpiCards,
    MindMapNode,
    MonthCalendar,
    Panel,
    Pyramid,
    Roadmap,
    SourceCode,
    Table,
    TreeNode,
    WeekCalendar,
    # Mutable Item & Style Models (12)
    BoxListItem,
    BulletPointItem,
    CalendarItem,
    CardListItem,
    ChevronItem,
    CycleCenter,
    CycleItem,
    GridItem,
    KpiCardItem,
    PyramidItem,
    RoadmapItem,
    SourceCodeStyles,
    # Helper Function Aliases (2)
    get_source_code_styles,
    sourcecode,
)
```

Common auxiliary imports for canvas setup, styling, and colors:

```python
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.styles import Colors, Styles
from drawlib.types import Style
```

---

## 2. Coordinate Anchor Conventions

Understanding anchor points is essential when positioning or combining multiple SmartArts on a canvas:

- **Top-Left Anchored (`align="top_left"` default)**:
  - **`Table`** (also supports `align="bottom_left"` and `align="center"`)
  - **`SourceCode`** / **`sourcecode`** (also supports `align="bottom_left"` and `align="center"`)
  - **`TreeNode`** (fixed top-left `(x, y)`)
  - **`BulletPoints`** (fixed top-left `(x, y)`)
  - *Geometry*: You specify the top-left coordinate `(x, y)`; elements flow rightward (`+x`) and downward (`-y`).
- **Bottom-Left Anchored (`align="bottom_left"` default)**:
  - **`BoxList`**, **`ChevronProcess`**, **`GridLayout`**, **`Pyramid`**, **`GeoMap`**, **`KpiCards`** (`KpiCard`), **`CardList`**, **`Roadmap`**, **`Panel`** (all also support `align="center"`)
  - **`MonthCalendar`**, **`WeekCalendar`**, **`DayCalendar`** (also support `align="center"` and `align="top_left"`)
  - *Geometry*: You specify the bottom-left coordinate `(x, y)` of the bounding box; elements extend rightward (`+x`) and upward (`+y`).
- **Center Anchored (`(cx, cy)` default)**:
  - **`MindMapNode`** (fixed root node center `(cx, cy)`)
  - **`Cycle`** (`align="center"` default anchors orbit center `(cx, cy)`; also supports `align="bottom_left"`)
  - *Geometry*: You specify the center coordinate `(cx, cy)`; elements expand radially or symmetrically around the center.

### Coordinate Normalization Formulas

To align components of size `(W, H)` on the same canvas grid, either pass `align="bottom_left"` / `align="center"` directly to `draw()`, or convert between Top-Left `(left_x, top_left_y)`, Bottom-Left `(left_x, bottom_y)`, and Center `(center_x, center_y)` anchors:

```python
center_x = left_x + W / 2.0
center_y = bottom_y + H / 2.0

top_left_x = left_x
top_left_y = bottom_y + H
```

| Component Group | Default `xy` Meaning | Supported `align` Options | To Align with Canvas Bottom-Left `(X, Y)` |
| :--- | :--- | :--- | :--- |
| **`Table`**, **`SourceCode`** | Top-Left `(x, y)` | `"top_left"`, `"bottom_left"`, `"center"` | Pass `align="bottom_left"` or `(X, Y + H)` |
| **`TreeNode`**, **`BulletPoints`** | Top-Left `(x, y)` | *(Fixed Top-Left)* | Pass `(X, Y + H)` |
| **`BoxList`**, **`ChevronProcess`**, **`GridLayout`**, **`Pyramid`**, **`GeoMap`**, **`KpiCards`**, **`CardList`**, **`Roadmap`**, **`Panel`** | Bottom-Left `(x, y)` | `"bottom_left"`, `"center"` | Pass `(X, Y)` directly |
| **`MonthCalendar`**, **`WeekCalendar`**, **`DayCalendar`** | Bottom-Left `(x, y)` | `"bottom_left"`, `"center"`, `"top_left"` | Pass `(X, Y)` directly |
| **`MindMapNode`** | Root Center `(cx, cy)` | *(Fixed Root Center)* | Pass `(X + W/2, Y + H/2)` |
| **`Cycle`** | Orbit Center `(cx, cy)` | `"center"`, `"bottom_left"` | Pass `align="bottom_left"` or `(X + R, Y + R)` |

---

## 3. Unified Component Lifecycle (`add()`, `.items`, `show`, `scale`, & Method Chaining)

Stateful SmartArts follow a unified 4-phase lifecycle (**1. Instantiate -> 2. Register via `add()` -> 3. Mutate State -> 4. Render via `draw()`**):

1. **Standardized Registration (`add(..., show=True)`) & `.items` Inspection**:
   - Every item-based SmartArt (`BoxList`, `BulletPoints`, `CardList`, `ChevronProcess`, `Cycle`, `GridLayout`, `Pyramid`, `KpiCards`, `Roadmap`, `MonthCalendar`, `WeekCalendar`, `DayCalendar`) uses `.add(...)` to register elements, returns the newly created public item model (`BoxListItem`, `BulletPointItem`, `CardListItem`, `ChevronItem`, `CycleItem`, `GridItem`, `PyramidItem`, `KpiCardItem`, `RoadmapItem`, `CalendarItem`), and exposes all registered items via the **`.items`** property.
   - Hierarchical components (`TreeNode`, `MindMapNode`) return the newly created child node from `.add(text, ...)` and expose child nodes via **`.children`**.
   - `Cycle` also exposes its central hub configuration via **`.center`** (`CycleCenter`).
2. **Layout-Preserving Visibility (`item.show`)**:
   - Every item and node exposes `item.show: bool = True`. Setting `item.show = False` skips drawing that specific element while **keeping the overall component geometry, item widths, orbit angles, and grid/tree coordinates completely unchanged** (ideal for `drawlib.anim` step-by-step reveals).
3. **Deferred Style & Text Evaluation**:
   - Item attributes (`item.style`, `item.text_style`, `item.text`, `item.description`, etc.) are resolved lazily inside `draw()`. Mutating an item's style or text between `draw()` calls immediately reflects on the next render without reconstructing the component.
4. **Proportional Scaling (`scale: float = 1.0`) & `.draw() -> Self`**:
   - Every `.draw(...)` and `.draw_flexible(...)` method accepts `scale: float = 1.0` (scaling all shapes, margins, corner radii, line widths, and font sizes relative to `xy`) and **returns `Self`** (or `SourceCode` for `SourceCode.draw()`) for fluent method chaining.

---

## 4. Decision Matrix & Routing Table to Component Rule Topics

Query the specific component rule manual via `uv run drawlib rules show <rule-topic>` when authoring diagrams with that SmartArt:

| Rule Topic | Component(s) & Item Models | Default Anchor | Layout Direction | Typical Architecture & Documentation Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **`lib-smartarts-table`** | `Table` | Top-Left (`align="top_left"`) | Downward & Rightward 2D grid | Service matrices, SLA comparisons, feature tables |
| **`lib-smartarts-tree`** | `TreeNode` | Top-Left `(x, y)` | Downward orthogonal tree lines | Monorepo directories, file trees, package layouts |
| **`lib-smartarts-mindmap`** | `MindMapNode` | Center `(cx, cy)` | Radial 4-way (`"bottom"`, `"top"`, `"left"`, `"right"`) | Architecture overviews, decision trees, org charts |
| **`lib-smartarts-box-list`** | `BoxList`, `BoxListItem` | Bottom-Left (`align="bottom_left"`) | `"left"`, `"right"`, `"bottom"`, `"top"` | Contiguous microservice cards, pipeline stages, status badges |
| **`lib-smartarts-bullet-points`** | `BulletPoints`, `BulletPointItem` | Top-Left `(x, y)` | Downward indented list | Architecture takeaways, RFC summaries, checklists |
| **`lib-smartarts-chevron-process`** | `ChevronProcess`, `ChevronItem` | Bottom-Left (`align="bottom_left"`) | Horizontal interlocking chevrons | CI/CD pipelines, ETL workflows, order lifecycles |
| **`lib-smartarts-cycle`** | `Cycle`, `CycleItem`, `CycleCenter` | Center (`align="center"`) | Radial circular orbit + optional hub | PDCA DevOps loops, token refresh cycles, state loops |
| **`lib-smartarts-grid-layout`** | `GridLayout`, `GridItem` | Bottom-Left (`align="bottom_left"`) | Multi-column/row spanning matrix | Multi-tier architecture layers, dashboard panels |
| **`lib-smartarts-pyramid`** | `Pyramid`, `PyramidItem` | Bottom-Left (`align="bottom_left"`) | `"bottom"`, `"top"`, `"left"`, `"right"` | Defense-in-depth, testing pyramid, memory hierarchies |
| **`lib-smartarts-source-code`** | `SourceCode`, `SourceCodeStyles`, `sourcecode`, `get_source_code_styles` | Top-Left (`align="top_left"`) | Vector syntax-highlighted code box | Embedded YAML/JSON configs, code samples, API payloads |
| **`lib-smartarts-geomap`** | `GeoMap` (`World`, `Countries`, `Cities`) | Bottom-Left (`align="bottom_left"`) | Equirectangular vector map | Multi-region cloud topology, country/city territory maps |
| **`lib-smartarts-kpi-cards`** | `KpiCards` (`KpiCard`), `KpiCardItem` | Bottom-Left (`align="bottom_left"`) | Vertical stack (`columns=1`) or grid (`columns>=2`) | SLA/latency metrics, executive summary KPIs, spec highlights |
| **`lib-smartarts-card-list`** | `CardList`, `CardListItem` | Bottom-Left (`align="bottom_left"`) | `"vertical"` or `"horizontal"` (optional `->` arrows) | Layered feature cards, numbered forensic steps, workflow cards |
| **`lib-smartarts-roadmap`** | `Roadmap`, `RoadmapItem` | Bottom-Left (`align="bottom_left"`) | `"vertical"` (straight/curved) or `"horizontal"` (alternating) | Release timelines, migration roadmaps, incident chronicles |
| **`lib-smartarts-panel`** | `Panel` | Bottom-Left (`align="bottom_left"`) | `"filled"`, `"underline"`, `"floating"`, `"window"` header | Titled container frames, comparison columns, window panels |
| **`lib-smartarts-calendar`** | `MonthCalendar`, `WeekCalendar`, `DayCalendar`, `CalendarItem` | Bottom-Left (`align="bottom_left"`) | 7-col month grid, N-day hourly grid, or vertical/horizontal day timeline | Monthly release schedules, sprint calendars, incident timelines |

---

## 5. Multi-Component Dashboard Integration Example

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess, SourceCode, SourceCodeStyles, Table
from drawlib.styles import Styles

setup(width=120, height=80)

# 1. Top Section: Pipeline Status (Bottom-Left anchored at y=62)
pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.add("1. Plan", description="Arch Review")
pipeline.add("2. Build", description="Docker Image")
pipeline.add("3. Test", description="E2E Verified", style=Styles.SecondaryNeutral)
pipeline.add(
    "4. Deploy",
    description="Production",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
    description_style=Styles.White.patch(text_size=9.5),
)
pipeline.draw(xy=(10, 62), width=100, height=12)

# 2. Bottom-Left Section: Service Matrix Table (Top-Left anchored at y=55)
table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.0),
    border_style=Styles.MutedThin,
)
table.draw(
    xy=(10, 55),
    width=50,
    height=45,
    data=[
        ["Service", "Status", "Latency"],
        ["User API", "Active", "12 ms"],
        ["Cart API", "Active", "15 ms"],
        ["Checkout", "Warning", "120 ms"],
        ["Billing", "Active", "45 ms"],
    ],
)

# 3. Bottom-Right Section: Active Schema Code Snippet (Top-Left anchored at y=50)
snippet = """# Migration Hook
def handle_event(ctx):
    ctx.metrics.inc("migrated")
    return ctx.forward()"""

code_styles = SourceCodeStyles.get("dark", font_lang="en", text_size=10.0)
SourceCode.draw(xy=(66, 50), width=48, code=snippet, styles=code_styles, code_lang="python", show_linenum=True)

save()
```

---

## 6. Common Troubleshooting & Pitfalls Across SmartArts

1. **Inverted `Table` or `GridLayout` Placement**:
   - `Table` and `SourceCode` default to `align="top_left"`. Passing `xy=(10, 10)` on an `80`-tall canvas draws downward past the bottom boundary (`y = 10 -> -35`). Pass a top-left `y` such as `(10, 70)` or pass `align="bottom_left"`.
   - `GridLayout` defaults to `align="bottom_left"`, and `row=0` is at the **bottom** (`row = num_row - 1` is at the top).
2. **`Table.set_style_cell_evenodd()` Overwriting Header Row (`row 0`)**:
   - `set_style_cell_evenodd()` applies alternating background and text styles across all rows, including `row 0`. Always call `set_style_cell_header()` (or `set_style_cell(..., rows=[0])`) **after** `set_style_cell_evenodd()` if you want to preserve a distinct header fill.
3. **`TreeNode.add()` and `MindMapNode.add()` Accept `text: str`**:
   - Calling `node.add(TreeNode("child"))` raises a validation error because `.add(text: str, ...)` constructs and appends a child node from a string label. Pre-built child node instances can only be passed via the constructor's `children=[...]` list.
4. **Missing Root Styles on `TreeNode` or `MindMapNode`**:
   - Root `TreeNode` requires `text_style`, `line_style`, `line_horizontal_margin`, `line_horizontal_length`, and `line_vertical_margin`.
   - Root `MindMapNode` requires `style`, `text_style`, and `line_style`.
5. **`GeoMap` Missing Dimensions or Pre-`draw()` Coordinate Queries**:
   - At least one of `width` or `height` must be passed to `GeoMap.draw()`.
   - `get_area_xy()` and `lonlat_to_xy()` must be called **after** `m.draw(...)` has executed. Use `m.get_areas()` to inspect valid area names before drawing.
