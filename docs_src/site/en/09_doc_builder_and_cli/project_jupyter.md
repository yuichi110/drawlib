# Jupyter & Colab Notebook Project Guide (`drawlib init project jupyter`)

The `jupyter` starter template brings **"Illustrated Notebook & Google Colab as Code"** to Drawlib. Instead of versioning monolithic, diff-hostile `.ipynb` JSON files with stale binary outputs, you author narrative prose, architectural diagrams (```` ```drawlib ````), and interactive Python exercises (```` ```python ```` or ```` ```drawlib cell=code ````) in clean Markdown (`jupyter_src/<lang>/**/*.md`)—compiling from a single `drawlib.toml` through an **in-process AI Dry-Run engine** into three dedicated deliverables: **standalone self-contained `.ipynb` notebooks (`drawlib build jupyter` -> `jupyter_jupyter/`)**, a **2-column HTML preview site with bundled `.ipynb` downloads (`drawlib build html` -> `jupyter_html/`)**, and **extracted diagram images (`drawlib build image` -> `jupyter_images/`)**:

```drawlib code=fold align=center file=project_jupyter_compilation_pipeline.png caption="How Markdown Notebook Sources Compile Through the In-Process AI Dry-Run Engine into Standalone .ipynb, HTML Preview, and Image Targets"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=62)

