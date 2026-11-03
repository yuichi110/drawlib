# Drawlib Project Architecture & Overview Guidelines

Drawlib provides a complete project scaffolding and multi-target build engine. It compiles Python drawing scripts and Markdown documents containing embedded ````drawlib```` blocks into publication-ready static HTML websites, linear vector PDFs, editable MS Word (`.docx`) documents, 16:9 presentation slide decks, editable MS PowerPoint (`.pptx`) decks, GitHub-Flavored Markdown, and standalone image assets.

This document covers the **universal project architecture, template selection, shared configuration files (`styles.py`, `utils.py`), and caching system**. For deep authoring best practices on a specific project type, consult its dedicated rule guide:
- **Standalone Images (`images`)**: `uv run drawlib rules show project-images`
- **Linear Document, PDF & Word (`doc`)**: `uv run drawlib rules show project-doc`
- **Multi-Page Website (`site`)**: `uv run drawlib rules show project-site`
- **Illustrated API & SDK Reference (`api`)**: `uv run drawlib rules show project-api`
- **16:9 Slide Deck & PowerPoint (`slide`)**: `uv run drawlib rules show project-slide`
- **3-Stage Review & Self-Correction Loop**: `uv run drawlib rules show review-guide`

---

## 1. Project-First Rule (`drawlib init project` — No Bare `.py` Files)

> **CRITICAL for AI Agents & Developers**: Never create standalone `.py` drawing scripts directly in an uninitialized directory, and never construct project folders from scratch manually.  
> Before writing any drawing code, check if a Drawlib project (`*_src/`) already exists in the workspace. If not, **always scaffold a project first using `drawlib init project`** (or guide the user to choose one) so that `styles.py` (theme & language fonts), `utils.py`, `_assets/`, and `build.sh` are properly configured:
> - **Diagram image(s) only** -> Scaffold an **`images`** project (`uv run drawlib init project images [-l <lang>] [-s <style>]`).
> - **Linear technical spec / whitepaper / PDF / Word (`.docx`)** -> Scaffold a **`doc`** project (`uv run drawlib init project doc [-l <lang[,lang...]>] [-s <style>]`).
> - **Multi-page documentation website** -> Scaffold a **`site`** project (`uv run drawlib init project site [-l <lang[,lang...]>] [-s <style>]`).
> - **Illustrated REST / SDK / CLI API reference** -> Scaffold an **`api`** project (`uv run drawlib init project api [-l <lang[,lang...]>] [-s <style>]`).
> - **16:9 presentation slide deck / PowerPoint (`.pptx`)** -> Scaffold a **`slide`** project (`uv run drawlib init project slide [-l <lang[,lang...]>] [-s <style>]`).
> - **Pass `--lang` for Non-English Labels**: When the user prompts in Japanese (or requires CJK/multilingual typography), pass `--lang ja` (or comma-separated `-l en,ja` for bilingual projects) to `drawlib init project` so `styles.py` automatically configures CJK-safe fonts.
> - **Clean Up Starter Samples**: After scaffolding, replace or delete the generated starter sample files (`sample1.py`, `sample2.py`, etc.) so only the user's requested diagrams are built.

### Scaffolding CLI Syntax & Options:
```bash
# List available starter templates:
uv run drawlib init project list

# Scaffold a project in the current directory:
uv run drawlib init project <images|doc|site|api|slide> [target] [-l <lang[,lang...]>] [-s <style>] [-f]

# Examples:
uv run drawlib init project images --lang ja -s google
uv run drawlib init project doc rbac -s google
uv run drawlib init project site docs -l en,ja -s default
uv run drawlib init project api sdk_api -l en,ja -s google
uv run drawlib init project slide pitch -l en,ja -s google
uv run drawlib init agent antigravity          # Generate per-agent AI rules (.agents/rules/drawlib.md, etc.)
```

| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--style` | `-s` | `<theme>` | `default` | Style preset theme (`default`, `google`, `monochrome`) or custom CSS path. Synchronously configures both `style.css` and `styles.py`. |
| `--lang` | `-l` | `<lang>` | `en` | Starter template language code (`en`, `ja`, `zh-cn`, `ko`, `th`, `hi`, etc.), or comma-separated locales (`-l en,ja`) for multi-language `doc`, `site`, `api`, and `slide` projects (`images` is single-language only). |
| `--force` | `-f` | flag | `False` | Overwrite existing files if the destination directory is not empty. |

> **Pure Scaffolding Principle**: `drawlib init project` only creates template and configuration files; it never runs compilation automatically. To compile your project, run `./<target>_src/build.sh` (or `./<target>_src/build_*.sh`).

---

## 2. Choosing Among the 5 Project Archetypes

Drawlib features 5 project starter templates tailored to distinct authoring and publishing workflows. All four Markdown-based archetypes (`doc`, `site`, `api`, `slide`) share a **unified `<src_dir>/<lang>/` locale layout** ($N \ge 1$ locales), so adding a second language later requires zero `git mv` file moves:

| Project Type | Source Folder | Generated Deliverables | When AI Agents Should Choose This | Dedicated Guide |
| :--- | :--- | :--- | :--- | :--- |
| **`images`** | `images_src/*.py` | `images/*.png` (or `.webp`) | User wants **diagram image(s) only** (architecture figures, README illustrations, standalone assets). | `project-images` |
| **`doc`** | `doc_src/<lang>/*.md` | `doc_html/` (`<lang>/` + root redirect)<br>`doc_<lang>.pdf`<br>`doc_markdown/<lang>/` (GitHub MD)<br>`doc_images/` (Extracted PNGs)<br>*(+ on-demand `doc_<lang>.docx` via `build docx`)* | User wants a **single linear technical document** (RFCs, design specs, whitepapers, quickstarts, printable PDFs, or editable MS Word `.docx`). | `project-doc` |
| **`site`** | `docs_src/<lang>/**/*.md`<br>+ `<lang>/navbar.md` | `docs_html/` (`<lang>/` + root `index.html`)<br>`docs_markdown/` (`<lang>/` + root `index.md`)<br>`docs_images/` (Extracted PNGs) | User wants a **multi-page documentation website** with a persistent navigation sidebar (portals, guides, wikis). | `project-site` |
| **`api`** | `api_src/<lang>/**/*.md`<br>*(no `navbar.md`)* | `api_html/` (`<lang>/` + root redirect)<br>`api_markdown/<lang>/` (GitHub MD)<br>`api_images/` (Extracted PNGs) | User wants a **dedicated REST / SDK / CLI API reference** (`1 MD = 1 HTML`, `# H1` category + `## H2` symbol list + semantic badges + `/` filter). | `project-api` |
| **`slide`** | `slide_src/<lang>/*.md` | `slide_html/` (`<lang>/index.html` + redirect)<br>`slide_<lang>.pdf` (16:9 vector PDF)<br>`slide_images/` (Extracted SVGs)<br>*(+ on-demand `slide_<lang>.pptx` via `build pptx`)* | User wants a **16:9 widescreen presentation deck** with `1920×1080` stage blocks, speaker notes, Presenter View, or editable MS PowerPoint `.pptx`. | `project-slide` |

