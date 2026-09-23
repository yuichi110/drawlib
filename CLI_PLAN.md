# Architecture & Implementation Plan: Drawlib CLI & Document Builder Modernization (`CLI_PLAN.md`)

## 1. Overview & Goals
- **Purpose**: Modernize the `drawlib` command-line interface (CLI) using **Typer (`typer`)** and **Rich (`rich`)**, restructure `drawlib build` into explicit format-specific subcommands (`markdown`, `html`, `pdf`), and establish a unified document input detection and processing pipeline in `drawlib._tools.doc_builder`.
- **Key Design Principles**:
  - **Rich & Discoverable CLI (Typer + Rich)**: Replace manual `sys.argv` slicing and fragmented `argparse` instances with a declarative, type-safe Typer CLI application that renders colorized, structured help panels (`Commands`, `Arguments`, `Options`).
  - **Format-Specific `build` Subcommands**: Separate `drawlib build` into `drawlib build markdown`, `drawlib build html`, and `drawlib build pdf` so each target exposes only relevant arguments and follows its natural input-to-output cardinality:
    - `markdown` / `html`: **1-to-1 / Tree-Preserving** compilation with cross-file navigation and links.
    - `pdf`: **N-to-1 / Ordered Merging (Book/Chapter Bundling)** that combines multiple input files/directories into a single merged HTML document before rendering to PDF via Headless Chromium.
  - **Unified Document Type Detection**: Automatically classify any input document into one of 4 canonical types (`markdown_drawlib`, `markdown`, `html_drawlib`, `html`) to avoid unnecessary rendering overhead and ensure consistent behavior across `build`, `show`, and `export`.
  - **Standardized HTML Drawlib Syntax**: Standardize HTML embedded drawing blocks on `<script type="text/drawlib" ...>...</script>` (valid HTML5 raw text element that prevents `<` / `>` operator corruption by HTML parsers/formatters).

---

## 2. Target Architecture & Module Layout

```text
src/drawlib/
├── _tools/                            # [Private Implementation Layer]
│   ├── cli/
│   │   ├── __init__.py                # Exports call_command() / app
│   │   ├── main.py                    # Entrypoint (drawlib = "drawlib._tools.cli.main:main")
│   │   ├── _app.py                    # Main Typer app and global options (-v, logging flags)
│   │   ├── _build.py                  # `drawlib build {image, markdown, html, pdf}` sub-app
│   │   └── _commands.py               # `cache`, `serve`, `template`, `css`, `show`, `export` commands
│   │
│   ├── image_builder.py               # Implementation of `build_image()` & `DrawlibExecuter`
│   ├── cache_manager.py               # Implementation of `clear_cache()`, `list_cache()`, `download_cache()`
│   ├── http_server.py                 # Implementation of `serve_docs()` (`run_server`)
│   │
│   └── doc_builder/
│       ├── __init__.py                # Core implementations: build_markdown(), build_html(), build_pdf()
│       ├── detector.py                # [New] Unified input classifier (DocumentInputInfo, DocType)
│       ├── merger.py                  # [New] Multi-document HTML merger for `build pdf`
│       ├── processor.py               # DrawlibBlockProcessor (```drawlib & <script type="text/drawlib">)
│       ├── parser_md.py               # Markdown AST to HTML converter & link rewriter
│       ├── exporter_md.py             # Rendered Markdown output writer
│       ├── exporter_html.py           # Jinja2 HTML renderer (standalone, sidebar, & in-place HTML)
│       ├── exporter_pdf.py            # Headless Chromium PDF printer
│       └── template.py                # Jinja2 template & CSS preset listing, export, and validation
│
└── tools/                             # [Public Facade Layer — Pure re-exports (`__all__`), no implementation]
    ├── __init__.py                    # Re-exports submodules (build, cache, css, template, serve, show, export)
    ├── build/
    │   ├── __init__.py                # Re-exports build_image, build_markdown, build_html, build_pdf
    │   ├── image.py                   # Re-exports `build_image` from `drawlib._tools.image_builder`
    │   ├── markdown.py                # Re-exports `build_markdown` from `drawlib._tools.doc_builder`
    │   ├── html.py                    # Re-exports `build_html` from `drawlib._tools.doc_builder`
    │   └── pdf.py                     # Re-exports `build_pdf` from `drawlib._tools.doc_builder`
    ├── cache.py                       # Re-exports `clear_cache`, `list_cache`, `download_cache`
    ├── css.py                         # Re-exports `list_css`, `export_css`
    ├── template.py                    # Re-exports `list_templates`, `export_template`, `validate_template`
    ├── serve.py                       # Re-exports `serve_docs`
    ├── show.py                        # Re-exports `show_block` (`show_code_block`)
    └── export.py                      # Re-exports `export_block` (`export_code_block`)
