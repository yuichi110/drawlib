# Drawlib CLI Guidelines

Drawlib provides a unified, production-grade Command Line Interface (`drawlib` / `python -m drawlib`) for compiling documentation, extracting standalone visual diagrams, managing cache assets, validating templates, and executing batch rendering workflows.

This document serves as an exhaustive reference and operational manual for software engineers, CI/CD pipelines, and AI pair-programming agents.

---

## Quick Reference & Subcommand Overview

```bash
# Compile documentation and illustrations
drawlib build html docs_src/ -o docs_html/ --css google     # Multi-page responsive HTML site
drawlib build markdown docs_src/ -o docs/                  # Rendered Markdown for GitHub browsing
drawlib build pdf docs_src/ -o manual.pdf --toc --css book  # Merged vector PDF via headless Chromium
drawlib build image scripts/ -o assets/ -g                 # Batch Python illustration rendering

# Project scaffolding
drawlib init site my_site/                                 # Create multi-page website project
drawlib init simple my_doc/                                # Create single-page document project
drawlib init pdf my_report/                                # Create multi-chapter PDF book project
drawlib init site --here                                   # Scaffold directly into current directory

# Inspection, visual preview, and extraction
drawlib export doc.md 1 -o scratch/fig1.png                # Extract block #1 without GUI
drawlib export doc.md 1 -g -o scratch/fig1_grid.png        # Extract block #1 with coordinate grid
drawlib export script.py -o scratch/script.png             # Render standalone Python script to image
drawlib show doc.md 1 --grid                               # Open desktop GUI preview with grid
drawlib show script.py                                     # Preview standalone Python script

# Local preview server and link verification
drawlib serve docs_html/                                   # Local HTTP server on http://localhost:8000
drawlib serve docs_html/ --check                           # Pre-flight broken link/asset check & exit
drawlib serve docs_html/ -p 8080 --no-browser              # Headless server on custom port

# Cache, template, and preset management
drawlib cache list                                         # Inspect cached font and icon assets
drawlib cache clear                                        # Purge downloaded font and icon cache
drawlib cache download --all                               # Pre-download all font/icon release assets
drawlib template html list                                 # List built-in HTML Jinja2 templates
drawlib template html export sidebar -o template.html.j2   # Export built-in sidebar template
drawlib template html validate template.html.j2            # Validate Jinja2 AST placeholders
drawlib css html list                                      # List built-in HTML stylesheets
drawlib css html export google -o style.css                # Export Google styling preset

# AI agent knowledge base
drawlib rules list                                         # List available architectural rule topics
drawlib rules show cli                                     # Display this CLI reference guide
drawlib rules show docs_build                              # Display documentation build conventions
```

---

## Global CLI Options & Runtime Environment

The `drawlib` command conforms to standard POSIX-compliant CLI conventions. Global options apply across all top-level commands and subcommands:

```bash
drawlib [GLOBAL_OPTIONS] COMMAND [SUBCOMMAND] [ARGS...]
```

### Global Options:
- `-v`, `--version`: Print library version and API specification version to `stderr`, then exit with status code 0.
- `-h`, `--help`: Display contextual help messages, arguments, options, and subcommand listings.
- `--quiet`: Suppress non-critical standard output. Only warnings and error messages are emitted.
- `--verbose`: Enable verbose logging including timing metrics and complete execution traces.
- `--debug`: Alias for `--verbose`. Emits diagnostic log messages.
- `--developer`: Developer mode. Enables verbose logging and disables user-facing error suppression, allowing full unhandled Python exceptions and tracebacks to propagate.

> **Note**: `--quiet` cannot be combined with `--verbose`, `--debug`, or `--developer`. Doing so triggers exit code 2 (`BadParameter`).

---

## 1. Document & Illustration Compiler (`drawlib build`)

The `drawlib build` subsystem compiles Markdown documents, HTML pages, and standalone Python illustration scripts into production-ready publishing targets.

```text
drawlib build
├── html       Compile Markdown/HTML documents into static HTML sites or single pages
├── markdown   Compile Markdown files with embedded drawlib blocks into GitHub-ready Markdown
├── pdf        Merge Markdown/HTML files into a cohesive vector PDF via headless Chromium
└── image(s)   Batch execute standalone Python scripts to generate image files
```

Common build behavior:
- **Automatic Clear / Reset**: Between separate code blocks or Python files, canvas state is automatically reset to avoid cross-diagram side effects.
- **SQLite Build Cache**: Rendered illustrations are hashed and stored in a local SQLite database (`.drawlib_cache/build_cache.sqlite`). Unchanged code blocks skip re-rendering automatically unless `--no-cache` is specified.
- **Working Directory Parity**: When compiling blocks, drawlib switches the current working directory (`os.chdir`) to the document's directory and prepends it to `sys.path[0]`, ensuring relative asset references and module imports resolve identically to standalone execution.