# Left: Markdown Notebook Source
rectangle((20.5, 31), width=33, height=52, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_code((10.0, 49.0), width=4.4, style=Styles.PrimaryBold)
text((23.0, 49.0), "jupyter_src/<lang>/", style=Styles.DarkBold.patch(text_size=10.5))
text(
    (20.5, 36.2),
    "01_tutorial.md\n• Narrative + # H1 / ## H2\n• ```drawlib (diagram)\n• ```python (code cell)",
    style=Styles.Dark.patch(text_size=10.0),
)
rectangle(
    (20.5, 13.5),
    width=28.5,
    height=8.2,
    style=Styles.PrimaryNeutral.patch(shape_r=1.2),
    text="styles.py & drawlib.toml",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

# Middle: In-Process AI Dry-Run Engine
line((37.0, 31), (43.5, 31), arrow_head="->", style=Styles.DarkBold)
rectangle((61.0, 31), width=35, height=52, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.play_circle((49.0, 49.0), width=4.6, style=Styles.WhiteBold)
text((63.5, 49.0), "AI Dry-Run Engine", style=Styles.WhiteBold.patch(text_size=10.6))
text(
    (61.0, 33.8),
    "Sequential shared globals\n• Executes code cells\n• Captures stdout & expr\n• Captures show() / save()\n• Fails on Geometry Warn",
    style=Styles.White.patch(text_size=10.0),
)
rectangle(
    (61.0, 13.5),
    width=29.5,
    height=7.8,
    style=Styles.White.patch(shape_r=1.2),
    text="--dry-run Verification",
    text_style=Styles.PrimaryBold.patch(text_size=10.0),
)

# Right: 3 Dedicated Build Targets
line((78.5, 31), (82.5, 31), style=Styles.DarkBold)
line((82.5, 13.0), (82.5, 49.0), style=Styles.DarkBold)
for ty in (49.0, 31.0, 13.0):
    line((82.5, ty), (87.0, ty), arrow_head="->", style=Styles.DarkBold)

rectangle((105.5, 49.0), width=37, height=15.0, style=Styles.PrimaryNeutral.patch(shape_r=1.6))
phosphor.notebook((95.0, 52.2), width=3.8, style=Styles.PrimaryBold)
text((108.5, 52.2), "build jupyter", style=Styles.DarkBold.patch(text_size=10.2))
text((105.5, 45.2), "jupyter_jupyter/<lang>/*.ipynb\n.ipynb only (Drive + Colab)", style=Styles.Dark.patch(text_size=9.5))

rectangle((105.5, 31.0), width=37, height=15.0, style=Styles.SecondaryNeutral.patch(shape_r=1.6))
phosphor.globe((95.0, 34.2), width=3.8, style=Styles.PrimaryBold)
text((108.5, 34.2), "build html", style=Styles.DarkBold.patch(text_size=10.2))
text((105.5, 27.2), "jupyter_html/<lang>/*.html\nIn[n]/Out[n] + bundled .ipynb", style=Styles.Dark.patch(text_size=9.5))

rectangle((105.5, 13.0), width=37, height=15.0, style=Styles.Neutral.patch(shape_r=1.6))
phosphor.images((95.0, 16.2), width=3.8, style=Styles.PrimaryBold)
text((108.5, 16.2), "build image", style=Styles.DarkBold.patch(text_size=10.2))
text((105.5, 9.2), "jupyter_images/<stem>/*.png\nExtracted diagram assets", style=Styles.Dark.patch(text_size=9.5))

save()
```

---

## 1. Why Author Jupyter & Colab Notebooks in Markdown?

Maintaining tutorials, data-science guides, and hands-on workshops directly inside `.ipynb` JSON files introduces friction for engineering teams and AI coding agents:

| Challenge with Raw `.ipynb` Files | How Drawlib's `jupyter` Project Solves It |
| :--- | :--- |
| **Noisy Git Diffs**: Base64 PNG blobs and execution counters clutter pull requests. | **Clean Markdown Source (`jupyter_src/<lang>/*.md`)**: Author plain-text Markdown with fenced ```` ```drawlib ```` and ```` ```python ```` blocks; `.ipynb` and HTML outputs are deterministic build artifacts. |
| **Broken Cells & Stale Outputs**: Out-of-order manual cell execution leaves hidden state bugs. | **In-Process AI Dry-Run (`execute = true` / `--dry-run`)**: Executes every notebook top-to-bottom in a fresh shared `globals` namespace on build, failing immediately on any exception or `[Geometry Warning]`. |
| **Separate Web Docs vs. Notebooks**: Teams duplicate effort maintaining web tutorials and Colab notebooks. | **Multi-Target Output from One `drawlib.toml`**: Compile standalone `.ipynb`-only folders (`drawlib build jupyter` -> `jupyter_jupyter/`) for Google Drive / Colab sharing, a 2-column HTML preview bundled with `.ipynb` downloads (`drawlib build html` -> `jupyter_html/`), or standalone PNGs (`drawlib build image` -> `jupyter_images/`). |
| **Multi-Locale Duplication**: Translating `.ipynb` notebooks into English and Japanese is error-prone. | **Native `[i18n]` Support (`-l en,ja`)**: Unified `<src_dir>/<lang>/` directories with automatic language switcher and per-locale `.ipynb` outputs. |

> **Live Showcase & Private Sharing:** Explore Drawlib's own 6-chapter bilingual interactive tutorial built with `type = "jupyter"` at [`https://www.drawlib.com/jupyter/`](https://www.drawlib.com/jupyter/en/). Need to distribute notebooks privately to clients or internal teams without a public GitHub repository? See the dedicated **[Jupyter Sharing via Google Drive & Colab (`rclone`)](./jupyter_google_drive.md)** guide.

---

## 2. Scaffolding & Directory Layout

Initialize a single-locale or multi-locale `jupyter` project using `drawlib init project jupyter`:

```bash
# Default English jupyter project (creates jupyter_src/en/):
uv run drawlib init project jupyter

# Custom target name + bilingual (en,ja) + Google theme:
uv run drawlib init project jupyter tutorials -l en,ja -s google

# Fast AI Dry-Run verification (executes all cells, checks [Geometry Warning], writes no files):
uv run drawlib build jupyter jupyter_src/ --dry-run

# Build all targets (HTML + bundled .ipynb in jupyter_html/, .ipynb-only in jupyter_jupyter/, PNGs in jupyter_images/):
./jupyter_src/build.sh

# Or build individual targets:
./jupyter_src/build_jupyter.sh   # -> jupyter_jupyter/<lang>/*.ipynb (standalone .ipynb only)
./jupyter_src/build_html.sh      # -> jupyter_html/ (2-column HTML preview + bundled .ipynb)
./jupyter_src/build_image.sh     # -> jupyter_images/ (extracted diagram PNGs)

# Validate HTML preview links and bundled .ipynb assets headlessly:
uv run drawlib serve jupyter_html/ --check
```

Scaffolded directory layout:

```text
jupyter_src/
├── drawlib.toml               # [MANDATORY] Project manifest (type = "jupyter", [i18n], [jupyter], optional [seo])
├── styles.py                  # Shared Drawlib Style / Color overrides (pre-loaded into notebook globals)
├── utils.py                   # Reusable Python helpers imported across notebooks
├── style.css                  # Responsive 2-column HTML preview stylesheet (includes In[n]/Out[n] cells)
├── template.html              # Jinja2 HTML preview layout with Open in Colab & .ipynb download bar
├── _assets/                   # Static images/logos & favicon.png (copied to HTML output _assets/)
├── en/                        # Locale notebook source directory (sorted naturally: 01_, 02_, ...)
│   ├── 01_sample_notebook.md  # Notebook 1: Markdown narrative + drawlib diagrams + python code cells
│   └── README.md              # Authoring guide (automatically excluded from notebook compilation)
├── build.sh                   # Master build script (runs build_html.sh, build_jupyter.sh & build_image.sh)
├── build_html.sh              # Compile 2-column HTML preview + bundled .ipynb -> jupyter_html/
├── build_jupyter.sh           # Compile standalone .ipynb notebooks ONLY -> jupyter_jupyter/
├── build_image.sh             # Extract rendered diagram images -> jupyter_images/
└── serve.sh                   # Local HTTP preview server (drawlib serve jupyter_html/)
```

Each build command emits a clean, purpose-built output directory from the exact same `drawlib.toml`:

```text
jupyter_jupyter/               # `drawlib build jupyter` — 100% standalone .ipynb only (ideal for Google Drive + Colab)
└── en/
    └── 01_sample_notebook.ipynb

jupyter_html/                  # `drawlib build html` — 2-column HTML preview + bundled .ipynb (deployable to any host)
├── index.html                 # Root entry page (rebased from default_lang first notebook)
├── en/
│   ├── index.html
│   ├── 01_sample_notebook.html  # 2-column HTML preview with "⬇ Download .ipynb" & "Open in Colab"
│   └── 01_sample_notebook.ipynb # Bundled executable Jupyter Notebook (linked relatively from HTML)
├── images/                    # Shared diagram images across locales
└── _assets/                   # Static assets & favicon

jupyter_images/                # `drawlib build image` — Extracted diagram images
└── 01_sample_notebook/
    ├── pipeline_overview.png
    └── live_bar_chart.png
```

---

## 3. Dual Code Block Semantics (`cell=markdown` vs. `cell=code`)

Inside `jupyter_src/<lang>/**/*.md`, standard Markdown prose and headings (`# H1`, `## H2`, tables, lists) become `.ipynb` `markdown` cells, while fenced code blocks are routed according to their language identifier (`drawlib` vs. `python`) and optional `cell=` attribute:

| Fence Syntax in `.md` Source | Compiled `.ipynb` Cell Type | Compiled HTML Preview Output | Primary Use Case |
| :--- | :--- | :--- | :--- |
| ```` ```drawlib file=arch.png caption="..." ````<br>*(default `cell=markdown`)* | **`markdown` cell** with self-contained `<img src="data:image/...;base64,..." />` | Rendered `<figure>` diagram with optional `<details>` source fold (`code=fold`) | Explanatory architecture, flow, sequence, or concept diagrams accompanying narrative text. |
| ```` ```drawlib cell=code file=exercise.png ````<br>*(or `[jupyter].drawlib_cell_mode = "code"`)* | Clean unexecuted **`code` cell** (`outputs: []`) with `save(...)` rewritten to `show()` | Notebook `In [n]:` code cell + `Out[n]:` rendered figure | Hands-on Drawlib coding exercises where learners modify coordinates/styles and run the cell in Jupyter/Colab. |
| ```` ```python ````<br>*(default `cell=code`)* | Clean unexecuted **`code` cell** (`outputs: []`) ready for interactive execution | Notebook `In [n]:` code cell + `Out[n]:` execution output | Live Python data preparation, state sharing across cells, or calling Drawlib APIs with `setup(..., cwd=True)` and `show()`. |
| ```` ```python cell=markdown ```` | **`markdown` cell** containing a static syntax-highlighted Python snippet | Standard static code block (not executed) | Non-executable reference pseudocode or configuration snippets. |

```drawlib code=fold align=center file=project_jupyter_cell_routing.png caption="Routing of drawlib and python Code Fences into .ipynb Cells and HTML Preview Blocks"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=128, height=58)

rectangle((64, 51.5), width=120, height=7.0, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.notebook((11.5, 51.5), width=4.4, style=Styles.PrimaryBold)
text(
    (66.0, 51.5),
    "Dual Code Block Routing: Narrative Diagrams (cell=markdown) vs. Live Code Cells (cell=code)",
    style=Styles.DarkBold.patch(text_size=10.8),
)

tbl = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.MutedThin,
    has_header=True,
)
tbl.set_style_cell_evenodd(
    even_color=Colors.White,
    even_text_style=Styles.Dark.patch(text_size=10.0),
    odd_color=Styles.SecondaryNeutral.shape_fill_color or Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.0),
)
tbl.set_style_cell_header(
    background_color=Styles.PrimaryFlat.shape_fill_color or Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
tbl.draw_flexible(
    xy=(4, 46.0),
    column_widths=[34.0, 28.0, 30.0, 28.0],
    row_heights=[8.2, 8.2, 8.2, 8.2, 8.2],
    data=[
        ["Markdown Fence", ".ipynb Cell Type", "Dry-Run Execution", "HTML Preview Rendering"],
        ["```drawlib file=a.png", "markdown cell (Image)", "Sandboxed Diagram", "<figure> + code=fold"],
        ["```drawlib cell=code", "code cell (show())", "Shared Notebook Globals", "In [n]: Code + Out[n]: PNG"],
        ["```python", "code cell", "Shared Notebook Globals", "In [n]: Code + Out[n]: Text/PNG"],
        ["```python cell=markdown", "markdown cell (Code)", "Skipped (Static)", "Syntax-Highlighted Block"],
    ],
)

save()
```

### Markdown Notebook Authoring Example (`01_quickstart.md`):

````markdown
# Chapter 1: Drawlib Quickstart in Google Colab

Learn how to combine explanatory architecture diagrams with live, editable Python cells.

```drawlib align=center code=fold file=ch01_concept_arch.png caption="Explanatory Architecture Diagram (Rendered as a Markdown Cell)"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=32)
rectangle((50, 16), width=76, height=18, style=Styles.PrimaryNeutral, text="Narrative Architecture Figure")
save()
```

```python
!pip install -q drawlib
```

## 1. Shared State Across Executable Python Cells

Variables defined in one `python` cell remain live in subsequent cells:

```python
# Define shared layout metrics
CANVAS_W, CANVAS_H = 100, 36
nodes = ["Ingest", "Transform", "Serve"]
print(f"Configured {len(nodes)} pipeline stages on {CANVAS_W}x{CANVAS_H} canvas")
```

```python
# Render inline using setup(..., cwd=True) and show()
from drawlib.canvas import setup, show
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=CANVAS_W, height=CANVAS_H, cwd=True)
for idx, label in enumerate(nodes):
    cx = 20 + idx * 30
    st = Styles.PrimaryFlat if idx == 2 else Styles.Neutral
    tst = Styles.WhiteBold if idx == 2 else Styles.DarkBold
    rectangle((cx, 18), width=22, height=14, style=st, text=label, text_style=tst)
