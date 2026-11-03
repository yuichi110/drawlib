# Drawlib Package Overview

Drawlib is a pure-Python library for **Illustration as Code** and **Illustrated Documentation as Code**, exposing 20 lazy-loaded top-level submodules (`PEP 562`) under `import drawlib` alongside dedicated `drawlib.charts` and `drawlib.diagrams` subpackages. Import domain symbols directly via `from drawlib.<module> import ...` or access package metadata from `drawlib`.

```drawlib align=center code=fold file=00_overview_hero.png caption="Drawlib Unified Python Package Architecture (import drawlib)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58, dpi=150)

# Outer package frame
rectangle((60, 29), width=112, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
phosphor.package((38.0, 48.5), width=4.4, style=Styles.DarkBold)
text(
    (63.5, 48.5),
    "Drawlib Package Architecture (v0.3.4)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# 1. Core Primitives & Styling
rectangle((23.5, 24), width=31, height=34, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.shapes((12.5, 35.5), width=4.2, style=Styles.DarkBold)
text((25.5, 35.5), "Core Primitives", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (23.5, 21.5),
    "canvas / shapes\nlines / text / images\nmath / styles / fonts",
    style=Styles.Dark.patch(text_size=10.0, text_line_spacing=1.35),
)

line((39.0, 24), (44.0, 24), arrow_head="->", style=Styles.DarkBold)

# 2. High-Level Components (Focal Hero)
rectangle((60, 24), width=32, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.graph((48.5, 35.5), width=4.2, style=Styles.WhiteBold)
text((62.0, 35.5), "High-Level API", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (60, 21.5),
    "smartarts / charts\ndiagrams / graph\nicons (34 suites)",
    style=Styles.White.patch(text_size=10.0, text_color=Colors.White, text_line_spacing=1.35),
)

line((76.0, 24), (81.0, 24), arrow_head="->", style=Styles.DarkBold)

# 3. Docs, Animation & CLI
rectangle((96.5, 24), width=31, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.terminal_window((86.0, 35.5), width=4.2, style=Styles.DarkBold)
text((98.5, 35.5), "Docs & CLI", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (96.5, 21.5),
    "anim / slide / tools\ndrawlib build & show\nHTML / PDF / PPTX",
    style=Styles.Dark.patch(text_size=10.0, text_line_spacing=1.35),
)

save()
```

### Package & Subpackage Re-exports (`__all__`)

Drawlib uses lazy module loading (`PEP 562`) so `import drawlib` incurs minimal startup overhead while keeping all public submodules discoverable via `dir()` and static type checkers:

| Package Namespace | Re-exported Submodules (`__all__`) |
| :--- | :--- |
| `drawlib` | `anim`, `canvas`, `charts`, `diagrams`, `fonts`, `graph`, `icons`, `images`, `lines`, `math`, `preset_colors`, `preset_styles`, `shapes`, `slide`, `smartarts`, `styles`, `text`, `tools`, `types`, `utils` |
| `drawlib.charts` | `area`, `bar`, `gantt`, `heatmap`, `line`, `pie`, `radar`, `scatter` (plus shared type `DrawDirection`) |
| `drawlib.diagrams` | `architecture`, `class_diagram`, `er`, `flow`, `sequence`, `state` |

### Complete API & CLI Reference Directory (29 Pages)