---

### 1.1 `drawlib build html` (Static Site & Single Page HTML)

Compiles a single Markdown/HTML document or an entire directory into responsive HTML with modern styling, sidebar navigation, dark/light theme support, and syntax highlighting.

#### Syntax:
```bash
drawlib build html <INPUT> [OPTIONS]
```

#### Arguments:
- `<INPUT>`: Path to input Markdown (`.md`), HTML (`.html`), or directory containing documentation.

#### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<path>` | `<input_dir>` or `<name>.html` | Destination HTML file path or output directory path. |
| `--config` | `-c` | `<path>` | `None` | Path to Python configuration script executed before blocks (e.g. `docs_config.py`). |
| `--css` | | `<name\|path>`| `default` | Built-in CSS preset (`default`, `google`, `github`, `minimal`, `monochrome`, or dark variants) or custom `.css` file path. |
| `--template` | `-t` | `<name\|path>`| `sidebar` (dir) / `simple` (file) | Built-in template preset (`sidebar`, `simple`) or path to custom `.html.j2` file. |
| `--image-format` | | `png \| webp` | `png` | Image output format for embedded `drawlib` blocks. |
| `--no-cache` | | flag | `False` | Disable reading and writing the SQLite image build cache (forces clean re-rendering). |

#### Directory Compilation Rules:
When `<INPUT>` is a directory, `drawlib build html` compiles a complete multi-page documentation website:
1. **Mandatory Root Files**:
   - `index.md`: The root landing page of the documentation site.
   - `navbar.md`: The sidebar navigation structure defining categories and links.
2. **Navigation Construction**: The builder parses `navbar.md`, generates hierarchical categories and links, computes relative paths for nested directories, and highlights the current page (`.active`).
3. **Static Asset Synchronization**: Non-markdown files (images, custom stylesheets, font files, data archives) located anywhere within `<INPUT>` are recursively mirrored to `--output` preserving folder hierarchy.
4. **Shared Stylesheet**: An external `style.css` is generated in the root of the output directory and referenced by all pages via relative paths.

#### Examples:
```bash
# Compile entire documentation directory to HTML site:
drawlib build html docs_src/ -o docs_html/ --css google

# Compile single Markdown document to standalone HTML:
drawlib build html docs_src/overview.md -o docs_html/overview.html

# Compile with custom Jinja2 template and global configuration:
drawlib build html docs_src/ -o docs_html/ -c docs_config.py -t custom_template.html.j2

# Force complete re-rendering ignoring cached images:
drawlib build html docs_src/ -o docs_html/ --no-cache
```

---

### 1.2 `drawlib build markdown` (Rendered Markdown for GitHub)

Compiles Markdown source files containing embedded ````drawlib```` blocks into standard GitHub-Flavored Markdown (`.md`). Rendered illustration images are written to a dedicated companion folder (e.g. `<doc_name>_images/`), and code blocks are replaced with syntax-highlighted Python code followed by relative image links.

#### Syntax:
```bash
drawlib build markdown <INPUT> [OPTIONS]
```

#### Arguments:
- `<INPUT>`: Path to input Markdown file (`.md`) or directory containing Markdown files.

#### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<path>` | `<stem>.rendered.md` or directory | Output destination file or directory path. |
| `--config` | `-c` | `<path>` | `None` | Path to Python configuration script executed before blocks. |
| `--image-format` | | `png \| webp` | `png` | Image output format for rendered blocks. |
| `--no-cache` | | flag | `False` | Disable reading and writing the SQLite image build cache. |

#### Overwrite Protection:
To safeguard author source files, `drawlib build markdown` strictly refuses to overwrite source Markdown files in-place (`src_abs == dest_abs`). When compiling a directory, you must specify a separate destination directory (e.g. `-o docs/`). For single files without `-o`, the compiler appends `.rendered.md` by default.

#### Code Visibility in Rendered Markdown:
- `hide-code` *(default)*: Embedded code block is replaced strictly by the relative image reference: `![alt](https://example.com/1.png)`.
- `show-code`: Embedded code block becomes a syntax-highlighted ````python```` block followed by the image reference.
- `fold-code`: The image reference is displayed first, followed by a collapsed `<details><summary>Source Code</summary>...</details>` block containing the Python source.

#### Examples:
```bash
# Compile author source directory to GitHub-ready docs/ directory:
drawlib build markdown docs_src/ -o docs/

# Compile single file using custom configuration:
drawlib build markdown docs_src/architecture.md -o docs/architecture.md -c docs_config.py

# Export images as modern WebP format:
drawlib build markdown docs_src/ -o docs/ --image-format webp
```

---

### 1.3 `drawlib build pdf` (Headless Vector PDF Compilation)

Merges one or more Markdown or HTML documents into a single document and compiles it directly into a high-fidelity vector PDF using local headless Chromium-based browsers.

