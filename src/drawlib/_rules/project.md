# Drawlib Project Architecture & Scaffolding Guidelines

Drawlib provides a complete project scaffolding and document build engine. It turns Markdown documents containing embedded `drawlib` Python blocks into publication-ready static HTML documentation sites, GitHub-flavored Markdown, headless vector PDFs, or standalone image assets.

---

## 1. Project Scaffolding (`drawlib init`)

> **Important**: Do **NOT** create project structures from scratch manually.  
> Always use `drawlib init` to scaffold the standard directory layout, configuration scripts, and build automations.

### Basic Syntax:
```bash
# List available starter templates:
drawlib init list

# Scaffold a project into a new destination directory:
drawlib init <type> [destination]

# Scaffold directly into the current directory (no wrapper subfolder):
drawlib init <type> --here

# Custom output project name (e.g. source is rbac_src/, targets rbac_html, rbac.pdf):
drawlib init doc my_report/ -o rbac -s google
```

### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<name>` | `docs` / `slide` / `images` | Base project and artifact name. Sets source folder to `<name>_src` and output targets accordingly (e.g. `<name>_html/`, `<name>.pdf`, `images/`). |
| `--style` | `-s` | `<theme>` | `default` | Style preset theme (`default`, `google`, `monochrome`, etc.) or custom CSS path. Synchronously configures both `style.css` and `styles.py`. |
| `--lang` | `-l` | `<lang>` | `en` | Starter template language code (`en`, `ja`, `zh-cn`, `ko`, `th`, `hi`, etc.). |
| `--here` | | flag | `False` | Scaffold directly in current working directory without a wrapper folder. |
| `--force` | `-f` | flag | `False` | Overwrite existing files if directory is not empty. |

> **Pure Scaffolding Principle**: `drawlib init` only scaffolds template and configuration files; it never runs compilation automatically. To build your project, run `./build.sh` (or the specific `./build_*.sh` script).

---

## 2. The 4 Project Types

Drawlib features 4 built-in project starter templates tailored to different publication workflows:

| Project Type | Purpose | Source Directory | Generated Artifacts | Best Used For |
| :--- | :--- | :--- | :--- | :--- |
| **`doc`** | **Linear Document** | `docs_src/` | `doc.html` (Web preview)<br>`doc.pdf` (Printable vector PDF)<br>`doc.md` (GitHub Markdown)<br>`images/*.png` (Extracted diagrams) | Technical specifications, RFCs, design docs, whitepapers, formal reports, and thesis papers. |
| **`site`** | **Multi-Page Website** | `docs_src/` | `docs_html/` (HTML site)<br>`docs/` (GitHub Markdown) | Software documentation, technical guides, architectural handbooks, API manuals. |
| **`slide`** | **Presentation Deck** | `slide_src/` | `slide/index.html` (Web)<br>`slide.pdf` (Printable vector PDF) | Conference talks, technical briefings, pitch decks, architectural presentations. |
| **`image`** | **Standalone Image Scripts** | `images_src/` | `images/*.png` (or `.webp`) | Generating standalone architecture diagrams, social cards, or presentation assets from Python scripts. |

---

## 3. Directory Structures & Anatomy of Generated Files

### 3.1 Linear Document (`doc` Template)
```text
my_doc/
├── docs_src/                  # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── 00_cover.md            # Cover page (title, author, metadata)
│   ├── 01_overview.md         # Executive overview chapter
│   ├── 02_design.md           # Technical design chapter
│   ├── styles.py              # Project-wide styling themes and color overrides
│   ├── utils.py               # Custom helper drawing functions
│   ├── build.sh               # Master build script (runs all target builds)
│   ├── build_html.sh          # Fast preview HTML build (doc.html)
│   ├── build_pdf.sh           # Headless Chromium vector PDF build (doc.pdf)
│   ├── build_markdown.sh      # Rendered Markdown for GitHub browsing (doc.md)
│   ├── build_image.sh         # Extract embedded drawlib blocks to images/
│   ├── serve.sh               # Local preview server script
│   └── README.md              # Project instructions
├── doc.html                   # [GENERATED] Single-page HTML document
├── doc.pdf                    # [GENERATED] High-quality vector PDF
├── doc.md                     # [GENERATED] Markdown with rendered images for GitHub
└── images/                    # [GENERATED] Extracted diagram images
```

### 3.2 Documentation Site (`site` Template)
```text
my_project/
├── docs_src/                  # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── index.md               # Root landing page
│   ├── navbar.md              # Sidebar navigation and brand definition
│   ├── styles.py              # Project-wide styling themes and color overrides
│   ├── utils.py               # Custom helper drawing functions
│   ├── build.sh               # Master build script (runs HTML + Markdown builds)
│   ├── build_html.sh          # Static HTML website build
│   ├── build_markdown.sh      # Rendered Markdown for GitHub browsing
│   ├── serve.sh               # Local preview server script
│   ├── README.md              # Project instructions
│   └── architecture/          # Chapter / section subdirectories
│       └── index.md
├── docs/                      # [GENERATED] Markdown site for GitHub (NEVER EDIT DIRECTLY!)
│   ├── index.md
│   └── index_images/          # Rendered companion images
└── docs_html/                 # [GENERATED] Static HTML website with sidebar (NEVER EDIT DIRECTLY!)
    ├── index.html
    └── index_images/
```

