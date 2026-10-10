# Drawlib Multi-Page Documentation Website Guidelines (`project-site`)

A **`site` project** (`drawlib init site`) compiles a directory tree of Markdown files (`docs_src/**/*.md`) governed by a sidebar definition (`docs_src/navbar.md`) into a **responsive multi-page static HTML documentation website (`docs_html/`)**, **GitHub-Flavored Markdown (`docs_markdown/`)**, and **extracted diagram assets (`docs_images/`)**.

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For single-file linear documents/PDFs, see `uv run drawlib rules show project-doc`. For the 3-stage review loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. When to Choose a `site` Project

Choose `drawlib init site` when the user wants a **multi-page documentation website with a navigation sidebar**:
- Official library or product documentation portals (such as Drawlib's own `docs/docs_src/`).
- Multi-chapter architecture handbooks, onboarding portals, and internal engineering wikis.
- Any documentation set with 4+ distinct topic pages organized into sidebar categories.

```bash
# Scaffold a multi-page documentation site (default target 'docs', creates 'docs_src/'):
uv run drawlib init site [target] [-l <lang>] [-s <default|google|monochrome>]

# Examples:
uv run drawlib init site --lang ja -s google
uv run drawlib init site docs -s default
```

---

## 2. Directory Structure & Mandatory Files (`docs_src/`)

```text
.
├── docs_src/                  # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── index.md               # [MANDATORY] Root landing page
│   ├── navbar.md              # [MANDATORY] Sidebar navigation menu & brand definition
│   ├── 01_getting_started/    # Categorized chapter subdirectories
│   │   ├── overview.md
│   │   └── quickstart.md
│   ├── 02_architecture/
│   │   ├── overview.md
│   │   └── data_model.md
│   ├── _assets/               # Static images, logos, or custom .ttf/.otf fonts
│   ├── styles.py              # Site-wide Drawlib Styles & Colors
│   ├── utils.py               # Site-wide Python drawing helpers & macros
│   ├── style.css              # Responsive HTML & sidebar CSS theme
│   ├── template.html          # Jinja2 multi-page HTML layout template
│   ├── build.sh               # Master build script (HTML + Markdown + Images)
│   ├── build_html.sh          # Static HTML website build (docs_html/)
│   ├── build_markdown.sh      # GitHub-ready Markdown build (docs_markdown/)
│   ├── build_image.sh         # Standalone diagram extraction (docs_images/)
│   └── serve.sh               # Local preview server + broken link checker
├── docs_html/                 # [GENERATED] Static HTML website with sidebar
├── docs_markdown/             # [GENERATED] Rendered Markdown for GitHub browsing
└── docs_images/               # [GENERATED] Extracted diagram PNG/WebP images
```

```drawlib center fold-code file:project_site_architecture.png caption:"Multi-Page Documentation Website (docs_src/) Architecture & Above-the-Fold Page Layout"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=58, dpi=150)

rectangle((75, 29), width=144, height=52, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (75, 50.5),
    "Multi-Page Website Architecture (docs_src/ -> docs_html/)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# 1. navbar.md + Page Tree
rectangle((26, 25), width=38, height=34, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.list_bullets((12, 36.5), width=5.0, style=Styles.PrimaryBold)
text((28, 36.5), "1. navbar.md & Tree", style=Styles.PrimaryBold.patch(text_size=11.5))
text(
    (26, 21),
    "• # Brand Title (H1)\n• ## Category (H2)\n• - [Page](path.md)\n• Build-time link check",
    style=Styles.Dark.patch(text_size=10.0),
)

line((45.5, 25), (54.5, 25), arrow_head="->", style=Styles.DarkBold)

# 2. Page Composition Rules
rectangle((75, 25), width=40, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.layout((60.5, 36.5), width=5.0, style=Styles.SecondaryBold)
text((77, 36.5), "2. Page Anatomy", style=Styles.SecondaryBold.patch(text_size=11.5))
text(
    (75, 21),
    "• Hero at Lines 5–15\n• fold-code & 2+ figs\n• 100% container width\n• text_size >= 10.0",
    style=Styles.Dark.patch(text_size=10.0),
)

line((95.5, 25), (104.5, 25), arrow_head="->", style=Styles.DarkBold)

# 3. Browser & Link Verification
rectangle((124, 25), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.browser((110, 36.5), width=5.0, style=Styles.WhiteBold)
text((126, 36.5), "3. Browser Check", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (124, 21),
    "• drawlib serve --check\n• 1280x920 Playwright\n• Above-the-fold Hero\n• Prose vs Fig parity",
    style=Styles.White.patch(text_size=10.0),
)

save()
```

---

## 3. Sidebar Navigation Architecture (`navbar.md`)

`docs_src/navbar.md` is **mandatory** for every `site` project and defines the persistent left navigation sidebar:

```markdown
# Cloud Platform Docs

- [Home](index.md)

## 1. Getting Started
- [Architecture Overview](01_getting_started/overview.md)
- [Quickstart Guide](01_getting_started/quickstart.md)

## 2. Core Services
- [Authentication Gateway](02_services/auth.md)
- [Order Pipeline](02_services/orders.md)

## External Links
- [GitHub Repository](https://github.com/example/platform)
```

### `navbar.md` Authoring Rules:
1. **Brand Title (`# Heading 1`)**: The first `# Heading 1` sets the site brand title displayed in the top-left sidebar header.
2. **Category Sections (`## Heading 2`)**: Each `## Heading 2` creates a collapsible/grouped category section in the sidebar. Bullet items placed before the first `##` render as top-level ungrouped links (e.g. `Home`).
3. **Internal Page Links (`- [Label](relative/path.md)`)**:
   - Paths are resolved relative to `docs_src/`.
   - Section anchors are supported (`- [Section](path.md#anchor)`).
   - **Strict Build-Time Link Validation**: Every local `.md` file referenced in `navbar.md` is verified during `drawlib build html`. If a target file is missing or misspelled, compilation halts immediately with the exact line number.
   - **Every New Page Must Be Registered**: Whenever you create a new `.md` page in `docs_src/`, add it to `navbar.md` and link to it from its parent/overview page.
4. **External Links**: Links starting with `http://` or `https://` automatically render with an external-link icon and `target="_blank"`.

---

## 4. Page Authoring & Visual Composition Best Practices

To achieve true **"Illustrated Documentation as Code"**, every page in `docs_src/` must follow these four layout laws:

### 4.1. Law 1: Above-the-Fold Top Hero Diagram (`Lines 5–15` + `fold-code`)
When a reader opens any page in `docs_html/` at a standard desktop viewport (`1280×920`), they must immediately see a rich architectural illustration—**never a wall of text or a 60-line Python code block**:
- Place the first ```` ```drawlib ```` block at **Lines 5–15** (immediately after `# Page Title` and a 1–2 sentence executive summary).
- Always specify **`fold-code`** on the Top Hero diagram (or `hide-code` on `index.md`) so the rendered illustration is displayed first and its Python source is tucked neatly inside a collapsible `<details><summary>Source Code</summary>` drawer.
- **Visual Richness**: Combine official iconography (`phosphor.*`, `gcp.*`, `font_icon`) with high-level layout components (`SmartArts`, `Diagrams`, `Graphs`, `Charts`) so the Top Hero serves as a visual mental map of the entire page.

````markdown
# Authentication & Zero-Trust Gateway

The Authentication Gateway terminates external TLS traffic, validates OAuth 2.0 / OIDC tokens, and enforces role-based access control (RBAC) across internal microservices.

```drawlib center fold-code file:auth_gateway_hero.png caption:"Authentication Gateway & mTLS Service Mesh Topology"
from drawlib.canvas import save, setup
...
save()
```
````

### 4.2. Law 2: Visual Density (`2+` Diagrams per Page)
- Include **at least `2` embedded ```` ```drawlib ```` diagrams per page**:
  1. **Top Hero Diagram (`fold-code`)**: High-level conceptual overview or architecture at `Lines 5–15`.
  2. **Section / Deep-Dive Diagram(s) (`fold-code` or `show-code`)**: Sequence flows, state transitions, data tables, or API examples illustrating specific subsections.
- **Always Specify `file:<name>.png` and `caption:"..."`**: Never rely on auto-numbered filenames (`0.png`, `1.png`), which shift and break caches whenever a block is inserted above them.

### 4.3. Law 3: Full Container Width & `720pt` Typography Scaling
Drawlib maps every canvas width (`setup(width=W)`) to `720pt` (`10 inches`), meaning any in-image `text_size` renders in HTML at:

$$\text{Rendered CSS Font Size (px)} = \text{text\_size} \times \frac{\text{Displayed Image Width (px)}}{720}$$

1. **Omit Narrow Pixel Width Caps on Fences**: Never add `500px`, `600px`, or `680px` to ```` ```drawlib ```` fences on standard documentation pages. Omitting pixel widths lets `.drawlib-image` fill `100%` of the content column (`~880px–960px`, `max-width: 1000px`).
2. **Set `text_size >= 10.0`**:
   - **Standard Node / Card / Axis Labels**: `text_size = 10.5` – `12.0` (renders at `~13.5px–15.5px` in HTML, matching `16px` body prose).
   - **Diagram Titles & Section Headers**: `text_size = 12.0` – `14.5`.
   - **Dense Code (`SourceCode`) / Small Badges**: `text_size >= 9.5` (strict minimum floor).
   - When increasing `text_size`, proportionally widen boxes (`width += 20%–30%`) and `Table` `col_widths` so labels never clip.

### 4.4. Law 4: Cross-Page Relative Markdown Links & Asset References
- **Strictly Relative Links**: In Markdown prose (`[Link Text](../02_architecture/overview.md)`), write links as relative `.md` paths (Drawlib's HTML compiler automatically rewrites internal `.md` links to `.html` in `docs_html/` while preserving `.md` in `docs_markdown/`).
- **Static Assets (`_assets/`)**: Reference local assets relatively from the current file (e.g. `![Logo](_assets/logo.png)` or `![Architecture](../_assets/arch.png)`).
- **No Absolute Paths or `file://` URLs**: Never write local filesystem absolute paths (`/usr/...`, `/home/...`, `/Users/...`, `C:\...`) or `file:///` URLs in documentation Markdown. All links and image paths must be relative or inline code.
- **Distinction from Agent Chat**: While the AI assistant uses `file:///` links when conversing with the user in chat responses for clickable local IDE navigation, repository documentation files published on the web or GitHub must never contain `file:///` or machine-specific absolute paths.
- **Automated Build Validation**: `drawlib build` automatically scans all links and images and aborts with line numbers if any forbidden `file://` or absolute filesystem path is detected.

---

## 5. Autonomous 3-Stage Verification Loop for `site` Projects

Never deliver changes to `docs_src/` without executing all 3 verification stages:

1. **Stage 1 — Static & Anchor Audit**:
   Verify `>= 2` diagrams per page, Top Hero at `Lines 5–15` with `fold-code`, zero narrow `px` fence caps, `text_size >= 10.0`, zero `file://` or absolute path links, and accurate `Center` (`shapes`/`text`/`icons`) vs. `Bottom-Left` (`SmartArts`/`Charts`/`Diagrams`/`Graphs`) coordinate anchors.
2. **Stage 2 — Micro-Geometry Grid Review (`drawlib show ... -g` + `view_file`)**:
   Export each modified diagram with the coordinate grid to `.drawlib/scratch/` (do not rebuild the entire site just to test one diagram):
   ```bash
   uv run drawlib show docs_src/02_architecture/overview.md auth_gateway_hero.png \
       -s docs_src/styles.py -u docs_src/utils.py \
       -g -o .drawlib/scratch/preview.png
   ```
   Inspect `.drawlib/scratch/preview.png` via `view_file` and fix any overlapping text, arrow collisions, perimeter margins (`< 4–6` units), or Rainbow Color Chaos (`50%+` neutral cards).
3. **Stage 3 — Macro-Page Browser HTML & Link Verification**:
   Compile the site and run the automated link/asset scanner:
   ```bash
   ./docs_src/build.sh
   uv run drawlib serve docs_html/ --check
   ```
   Then capture a `1280×920` headless Chromium screenshot of the modified `docs_html/<page>.html` page via Playwright and inspect it with `view_file` to confirm:
   - The `# Title`, lead paragraph, and **Top Hero diagram** are immediately visible above the fold without scrolling.
   - Diagram labels match the surrounding `16px` HTML body prose in visual font size.
   - Clean up `.drawlib/scratch/` when finished.