#### Syntax:
```bash
drawlib build pdf <INPUTS...> [OPTIONS]
```

#### Arguments:
- `<INPUTS...>`: One or more Markdown (`.md`) files, HTML (`.html`) files, or directory paths to merge into the final PDF.

#### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<path>` | `<first_stem>.pdf` | Destination PDF output file path. |
| `--title` | | `<str>` | Extracted from H1 | Overall document title displayed on cover and running headers. |
| `--generate-index` | `--toc` | flag | `False` | Generate a Table of Contents (ToC) and insert it between chapters. |
| `--page-break` | `--no-page-break` | flag | `True` | Insert CSS page breaks (`page-break-before: always`) between chapters. |
| `--css` | | `<name\|path>`| `default` | PDF CSS preset (`default`, `google`, `github`, `minimal`, `monochrome`, etc.) or custom `.css`. |
| `--template` | `-t` | `<name\|path>`| `default` | PDF template preset (`default`, `book`) or custom `.html.j2` file path. |
| `--config` | `-c` | `<path>` | `None` | Path to Python configuration script executed before blocks. |
| `--no-cache` | | flag | `False` | Force clean diagram generation ignoring SQLite cache. |

#### Headless PDF Engine Mechanics:
Drawlib renders PDFs using Playwright and a headless Chromium browser instance (`page.pdf()`). This guarantees identical layout across all operating systems, accurate web font loading, and background CSS rendering.

Prerequisites:
- Install Playwright: `uv add "drawlib[pdf]"` or `pip install "drawlib[pdf]"`
- Download Chromium: `uv run playwright install chromium` or `playwright install chromium`

#### Examples:
```bash
# Compile single document to vector PDF:
drawlib build pdf doc.md -o output.pdf --css google

# Compile multi-chapter book with Table of Contents and cover page:
drawlib build pdf docs_src/00_cover.md docs_src/01_intro.md docs_src/02_arch.md \
  -o architecture_handbook.pdf --toc --css google -t book

# Merge an entire directory of chapters into a single PDF:
drawlib build pdf docs_src/ -o comprehensive_guide.pdf --page-break --toc
```

---

### 1.4 `drawlib build images` / `drawlib build image` (Batch Python Script Execution)

Executes one or more standalone Python drawing scripts (`.py`) or directories containing Python scripts to generate image assets.

#### Syntax:
```bash
drawlib build image <INPUTS...> [OPTIONS]
# Alias:
drawlib build images <INPUTS...> [OPTIONS]
```

#### Arguments:
- `<INPUTS...>`: Python script file paths (`.py`) or directory paths containing Python scripts.

#### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output`, `--output-dir` | `-o` | `<path>` | `None` | Output file path (for single script) or destination directory path. |
| `--format` | `-f` | `png \| webp \| jpg \| pdf` | `None` (uses script setting) | Global output image format override. |
| `--config` | `-c` | `<path>` | `None` | Path to Python setup/configuration script. |
| `--grid` | `-g` | flag | `False` | Save companion `*_grid.<ext>` images with coordinate grid overlaid. |
| `--disable-auto-clear` | | flag | `False` | Disable clearing canvas per executing drawing code files. |
| `--enable-auto-initialize` | | flag | `False` | Enable complete canvas re-initialization per executing code file. |
| `--no-cache` | | flag | `False` | Disable reading and writing the SQLite build image cache. |

#### Directory Hierarchy Preservation:
When pointing `drawlib build image` at a directory containing subdirectories (e.g. `scripts/chapter1/diagram1.py`), specifying an output directory `-o build/images/` mirrors the relative directory structure (`build/images/chapter1/diagram1.png`), preventing namespace collisions.

#### Duplicate Output Collision Detection:
Before executing scripts in batch, Drawlib performs static AST analysis across all target files to inspect `save(...)` calls. If two separate scripts would write to the exact same image file path, the build aborts immediately with a descriptive collision error before modifying disk state.

#### Examples:
```bash
# Execute a single Python drawing script:
drawlib build image my_diagram.py -o out.png

# Execute all Python scripts in a folder and output to an assets directory:
drawlib build images scripts/ -o assets/

# Batch build illustrations with coordinate grid companion images:
drawlib build images scripts/ -o assets/ --grid

# Override output format to WebP across all scripts:
drawlib build images scripts/ -o assets/ -f webp
```

---

## 2. Project Scaffolding (`drawlib init`)

Bootstraps new documentation projects with production-ready file layouts, sample illustrations, navigation configurations, and automated build scripts.

> **Guideline for AI Agents & Developers**: Never craft documentation directory structures manually. Always scaffold projects using `drawlib init` to guarantee structural compliance.

### Syntax:
```bash
drawlib init [TYPE] [DESTINATION] [OPTIONS]
```

