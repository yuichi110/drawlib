---
trigger: always_on
---

# Documentation System & Build Guidelines for drawlib

This document defines the architecture, compilation mechanisms, CLI commands, and rules for managing documentation in the `drawlib` project.

---

## 1. Core Principles & Philosophy

`drawlib` follows an **"Illustration as Code"** and **"Documentation as Code"** philosophy:
- Documentation source files are written in standard Markdown containing embedded `drawlib` code blocks.
- The built-in `drawlib.doc_builder` engine compiles these sources into publication-ready formats without requiring external documentation generators (e.g., Sphinx, MkDocs, Docusaurus).
- Three distinct output targets are supported:
  1. **Rendered Markdown (`docs/`)**: Optimized for GitHub repository browsing. Code blocks become syntax-highlighted Python blocks followed by relative image links.
  2. **Responsive Static HTML (`docs_html/`)**: Complete static documentation website with sidebar navigation, clean modern typography, responsive layout, and dark/light themes.
  3. **Headless PDF (`docs_pdf/`)**: High-fidelity PDF documents generated via headless Chromium-based browsers.

---

## 2. Directory Structure & Lifecycle

```text
drawlib/
├── docs_src/                  # [SOURCE OF TRUTH] Authoring directory. ONLY edit files here!
│   ├── index.md               # Root landing page (H1 title becomes website title)
│   ├── diagrams/              # Topic subdirectories containing .md files
│   └── images/                # Static image assets (logos, screenshots, external diagrams)
│
├── docs/                      # [GENERATED] Compiled Markdown for GitHub browsing. NEVER EDIT DIRECTLY!
│   ├── index.md
│   ├── diagrams/
│   └── *_images/              # Generated diagram PNG/SVG images for each document
│
├── docs_html/                 # [GENERATED] Compiled HTML site for web hosting. NEVER EDIT DIRECTLY!
│   ├── index.html
│   ├── style.css              # Extracted or customized CSS stylesheet
│   └── *_images/              # Generated images and copied static assets
│
└── tools/
    ├── dcli/docs.py           # Developer CLI command handlers (./dcli docs build/serve)
    └── scripts/build_docs.py  # Standalone build automation script
```

### ⚠️ The Golden Rule of Documentation
**NEVER edit files in `docs/` or `docs_html/` directly.**  
All manual edits, new chapters, or updates must be performed in `docs_src/`. Changes to `docs/` and `docs_html/` are produced exclusively by running the build pipeline.

---

## 3. `drawlib` Code Block Syntax

Embedded drawing code blocks in Markdown use the `drawlib` language identifier.

### 3.1. Basic Syntax
````markdown
```drawlib
from drawlib.canvas import config
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=30)
```
````

### 3.2. Block Header Options
Options can be specified as space-separated tokens, `key:value` pairs, or `key=value` pairs:

````markdown
```drawlib 500px center show-code caption:"Figure 1: Architecture" file:arch.png
# Code here...
```
````

Supported options:
| Option | Syntax Examples | Description |
| :--- | :--- | :--- |
| **Code Visibility** | `show-code`, `fold-code`, `hide-code`, `code:show`, `code:fold`, `code:hide` | Code display mode. Default: `hide` (renders image only). `show-code` shows Python code followed by image. `fold-code` displays image followed by collapsed `<details>` dropdown (omitted in PDF). |
| **Width** | `400px`, `100%`, `w:500px`, or integer `400` | Display width of the rendered image in HTML. |
| **Height** | `300px`, `h:300px` | Display height of the rendered image. |
| **Alignment** | `center`, `left`, `right`, `a:center` | Image alignment within the document. Default: `center`. |
| **Filename** | `file:custom_name.png` | Explicit filename for the generated image. (Default: auto-numbered `1.png`, `2.png`). |
| **Caption** | `caption:"System Overview"` | Caption displayed below the image in a `<figcaption>`. |
| **CSS Class**| `class:"shadow rounded border"` | Custom CSS classes applied to the figure wrapper. |
| **Format** | `format:png`, `format:webp` | Image output format. Default: `png`. |

