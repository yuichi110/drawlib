---
trigger: always_on
---

# Drawlib AI Agent Instructions

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Illustrated Documentation as Code"**.
AI coding agents must use Drawlib to create all architectural diagrams, workflows, and technical documentation.

---

## 1. Why Drawlib? (Illustration & Illustrated Documentation as Code)

Traditional technical documentation suffers from severe tool fragmentation:
- **The Fragmentation Problem**: Writing code in Git, drawing diagrams in external GUI tools (e.g. draw.io, Visio), exporting images, and manually pasting them into external documents (Word, Confluence, wikis). Diagrams quickly become outdated, inconsistent, and disconnected from the real codebase because maintenance requires tedious multi-tool handoffs.
- **The Drawlib Solution**: Unifies source code, documentation, and technical diagrams inside your Git repository as version-controlled code.
  - **Single Source of Truth (SoT)**: Markdown and declarative Python drawing blocks live alongside the codebase. Updating an architecture or database diagram is as painless and maintainable as editing code.
  - **Autonomous AI Feedback Loop**: AI coding agents can inspect repository code, generate diagrams, render them headlessly, review images multimodally, and iterate autonomously to continually elevate documentation quality.

---

## 2. Core Principles for AI Agents

1. **Draw with Drawlib (No Raw SVGs or Matplotlib Boilerplate)**:
   Never generate raw SVG files or complex low-level matplotlib boilerplate. Always use Drawlib's declarative Python API and high-level components.
2. **Project-First Rule: Always Start with `drawlib init` (No Bare `.py` Files)**:
   Never create standalone `.py` drawing files directly in an uninitialized directory, and never construct project folders from scratch. Even if the user only asks for a single diagram image, check if a Drawlib project (`*_src/`) exists in the workspace; if not, **always scaffold a project first using `drawlib init`** (or guide the user to choose one) so `styles.py` (theme & language fonts), `utils.py`, `_assets/`, and `build.sh` are properly configured:
   - **Diagram image(s) only** -> **`images`** project: `uv run drawlib init images [target] [-l <lang>] [-s <style>]` (see `project-images`)
   - **Linear document / spec / RFC / PDF** -> **`doc`** project: `uv run drawlib init doc [target] [-l <lang>] [-s <style>]` (see `project-doc`)
   - **Multi-page documentation website** -> **`site`** project: `uv run drawlib init site [target] [-l <lang>] [-s <style>]` (see `project-site`)
   - **16:9 presentation slide deck** -> **`slide`** project: `uv run drawlib init slide [target] [-l <lang>] [-s <style>]` (see `project-slide`)
   - **Pass `--lang` for Non-English Diagrams**: When the user prompts in Japanese (or needs CJK/multilingual labels), pass `--lang ja` (e.g. `uv run drawlib init images --lang ja`) so `styles.py` automatically configures CJK-safe fonts.
   - **Clean Up Starter Samples**: After scaffolding, replace or delete the generated starter sample files (`sample1.py`, `sample2.py`, etc.) so only the user's requested diagrams are built.
3. **Start with Overview**:
   Before writing drawing code, inspect canvas geometry, coordinates, and lifecycle rules:
   `uv run drawlib rules show overview`
   *(Canvas origin (0,0) is at bottom-left; Cartesian coordinate system).*
