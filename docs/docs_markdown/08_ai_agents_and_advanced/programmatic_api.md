# Programmatic Python API (`drawlib.tools`)

While the `drawlib` CLI provides terminal commands for common workflows, Drawlib exposes a comprehensive Python developer API under `drawlib.tools`. This API allows you to integrate document compilation, diagram export, image snapshot testing, and template automation directly into CI/CD pipelines, web servers, and custom build scripts.

---

## 1. Module Overview & Core Imports

```python
from drawlib.tools import (
    # Document, Slide, & Image Compilation
    build_document,
    build_html,
    build_markdown,
    build_pdf,
    build_slide,
    build_image,
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

## 2. Document Compilation API

### 2.1 `build_html()`
Compiles Markdown documents or directories into a responsive static HTML website:

```python
from drawlib.tools import build_html

build_html(
    input_path="docs_src/",
    output_path="docs_html/",
    styles_path="docs_src/styles.py",  # Optional custom styles script
    utils_path="docs_src/utils.py",    # Optional drawing helper script
    no_cache=False,                    # Set True to bypass SQLite cache
    image_format="png",                # "png" or "webp"
)
```

### 2.2 `build_markdown()`
Compiles source Markdown containing embedded ````drawlib```` blocks into standard GitHub-Flavored Markdown:

```python
from drawlib.tools import build_markdown

build_markdown(
    input_path="docs_src/",
    output_path="docs/",
    styles_path="docs_src/styles.py",
)
```

### 2.3 `build_pdf()`
Compiles documents directly to vector PDF using headless Chromium:

```python
from drawlib.tools import build_pdf

build_pdf(
    inputs="docs_src/",
    output_path="docs.pdf",
    generate_index=True,               # Generate Table of Contents
    page_break=True,                   # Page break before each chapter
)
```

---

## 3. Single Diagram Extraction (`export_code_block`)

Extracts and renders a single diagram from a Markdown file or a standalone `.py` script without opening a GUI display:

```python
from drawlib.tools import export_code_block

# Extract block 1 from Markdown with coordinate grid:
export_code_block(
    file_path="docs_src/architecture.md",
    target="1",                        # 1-based index or target filename
    output_path=".drawlib/scratch/arch.png",
    grid=True,                         # Overlay coordinate grid
)

# Export from standalone Python script:
export_code_block(
    file_path="scripts/diagram.py",
    output_path="assets/diagram.png",
    grid=False,
)
```

---

## 4. In-Memory Image API (`Dimage`)

Drawlib can export canvases directly to in-memory `Dimage` objects without writing temporary files to disk:

```python
from drawlib import canvas, shapes, styles

canvas.setup(width=60, height=40)
shapes.rectangle((30, 20), width=40, height=25, style=styles.Styles.PrimaryFlat, text="In-Memory", text_style=styles.Styles.WhiteBold)

# Export directly to Dimage object
dimage = canvas.export_dimage()

# Access underlying PIL Image or save
pil_image = dimage.image
dimage.save("output.png")
```

---

## 5. Automated Visual Regression Testing with Pytest

Integrate diagram rendering into your test suite to ensure code changes never break visual illustrations:

```python
from pathlib import Path
from drawlib.tools import export_code_block

def test_architecture_diagram_renders(tmp_path: Path):
    target_png = tmp_path / "test_diagram.png"
    
    export_code_block(
        file_path="docs_src/index.md",
        target="1",
        output_path=str(target_png),
        grid=False,
    )
    
    # Assert diagram was generated with valid file size
    assert target_png.exists()
    assert target_png.stat().st_size > 2048
```
