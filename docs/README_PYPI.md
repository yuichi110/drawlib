# Drawlib

**Pure-Python Library for "Illustration as Code" & "Illustrated Documentation as Code"**

Drawlib is a declarative Python drawing library and integrated multi-format documentation compiler engineered for software developers and **autonomous AI coding agents**. Instead of maintaining brittle diagrams in external GUI tools (draw.io, Visio, PowerPoint) and manually pasting exported screenshots into wikis, Drawlib lets you author, animate, localize, version-control, and compile architectural diagrams, quantitative charts, technical documents, and 16:9 slide decks entirely from code in Git.

![Autonomous AI Documentation Workflow](https://www.drawlib.com/images/index/hero_ai_doc_loop.png)

- **Official Website & Documentation**: [English (`www.drawlib.com`)](https://www.drawlib.com/) | [日本語 (`www.drawlib.com/ja/`)](https://www.drawlib.com/ja/)
- **Repository Guides & Whitepapers**:
  - [Quickstart Guide (PDF)](https://github.com/yuichi110/drawlib/blob/main/docs/quickstart_en.pdf)
  - [16:9 Presentation Slide Deck (PDF)](https://github.com/yuichi110/drawlib/blob/main/docs/slide_about_drawlib_en.pdf)
  - [Dogfooding Whitepaper — English (PDF)](https://github.com/yuichi110/drawlib/blob/main/docs/drawlib-dogfooding_en.pdf) | [日本語版 (PDF)](https://github.com/yuichi110/drawlib/blob/main/docs/drawlib-dogfooding_ja.pdf)

---

## Why Drawlib?

### 1. SmartArt Infographics, Quantitative Charts & Declarative Animations

Compose executive-ready infographics (`drawlib.smartarts`), quantitative data plots (`drawlib.charts`), and multi-frame **APNG / WebP / GIF** animations (`drawlib.anim`) on the exact same coordinate canvas:

![SmartArts Visual Showcase](https://www.drawlib.com/images/04_smartarts/overview/smartarts_showcase.png)

- **18 SmartArt Components (`drawlib.smartarts`)**: High-level structured layouts including `ChevronProcess`, `Cycle`, `Table`, `TreeNode`, `MindMapNode`, `Pyramid`, `BoxList`, `CardList`, `KpiCards`, `Roadmap`, `Panel`, `BulletPoints`, `GridLayout`, syntax-highlighted `SourceCode`, offline vector maps (`GeoMap`), and `MonthCalendar` / `WeekCalendar` / `DayCalendar`.

![Animated Quantitative Charts](https://www.drawlib.com/images/08_animations/charts/anim_charts_hero.png)

- **9 Quantitative Charts (`drawlib.charts`)**: Pure-Python `BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`, and `HeatmapChart` / `HeatmapOverlay` styled with the same design tokens as surrounding diagrams—no low-level Matplotlib boilerplate required.
- **Declarative Animations (`drawlib.anim`)**: Turn any diagram, chart, or workflow into a crisp multi-frame **APNG**, **WebP**, or **GIF** animation (`Animation(fps=..., loop=0)`) that plays natively inside GitHub `README.md` files, pull requests, and HTML documentation sites.

---

### 2. Auto-Layout Graphs & Software Engineering Diagrams

Stop hand-tuning complex node coordinates. Combine automatic graph layout solvers (`drawlib.graph`) with domain-specific software engineering diagrams (`drawlib.diagrams`):

![Five Auto-Layout Graph Solvers](https://www.drawlib.com/images/07_graph/overview/graph_five_solvers_hero.png)

- **5 Auto-Layout Coordinate Solvers (`drawlib.graph`)**: Pure coordinate calculators (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`) that compute overlap-free node centers (`.xy`), nested cluster bounds, and `offset()` fine-tuning via `get_layout()` for seamless rendering with `drawlib.diagrams` and `drawlib.shapes`.

![Six Software Engineering Diagram Families](https://www.drawlib.com/images/06_diagrams/overview/diagrams_six_families_hero.png)

- **6 Technical Diagram Engines (`drawlib.diagrams`)**:
  - **Cloud Architecture (`ArchitectureDiagram`)**: Nested VPC/subnet boundaries, multi-tier service cards, and official cloud provider icons.
  - **Flowcharts (`FlowDiagram`)**: Process steps, decision branches, and orthogonal connectors.
  - **Sequence Diagrams (`SequenceDiagram`)**: Client/server lifelines, synchronous/asynchronous calls, activation bars, and loop/alt frames.
  - **State, UML Class & ER Diagrams (`StateDiagram`, `ClassDiagram`, `ERDiagram`)**: State lifecycles, object-oriented class hierarchies, and relational database schemas.

---

### 3. 34 Icon Suites (4,500+ Icons), 43 Primitives & Semantic Design System

At its core, Drawlib cleanly separates **Content** (geometry, coordinates, structure) from **Style** (colors, typography, borders, themes)—just like HTML and CSS:

![34 Standardized Icon Suites Overview](https://www.drawlib.com/images/03_icons/overview/icons_overview_hero.png)

- **34 Standardized Icon Suites (`drawlib.icons`)**: Over **4,500 offline-cached vector icons** spanning **Phosphor** (`1,512` icons across `5` weights), **Cloud Providers** (`gcp`, `aws`, `azure`), **15 Official Tech Brand Suites** (`ai`, `cicd`, `cloud`, `code`, `compute`, `container`, `data`, `database`, `k8s`, `linux`, `mobile`, `monitoring`, `network`, `security`, `workspace`), and **15 Flat 2D Suites** (`original_*`).
- **Rich Primitives (`drawlib.shapes`, `lines`, `images`, `text`, `fonts`)**:
  - **43 Geometric Shapes**: Spanning `basic`, `polygon`, `arrow`, `badge`, `container`, and `symbol` primitives.
  - **Lines & Connectors**: Straight, curved (`bend`), quadratic/cubic Bezier, and rounded polylines with rich arrowheads (`"->"`, `"<-"`, `"<->"`).
  - **Images & Nested Canvases**: Non-destructive `Dimage` transformations (`crop()`, `sepia()`, `grayscale()`, `mosaic()`, `mirror()`) plus in-memory diagram nesting via `get_dimage_from_code()`.
  - **Multilingual Typography**: Automatic on-demand font caching (`FontRoboto`, `FontSansSerif`, `FontSerif`, `FontSourceCode`, `FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, etc.).
- **7-Role Semantic Style System (`drawlib.styles`)**:
  - 6 built-in themes (`default`, `google`, `essentials`, `monochrome`, `warm`, `cold`) accessed via `Styles.<Token>` (`Styles.Neutral`, `Styles.PrimaryFlat`, `Styles.SecondaryNeutral`, `Styles.MutedDashed`, `Styles.SuccessNeutral`, `Styles.WarningNeutral`, `Styles.DangerNeutral`).

---

### 4. Illustrated Documentation & 16:9 Slide Deck as Code (Multi-Locale Ready)

Author Markdown files with embedded ```` ```drawlib ```` code fences inside a unified `drawlib.toml` project. A single build compiles your repository into web portals, GitHub Markdown, PDFs, editable Word documents, HTML slide decks, and PowerPoint files:

![Multi-Locale Documentation and Slide Build Pipeline](https://www.drawlib.com/images/01_getting_started/project_quicklook/doc_build_pipeline.png)

- **Unified `drawlib.toml` & Multi-Locale (`<lang>/`) Architecture**: Configure project metadata, `[build]` flags, and `[i18n]` locales (`langs = ["en", "ja"]`) in `drawlib.toml` with built-in structural parity checks across `<src_dir>/<lang>/` trees and locale-suffixed deliverables (`*_<lang>.pdf`, `*_<lang>.docx`, `*_<lang>.pptx`).
- **4 Project Scaffolds (`drawlib init <type>`)**:
  - `drawlib init site [-l en,ja]`: Multi-page documentation website (`docs_html/` with language switcher, search, and sidebar TOC) and GitHub Markdown (`docs_markdown/`).
  - `drawlib init doc [-l en,ja]`: Linear technical specification or whitepaper (`*_html/`, `*_markdown/`, vector `*_<lang>.pdf`, plus editable MS Word `*_<lang>.docx` via `drawlib build docx`).
  - `drawlib init slide [-l en,ja]`: 16:9 presentation slide deck (`::: block` + `::: note` speaker notes) with native SVG typography, Presenter View, keyboard navigation (`slide_html/`), vector `slide_<lang>.pdf`, and editable MS PowerPoint `slide_<lang>.pptx` via `drawlib build pptx`.
  - `drawlib init images`: Standalone batch Python illustration scripts (`images_src/` -> `images/`) backed by sub-millisecond `.drawlib/cache.db` incremental caching.
- **AI Inner Loop & Human Outer Loop**: Built from the ground up for AI coding agents (Claude Code, Cursor, Gemini, Codex). Agents query `drawlib rules show <topic>` on demand, render headless coordinate-grid previews via `drawlib show -g`, and multimodally self-correct text clipping or layout defects—freeing engineers to focus on high-level architecture and review.

---

## Installation

Install `drawlib` from PyPI using `pip` or `uv` (Python `>= 3.11`):

```bash
pip install drawlib
# or: uv add drawlib
```

PDF, MS Word (`.docx`), and MS PowerPoint (`.pptx`) export work out of the box—`playwright`, `python-docx`, and `python-pptx` are standard dependencies, and headless Chromium (`chromium-headless-shell`) downloads automatically on your first `drawlib build pdf` or `drawlib build pptx` run.

- **Offline / Air-Gapped / CI Environments**: Pre-download all fonts, icons, maps, and headless Chromium ahead of time with `drawlib cache download --all` (or Chromium only with `drawlib cache download --browser`).
- **Minimal Linux Containers** (e.g., `python:3.12-slim` lacking OS shared libraries such as `libnss3` or `libgbm1`): Install OS browser dependencies once via `playwright install-deps chromium` (or `playwright install --with-deps --only-shell chromium`).

Verify the installation:

```bash
drawlib --version
```

---

## Quick Start

### 1. Standalone Python Script (5-Step Drawing Workflow)

Every Drawlib script follows a clean 5-step pattern: **Import -> Setup Canvas -> Draw Zones (Optional) -> Shapes & Lines -> Save**:

![5-Step Standalone Python Drawing Workflow](https://www.drawlib.com/images/01_getting_started/quick_start/quickstart_five_step_workflow.png)

Create `client_server.py`:

```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=100, height=44)
# Optional: boundary zone
rectangle((50, 22), 92, 36, style=Styles.MutedDashed)
circle((25, 22), 12,
       style=Styles.Neutral, text="Client")
rectangle((75, 22), 26, 20,
          style=Styles.PrimaryFlat, text="Server")
line((37, 22), (62, 22),
     arrow_head="->", style=Styles.DarkBold)
text((49.5, 27), "REST API", style=Styles.DarkBold)
save()
```

Run the script with Python to generate `client_server.png`:

```bash
python client_server.py
```

#### Core Principles at a Glance
- **Bottom-Left Origin `(0, 0)`**: `setup(width=100, height=44)` defines a Cartesian coordinate canvas where `x` spans `0..100` (left to right) and `y` spans `0..44` (bottom to top).
- **Predictable Coordinate Anchors**: Core primitives (`rectangle`, `circle`, `icon`, `image`, `text`) anchor at their **center `(cx, cy)`** for effortless alignment, while high-level `Charts` and `Diagrams` anchor at **bottom-left `(x0, y0)`**.
- **50%+ Neutral Baseline**: Ground supporting shapes in calm neutral tokens (`Styles.Neutral`, `Styles.SecondaryNeutral`, `Styles.MutedDashed`) and reserve saturated fills (`Styles.PrimaryFlat`) for 1–2 focal elements.
- **Non-Destructive Style Patching (`.patch()`)**: Customize any preset token cleanly via `Styles.MutedBold.patch(text_size=10)` or `Styles.Primary.patch(shape_line_width=2)`.

---

### 2. Illustrated Documentation & Slide Deck Workflow

Scaffold a multi-page documentation site, linear whitepaper, or 16:9 slide deck in seconds (pass `-l en,ja` for multi-locale `<src_dir>/<lang>/` projects):

```bash
# Initialize a bilingual multi-page documentation site in docs_src/ (en/ & ja/)
drawlib init site -l en,ja

# Or initialize a 16:9 presentation slide deck in slide_src/
drawlib init slide -l en,ja
```

Inside your Markdown files (`docs_src/en/index.md`), embed Python drawing blocks using the ```` ```drawlib ```` fence:

````markdown
# System Architecture

Below is our core request routing pipeline:

```drawlib code=fold align=center file=service_routing.png caption="Service Routing Pipeline"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=40)
rectangle((25, 20), width=30, height=16, r=2, style=Styles.Neutral, text="Ingress")
rectangle((75, 20), width=30, height=16, r=2, style=Styles.PrimaryFlat, text="Core API", text_style=Styles.WhiteBold)
line((40, 20), (60, 20), arrow_head="->", style=Styles.DarkBold)
save()
```
````

Compile, export, and preview with the `drawlib` CLI:

```bash
# Build HTML site, GitHub Markdown, or PDF via generated build script
./docs_src/build.sh

# Export editable MS Word (.docx) or MS PowerPoint (.pptx) per locale
drawlib build docx doc_src/ -o spec.docx --generate-index   # -> spec_en.docx, spec_ja.docx
drawlib build pptx slide_src/ -o deck.pptx                  # -> deck_en.pptx, deck_ja.pptx

# Launch local HTTP server with pre-flight broken-link verification
drawlib serve docs_html/ --check

# Render a single diagram with coordinate grid (-g) for visual layout inspection
drawlib show docs_src/en/index.md service_routing.png -g -o preview_grid.png
```

---

### 3. CLI Reference Summary

| Command | Description |
| :--- | :--- |
| `drawlib init <site\|doc\|slide\|images> [-l <langs>]` | Scaffold a documentation site, linear spec, 16:9 slide deck, or image project (`drawlib.toml`) |
| `drawlib build <html\|markdown\|pdf\|docx\|slide\|pptx\|image>` | Compile sources into HTML, Markdown, PDF, MS Word (`.docx`), HTML Slides, MS PowerPoint (`.pptx`), or PNG/APNG/WebP images |
| `drawlib serve <html_dir> [--check]` | Start a local HTTP server for built HTML docs/slides with broken-link verification |
| `drawlib show <file> [target] [-g]` | Render and inspect a single script or embedded Markdown diagram (with optional coordinate grid) |
| `drawlib rules show [topic]` | On-demand CLI manual for AI coding agents (`overview`, `style-guide`, `review-guide`, `api`, `lib-*`) |
| `drawlib cache <list\|download\|clear>` | Manage local font, icon, map, and headless Chromium caches (`--all`, `--browser`, `--images`) |

---

## Links & Resources

- **Official Documentation**: [English (`https://www.drawlib.com/`)](https://www.drawlib.com/) | [日本語 (`https://www.drawlib.com/ja/`)](https://www.drawlib.com/ja/)
- **PyPI Package**: [https://pypi.org/project/drawlib/](https://pypi.org/project/drawlib/)
- **GitHub Repository**: [https://github.com/yuichi110/drawlib](https://github.com/yuichi110/drawlib)
- **License**: Apache License 2.0
