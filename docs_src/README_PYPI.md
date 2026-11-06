<div align="center">
  <a href="https://www.drawlib.com/">
    <img alt="Drawlib" src="https://raw.githubusercontent.com/yuichi110/drawlib/main/docs/logo/logo_transparent.png" width="340">
  </a>

  <p><strong>Pure-Python Library for "Illustration as Code" &amp; "Illustrated Documentation as Code"</strong></p>

  <p>
    <a href="https://pypi.org/project/drawlib/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/drawlib.svg"></a>
    <a href="https://pypi.org/project/drawlib/"><img alt="Python 3.11–3.13" src="https://img.shields.io/pypi/pyversions/drawlib.svg"></a>
    <a href="https://github.com/yuichi110/drawlib/actions/workflows/quality.yml"><img alt="Code Quality" src="https://github.com/yuichi110/drawlib/actions/workflows/quality.yml/badge.svg"></a>
    <a href="https://github.com/yuichi110/drawlib/actions/workflows/ut_github.yml"><img alt="Unit Tests" src="https://github.com/yuichi110/drawlib/actions/workflows/ut_github.yml/badge.svg"></a>
    <a href="https://opensource.org/licenses/Apache-2.0"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"></a>
    <a href="https://www.drawlib.com/"><img alt="Official Docs" src="https://img.shields.io/badge/Docs-www.drawlib.com-0ea5e9"></a>
    <a href="https://examples.drawlib.com/"><img alt="Live Examples" src="https://img.shields.io/badge/Examples-examples.drawlib.com-4f46e5"></a>
  </p>

  <p>
    <strong>English</strong> | <a href="https://github.com/yuichi110/drawlib/blob/main/docs_src/README_JA.md"><strong>日本語</strong></a>
  </p>
</div>

---

Drawlib is a declarative drawing library and integrated multi-format documentation compiler engineered for software developers, technical writers, and **autonomous AI coding agents**. Instead of maintaining brittle diagrams in external GUI tools (draw.io, Visio, PowerPoint) and manually pasting exported screenshots into wikis, Drawlib lets you author, animate, localize, version-control, and compile architectural diagrams, quantitative charts, technical documents (HTML / PDF / Word `.docx`), and 16:9 slide decks (PowerPoint `.pptx`) entirely from code in Git. Beyond Python projects, zero-install **`uvx drawlib`** works immediately in **any language repository (Go, Rust, TypeScript, Java, Terraform)** as well as **standalone non-code documentation and slide folders** with zero Python environment setup.