### 3.3. HTML Syntax (Alternative)
For raw HTML source documents, `<drawlib>` tags or `<script type="text/drawlib">` are also supported:
```html
<drawlib width="500px" align="center" caption="My Diagram">
circle((50, 50), radius=20)
</drawlib>
```

---

## 4. Developer CLI (`dcli`) Commands

Always use `./dcli` (or `uv run python tools/scripts/...`) for standard documentation workflows.

### 4.1. Full Documentation Build
Rebuilds both `docs/` (Markdown) and `docs_html/` (HTML) from `docs_src/`:
```bash
./dcli docs build
```
Behind the scenes, this executes `uv run python tools/scripts/build_docs.py`, which:
1. Cleans existing `docs/` and `docs_html/` directories.
2. Compiles `docs_src/ -> docs/` in `markdown` mode.
3. Compiles `docs_src/ -> docs_html/` in `html` mode with default styling.

### 4.2. Local Preview Server
Starts a local development HTTP server serving `docs_html/`:
```bash
# Serve on default port 8000 (opens browser automatically):
./dcli docs serve

# Custom port without opening browser:
./dcli docs serve -p 8080 --no-browser

# Run broken link / missing asset check only and exit:
./dcli docs serve --check

# Start server skipping pre-scan checks:
./dcli docs serve --skip-check
```

### 4.3. Running Tests
```bash
# Run doc_builder unit and integration tests:
./dcli test target tests/doc_builder/

# Run CLI documentation command tests (build, show, export, serve, template):
./dcli test target tests/cli/
```

---

## 5. Direct `drawlib` CLI Commands

The `drawlib` CLI (`uv run python -m drawlib` or `drawlib`) provides fine-grained subcommands:

### 5.1. `drawlib build` (Document Compiler)
Compiles a single file or directory to HTML, Markdown, or PDF:
```bash
# Compile single markdown to HTML:
drawlib build doc.md -o output.html

# Compile single markdown to rendered Markdown for GitHub:
drawlib build doc.md -o rendered.md -f markdown

# Compile entire directory to HTML site:
drawlib build docs_src/ -o docs_html/ -f html

# Export to PDF via headless browser:
drawlib build doc.md -o output.pdf -f pdf

# Compile with external config, custom CSS, or custom Jinja2 template:
drawlib build docs_src/ -o docs_html/ --config config.py --css custom.css -t custom_template.j2
```

Key Options:
- `-o`, `--output <path>`: Destination file or directory.
- `-f`, `--format <html|pdf|markdown>`: Output document format.
- `--image-format <png|svg|inline_svg>`: Format for rendered illustration images (default: `png`).
- `--css-mode <auto|embed|external>`: CSS embedding strategy for HTML. `auto` embeds for single files and writes `style.css` for directories.
- `--config <path>`: Python configuration script executed before code blocks (e.g. setting themes, fonts, canvas defaults).
- `--css <path>`: Custom CSS file to augment or override default styles.
- `-t`, `--template <path>`: Custom Jinja2 HTML template file.

### 5.2. `drawlib export` (Single Diagram Export)
Extracts and renders an individual illustration from a Markdown file or Python script directly to an image file. Designed for CI, AI verification, and automation without GUI displays.
```bash
# List all drawlib blocks found in a document:
drawlib export doc.md

# Export block by index (1-based) to specific path:
drawlib export doc.md 1 -o scratch/diagram_1.png

# Export block by target image name:
drawlib export doc.md diagram.png -o scratch/diagram.png

# Apply custom configuration script:
drawlib export doc.md 1 -c config.py -o scratch/diagram.png

# Overlay coordinate grid lines and center axes:
drawlib export doc.md 1 -g -o scratch/diagram_grid.png

# Export directly from a standalone Python script:
drawlib export my_drawing.py -o scratch/drawing.png
```

### 5.3. `drawlib show` (Desktop Preview)
Displays the rendered illustration in a local GUI window:
```bash
# Preview block 1 in GUI window:
drawlib show doc.md 1

# Preview with coordinate grid overlay:
drawlib show doc.md 1 --grid

# Headless mode: save directly to file without GUI popup (same as export):
drawlib show doc.md 1 -o preview.png
```