```

---

## 3. Unified Document Input Detection (`doc_builder/detector.py`)

### 3.1. Canonical Document Types (`DocType`)
Every input file passed to `build`, `show`, or `export` is inspected via `detect_document_type(file_path, content)` and classified into:

| `DocType` | File Extension | Content Condition | Additional Metadata |
| :--- | :--- | :--- | :--- |
| **`markdown_drawlib`** | `.md`, `.markdown` | Contains ```` ```drawlib ```` code fence | `block_count > 0` |
| **`markdown`** | `.md`, `.markdown` | No ```` ```drawlib ```` code fence | Skips `DrawlibBlockProcessor` / Matplotlib init |
| **`html_drawlib`** | `.html`, `.htm` | Contains `<script type="text/drawlib"...>` | `is_full_html: bool` (`<!DOCTYPE html>` or `<html`) |
| **`html`** | `.html`, `.htm` | No `<script type="text/drawlib"...>` | `is_full_html: bool`, skips `DrawlibBlockProcessor` |

### 3.2. Standardized Drawlib Block Syntax
1. **Markdown (`markdown_drawlib`)**:
   ````markdown
   ```drawlib width=500px align=center caption="System Overview" file=arch.png
   config(width=100, height=100)
   circle((50, 50), radius=30)
   ```
   ````
2. **HTML (`html_drawlib`)**:
   ```html
   <script type="text/drawlib" width="500px" align="center" caption="システム構成図" file="arch.png">
   config(width=100, height=100)
   circle((50, 50), radius=30)
   </script>
   ```
   *(Note: Legacy `<drawlib>` tags are retired in favor of `<script type="text/drawlib">`.)*

3. **Supported Block Attributes & Output Image Naming (`file` option)**:
   Both Markdown code fences and HTML `<script type="text/drawlib">` tags support the same options (`file`, `width`, `height`, `align`, `caption`, `class`, `format`):
   - **Omitted (`file` not specified)**: Defaults to `{doc_base_name}_images/{block_index}.{ext}` (e.g., `index_images/1.png`).
   - **Filename only (`file="arch.png"` or `file="arch"`)**: Saved under the document's image directory as `{doc_base_name}_images/arch.png` (automatically appending `.{ext}` if no extension is given).
   - **Relative path with directory (`file="assets/arch.png"` or `file="./arch.png"`)**: Saved directly to the specified path relative to the output document directory (`assets/arch.png`) and referenced as `<img src="assets/arch.png" ... />`.
   - **Target Selection in CLI**: The specified `file` name can also be used as the `[target]` selector in `drawlib show page.html arch.png` and `drawlib export page.html arch.png`.

### 3.3. Processing Matrix Across Commands

| Input `DocType` | `drawlib build markdown` | `drawlib build html` | `drawlib build pdf` | `drawlib show` / `export` |
| :--- | :--- | :--- | :--- | :--- |
| **`markdown_drawlib`** | Execute blocks → save images → output standard `.md` | Execute blocks → save/embed images → convert to `.html` with template | Execute blocks → convert to HTML chapter → merge into combined HTML → PDF | List, preview, or export target `drawlib` block |
| **`markdown`** | Copy `.md` directly (fast path, no canvas init) | Convert `.md` directly to `.html` with template (fast path) | Convert `.md` to HTML chapter → merge into combined HTML → PDF | Inform user no `drawlib` blocks exist |
| **`html_drawlib`** | Skip (or warn if single file) | Execute `<script type="text/drawlib">` → replace with `<figure>/<img>`. If `is_full_html` & no `-t`, replace in-place without double `<html>` wrapping | Execute `<script type="text/drawlib">` → extract `<body>` content → merge into combined HTML → PDF | List, preview, or export target `<script type="text/drawlib">` block |
| **`html`** | Skip (or warn if single file) | Copy `.html` directly (or wrap in template if fragment / `-t` specified) | Extract `<body>` content → merge into combined HTML → PDF (or print directly if single full HTML) | Inform user no `drawlib` blocks exist |

---

## 4. CLI Command Hierarchy & Specifications (Typer + Rich)

### 4.1. Dependencies (`pyproject.toml`)
Move `typer>=0.12.0` and `rich>=13.0.0` from `[dependency-groups] dev` to `[project] dependencies` so end-users have full Rich CLI rendering out of the box.

### 4.2. Top-Level CLI (`drawlib -h`)
```bash
drawlib [GLOBAL_OPTIONS] COMMAND [ARGS]...
```
- **Global Options**:
  - `-v`, `--version`: Display `drawlib` version and exit.
  - `--quiet` / `--verbose` / `--debug` / `--developer`: Configure global logging and error handling mode across **all** subcommands.

---

### 4.3. `drawlib build` Subcommand Group (`image`, `markdown`, `html`, `pdf`)

#### 1) `drawlib build image`
Executes one or more Python drawing scripts (`.py`) or package directories to generate illustration image files.
```bash
drawlib build image <inputs...> [-o OUTPUT] [-f {png,webp,jpg,pdf}] [-c CONFIG] [-g] [--disable-auto-clear] [--enable-auto-initialize]
```
- `inputs...`: One or more target Python file(s) (e.g. `a.py`) or directories containing Python drawing code.
- `-o`, `--output`: Output image file path (for a single `.py` script) or output directory path (for multiple scripts / directory).
- `-f`, `--format`: Output image format (`png` [default], `webp`, `jpg`, `pdf`). Overrides default output format when saving canvas.
- `-c`, `--config`: Optional Python setup/config script (`config.py`) executed prior to each script.
- `-g`, `--grid`: Save companion `*_grid.<ext>` images with coordinate grid overlaid in addition to normal images.
- `--disable-auto-clear`: Disable clearing canvas between executing drawing code files.
- `--enable-auto-initialize`: Enable full canvas re-initialization (`initialize()`) before each drawing code file.

#### 2) `drawlib build markdown`
Compiles a Markdown file or directory containing `drawlib` blocks into standard Markdown with rendered image files (ideal for GitHub browsing).
```bash
drawlib build markdown <input> [-o OUTPUT] [--image-format {png,webp}] [-c CONFIG]
```
- `input`: Input Markdown file (`.md`) or directory path.
- `-o`, `--output`: Output file or directory path.
- `--image-format`: `png` (default) or `webp`.
- `-c`, `--config`: Optional Python setup/config script (`config.py`).

#### 3) `drawlib build html`
Compiles a Markdown/HTML file or directory into a responsive static HTML page or multi-page website (always outputs an external `style.css` file alongside the generated HTML and images).
```bash
drawlib build html <input> [-o OUTPUT] [--image-format {png,webp}] [--css CSS] [-t TEMPLATE] [-c CONFIG]
```
- `input`: Input Markdown (`.md`), HTML (`.html`), or directory path.
- `-o`, `--output`: Output file or directory path.
- `--image-format`: `png` (default) or `webp`.
- `--css`: Preset name (`default`, `github`, `monochrome`, `minimal`) or custom `.css` file path (written to `style.css` in the output directory).
- `-t`, `--template`: Template preset (`simple`, `sidebar`) or custom `.html.j2` path.
- `-c`, `--config`: Optional Python setup/config script (`config.py`).

#### 4) `drawlib build pdf`
Combines one or more Markdown/HTML files or directories in the specified order into a single merged HTML document, then renders it to a PDF file via Headless Chromium.
```bash
drawlib build pdf <inputs...> [-o OUTPUT] [--page-break / --no-page-break] [--toc / --no-toc] [--title TITLE] [--css CSS] [-t TEMPLATE] [-c CONFIG]
```
- `inputs...`: **One or more** input files (`.md`, `.html`) or directories, merged in the exact order specified. (Directories are expanded in sorted file order, placing `index.md` first).
- `-o`, `--output`: Output PDF file path (default: `<first_input_stem>.pdf` or `document.pdf`).
- `--page-break / --no-page-break`: Insert CSS page breaks (`page-break-before: always`) between merged files/chapters (default: `--page-break`).
- `--toc / --no-toc`: Generate a Table of Contents at the beginning of the merged document from chapter headings (default: `--no-toc`).
- `--title`: Document title for the merged HTML/PDF (default: extracted from the first input's H1 heading).
- `--css`, `-t / --template`, `-c / --config`: Styling, template, and Python configuration options.

---

### 4.4. Other Top-Level Subcommands

- **`drawlib cache {clear, list, download}`**:
  - `drawlib cache clear` (alias `purge`): Delete downloaded font and icon cache files (`purge_font_cache()`).
  - `drawlib cache list`: Display cached font and icon packages and local disk usage in a Rich table.
  - `drawlib cache download [--all | --fonts | --icons]`: Pre-download font/icon assets (`download_all_assets()`, `download_all_fonts()`, `download_all_icons()`) for offline or container environments.
- **`drawlib serve [directory]`**:
  - Options: `-p / --port` (default `8000`), `--no-browser`, `--skip-check`, `--check / --check-only`.
- **`drawlib template {list, export, validate}`**:
  - `drawlib template list`: Display available built-in HTML templates (`sidebar`, `simple`) and their descriptions in a Rich table.
  - `drawlib template export [name] [-o OUTPUT]`: Export a built-in HTML template (`sidebar` [default] or `simple`) to a file (default: `template.html.j2`).
  - `drawlib template validate <template_file>`: Validate a custom Jinja2 template for syntax and required placeholders.
- **`drawlib css {list, export}`**:
  - `drawlib css list`: Display available built-in CSS presets (`default`, `github`, `minimal`, `monochrome`) and their descriptions in a Rich table.
  - `drawlib css export [name] [-o OUTPUT]`: Export a built-in CSS preset (`default` [default], `github`, `minimal`, or `monochrome`) to a file (default: `style.css`) for customization.
- **`drawlib show <file> [target]`**:
  - Supports `.py`, `markdown_drawlib` (`.md`), and `html_drawlib` (`.html`).
  - Options: `-o / --output`, `-g / --grid`, `-c / --config`.
- **`drawlib export <file> [target]`**:
  - Supports `.py`, `markdown_drawlib` (`.md`), and `html_drawlib` (`.html`).
  - Options: `-o / --output`, `-g / --grid`, `-c / --config`.

---

## 5. Public Python API Facade (`drawlib.tools`)

All CLI functionality is implemented in `src/drawlib/_tools/` and exposed publicly via pure re-export facade modules under `src/drawlib/tools/` (matching the `_diagrams` / `diagrams` architectural pattern).

### 5.1. Supported Import Styles
```python
# 1. Exact CLI Hierarchy Match
from drawlib.tools.build.image import build_image
from drawlib.tools.build.markdown import build_markdown
from drawlib.tools.build.html import build_html
from drawlib.tools.build.pdf import build_pdf
from drawlib.tools.cache import clear_cache, list_cache, download_cache
from drawlib.tools.template import list_templates, export_template, validate_template
from drawlib.tools.css import list_css, export_css
from drawlib.tools.serve import serve_docs
from drawlib.tools.show import show_block
from drawlib.tools.export import export_block

