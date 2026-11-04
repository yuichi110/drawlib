# 2. Architecture & Source Code Structure

Drawlib implements a strict **6-tier downward Directed Acyclic Graph (DAG)** across **424 Python source files (`85,323` LOC)**, separating a stateless-style Cartesian rendering core (`_core/l1_core` through `_core/l4_canvas`) from declarative visual domains, multi-format document/slide compilers, and 20 PEP 562 lazy public API facades (`drawlib/*.py`). Zero cross-layer circular imports exist across the codebase, while PNI hotspot telemetry localizes operational risk to container packaging (`Dockerfile.prod`), `uv.lock`, and document/slide compiler boundaries.

```drawlib align=center code=hide file=ch02_source_tree_inventory.png caption="Figure 2.1 — Physical Source Directory Hierarchy & Reconciled Module Inventory (424 Files, 85,323 LOC)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import Panel, Table, TreeNode
from drawlib.styles import Colors, Styles

setup(width=168, height=90)

# Left Panel: Hierarchical Source Tree
tree_panel = Panel(
    "Source Tree",
    "src/drawlib/",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral.patch(shape_line_width=1.2),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    icon=phosphor.folder_open,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.5,
)
tree_panel.draw((4.5, 5.0), width=56.5, height=80.0, align="bottom_left")

TreeNode.register_drawing_item(
    name="ch02_dir",
    location="before",
    padding_width=4.0,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 2.7},
)
TreeNode.register_drawing_item(
    name="ch02_py",
    location="before",
    padding_width=4.0,
    function=phosphor.file_py,
    style=Styles.Dark.patch(icon_color=Colors.Dark),
    args={"width": 2.7},
)

root = TreeNode(
    "src/drawlib/ (424 files)",
    text_style=Styles.DarkBold.patch(text_size=10.0),
    line_style=Styles.Muted.patch(line_width=1.0),
    line_horizontal_margin=2.5,
    line_horizontal_length=2.5,
    line_vertical_margin=4.4,
    children=[
        TreeNode(
            "_core/ (57 files)",
            text_style=Styles.DarkBold.patch(text_size=10.0),
            children=[
                TreeNode("l1_core & l2_types (14)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
                TreeNode("l3_colors..external (20)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
                TreeNode("l4_canvas/ (22 files)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
            ],
        ).set_drawing_item("ch02_dir"),
        TreeNode("_diagrams/ (56 files)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_builder/ (39 files)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_preset_styles+colors (10)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_smartarts/ (28 files)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_charts/ (41 files)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_icons/ + manifest (77)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_slide/ + _templates/ (27)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_cli/ + server + rules (31)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("_graph/ + _anim/ (22)", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch02_dir"),
        TreeNode("*.py Public Facades (36)", text_style=Styles.DarkBold.patch(text_size=10.0)).set_drawing_item("ch02_py"),
    ],
).set_drawing_item("ch02_dir")
root.draw(xy=(7.5, 72.8))

# Right Panel: Reconciled Module Inventory Table
table_panel = Panel(
    "Module Inventory & Roles",
    "424 Files · 85,323 LOC",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral.patch(shape_line_width=1.2),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.5,
)
table_panel.draw((64.0, 5.0), width=99.5, height=80.0, align="bottom_left")

inv_table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.2),
    border_style=Styles.MutedThin,
)
inv_table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)
inv_table.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.2),
)
inv_table.set_style_cell(
    background_color=Styles.PrimaryNeutral.shape_fill_color or Colors.Light,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    rows=[12],
)
inv_table.set_style_border(
    top=Styles.Dark.patch(line_width=1.2),
    top2=Styles.Dark.patch(line_width=1.0),
    bottom=Styles.Dark.patch(line_width=1.2),
    left=Styles.Dark.patch(line_width=1.0),
    right=Styles.Dark.patch(line_width=1.0),
    between_rows=Styles.MutedThin,
    between_columns=Styles.MutedThin,
)

inv_data = [
    ["Package / Subsystem", "Files", "LOC", "Primary Architectural Role"],
    ["_diagrams/", "56", "13,125", "6 diagram engines (Arch, Flow, UML, ER)"],
    ["_core/ (l1..l4)", "57", "13,018", "Settings, types, L3 assets & L4 Canvas"],
    ["_preset_styles + _colors", "10", "12,997", "8-role semantic styles & palettes"],
    ["_builder/", "39", "12,542", "MD fences, SQLite cache, HTML/PDF/DOCX"],
    ["_smartarts/", "28", "8,680", "18 SmartArts (Table, Tree, Roadmap, KPI)"],
    ["_charts/", "41", "6,120", "9 quantitative charts & HeatmapOverlay"],
    ["_slide/ + _templates/", "27", "5,606", "16:9 HTML/PDF/PPTX compiler & themes"],
    ["_icons/ + _assets", "77", "5,437", "34 icon suites & SHA-256 zip manifest"],
    ["_cli/ + server + _rules", "31", "3,160", "Typer CLI, preview server & AI rules"],
    ["_graph/ + _anim/", "22", "3,120", "5 graph layout solvers & Animation"],
    ["drawlib/*.py facades", "36", "1,518", "PEP 562 lazy public API (__all__)"],
    ["Total (src/drawlib/)", "424", "85,323", "100% typed · 0 cross-layer cycles"],
]
inv_table.draw_flexible(
    xy=(66.5, 73.8),
    column_widths=[27.5, 7.5, 11.0, 48.5],
    row_heights=[5.3] + [5.0] * 11 + [5.4],
    data=inv_data,
    align="top_left",
)

save()
```

