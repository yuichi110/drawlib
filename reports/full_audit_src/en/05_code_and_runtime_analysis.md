# 5. Deep Dive: Code Quality, Testing & Runtime

Drawlib v0.3.5 pairs 100.0% static function type-annotation coverage and 99.3% Google-style docstring discipline across 424 source modules (`85,323` LOC) with an 86.3% line-covered test suite—and following in-tree `pkg.files` validation for offline icon lookups, hermetic `--network=none` container verification achieves a **99.5% offline pass rate (`1,405 / 1,412`)**, leaving only localized DOCX/Markdown compiler complexity and pre-baked Playwright browser caching for `.pptx` tests.

```drawlib align=center code=hide file=ch05_module_fitness_heatmap.png caption="Figure 5.1 — Subsystem × Quality Dimension Fitness Matrix highlighting core typing/docstring uniformity versus localized DOCX complexity and offline PPTX coverage gaps."
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapChart
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

setup(width=170, height=84)

chart = HeatmapChart(
    styles=[
        Styles.DangerFlat,
        Styles.WarningNeutral,
        Styles.Neutral,
        Styles.PrimaryNeutral,
    ],
    x_categories=[
        "Type\nSafety",
        "Docstring\nHygiene",
        "Import\nHygiene",
        "Complexity\nHealth",
        "Offline\nLine Cov",
    ],
    min_value=0.0,
    max_value=100.0,
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.DarkBold.patch(text_size=10.0),
    value_text_style=Styles.DarkBold.patch(text_size=10.0),
    width=98.0,
    height=60.0,
    cell_gap=0.8,
    cell_r=0.6,
    value_format="{:.1f}%",
    title="Subsystem × Engineering Quality Fitness Matrix (0–100%)",
    title_style=Styles.DarkBold.patch(text_size=12.5),
)

chart.add_row("_core/l1..l4", [100.0, 100.0, 100.0, 89.0, 95.5])
chart.add_row("_diagrams & _graph", [100.0, 100.0, 100.0, 82.0, 96.0])
chart.add_row("_charts & _smartarts", [100.0, 96.5, 100.0, 68.0, 92.7])
chart.add_row("cache & manifest", [100.0, 100.0, 100.0, 80.0, 89.2])
chart.add_row("exporter_docx.py", [100.0, 100.0, 100.0, 24.0, 82.2])
chart.add_row("_pptx_writer.py", [100.0, 100.0, 96.0, 96.0, 11.1])
chart.add_row("_cli", [100.0, 100.0, 100.0, 86.0, 85.1])

chart.set_cell(
    "Complexity\nHealth",
    "exporter_docx.py",
    24.0,
    label="24.0%\n(cog=174)",
    style=Styles.DangerFlat,
)
chart.set_cell(
    "Offline\nLine Cov",
    "_pptx_writer.py",
    11.1,
    label="11.1%\n(35/314)",
    style=Styles.DangerFlat,
)

chart.draw(xy=(12.0, 18.0))
chart.draw_colorbar(
    xy=(28.0, 5.5),
    text_style=Styles.Dark.patch(text_size=10.0),
    length=64.0,
    thickness=2.2,
    value_format="{:.0f}%",
    label="Normalized Dimension Fitness Score (%)",
)

panel = Panel(
    "Key Diagnostic Outliers",
    style=Styles.Neutral,
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.gauge,
    icon_style=Styles.DarkBold,
    header_variant="filled",
    header_height=8.8,
)
panel.draw((114.0, 6.0), width=50.0, height=72.0, align="bottom_left")
in_xy, in_w, in_h = panel.get_content_box((114.0, 6.0), width=50.0, height=72.0, padding=(2.8, 2.8))

cards = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=10.3),
    description_style=Styles.Dark.patch(text_size=9.7),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=9.8),
    spacing=2.5,
)
cards.add(
    "Core & Icon Parity",
    "100% typed & pkg.files checked;\n95.5%–96.0% line coverage",
    badge_text="OK",
)
cards.add(
    "DOCX Complexity Peak",
    "render_chapter=174 &\n_render_inline=102",
    badge_text="C1",
    badge_style=Styles.WarningFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.8),
)
cards.add(
    "Offline PPTX Gap",
    "_pptx_writer.py at 11.1%\n(no pre-baked Chromium)",
    badge_text="R1",
    badge_style=Styles.DangerFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.8),
)
cards.draw(in_xy, width=in_w, height=in_h)

save()
```

