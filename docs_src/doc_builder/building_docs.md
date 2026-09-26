# Building Documents

This guide explains how to compile your Markdown documentation into static HTML websites, rendered Markdown for GitHub, and PDF documents using both the CLI and Python API.

---

## 1. Compiling with the CLI

The `drawlib build` command is the primary tool for compiling documentation.

### 1.1 Compile to Static HTML Website
```bash
# Compile an entire directory into an HTML site:
drawlib build html docs_src/ -o docs_html/

# Compile a single Markdown file to an HTML page:
drawlib build html docs_src/index.md -o docs_html/index.html
```

When compiling a directory to HTML:
- An interactive sidebar navigation is automatically generated based on the document hierarchy or `navbar.md`.
- Static assets (images, PDFs, fonts) in `docs_src/` are copied to `docs_html/` preserving relative paths.
- Default CSS styles are written to `docs_html/style.css`.

### 1.2 Compile to Rendered Markdown (GitHub Browsing)
```bash
# Compile an authoring directory into GitHub-ready Markdown:
drawlib build markdown docs_src/ -o docs/

# Compile a single file:
drawlib build markdown docs_src/index.md -o docs/index.md
```

In Markdown output mode:
- Code blocks are replaced with Python syntax-highlighted blocks followed by Markdown image links (e.g. `![diagram.png](<doc_images>/diagram.png)`).
- Images are saved in a subfolder named `<doc_name>_images/`.
- Document cross-links (e.g. `[Guide](guide.md)`) remain relative Markdown links.

### 1.3 Compile to Headless PDF
```bash
# Compile a single file or directory into a unified vector PDF:
drawlib build pdf doc_src/ -o doc.pdf
```

---

## 2. Compiling with the Python API

You can automate documentation compilation inside Python build scripts or CI/CD pipelines via `drawlib.doc_builder`.

```python
from drawlib.doc_builder import (
    build,
    build_document,
    build_html,
    build_markdown,
    build_pdf,
)

# High-level build function (auto-detects source file/directory):
build(
    source="docs_src/",
    output="docs_html/",
    format="html",
    config_path="config.py",
)

# Compile directly to PDF:
build_pdf(
    source="doc_src/",
    output="doc.pdf",
)
```

### Key Python API Functions

| Function | Signature | Description |
| :--- | :--- | :--- |
| `build()` | `build(source, output, format="html", ...)` | Unified compiler entrypoint for files and directories. |
| `build_document()` | `build_document(source_file, output_path, format="html", ...)` | Compiles a single `.md` or `.html` file. |
| `build_html()` | `build_html(source, output, ...)` | Compiles source into static HTML output. |
| `build_markdown()` | `build_markdown(source, output, ...)` | Compiles source into rendered Markdown output. |
| `build_pdf()` | `build_pdf(source, output, ...)` | Compiles source into a vector PDF file. |

---

## 3. Configuration Scripts (`--config`)

You can provide an external Python configuration script to establish shared settings across all illustrations before they execute.

```bash
drawlib build html docs_src/ -o docs_html/ --config setup_theme.py
```

> **Note**: If a `config.py` file exists inside your source directory (e.g., `docs_src/config.py`), Drawlib automatically detects and loads it without requiring the `--config` flag. Use `--config` when specifying a custom path or alternative configuration file.

### Example `setup_theme.py`:
```python
from drawlib.preset_styles import monochrome_styles

# Override default theme styles or define project constants:
styles = monochrome_styles
PROJECT_NAME = "Enterprise Architecture Docs"
```

All functions, classes, and global variables declared in the configuration script are automatically available within every embedded `drawlib` code block.

---

## 4. Headless PDF Prerequisites

Drawlib generates publication-ready vector PDFs by compiling documents to HTML and rendering them via Playwright and headless Chromium.

### Installing PDF Support

PDF export requires Playwright and the Chromium browser binary:

#### 1. Install Playwright

- **Using uv:**
  ```bash
  uv add "drawlib[pdf]"
  ```
- **Using pip:**
  ```bash
  pip install "drawlib[pdf]"
  ```

#### 2. Install Headless Chromium

- **Using uv:**
  ```bash
  uv run playwright install chromium
  ```
- **Using pip:**
  ```bash
  playwright install chromium
  ```

Once installed, compile your documents to PDF using:

```bash
drawlib build pdf doc_src/ -o doc.pdf
```

> **Deterministic Builds & Timestamps**: By default, Drawlib normalizes PDF `/CreationDate` and `/ModDate` metadata to a fixed timestamp so that consecutive builds produce byte-identical files with no Git changes. If you need to include the actual build time in the PDF metadata, pass the `--timestamp` flag (or `timestamp=True` in Python).

---

## 5. Diagram Build Cache

Drawlib automatically caches rendered diagram images in a local SQLite database at `.drawlib/cache.db` relative to the current working directory.

- **Incremental Builds**: On subsequent runs, code blocks whose code and configuration have not changed are instantly served from the cache, avoiding re-rendering and significantly speeding up builds.
- **Bypassing Cache**: Pass `--no-cache` to force re-executing and re-rendering all diagram code blocks:
  ```bash
  drawlib build html docs_src/ -o docs_html/ --no-cache
  ```
- **Clearing Cache**: To wipe the cache completely, simply delete the `.drawlib/` directory:
  ```bash
  rm -rf .drawlib/
  ```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
