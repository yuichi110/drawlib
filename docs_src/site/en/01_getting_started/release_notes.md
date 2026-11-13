# Release Notes & Migration Guide

## Version 0.3.10

*Release Date: 2026/11/13*

Version 0.3.10 introduces **interactive animation range looping (`anim_pause=(0-3, 4-7)`) for 16:9 HTML slide decks**, allowing presentations to continuously loop specific frame segments (such as steady-state data flows or request/response cycles) and advance immediately to the next phase on click, `A` key, or Presenter View's `⏭ Next Step` control, alongside **documentation portal analytics and updated bilingual guides**.

---

### Highlights & New Features

#### 1. Interactive Slide Animation Range Looping (`anim_pause=(0-3, 4-7)`, `slide`)
- **Hyphenated Frame Range Syntax (`options.py`, `_assets.py`)**: Extended `anim_pause` on ```` ```drawlib ```` slide code blocks to accept 0-based hyphenated loop ranges (`start-end`, where `0 <= start < end`) in addition to single pause frames (`0`, `2`, `4`), freely combinable in a single declaration such as `anim_pause=(0, 1-4, 5-8)`.
- **Canvas-Driven Loop Engine & Instant Advance (`slide.js`, `slide.css`)**: Added a dedicated `LOOPING` playback state to the HTML slide `<canvas>` WebP/GIF frame engine. When playback reaches `end` of an active `start-end` range, the engine wraps seamlessly back to `start` until the presenter clicks the canvas, presses `A`, or triggers `⏭ Next Step` in Presenter View (`?presenter=1`), which immediately jumps to frame `end + 1` without waiting for the end of the cycle (while keeping `→` / `Space` strictly bound to slide navigation). Hovering over a looping animation reveals the `▶Click` badge as an interactive cue.

#### 2. Documentation Portal Analytics & Bilingual Guide Updates
- **Documentation Portal Enhancements (`docs_src/`)**: Added Google Analytics (`gtag.js`) integration across documentation templates (`site`, `api`, `architecture`) and expanded bilingual documentation and AI agent rules (`anim-guide`, `project-slide`, `08_animations/overview`, `09_doc_builder_and_cli/code_blocks`, and `09_doc_builder_and_cli/project_slide`) with range-loop patterns and state machine specifications.

---

## Version 0.3.9

*Release Date: 2026/11/08*

Version 0.3.9 introduces **secant-aligned curved arrowhead rendering with exact de Casteljau Bezier subdivision** across all curved line and diagram primitives, **offset side anchors (`top_right`, `top_left`, `bottom_right`, `bottom_left`) on normal `StateDiagram` transitions**, and **non-fatal `[Geometry Warning]` arrowhead clearance diagnostics in `drawlib show`**, alongside updated AI agent geometry rules and refined orthogonal routing across bilingual documentation.

---

### Highlights & New Features

#### 1. Secant-Aligned Curved Arrowheads & `StateDiagram` Offset Anchors (`l4_canvas`, `diagrams.state`)
- **Secant Orientation & de Casteljau Tip Subdivision (`_SecantCurveArrowStyle`)**: Curved arrow lines (`line_curved`, `line_bezier1`, `line_bezier2`, `line_arc`, `lines_curved`, and curved `lines_bezier`) now align arrowhead wings along the secant vector from `P_base` (one `head_length` back along the curve) to the retracted tip `P_tip`, while subdividing the underlying Bezier shaft via de Casteljau's algorithm. Curved shafts stay cleanly centered between both wings on tight or short arcs without requiring manual angle parameters or shrinking arrowhead scale.
- **Bidirectional Offset Side Anchors in `StateDiagram` (`_state_node.py`, `_render_transition.py`)**: Normal `StateDiagram.connect(...)` transitions now resolve `"top_right"`, `"top_left"`, `"bottom_right"`, and `"bottom_left"` perimeter offsets (`±0.35` along the secondary axis) on box, ellipse, circle, and diamond state nodes, cleanly separating opposing `A <-> B` transition arcs on compact cards.

#### 2. Non-Fatal Arrowhead Clearance Geometry Warnings (`drawlib show`)
- **Terminal Segment Footprint Checker (`LineUtils.check_arrowhead_segment_warnings`)**: `Canvas` now evaluates rendered `FancyArrowPatch` paths against Drawlib's `720pt` reference canvas geometry and prints non-fatal `[Geometry Warning]` messages to `stderr` during `drawlib show` whenever an orthogonal corner's final segment (or total line/curve length) is shorter than the arrowhead's physical footprint—preserving declarative `line_arrow_head_scale` uniformity without failing builds.

#### 3. AI Agent Geometry Rules & Bilingual Documentation Refinements
- **Stage 2 Orthogonal Clearance Guidance (`_rules/`)**: Updated `review-guide`, `lib-lines`, `lib-graph-layer`, `lib-graph-tree`, `lib-diagrams-state`, and `drawlib init agent` workspace instructions with `[Geometry Warning]` verification and minimum orthogonal routing gap guidelines (`>= 6.0` units for midpoint Z-routing).
- **Documentation Diagram Polish (`docs_src/`)**: Refined orthogonal fork positions, rank/level separations, and mini-card arrowhead scales across bilingual `site`, `api`, `architecture`, and `readme` diagrams to achieve zero geometry warnings repo-wide.

---

## Version 0.3.8

*Release Date: 2026/11/07*

Version 0.3.8 introduces **multi-core parallel diagram rendering (`-w` / `--workers`, `DRAWLIB_BUILD_WORKERS`)** across all 7 `drawlib build` CLI subcommands and programmatic `build_*` APIs—accelerating cold builds by **3x–6x** on multi-core machines while keeping warm-cache builds instantaneous—alongside **cross-process asset download locking & atomic Zip-Slip-safe archive extraction** and **official Python 3.14 support (`Python 3.11–3.14`)**.

---

### Highlights & New Features

#### 1. Multi-Core Parallel Rendering Across All 7 `drawlib build` Targets (`-w` / `--workers`, `DRAWLIB_BUILD_WORKERS`)
- **2-Phase Multi-Process Pre-Renderer (`_builder._common.parallel`)**: Uncached embedded ```` ```drawlib ```` code blocks and standalone `.py` scripts now render concurrently across isolated `spawn` `ProcessPoolExecutor` worker processes (`html`, `markdown`, `pdf`, `docx`, `slide`, `pptx`, and `image`) using **Longest-Job-First** scheduling (prioritizing multi-frame `Animation` blocks) and cross-locale shared diagram deduplication. Non-daemonic workers preserve full compatibility with nested `get_dimage_from_code()` subprocesses.
- **Smart `"auto"` Concurrency & Zero-Overhead Warm Cache**: Defaults to `-w auto` / `workers="auto"`, automatically resolving to **`1 <= (CPU cores - 1) <= 8`** (overridable via `-w <N>`, `workers=<N>`, or `DRAWLIB_BUILD_WORKERS=<N>`; `-w 1` runs sequentially in-process). When `<= 1` cache misses remain, process pool startup is bypassed entirely for sub-millisecond warm-cache rebuilds, while all `.drawlib/cache.db` SQLite WAL writes stay serialized in the parent process (and `BuildImageCache.prerendered_blobs` eliminates duplicate rendering during `--no-cache` inline `pdf` / `docx` builds).