show()
```
````

---

## 4. Configuring `[jupyter]` & Google Colab Integration (`drawlib.toml`)

Configure default cell modes, dry-run execution, and **Open in Colab** links under `[jupyter]` in `jupyter_src/drawlib.toml`:

```toml
[project]
name = "jupyter"
type = "jupyter"
title = "Drawlib Interactive Notebooks"
description = "Interactive Jupyter & Google Colab Hands-on Tutorials"
style = "google"

[i18n]
default_lang = "en"
langs = ["en", "ja"]

[jupyter]
# Base URL prefix (auto-appends /<lang>/<stem>.ipynb) or {path} URL template:
colab_base_url = "https://colab.research.google.com/github/owner/repo/blob/main/jupyter_jupyter"
drawlib_cell_mode = "markdown"             # Default for ```drawlib fences: "markdown" | "code"
execute = true                             # Sequentially dry-run all code cells during build and render Out[n] in HTML preview

# [seo]
# site_url = "https://example.com/jupyter" # Optional public URL for HTML canonical/OGP/sitemap tags
```

> **100% Self-Contained `.ipynb` Files & Explicit Per-Page `!pip install`:**
> - **Zero Broken Image Links**: All `cell=markdown` ```` ```drawlib ```` diagrams, local Markdown images (`![alt](_assets/...)` / `<img src="...">`), and the official `Open in Colab` badge are automatically embedded inline as Base64 Data URIs via HTML `<img src="data:..." />` tags. Every compiled `.ipynb` works standalone across Google Colab, VS Code Jupyter, and JupyterLab—online or offline—while the HTML preview site serves fast external image files (`images/`).
> - **Explicit Package Installation per Page**: Because required libraries differ from notebook to notebook, write `!pip install -q drawlib ...` (or `%pip install ...`) directly inside a ```` ```python ```` code block near the top of each `.md` file; shell/magic lines are preserved in `.ipynb` and HTML while automatically skipped during in-process AI Dry-Run execution.

### 4.1. `[jupyter]` Reference Table

| Key | Type | Default | Behavior |
| :--- | :--- | :--- | :--- |
| `colab_base_url` | `str` | `""` | Base URL or `{path}` URL template for the **Open in Colab** button injected into `.ipynb` notebooks and HTML preview pages:<ul><li>**Base URL Prefix**: When set to a URL without `{path}` (e.g. `"https://colab.research.google.com/github/owner/repo/blob/main/docs/jupyter"`), Drawlib automatically appends `/<lang>/<stem>.ipynb`.</li><li>**`{path}` URL Template (Non-GitHub / Custom Host)**: Include `{path}` (e.g. `"https://colab.example.com/open?notebook={path}"`) to substitute `<lang>/<stem>.ipynb` at an arbitrary position.</li><li>**Empty (`""`)**: Omits the Colab button while keeping the relative **⬇ Download .ipynb** button active on all HTML pages.</li></ul> |
| `drawlib_cell_mode` | `"markdown" \| "code"` | `"markdown"` | Project-wide default cell mode for ```` ```drawlib ```` blocks when `cell=` is omitted on the fence. |
| `execute` | `bool` | `true` | When `true`, executes all `code` cells sequentially in-process during build and renders `stdout`, expression results, and `show()` / `save()` figures in the HTML preview (`Out [n]`), while keeping `.ipynb` code cells clean (`outputs: []`) for hands-on execution. |

