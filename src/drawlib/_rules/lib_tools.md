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
    # Project Scaffolding, AI Agent Rules, Local Server, Cache, & CSS Presets
    init_project,
    list_project_types,
    init_agent_instruction,
    list_agent_targets,
    detect_agent_targets,
    get_agent_instruction,
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
Compiles an `i18n`-native `site` or `doc` project directory (`docs_src/` or `doc_src/` containing `drawlib.toml` and `<lang>/` subdirectories) into responsive HTML pages with localized stylesheets, shared deduplicated `images/`, a language switcher (when 2+ locales are configured), and a root default-locale `index.html`:

```python
from drawlib.tools import build_html

build_html(
    input_dir="docs_src/",
    output_dir="docs_html/",
    image_format="png",      # "png" or "webp"
    styles_path=None,        # Optional custom styles.py override
    utils_path=None,         # Optional custom utils.py override
    no_cache=False,          # Force re-rendering all code blocks
    css_mode="external",     # "external" (default) or "embed"
)
```

### 2.2. Markdown Build (`build_markdown`)
Compiles an `i18n`-native `site` or `doc` project directory into GitHub-ready Markdown (`<output_dir>/<lang>/` + shared `<output_dir>/images/`). ````drawlib```` code blocks are replaced with syntax-highlighted Python code (according to `code=` options) and relative image links:

```python
from drawlib.tools import build_markdown

build_markdown(
    input_dir="docs_src/",
    output_dir="docs_markdown/",
    image_format="png",
    styles_path=None,
    utils_path=None,
    no_cache=False,
)
```

### 2.3. PDF Build (`build_pdf`)
Compiles a `doc` project directory, `slide` project directory, or standalone Markdown/HTML file directly to print-ready vector PDF(s) using headless Chromium via Playwright (`playwright` is a standard dependency, and `chromium-headless-shell` downloads automatically on first `build_pdf` or `build_pptx` run). For `doc` and `slide` project directories, emits `<base>_<lang>.pdf` per configured locale and returns the `default_lang` PDF path:

```python
from drawlib.tools import build_pdf

# Compile all locales of a doc project -> emits doc_<lang>.pdf:
pdf_path = build_pdf(
    input_path="doc_src/",
    output_file="doc.pdf",
    generate_index=True,
    styles_path=None,
    utils_path=None,
)

# Or compile a single Markdown page -> writes exact output.pdf:
build_pdf(
    input_path="docs_src/en/index.md",
    output_file="output.pdf",
)
```

*(Note: In minimal Linux containers such as `python:3.12-slim` lacking OS shared libraries like `libnss3` or `libgbm1`, run `playwright install-deps chromium` or `playwright install --with-deps --only-shell chromium`.)*

### 2.4. MS Word Build (`build_docx`)
Compiles a linear `doc` project directory (`doc_src/` -> emits `manual_<lang>.docx` per locale and returns the `default_lang` `.docx` path) or a single Markdown file (`.md` -> writes exact `output_file`) into a native editable Microsoft Word (`.docx`) document (`python-docx`). Outputs native editable Word headings, prose, lists, tables, blockquotes, and syntax-highlighted code blocks, with ````drawlib```` diagrams embedded as high-DPI static PNGs (default `dpi=200`):

```python
from drawlib.tools import build_docx

output_docx = build_docx(
    input_path="doc_src/",       # Or pass keyword input_dir="doc_src/"
    output_file="manual.docx",   # Emits manual_<lang>.docx per locale for doc projects
    title=None,
    page_break=True,
    generate_index=False,
    dpi=200,
    styles_path=None,
    utils_path=None,
    no_cache=False,
    timestamp=False,
)
```

### 2.5. HTML Slide Deck & MS PowerPoint Build (`build_slide` & `build_pptx`)
Compiles an `i18n`-native `slide` project directory (`slide_src/` containing `drawlib.toml` and `<lang>/` slides) into an interactive multi-locale 16:9 HTML presentation (`build_slide`, returning `<output_dir>/<default_lang>/index.html`) or measures the `1920x1080` slide DOM via headless Chromium to write native editable 16:9 (`960x540 pt`) Microsoft PowerPoint slides (`build_pptx`, emitting `<stem>_<lang>.pptx` per locale with `::: block` cards, `rgba` alpha, text boxes, lists, tables, code blocks, `::: note` speaker notes, and high-DPI static PNG diagrams):

