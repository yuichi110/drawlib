# 7. SmartArts: 18 Structured Visual Components

Instead of calculating manual rectangle coordinates and text offsets for common engineering visuals, `drawlib.smartarts` provides **18 high-level components** that automate geometry, alignment, borders, and typography out of the box. Every SmartArt shares the same `GoogleStyles` design tokens and Cartesian canvas, letting you compose KPI executive headers, pipelines, SLA tables, and repository trees inside a single figure.

```drawlib align=center code=fold file=smartarts_chevron_kpi.png caption="Figure 7.1: Executive Release Dashboard Combining KpiCards and ChevronProcess"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import ChevronProcess, KpiCards
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=66)

text(
    (74.0, 60.5),
    "v0.3.10 Release Readiness & Publishing Pipeline",
    style=Styles.DarkBold.patch(text_size=12.5),
)

kpi = KpiCards(
    style=Styles.Neutral.patch(shape_r=1.8),
    metric_style=Styles.DarkBold.patch(text_size=15.5),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=10.0),
    accent_style=Styles.SecondaryFlat,
    icon_style=Styles.PrimaryBold,
    accent_position="top_bar",
    metric_layout="top_stack",
    spacing=3.5,
)
kpi.add(
    "99.99%",
    "Availability SLA",
    "Active-active multi-region",
    icon=phosphor.shield_check,
)
kpi.add(
    "11.4 ms",
    "Edge P99 Latency",
    "v0.3.10 zero-copy router",
    icon=phosphor.lightning,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    metric_style=Styles.WhiteBold.patch(text_size=15.5),
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=10.0),
    accent_style=Styles.WhiteFlat,
    icon_style=Styles.WhiteBold,
)
kpi.add(
    "4.2x",
    "Build Throughput",
    "Incremental SQLite cache",
    icon=phosphor.cpu,
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    accent_style=Styles.PrimaryFlat,
)
kpi.draw(xy=(6.0, 29.0), width=136.0, height=26.0, columns=3)

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.8),
    description_style=Styles.Muted.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
pipeline.add("1. Author", description="Python + Markdown")
pipeline.add("2. Grid Review", description="drawlib show -g")
pipeline.add(
    "3. Build Docs",
    description="HTML / PDF / Office",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.8),
    description_style=Styles.White.patch(text_size=10.0),
)
pipeline.add(
    "4. Publish",
    description="CI / Static Portal",
    style=Styles.SecondaryNeutral,
)
pipeline.draw(xy=(6.0, 7.0), width=136.0, height=16.5)

save()
```

## 7.1 Complete Catalog of 18 SmartArts & Coordinate Anchors

Because Drawlib uses a bottom-left `(0, 0)` Cartesian canvas where `+Y` points upward, knowing each SmartArt's default `.draw(xy=...)` coordinate anchor guarantees one-shot placement without trial-and-error shifts:

- **Bottom-Left `(x0, y0)`**: Most rectangular containers (`ChevronProcess`, `KpiCards`, `GeoMap`, `*Calendar`, etc.) start at `(x0, y0)` and extend rightward (`+X`) and upward (`+Y`).
- **Top-Left `(x0, y_top)`**: Reading-order components (`Table`, `BulletPoints`, `SourceCode`, `TreeNode`) start at `(x0, y_top)` and grow downward (`-Y`), so always pass an upper `y_top` coordinate.
- **Center `(cx, cy)`**: Radial layouts (`Cycle`, `MindMapNode`) expand outward around `(cx, cy)`.

### 7.1.1 Processes, Cycles & Timelines

| Component | Item / Helper Models | Default `.draw(xy=...)` Anchor | Primary Engineering Use Cases |
| :--- | :--- | :--- | :--- |
| **`ChevronProcess`** | `ChevronItem` | **Bottom-Left** (`align="bottom_left"`) | CI/CD pipelines, ETL workflows, phased rollouts (`flat_left_end=True`) |
| **`Cycle`** | `CycleItem`, `CycleCenter` | **Center** (`align="center"`) | PDCA feedback loops, OAuth token refresh cycles, SRE incident loops |
| **`Roadmap`** | `RoadmapItem` | **Bottom-Left** (`align="bottom_left"`) | Quarterly release milestones, migration timelines, postmortem chronicles |

### 7.1.2 Cards, Grids & Summaries