### 4.2. Title & Sidebar Brand Header Resolution (`drawlib.toml` vs. `# H1`)

In the compiled HTML preview site (`jupyter_html/`):
- **Left Sidebar Brand Header (`site_title`)**: Prioritizes `drawlib.toml` `[project].title` -> optional `<lang>/navbar.md` `# H1` -> `"Notebooks"`.
- **Browser Tab `<title>`**: Combines the current notebook's first `# H1` heading and `site_title` as `<Notebook H1> — <site_title>`.
- **Sidebar Navigation Tree**: Automatically extracted from each `.md` file's `# H1` (notebook link) and `## H2` headings (section links) with an instant `/` filter—no manual `navbar.md` maintenance required.

---

## 5. Deterministic Path Resolution in Notebooks (`setup(..., cwd=True)`)

In standard `.py` scripts, `setup(width=..., height=...)` defaults to `cwd=False`, resolving relative paths (`save("chart.png")`, `image("logo.png")`, `Dimage("photo.png")`) relative to the directory of the calling Python script.

In interactive **JupyterLab** or **Google Colab** notebooks, code cells execute inside a temporary kernel frame rather than a `.py` file on disk. Pass **`cwd=True`** to `setup()` inside notebook code cells so relative paths resolve deterministically against `os.getcwd()`:

```python
from drawlib.canvas import save, setup, show
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# Resolve all relative paths (save(), image(), Dimage()) against os.getcwd():
setup(width=100, height=40, cwd=True)
rectangle((50, 20), width=70, height=22, style=Styles.PrimaryNeutral, text="Interactive Notebook Cell")
show()  # Displays inline in Jupyter/Colab and is captured by drawlib build jupyter
```

- When `setup(..., cwd=True)` is active:
  - `save("out.png")` writes to `<os.getcwd()>/out.png` (and `save()` with no filename writes to `<os.getcwd()>/output.png`).
  - `image("data/pic.png")` and `Dimage("data/pic.png")` read from `<os.getcwd()>/data/pic.png`.
- Calling `clear()` resets `cwd` back to `False`.

---

## 6. CLI Build Targets & In-Process AI Dry-Run Verification

Use `drawlib build jupyter`, `drawlib build html`, and `drawlib build image` depending on your delivery target:

```bash
# 1. Fast in-process AI Dry-Run (executes all cells, checks [Geometry Warning], writes no files):
uv run drawlib build jupyter jupyter_src/ --dry-run

# 2. Standalone .ipynb notebooks ONLY -> jupyter_jupyter/<lang>/*.ipynb (ideal for Google Drive + Colab):
uv run drawlib build jupyter jupyter_src/ -o jupyter_jupyter/

# 3. 2-column HTML preview site + bundled .ipynb downloads -> jupyter_html/:
uv run drawlib build html jupyter_src/ -o jupyter_html/

# 4. Extracted diagram PNGs -> jupyter_images/:
uv run drawlib build image jupyter_src/ -o jupyter_images/
```

