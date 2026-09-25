# `drawlib build`

The `drawlib build` command compiles Python drawing scripts or Markdown/HTML documents containing embedded `drawlib` code blocks into images, rendered Markdown, static HTML sites, or vector PDFs.

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

# Apply custom configuration, custom CSS, and custom Jinja2 template:
drawlib build html docs_src/ -o docs_html/ -c config.py --css custom.css -t template.j2
```

### Options:
- `-o`, `--output <path>`: Output file or destination directory path.
- `-c`, `--config <path>`: Path to a Python setup script executed before illustrations (e.g. `config.py`).
- `--image-format <png|svg|inline_svg|webp>`: Output image format for rendered illustrations (default: `png`).
- `--css <path>`: Path to custom CSS stylesheet.
- `-t`, `--template <path>`: Path to custom Jinja2 template file.
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

Compiles documents into a high-fidelity vector PDF using system Chromium-based browsers (Chrome, Chromium, Edge).

```bash
# Compile single document to PDF:
drawlib build pdf report.md -o report.pdf

# Compile multi-file directory into a unified manual:
drawlib build pdf docs_src/ -o manual.pdf --config setup.py
```

- Automatically optimizes page breaks, headers, footers, and margins for A4/Letter print formats.
- Suppresses folded dropdown code elements to produce clean, executive-ready documentation.

---

## 5. `drawlib build image` (or `images`)

Executes standalone Python drawing scripts to generate standalone images.

```bash
# Run a single drawing script:
drawlib build image my_chart.py

# Run all drawing scripts in a directory:
drawlib build images diagrams/ -o output/
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