| Component | Item / Helper Models | Default `.draw(xy=...)` Anchor | Primary Engineering Use Cases |
| :--- | :--- | :--- | :--- |
| **`KpiCards`** (`KpiCard`) | `KpiCardItem` | **Bottom-Left** (`align="bottom_left"`) | Executive SLA metrics, latency targets, benchmark summary headers |
| **`CardList`** | `CardListItem` | **Bottom-Left** (`align="bottom_left"`) | Vertical or horizontal feature cards with optional `->` step connectors |
| **`BoxList`** | `BoxListItem` | **Bottom-Left** (`align="bottom_left"`) | Contiguous service strips, protocol frame headers, compact status blocks |
| **`GridLayout`** | `GridItem` | **Bottom-Left** (`align="bottom_left"`) | Multi-row/column spanning architecture matrices (`row=0` at bottom) |
| **`Pyramid`** | `PyramidItem` | **Bottom-Left** (`align="bottom_left"`) | Testing pyramids, storage/cache hierarchies, defense-in-depth layers |
| **`Panel`** | — | **Bottom-Left** (`align="bottom_left"`) | Titled container frames (`"filled"`, `"underline"`, `"floating"`, `"window"`) |

### 7.1.3 Tables, Text & Code Blocks

| Component | Item / Helper Models | Default `.draw(xy=...)` Anchor | Primary Engineering Use Cases |
| :--- | :--- | :--- | :--- |
| **`Table`** | — | **Top-Left** (`align="top_left"`) | Service SLA matrices, feature comparisons, quota schedules (`draw_flexible`) |
| **`BulletPoints`** | `BulletPointItem` | **Top-Left** *(fixed `(x, y)`)* | Architecture takeaways, design review checklists, slide callouts |
| **`SourceCode`** | `SourceCodeStyles`, `sourcecode` | **Top-Left** (`align="top_left"`) | Vector syntax-highlighted Python/YAML/JSON snippets inside diagrams |

### 7.1.4 Hierarchies & Mind Maps

| Component | Item / Helper Models | Default `.draw(xy=...)` Anchor | Primary Engineering Use Cases |
| :--- | :--- | :--- | :--- |
| **`TreeNode`** | — | **Top-Left** *(fixed `(x, y)`)* | Monorepo directory layouts, package hierarchies, CLI command trees |
| **`MindMapNode`** | — | **Center** *(fixed `(cx, cy)`)* | 4-way radial system taxonomies, domain decompositions, org charts |

### 7.1.5 Geographic & Temporal

| Component | Item / Helper Models | Default `.draw(xy=...)` Anchor | Primary Engineering Use Cases |
| :--- | :--- | :--- | :--- |
| **`GeoMap`** | — | **Bottom-Left** (`align="bottom_left"`) | Multi-region cloud deployments (`World`, `Countries`, `Cities`, `lonlat_to_xy`) |
| **`MonthCalendar`** | `CalendarItem` | **Bottom-Left** (`align="bottom_left"`) | 7-column monthly or multi-week release schedules (`"YYYY-MM-DD"`) |
| **`WeekCalendar`** | `CalendarItem` | **Bottom-Left** (`align="bottom_left"`) | N-day hourly sprint and maintenance windows (`"YYYY-MM-DD HH:MM"`) |
| **`DayCalendar`** | `CalendarItem` | **Bottom-Left** (`align="bottom_left"`) | Single-day incident timelines and minute-level change runbooks |

> **Tip — Aligning Top-Left and Bottom-Left Components Side by Side**: To align a `Table` or `TreeNode` of height `H` with a Bottom-Left box sitting at `(x0, y_bottom)`, pass `xy=(x0, y_bottom + H)` as the Top-Left anchor (or pass `align="bottom_left"` directly on `Table` and `SourceCode`).

## 7.2 Top-Left Composition: Pairing Table and TreeNode

`Table` and `TreeNode` both default to **Top-Left** `(x0, y_top)` coordinates, making them natural partners for side-by-side specification figures:

- **`Table` Styling Order Rule**: `Table` evaluates cell rules in registration order. Because `0` is an even row index, always call `set_style_cell_evenodd(...)` **before** `set_style_cell_header(...)` so the header row (`row 0`) retains its dark/accent banner, then highlight individual target cells last via `set_style_cell(..., rows=[r], columns=[c])`.
- **`TreeNode` Cascading & Icons**: Define all five layout attributes (`text_style`, `line_style`, `line_horizontal_margin`, `line_horizontal_length`, `line_vertical_margin`) on the root `TreeNode`—descendants inherit them automatically. Attach vector `phosphor` icons via `TreeNode.register_drawing_item(...)` and `.set_drawing_item(name)`. Pass pre-built `TreeNode` children via `children=[...]`, or append string labels dynamically via `node.add("filename.py")`.

