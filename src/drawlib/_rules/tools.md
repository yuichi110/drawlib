# Drawlib Tools Guidelines

`drawlib.tools` is the programmatic Python developer API powering the Drawlib CLI.  
While `drawlib` CLI commands (`drawlib build`, `drawlib export`, etc.) are designed for terminal execution, `drawlib.tools` provides direct Python function interfaces to embed document compilation, diagram export, template validation, and cache management into custom automation scripts, CI/CD pipelines, and testing suites.

---

## 1. Imports & Core Architecture

All public developer tools can be imported directly from `drawlib.tools` or their dedicated submodules:

```python
from drawlib.tools import (
    # Top-Level Facade Modules
    build,           # Document and image compilation (HTML, Markdown, PDF, image)
    export,          # Single illustration block extraction and rendering
    show,            # Desktop GUI preview window
    init,            # Project scaffolding generator
    serve,           # Local development HTTP server
    cache,           # Font and icon cache manager
    css,             # Built-in CSS presets management
    template,        # Jinja2 template export and validation

    # Direct Function Re-exports
    build_html,
    build_markdown,
    build_pdf,
    build_image,
    export_block,
    export_code_block,
    show_block,
    show_code_block,
    init_project,
    list_project_types,
    serve_docs,
    list_cache,
    clear_cache,
    download_cache,
    list_css,
    export_css,
    list_templates,
    export_template,
    validate_template,
)
```

---

## 2. Document & Image Compilation (`drawlib.tools.build`)

The `build` package compiles Markdown documents, multi-page document sites, and standalone Python illustration scripts into production outputs.

### 2.1. HTML Build (`build_html`)
Compiles a single Markdown file or a documentation source directory (`docs_src/`) into responsive HTML pages with navigation and styling:

```python
from drawlib.tools import build_html

build_html(
    input_path="docs_src/",
    output_path="docs_html/",
    config_path="config.py",        # Optional global Python config
    css_path="custom.css",          # Optional custom CSS file or preset name
    template_path="template.j2",    # Optional custom Jinja2 HTML template
    css_mode="auto",                # "auto", "embed", or "external"
    no_cache=False,                 # Force re-rendering all code blocks
    image_format="png",             # "png", "svg", or "inline_svg"
)
```

### 2.2. Markdown Build (`build_markdown`)
Compiles Markdown documents for GitHub repository browsing. ````drawlib```` code blocks are replaced with syntax-highlighted Python code followed by relative image links:

```python
from drawlib.tools import build_markdown

build_markdown(
    input_path="docs_src/",
    output_path="docs/",
    config_path="config.py",
    image_format="png",
)
```

### 2.3. PDF Build (`build_pdf`)
Compiles documents directly to print-ready vector PDF using headless Chromium via Playwright:

```python
from drawlib.tools import build_pdf

build_pdf(
    input_path="docs_src/index.md",
    output_path="output.pdf",
    config_path="config.py",
    css_path="custom.css",
    template_path="template.j2",
)
```

### 2.4. Python Image Batch Build (`build_image`)
Executes standalone Python drawing scripts in batch mode:

```python
from drawlib.tools import build_image

build_image(
    input_path="drawings/",
    output_path="dist/images/",
    config_path="config.py",
    grid=False,
)
```

---

## 3. Diagram Export & Preview (`export` & `show`)

### 3.1. `export_block` (Single Diagram Extraction)
Extracts and renders a single ````drawlib```` illustration from a Markdown file or a standalone `.py` script without opening a GUI display:

```python
from drawlib.tools import export_block

# Export block 1 from a Markdown document:
export_block(
    file_path="docs_src/architecture.md",
    target="1",                      # 1-based index or target filename (e.g. "arch.png")
    output_path="scratch/arch.png",
    grid=True,                       # Overlay coordinate grid lines (-g)
    config_path="config.py",
)

# Export directly from a standalone Python script:
export_block(
    file_path="scratch/my_diagram.py",
    output_path="scratch/output.png",
    grid=False,
)
```

### 3.2. `show_block` (Desktop GUI Preview)
Displays the rendered illustration in a local GUI window for interactive alignment:

```python
from drawlib.tools import show_block

show_block(
    file_path="docs_src/architecture.md",
    target="1",
    grid=True,
)
```

---

## 4. Project Scaffolding (`drawlib.tools.init`)

Automates initial project creation with pre-configured directories, sample Markdown files, and build scripts:

```python
from drawlib.tools import init_project, list_project_types

# Inspect available starter templates:
types = list_project_types()
# Returns: ["site", "simple", "pdf"]

# Scaffold a multi-page documentation website:
init_project(
    project_type="site",
    target_dir="./my_docs",
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
    check_links=True,
)
```

### 5.2. Cache Management (`drawlib.tools.cache`)
Inspect and manage cached font and icon assets:

```python
from drawlib.tools.cache import clear_cache, download_cache, list_cache

# List cached font families and icons:
cached_items = list_cache()

# Download all default font packs for offline use:
download_cache()

# Purge cache to reclaim disk space:
clear_cache()
```

### 5.3. Template & CSS Presets (`template` & `css`)
Inspect and export built-in Jinja2 templates and CSS themes:

```python
from drawlib.tools.template import export_template, list_templates, validate_template
from drawlib.tools.css import export_css, list_css

# List and export built-in Jinja2 templates:
templates = list_templates()
export_template("sidebar", "custom_sidebar.html.j2")

# Validate a custom template for required placeholders:
validate_template("custom_sidebar.html.j2")

# List and export CSS style presets:
presets = list_css()
export_css("google", "theme_google.css")
```

---

## 6. Practical Code Examples

### 6.1. Custom CI/CD Build & Verification Automation Script

```python
from pathlib import Path
from drawlib.tools import build_html, build_markdown, export_block

def run_documentation_pipeline() -> None:
    src_dir = Path("docs_src")
    html_dir = Path("docs_html")
    md_dir = Path("docs")

    print("[1/3] Compiling GitHub Markdown documentation...")
    build_markdown(input_path=str(src_dir), output_path=str(md_dir))

    print("[2/3] Compiling Responsive HTML static site...")
    build_html(input_path=str(src_dir), output_path=str(html_dir), css_path="google")

    print("[3/3] Exporting hero diagram for release badge...")
    export_block(
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
from drawlib.tools import export_block

def test_architecture_diagram_generation(tmp_path: Path) -> None:
    output_png = tmp_path / "test_arch.png"

    # Export diagram block 1 to temporary directory
    export_block(
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
- Documentation Site Structure & Navbar: `uv run drawlib rules show docs_build`
- Canvas Lifecycle & Export: `uv run drawlib rules show canvas`