#### 2. Cross-Process Asset Locking & Atomic Zip-Slip-Safe Extraction (`l3_external`)
- **Cross-Process Advisory File Lock (`_download.py`)**: Added per-package cross-process advisory locks (POSIX `fcntl.flock` and Windows `msvcrt.locking` under `<cached_assets>/.locks/`, with XDG / `LOCALAPPDATA` / tempdir fallbacks for read-only containers) plus post-lock checksum re-verification so parallel build workers never race on first-run font, icon, or GeoMap downloads.
- **Zip-Slip Guard & Atomic File Replacement (`_package.py`)**: Hardened `ReleaseAssetPackage.download_and_extract()` with strict `Path.is_relative_to()` archive entry boundary checks and atomic `.tmp_<pid>_<tid>_*` + `os.replace()` writes so concurrent readers never observe partially written font or icon files.

#### 3. Official Python 3.14 Runtime Support (`Python 3.11–3.14`)
- **Verified Cross-Platform Python 3.14 Compatibility**: Added official `Programming Language :: Python :: 3.14` package metadata, expanded Linux/Windows/macOS GitHub Actions test matrices and `./dcli docker` clean-room container testing to Python `3.11`–`3.14`, modernized AST string/constant node checks (`ast.Constant`), and preserved `__spec__` across `drawlib.utils` module resets for `importlib.reload()` compatibility.

---

## Version 0.3.7

*Release Date: 2026/11/07*

Version 0.3.7 introduces **dither-free Animated & Static GIF export (`.gif`)** across `Animation`, `canvas.save()`, Markdown code fences, and CLI batch builds for universal social, presentation, and wiki playback, alongside **cross-platform parallel headless Chromium locking**, **localized external `navbar.md` URL validation**, and **multi-portal SEO / `llms.txt` discovery enhancements**.

---

### Highlights & New Features