### Arguments:
- `[TYPE]`: Starter project template type (`site`, `simple`, `pdf`).
- `[DESTINATION]`: Target directory path (defaults to current working directory).

### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--here` | | flag | `False` | Initialize directly into current directory without creating a subfolder. |
| `--list` | `-l` | flag | `False` | List all available starter project types and their descriptions. |
| `--force` | `-f` | flag | `False` | Overwrite existing files if destination directory is not empty. |

---

### Project Types & Generated Directory Structures

#### 1. `site`: Multi-page Website with Navigation Sidebar
Designed for technical documentation, library user guides, and architecture wikis.
```text
my_site/
├── docs_src/
│   ├── index.md               # [MANDATORY] Root landing page
│   ├── navbar.md              # [MANDATORY] Sidebar categories and links definition
│   ├── architecture/
│   │   └── index.md           # Chapter page with embedded diagrams
│   └── workflow/
│       └── index.md           # Workflow chapter page
├── docs_config.py             # Global canvas settings, themes, and font defaults
├── docs_build.sh              # Executable build script (Markdown + HTML)
└── README_DOCS.md             # Project documentation workflow guide
```

#### 2. `simple`: Single Markdown Document Project
Designed for standalone technical specifications, whitepapers, or README assets.
```text
my_doc/
├── docs_src/
│   └── doc.md                 # Single authoring document
├── docs_config.py             # Global drawing configuration
├── docs_build.sh              # Automation script for Markdown & HTML export
└── README_DOCS.md             # Quickstart guide
```

#### 3. `pdf`: Multi-Chapter Report with Cover & Table of Contents
Designed for formal reports, whitepapers, design documents, and printable manuals.
```text
my_report/
├── docs_src/
│   ├── 00_cover.md            # Cover page (title, author, metadata)
│   ├── 01_overview.md         # Executive overview chapter
│   └── 02_design.md           # Technical design chapter
├── docs_config.py             # Global drawing configuration
├── docs_build.sh              # Headless PDF generation script
└── README_DOCS.md             # Compilation instructions
```

### Scaffolding Examples:
```bash
drawlib init --list                  # List available project types
drawlib init site my_docs/           # Scaffold a multi-page documentation website
drawlib init site --here             # Scaffold a documentation site directly in current repo
drawlib init simple my_doc/ --force  # Force scaffolding in a non-empty directory
drawlib init pdf my_whitepaper/      # Scaffold a multi-chapter PDF report
```

---

## 3. Single Illustration Export (`drawlib export`)

Extracts, compiles, and renders a single illustration from a Markdown file or a standalone Python script directly to an image file.

Designed specifically for:
- **Headless Environments & CI/CD**: Renders illustrations on headless servers without requiring an X11/Wayland display server.
- **AI Coding Agent Rapid Feedback**: Enables coding assistants to verify shape coordinates, colors, and layout in seconds without triggering a full site rebuild.
- **Selective Diagram Extraction**: Rapidly export a single figure for inclusion in slide decks, tickets, or chat conversations.

### Syntax:
```bash
drawlib export <FILE> [TARGET] [OPTIONS]
```

### Arguments:
- `<FILE>`: Path to a Markdown (`.md`), HTML (`.html`), or standalone Python script (`.py`).
- `[TARGET]`: *(Optional for Markdown/HTML)* 1-based block index (e.g. `1`, `2`, `-1`) or target image filename (e.g. `arch.png`). If omitted for Markdown/HTML, Drawlib prints a summary table of all detected blocks.

### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<path>` | `<stem>_export.png` | Destination image file path or output directory path. |
| `--config` | `-c` | `<path>` | `None` | Path to Python configuration script (e.g. `docs_config.py`). |
| `--grid` | `-g` | flag | `False` | Overlay coordinate grid lines, axes, and numeric labels on exported image. |

---

### Discovering Code Blocks in a Document:
If `[TARGET]` is omitted when pointing to a Markdown or HTML document, `drawlib export` scans the file and prints all available illustration blocks without executing them:

```bash
drawlib export docs_src/architecture.md
```

Example Output:
```text
Available drawlib code blocks in 'docs_src/architecture.md':
Index   Line    File Target                  Header Options
-----------------------------------------------------------------
1       L34     architecture_images/1.png    600px center caption:"System Overview"
2       L88     architecture_images/db.png   caption:"Database Schema" file:db.png
3       L145    architecture_images/3.png    show-code
```

---

### Exporting by Index or Image Name:
```bash
# Export block #1 by index:
drawlib export docs_src/architecture.md 1 -o scratch/fig1.png

# Export the last block in the document using negative index:
drawlib export docs_src/architecture.md -1 -o scratch/last_fig.png

# Export block by explicit image filename:
drawlib export docs_src/architecture.md db.png -o scratch/db.png

# Export with coordinate grid overlay for alignment verification:
drawlib export docs_src/architecture.md 1 -g -o scratch/fig1_grid.png

# Export using project configuration (ensuring identical fonts and styling):
drawlib export docs_src/architecture.md 1 -c docs_config.py -o scratch/fig1.png

# Export from a standalone Python script:
drawlib export my_drawing.py -o scratch/my_drawing.png
```