```drawlib align=center code=fold file=project_archetypes_overview.png caption="Drawlib's Five Project Archetypes & Compilation Deliverables"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=180, height=64, dpi=150)

rectangle((90, 32), width=174, height=58, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (90, 55.0),
    "Five Drawlib Project Archetypes (drawlib init project <type>)",
    style=Styles.DarkBold.patch(text_size=13.0),
)

cards = [
    (22.0, "images", "images_src/*.py", "• Batch Python scripts\n• Standalone PNG/WebP\n• Rule: project-images", Styles.Neutral, Styles.PrimaryBold, phosphor.image),
    (56.0, "doc", "doc_src/<lang>/*.md", "• Linear chapters + ToC\n• A4 PDF, HTML & .docx\n• Rule: project-doc", Styles.PrimaryNeutral, Styles.PrimaryBold, phosphor.file_pdf),
    (90.0, "site", "docs_src/<lang>/**/*.md", "• Multi-page + navbar.md\n• Static Website & Search\n• Rule: project-site", Styles.PrimaryFlat, Styles.WhiteBold, phosphor.globe),
    (124.0, "api", "api_src/<lang>/*.md", "• H1/H2 Auto-Sidebar\n• REST/SDK Badges & Filter\n• Rule: project-api", Styles.Neutral, Styles.SecondaryBold, phosphor.brackets_curly),
    (158.0, "slide", "slide_src/<lang>/*.md", "• 1920x1080 ::: block\n• Web, 16:9 PDF & .pptx\n• Rule: project-slide", Styles.SecondaryNeutral, Styles.SecondaryBold, phosphor.presentation_chart),
]

for cx, title, sub, body, card_st, hdr_st, icon_fn in cards:
    rectangle((cx, 26.0), width=31.5, height=39, style=card_st.patch(shape_r=2.0))
    icon_fn((cx - 8.5, 39.2), width=4.6, style=hdr_st)
    text((cx + 2.5, 39.2), title, style=hdr_st.patch(text_size=11.5))
    sub_st = Styles.White.patch(text_size=9.5) if card_st == Styles.PrimaryFlat else Styles.Muted.patch(text_size=9.5)
    body_st = Styles.White.patch(text_size=9.6) if card_st == Styles.PrimaryFlat else Styles.Dark.patch(text_size=9.6)
    text((cx, 32.0), sub, style=sub_st)
    line((cx - 12.5, 28.6), (cx + 12.5, 28.6), style=Styles.White if card_st == Styles.PrimaryFlat else Styles.Muted)
    text((cx, 17.8), body, style=body_st)

save()
```

---

## 3. Shared Project Architecture (`drawlib.toml`, `styles.py`, `utils.py`, `_assets/`, `build.sh`)

Every scaffolded `<target>_src/` directory shares foundational configuration and build conventions:

### 3.1. Golden Rule: `<target>_src/` Is the Single Source of Truth
- **Author & Edit Strictly Inside `<target>_src/`**: All Markdown documents, Python scripts, stylesheets, and assets live inside `images_src/`, `doc_src/`, `docs_src/`, `api_src/`, or `slide_src/`.
- **Never Manually Edit Output Directories**: Generated folders and artifacts (`images/`, `doc_html/`, `docs_html/`, `docs_markdown/`, `api_html/`, `api_markdown/`, `slide_html/`, `*_<lang>.pdf`, `*_<lang>.docx`, `*_<lang>.pptx`) are overwritten on build.
- **Overwrite Protection**: `drawlib build` strictly refuses to execute if the source and destination paths resolve to the same directory (`src_abs == dest_abs`).