#### 1. Dither-Free Animated & Static GIF Export (`Animation`, `save("*.gif")`, `drawlib build image -f gif`)
- **Crisp Diagram-Tuned Palette Quantization (`l3_images._gif`)**: Added native `.gif` export (`ImageFormat` includes `"gif"`, `"apng"`, and `"svg"`) powered by Median Cut 256-color quantization with dithering disabled (`Image.Quantize.MEDIANCUT` + `Image.Dither.NONE`), preserving flat `Styles.Neutral` surfaces and anti-aliased text without Floyd-Steinberg grain noise.
- **End-to-End Animation, Markdown & CLI Support**: Export multi-frame GIF animations via `save("flow.gif")` or `save("flow", format="gif")` (with automatic `10ms` GIF tick rounding and reserved palette index `255` + `disposal=2` 1-bit transparency on transparent canvases), embed `file=demo.gif` / `format=gif` inside Markdown ```` ```drawlib ```` blocks (with automatic static PNG extraction for `.docx` / `.pptx`), and batch-render via `drawlib build image -f gif`.

#### 2. Cross-Platform Parallel Browser Locking & Multi-Locale Navbar Parity
- **Cross-Process Headless Chromium Locking & Sentinel Verification (`browser.py`)**: Extended `_browser_install_lock()` with Windows `msvcrt.locking` support alongside POSIX `fcntl.flock`, and added post-lock `INSTALLATION_COMPLETE` sentinel verification so parallel workers (such as `pytest-xdist` or concurrent PDF/PPTX builds) safely serialize first-time `chromium-headless-shell` downloads and skip redundant CLI invocations.
- **Localized External Navbar Links (`i18n.py`)**: Multi-locale `site` parity validation now permits localized `/{lang}/` path segments in external `navbar.md` URLs (for example, linking to `/api/en/` in `en/navbar.md` and `/api/ja/` in `ja/navbar.md`).

#### 3. CLI, Scaffolding, SEO Discovery & Documentation Refinements
- **Catalog Scaffolding & CLI Help Polish**: Updated `drawlib init project` help descriptions and `catalog` project build script progress messages (`Catalog HTML`), and refined Bezier/line coordinate tuple narrowing in `l3_math` and `l4_canvas`.
- **Multi-Portal Sitemap & `llms.txt` Discovery**: Root `robots.txt` and `llms.txt` on `www.drawlib.com` now reference `/api/` and `/architecture/` sitemaps and LLM discovery indexes, alongside updated `BoxChart` (10-chart) and 15 tech-brand icon suite references across GitHub and PyPI READMEs.

---

## Version 0.3.6

*Release Date: 2026/11/06*

Version 0.3.6 introduces **`BoxChart` and `BoxStats` (`drawlib.charts.box`)**—a unified statistical distribution chart engine for box plots, strip/jitter plots, and hybrid benchmark overlays—alongside **supply-chain security hardening, non-root container images, and offline reliability enhancements** validated by the PNI501 full engineering audit.

---

### Highlights & New Features

#### 1. Statistical Box Plots, Strip Plots & Hybrid Overlays (`drawlib.charts.box`, `BoxChart`, `BoxStats`)
- **Unified 3-Mode Distribution Builder (`show_box`, `show_points`, `show_outliers`, `show_mean`)**: Visualize categorical numerical dispersion as classic **Box Plots** (`show_box=True, show_points=False`), **1D / Jittered Strip Plots** (`show_box=False, show_points=True`), or **Box + Strip Hybrid Overlays** (`show_box=True, show_points=True`—ideal for $N = 5 \sim 30$ PoC and latency benchmarks), with defaults configurable on `BoxChart` and overridable per series via `add_series(...)`.
- **Raw Sample Arrays & Pre-Aggregated `BoxStats` (`whisker_mode="iqr" | "min_max" | "percentile"`)**: Pass raw `Sequence[float]` samples for pure-Python inclusive quartile calculation (`iqr_k=1.5` Tukey fences, full `min_max`, or custom tail-latency `whisker_percentiles=(5.0, 95.0)`), or pass pre-computed `BoxStats(min=..., q1=..., median=..., q3=..., max=..., mean=..., outliers=...)` directly from BigQuery or Cloud Monitoring telemetry.
- **Process- & Animation-Invariant Deterministic Jitter & High-Contrast Auto-Styling**: Generates reproducible transverse offsets per `(jitter_seed, series_idx, category_idx)` without touching global RNG state, automatically derives contrasting whisker/median/marker colors from a single `Style` token (`Styles.PrimaryNeutral`, `Styles.PrimaryFlat`, etc.), and supports `"vertical"` / `"horizontal"` layouts, `scale="log"` axes, `draw_ratio` animations, and `drawlib rules show lib-charts-box`.

#### 2. Supply-Chain Security Hardening, Non-Root Containers & Offline Reliability
- **Dependency & Container Hardening**: Upgraded `pillow>=13.0.0` to eliminate upstream image-processing CVEs and hardened all production and clean-room test Dockerfiles to execute under non-root `USER drawlib` (`UID 10001`).
- **Air-Gapped Asset Pre-Validation & Audit Report ([`/reports/pni-full-audit/`](https://www.drawlib.com/reports/pni-full-audit/))**: Added `pkg.files` membership pre-validation before network downloads for `--network=none` environments, refined SQLite build cache connection handling, and published the [PNI501 Engineering & Security Audit Report](https://www.drawlib.com/reports/pni-full-audit/).

---

## Version 0.3.5

*Release Date: 2026/11/03*

Version 0.3.5 introduces the 5th project archetype—**Illustrated Catalog & Reference (`catalog`, `drawlib init project catalog`)**—designed for API/CLI references, data schemas, microservice registries, and operational runbooks, alongside **Declarative Project SEO & `llms.txt` generation (`[seo]`)**, **zero-install `uvx` build script fallbacks**, and the **Official Bilingual Python API & CLI Reference (`/api/`)**.

---

### Highlights & New Features

#### 1. Illustrated Catalog & Reference Project Archetype (`catalog`, `drawlib init project catalog`)
- **Zero-Navbar 2-Column Catalog Builder (`1 Markdown = 1 HTML Page`)**: Scaffold `catalog` projects via `drawlib init project catalog [target] [-l en,ja] [-s google]` (`drawlib.tools.init_project("catalog", ...)`). Each Markdown file in `<src_dir>/<lang>/` automatically becomes a collapsible `# H1` sidebar category (`<details class="catalog-nav-group">`) with `## H2` entries linked as `#slug` items and tracked via live scroll-spy—no manual `navbar.md` maintenance required.
- **50+ Semantic `H2` Badges & `/` Instant Filter**: Prefix `## ` headings with inline backtick tokens—covering HTTP (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `gRPC`), code/CLI (`def`, `class`, `type`, `cmd`, `flag`, `env`, `config`), data/infra (`table`, `schema`, `service`, `job`, `pipeline`, `metric`), design/governance (`token`, `style`, `icon`, `adr`, `rule`), and operational status (`ok`, `warn`, `error`, `deprecated`)—to render color-coded pills in both the page body and sidebar, paired with `/` keyboard incremental filtering.
- **Declarative `[catalog]` Customization & Dedicated CSS Target**: Configure `sidebar_expanded`, `badge_text`, `badge_url`, `breadcrumb_root`, `repo_url`, and `[[catalog.header_links]]` in `drawlib.toml`, inspect or export catalog stylesheets via `drawlib css list|show catalog` (`get_css(target="catalog")`, `export_css(target="catalog")`), and access authoring guidance via `drawlib rules show project-catalog`.