```drawlib align=center code=fold file=smartarts_table_tree.png caption="Figure 7.2: Side-by-Side Top-Left Composition Pairing a Styled Table and Project TreeNode"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Table, TreeNode
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=148, height=64)

text(
    (43.0, 56.5),
    "Archetype Output Matrix (Table)",
    style=Styles.DarkBold.patch(text_size=11.5),
)
text(
    (114.5, 56.5),
    "Scaffolded Project Tree (TreeNode)",
    style=Styles.DarkBold.patch(text_size=11.5),
)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.2),
    header_cell_style=Styles.DarkFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=Colors.Gray1,
    even_text_style=Styles.Dark.patch(text_size=10.2),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.2),
)
table.set_style_cell_header(
    background_color=Colors.Gray8,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.2),
    rows=[1],
    columns=[2],
)
table.set_style_border(
    top=Styles.DarkBold.patch(line_width=1.4),
    top2=Styles.DarkBold.patch(line_width=1.0),
    bottom=Styles.DarkBold.patch(line_width=1.4),
    between_rows=Styles.MutedThin.patch(line_width=0.6),
)

matrix = [
    ["Archetype", "Primary Output", "Office / Print"],
    ["doc", "Chapter HTML", "PDF + DOCX"],
    ["site", "Multi-Page Docs", "llms.txt + SEO"],
    ["catalog", "Searchable Ref", "JSON Index"],
    ["slide", "16:9 Web Deck", "PDF + PPTX"],
]
table.draw_flexible(
    xy=(7.0, 51.5),
    column_widths=[20.0, 28.0, 24.0],
    row_heights=[8.6, 8.6, 8.6, 8.6, 8.6],
    data=matrix,
    align="top_left",
)

rectangle(
    (114.5, 30.0),
    width=53.0,
    height=43.0,
    style=Styles.Neutral.patch(shape_r=2.0),
)

TreeNode.register_drawing_item(
    name="ch07_dir",
    location="before",
    padding_width=4.4,
    function=phosphor.folder,
    style=Styles.PrimaryBold,
    args={"width": 3.2},
)
TreeNode.register_drawing_item(
    name="ch07_py",
    location="before",
    padding_width=4.4,
    function=phosphor.file_py,
    style=Styles.SecondaryBold,
    args={"width": 3.2},
)
TreeNode.register_drawing_item(
    name="ch07_md",
    location="before",
    padding_width=4.4,
    function=phosphor.file_text,
    style=Styles.DarkBold,
    args={"width": 3.2},
)

root = TreeNode(
    "quickstart/",
    text_style=Styles.DarkBold.patch(text_size=10.2),
    line_style=Styles.Muted.patch(line_width=1.1),
    line_horizontal_margin=2.8,
    line_horizontal_length=2.8,
    line_vertical_margin=5.4,
    children=[
        TreeNode(
            "en/",
            text_style=Styles.DarkBold.patch(text_size=10.2),
            children=[
                TreeNode("00_cover.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch07_md"),
                TreeNode("07_smartarts.md", text_style=Styles.PrimaryBold.patch(text_size=10.0)).set_drawing_item("ch07_md"),
            ],
        ).set_drawing_item("ch07_dir"),
        TreeNode(
            "ja/",
            text_style=Styles.DarkBold.patch(text_size=10.2),
            children=[
                TreeNode("07_smartarts.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch07_md"),
            ],
        ).set_drawing_item("ch07_dir"),
    ],
).set_drawing_item("ch07_dir")
root.add("styles.py", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch07_py")

root.draw(xy=(91.5, 47.0))

save()
```

## 7.3 Step-by-Step Slide & Animation Builds with `show=False`

Every stateful SmartArt follows a four-phase lifecycle (**Instantiate -> Register via `.add()` -> Mutate `.items` / `.children` -> Render via `.draw()`**). Each registered item or node exposes a boolean `show: bool = True` flag (`ChevronItem`, `KpiCardItem`, `CardListItem`, `BoxListItem`, `CycleItem`, `GridItem`, `PyramidItem`, `RoadmapItem`, `BulletPointItem`, `CalendarItem`, `TreeNode`, and `MindMapNode`).

Setting `item.show = False` (or passing `show=False` in `.add(...)`) hides that specific step while **preserving the exact bounding widths, column positions, orbit angles, and vertical row spacing of all sibling items**. This makes progressive slide builds and multi-frame `drawlib.anim` animations effortless—earlier steps never jump or stretch as later steps appear:

```python
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=120, height=32)

flow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    flat_left_end=True,
)
flow.add("1. Ingest", description="Parquet Stream")
flow.add(
    "2. Validate",
    description="Schema Check",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
# Hidden in Frame 1, yet Steps 1 & 2 keep their exact 4-column widths!
step3 = flow.add("3. Enrich", description="Vector Join", show=False)
step4 = flow.add("4. Serve", description="Low-Latency API", show=False)

flow.draw(xy=(8.0, 8.0), width=104.0, height=16.0)
save()
```

Query any SmartArt's full constructor reference on demand via `uv run drawlib rules show lib-smartarts-overview` (or component manuals such as `lib-smartarts-calendar`, `lib-smartarts-geomap`, and `lib-smartarts-source-code`).