### 3.2. Unified Project Manifest (`drawlib.toml`)
`drawlib init` automatically writes `<target>_src/drawlib.toml` as the canonical project manifest:
```toml
# Markdown archetypes ("doc", "site", "api", "slide") — [i18n] is REQUIRED (1 or more locales):
[project]
name = "whitepaper"
type = "doc"                  # "doc" | "site" | "api" | "slide"
title = ""                    # Optional explicit title override (empty = auto-infer from # H1 / navbar.md)
description = ""              # Human & AI agent project summary
style = "google"

[i18n]                        # Always present on doc, site, api, and slide (even single-locale ["en"])
default_lang = "en"
langs = ["en", "ja"]

[i18n.labels]                 # Optional custom switcher display labels
en = "English"
ja = "日本語"

[i18n.descriptions]           # Optional per-locale meta/OGP & llms.txt summary overrides
en = "English summary for search engines, social cards, and llms.txt."
ja = "検索エンジン・SNS カード・llms.txt 向けの日本語概要。"

[seo]                         # Optional project-managed SEO, OGP, sitemap.xml, robots.txt & llms.txt
site_url = "https://docs.example.com"
og_image = "_assets/ogp.png"  # Copied to output and resolved against site_url
twitter_card = "summary_large_image"
sitemap = true
robots = true
llms_txt = true
```
*(For `type = "api"`, an optional `[api]` section configures `sidebar_expanded = true`, `badge_text`, `badge_url`, `repo_url`, and `header_links` — see `uv run drawlib rules show project-api`.)*
```toml
# Standalone Python scripts ("images") — lang is set under [project] (no [i18n] or [seo]):
[project]
name = "images"
type = "images"
title = ""
description = ""
lang = "en"
style = "default"
```
- **Required Manifest & `[i18n]` for `doc`, `site`, `api`, and `slide`**: Directory builds for `doc`, `site`, `api`, and `slide` strictly require `drawlib.toml` with an `[i18n]` table (`default_lang`, `langs` with `len >= 1`, and optional `[i18n.labels]` / `[i18n.descriptions]`), and disallow `lang` under `[project]`. Even single-language projects (`langs = ["en"]` or `langs = ["ja"]`) place Markdown inside `<target>_src/<lang>/` and emit locale-suffixed document/deck files (`<base>_<lang>.pdf`, `<base>_<lang>.docx`, `<base>_<lang>.pptx`), while automatically hiding the HTML language switcher until `len(langs) >= 2`.
- **Optional Project-Managed SEO, Open Graph & `llms.txt` (`[seo]`)**: On `doc`, `site`, `api`, and `slide` HTML directory builds, configuring `[seo]` (or `[project].description` / `[i18n.descriptions]`) injects `<meta name="description">`, Open Graph (`og:*`), Twitter/X Card (`twitter:*`), and `<link rel="canonical">` tags into HTML `<head>`, upgrades `hreflang` links to absolute URLs when `site_url` is set, and generates `sitemap.xml`, `robots.txt` (when `site_url` is set), and `llms.txt` (`llmstxt.org` AI-agent index) at the HTML output root.
- **Standalone Single-File Builds Preserved**: Single-file CLI/API calls (`drawlib build pdf spec.md -o spec.pdf`, `drawlib build docx spec.md -o spec.docx`, `drawlib build image fig.py -o fig.png`) continue to work directly without a project manifest.

### 3.3. Global Theme & Font Configuration (`styles.py` & `<lang>/styles.py`)
`styles.py` defines project-wide `Styles` and `Colors` overrides (including regional CJK font patching when initialized with `--lang`). In `doc`, `site`, `api`, and `slide` projects, an optional per-locale `<target>_src/<lang>/styles.py` (and `<lang>/utils.py`) overrides the root `styles.py` / `utils.py` for that locale's localized diagrams (`file=<stem>_<lang>.png` / `.svg`).
Inside any drawing script or embedded ````drawlib```` block, always import uppercase `Styles` and `Colors`:
```python
from drawlib.styles import Colors, Styles
```
Never import lowercase `styles` or `colors`, which shadows the module namespace.

### 3.4. Reusable Drawing Macros (`utils.py`)
`utils.py` holds project-specific helper functions, recurring diagram sub-components (e.g., `draw_service_card()`, `draw_page_number()`), and layout constants. Any top-level function or constant in `utils.py` can be imported via:
```python
from drawlib.utils import draw_service_card
```