#### 2. Declarative Project SEO, Open Graph & `llms.txt` Generation (`[seo]`, `[i18n.descriptions]`)
- **Turnkey Search & Social Metadata Across `site`, `doc`, `catalog`, and `slide`**: Configure `[seo]` (`site_url`, `og_image`, `twitter_card`, `twitter_site`, `sitemap`, `robots`, `llms_txt`) and `[i18n.descriptions]` in `drawlib.toml` to automatically emit `<meta name="description">`, `<link rel="canonical">`, multi-locale `hreflang` & `og:locale` alternates, Open Graph / X Card tags, `sitemap.xml`, `robots.txt`, and `llms.txt` (alongside `.nojekyll` and `CNAME` deployment assets on `www.drawlib.com`).
- **AI-Ready `llms.txt` Discovery Index**: Automatically generates a clean `llms.txt` index summarizing site structure, localized entry URLs, and page descriptions so LLM agents and search crawlers can navigate compiled documentation sites effortlessly.

#### 3. Zero-Install `uvx` Fallback Scripts & Official Bilingual API Reference (`/api/`, `/architecture/`)
- **Polyglot Zero-Install Build & Preview Scripts (`uvx drawlib`)**: Scaffolded `build*.sh` and `serve.sh` scripts now detect `uv run drawlib` first and automatically fall back to `uvx drawlib` (or global `drawlib`), enabling zero-Python-setup diagram and documentation builds inside Go, Rust, TypeScript, Java, or standalone Git repositories.
- **Official Bilingual Python API & CLI Reference & Architecture Portal**: Published a 100% complete bilingual (`en`/`ja`, 29 modules & CLI pages) API & CLI Reference at `https://www.drawlib.com/api/` dogfooding the new `catalog` archetype, alongside the internal Software Architecture Specification at `https://www.drawlib.com/architecture/`.

---

## Version 0.3.4

*Release Date: 2026/11/02*

Version 0.3.4 introduces a one-command **AI Agent Workspace Instruction Initializer (`drawlib init agent`)** supporting 9 major AI coding assistants, reorganizes `drawlib init` into a symmetrical **`drawlib init project` / `drawlib init agent`** CLI hierarchy, and adds executable **MS Word (`build_docx.sh`)** and **MS PowerPoint (`build_pptx.sh`)** build scripts to project scaffolds.

---

### Highlights & New Features

#### 1. AI Agent Workspace Instruction Initializer (`drawlib init agent`, `drawlib.tools.init_agent_instruction`)
- **9 Native AI Coding Agent Targets**: Generate ready-to-use workspace instruction files in one command via `drawlib init agent <target...|all|list>` for **Antigravity** (`.agents/rules/drawlib.md`), **Claude Code** (`.claude/rules/drawlib.md`), **Cursor** (`.cursor/rules/drawlib.mdc`), **GitHub Copilot** (`.github/instructions/drawlib.instructions.md`), **Windsurf** (`.windsurf/rules/drawlib.md`), **Cline** (`.clinerules/drawlib.md`), **Roo Code** (`.roo/rules/drawlib.md`), **OpenAI Codex** (`AGENTS.md`), and **Gemini CLI** (`GEMINI.md`).
- **Context-Aware Trigger Modes & Idempotent Root File Merging**: Supports `--mode auto|always` (defaulting to context-aware `auto` with `.py`, `drawlib.toml`, and `.md` file globs while staying compact under `< 10 KB` for strict IDE limits), safe overwrite protection (`--force`), and non-destructive `<!-- drawlib:begin -->` / `<!-- drawlib:end -->` marker updates when appending to existing `AGENTS.md` or `GEMINI.md` files.
- **Programmatic Python API (`drawlib.tools`)**: Added `init_agent_instruction()`, `list_agent_targets()`, `detect_agent_targets()`, and `AgentTargetInfo` for automated workspace tooling.