---

## 4. Desktop Visual Preview (`drawlib show`)

Executes and displays an illustration in a native desktop GUI preview window.

### Syntax:
```bash
drawlib show <FILE> [TARGET] [OPTIONS]
```

### Arguments:
- `<FILE>`: Target Markdown (`.md`), HTML (`.html`), or Python script (`.py`).
- `[TARGET]`: Optional 1-based block index or target image filename for Markdown/HTML files.

### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<path>` | `None` | Save output image to file path without opening GUI viewer (headless mode). |
| `--grid` | `-g` | flag | `False` | Display canvas with coordinate grid overlaid. |
| `--config` | `-c` | `<path>` | `None` | Path to Python configuration script (e.g. `docs_config.py`). |

---

### Interactive Desktop Usage:
```bash
# Preview standalone Python script in desktop window:
drawlib show my_drawing.py

# Preview standalone script with coordinate grid overlay:
drawlib show my_drawing.py --grid

# List all blocks in a Markdown file:
drawlib show docs_src/architecture.md

# Preview block #2 in desktop window:
drawlib show docs_src/architecture.md 2

# Preview block with coordinate grid overlay:
drawlib show docs_src/architecture.md 2 -g
```

> **Headless Redirection**: When `-o` / `--output` is provided, `drawlib show` automatically suppresses the GUI window and writes the image directly to disk. This makes `drawlib show file.md 1 -o out.png` functionally equivalent to `drawlib export`.

---

## 5. Local Documentation Server (`drawlib serve`)

Starts a zero-dependency local development HTTP server to preview built HTML documentation websites with automatic browser launching and pre-flight link validation.

### Syntax:
```bash
drawlib serve [DIRECTORY] [OPTIONS]
```

### Arguments:
- `[DIRECTORY]`: Directory path to serve. If omitted, Drawlib auto-detects `docs_html/`, `docs/`, or the current directory in that order.

### Options:
| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--port` | `-p` | `<int>` | `8000` | Port number to bind the HTTP server to. |
| `--no-browser` | | flag | `False` | Do not open default web browser automatically upon startup. |
| `--check`, `--check-only` | | flag | `False` | Check for broken links/missing assets and exit immediately without serving. |
| `--skip-check` | | flag | `False` | Start the server immediately without running pre-flight link checks. |

---

### Pre-Flight Link & Asset Checking:
Before launching the server, `drawlib serve` automatically scans all generated HTML files in the target directory to verify:
1. **Internal Anchor & Page Links**: Ensures every relative `<a href="...">` resolves to an existing `.html` file.
2. **Static Image References**: Confirms every `src` attribute in `<img>` tags resolves to an existing file on disk.

If broken links or missing assets are discovered, Drawlib outputs a diagnostic report indicating the affected file and link target:
```text
[CHECK] Scanning docs_html/ for broken links and missing assets...
[ERROR] docs_html/workflow/index.html: broken link to '../arch/system.html' (file not found)
[ERROR] docs_html/index.html: missing image asset 'index_images/missing_logo.png'
```

---

### Server Usage Examples:
```bash
# Preview default docs_html/ directory on port 8000 (opens browser automatically):
drawlib serve

# Serve custom directory on port 8080 without opening browser:
drawlib serve my_site/ -p 8080 --no-browser

# Run broken link and missing asset check only (ideal for CI/CD gates):
drawlib serve docs_html/ --check