### 3.5. Local Static Assets (`_assets/`)
Place static logos, custom `.ttf`/`.otf` font files, or reference screenshots inside `<target>_src/_assets/`.
- During HTML/Markdown/Slide builds, `_assets/` is automatically copied to the output directory.
- `drawlib init` automatically provisions `_assets/favicon.png` so HTML pages, documentation websites, and slide presentations display the brand favicon out-of-the-box (customizable by replacing `_assets/favicon.png`).
- Inside Python drawing code, reference files as `"_assets/logo.png"` or `FontFile("_assets/brand.ttf")`—Drawlib automatically walks up ancestor directories from `<target>_src/<lang>/...` to resolve `_assets/` at the project root and hashes them in `.drawlib/cache.db`.
- Inside Markdown prose (`![Logo](...)`), reference `_assets/` relatively from the current Markdown file inside `<target>_src/<lang>/` (e.g. `../_assets/logo.png` from `<lang>/index.md`, or `../../_assets/logo.png` from `<lang>/01_section/page.md`).
- **Strictly Relative Referencing (No Absolute Paths or `file://` URLs)**: Always reference assets relatively. Never use machine-specific absolute paths (`/usr/...`, `/home/...`, `C:\...`) or `file:///` URLs. The compiler validates link hygiene at build time and rejects prohibited paths.

### 3.6. Link & Path Hygiene in Markdown Documents
- **Relative Links Only**: All internal page links, cross-chapter references, and asset links in Markdown source files (`*_src/**/*.md`) must be written as relative paths (e.g. `../architecture/overview.md`) or inline code format.
- **Prohibition of `file://` and Local Absolute Paths**: Never write `file:///` URIs or local filesystem roots (`/usr/...`, `/home/...`, `/Users/...`, `C:\...`) into documentation files. While AI assistants use `file:///` links for chat UI navigation, committed documentation files must remain 100% portable.

### 3.7. Modular Build Scripts (`build_*.sh`) & On-Demand Office Exports
Each project scaffolds focused shell scripts alongside the master `build.sh`:
- **`build_html.sh`**: Fast HTML compilation for rapid browser verification.
- **`build_pdf.sh`**: Headless Chromium print to vector PDF (`doc` -> `<target>_<lang>.pdf` and `slide` -> `<target>_<lang>.pdf`).
- **`build_docx.sh`**: On-demand editable MS Word export (`doc` -> `<target>_<lang>.docx`; pre-scaffolded with `+x`, not invoked by `build.sh`).
- **`build_pptx.sh`**: On-demand editable 16:9 MS PowerPoint export (`slide` -> `<target>_<lang>.pptx`; pre-scaffolded with `+x`, not invoked by `build.sh`).
- **`build_markdown.sh`**: GitHub-Flavored Markdown compilation (`doc` and `site`).
- **`build_image.sh`**: Standalone diagram image compilation/extraction.
- **`build.sh`**: Master script that runs the standard target builds for the project sequentially (HTML, PDF, Markdown, Images).
- **`serve.sh`**: Local preview HTTP server (`drawlib serve`).
- **On-Demand Office Exports (`docx` & `pptx`)**: Run `./doc_src/build_docx.sh` (`uv run drawlib build docx doc_src/ -o doc.docx` -> `doc_<lang>.docx`) or `./slide_src/build_pptx.sh` (`uv run drawlib build pptx slide_src/ -o slide.pptx` -> `slide_<lang>.pptx`) on demand without slowing down standard `build.sh` pipelines.

---

## 4. Build Cache (`.drawlib/cache.db`) & Asset Cache (`drawlib cache`)

### 4.1. SQLite Incremental Build Cache (`.drawlib/cache.db`)
- **Automatic Hashing**: Before executing any ````drawlib```` block or `.py` script, Drawlib computes a SHA-256 key over:
  1. The Python drawing code block.
  2. Global `styles.py` (`-s`) and `utils.py` (`-u`) contents.
  3. Local asset files referenced as string literals (e.g. `_assets/*`).
  4. Source/target file paths, image format (`png` / `webp` / `svg`), and slide count.
- **Auto-Ignore & Eviction**: Automatically creates `.drawlib/.gitignore` (`*`), invalidates on `drawlib`/`matplotlib` version upgrades, and evicts the oldest 50% of blobs when exceeding 1 GiB.
- **When to Bypass Cache (`--no-cache`)**: If your drawing code imports an external custom `.py` file outside `styles.py` and `utils.py`, pass `--no-cache` or clear the image cache:
  ```bash
  uv run drawlib build html docs_src/ -o docs_html/ --no-cache
  uv run drawlib cache clear --images
  ```