### 3.3 Presentation Deck (`slide` Template)
```text
my_slides/
├── slide_src/                 # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── 01_title.md            # Title slide
│   ├── 02_agenda.md           # Agenda slide
│   ├── 03_architecture.md     # Architecture slide with diagrams
│   ├── styles.py              # Slide-wide styling and color overrides
│   ├── utils.py               # Slide layout helpers (cards, badges, grids)
│   ├── slide.js               # Slide runtime keyboard / navigation engine
│   ├── build.sh               # Master build script (HTML + PDF)
│   ├── build_html.sh          # HTML presentation deck build
│   ├── build_pdf.sh           # 16:9 vector PDF presentation export (1 slide per page)
│   ├── serve.sh               # Local preview server script
│   └── README.md              # Slide authoring guide
├── slide/                     # [GENERATED] HTML presentation deck
│   ├── index.html
│   └── index_images/
└── slide.pdf                  # [GENERATED] High-quality vector presentation PDF
```

### 3.4 Standalone Images Project (`image` Template)
```text
my_images_project/
├── images_src/                # [SOURCE OF TRUTH] Python drawing scripts (*.py)
│   ├── sample1.py             # Starter Drawlib drawing script
│   ├── sample2.py             # Advanced drawing script
│   ├── styles.py              # Shared project styling themes
│   ├── utils.py               # Shared project helper functions
│   ├── build.sh               # Master build script
│   ├── build_image.sh         # Batch image rendering script
│   └── README.md              # Illustration workflow guide
└── images/                    # [GENERATED] Rendered PNG/WebP output images
    ├── sample1.png
    └── sample2.png
```

### 3.5 Modular Build Scripts Architecture
Each project type generates focused, specialized shell scripts alongside a master `build.sh`:
- **`build_html.sh`**: Fast preview HTML build. Perfect for rapid editing and browser verification.
- **`build_pdf.sh`**: Headless Chromium print to vector PDF. Respects `@page` sizing (A4 for `doc`, 16:9 for `slide`).
- **`build_markdown.sh`**: Replaces ````drawlib```` blocks with generated image links for GitHub repo viewing.
- **`build_image.sh`**: Generates standalone image files (executing Python scripts for `image`, or extracting embedded code blocks for `doc`).
- **`build.sh` (Master)**: Sequentially executes all target builds applicable to the project.

### Golden Rule of Documentation:
- **Source of Truth**: Edit files **strictly** inside `<base>_src/` (e.g. `docs_src/` or `images_src/`).
- **Never Manually Edit Output Directories**: Folders like `docs/`, `docs_html/`, or `images/` are managed and regenerated by Drawlib. Manual edits will be overwritten on the next build.

---

## 4. Sidebar Navigation Architecture (`navbar.md`)

Multi-page documentation sites (`site` template) define sidebar navigation in `docs_src/navbar.md`:

```markdown
# Cloud Platform Architecture

- [Home](index.md)

## Core Infrastructure
- [VPC & Networking](infrastructure/vpc.md)
- [Kubernetes Clusters](infrastructure/k8s.md)

## Microservices
- [Authentication Gateway](services/auth.md)
- [Order Processing](services/orders.md)

## External Links
- [GitHub Repository](https://github.com/example/repo)
```

### Authoring Rules & Syntax:
1. **Brand Name (Heading 1)**:
   - The first `# Heading 1` defines the brand title displayed in the top-left sidebar header.
2. **Category Grouping (Heading 2)**:
   - Each `## Heading 2` defines a distinct navigation section in the sidebar.
   - Bullets placed before the first `##` become top-level ungrouped items.
3. **Internal Links**:
   - Bullet items `- [Title](path/to/doc.md)` specify Markdown files relative to `navbar.md`.
   - Anchors are supported: `- [Section](path.md#section-anchor)`.
4. **External Links**:
   - URLs starting with `http://` or `https://` automatically render with external link icons and open in a new tab (`target="_blank"`).
5. **Strict Build-Time Link Validation**:
   - Drawlib validates every internal file reference in `navbar.md` during compilation.
   - If any linked Markdown file does not exist, the build immediately aborts with a descriptive error specifying the missing file and line number.
6. **Active Page Tracking**:
   - The currently displayed page is highlighted automatically (`.nav-item.active`) with dynamic relative path computation for nested directories.

---

## 5. Document Authoring & Embedded Code Blocks (````drawlib````)

Embed Python drawing code directly into Markdown files using the ````drawlib```` code fence:

````markdown
```drawlib 600px center caption:"System Architecture"
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.lines import line
from drawlib.shapes import rectangle

setup(width=100, height=50)

rectangle((25, 25), width=30, height=20, style=Styles.PrimaryFlat, text="Client", text_style=Styles.WhiteBold)
rectangle((75, 25), width=30, height=20, style=Styles.SecondaryFlat, text="Server", text_style=Styles.WhiteBold)
line((40, 25), (60, 25), arrow_head="->", style=Styles.PrimaryBold)
```
````

### Header Options:
- **Code Visibility**:
  - `hide-code` *(default)*: Renders illustration only.
  - `show-code`: Displays Python source followed by the rendered image.
  - `fold-code`: Displays image followed by a collapsed `<details><summary>Source Code</summary>...</details>` dropdown.
- **Dimensions**: `500px`, `600px`, `100%` (width tokens).
- **Alignment**: `center` *(default)*, `left`, `right`.
- **Caption**: `caption:"Description"` (rendered in `<figcaption>`).
- **Filename**: `file:custom_name.png` (explicitly name the companion image).

### Auto-Injected Globals & Sandbox:
- Common Drawlib modules (`canvas`, `shapes`, `lines`, `text`, `icons`, `smartarts`, `charts`, `colors`, `styles`) are pre-injected into globals for concise code blocks.
- The canvas lifecycle (`clear()`) automatically resets between consecutive code blocks to prevent image bleeding.
- **Handling `save()`**: The build engine automatically captures and saves the canvas upon block completion. Calling `save()` is optional (and safely treated as a no-op if present). Including `save()` in complete examples is recommended for standalone `.py` portability.

---

## 6. Compilation Pipelines (`drawlib build`)

### Recommended: Use `build.sh`
Projects scaffolded with `drawlib init` include a self-contained `build.sh`:
```bash
./build.sh
```

### Direct CLI Commands:
```bash
# 1. Compile multi-page directory or linear document to HTML:
drawlib build html docs_src/ -o docs_html/ -s styles.py -u utils.py

# 2. Compile directory or linear document to GitHub-ready rendered Markdown:
drawlib build markdown docs_src/ -o docs/ -s styles.py -u utils.py

# 3. Compile linear document or slide presentation to vector PDF:
drawlib build pdf docs_src/ -o doc.pdf -s styles.py
drawlib build pdf slide_src/ -o slide.pdf

# 4. Extract embedded Markdown diagrams to standalone images:
drawlib build image docs_src/ -o images/ -s styles.py

# 5. Compile standalone Python illustration scripts to images:
drawlib build image images_src/ -o images/ -s styles.py
```

### Key Options:
- `-o`, `--output <path>`: Destination directory or file path.
- `-s`, `--styles <path>`: Python styles script containing custom themes (e.g. `styles.py`).
- `-u`, `--utils <path>`: Python utils script containing helper functions (e.g. `utils.py`).
- `--no-cache`: Force complete re-rendering, ignoring the SQLite image cache.

### Overwrite Protection:
Drawlib strictly prevents accidental source loss: `drawlib build` refuses to run if input source and destination path point to the exact same directory (`src_abs == dest_abs`).

---

## 7. Local Preview & Link Verification (`drawlib serve`)

Preview the generated static HTML site with built-in asset and broken-link scanning:

```bash
# Preview using scaffolded script inside source directory or project root:
./serve.sh

# Or start local development server directly (default port 8000, opens browser):
drawlib serve docs_html/

# Start server on custom port without opening browser:
drawlib serve docs_html/ -p 8080 --no-browser

# Run link, anchor, and image asset verification only and exit:
drawlib serve docs_html/ --check
```

---

## 8. Recommended Agent & Developer Workflow

When creating or modifying documentation:
1. **Rapid Diagram Iteration**:
   Do **not** rebuild the entire documentation site to test a single diagram!
   Export and inspect individual diagrams instantly into the isolated `.drawlib/scratch/` directory using `drawlib show` (ensure `.drawlib/` is in `.gitignore`):
   ```bash
   uv run drawlib show docs_src/architecture/index.md 1 -g -o .drawlib/scratch/test.png
   ```
2. **Multimodal Verification**:
   Inspect `.drawlib/scratch/test.png` with your image viewing tool (`view_file`). Check spatial alignment, text clipping, and margin breathing room.
3. **Full Site Build**:
   Once code blocks are verified, compile the complete project:
   ```bash
   ./build.sh
   ```
4. **Site Health Check**:
   Run pre-flight link validation:
   ```bash
   uv run drawlib serve docs_html/ --check
   ```

---

## 9. Related Rules

- AI Agent Instructions: `uv run drawlib rules show agent-instruction`
- Aesthetic & Style Guide: `uv run drawlib rules show style-guide`
- Drawing Engine Overview: `uv run drawlib rules show overview`
- CLI Reference & Commands: `uv run drawlib rules show cli`
- Python Tools API: `uv run drawlib rules show lib-tools`
- Dynamic Styles & Theming: `uv run drawlib rules show lib-styles`