| Page | Module / Scope | Primary Contents |
| :--- | :--- | :--- |
| [00. Drawlib Package Overview](00_overview.md) | `drawlib`, `drawlib.utils`, `drawlib.charts`, `drawlib.diagrams` | Package constants, lazy submodule index, `drawlib.utils`, `DrawDirection` |
| [01. drawlib.canvas](01_canvas.md) | `drawlib.canvas` | Cartesian `(0, 0)` canvas lifecycle (`setup`, `save`, `clear`, `show`, `get_dimage`, `canvas`) |
| [02. drawlib.shapes](02_shapes.md) | `drawlib.shapes` | 43 geometric, arrow, 3D container, badge, and symbol primitives |
| [03. drawlib.lines & drawlib.text](03_lines_and_text.md) | `drawlib.lines`, `drawlib.text` | Straight, curved, Bézier, arc, and filleted lines; horizontal & vertical text |
| [04. drawlib.images & drawlib.math](04_images_and_math.md) | `drawlib.images`, `drawlib.math` | `image()`, immutable `Dimage` filters, subprocess `get_dimage_from_code()`, 2D geometry math |
| [05. drawlib.styles & drawlib.types](05_styles_and_types.md) | `drawlib.styles`, `drawlib.types` | Active `Styles` / `Colors` proxies, immutable `Style` & `Color` models, type aliases |
| [06. drawlib.preset_styles & preset_colors](06_presets.md) | `drawlib.preset_styles`, `drawlib.preset_colors` | `DefaultStyles`, `GoogleStyles`, `MonochromeStyles`, `CssColors`, palette presets |
| [07. drawlib.fonts](07_fonts.md) | `drawlib.fonts` | Standardized cross-platform font families (`Font`, CJK/global scripts, `FontFile`) |
| [08. drawlib.icons](08_icons.md) | `drawlib.icons` | 34 vector icon suites (`phosphor`, `gcp`, `aws`, `azure`, domain & flat suites) |
| [09. drawlib.smartarts (Lists, Cards & Tables)](09_smartarts_lists_cards.md) | `drawlib.smartarts` | `Table`, `BoxList`, `CardList`, `KpiCards`, `BulletPoints`, `Panel`, `SourceCode`, `GridLayout` |
| [10. drawlib.smartarts (Flows, Trees & Maps)](10_smartarts_flows_trees_maps.md) | `drawlib.smartarts` | `ChevronProcess`, `Cycle`, `Pyramid`, `Roadmap`, `TreeNode`, `MindMapNode`, `GeoMap`, `*Calendar` |
| [11. drawlib.charts.bar](11_charts_bar.md) | `drawlib.charts.bar` | Grouped, stacked, horizontal, and annotated `BarChart` |
| [12. drawlib.charts.line](12_charts_line.md) | `drawlib.charts.line` | Multi-series `LineChart` with markers, thresholds, and smooth interpolation |
| [13. drawlib.charts.area](13_charts_area.md) | `drawlib.charts.area` | Stacked and overlapping `AreaChart` |
| [14. drawlib.charts.pie](14_charts_pie.md) | `drawlib.charts.pie` | Proportional `PieChart` and donut ring charts |
| [15. drawlib.charts.radar](15_charts_radar.md) | `drawlib.charts.radar` | Multi-axis spider / polygon `RadarChart` |
| [16. drawlib.charts.scatter](16_charts_scatter.md) | `drawlib.charts.scatter` | 2D correlation `ScatterChart` and variable-radius bubble plots |
| [17. drawlib.charts.gantt](17_charts_gantt.md) | `drawlib.charts.gantt` | Project timeline, milestone, and dependency `GanttChart` |
| [18. drawlib.charts.heatmap](18_charts_heatmap.md) | `drawlib.charts.heatmap` | Matrix `HeatmapChart` and spatial `HeatmapOverlay` |
| [19. drawlib.diagrams.architecture](19_diagrams_architecture.md) | `drawlib.diagrams.architecture` | Cloud & microservice `ArchitectureDiagram`, groups, nodes, and orthogonal edges |
| [20. drawlib.diagrams.flow](20_diagrams_flow.md) | `drawlib.diagrams.flow` | Algorithmic `FlowDiagram`, swimlanes, decisions, and process nodes |
| [21. drawlib.diagrams.sequence](21_diagrams_sequence.md) | `drawlib.diagrams.sequence` | API `SequenceDiagram`, lifelines, activations, fragments, and notes |
| [22. drawlib.diagrams.class_diagram](22_diagrams_class.md) | `drawlib.diagrams.class_diagram` | OOP UML `ClassDiagram`, attributes, methods, and inheritance/composition links |
| [23. drawlib.diagrams.er](23_diagrams_er.md) | `drawlib.diagrams.er` | Database `ERDiagram`, entity tables, keys, and Crow's Foot cardinalities |
| [24. drawlib.diagrams.state](24_diagrams_state.md) | `drawlib.diagrams.state` | Lifecycle `StateDiagram`, composite states, forks/joins, and transitions |
| [25. drawlib.graph](25_graph.md) | `drawlib.graph` | 5 deterministic auto-layout coordinate solvers (`get_layout()`) |
| [26. drawlib.anim & drawlib.slide](26_anim_and_slide.md) | `drawlib.anim`, `drawlib.slide` | Multi-frame WebP `Animation` builder and 16:9 `SlideDeck` / `.pptx` engine |
| [27. drawlib.tools](27_tools.md) | `drawlib.tools` | Programmatic project builders, cache management, server, and agent rule APIs |
| [28. CLI Reference (drawlib)](28_cli.md) | `drawlib._cli` | Command-line interface (`init`, `build`, `show`, `serve`, `cache`, `rules`) |