# Launch server immediately bypassing pre-flight checks:
drawlib serve docs_html/ --skip-check
```

---

## 6. Cache Management (`drawlib cache`)

Drawlib manages two distinct caching layers to maximize performance and minimize redundant network transfers and image rendering:
1. **Release Asset Cache**: Locally cached font families and icon sets downloaded from official GitHub Releases.
2. **Diagram Build Cache**: A local SQLite database (`.drawlib_cache/build_cache.sqlite`) storing hashes of illustration code and rendered image binaries.

### Subcommands:
```text
drawlib cache
├── list        List all downloadable font and icon packages and their local cache status
├── clear       Delete all locally cached font and icon files (alias: purge)
└── download    Pre-download font and/or icon packages from GitHub Releases
```

---

### 6.1 `drawlib cache list`
Inspects all available font and icon packages and prints an overview of cached status, file count, and disk space utilization:

```bash
drawlib cache list
```

Example Output:
```text
                       Drawlib Font & Icon Cache                       
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Package                  ┃ Category ┃ Cached ┃    Files ┃  Size (KB) ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ font-roboto              │ font     │  Yes   │      4/4 │     1240.2 │
│ font-source-code-pro     │ font     │  Yes   │      4/4 │      980.5 │
│ icon-phosphor            │ icon     │  Yes   │  124/124 │     3420.1 │
│ icon-fontawesome         │ icon     │  No    │    0/250 │          - │
│ icon-gcp                 │ icon     │  No    │    0/180 │          - │
└──────────────────────────┴━━━━━━━━━━┴━━━━━━━━┴━━━━━━━━━━┴────────────┘
Cached packages: 3/5 (Total local size: 5.64 MB)
```

---

### 6.2 `drawlib cache clear`
Deletes all locally downloaded font and icon files from disk to reclaim storage:

```bash
drawlib cache clear
# Hidden alias:
drawlib cache purge
```

---

### 6.3 `drawlib cache download`
Pre-fetches font and icon asset archives from GitHub Releases. Ideal for provisioning CI/CD build runners or offline development environments:

```bash
drawlib cache download --all       # Pre-download all font and icon packages
drawlib cache download --fonts     # Download font packages only
drawlib cache download --icons     # Download icon packages only
```

---

### 6.4 SQLite Diagram Build Cache & Cache Bypassing
When compiling Markdown documents or batch images, Drawlib computes a SHA-256 hash derived from:
- The exact Python drawing code content.
- The global configuration script hash (if `-c` / `--config` is supplied).
- The requested image output format (`png` or `webp`).

If the computed hash matches an entry in `.drawlib_cache/build_cache.sqlite`, Drawlib restores the cached image directly without executing Python code, speeding up document compilation significantly.

To bypass the build cache and force fresh diagram generation:
```bash
drawlib build html docs_src/ -o docs_html/ --no-cache
drawlib build markdown docs_src/ -o docs/ --no-cache
drawlib build pdf docs_src/ -o out.pdf --no-cache
drawlib build image scripts/ -o assets/ --no-cache
```

To clean the SQLite build cache completely, remove the local cache folder:
```bash
rm -rf .drawlib_cache/
```

---

## 7. HTML & PDF Template Customization (`drawlib template`)

Drawlib uses Jinja2 templates to assemble rendered documentation pages into final HTML and PDF files. The `drawlib template` command group inspects, exports, and validates these templates.

### Subcommands:
```text
drawlib template
├── html
│   ├── list       List available built-in HTML templates (sidebar, simple)
│   ├── export     Export a built-in HTML template to a local file for customization
│   └── validate   Validate a custom Jinja2 HTML template file
└── pdf
    ├── list       List available built-in PDF templates (default, book)
    ├── export     Export a built-in PDF template to a local file for customization
    └── validate   Validate a custom Jinja2 PDF template file
```

---

### 7.1 Listing Built-in Templates:
```bash
drawlib template html list
drawlib template pdf list
```

Built-in Template Presets:
- **HTML**:
  - `sidebar`: Multi-page documentation website template with collapsible navigation sidebar, breadcrumbs, search, and responsive layout.
  - `simple`: Standalone single-page document template without sidebar navigation.
- **PDF**:
  - `default`: Clean report layout with header, footer, and page numbering.
  - `book`: Multi-chapter book template with front matter, cover page styling, and chapter dividers.

---

### 7.2 Exporting Templates for Customization:
```bash
# Export the HTML sidebar template:
drawlib template html export sidebar -o my_template.html.j2

# Export the PDF book template:
drawlib template pdf export book -o my_pdf_template.html.j2
```

---

### 7.3 Validating Custom Templates:
Custom templates must contain mandatory Jinja2 placeholders required by the compiler. Run `validate` to check AST structure and variable conformance:

```bash
drawlib template html validate my_template.html.j2
drawlib template pdf validate my_pdf_template.html.j2
```

Required Placeholders:
- **HTML Templates**: `{{ title }}`, `{{ body_html }}`, `{{ site_title }}`, `{{ nav_sections }}` (for sidebar).
- **PDF Templates**: `{{ title }}`, `{{ body_html }}`.

---

### 7.4 Compiling with Custom Templates:
```bash
# Compile HTML site using custom Jinja2 template:
drawlib build html docs_src/ -o docs_html/ -t my_template.html.j2

# Compile PDF using custom Jinja2 template:
drawlib build pdf docs_src/ -o output.pdf -t my_pdf_template.html.j2
```

---

## 8. CSS Stylesheet Presets & Theming (`drawlib css`)

Drawlib includes professionally designed CSS presets for HTML documentation and headless PDF printing.

### Subcommands:
```text
drawlib css
├── html
│   ├── list       List available built-in HTML CSS presets
│   └── export     Export a built-in HTML CSS preset to a local file
└── pdf
    ├── list       List available built-in PDF CSS presets
    └── export     Export a built-in PDF CSS preset to a local file