#### 2. Symmetrical `drawlib init` CLI Hierarchy & Executable Office Build Scripts
- **Symmetrical `drawlib init project` & `drawlib init agent` Subcommands**: Unified initialization workflows under `drawlib init project <doc|site|slide|images|list>` for project scaffolding and `drawlib init agent <agent...|all|list>` for AI agent configuration.
- **Executable `build_docx.sh` & `build_pptx.sh` Template Scripts**: Scaffolding `doc` (`drawlib init project doc`) and `slide` (`drawlib init project slide`) projects now generates executable (`chmod +x`) `build_docx.sh` and `build_pptx.sh` helper scripts alongside `build.sh` for turnkey `.docx` and `.pptx` generation.

#### 3. Documentation, README & Asset Enhancements
- **Refreshed GitHub & PyPI READMEs and Installation Guide**: Added animated APNG/PNG feature showcases, post-installation AI agent setup guidance (`Optional — Strongly Recommended`), and OGP / GitHub Social Preview banner generation (`docs/ogp_src/`).

---

### Breaking Changes & Migration from v0.3.3

1. **Project Scaffolding CLI Subcommands Moved Under `drawlib init project`**:
   - Top-level `drawlib init <doc|site|slide|images|list>` commands have moved to `drawlib init project <doc|site|slide|images|list>`:
   ```bash
   # Before (v0.3.3 and earlier)
   drawlib init site -l en,ja
   drawlib init list

   # Now (v0.3.4+)
   drawlib init project site -l en,ja
   drawlib init project list
   ```
   - The programmatic Python API `drawlib.tools.init_project()` remains unchanged.

---

## Version 0.3.3

*Release Date: 2026/11/01*

Version 0.3.3 introduces a unified **`drawlib.toml` project manifest** and **`i18n`-native `<src_dir>/<lang>/` multi-locale architecture** across all documentation (`doc`), website (`site`), and presentation (`slide`) projects, alongside full **English/Japanese (`en`/`ja`) official documentation** and **animated parameter tours**.

---

### Highlights & New Features