### 4.2. Font, Icon, Map & Headless Browser Cache (`drawlib cache`)
`playwright`, `python-docx`, and `python-pptx` are standard dependencies of `drawlib` (no optional extras needed). Font families, icon packs (`icon_phosphor`, `icon_gcp`, `icon_aws`, `icon_azure`, `icon_ai`..`icon_workspace`), and GeoJSON maps (`map_world`) download on demand into `drawlib/_cached_assets/`, while headless Chromium (`chromium-headless-shell`) downloads automatically on first `drawlib build pdf` or `drawlib build pptx` execution:
```bash
uv run drawlib cache list              # Inspect cached packages and disk size
uv run drawlib cache download --all    # Pre-download all fonts, icons, maps & headless Chromium for offline/CI builds
uv run drawlib cache download --browser # Pre-download headless Chromium only
uv run drawlib cache clear --all       # Purge all font, icon, map, and SQLite image caches
```
*(In minimal Linux containers such as `python:3.12-slim` lacking OS shared libraries like `libnss3` or `libgbm1`, run `playwright install-deps chromium` or `playwright install --with-deps --only-shell chromium`.)*

---

## 5. Parallel Multi-Agent Workflow Across the 5 Project Archetypes

Drawlib projects are intentionally structured as **modular collections of independent `.py` scripts or `.md` files** sharing a common `styles.py` and `utils.py` foundation. When creating or updating multiple diagrams, chapters, pages, or slides, **AI coding agents should actively distribute and parallelize work across multiple subagents** (whenever subagent invocation tools are available) rather than authoring every file sequentially in a single context window.

### 5.1. Why Multi-Agent Parallelization Fits Drawlib
1. **Context Window Preservation for Multimodal Review**: Every `drawlib show ... -g` + `view_file` cycle loads high-resolution diagram images into the agent's context window. Delegating files to subagents lets each subagent perform its own **Stage 1 (Static Check)** and **Stage 2 (Grid Review `-g`)** in an isolated context window, keeping the parent orchestrator's context clean.
2. **Natural File-Level Partitioning**: Each of the 5 project archetypes partitions cleanly along file or directory boundaries:

| Project Type | Partition Unit per Subagent | Shared Files (Parent Sets Up First) | Subagent Responsibility (Phase 2) | Parent Finalization (Phase 3) |
| :--- | :--- | :--- | :--- | :--- |
| **`images`** | Individual `images_src/<name>.py` script (or subset of scripts) | `images_src/styles.py`, `utils.py`, `_assets/` | Author assigned `.py` script(s) & run `drawlib show ... -g -o .drawlib/scratch/<script>_grid.png` + `view_file` | Run `./images_src/build.sh` & inspect `images/*.png` |
| **`doc`** | Individual chapter `doc_src/<lang>/0N_<topic>.md` | `doc_src/drawlib.toml`, `styles.py`, `utils.py`, `<lang>/00_cover.md`, chapter outline | Author assigned chapter(s) (`2+` diagrams, Hero at Lines 5–15) & run Stage 1 + Stage 2 grid review | Run `./doc_src/build.sh`, `serve --check`, & inspect `doc_<lang>.pdf` / `doc_html/` |
| **`site`** | Topic page `docs_src/<lang>/<sec>/<page>.md` or section folder | `docs_src/drawlib.toml`, `styles.py`, `utils.py`, `<lang>/navbar.md`, `<lang>/index.md` | Author assigned page(s) & run Stage 1 + Stage 2 grid review with unique scratch filenames | Run `./docs_src/build.sh`, `serve --check`, & `1280×920` browser check |
| **`api`** | Category/module page `api_src/<lang>/0N_<module>.md` | `api_src/drawlib.toml` (`[api]`), `styles.py`, `utils.py`, `<lang>/00_overview.md` | Author assigned API page(s) (`# H1` + `## H2` badges + diagrams) & Stage 1 + Stage 2 grid review | Run `./api_src/build.sh`, `serve --check`, & `1440×920` browser check |
| **`slide`** | Individual slide `slide_src/<lang>/0N_<slide>.md` or section folder | `slide_src/drawlib.toml`, `styles.py`, `utils.py`, deck story arc & slide numbering | Author assigned slide(s) (`::: block` + `::: note`) & run Stage 1 + Stage 2 grid review | Run `./slide_src/build.sh` & inspect `slide_<lang>.pdf` / `1920×1080` stage |