| Option | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `--output` | `-o` | `<base>_jupyter/` | Destination output directory path (or `.ipynb` file path for single-file build). |
| `--format` | `-f` | `png` | Image output format for embedded `drawlib` blocks (`png` or `webp`). |
| `--styles` / `--utils` | `-s` / `-u` | Auto-resolved | Path to `styles.py` and `utils.py` (pre-loaded into notebook execution `globals`). |
| `--execute` / `--no-execute` | | `None` (from `[jupyter].execute`) | Execute `code` cells sequentially in-process to verify zero errors and `[Geometry Warning]` (`.ipynb` code cells remain clean). |
| `--dry-run` | | `False` | Execute all cells and validate `[Geometry Warning]` without writing output files to disk. |
| `--no-cache` | | `False` | Bypass `.drawlib/cache.db` and re-execute all diagram blocks. |
| `--workers` | `-w` | `auto` | Parallel worker process count (`auto` uses `1 <= (CPU cores - 1) <= 8`). |

### What the In-Process AI Dry-Run Engine Verifies:
1. **Shared State Across Cells**: Cell 1's variables, functions, and imports are live in Cell 2, Cell 3, etc., matching real Jupyter/Colab kernel behavior (`styles.py` and `utils.py` are pre-loaded into the notebook namespace).
2. **Zero Unhandled Exceptions**: Any `SyntaxError`, `NameError`, `TypeError`, or Drawlib validation error halts the build and reports the exact notebook path, cell number (`In [n]`), and traceback.
3. **Zero `[Geometry Warning]`**: Any canvas clipping, out-of-bounds artist, or overlap warning emitted during either `cell=markdown` diagram rendering or `cell=code` execution fails the build (`NotebookExecutionError`).
4. **HTML-Only Execution Outputs (`.ipynb` Kept Clean)**: Standard output (`print(...)`), final cell expressions (`text/plain`), and `show()` / `save()` figures (`image/png`) are rendered into the HTML preview page (`In [n]` / `Out[n]`) so browser readers can inspect outputs immediately, while `.ipynb` code cells start in a clean unexecuted state (`outputs: []`, `execution_count: null`) for hands-on Google Colab / JupyterLab execution.