### 5.4. `drawlib template` (HTML Template Management)
```bash
# Export the built-in Jinja2 sidebar template for customization:
drawlib template export my_template.html.j2

# Validate a custom Jinja2 template for required placeholders:
drawlib template validate my_template.html.j2
```

---

## 6. Internal Architecture & Compilation Mechanics

The `drawlib._tools.doc_builder` package is structured into clean, modular layers:

```text
src/drawlib/_tools/doc_builder/
├── __init__.py           # High-level pipeline orchestration: build(), build_document()
├── config.py             # Config loader (load_config): namespace setup and shared globals
├── parser_md.py          # Markdown AST parser (parse_markdown_to_html) via markdown-it-py
├── processor.py          # Code block extraction (DrawlibBlockProcessor, export_code_block, show_code_block)
├── exporter_md.py        # Rendered Markdown writer (write_rendered_markdown)
├── exporter_html.py      # HTML renderer (render_html_document, get_default_css)
├── exporter_pdf.py       # Headless Chromium printer (export_html_to_pdf, find_system_browser)
├── template.py           # Template export and Jinja2 AST validator (validate_template)
├── html_templates/       # Built-in Jinja2 templates (sidebar.html.j2, simple.html.j2)
└── html_styles/          # Built-in CSS (default.css, pygments.css)
```

### 6.1. Execution Context & Isolation
1. **Working Directory & Path Resolution**:
   When compiling a code block, `processor.py` temporarily switches working directory (`os.chdir`) to the document's directory and inserts it into `sys.path[0]`. This guarantees relative imports and relative asset paths resolve identically to running the script directly.
2. **Global Namespace Injection**:
   `config.py` automatically injects all drawlib domain symbols (`canvas`, `shapes`, `lines`, `text`, `icons`, `smartarts`, `charts`, `colors`, etc.) into the block's `shared_globals`. Authors do not need boilerplate imports in every Markdown block.
3. **Canvas State Isolation**:
   The canvas is automatically cleared and re-initialized between blocks to prevent leaking shapes or themes across illustrations.

### 6.2. Navigation & Static Asset Pipeline
- **Title Extraction**: The document's title is extracted from the first `# Heading 1` in the Markdown source.
- **Sidebar Navigation**: For multi-file directories, `_build_directory_nav_list()` indexes all Markdown files, placing `index.md` at the top, computing relative hyperlinks (`.html`), and marking active pages.
- **Static Assets**: Non-markdown files (images, fonts, PDFs) in the source directory are copied to the destination preserving directory structure.
- **Static Image Validation**: Local images referenced via `![alt](path)` are validated before compilation, emitting warnings if missing.

### 6.3. Headless PDF Compilation
`exporter_pdf.py` detects local Chromium installations (Chrome, Chromium, Edge) or uses `DRAWLIB_CHROME_PATH`. It executes:
```bash
<browser> --headless --disable-gpu --print-to-pdf=<out.pdf> <temp_html>
```
This produces crisp vector PDFs without requiring heavy browser automation packages like Playwright or Selenium.

---

## 7. AI & Contributor Workflow Guidelines

1. **Authoring Changes**:
   - Write or update Markdown files exclusively under `docs_src/`.
   - Ensure each file begins with a single `# Document Title` header.
   - Use relative links to reference other documentation files (e.g. `[Quickstart](quickstart.md)`). The compiler automatically rewrites them to `.html` in HTML builds.
2. **Rapid Verification during Development**:
   - Do **NOT** run `./dcli docs build` repeatedly while tweaking an individual diagram (it rebuilds the entire site).
   - Instead, use `drawlib export` to quickly render the specific block:
     ```bash
     uv run python -m drawlib export docs_src/diagrams/state_diagram.md 1 -o scratch/test.png
     ```
   - Inspect the generated image using `view_file` to verify layout and aesthetics.
3. **Pre-Commit Verification**:
   - Once content is finalized, run the full build:
     ```bash
     ./dcli docs build
     ```
   - Run static checks and CLI tests:
     ```bash
     ./dcli check all
     ./dcli test target tests/cli/
     ```
   - Verify that Git status shows changes in `docs_src/`, `docs/`, and `docs_html/` as expected.