```

---

### 8.1 Available CSS Themes:

| Theme Preset | HTML Support | PDF Support | Description |
| :--- | :---: | :---: | :--- |
| `default` | Yes | Yes | Clean modern typography, neutral borders, light background. |
| `default-dark`| Yes | Yes | Inverted dark palette for dark-mode documentation and printable pages. |
| `default-auto`| Yes | No | Automatic light/dark switching responding to `@media (prefers-color-scheme)`. |
| `google` | Yes | Yes | Material-inspired styling, Roboto typography, Google blue accents. |
| `google-dark` | Yes | Yes | Dark theme variant with Material palette. |
| `google-auto` | Yes | No | Google theme with automatic system color scheme switching. |
| `github` | Yes | Yes | GitHub Markdown style, monospace code fonts, standard alert boxes. |
| `minimal` | Yes | Yes | Unadorned typography, high density, minimal padding. |
| `monochrome` | Yes | Yes | High-contrast grayscale aesthetic. |

---

### 8.2 Listing and Exporting Presets:
```bash
# List all HTML CSS presets:
drawlib css html list

# Export Google preset to local style.css:
drawlib css html export google -o custom_style.css

# List all PDF CSS presets:
drawlib css pdf list

# Export PDF preset to local pdf_style.css:
drawlib css pdf export default -o custom_pdf.css
```

---

### 8.3 Compiling with Custom CSS:
```bash
# Compile HTML site using custom CSS:
drawlib build html docs_src/ -o docs_html/ --css custom_style.css

# Compile PDF using custom CSS:
drawlib build pdf docs_src/ -o output.pdf --css custom_pdf.css
```

---

## 9. AI Agent Guidelines & Rule Topics (`drawlib rules`)

Drawlib features a built-in knowledge subsystem (`drawlib rules`) that delivers detailed coding standards, shape rules, coordinate conventions, and syntax examples directly to your terminal.

AI pair-programming assistants and developers can query these rules at any time during development to ensure API consistency.

### Subcommands:
```text
drawlib rules
├── list                    List all available rule topics and cache status
├── show [TOPIC]            Display rules and examples (on-demand illustration build)
│   ├── --rebuild, -r       Force regenerate illustrations even if cached
│   └── --raw               Display raw Markdown without building or checking cache
├── build [TOPIC]           Pre-build illustrations into _assets/rules/
│   ├── --all, -a           Compile illustrations for all topics
│   └── --force, -f         Force recompile even if up-to-date
└── clean                   Delete all cached rule documents and generated images
```

---

### 9.1 Rule Topic Catalog:

| Topic Name | Aliases | Description |
| :--- | :--- | :--- |
| `overview` | *(default)* | Canvas lifecycle, coordinate systems, core imports, and workflow. |
| `cli` | | Complete CLI reference manual, options, and CI/CD automation. |
| `docs_build` | `doc`, `docs`, `doc_build` | Documentation site layout, `navbar.md` rules, and build scripts. |
| `shapes` | | Rectangles, circles, ellipses, wedges, and polygons. |
| `lines` | | Straight, curved, and chained lines with arrowheads. |
| `text` | | Text rendering, alignment, fonts, and multiline formatting. |
| `icons` | | Phosphor, FontAwesome, and GCP cloud architecture icons. |
| `preset_styles` | `theme`, `themes` | Pre-defined style naming rules and color palette classes. |
| `smartarts` | | Tables, trees, mindmaps, and structured visual elements. |
| `charts` | | Bar, line, pie, scatter, radar, area, and Gantt charts. |
| `diagrams` | | Flowcharts, sequence, state, class, ER, and architecture diagrams. |

---

### 9.2 On-Demand Multimodal Illustration Pairing:
When an AI agent or developer runs `drawlib rules show <topic>`, Drawlib automatically checks if the rendered document and its companion illustration images are cached under `drawlib/_assets/rules/`.
- **First Call**: If not cached or if source rules were modified, Drawlib compiles code blocks on demand, generates companion PNG illustrations, and injects an agent instruction banner with local image paths.
- **Subsequent Calls**: Instant retrieval directly from local cache.
- **Multimodal Grounding**: AI coding assistants can view the companion images using their file viewing tools (`view_file`, etc.) to visually verify geometric layouts, alignments, and aesthetics alongside the Python source code.
- **PyPI Safety**: All cached rule assets reside inside `_assets/rules/` which is ignored by Git and automatically purged before package publishing, keeping wheel distributions minimal.

### 9.3 Usage Examples:
```bash
drawlib rules list                        # List all topics and cache status
drawlib rules show overview               # Display canvas overview and core rules
drawlib rules show shapes                 # Display shapes API rules (builds on-demand)
drawlib rules show shapes --rebuild       # Force regenerate illustrations for shapes
drawlib rules show shapes --raw           # Output raw Markdown source without cache
drawlib rules build --all                 # Pre-build illustrations for all topics
drawlib rules clean                       # Delete all cached illustrations and docs
```

---

## 10. CI/CD & Automation Integration

Integrating Drawlib into continuous integration workflows guarantees documentation is consistently validated, diagrams are automatically rendered, and broken links are caught prior to deployment.

---

### 10.1 GitHub Actions Workflow (`.github/workflows/docs.yml`)

The following complete workflow builds HTML documentation, validates links, and deploys the static site to GitHub Pages:

```yaml
name: Documentation Build & Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-verify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install uv package manager
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: Set up Python 3.12
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --frozen

      - name: Pre-download font and icon assets
        run: uv run python -m drawlib cache download --all

      - name: Build documentation site
        run: |
          uv run python -m drawlib build html docs_src/ -o docs_html/ --css google
          uv run python -m drawlib build markdown docs_src/ -o docs/

      - name: Run pre-flight link and asset validation
        run: uv run python -m drawlib serve docs_html/ --check

      - name: Upload GitHub Pages artifact
        if: github.ref == 'refs/heads/main'
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs_html/

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: build-and-verify
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