![Autonomous AI Documentation Workflow](https://www.drawlib.com/images/index/hero_ai_doc_loop.png)

- **Official Website & Documentation**: [English (`www.drawlib.com`)](https://www.drawlib.com/) | [日本語 (`www.drawlib.com/ja/`)](https://www.drawlib.com/ja/) | [Zero-Install `uvx` Guide](https://www.drawlib.com/en/01_getting_started/uvx_any_project.html) | [API & CLI Reference (`www.drawlib.com/api/`)](https://www.drawlib.com/api/) | [Internal Architecture Spec](https://www.drawlib.com/architecture/)
- **Live Examples Gallery**: [Browse All Showcase Projects (`examples.drawlib.com`)](https://examples.drawlib.com/) | [Source (`drawlib-examples`)](https://github.com/yuichi110/drawlib-examples)
  - **16:9 Slide Decks**: [About Drawlib (HTML / PDF / PPTX)](https://examples.drawlib.com/about-drawlib/en/) · [DDoS Incident Postmortem (HTML / PDF / PPTX)](https://examples.drawlib.com/ddos-incident-response/en/)
  - **Guides & Whitepapers**: [Dogfooding Whitepaper — English](https://examples.drawlib.com/dogfooding/en/) / [日本語版](https://examples.drawlib.com/dogfooding/ja/) · [Quickstart Guide (HTML / PDF / DOCX)](https://examples.drawlib.com/quickstart/en/)

---

## Try in 30 Seconds (Zero Install with `uvx`)

No `pyproject.toml`, virtual environment, or package installation required—works immediately in **any directory** (including **Go, Rust, TypeScript, Java, and Terraform** codebases, or **standalone non-development documentation/slide folders**) using [`uv`](https://docs.astral.sh/uv/):

```bash
# 1. Scaffold a bilingual documentation site (or: catalog, doc, slide, images)
uvx drawlib init project site -l en,ja

# 2. (Optional) Generate Drawlib rules for your AI coding agent (claude, cursor, antigravity, copilot, ...)
uvx drawlib init agent claude

# 3. Compile HTML site + Markdown + diagrams & launch local preview
./docs_src/build.sh
uvx drawlib serve docs_html/
```

> **Python project or global CLI?** Install with `uv add drawlib`, `uv tool install drawlib`, or `pip install drawlib`. See the [Zero-Install Workflow with `uvx` guide](https://www.drawlib.com/en/01_getting_started/uvx_any_project.html) for polyglot repository and non-code documentation patterns.

---

## Why Drawlib?

### 1. SmartArt Infographics, Quantitative Charts & Declarative Animations

Compose executive-ready infographics (`drawlib.smartarts`), quantitative data plots (`drawlib.charts`), and multi-frame **APNG / WebP** animations (`drawlib.anim`) on the exact same coordinate canvas:

![SmartArts Visual Showcase](https://www.drawlib.com/images/04_smartarts/overview/smartarts_showcase.png)

- **18 SmartArt Components (`drawlib.smartarts`)**: High-level structured layouts including `ChevronProcess`, `Cycle`, `Table`, `TreeNode`, `MindMapNode`, `Pyramid`, `BoxList`, `CardList`, `KpiCards`, `Roadmap`, `Panel`, `BulletPoints`, `GridLayout`, syntax-highlighted `SourceCode`, offline vector maps (`GeoMap`), and `MonthCalendar` / `WeekCalendar` / `DayCalendar`.

![Animated Quantitative Charts](https://www.drawlib.com/images/08_animations/charts/anim_charts_hero.png)

- **10 Quantitative Charts (`drawlib.charts`)**: Pure-Python `BarChart`, `BoxChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`, and `HeatmapChart` / `HeatmapOverlay` styled with the same design tokens as surrounding diagrams—no low-level Matplotlib boilerplate required.
- **Declarative Animations (`drawlib.anim`)**: Turn any diagram, chart, or workflow into a crisp multi-frame **APNG** or **WebP** animation (`Animation(fps=..., loop=0)`) that plays natively inside GitHub `README.md` files, pull requests, and HTML documentation sites.

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

- **34 Standardized Icon Suites (`drawlib.icons`)**: Over **4,500 offline-cached vector icons** spanning **Phosphor** (`1,512` icons across `5` weights), **Cloud Providers** (`gcp`, `aws`, `azure`), **15 Official Tech Brand Suites** (`ai`, `business`, `client`, `cloud`, `cnative`, `code`, `data`, `devops`, `facility`, `itservice`, `network`, `security`, `server`, `social`, `workspace`), and **15 Flat 2D Suites** (`original_*`).
- **Rich Primitives (`drawlib.shapes`, `lines`, `images`, `text`, `fonts`)**:
  - **43 Geometric Shapes**: Spanning `basic`, `polygon`, `arrow`, `badge`, `container`, and `symbol` primitives.
  - **Lines & Connectors**: Straight, curved (`bend`), quadratic/cubic Bezier, and rounded polylines with rich arrowheads (`"->"`, `"<-"`, `"<->"`).
  - **Images & Nested Canvases**: Non-destructive `Dimage` transformations (`crop()`, `sepia()`, `grayscale()`, `mosaic()`, `mirror()`) plus in-memory diagram nesting via `get_dimage_from_code()`.
  - **Multilingual Typography**: Automatic on-demand font caching (`FontRoboto`, `FontSansSerif`, `FontSerif`, `FontSourceCode`, `FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, etc.).
- **7-Role Semantic Style System (`drawlib.styles`)**:
  - 6 built-in themes (`default`, `google`, `essentials`, `monochrome`, `warm`, `cold`) accessed via `Styles.<Token>` (`Styles.Neutral`, `Styles.PrimaryFlat`, `Styles.SecondaryNeutral`, `Styles.MutedDashed`, `Styles.SuccessNeutral`, `Styles.WarningNeutral`, `Styles.DangerNeutral`).

---

### 4. Illustrated Documentation & 16:9 Slide Deck as Code (Multi-Locale & SEO Ready)

Author Markdown files with embedded ```` ```drawlib ```` code fences inside a unified `drawlib.toml` project. A single build compiles your repository into web portals, GitHub Markdown, PDFs, editable Word documents, HTML slide decks, and PowerPoint files:

![Multi-Locale Documentation and Slide Build Pipeline](https://www.drawlib.com/images/01_getting_started/project_quicklook/doc_build_pipeline.png)

- **Unified `drawlib.toml`, Multi-Locale (`[i18n]`) & Declarative SEO (`[seo]`)**: Configure `[project]` metadata, `[i18n]` locales (`langs = ["en", "ja"]` with structural parity checks), `[seo]` publishing (`site_url`, Open Graph / X social cards, `hreflang`, `sitemap.xml`, `robots.txt`, and AI-ready `llms.txt`), and `[catalog]` reference navigation directly in `drawlib.toml`.
- **5 Project Scaffolds (`drawlib init project <type>`)**:
  - `drawlib init project site [-l en,ja]`: Multi-page documentation website (`docs_html/` with language switcher, search, and sidebar TOC) and GitHub Markdown (`docs_markdown/`).
  - `drawlib init project catalog [-l en,ja]`: Illustrated catalog & reference website (`catalog_html/` with automatic `# H1` / `## H2` sidebar extraction, 50+ semantic badges, and `/` instant filter) for APIs, CLI references, schemas, and service registries.
  - `drawlib init project doc [-l en,ja]`: Linear technical specification or whitepaper (`*_html/`, `*_markdown/`, vector `*_<lang>.pdf`, plus editable MS Word `*_<lang>.docx` via `./<target>_src/build_docx.sh` or `drawlib build docx`).
  - `drawlib init project slide [-l en,ja]`: 16:9 presentation slide deck (`::: block` + `::: note` speaker notes) with native SVG typography, Presenter View, keyboard navigation (`slide_html/`), vector `slide_<lang>.pdf`, and editable MS PowerPoint `slide_<lang>.pptx` via `./<target>_src/build_pptx.sh` or `drawlib build pptx`.
  - `drawlib init project images`: Standalone batch Python illustration scripts (`images_src/` -> `images/`) backed by sub-millisecond `.drawlib/cache.db` incremental caching.
- **AI Inner Loop & Human Outer Loop (`drawlib init agent <agent>`)**: Built from the ground up for AI coding agents (Claude Code, Cursor, Antigravity, Copilot, Windsurf, Cline, Roo, Codex, Gemini). Generate native workspace instruction files in one command (`drawlib init agent claude`), while agents query `drawlib rules show <topic>` on demand, render headless coordinate-grid previews via `drawlib show -g`, and multimodally self-correct text clipping or layout defects—freeing engineers to focus on high-level architecture and review.

---

## Installation

![Drawlib Environment & AI Agent Setup Workflow](https://www.drawlib.com/images/01_getting_started/installation/installation_setup_workflow.png)

Run `drawlib` instantly with zero installation via `uvx`, or install from PyPI into your Python project or global CLI environment (Python `>= 3.11`):

```bash
# Zero-install CLI (ideal for quick try & non-Python repos: Go, Rust, TypeScript, Java)
uvx drawlib --version

# Add to a Python uv project (for importing `drawlib.*` in scripts/tests)
uv add drawlib

# Or install globally as a persistent CLI tool / via pip
uv tool install drawlib   # or: pip install drawlib
```

### Configure AI Agent Instructions *(Optional — Strongly Recommended)*

If you author code or documentation with an AI coding agent (**Claude Code**, **Cursor**, **Antigravity**, **GitHub Copilot**, **Windsurf**, **Cline**, **Roo Code**, **OpenAI Codex**, or **Gemini CLI**), initialize workspace agent instructions right after setup (prefix with `uvx` or `uv run` as needed) so your agent automatically follows Drawlib's bottom-left `(0, 0)` coordinate space, `50%+` neutral style discipline, `drawlib init project` scaffolding, and 3-stage visual self-correction loop:

```bash
drawlib init agent list                   # List supported agents & target file paths
drawlib init agent claude                 # -> .claude/rules/drawlib.md
drawlib init agent cursor                 # -> .cursor/rules/drawlib.mdc
drawlib init agent antigravity            # -> .agents/rules/drawlib.md
drawlib init agent claude cursor copilot  # Initialize multiple agents (or 'all')
```

### Zero-Config Export & Offline Caching

PDF, MS Word (`.docx`), and MS PowerPoint (`.pptx`) export work out of the box—`playwright`, `python-docx`, and `python-pptx` are standard dependencies, and headless Chromium (`chromium-headless-shell`) downloads automatically on your first `drawlib build pdf` or `drawlib build pptx` run.

- **Offline / Air-Gapped / CI Environments**: Pre-download all fonts, icons, maps, and headless Chromium ahead of time with `drawlib cache download --all` (or Chromium only with `drawlib cache download --browser`).
- **Minimal Linux Containers** (e.g., `python:3.12-slim` lacking OS shared libraries such as `libnss3` or `libgbm1`): Install OS browser dependencies once via `playwright install-deps chromium` (or `playwright install --with-deps --only-shell chromium`).

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

Run the script to generate `client_server.png`:

```bash
# Zero-install via uvx (works anywhere without project setup)
uvx drawlib show client_server.py -o client_server.png

# Or inside a Python uv project (`uv add drawlib`)
uv run python client_server.py
```

#### Core Principles at a Glance
- **Bottom-Left Origin `(0, 0)`**: `setup(width=100, height=44)` defines a Cartesian coordinate canvas where `x` spans `0..100` (left to right) and `y` spans `0..44` (bottom to top).
- **Predictable Coordinate Anchors**: Core primitives (`rectangle`, `circle`, `icon`, `image`, `text`) anchor at their **center `(cx, cy)`** for effortless alignment, while high-level `Charts` and `Diagrams` anchor at **bottom-left `(x0, y0)`**.
- **50%+ Neutral Baseline**: Ground supporting shapes in calm neutral tokens (`Styles.Neutral`, `Styles.SecondaryNeutral`, `Styles.MutedDashed`) and reserve saturated fills (`Styles.PrimaryFlat`) for 1–2 focal elements.
- **Non-Destructive Style Patching (`.patch()`)**: Customize any preset token cleanly via `Styles.MutedBold.patch(text_size=10)` or `Styles.Primary.patch(shape_line_width=2)`.

---

### 2. Illustrated Documentation & Slide Deck Workflow

Scaffold a multi-page documentation site, linear whitepaper, or 16:9 slide deck in seconds (pass `-l en,ja` for multi-locale `<src_dir>/<lang>/` projects; prefix with `uvx` if running zero-install):

```bash
# Initialize a bilingual multi-page documentation site in docs_src/ (en/ & ja/)
drawlib init project site -l en,ja

# Or initialize a 16:9 presentation slide deck in slide_src/
drawlib init project slide -l en,ja

# Generate AI coding agent instructions for your IDE / CLI agent
drawlib init agent claude
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

Compile, export, and preview with the generated scripts (which automatically detect `uv run drawlib`, `drawlib`, or `uvx drawlib`) or the CLI:

```bash
# Build HTML site, GitHub Markdown, or PDF via generated build script
./docs_src/build.sh

# Export editable MS Word (.docx) or MS PowerPoint (.pptx) per locale
./doc_src/build_docx.sh      # or: drawlib build docx doc_src/ -o spec.docx --generate-index
./slide_src/build_pptx.sh    # or: drawlib build pptx slide_src/ -o deck.pptx

# Launch local HTTP server with pre-flight broken-link verification
drawlib serve docs_html/ --check

# Render a single diagram with coordinate grid (-g) for visual layout inspection
drawlib show docs_src/en/index.md service_routing.png -g -o preview_grid.png
```

---

### 3. CLI Reference Summary

| Command | Description |
| :--- | :--- |
| `drawlib init project <site\|catalog\|doc\|slide\|images\|list> [-l <langs>]` | Scaffold a documentation site, catalog/reference, linear spec, 16:9 slide deck, or image project (`drawlib.toml`) |
| `drawlib init agent <agent...\|all\|list> [-m <auto\|always>]` | Generate workspace rule/instruction files for AI coding agents (`claude`, `cursor`, `antigravity`, `copilot`, `windsurf`, `cline`, `roo`, `codex`, `gemini`) |
| `drawlib build <html\|markdown\|pdf\|docx\|slide\|pptx\|image>` | Compile sources into HTML, Markdown, PDF, MS Word (`.docx`), HTML Slides, MS PowerPoint (`.pptx`), or PNG/APNG/WebP images |
| `drawlib serve <html_dir> [--check]` | Start a local HTTP server for built HTML docs/slides with broken-link verification |
| `drawlib show <file> [target] [-g]` | Render and inspect a single script or embedded Markdown diagram (with optional coordinate grid) |
| `drawlib css <list\|show> [target] [preset] [-o <file>]` | List, preview, or export built-in CSS theme stylesheets (`html`, `catalog`, `slide`, `pdf`) |
| `drawlib rules show [topic]` | On-demand CLI manual for AI coding agents (`overview`, `style-guide`, `review-guide`, `api`, `lib-*`) |
| `drawlib cache <list\|download\|clear>` | Manage local font, icon, map, and headless Chromium caches (`--all`, `--browser`, `--images`) |

---

## Links & Resources

- **Official Documentation**: [English (`https://www.drawlib.com/`)](https://www.drawlib.com/) | [日本語 (`https://www.drawlib.com/ja/`)](https://www.drawlib.com/ja/) | [API & CLI Reference (`https://www.drawlib.com/api/`)](https://www.drawlib.com/api/) | [Internal Architecture Spec (`https://www.drawlib.com/architecture/`)](https://www.drawlib.com/architecture/)
- **Live Examples Gallery**: [https://examples.drawlib.com/](https://examples.drawlib.com/) ([`yuichi110/drawlib-examples`](https://github.com/yuichi110/drawlib-examples))
- **Release Notes & Changelog**: [English](https://www.drawlib.com/en/01_getting_started/release_notes.html) | [日本語](https://www.drawlib.com/ja/01_getting_started/release_notes.html)
- **Contributor & Developer Guide**: [`CONTRIBUTING.md`](https://github.com/yuichi110/drawlib/blob/main/.github/CONTRIBUTING.md) | [`docs_src/README_DEV.md`](https://github.com/yuichi110/drawlib/blob/main/docs_src/README_DEV.md)
- **PyPI Package**: [https://pypi.org/project/drawlib/](https://pypi.org/project/drawlib/)
- **GitHub Repository**: [https://github.com/yuichi110/drawlib](https://github.com/yuichi110/drawlib)
- **License**: Apache License 2.0