4. **Follow the Style Guide**:
   Always obey design token discipline:
   `uv run drawlib rules show style-guide`
   - **50%+ Neutral Baseline**: Ground at least 50% of shapes in calm neutral cards (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`). Never produce rainbow diagrams.
   - **Reserved Saturated Fills**: Use `Styles.PrimaryFlat` or `Styles.AccentFlat` strictly for 1–2 primary focal points.
   - **PascalCase Tokens**: Always import `from drawlib.styles import Colors, Styles` (never lowercase `styles` or `colors`).

---

## 3. What Drawlib Can Do (Favor High-Level Components)

Never manually assemble diagrams out of dozens of primitive rectangles and lines. Always favor tailored high-level components:

| Category | Recommended Module | Primary Use Cases |
| :--- | :--- | :--- |
| **Auto-Layout Graphs** | `drawlib.graph` | Declarative auto-layout DAGs, nested clusters, topologies |
| **Cloud Architecture** | `drawlib.diagrams.architecture` | VPCs, microservices, cloud topologies, official icons |
| **Workflows & Pipelines** | `drawlib.diagrams.flow`, `smartarts.ChevronProcess` | Decision trees, CI/CD pipelines, linear stages |
| **API Sequences** | `drawlib.diagrams.sequence` | Client/server lifelines, message exchanges, sync/async calls |
| **Data & Relational Models**| `drawlib.diagrams.er`, `smartarts.Table` | Database schemas, entity relationships, matrix comparisons |
| **Code & State Models** | `drawlib.diagrams.class_diagram`, `diagrams.state` | OOP UML class models, state machine lifecycles |
| **Hierarchy & Organization**| `drawlib.smartarts.TreeNode`, `smartarts.MindMapNode` | Directory trees, org charts, radial brainstorming maps |
| **Quantitative Charts** | `drawlib.charts` | Bar, Line, Area, Pie, Radar, Scatter, and Gantt charts |
| **Standardized Icons** | `drawlib.icons` | Phosphor, FontAwesome, and GCP architecture vector/PNG icons |
| **Drawing Primitives** | `drawlib.shapes`, `lines`, `text` | 23 geometric primitives, curved lines, bezier curves, styled text |

---

## 4. Illustrated Documentation as Code (Embedded Markdown Blocks)

In technical documentation (`docs_src/`), embed diagrams directly within markdown files using the ````drawlib```` code fence:

````markdown
```drawlib center fold-code file:service_architecture.png caption:"Service Architecture"
from drawlib.canvas import save, setup
from drawlib.styles import Styles
from drawlib.shapes import rectangle

setup(width=100, height=40)
rectangle((50, 20), width=60, height=20, style=Styles.Neutral, text="Service")
save()
```
````
- **Top Hero & Visual Density**: Place a **Top Hero diagram at Lines 5–15** (right after `# Title` and lead paragraph) using `fold-code` so the visual is immediately visible above the fold. Include **`2+` diagrams per page**, pairing icons (`phosphor`, `gcp`) with high-level components (`SmartArts`, `Diagrams`, `Graphs`, `Charts`).
- **Attributes & `720pt` Typography Sizing**: Always specify `file:<name>.png` and `caption:"..."`. Omit narrow pixel widths (`500px`, `600px`) so the image fills `100%` of `.drawlib-image`, and keep in-image `text_size >= 10.0` (standard `10.5`–`12.0`, headers `12.0`–`14.0`, floor `9.5`) so rendered labels ($\text{text\_size} \times \text{Width} / 720$) match `16px` HTML body text.
- **Source of Truth**: Always edit `<base>_src/` (e.g. `docs_src/`). Never manually edit generated output directories (`docs/`, `docs_html/`).
- **No Absolute Paths or file:// URLs (Relative Links Only)**: Never write local filesystem absolute paths (`/usr/...`, `/home/...`, `/Users/...`, `C:\...`) or `file:///` URLs inside documentation Markdown source files (`docs/*_src/**/*.md`). All links must use relative paths (e.g. `../foo.md`) or inline code format. While the AI assistant uses `file:///` links when conversing with the user in chat responses for clickable IDE navigation, repository documentation files published on the web or GitHub must never contain `file:///` or machine-specific absolute paths.
- **Incremental Build Cache (`.drawlib/cache.db`)**: `drawlib build` and `drawlib show` cache rendered images by hashing the code block, `styles.py`, `utils.py`, and referenced local assets (`_assets/`). If you edit an external imported Python module outside `styles.py`/`utils.py`, pass `--no-cache` or run `uv run drawlib cache clear --images` to force re-rendering.
- **Font & Icon Asset Cache**: Pre-download font and icon packages for offline or CI builds via `uv run drawlib cache download --all` (inspect with `uv run drawlib cache list`, clear all with `uv run drawlib cache clear --all`).

---

## 5. Autonomous 3-Stage Review & Self-Correction Loop

Never deliver unverified diagrams or documentation. Always execute this 3-stage verification loop (details: `uv run drawlib rules show review-guide`):
1. **Stage 1 — Static & Anchor Check**: Verify `2+` diagrams/page, Top Hero at `Lines 5–15` with `fold-code`, no narrow `px` fence caps, `text_size >= 10.0`, and accurate coordinate anchors (`shapes`/`text`/`icons` = **Center `(cx, cy)`** vs. `SmartArts`/`Charts`/`Diagrams`/`Graphs` = **Bottom-Left `(x0, y0)`**).
2. **Stage 2 — Micro-Geometry Grid Review (`-g`)**: Export each diagram with the 10-unit/5-unit coordinate grid (`uv run drawlib show <file> [block.png] -s styles.py -u utils.py -g -o .drawlib/scratch/preview.png`) and inspect via `view_file` to fix text clipping, arrow routing, margins (`>= 4–6` units), and `50%+` neutral balance in 1 shot.
3. **Stage 3 — Macro-Page Browser HTML Review**: Build HTML (`./build.sh`), verify zero broken links (`uv run drawlib serve docs_html/ --check`), and inspect a `1280×920` headless browser screenshot of `docs_html/*.html` via `view_file` to confirm above-the-fold Hero visibility and prose-to-diagram font size parity.

---

## 6. On-Demand Rules Catalog

Query specific detailed rule manuals as needed:

```bash
uv run drawlib rules show overview          # Geometry, coordinate space (0,0 at bottom-left), lifecycle
uv run drawlib rules show style-guide       # Color tokens, typography, 50%+ neutral rule
uv run drawlib rules show review-guide      # 3-stage multimodal review loop, 720pt font math, anchor table
uv run drawlib rules show anim-guide        # Animation loop idioms and component animation patterns
uv run drawlib rules show slide-guide       # Slide deck story arc, Dual-Layer (::: block vs. ::: note) & visual best practices
uv run drawlib rules show project-overview  # Project scaffolding (init), 4 archetypes, shared config & cache
uv run drawlib rules show project-images    # Standalone Python scripts (images_src/*.py) best practices
uv run drawlib rules show project-doc       # Linear documents, whitepapers & A4 vector PDFs (doc_src/)
uv run drawlib rules show project-site      # Multi-page websites, navbar.md & Top Hero layout (docs_src/)
uv run drawlib rules show project-slide     # 16:9 slide decks, 1920x1080 ::: block/note & Presenter View
uv run drawlib rules show cli               # CLI commands (build, show, init, serve, cache)
uv run drawlib rules show api               # Complete API index & symbol cheat sheet
uv run drawlib rules show lib-<module>      # Module specifics (e.g. lib-shapes, lib-lines, lib-diagrams, lib-graph)
```