### 10.2 Makefile Integration

Add the following targets to your project's `Makefile` for streamlined local development:

```makefile
.PHONY: docs-build docs-serve docs-check docs-clean

DOCS_SRC := docs_src
DOCS_HTML := docs_html
DOCS_MD := docs
CONFIG := docs_config.py

docs-build:
	@echo "==> Compiling Drawlib documentation..."
	uv run python -m drawlib build html $(DOCS_SRC) -o $(DOCS_HTML) -c $(CONFIG) --css google
	uv run python -m drawlib build markdown $(DOCS_SRC) -o $(DOCS_MD) -c $(CONFIG)

docs-serve:
	@echo "==> Starting local documentation server..."
	uv run python -m drawlib serve $(DOCS_HTML)

docs-check:
	@echo "==> Verifying internal links and assets..."
	uv run python -m drawlib serve $(DOCS_HTML) --check

docs-clean:
	@echo "==> Cleaning generated documentation and cache..."
	rm -rf $(DOCS_HTML) $(DOCS_MD) .drawlib_cache/
```

---

### 10.3 Pre-commit Hook Integration (`.pre-commit-config.yaml`)

Enforce documentation integrity and prevent broken links from entering the repository:

```yaml
repos:
  - repo: local
    hooks:
      - id: drawlib-docs-check
        name: Check Drawlib Documentation Links
        entry: uv run python -m drawlib serve docs_html/ --check
        language: system
        pass_filenames: false
        files: ^docs_src/
```

---

## 11. Troubleshooting & Diagnostics Reference

### Common Error Messages & Solutions:

#### 1. `Directory build requires "index.md" at the root of the input directory`
- **Cause**: Running `drawlib build html` on a directory that does not have an `index.md` file at its top level.
- **Fix**: Create `docs_src/index.md` as the root landing page or scaffold the directory with `drawlib init site --here`.

#### 2. `Directory build requires "navbar.md" at the root of the input directory`
- **Cause**: Multi-page website builds require `navbar.md` in the root of the input directory to construct sidebar navigation.
- **Fix**: Add `docs_src/navbar.md` defining categories and links. Refer to `drawlib rules show docs_build` for navbar syntax.

#### 3. `Refusing to overwrite input source file "..."`
- **Cause**: The output path `-o` points to the exact same file or directory as the input source.
- **Fix**: Specify a distinct destination path (e.g. `drawlib build markdown docs_src/ -o docs/`).

#### 4. `Broken links / missing assets detected`
- **Cause**: `drawlib serve --check` detected `<a href="...">` or `<img src="...">` paths that do not exist on disk.
- **Fix**: Review the terminal error log for the exact file and line number. Verify relative paths and filename spelling.

#### 5. Playwright or Chromium Not Found for PDF Build
- **Cause**: `drawlib build pdf` requires Playwright and a downloaded headless Chromium binary.
- **Fix**: Install `drawlib[pdf]` (`uv add "drawlib[pdf]"` or `pip install "drawlib[pdf]"`) and download Chromium (`uv run playwright install chromium` or `playwright install chromium`).

#### 6. Duplicate Image Output Collision
- **Cause**: Two standalone Python scripts in batch mode or two embedded Markdown blocks write to the exact same output image filename.
- **Fix**: Specify explicit unique filenames in block headers (e.g. `file:auth_flow.png`) or rename target scripts.

---

### CLI Exit Codes:

| Exit Code | Meaning | Common Causes |
| :---: | :--- | :--- |
| `0` | Success | Command completed execution normally without errors. |
| `1` | Build / Execution Error | Missing required files (`index.md`, `navbar.md`), code execution failure, broken links on `--check`. |
| `2` | Bad Parameter / Syntax Error | Invalid option combination (e.g. `--quiet` with `--verbose`), unknown subcommand or missing required arguments. |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