---

## 2.1 System Profile & Physical Module Inventory

Drawlib operates simultaneously as a **programmatic Python library** (`drawlib.*`) and a **headless compiler CLI** (`drawlib`), built on Python `>=3.11` (verified across `3.11`, `3.12`, and `3.13` via `uv`). Its core technology stack pairs **Matplotlib, Pillow, and NumPy** for Cartesian `(0, 0)` bottom-left 2D vector/raster rendering with **Pydantic v2** (`@validate_call` boundary validation), **Typer & Rich** (CLI UX), **markdown-it-py, Pygments, Jinja2, and MarkupSafe** (Markdown/HTML compilation), **Playwright** (headless Chromium A4 PDF and slide rendering), **python-docx & python-pptx** (OpenXML `.docx`/`.pptx` generation), and **stdlib `sqlite3`** (`.drawlib/cache.db` incremental build caching).

Three external runtime boundaries are cleanly encapsulated behind dedicated adapters:
1. **GitHub Releases Asset Distribution (`src/drawlib/_core/l3_external/_package.py`)**: Lazily downloads font and icon `.zip` archives over HTTPS with an explicit `timeout=60` and cryptographic SHA-256 manifest verification (`src/drawlib/_release_assets.py`, `4,497` LOC).
2. **Playwright Headless Chromium Driver (`src/drawlib/_builder/_common/browser.py`)**: Coordinates on-demand browser installation (`fcntl` file locking) and deterministic A4 PDF / slide DOM extraction.
3. **Content-Addressed SQLite Build Cache (`src/drawlib/_builder/_common/cache.py`)**: `BuildImageCache` and `CliImageCache` (`640` LOC) hash embedded Python code, `styles.py`, `utils.py`, and referenced local assets using parameterized SQL queries.

---

## 2.2 Multi-Tier Layering, Dependency DAG & Risk Hotspots

Architectural boundaries enforce a strict downward dependency hierarchy from public facades and builders down to zero-dependency core types:
- **Zero Cross-Layer Cycles**: All cross-layer and internal-to-facade circular dependencies have been eliminated (`40` type-only annotations are guarded behind `if TYPE_CHECKING:`). Only **`2` localized intra-package sibling cycles** remain (`_edge.py <-> _junction.py` inside `src/drawlib/_diagrams/architecture/` and `src/drawlib/_diagrams/flow/`).
- **Underscore-Prefixed Encapsulation**: PNI's generic underscore heuristic records `86` cross-package underscore imports solely because Drawlib prefixes all private implementation subpackages (`_core`, `_charts`, `_diagrams`, `_smartarts`, `_graph`, `_icons`, `_builder`, `_slide`, `_cli`) behind thin public facade modules (`drawlib/*.py`) governed by PEP 562 lazy `__getattr__` loading in `src/drawlib/__init__.py`.

