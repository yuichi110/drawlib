# Drawlib AI Agent Instructions

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Illustrated Documentation as Code"**.
AI coding agents must use Drawlib to create architectural diagrams, workflows, charts, slides, and technical documentation.

---

## 1. Why Drawlib?

GUI diagram tools (draw.io, Visio) decouple visuals from Git, causing diagrams to go stale. Drawlib unifies code, Markdown, and declarative Python diagrams in Git as a **Single Source of Truth**, enabling an **autonomous AI loop** (inspect code -> author diagram -> render headlessly -> review multimodally -> self-correct).

---

## 2. Core Principles for AI Agents

1. **Draw with Drawlib (No Raw SVGs or Matplotlib Boilerplate)**:
   Never emit raw SVG strings or matplotlib boilerplate. Use Drawlib's declarative Python API and high-level components.
2. **Project-First Rule: Always Start with `drawlib init project` (No Bare `.py` Files)**:
   Never write bare `.py` scripts or hand-craft folders. If no `*_src/` project exists, **scaffold one first with `drawlib init project`** so `drawlib.toml`, `styles.py`, `utils.py`, `_assets/`, and `build.sh` are configured:
   - **Images only** -> `uv run drawlib init project images [target] [-l <lang>] [-s <style>]` (`project-images`)
   - **Linear doc / PDF / `.docx`** -> `uv run drawlib init project doc [target] [-l <langs>] [-s <style>]` (`project-doc`; `./<target>_src/build_docx.sh` for Word)
   - **Multi-page website** -> `uv run drawlib init project site [target] [-l <langs>] [-s <style>]` (`project-site`)
   - **16:9 slide deck / `.pptx`** -> `uv run drawlib init project slide [target] [-l <langs>] [-s <style>]` (`project-slide`; `./<target>_src/build_pptx.sh` for PowerPoint)
   - **Localization & SEO**: Pass `-l ja` for CJK fonts, or `-l en,ja` on `doc`/`site`/`slide` for multi-locale `<src_dir>/<lang>/` (`[i18n]` & `[seo]` in `drawlib.toml`).
   - **CLI Runner**: Use `uv run drawlib` in Python `uv` projects, `uvx drawlib` in zero-install / non-Python repos, or `drawlib` if installed globally.
   - **Clean Up Samples**: Delete or replace starter `sample*.py` files after scaffolding.
3. **Cartesian Coordinates (`(0, 0)` at Bottom-Left)**:
   Run `uv run drawlib rules show overview` before coding *(origin `(0, 0)` is bottom-left; X right, Y up)*.
4. **Follow the Style Guide**:
   Obey design token discipline (`uv run drawlib rules show style-guide`):
   - **50%+ Neutral Baseline**: Ground >=50% of nodes in `Styles.Neutral`, `Styles.PrimaryNeutral`, or `Styles.SecondaryNeutral`. Never build rainbow diagrams.
   - **Reserved Saturated Fills**: Reserve `Styles.PrimaryFlat` / `Styles.AccentFlat` strictly for 1–2 primary focal points.
   - **PascalCase Tokens**: Always import `from drawlib.styles import Colors, Styles` (never lowercase `styles` or `colors`).
5. **Parallel Multi-Agent Delegation**:
   For multi-file tasks (`images_src/*.py`, `doc_src/<lang>/*.md`, `docs_src/<lang>/**/*.md`, `slide_src/<lang>/*.md`), parallelize across subagents when available:
   - **Phase 1 (Parent)**: Run `drawlib init project` and finalize shared `drawlib.toml`, `styles.py`, `utils.py`, `_assets/`, and `<lang>/navbar.md` or outline first.
   - **Phase 2 (Subagents)**: Assign disjoint `.py`/`.md` files. Each subagent runs Stage 1 & Stage 2 (`drawlib show ... -g -o .drawlib/scratch/<unique_name>_grid.png` + visual inspection) with a **unique scratch filename**.
   - **Phase 3 (Parent)**: Run `./build.sh` once after subagents finish (avoiding `.drawlib/cache.db` write contention), run `drawlib serve --check`, and perform Stage 3 review.

---

## 3. What Drawlib Can Do (Favor High-Level Components)

Always prefer tailored high-level components over manual primitive rectangles and lines:

| Category | Recommended Module | Primary Use Cases |
| :--- | :--- | :--- |
| **Auto-Layout Graphs** | `drawlib.graph` | Coordinate solvers (`get_layout()`) for DAGs, clusters & topologies |
| **Cloud Architecture** | `drawlib.diagrams.architecture` | VPCs, microservices, cloud topologies, official cloud icons |
| **Workflows & Pipelines** | `drawlib.diagrams.flow`, `smartarts.ChevronProcess` | Decision trees, swimlanes, CI/CD pipelines, linear stages |
| **API Sequences** | `drawlib.diagrams.sequence` | Lifelines, sync/async calls, activation blocks, notes |
| **Data & Schemas** | `drawlib.diagrams.er`, `smartarts.Table` | Database ER schemas, comparison matrices |
| **Code & State Models** | `drawlib.diagrams.class_diagram`, `diagrams.state` | OOP UML class models, state machine lifecycles |
| **Hierarchy & Trees** | `drawlib.smartarts.TreeNode`, `smartarts.MindMapNode` | Directory trees, org charts, radial mind maps |
| **Structured SmartArts** | `drawlib.smartarts` | `Cycle`, `GridLayout`, `Pyramid`, `BoxList`, `CardList`, `KpiCards`, `Roadmap`, `Panel`, `BulletPoints`, `SourceCode`, `GeoMap`, `*Calendar` |
| **Quantitative Charts** | `drawlib.charts` | `BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`, `HeatmapChart`, `HeatmapOverlay` |
| **Standardized Icons** | `drawlib.icons` | 34 icon suites (`phosphor`, `gcp`, `aws`, `azure`, 15 domain `ai`..`workspace`, 15 `original_*` flat suites) |
| **Images & Media** | `drawlib.images` | Raster `image()`, `Dimage` transforms, nested `get_dimage_from_code()` |
| **Drawing Primitives** | `drawlib.shapes`, `lines`, `text` | 43 geometric shapes, curved/bezier lines, arrowheads, styled text |