---

## `const` __version__

Standard PEP 396 package version string exposed at `drawlib.__version__` (aliased to `LIB_VERSION`).

```python
from drawlib import __version__

__version__: Final[str] = "0.3.4"
```

| Attribute | Type | Value | Description |
| :--- | :--- | :--- | :--- |
| `__version__` | `Final[str]` | `'0.3.4'` | Installed Drawlib semantic version string. |

---

## `const` LIB_NAME

Canonical distribution and package identifier constant exposed at `drawlib.LIB_NAME`.

```python
from drawlib import LIB_NAME

LIB_NAME: Final[str] = "drawlib"
```

| Attribute | Type | Value | Description |
| :--- | :--- | :--- | :--- |
| `LIB_NAME` | `Final[str]` | `'drawlib'` | Canonical library name used in metadata, caching, and CLI reporting. |

---

## `const` LIB_VERSION

Canonical semantic version constant exposed at `drawlib.LIB_VERSION`.

```python
from drawlib import LIB_VERSION

LIB_VERSION: Final[str] = "0.3.4"
```

| Attribute | Type | Value | Description |
| :--- | :--- | :--- | :--- |
| `LIB_VERSION` | `Final[str]` | `'0.3.4'` | Semantic version string matching `drawlib.__version__`. |

---

## `type` drawlib.utils

Dynamic user helper module (`import drawlib.utils` or `from drawlib import utils`) automatically populated at build/render time with all top-level functions, classes, and constants defined in your project's `utils.py` file (or the file passed via `drawlib show -u <path>` / `drawlib build`).

```python
# In project utils.py:
# def service_card(xy: tuple[float, float], title: str) -> None: ...

from drawlib import utils

utils.service_card((60, 30), "API Gateway")
```

| Behavior / Property | Type | Description |
| :--- | :--- | :--- |
| `drawlib.utils.<name>` | `Any` | Resolves any top-level helper function, class, or constant loaded from `utils.py`. |
| Missing attribute access | `AttributeError` | Raises a descriptive `AttributeError` instructing how to define the symbol in `utils.py` or pass `--utils`. |

---

## `type` drawlib.charts.DrawDirection

Shared literal type alias exported from `drawlib.charts` specifying progressive reveal or orientation direction across chart components (such as `BarChart`, `LineChart`, and `AreaChart`).

```python
from typing import Literal
from drawlib.charts import DrawDirection

DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| Allowed Literal | Description |
| :--- | :--- |
| `'bottom_to_top'` | Grows or orientations chart elements vertically from bottom (`y0`) toward top. |
| `'left_to_right'` | Grows or orientations chart elements horizontally from left (`x0`) toward right. |
