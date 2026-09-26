# `drawlib build`

The `drawlib build` command compiles Python drawing scripts or Markdown/HTML documents containing embedded `drawlib` code blocks into images, rendered Markdown, static HTML sites, or vector PDFs.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib build html docs_src/`).

---

## 1. Syntax Overview

```bash
drawlib build <subcommand> [TARGET] [OPTIONS]
```

### Available Subcommands

| Subcommand | Purpose | Primary Output |
| :--- | :--- | :--- |
| **`image`** (alias: `images`) | Executes one or more Python scripts (`.py`) or directories to generate image files. | PNG, WebP, JPG, SVG images |
| **`markdown`** | Compiles Markdown documents containing `drawlib` code blocks into rendered Markdown for GitHub. | `.md` files + `*_images/` |
| **`html`** | Compiles a single file or an entire directory into a static HTML page or responsive website. | `.html` files + `style.css` + `*_images/` |
| **`pdf`** | Compiles one or more Markdown/HTML files into a unified vector PDF via headless Chromium. | `.pdf` file |

---

## 2. `drawlib build html`

Compiles documentation into responsive static HTML.

```bash
# Compile entire directory into a multi-page documentation website:
drawlib build html docs_src/ -o docs_html/

# Compile a single Markdown file:
drawlib build html docs_src/index.md -o docs_html/index.html

# Apply custom Python configuration script:
drawlib build html docs_src/ -o docs_html/ -c config.py
```

> **Note**: `drawlib build html` and `drawlib build pdf` require `template.html` and `style.css` in the project directory. Run `drawlib init` to scaffold them, or provide them manually.

### Options:
- `-o`, `--output <path>`: Output file or destination directory path.
- `-c`, `--config <path>`: Path to a Python setup script executed before illustrations (e.g. `config.py`).
- `--image-format <png|svg|inline_svg|webp>`: Output image format for rendered illustrations (default: `png`).
- `--css-mode <auto|embed|external>`: CSS embedding strategy (default: `auto`).

---

## 3. `drawlib build markdown`

Compiles documentation into rendered Markdown optimized for browsing on GitHub or GitLab repositories.

```bash
# Compile documentation tree to docs/:
drawlib build markdown docs_src/ -o docs/
```

- Embedded `drawlib` blocks are converted to standard syntax-highlighted Python blocks followed by relative Markdown image links:
  ````text
  ```python
  # Rendered Python code...
  ```
  ![Figure 1](doc_images/1.png)
  ````
- Local images and cross-document links are preserved as relative links.

---

## 4. `drawlib build pdf`

Compiles documents into publication-ready vector PDFs using Playwright and headless Chromium.

### Prerequisites (PDF Support & Chromium)

PDF export requires Playwright and the headless Chromium browser binary:

#### Using uv (Recommended)

```bash
$ uv add "drawlib[pdf]"
$ uv run playwright install chromium
```

#### Using pip

```bash
$ pip install "drawlib[pdf]"
$ playwright install chromium
```

### Usage Examples

```bash
# Compile single document to PDF:
drawlib build pdf doc_src/01_overview.md -o overview.pdf

# Compile multi-file directory into a unified manual:
drawlib build pdf doc_src/ -o doc.pdf --generate-index

# Include current build timestamp in PDF metadata:
drawlib build pdf doc_src/ -o doc.pdf --timestamp
```

- **Deterministic Builds by Default**: By default, Drawlib normalizes the PDF `/CreationDate` and `/ModDate` metadata to fixed timestamps of identical length. If the document content does not change, consecutive builds produce byte-identical PDF files with zero Git diff.
- **Bypassing Normalization (`--timestamp`)**: Pass `--timestamp` if you wish to record the actual current build date and time in the PDF metadata.
- Automatically optimizes page breaks, headers, footers, and margins for A4/Letter print formats.
- Suppresses folded dropdown code elements to produce clean, executive-ready documentation.

---

## 5. `drawlib build image` (or `images`)

Executes standalone Python drawing scripts to generate standalone images.

```bash
# Run a single drawing script:
drawlib build image my_chart.py

# Run all drawing scripts in a directory:
drawlib build images images_src/ -o images/
```

---

## 6. Diagram Build Cache & Caching Behavior

Drawlib automatically caches rendered illustrations in a local SQLite database (`.drawlib/cache.db`) located in the current working directory. Unchanged code blocks are restored from the cache without re-executing Python code, dramatically speeding up subsequent builds.

### Bypassing Cache
To bypass the cache and force a complete re-render of all illustrations:

```bash
drawlib build html docs_src/ -o docs_html/ --no-cache
drawlib build markdown docs_src/ -o docs/ --no-cache
drawlib build pdf doc_src/ -o doc.pdf --no-cache
drawlib build image images_src/ -o images/ --no-cache
```

### Clearing Cache
To clear the local diagram cache, delete the `.drawlib/` directory:

```bash
rm -rf .drawlib/
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