```python
from drawlib.tools import build_pptx, build_slide

default_index_html = build_slide(
    input_dir="slide_src/",
    output_dir="slide_html/",
    styles_path=None,
    utils_path=None,
)

output_pptx = build_pptx(
    input_dir="slide_src/",
    output_file="deck.pptx",     # Emits deck_<lang>.pptx per locale
    title=None,
    theme=None,
    dpi=240,
    anim_frame="last",           # "first" or "last" for animated blocks
    styles_path=None,
    utils_path=None,
    no_cache=False,
    timestamp=False,
)
```

### 2.6. Python Image Batch Build (`build_image`)
Executes standalone Python drawing scripts (`images_src/*.py`) or extracts diagrams from `doc` / `site` / `slide` Markdown projects in batch mode:

```python
from drawlib.tools import build_image

build_image(
    input_path="images_src/",
    output_path="images/",
    styles_path="images_src/styles.py",
    utils_path="images_src/utils.py",
    grid=False,
)
```

---

## 3. Diagram Export & Preview (`export` & `show`)

### 3.1. `export_code_block` (Single Diagram Extraction)
Extracts and renders a single ````drawlib```` illustration from a Markdown file or a standalone `.py` script without opening a GUI display:

```python
from drawlib.tools import export_code_block

# Export block 1 (or named file) from a Markdown document:
export_code_block(
    file_path="docs_src/en/architecture.md",
    target="1",  # 1-based index or target filename (e.g. "arch.png")
    output_path=".drawlib/scratch/arch.png",
    grid=True,  # Overlay coordinate grid lines (-g)
    styles_path="docs_src/styles.py",
    utils_path="docs_src/utils.py",
)

# Export directly from a standalone Python script:
export_code_block(
    file_path="images_src/my_diagram.py",
    output_path=".drawlib/scratch/output.png",
    grid=False,
)
```

### 3.2. `show_code_block` (Desktop GUI Preview)
Displays the rendered illustration in a local GUI window for interactive alignment:

```python
from drawlib.tools import show_code_block

show_code_block(
    file_path="docs_src/en/architecture.md",
    target="1",
    grid=True,
    styles_path="docs_src/styles.py",
    utils_path="docs_src/utils.py",
)
```

---

## 4. Project Scaffolding

Automates initial project creation with `drawlib.toml`, pre-configured `<lang>/` directories (for `doc`, `site`, `slide`), `styles.py`, `utils.py`, and `build.sh`:

```python
from drawlib.tools import init_project, list_project_types

# Inspect available starter templates:
types = list_project_types()
# Returns: {"site": "Multi-page documentation...", "doc": "...", "slide": "...", "images": "..."}

# Scaffold a bilingual EN/JA multi-page documentation website:
init_project(
    project_type="site",
    target="docs",
    destination=".",
    lang="en,ja",
    style="google",
    force=False,
)
```

### 4.2. AI Coding Agent Instructions (`init_agent_instruction`)
Generates tool-idiomatic Drawlib instruction files (with YAML/MDC frontmatter or non-destructive HTML comment markers) for Antigravity, Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, Roo Code, OpenAI Codex (`AGENTS.md`), and Gemini CLI (`GEMINI.md`):

```python
from drawlib.tools import (
    detect_agent_targets,
    get_agent_instruction,
    init_agent_instruction,
    list_agent_targets,
)

# Inspect supported AI coding agent targets:
targets = list_agent_targets()

# Detect existing agent config directories/files in a workspace:
detected = detect_agent_targets(".")  # e.g. ["antigravity", "claude"]

# Generate .agents/rules/drawlib.md (default mode="auto" for on-demand loading):
written = init_agent_instruction(
    agent=["antigravity", "claude"],
    destination=".",
    mode="auto",      # "auto" (on-demand) or "always" (always-on)
    global_scope=False,
    force=False,
)

# Render instruction Markdown string in memory:
md_text = get_agent_instruction("cursor", mode="auto")
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
    md_dir = Path("docs_markdown")

    print("[1/3] Compiling GitHub Markdown documentation...")
    build_markdown(input_dir=str(src_dir), output_dir=str(md_dir))

    print("[2/3] Compiling Responsive HTML static site...")
    build_html(input_dir=str(src_dir), output_dir=str(html_dir))

    print("[3/3] Exporting hero diagram for release badge...")
    export_code_block(
        file_path=str(src_dir / "en" / "index.md"),
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
        file_path="docs_src/en/architecture.md",
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