```drawlib align=center code=hide file=ch02_layer_dependency_heatmap.png caption="Figure 2.2 — 6-Tier Architectural Dependency DAG with PNI Module Hotspot Risk Overlay (risk_score 0.28–0.73)"
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Colors, Styles

setup(width=168, height=92)

cd = ClassDiagram(
    node_style=Styles.Neutral.patch(text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_color=Colors.Dark, text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    title="6-Tier Architecture Dependency DAG & PNI Thermal Risk Overlay",
    title_style=Styles.DarkBold.patch(text_size=13.0),
)

# Row 1: Tier 6 Public Facades, Tier 5 CLI/DocProcessor, and Container Packaging
t6_facades = cd.add(
    ClassNode(
        "Tier 6: Public Facades",
        width=46.0,
        header_style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=10.5),
    )
    .add_attribute("modules", "drawlib/*.py (36 files)")
    .add_method("__getattr__", "PEP 562 lazy", "Module"),
    xy=(30.0, 74.5),
)
t5_doc_cli = cd.add(
    ClassNode("Tier 5: CLI & Doc Builder", width=46.0)
    .add_attribute("processor.py", "risk = 0.51 (exec)")
    .add_attribute("styles_loader.py", "risk = 0.36 (exec)"),
    xy=(84.0, 74.5),
)
infra_docker = cd.add(
    ClassNode(
        "Infra: Docker Packaging",
        width=46.0,
        header_style=Styles.SecondaryNeutral.patch(text_color=Colors.Dark, text_size=10.5),
    )
    .add_attribute("Dockerfile.prod", "risk = 0.73 (UID 0)")
    .add_attribute("Dockerfile.test_*", "risk = 0.30 (DS-0002)"),
    xy=(138.0, 74.5),
)

# Row 2: Tier 4 Visual Domains, Tier 5 Browser/Slide Compilers, and Supply-Chain Lockfile
t4_domains = cd.add(
    ClassNode("Tier 4: Visual Domains", width=46.0)
    .add_attribute("packages", "_diagrams, _smartarts, _charts")
    .add_attribute("solvers", "_graph, _icons, _anim"),
    xy=(30.0, 49.0),
)
t5_browser_slide = cd.add(
    ClassNode("Tier 5: Browser & Slide", width=46.0)
    .add_attribute("browser.py", "risk = 0.35 (Chromium)")
    .add_attribute("_pptx_writer.py", "risk = 0.28 (11% cov)"),
    xy=(84.0, 49.0),
)
infra_lock = cd.add(
    ClassNode(
        "Infra: Supply-Chain Lock",
        width=46.0,
        header_style=Styles.SecondaryNeutral.patch(text_color=Colors.Dark, text_size=10.5),
    )
    .add_attribute("uv.lock", "risk = 0.45 (pillow)")
    .add_attribute("pyproject.toml", "risk = 0.21 (13 deps)"),
    xy=(138.0, 49.0),
)

# Row 3: Core Rendering Engine Tiers 3, 2, and 1
t3_canvas = cd.add(
    ClassNode("Tier 3: L4 Canvas Engine", width=46.0)
    .add_attribute("_canvas.py", "Cartesian (0,0) engine")
    .add_method("shapes_lines_text", "43 shapes", "None"),
    xy=(30.0, 23.5),
)
t2_l3 = cd.add(
    ClassNode("Tier 2: L3 Core Subsystems", width=46.0)
    .add_attribute("subsystems", "colors, fonts, Dimage, math")
    .add_attribute("_download.py", "risk = 0.28 (offline)"),
    xy=(84.0, 23.5),
)
t1_l1l2 = cd.add(
    ClassNode("Tier 1: L1–L2 Foundation", width=46.0)
    .add_attribute("l1_core", "DrawlibSettings, @validate_call")
    .add_attribute("l2_types", "Canonical geometry/style types"),
    xy=(138.0, 23.5),
)

# Downward & Cross-Tier UML Dependency Edges
cd.connect(t6_facades, t4_domains, "dependency", start_side="bottom", end_side="top")
cd.connect(t5_doc_cli, t6_facades, "dependency", start_side="left", end_side="right")
cd.connect(t5_doc_cli, t5_browser_slide, "dependency", start_side="bottom", end_side="top")
cd.connect(infra_docker, t5_doc_cli, "dependency", start_side="left", end_side="right")
cd.connect(t4_domains, t3_canvas, "dependency", start_side="bottom", end_side="top")
cd.connect(t5_browser_slide, t4_domains, "dependency", start_side="left", end_side="right")
cd.connect(infra_lock, t2_l3, "dependency", start_side="bottom", end_side="top")
cd.connect(t3_canvas, t2_l3, "dependency", start_side="right", end_side="left")
cd.connect(t2_l3, t1_l1l2, "dependency", start_side="right", end_side="left")

cd.draw(xy=(0.0, 0.0))

# Thermal Risk HeatmapOverlay (show_contour_lines=False mandatory)
overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    blend_mode="max",
    min_value=0.0,
    max_value=0.80,
    max_alpha=0.48,
    show_contour_lines=False,
)
overlay.add_spot((138.0, 74.5), value=0.73, radius=20.0)  # Dockerfile.prod = 0.73
overlay.add_spot((76.0, 75.5), value=0.51, radius=16.5)   # processor.py = 0.51
overlay.add_spot((138.0, 49.0), value=0.45, radius=18.0)  # uv.lock = 0.45
overlay.add_spot((93.0, 72.5), value=0.36, radius=14.0)   # styles_loader.py = 0.36
overlay.add_spot((76.0, 50.0), value=0.35, radius=14.5)   # browser.py = 0.35
overlay.add_spot((93.0, 47.0), value=0.28, radius=13.5)   # _pptx_writer.py = 0.28
overlay.draw(xy=(0.0, 0.0))
overlay.draw_colorbar(
    xy=(44.0, 5.5),
    text_style=Styles.Dark.patch(text_size=10.0),
    length=80.0,
    thickness=2.2,
    num_ticks=5,
    value_format="{:.2f}",
    label="PNI Module Hotspot Risk Score (Peak: Dockerfile.prod = 0.73)",
)

save()
```