# 2. Group-Level Shortcut Import
from drawlib.tools.build import build_image, build_markdown, build_html, build_pdf

# 3. Module Dot-Notation (mirrors CLI subcommands)
from drawlib.tools import build, cache, template, css
build.markdown("docs_src/", output="docs/")
build.html("docs_src/", output="docs_html/", css="github")
build.pdf(["intro.md", "chap1.md"], output="book.pdf", toc=True)
```

---

## 6. Step-by-Step Implementation Plan

1. **Phase 1: Document Detector & HTML `<script type="text/drawlib">` Unification**
   - Create `src/drawlib/_tools/doc_builder/detector.py` implementing `DocType`, `DocumentInputInfo`, and `detect_document_type()`.
   - Update `DrawlibBlockProcessor` and `extract_code_blocks()` in `processor.py` to standardize HTML block parsing on `<script type="text/drawlib">`, support the `file` option in HTML blocks, drop `svg`/`inline_svg`, and support `webp`.
2. **Phase 2: Core Tool Implementations (`_tools/`)**
   - Create `src/drawlib/_tools/doc_builder/merger.py` for multi-input merging (`<section class="pdf-chapter">`), cross-file link rewriting (`other.md` → `#chapter-other`), relative static image resolution, and optional TOC generation.
   - Implement `build_markdown()`, `build_html()`, and `build_pdf()` in `src/drawlib/_tools/doc_builder/__init__.py`, plus `list_templates()`, `export_template()`, `list_css()`, and `export_css()` in `template.py`.
   - Implement `build_image()` in `src/drawlib/_tools/image_builder.py` and `clear_cache()`, `list_cache()`, `download_cache()` in `src/drawlib/_tools/cache_manager.py`.
3. **Phase 3: Public Facade (`src/drawlib/tools/`) & Typer CLI (`src/drawlib/_tools/cli/`)**
   - Create pure re-export facade modules under `src/drawlib/tools/` and register `tools` in `src/drawlib/__init__.py`.
   - Update `pyproject.toml` to include `typer>=0.12.0` and `rich>=13.0.0` in `[project] dependencies`.
   - Implement the Typer CLI hierarchy (`build {image, markdown, html, pdf}`, `cache {clear, list, download}`, `serve`, `template {list, export, validate}`, `css {list, export}`, `show`, `export`, plus global options).
4. **Phase 4: Scripts, Documentation & Test Suite Verification**
   - Update `tools/scripts/build_docs.py` and `tools/dcli/docs.py` to use `drawlib.tools.build`.
   - Update and expand unit/integration tests in `tests/doc_builder/` and `tests/cli/`.
   - Run `./dcli check all` and `./dcli test target tests/doc_builder/ tests/cli/` to verify 100% compliance.