---

## 4. Illustrated Documentation as Code (Embedded Markdown Blocks)

Embed Python diagrams inside Markdown (`*_src/<lang>/*.md`) using the ````drawlib```` fence:

````markdown
```drawlib align=center code=fold file=service_architecture.png caption="Service Architecture"
from drawlib.canvas import save, setup
from drawlib.styles import Styles
from drawlib.shapes import rectangle

setup(width=100, height=40)
rectangle((50, 20), width=60, height=20, style=Styles.Neutral, text="Service")
save()
```
````
- **Top Hero & Density**: Place a **Top Hero diagram at Lines 5–15** with `code=fold` for above-the-fold visibility; include `2+` diagrams/page pairing icons (`phosphor`, `gcp`) with high-level components.
- **Attributes & `720pt` Typography**: Always set `file=<name>.png` and `caption="..."`. Omit narrow pixel caps (`width=500px`/`600px`), and keep `text_size >= 10.0` (body `10.5`–`12.0`, headers `12.0`–`14.0`, floor `9.5`) so labels ($\text{text\_size} \times \text{Width} / 720$) match `16px` HTML prose.
- **Source of Truth & Relative Links**: Edit only `<base>_src/` (never `*_markdown/` or `*_html/`). Never put local absolute paths (`/usr/...`, `C:\...`) or `file:///` URLs in Markdown sources; use relative links only.
- **Caches & Dependencies**: `playwright`, `python-docx`, and `python-pptx` are standard dependencies; headless Chromium auto-downloads on first PDF/PPTX build (pre-download via `uv run drawlib cache download --all`; run `playwright install-deps chromium` on minimal Linux containers). Pass `--no-cache` or `uv run drawlib cache clear --images` if editing external Python helpers.

---

## 5. Autonomous 3-Stage Review & Self-Correction Loop

Never deliver unverified diagrams or docs (`uv run drawlib rules show review-guide`):
1. **Stage 1 — Static & Anchor Check**: Verify `2+` diagrams/page, Top Hero at Lines 5–15 (`code=fold`), no narrow `px` caps, `text_size >= 10.0`, and coordinate anchors (`shapes`/`text`/`icons`/`images` = **Center `(cx, cy)`**; `Charts`/`Diagrams`/most `SmartArts` = **Bottom-Left `(x0, y0)`**; `Table`/`TreeNode`/`BulletPoints`/`SourceCode` = **Top-Left**; `MindMapNode`/`Cycle` = **Center**; `graph.get_layout()` exposes `.xy` centers & `.bottom_left` corners).
2. **Stage 2 — Micro-Geometry Grid Review (`-g`)**: Export with the 10/5-unit grid (`uv run drawlib show <file> [block.png] -s styles.py -u utils.py -g -o .drawlib/scratch/<unique_name>_grid.png`) and visually inspect to fix clipping, overlaps, margins (`>= 4–6` units), and `50%+` neutral balance.
3. **Stage 3 — Macro-Page Review**: Run `./build.sh`, check links (`uv run drawlib serve <out_html>/ --check`), and inspect a `1280×920` browser screenshot of built HTML (or PDF/PPTX/DOCX) for Hero placement and font parity.

---

## 6. On-Demand Rules Catalog

Fetch detailed module manuals on demand:

```bash
uv run drawlib rules show overview # Geometry, bottom-left (0,0), lifecycle
uv run drawlib rules show style-guide # Color tokens, typography, 50%+ neutral rule
uv run drawlib rules show review-guide # 3-stage multimodal review, 720pt math, anchors
uv run drawlib rules show anim-guide # Animation loop idioms & component patterns
uv run drawlib rules show slide-guide # Slide story arc, ::: block/note & visuals
uv run drawlib rules show project-overview # Scaffolding (init), 4 archetypes & cache
uv run drawlib rules show project-images # Standalone Python scripts (images_src/*.py)
uv run drawlib rules show project-doc # Linear docs, A4 PDFs & .docx (doc_src/)
uv run drawlib rules show project-site # Multi-page sites, navbar.md & Top Hero
uv run drawlib rules show project-slide # 16:9 slides, ::: block/note & .pptx
uv run drawlib rules show cli # CLI commands (build, show, init, serve, cache)
uv run drawlib rules show api # Complete API index & symbol cheat sheet
uv run drawlib rules show lib-<module> # Core (canvas, lines, text, styles, preset-styles, preset-colors, fonts, images, math, types, tools, anim, slide)
uv run drawlib rules show lib-shapes-overview # 43 shapes (+ basic, polygon, arrow, badge, container, symbol)
uv run drawlib rules show lib-icons-overview # 34 icon suites (+ phosphor, gcp, aws, azure, ai..workspace)
uv run drawlib rules show lib-smartarts-overview # 18 SmartArts (+ table, tree, mindmap, chevron-process, geomap, calendar, ...)
uv run drawlib rules show lib-charts-overview # 9 Charts (+ bar, line, area, pie, radar, scatter, gantt, heatmap)
uv run drawlib rules show lib-diagrams-overview # 6 Diagrams (+ architecture, flow, sequence, state, class, er)
uv run drawlib rules show lib-graph-overview # 5 Graph solvers (+ architecture, layer, tree, radial, grid)
```