### 5.2. The 3-Phase Orchestrator–Subagent Protocol & Concurrency Guardrails

1. **Phase 1 — Parent Orchestrator Establishes Shared Foundation First**:
   - Run `drawlib init project <type>` and configure `drawlib.toml`, `styles.py` (theme, language fonts), `utils.py` (shared helpers/macros), `_assets/`, and the structural index (`<lang>/navbar.md` for `site`, module numbering for `api`, chapter numbering for `doc`, or slide numbering/story arc for `slide`) **before** launching subagents.
   - Subagents must treat `drawlib.toml`, `styles.py`, `utils.py`, and `<lang>/navbar.md` as **read-only** so parallel workers never overwrite shared configuration.
2. **Phase 2 — Parallel Subagents Author Disjoint Files & Run Stage 1 + Stage 2**:
   - **Strict Disjoint File Ownership**: Never assign the same `.py` or `.md` file to two subagents concurrently.
   - **Unique Scratch Preview Filenames (Critical)**: When running `drawlib show ... -g` in parallel, each subagent **must** write to a unique scratch file path named after its script or diagram block:
     ```bash
     uv run drawlib show docs_src/en/02_arch/vpc.md vpc_hero.png \
         -s docs_src/styles.py -u docs_src/utils.py \
         -g -o .drawlib/scratch/vpc_hero_grid.png
     ```
     Never use a hardcoded shared filename like `.drawlib/scratch/preview.png` across concurrent subagents, or subagents will overwrite and inspect each other's images.
   - **No Full-Project Builds Inside Subagents**: Subagents should only run `drawlib show ... -g` for their assigned diagrams and must **not** run `./build.sh`, avoiding concurrent SQLite write contention on `.drawlib/cache.db`.
3. **Phase 3 — Parent Orchestrator Runs Unified Build & Stage 3 Macro Review**:
   - Once all subagents complete their assigned files and Stage 2 fixes, the parent orchestrator runs `./<target>_src/build.sh` once, verifies link integrity (`uv run drawlib serve <target>_html/ --check`), performs **Stage 3 (Macro-Page Browser HTML / PDF Review)**, and cleans up `.drawlib/scratch/`.

---

## 6. Dedicated Project & Module Rule Guides

Query the specific project or module manual matching your target deliverable:
- **`uv run drawlib rules show project-images`**: Standalone `.py` illustration scripts (`images_src/`).
- **`uv run drawlib rules show project-doc`**: Linear technical documents, whitepapers, A4 vector PDFs & editable `.docx` (`doc_src/`).
- **`uv run drawlib rules show project-site`**: Multi-page documentation websites & `navbar.md` (`docs_src/`).
- **`uv run drawlib rules show project-api`**: Illustrated REST / SDK / CLI API references, `# H1` / `## H2` auto-sidebar, semantic badges & `[api]` manifest (`api_src/`).
- **`uv run drawlib rules show project-slide`**: 16:9 widescreen presentation decks, `::: block` stage layouts & editable `.pptx` (`slide_src/`).
- **`uv run drawlib rules show review-guide`**: 3-Stage Autonomous Multimodal Review & Self-Correction Loop.
- **Component Overviews**: `uv run drawlib rules show lib-shapes-overview`, `lib-icons-overview`, `lib-smartarts-overview`, `lib-charts-overview`, `lib-diagrams-overview`, `lib-graph-overview`.