---

## 5.1 Static AST Code Quality, Typing & Maintainability

PNI's Python AST audit (`python_ast_audit`: **92/100, Grade S**) inspected all `424` non-generated source modules (`85,323` LOC, `300` classes, and `1,958` functions/methods; `**/*_generated.py` icon wrappers excluded from human-authored AST lint). Across core layers (`_core/l1_core` through `_core/l4_canvas`) and domain packages (`_charts`, `_diagrams`, `_smartarts`, `_graph`, `_icons`, `_anim`), static hygiene is unusually disciplined:

| Static Quality & Maintainability Metric | Measured Value | Rule Threshold / Target | Status & Engineering Interpretation |
| :--- | :---: | :---: | :--- |
| **Function Type-Annotation Coverage** | **`100.0%`** (`1,958/1,958`) | `>= 95.0%` (`python/typing`) | **PASS** — `src/drawlib/py.typed` (PEP 561), `0` unscoped `# type: ignore`, `0` `ty` errors, and runtime Pydantic `@validate_call` boundary checks. |
| **Docstring Coverage** | **`99.3%`** | `>= 90.0%` (`python/code_quality`) | **PASS** — `0` empty docstrings; only `12` fluent builder setters in `_mindmap.py` (`9`), `_tree.py` (`3`), and `_bulletpoints.py` (`1`—`style`) omit one-liners. |
| **Import Hygiene & Dependency Parity** | **`99.3%`** | `>= 95.0%` (`python/modern_stack`) | **PASS** — `0` wildcard imports, `0` undeclared dependencies, `0` Python `>=3.11` version mismatches, and `3` minor `isort` member-order notices. |
| **Shared Mutable Global State** | **`0`** | `0` (`common/maintainability`) | **PASS** — Canvas lifecycle state is encapsulated inside `_core/l4_canvas/_base.py` and reset cleanly per render/test. |
| **Cross-Layer & Sibling Import Cycles** | **`2` sibling (`0` layer)** | `0` (`common/architecture`) | **WARN** — `40` type-only cycles are isolated under `if TYPE_CHECKING:`; `2` sibling runtime cycles remain (`_edge.py <-> _junction.py` in `architecture` and `flow`). |
| **High-Complexity Functions (`> 15`)** | **`399`** | `<= 15` cognitive (`SIG`) | **WARN** — Concentrated in Markdown/OpenXML AST walkers (`exporter_docx.py`, `options.py`, `merger.py`) and rich border/layout solvers. |
| **Wide Parameter Signatures (`> 6` args)** | **`330` (`WAIVED`)** | `<= 6` positional (`SIG`) | **WAIVED (`.pni/pni.toml`)** — Intentional declarative keyword-only (`*`) styling, typography, and axis configuration APIs across Charts and SmartArts. |
| **12-Factor Operational Hygiene** | **`0` missing HTTP timeouts** | `common/production_readiness` | **PASS / INFO** — `urllib.request.urlopen(..., timeout=60)` in `_package.py:165`; `9` direct `os.environ` reads and `30` `print()` calls remain in `_builder/`. |

### Top Cognitive-Complexity Hotspots (`common/maintainability`)

While foundational geometry and canvas primitives stay compact, multi-format document compilation accumulates deep nested branching when walking `markdown-it-py` token streams and emitting OpenXML (`python-docx`) or merged single-file HTML:

