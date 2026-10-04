# CLI Reference Manual

Drawlib provides a unified Command Line Interface (`drawlib`) for compiling documentation, extracting standalone visual diagrams, managing cache assets, validating links, and inspecting built-in design systems.

---

## 1. Quick Command Matrix

```bash
# Compilation
drawlib build html docs_src/ -o docs_html/                  # Responsive static HTML website
drawlib build markdown docs_src/ -o docs/                  # GitHub-ready Markdown
drawlib build pdf docs_src/ -o manual.pdf --toc             # High-fidelity vector PDF
drawlib build image scripts/ -o assets/ -g                 # Batch Python image rendering

# Scaffolding
drawlib init list                                          # List starter project templates (site, doc, slide, image)
drawlib init doc my_doc/                                   # Scaffold linear document project (HTML, PDF, MD, images)
drawlib init site my_site/                                 # Scaffold documentation site
drawlib init slide my_deck/ -s google                      # Scaffold 16:9 presentation slide deck
drawlib init image my_images/                              # Scaffold standalone image project

# Inspection & Preview
drawlib show doc.md 1 -o .drawlib/scratch/fig1.png                 # Headless extraction of block 1
drawlib show doc.md 1 -g -o .drawlib/scratch/fig1_grid.png         # Export block 1 with coordinate grid
drawlib show script.py -o .drawlib/scratch/fig.png                 # Export standalone Python script

# Local Server & Verification
drawlib serve docs_html/                                   # Local preview on http://localhost:8000
drawlib serve docs_html/ --check                           # Pre-flight broken link/asset audit

# Design Systems & Cache
drawlib colors list                                        # List color catalogs (default, google, mono, 140)
drawlib styles list                                        # List style catalogs (default, google, mono)
drawlib css list                                           # List CSS presets for HTML and PDF
drawlib cache list                                         # Inspect cached fonts and icons
drawlib rules list                                         # List AI rule instruction manuals
```

---

## 2. Compilation Subsystem (`drawlib build`)

### 2.1 `drawlib build html`
Compiles Markdown documents or directories into a responsive static HTML documentation website with sidebar navigation and syntax highlighting.

```bash
drawlib build html <INPUT> [OPTIONS]
```

- `-o`, `--output <path>`: Destination directory or file path.
- `-f`, `--format <png|webp>`: Image format for embedded diagrams (default: `png`).
- `-s`, `--styles <path>`: Path to project styles script (e.g. `styles.py`).
- `-u`, `--utils <path>`: Path to helper drawing script (e.g. `utils.py`).
- `--no-cache`: Force clean diagram rendering, ignoring the SQLite image cache.

### 2.2 `drawlib build markdown`
Compiles source Markdown containing embedded ````drawlib```` blocks into standard GitHub-Flavored Markdown. Rendered diagrams are exported to companion image folders (`<doc>_images/`).

```bash
drawlib build markdown docs_src/ -o docs/
```

- **Overwrite Protection**: Refuses to overwrite source files in-place (`src_abs == dest_abs`). Always compile to an output directory (e.g. `docs/`).

### 2.3 `drawlib build pdf`
Merges Markdown chapters into a high-fidelity vector PDF using headless Chromium.

```bash
drawlib build pdf docs_src/ -o report.pdf --toc --page-break
```

- `--toc`, `--generate-index`: Insert an automated Table of Contents.
- `--page-break`: Insert CSS page breaks between chapters (`page-break-before: always`).

### 2.4 `drawlib build image`
Batch executes standalone Python illustration scripts (`.py`) or extracts embedded drawing blocks from Markdown files (`.md`) to generate image assets.

```bash
drawlib build image docs_src/ -o docs_images/ --grid
```

- For Python scripts: outputs `<script_name>.png` (or format) directly into the destination folder.
- For Markdown files: outputs diagrams cleanly into `<markdown_name>_images/<image_file>` subdirectories to prevent file collisions across chapters.
- `-g`, `--grid`: Saves companion `*_grid.png` images overlaid with coordinate grids.
- Mirrors nested subdirectory hierarchies automatically in the destination folder.

---

## 3. Scaffolding Subsystem (`drawlib init`)

Bootstraps new projects with standardized folder structures, configuration scripts, and build automations:

```bash
drawlib init <TYPE> [DESTINATION] [OPTIONS]
```

- `<TYPE>`: `site`, `doc`, `slide`, `image`, or `list`.
- `-o`, `--output <name>`: Base project/artifact name (sets source folder to `<name>_src` and output to `<name>_html/`, `<name>.pdf`, etc.).
- `-s`, `--style <theme>`: Style preset theme (`default`, `google`, `monochrome`, etc.) configuring both `style.css` and `styles.py`.
- `--here`: Scaffold directly in the current working directory without a wrapper folder.
- `--force`: Overwrite existing files if directory is not empty.
- `--lang <code/alias>`: Starter content language (`en`, `ja`, `zh-cn`, `ko`, `th`, `hi`, etc.).

---

## 4. Single Diagram Extraction (`drawlib show`)

Previews diagrams in a desktop GUI window, or exports them directly to an image file when `-o` is supplied:

```bash
# Export block 1 with coordinate grid:
drawlib show docs_src/overview.md 1 -g -o .drawlib/scratch/fig1.png

# Preview standalone Python script in GUI window:
drawlib show my_drawing.py
```

---

## 5. Local Server & Pre-Flight Link Checking (`drawlib serve`)

Starts a zero-dependency local HTTP development server to test built HTML documentation:

```bash
# Start server on default port 8000:
drawlib serve docs_html/

# Pre-flight broken link and missing asset check only (ideal for CI/CD gates):
drawlib serve docs_html/ --check
```

---

## 6. AI Rules Catalog (`drawlib rules`)

Inspect built-in architectural and library manuals on demand from the terminal:

```bash
drawlib rules list                  # View all available rule topics
drawlib rules show agent-instruction # View agent bootstrap manual
drawlib rules show overview         # View Cartesian geometry principles
drawlib rules show lib-charts       # View chart APIs and data models
drawlib rules show lib-diagrams     # View technical diagram APIs
```