| Tier | Architectural Layer | Physical Paths | Allowed Downward Dependencies |
| :---: | :--- | :--- | :--- |
| **Tier 6** | **Public User-Facing Facades** | `src/drawlib/__init__.py`, `canvas.py`, `styles.py`, `shapes.py`, `lines.py`, `text.py`, `charts/`, `diagrams/`, `smartarts.py`, `graph.py`, `icons.py`, `anim.py`, `slide.py` | Tiers 4, 3, 2, 1 (`_charts`..`_preset_styles`, `_core/l1..l4`) |
| **Tier 5** | **Document, Slide & CLI Builders** | `src/drawlib/_builder`, `_slide`, `_templates`, `_cli` | Tiers 4, 3, 2, 1 (`_charts`..`_preset_styles`, `_core/l1..l4`) |
| **Tier 4** | **High-Level Visual Domains** | `src/drawlib/_charts`, `_diagrams`, `_smartarts`, `_graph`, `_icons`, `_anim`, `_preset_styles` | Tiers 3, 2, 1 (`_core/l4_canvas`, `_core/l3_*`, `_core/l1..l2`) |
| **Tier 3** | **L4 Canvas Rendering Engine** | `src/drawlib/_core/l4_canvas` | Tiers 2, 1 (`_core/l3_*`, `_core/l1_core`, `_core/l2_types`) |
| **Tier 2** | **L3 Core Subsystems** | `src/drawlib/_core/l3_colors`, `l3_fonts`, `l3_images`, `l3_math`, `l3_styles`, `l3_external` | Tier 1 (`_core/l1_core`, `_core/l2_types`) |
| **Tier 1** | **L1–L2 Core Foundation & Types** | `src/drawlib/_core/l1_core`, `_core/l2_types` | Python `stdlib` & `pydantic` validation only |

---

## 2.3 Runtime Execution Flows, State & Concurrency Model

