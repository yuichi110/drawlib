# Drawlib Tools Guidelines

`drawlib.tools` is the programmatic Python developer API powering the Drawlib CLI.  
While `drawlib` CLI commands (`drawlib build`, `drawlib show`, etc.) are designed for terminal execution, `drawlib.tools` provides direct Python function interfaces to embed document compilation, diagram export, template validation, and cache management into custom automation scripts, CI/CD pipelines, and testing suites.

---

## 1. Imports & Core Architecture

All public developer and build tools are imported directly from `drawlib.tools`:

```python
from drawlib.tools import (
    # Document, Slide, & Image Compilation
    build_document,
    build_docx,
    build_html,
    build_image,
    build_markdown,
    build_pdf,
    build_pptx,
    build_slide,
    detect_document_type,
    export_code_block,
    show_code_block,
    # Project Scaffolding, Local Server, Cache, & CSS Presets
    init_project,
    list_project_types,
    serve_docs,
    scan_broken_links,
    list_cache,
    clear_cache,
    download_cache,
    list_css,
    export_css,
    get_css,
)
```

---

## 2. Document, Slide & Image Compilation

The compilation tools compile Markdown documents, multi-page document sites, presentation slides, MS Word/PowerPoint Office files, and standalone Python illustration scripts into production outputs.

### 2.1. HTML Build (`build_html`)
Compiles a single Markdown file or a documentation source directory (`docs_src/`) into responsive HTML pages with navigation and styling:

```python
from drawlib.tools import build_html

build_html(
    input_path="docs_src/",
    output="docs_html/",
    styles="styles.py",  # Optional Python styles script
    utils="utils.py",  # Optional Python utils script
    css_mode="external",  # "external" (default) or "embed"
    no_cache=False,  # Force re-rendering all code blocks
    image_format="png",  # "png" or "webp"
)
```

### 2.2. Markdown Build (`build_markdown`)
Compiles Markdown documents for GitHub repository browsing. ````drawlib```` code blocks are replaced with syntax-highlighted Python code followed by relative image links:

```python
from drawlib.tools import build_markdown

build_markdown(
    input_path="docs_src/",
    output="docs/",
    styles="styles.py",
    utils="utils.py",
    image_format="png",
)
```

### 2.3. PDF Build (`build_pdf`)
Compiles documents or slide decks directly to print-ready vector PDF using headless Chromium via Playwright (`playwright` is a standard dependency, and `chromium-headless-shell` downloads automatically on first `build_pdf` or `build_pptx` run):

```python
from drawlib.tools import build_pdf

build_pdf(
    inputs="docs_src/index.md",
    output="output.pdf",
    styles="styles.py",
    utils="utils.py",
)
```

*(Note: In minimal Linux containers such as `python:3.12-slim` lacking OS shared libraries like `libnss3` or `libgbm1`, run `playwright install-deps chromium` or `playwright install --with-deps --only-shell chromium`.)*

### 2.4. MS Word Build (`build_docx`)
Compiles a linear document directory (`doc_src/`) or a single Markdown file (`.md`) into a native editable Microsoft Word (`.docx`) document (`python-docx`). Outputs native editable Word headings, prose, lists, tables, blockquotes, and syntax-highlighted code blocks, with ````drawlib```` diagrams embedded as high-DPI static PNGs (default `dpi=200`):

```python
from drawlib.tools import build_docx

output_docx = build_docx(
    input_path="doc_src/",       # Or pass keyword input_dir="doc_src/"
    output_file="manual.docx",
    title=None,
    page_break=True,
    generate_index=False,
    dpi=200,
    styles_path="doc_src/styles.py",
    utils_path="doc_src/utils.py",
    no_cache=False,
    timestamp=False,
)
```

### 2.5. HTML Slide Deck & MS PowerPoint Build (`build_slide` & `build_pptx`)
Compiles a slide deck directory (`slide_src/`) into an interactive 16:9 HTML presentation (`build_slide`) or measures the `1920x1080` slide DOM via headless Chromium to write native editable 16:9 (`960x540 pt`) Microsoft PowerPoint slides (`build_pptx`, embedding `::: block` cards with `rgba` alpha, text boxes, bullet/numbered lists, tables, code blocks, `::: note` speaker notes, and high-DPI static PNG diagrams):

```python
from drawlib.tools import build_pptx, build_slide

build_slide(
    input_dir="slide_src/",
    output_dir="slide_html/",
    styles_path="slide_src/styles.py",
    utils_path="slide_src/utils.py",
)

output_pptx = build_pptx(
    input_dir="slide_src/",
    output_file="deck.pptx",
    title=None,
    theme=None,
    dpi=240,
    anim_frame="last",  # "first" or "last" for animated blocks
    styles_path="slide_src/styles.py",
    utils_path="slide_src/utils.py",
    no_cache=False,
    timestamp=False,
)
```

### 2.6. Python Image Batch Build (`build_image`)
Executes standalone Python drawing scripts in batch mode:

```python
from drawlib.tools import build_image

build_image(
    inputs="drawings/",
    output="dist/images/",
    styles="styles.py",
    utils="utils.py",
    grid=False,
)
```

---

## 3. Diagram Export & Preview (`export` & `show`)

### 3.1. `export_code_block` (Single Diagram Extraction)
Extracts and renders a single ````drawlib```` illustration from a Markdown file or a standalone `.py` script without opening a GUI display:

```python
from drawlib.tools import export_code_block

# Export block 1 from a Markdown document:
export_code_block(
    file_path="docs_src/architecture.md",
    target="1",  # 1-based index or target filename (e.g. "arch.png")
    output_path=".drawlib/scratch/arch.png",
    grid=True,  # Overlay coordinate grid lines (-g)
    styles_path="styles.py",
    utils_path="utils.py",
)

# Export directly from a standalone Python script:
export_code_block(
    file_path=".drawlib/scratch/my_diagram.py",
    output_path=".drawlib/scratch/output.png",
    grid=False,
)
```

### 3.2. `show_code_block` (Desktop GUI Preview)
Displays the rendered illustration in a local GUI window for interactive alignment:

```python
from drawlib.tools import show_code_block

show_code_block(
    file_path="docs_src/architecture.md",
    target="1",
    grid=True,
    styles_path="styles.py",
    utils_path="utils.py",
)
```

---

## 4. Project Scaffolding

Automates initial project creation with pre-configured directories, sample Markdown files, and build scripts:

```python
from drawlib.tools import init_project, list_project_types

# Inspect available starter templates:
types = list_project_types()
# Returns: {"site": "Multi-page documentation...", "doc": "...", "slide": "...", "images": "..."}

# Scaffold a multi-page documentation website:
init_project(
    project_type="site",
    target="docs",
    destination=".",
    style="default",
    force=False,
)
```

---

## 5. Local Server & Asset Management

### 5.1. Local HTTP Server (`serve_docs`)
Runs a local development web server to preview generated HTML sites:

```python
from drawlib.tools import serve_docs

serve_docs(
    directory="docs_html/",
    port=8000,
    open_browser=True,
    skip_check=False,
    check_only=False,
)
```

### 5.2. Cache Management
Inspect and manage cached font, icon, map, and headless Chromium assets (`download_cache(all_assets=True, fonts=False, icons=False, maps=False, browser=False)`):

```python
from drawlib.tools import clear_cache, download_cache, list_cache

# List cached font families, icons, and maps:
cached_items = list_cache()

# Pre-download all fonts, icons, maps, and headless Chromium for offline/CI use:
download_cache(all_assets=True)

# Pre-download headless Chromium only:
download_cache(all_assets=False, browser=True)

# Purge cache to reclaim disk space:
clear_cache()
```

### 5.3. CSS Presets
Inspect available CSS themes and export stylesheets:

```python
from drawlib.tools import export_css, list_css

# List CSS style presets:
html_presets = list_css(target="html")  # [{"name": "google", "description": ...}, ...]
pdf_presets = list_css(target="pdf")  # [{"name": "default", ...}, ...]

# Export a preset CSS stylesheet:
export_css(name="google", output_path="style.css", target="html", force=True)
```

---

## 6. Practical Code Examples

### 6.1. Custom CI/CD Build & Verification Automation Script

```python
from pathlib import Path
from drawlib.tools import build_html, build_markdown, export_code_block


def run_documentation_pipeline() -> None:
    src_dir = Path("docs_src")
    html_dir = Path("docs_html")
    md_dir = Path("docs")

    print("[1/3] Compiling GitHub Markdown documentation...")
    build_markdown(input_path=str(src_dir), output=str(md_dir))

    print("[2/3] Compiling Responsive HTML static site...")
    build_html(input_path=str(src_dir), output=str(html_dir))

    print("[3/3] Exporting hero diagram for release badge...")
    export_code_block(
        file_path=str(src_dir / "index.md"),
        target="1",
        output_path="assets/hero_diagram.png",
    )
    print("Documentation build completed successfully!")


if __name__ == "__main__":
    run_documentation_pipeline()
```

### 6.2. Automated Visual Snapshot Testing with Pytest

```python
from pathlib import Path
from drawlib.tools import export_code_block


def test_architecture_diagram_generation(tmp_path: Path) -> None:
    output_png = tmp_path / "test_arch.png"

    # Export diagram block 1 to temporary directory
    export_code_block(
        file_path="docs_src/architecture.md",
        target="1",
        output_path=str(output_png),
        grid=False,
    )

    # Verify that image was produced with non-zero file size
    assert output_png.exists()
    assert output_png.stat().st_size > 1024
```

---

## 7. Related Rules
- CLI Commands & Terminal Usage: `uv run drawlib rules show cli`
- Project Architecture & Scaffolding: `uv run drawlib rules show project-overview`
- Canvas Lifecycle & Export: `uv run drawlib rules show lib-canvas`