| File & Line | Function / Method | Lines | Branches | Cognitive Complexity | Primary Responsibility & Decomposition Strategy |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `src/drawlib/_builder/doc_builder/exporter_docx.py:565` | `render_chapter` | `283` | `55` | **`174`** | Monolithic Markdown token-stream loop emitting headings, callouts, lists, code fences, images, and tables; split into a per-token dispatch table. |
| `src/drawlib/_builder/doc_builder/processor/options.py:93` | `parse_block_info` | `74` | `33` | **`106`** | Parses ```` ```drawlib ```` fence attributes (`file`, `width`, `align`, `code`, `caption`); extract per-key validator functions. |
| `src/drawlib/_builder/doc_builder/exporter_docx.py:301` | `_render_inline` | `124` | `36` | **`102`** | Inline formatting state machine (`strong`, `em`, `code_inline`, `link`, math/HTML spans); extract dedicated span handlers. |
| `src/drawlib/_builder/doc_builder/merger.py:142` | `build_merged_html` | `260` | `40` | **`87`** | Multi-chapter HTML concatenation, heading-level shifting, anchor rewriting, and TOC synthesis; separate into discrete AST passes. |
| `src/drawlib/_smartarts/_table.py:490` | `_draw_border_lines` | `96` | `32` | **`74`** | Resolves outer (`top`, `bottom`, `left`, `right`), header (`top2`, `left2`), and inner grid strokes; separate perimeter vs inner-grid helpers. |
| `src/drawlib/_builder/doc_builder/exporter_docx.py:426` | `_emit_table` | `100` | `20` | **`57`** | Converts Markdown tables into OpenXML `<w:tbl>` structures with column alignments and cell shading. |
| `src/drawlib/_builder/_common/seo.py:205` | `extract_markdown_description` | `77` | `20` | **`46`** | Strips fences, directives, headings, and inline markup to synthesize clean meta/OGP page descriptions. |
| `src/drawlib/_builder/doc_builder/exporter_docx.py:884` | `export_chapters_to_docx` | `202` | `23` | **`46`** | Orchestrates cover page, TOC field generation, chapter assembly, and deterministic OPC zip timestamp normalization. |

### Library vs. CLI Boundary Hygiene (`common/library_guidelines`: **91/100, Grade S**)

`src/drawlib/__init__.py` implements **PEP 562 lazy `__getattr__` loading**, ensuring `import drawlib` executes in milliseconds with zero heavy Matplotlib/Playwright initialization or network side effects. Two minor boundary couplings merit cleanup in `P2`:
1. **Library-Level `sys.exit(1)` Calls**: `src/drawlib/_core/l1_core/_settings.py` (lines `123`, `297`, `304`, `313`) and `src/drawlib/_builder/doc_builder/processor/viewer.py` (lines `189`, `193`, `245`) invoke `sys.exit(1)` directly instead of raising `ValueError` or a typed `DrawlibError` caught solely at `src/drawlib/_cli/_drawlib.py:call_command`.
2. **Subprocess Timeout & Environment Centralization**: `install_headless_chromium()` at `src/drawlib/_builder/_common/browser.py:210` invokes `subprocess.run(...)` without an explicit `timeout=300` guard, and `9` direct `os.environ` lookups across `_builder/_common/{browser.py,cache.py,office.py}`, `exporter_pdf.py`, `viewer.py`, and `rules_builder.py` should be consolidated into a typed builder settings helper.

---

## 5.2 Clean-Room Container Verification & Measured Coverage

Static test analysis (`python_test_audit`: **93/100, Grade S**) confirmed `150` test modules and `1,293` test functions (`1,420` collected pytest items with parametrization) achieving **100.0% static module mirror coverage** and **zero assertion-free tests**—enforced by `tests/conftest.py`, which resets canvas state via an `autouse` `preprocess()` fixture and intercepts `pytest_runtest_call` to verify rendered outputs pixel-for-pixel against `*_answers/*.png` baselines.

PNI executed **4 containerized runtime verification stages** (`container_runtime_audit`: **88/100, Grade A**) inside `.pni/dockerfiles/Dockerfile` (`python:3.12` + `uv`, `pytest-cov`) with external networking completely disabled (`--network=none`) during test execution:

```drawlib align=center code=hide file=ch05_runtime_coverage_breakdown.png caption="Figure 5.2 — Hermetic container runtime verification KPIs (RV-01 through RV-04) and lowest-covered non-generated modules under --network=none."
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards, Panel
from drawlib.styles import Styles

setup(width=170, height=84)

left_panel = Panel(
    "Clean-Room Stages (--network=none)",
    style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.8),
    icon=phosphor.cube,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.8,
)
left_panel.draw((5.0, 6.0), width=62.0, height=72.0, align="bottom_left")
l_xy, l_w, l_h = left_panel.get_content_box((5.0, 6.0), width=62.0, height=72.0, padding=(2.6, 2.8))

kpis = KpiCards(
    style=Styles.White,
    metric_style=Styles.PrimaryBold.patch(text_size=13.0),
    text_style=Styles.DarkBold.patch(text_size=10.2),
    description_style=Styles.Muted.patch(text_size=9.5),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.32,
    spacing=2.5,
)
kpis.add(
    "PASS",
    "RV-01 Clean Build (3.76s)",
    ".pni/dockerfiles/Dockerfile exit 0",
    metric_style=Styles.SuccessBold.patch(text_size=13.0),
    accent_style=Styles.SuccessFlat,
)
kpis.add(
    "PASS",
    "RV-04 Smoke Check (2.42s)",
    "drawlib --help & import drawlib",
    metric_style=Styles.SuccessBold.patch(text_size=13.0),
    accent_style=Styles.SuccessFlat,
)
kpis.add(
    "86.3%",
    "RV-03 Line Cov (75.5% Br)",
    "37,221 / 43,108 statements",
    metric_style=Styles.PrimaryBold.patch(text_size=13.0),
    accent_style=Styles.PrimaryFlat,
)
kpis.add(
    "99.5%",
    "RV-02 Offline (1,405/1,412)",
    "12 icon tests fixed · 6 PPTX open",
    metric_style=Styles.SuccessBold.patch(text_size=13.0),
    accent_style=Styles.SuccessFlat,
)
kpis.draw(l_xy, width=l_w, height=l_h, columns=1)

bar = BarChart(
    axis_line_style=Styles.Muted,
    categories=[
        "__main__.py",
        "_pptx_writer.py",
        "_icons/__init__.py",
        "font_icons/__init__.py",
        "png_icons/__init__.py",
        "compiler/pdf.py",
        "_pptx_dom.py",
    ],
    width=78.0,
    height=58.0,
    orientation="horizontal",
    bar_mode="group",
    bar_width_ratio=0.72,
    bar_r=0.7,
    title="Lowest-Covered Non-Generated Modules (%)",
    title_style=Styles.DarkBold.patch(text_size=11.8),
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.6),
    value_format="{:.1f}%",
)
bar.add_series("Line Coverage (%)", [0.0, 11.1, 33.3, 37.5, 50.0, 52.2, 58.6], style=Styles.PrimaryFlat)
bar.add_series("Branch Coverage (%)", [0.0, 0.0, 0.0, 0.0, 0.0, 38.9, 4.0], style=Styles.SecondaryNeutral)
bar.configure_x_axis(min_value=0.0, max_value=75.0, tick_step=15.0, unit="%")
bar.draw(xy=(86.0, 7.0))
bar.draw_legend(
    xy=(90.0, 68.5),
    text_style=Styles.Dark.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=5.5,
)

save()
```

### Lowest-Covered Modules Inventory (`RV-03`: `86.3%` Line, `75.5%` Branch)

Across all `43,108` executable statements in `src/drawlib/`, `pytest-cov` recorded `37,221` covered lines (`86.3%`) and `75.5%` branch coverage. All modules below `60%` line coverage fall into three well-defined buckets: (1) CLI `python -m drawlib` entry wrapper (`__main__.py`), (2) Playwright/OpenXML exporters blocked when headless Chromium is absent offline (`_pptx_writer.py`, `compiler/pdf.py`, `_pptx_dom.py`), and (3) lazy icon `__getattr__` facades plus auto-generated `*_generated.py` icon wrappers (`51.6%`–`58.2%`, where unit tests sample representative icons rather than invoking all 4,500+ bindings):

| Module Path (Sorted Ascending by Line Coverage) | Line Coverage | Branch Coverage | Covered / Total Stmts | Primary Uncovered Lines & Root Cause |
| :--- | :---: | :---: | :---: | :--- |
| `src/drawlib/__main__.py` | **`0.0%`** | `0.0%` | `0 / 6` | Lines `12–23`: `python -m drawlib` wrapper not invoked directly by CLI runner tests (`CliRunner` invokes Typer app directly). |
| `src/drawlib/_slide/_pptx_writer.py` | **`11.1%`** | `0.0%` | `35 / 314` | Lines `81–90+`: OpenXML shape/table/notes emitter bypassed offline because upstream `extract_deck_dom()` failed launching Chromium. |
| `src/drawlib/_icons/__init__.py` | **`33.3%`** | `0.0%` | `7 / 21` | Lines `99–109`: Lazy `__getattr__` fallback branches and `AttributeError` paths on internal icon package root. |
| `src/drawlib/_icons/font_icons/__init__.py` | **`37.5%`** | `0.0%` | `6 / 16` | Lines `24–38`: Lazy attribute resolution and `dir()` introspection helpers. |
| `src/drawlib/_icons/png_icons/__init__.py` | **`50.0%`** | `0.0%` | `6 / 12` | Lines `57–66`: Lazy PNG icon suite loader error/fallback branches. |
| `src/drawlib/_icons/font_icons/phosphor/_generated.py` | **`51.6%`** | `N/A` | `1,580 / 3,064` | Auto-generated Phosphor glyph wrappers (representative subset exercised by visual tests). |
| `src/drawlib/_icons/png_icons/aws/_generated.py` | **`51.6%`** | `N/A` | `342 / 663` | Auto-generated AWS architecture icon wrappers (`azure/_generated.py` `52.1%`, `gcp/_generated.py` `52.7%`). |
| `src/drawlib/_builder/doc_builder/compiler/pdf.py` | **`52.2%`** | `38.9%` | `47 / 90` | Lines `51, 97–115`: Multi-locale and error-handling branches in A4 PDF compilation. |
| `src/drawlib/_slide/_pptx_dom.py` | **`58.6%`** | `4.0%` | `139 / 237` | Lines `989–1011`: In-browser Playwright DOM bounding-box extraction aborted before Chromium page evaluation. |

---

## 5.3 Root-Cause Analysis: Two Authentic Bugs Uncovered by `--network=none`

Online GitHub Actions runners mask unintended live network dependencies because outbound HTTPS requests to `github.com` and `cdn.playwright.dev` succeed transparently. Running `pytest` inside an air-gapped `--network=none` container surfaced **two genuine architectural defects**:

### Bug A (`RESOLVED`) — Negative Icon Tests Triggered Live HTTPS Archive Downloads (`12` Icon Failures Fixed)

Twelve negative icon tests (`test_nonexistent_*_icon_error`) pass an intentionally bogus icon filename under a valid suite directory (such as `icons/ai/nonexistent_icon.png`) and assert that Drawlib raises a missing-file error. Previously, the lookup chain triggered a live HTTPS archive download:
1. `find_package_for_icon_path()` in `src/drawlib/_release_assets.py` extracted only the top-level directory segment (`family = normalized.split("/")[0]`, e.g., `icon_ai`) and returned the `ReleaseAssetPackage` **without checking whether the requested relative path existed in `pkg.files`**.
2. `resolve_png_icon_path()` in `src/drawlib/_icons/png_icons/_base.py` then called `download_if_not_exist()`, attempting to download `https://github.com/yuichi110/drawlib/releases/download/v0.3/icon_<suite>.zip` just to discover after extraction that `nonexistent_icon.png` was never in the archive.
3. **In-Tree Fix (`COMPLETED`)**: `find_package_for_resource_path()` and `find_package_for_icon_path()` in `src/drawlib/_release_assets.py` now verify `normalized in pkg.files` before returning a package, and `resolve_png_icon_path()` in `src/drawlib/_icons/png_icons/_base.py` checks `find_package_for_icon_path(rel_path) is None` before calling `download_if_not_exist()`, immediately raising `ValueError(f'Icon "{file_name}" not found in "{category}" icon set.')` with zero network I/O. All `12` negative icon tests (`#2–#13` below) now pass offline in `< 1 ms`.

### Bug B (`OPEN`) — Runtime Headless Chromium Download in `.pptx` Export Tests (`6` PPTX Failures + `1` Uncached Font)

Six PowerPoint compilation tests (`test_cli_build_pptx` plus all `5` `TestBuildPptx` methods in `tests/drawlib/slide/test_pptx.py`) compile Markdown slide decks into `.pptx` archives. Drawlib's slide compiler renders slide HTML in headless Chromium (`src/drawlib/_slide/_pptx_dom.py:extract_deck_dom`) to measure exact CSS layout coordinates before `src/drawlib/_slide/_pptx_writer.py` emits native OpenXML shapes:
1. `launch_headless_chromium()` at `src/drawlib/_builder/_common/browser.py:247` invokes `playwright.chromium.launch(headless=True, args=launch_args)`.
2. Because `.pni/dockerfiles/Dockerfile` uses the standard Python/uv base image without pre-installed Playwright browser binaries, `launch()` raises a missing-executable error, triggering `install_headless_chromium()` (`browser.py:256` -> `browser.py:210`), which spawns `playwright install chromium-headless-shell` and fails resolving `cdn.playwright.dev` (`EAI_AGAIN`) under `--network=none`.
3. **Remediation (`P1`)**: Pre-bake `playwright install --with-deps --only-shell chromium` and `drawlib cache download --all` into `.pni/dockerfiles/Dockerfile`, add an offline-aware skip marker when browser binaries are intentionally absent, and add pure-Python unit tests passing synthetic `PptxSlide` DOM fixtures directly into `_pptx_writer.py`.

### Complete Offline Container Test Log (`RV-02`: `12` Fixed, `7` Requiring Pre-Baked Browser/Font Cache)

| # | Status | Test Case (`classname::name`) | Root Cause Bucket | Diagnostic & Resolution Summary |
| :-: | :---: | :--- | :--- | :--- |
| 1 | `OPEN` | `tests.drawlib.cli.test_cli_build::test_cli_build_pptx` | **Bug B** (Playwright CDN) | Requires pre-baked Chromium in `.pni/dockerfiles/Dockerfile` (`browser.py:247`) |
| 2–13 | **`FIXED`** | `12x test_nonexistent_*_icon_error` (`test_ai`, `test_aws_azure`, `test_cnative`, `test_data`, `test_devops`, `test_network`, `test_server`) | **Bug A** (`_release_assets.py`) | **Resolved**: `find_package_for_icon_path()` checks `pkg.files` before network I/O (`0` DNS calls) |
| 14–18 | `OPEN` | `5x tests.drawlib.slide.test_pptx.TestBuildPptx::*` | **Bug B** (Playwright CDN) | Requires pre-baked Chromium in `.pni/dockerfiles/Dockerfile` (`browser.py:247`) |
| 19 | `OPEN` | `tests.drawlib.smartarts.test_sourcecode.TestSourceCode::test_sourcecode_japanese` | **Uncached Font** | Requires `drawlib cache download --all` (`font_mono_source_han_code_jp.zip`) in test image |