#### 1. Unified Project Manifest (`drawlib.toml`) & Multi-Locale `i18n` Architecture
- **Declarative `drawlib.toml` Manifest**: Unifies `[project]` metadata and `[i18n]` locale configuration (`default_lang`, `langs`, and optional `[i18n.labels]`) across `doc`, `site`, and `slide` archetypes (and `[project].lang` on `images`). Scaffold single- or multi-locale projects directly via `drawlib init <doc|site|slide> [-l en,ja]` or `drawlib.tools.init_project(..., lang="en,ja")`.
- **Unified `<src_dir>/<lang>/` Layout & Structural Parity Validation**: Every `doc`, `site`, and `slide` project organizes Markdown sources under `<src_dir>/<lang>/` with optional per-locale `<lang>/styles.py` and `<lang>/utils.py` overrides. Pre-flight validation verifies identical relative file paths, Markdown heading hierarchies (`#`–`######`), and ````drawlib```` `file=` blocks across all configured locales, while language-neutral diagrams render once and share `<output>/images/` across locales.
- **Multi-Locale 16:9 Slide Decks (`drawlib build slide`, `drawlib build pptx`, `drawlib build pdf`)**: Interactive HTML slide decks now include an upward-opening `.slide-lang-dropdown` language switcher in the bottom controls bar (`L` keyboard shortcut) that preserves the current `#N` slide hash across locales, a browser-language root `index.html` redirector, and per-locale PDF / PPTX deliverables.
- **Locale-Aware Typography, `hreflang` SEO & Consistent Output Naming**: Automatically injects `<html lang="..." dir="ltr|rtl">`, `<link rel="alternate" hreflang="...">` tags, CJK/RTL CSS typography rules (`line-break: strict`, zero heading letter-spacing), localized font presets (`FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, etc.), and unified `<stem>_<lang>.{pdf,docx,pptx}` deliverable filenames.

#### 2. Bilingual EN/JA Official Documentation & Animated Parameter Tours
- **Bilingual Official Documentation & Dogfooding Whitepaper**: Published complete English (`en/`) and Japanese (`ja/`) editions of the official documentation portal and the Dogfooding whitepaper with in-page language switching.
- **Animated Parameter Tours (`drawlib.anim`)**: Added lossless APNG parameter tour animations across geometric primitives, icons, SmartArts, quantitative charts, domain diagrams, auto-layout graphs, and builder workflows.

#### 3. Bug Fixes & Internal Improvements
- Fixed a circular import between `drawlib._release_assets` and `drawlib._core.l3_external` when `drawlib._release_assets` was imported prior to `drawlib._core`.

---

### Breaking Changes & Migration from v0.3.2

If you have existing `doc`, `site`, or `slide` directory projects created in v0.3.2 or earlier, migrate them to the unified `i18n`-native layout:

1. **Add `drawlib.toml` with `[i18n]` & Move Markdown Sources Under `<src_dir>/<lang>/`**:
   - Legacy flat directory layouts (`doc_src/*.md`, `docs_src/*.md`, `slide_src/*.md`) and standalone `i18n.toml` / `i18nsite` configurations have been replaced by `drawlib.toml` + `<src_dir>/<lang>/` (even for single-locale `langs = ["en"]` projects). Single `.md` file builds (e.g., `drawlib build html report.md`, `drawlib build pdf report.md`) remain unchanged.
   ```toml
   [project]
   type = "site" # or "doc" / "slide"
   style = "default"

   [i18n]
   default_lang = "en"
   langs = ["en"] # or ["en", "ja"]
   ```
   - Move `*.md` (including `navbar.md` for `site`) into `<src_dir>/en/`, while keeping shared `styles.py`, `utils.py`, `_assets/`, `template.html`, `style.css`, and `slide.js` at the `<src_dir>/` root.
2. **Locale-Suffixed Deliverable Paths (`<stem>_<lang>.{pdf,docx,pptx}` & `<output_dir>/<lang>/`)**:
   - Directory builds of `doc`, `site`, and `slide` now always emit locale-suffixed files—for example, `doc_en.pdf`, `doc_en.docx`, `slide_en.pdf`, and `slide_en.pptx`—and place HTML / Markdown pages under `<output_dir>/<lang>/` with an automatic root `index.html` redirector at `<output_dir>/index.html`.

---

## Version 0.3.2

*Release Date: 2026/10/30*

Version 0.3.2 introduces native editable **MS Word (`.docx`)** and **MS PowerPoint (`.pptx`)** exporters, promotes **headless Chromium, `python-docx`, and `python-pptx`** into unified zero-config standard dependencies, and reorganizes embedded AI agent rules into modular category directories.

---

### Highlights & New Features

#### 1. MS Word (`.docx`) & MS PowerPoint (`.pptx`) Export (`drawlib build docx`, `drawlib build pptx`)
- **`drawlib build docx` & `drawlib.tools.build_docx()`**: Compiles linear `doc` projects or single `.md` files into native editable MS Word (`.docx`) documents—complete with styled headings, prose, bullet/numbered lists, tables, blockquotes, syntax-highlighted code blocks, optional cover page, and automated Table of Contents (`--generate-index`)—rendering ````drawlib```` blocks (including SVG, WebP, and animated blocks) as crisp high-DPI static PNGs (`--dpi 200` default).
- **`drawlib build pptx` & `drawlib.slide.build_pptx()` / `drawlib.tools.build_pptx()`**: Measures `1920x1080` slide layouts and computed CSS styles via headless Chromium and exports native editable 16:9 (`960x540 pt`) MS PowerPoint (`.pptx`) decks—preserving `::: block` cards with `rgba` alpha fills/borders, text boxes, bullet/numbered lists, tables, inline code, and `::: note` speaker notes—while embedding ````drawlib```` diagrams as high-DPI static PNGs (`--dpi 240` default, `--anim-frame first|last` defaulting to `last`).

#### 2. Zero-Config Headless Chromium & Unified Standard Dependencies
- **Unified Standard Dependencies**: Promoted `playwright>=1.49.0`, `python-docx>=1.2.0`, and `python-pptx>=1.0.2` to standard `dependencies` and removed `[project.optional-dependencies]`. Installing `drawlib` via `uv add drawlib` or `pip install drawlib` now works out of the box for PDF, MS Word, and MS PowerPoint exports without extra flags.
- **Automatic Headless Browser Provisioning**: Running `drawlib build pdf` or `drawlib build pptx` automatically installs `chromium-headless-shell` on first run via Playwright's bundled driver. Added explicit offline pre-download support via `drawlib cache download --browser` (also included in `drawlib cache download --all`) and actionable shared-library diagnostics (`playwright install-deps chromium`) for minimal Linux containers.

#### 3. Modular Category-Based AI Agent Rules (`drawlib rules`)
- **Modular `_rules/` Organization**: Reorganized embedded rule manuals (`src/drawlib/_rules/`) into modular category directories (`charts/`, `diagrams/`, `graph/`, `icons/`, `shapes/`, `smartarts/`) for cleaner maintainability and fast topic lookup.

---

## Version 0.3.1

*Release Date: 2026/10/23*

Version 0.3.1 introduces the **`drawlib.charts.heatmap`** visualization suite (`HeatmapChart` and `HeatmapOverlay`) alongside a comprehensive **startup and import performance optimization** across the library and CLI.

---

### Highlights & New Features

#### 1. 2D Matrix Heatmaps & Spatial Thermal Overlays (`drawlib.charts.heatmap`)
- **`HeatmapChart`**: Declarative 2D matrix/grid heatmap across categorical `x_categories` and `y_categories`, featuring `Style`-based multi-stop color interpolation (`styles=[...]` or `min_style` / `max_style`), auto-contrasting in-cell value labels, configurable cell gaps and corner rounding (`cell_gap`, `cell_r`), continuous colorbars (`draw_colorbar`), and stepped swatch legends (`draw_legend`).
- **`HeatmapOverlay`**: Spatial thermal and hotspot overlay engineered to render directly over existing diagrams (`ClassDiagram`, `ArchitectureDiagram`, `ERDiagram`, `FlowDiagram`, `GeoMap`, etc.) to highlight complexity, incident density, or regional hotspots in `"smooth"` (2D Gaussian thermal gradient) or `"contour"` (concentric vector isoline rings) modes with `"add"` and `"max"` accumulation (`Spot`).

#### 2. Major Startup & Import Performance Optimization
- **PEP 562 Lazy Module & Icon Suite Loading**: Deferred submodule imports across `drawlib`, `drawlib.tools`, `drawlib.styles`, `drawlib.preset_styles`, `drawlib.preset_colors`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`, `drawlib.icons`, and CLI subcommands. Importing `drawlib`, calling non-rendering `drawlib.tools` utilities, or running lightweight CLI commands (`drawlib --version`, `drawlib init`, `drawlib serve`) no longer loads `matplotlib` or unused domain modules, reducing startup latency by **15x–40x** (and cutting `import drawlib` function calls by over **99%**).
- **On-Demand Preset Themes & Fast `Style` Construction**: Deferred preset theme instantiation (`DefaultStyles`, `GoogleStyles`, `MonochromeStyles`, etc.) until first access, adopted `defer_build=True` and `model_construct` fast paths for built-in style tokens, optimized `_BaseStylesMeta` attribute lookup, and deferred `@validate_call` schema compilation until first function call.

#### 3. Bug Fixes & Compatibility
- Resolved `PydanticDeprecatedSince211` deprecation warnings triggered when accessing `model_fields` on `BaseStyles` instances in Pydantic v2.11+.

---

## Version 0.3.0

*Release Date: 2026/10/21*

Version 0.3.0 represents a major architectural milestone for Drawlib, transforming it from a raw vector drawing tool into a comprehensive **"Illustration & Documentation as Code"** platform engineered for both software developers and **autonomous AI coding agents**.

---

### Highlights & New Features

#### 1. Modern Flat Package Architecture
- Consolidated legacy version-namespaced packages into a modern, standard flat package structure (`drawlib`).
- Clean, ergonomic public imports directly from domain modules:
  - `drawlib.canvas`, `drawlib.math`, `drawlib.types`, `drawlib.fonts`
  - `drawlib.shapes`, `drawlib.lines`, `drawlib.text`, `drawlib.icons`, `drawlib.images`
  - `drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`
  - `drawlib.anim`, `drawlib.slide`, `drawlib.tools`
  - `drawlib.styles`, `drawlib.preset_colors`, `drawlib.preset_styles`, `drawlib.utils`

#### 2. Built-in Integrated Documentation Builder, Slide Compiler & Developer Tools (`drawlib.tools`)
- Native Markdown, HTML, Slide, and PDF compiler (`drawlib build html`, `drawlib build markdown`, `drawlib build pdf`, `drawlib build slide`, `drawlib build image`).
- Compiles Markdown documents containing ````drawlib```` code blocks into:
  - Responsive multi-page static HTML documentation sites (`docs_html/`).
  - GitHub-optimized Markdown documents with embedded images (`docs/`).
  - Print-ready vector PDF documents (`doc.pdf` / `slide.pdf`).
  - Interactive 16:9 widescreen HTML presentation decks (`slide_html/`).
- **SQLite Incremental Build Cache (`.drawlib/cache.db`)**: Deterministic SHA-256 content-hash caching of code blocks, `styles.py`, `utils.py`, and local assets prevents unnecessary re-rendering of unchanged diagrams.
- **Programmatic Developer API (`drawlib.tools`)**: Full Python API (`build_html`, `build_markdown`, `build_pdf`, `build_slide`, `build_image`, `export_code_block`, `init_project`, `serve_docs`, `list_cache`, `download_cache`, `clear_cache`) for CI/CD and custom automation.

#### 3. Auto-Layout Graph Engine (`drawlib.graph`)
- Five specialized auto-layout graph solvers that eliminate manual coordinate math and support nested `Cluster` containers:
  - **`LayerGraph`**: Sugiyama-style hierarchical DAG layout.
  - **`ArchitectureGraph`**: Cloud and system topology solver with semantic tier alignment.
  - **`TreeGraph`**: Balanced parent-child hierarchy layout.
  - **`RadialGraph`**: Concentric radial ring layout.
  - **`GridGraph`**: Structured matrix placement solver.
- **2-Step Layout Inspection & Diagram Rendering (`get_layout()`)**: Computes structured `GraphLayout` coordinates (`xy`, `bottom_left`, `local_xy`, `local_bottom_left`, `points`) with human- and AI-readable `print(layout)` inspection and `offset()` fine-tuning.

#### 4. High-Level Technical Diagrams (`drawlib.diagrams`)
- **Architecture Diagrams (`drawlib.diagrams.architecture.ArchitectureDiagram`)**: Cloud topologies, nested cluster groups, and Phosphor / official GCP vector icons.
- **Flow Diagrams (`drawlib.diagrams.flow.FlowDiagram`)**: Standard flowchart symbols (ISO 5807 / JIS X 0121), decision branching, T-junction merging, and swimlanes (`Lane`).
- **Sequence Diagrams (`drawlib.diagrams.sequence.SequenceDiagram`)**: Client/server lifelines, activation bars, sync/async message arrows, self-calls, and interaction frames (`alt`, `opt`, `loop`, `par`).
- **ER Diagrams (`drawlib.diagrams.er.ERDiagram`)**: Full support for Information Engineering (IE / Crow's Foot) notation, table entity compartments, and automatic orthogonal routing.
- **UML Class Diagrams (`drawlib.diagrams.class_diagram.ClassDiagram`)**: 3-compartment class cards, stereotypes (`«interface»`), visibility indicators, and relationship methods (`inherit()`, `realize()`, `composite()`, `aggregate()`, `associate()`, `depend()`).
- **State Machine Diagrams (`drawlib.diagrams.state.StateDiagram`)**: Declarative statecharts with initial/final pseudo-states, internal activity compartments (`entry`, `do`, `exit`), curved transitions with bend control, and self-loops.

#### 5. Pure-Python Declarative Charts (`drawlib.charts`)
- Zero external plotting dependencies:
  - **BarChart**: Vertical/horizontal, grouped, and stacked.
  - **LineChart**: Straight segments, smoothed spline curves, and custom markers.
  - **AreaChart**: Overlapping and cumulative stacked area plots.
  - **PieChart**: Solid pies and donut rings with center KPI badges.
  - **RadarChart**: Multiaxis spider webs and concentric circular rings.
  - **ScatterChart**: 2D scatter and bubble plots with custom marker shapes.
  - **GanttChart**: Project schedules, progress bars, milestones, and task dependency arrows.

#### 6. Expanded SmartArts & Geographic Maps (`drawlib.smartarts`)
- **`GeoMap`**: Offline vector world, regional, and country maps (`World`, `Asia`, `Europe`, `USA`, `Japan`, etc.) with country/prefecture highlighting, pins, connections, and choropleth coloring.
- **`TreeNode`** & **`MindMapNode`**: Hierarchical node trees and radial brainstorming mind maps.
- **`SourceCode`**: Syntax-highlighted source code cards with line numbers, window chrome, and dark/light themes.
- **`ChevronProcess`** & **`Cycle`**: Sequential chevron process pipelines and radial circular life cycles with center hubs.
- **`Table`**, **`GridLayout`**, **`Pyramid`**, **`BoxList`**, **`BulletPoints`**: Structured tabular and card-based visual components.

#### 7. Multi-Frame Animations (`drawlib.anim`) & 16:9 Presentation Stage (`drawlib.slide`)
- **`drawlib.anim.Animation`**: Declarative multi-frame animation builder exporting lossless **APNG** and **Animated WebP** with frame context managers (`with anim.frame():`), configurable FPS, and interpolation helpers in `drawlib.math`.
- **`drawlib.slide`**: Universal `1920x1080` (16:9 widescreen) presentation coordinate stage with Markdown layout containers (`::: block`, `::: note`), Presenter View (`?presenter=1`), and the `current_slide` runtime proxy (`SlideContext`, `BoundingBox`).

#### 8. AI Agent Guidelines & Rule System (`drawlib rules`)
- Integrated on-demand manual accessible via CLI:
  - `drawlib rules show <topic>`: Inject concise syntax documentation directly into agent context windows.
  - `drawlib rules list`: Explore all available drawing rules.
- Autonomous visual self-correction loop via coordinate grid overlay (`drawlib show -g`).

#### 9. Project Scaffolding (`drawlib init`)
- Quickly scaffold complete starter projects for four primary use cases:
  - `drawlib init doc`: Linear technical document (HTML, PDF, Markdown, images).
  - `drawlib init site`: Multi-page documentation website.
  - `drawlib init slide`: 16:9 presentation slide deck (web & vector PDF).
  - `drawlib init images`: Standalone Python illustration batch project.

---

### Breaking Changes & Migration from v0.2

If you are upgrading from Drawlib v0.2, review the following required changes:

1. **Python 3.11+ Required**: Python 3.10 and earlier are no longer supported.
2. **Top-Level CLI `drawlib export` Removed**:
   - Use `drawlib show input.py -o output.png` instead.
3. **Legacy `dsart` Namespace Removed & `Tree` Renamed to `TreeNode`**:
   - Change `from drawlib.apis import dsart` to:
     ```python
     from drawlib.smartarts import Table, TreeNode, MindMapNode, ChevronProcess, Cycle, GeoMap, SourceCode
     ```
4. **Semantic Style Naming Normalized**:
   - Styles tokens unified to PascalCase (`Styles.PrimaryFlat`, `Styles.AccentBold`). Legacy snake-case style attributes are completely removed.
5. **Diagram Class Naming Unified**:
   - All diagram containers follow PascalCase with the `Diagram` suffix:
     - `ArchitectureDiagram`
     - `ERDiagram`
     - `FlowDiagram`
     - `SequenceDiagram`
     - `ClassDiagram`
     - `StateDiagram`

---

## Version 0.2.x Archive

- **v0.2.3** (2024/09/08): Added block arrow functions (`arrow_polyline`, `arrow_l`, `arrow_u`, `arrow_arc`) and initial SmartArts (`Table`, `Tree`, `GridLayout`, `Pyramid`, `BoxList`, `BulletPoints`).
- **v0.2.2** (2024/07/02): Initial public release of Drawlib 0.2.