```drawlib align=center code=hide file=ch02_execution_flows_roadmap.png caption="Figure 2.3 — Recorded Runtime Execution Pipelines & Stateful/Persistent Storage Architecture"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel, Roadmap
from drawlib.styles import Styles

setup(width=168, height=84)

# Left Panel: 3 Runtime Execution Flows Roadmap
flows_panel = Panel(
    "Runtime Execution Flows",
    "Library & CLI Lifecycles",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral.patch(shape_line_width=1.2),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    icon=phosphor.git_branch,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.5,
)
flows_panel.draw((5.0, 5.0), width=97.0, height=74.0, align="bottom_left")
f_xy, f_w, f_h = flows_panel.get_content_box(
    (5.0, 5.0),
    width=97.0,
    height=74.0,
    padding=(3.0, 2.8),
)

rm = Roadmap(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    spine_style=Styles.DarkBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.0,
    card_shape="rounded_rect",
    spacing=2.6,
)
rm.add(
    "1. Declarative Python Canvas (setup -> draw -> save)",
    "canvas.setup() -> @validate_call domains -> L4 Canvas;\nlazy SHA-256 asset zip fetch -> PNG/WEBP/SVG/PDF",
    badge_text="F1",
    icon=phosphor.code,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rm.add(
    "2. Illustrated Doc Build (MD -> HTML / PDF / DOCX)",
    "drawlib.toml -> processor.py + SQLite BuildImageCache;\ncompiles HTML sites, Chromium A4 PDF & OpenXML DOCX",
    badge_text="F2",
    icon=phosphor.book_open,
)
rm.add(
    "3. 16:9 Slide Deck & Interactive Grid Preview (-g)",
    "::: block/note -> HTML/PDF/.pptx (_pptx_writer.py);\ndrawlib show -g renders 10/5u AI self-repair grid",
    badge_text="F3",
    icon=phosphor.presentation_chart,
)
rm.draw(f_xy, width=f_w, height=f_h)

# Right Panel: State, Storage & Concurrency Architecture
state_panel = Panel(
    "State & Storage",
    "Locks & WAL",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral.patch(shape_line_width=1.2),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    icon=phosphor.database,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.5,
)
state_panel.draw((106.0, 5.0), width=57.0, height=74.0, align="bottom_left")
s_xy, s_w, s_h = state_panel.get_content_box(
    (106.0, 5.0),
    width=57.0,
    height=74.0,
    padding=(2.8, 2.6),
)

state_cards = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=10.2),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=10.0),
    direction="vertical",
    spacing=2.0,
)
state_cards.add(
    "Active Canvas Singleton",
    "l4_canvas/_base.py; reset on\nsetup() / clear() lifecycle",
    badge_text="M1",
)
state_cards.add(
    "DrawlibSettings",
    "l1_core/_settings.py; verbosity\n& nested save suppression",
    badge_text="M2",
)
state_cards.add(
    ".drawlib/cache.db",
    "SQLite WAL BuildImageCache;\nhashes code, styles & assets",
    badge_text="D1",
)
state_cards.add(
    "~/.cache/drawlib",
    "SHA-256 font/icon zips &\nfcntl Chromium browser locks",
    badge_text="D2",
)
state_cards.draw(s_xy, width=s_w, height=s_h)

save()
```

- **Execution & Entrypoints**: Public programmatic callers enter via `src/drawlib/canvas.py` and `src/drawlib/tools.py`, while CLI automation enters through `src/drawlib/__main__.py:main` -> `src/drawlib/_cli/main.py:main` -> `src/drawlib/_cli/_drawlib.py:call_command` across 9 subcommands (`build`, `show`, `init`, `serve`, `cache`, `rules`, `styles`, `colors`, `css`).
- **Error & Concurrency Model**: Each CLI invocation runs synchronously in a single Python process, translating Pydantic `@validate_call` `ValidationError` and `ValueError` exceptions into clean exit codes inside `call_command()`. Cross-process Chromium downloads synchronize via `fcntl` locks in `src/drawlib/_builder/_common/browser.py`, and `.drawlib/cache.db` commits per-operation SQLite transactions (parallel callers targeting the same workspace should serialize `build.sh` runs to avoid SQLite write contention).
