# Drawlib Jupyter & Google Colab Notebook Guidelines (`project-jupyter`)

A **`jupyter` project** (`drawlib init project jupyter`) compiles Markdown notebook sources (`jupyter_src/<lang>/**/*.md`) into a **unified notebook & HTML preview bundle (`jupyter_jupyter/` or `jupyter_html/`)** containing **interactive Jupyter Notebooks (`<lang>/**/*.ipynb`)**, a **notebook-styled HTML preview website (`<lang>/**/*.html` + root `index.html`)**, and **shared diagram assets (`images/`)** side-by-side—ready to serve directly from any custom domain or GitHub repository.

Every compiled notebook and HTML page supports:
- **In-Process AI Dry-Run Execution (`execute = true` / `--dry-run`)**: Sequentially executes all `code` cells in a shared `globals` dictionary per notebook, capturing `stdout`, final expression `text/plain` values, rendered `image/png` (`show()` / `save()`) outputs, and failing immediately on any unhandled exception or `[Geometry Warning]`.
- **Dual Code Block Semantics (`cell=markdown` vs. `cell=code`)**: Author rendered architectural diagrams inside Markdown narrative cells (` ```drawlib `) alongside live, user-editable executable Python code cells (` ```python ` or ` ```drawlib cell=code `).
- **One-Click Google Colab Integration (`Open in Colab`)**: Automatically injects an **Open in Colab** badge and `!pip install -q drawlib` setup cell when `colab_base_url` (or `setup_packages`) is configured under `[jupyter]` in `drawlib.toml`.
- **Deterministic Interactive Path Resolution (`setup(..., cwd=True)`)**: Resolves relative file paths (`save()`, `image()`, `Dimage()`) deterministically against `os.getcwd()` inside interactive Jupyter and Colab kernels without fragile stack-frame heuristics.

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For the 3-Stage Review & Self-Correction Loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. Dual Code Block Semantics (` ```drawlib ` vs. ` ```python `)

Inside `jupyter_src/<lang>/**/*.md`, Markdown prose and headings (`# H1`, `## H2`) become `.ipynb` `markdown` cells, while fenced code blocks are routed according to their fence language and `cell=` option:

| Fence Syntax in `.md` Source | Compiled `.ipynb` Cell Type | Compiled HTML Preview Output | Primary Use Case |
| :--- | :--- | :--- | :--- |
| ```` ```drawlib file=arch.png caption="..." ````<br>*(default `cell=markdown`)* | **`markdown` cell** containing the rendered diagram (`attachment:<file>.png`, `[seo].site_url` URL, or relative path) | Rendered `<figure>` diagram with optional `<details>` source fold (`code=fold`) | Explanatory architecture, flow, sequence, or concept diagrams accompanying narrative text. |
| ```` ```drawlib cell=code file=exercise.png ````<br>*(or `[jupyter].drawlib_cell_mode = "code"`)* | Clean unexecuted **`code` cell** (`outputs: []`) with `save(...)` rewritten to `show()` | Notebook `In [n]:` code cell + `Out[n]:` rendered figure | Hands-on Drawlib coding exercises where learners modify coordinates/styles and run the cell in Jupyter/Colab. |
| ```` ```python ````<br>*(default `cell=code`)* | Clean unexecuted **`code` cell** (`outputs: []`) ready for interactive execution | Notebook `In [n]:` code cell + `Out[n]:` execution output | Live Python data preparation, state sharing across cells, or calling Drawlib APIs directly. |
| ```` ```python cell=markdown ```` | **`markdown` cell** containing a static syntax-highlighted Python snippet | Standard static code block (not executed) | Non-executable reference pseudocode or configuration snippets. |

```drawlib align=center code=fold file=project_jupyter_pipeline.png caption="Jupyter & Google Colab Compilation Pipeline and AI Dry-Run Engine"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=156, height=58, dpi=150)

rectangle((78, 29), width=150, height=52, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (78, 49.5),
    "Illustrated Notebook as Code: Markdown Source -> AI Dry-Run -> Unified .ipynb & HTML Bundle",
    style=Styles.DarkBold.patch(text_size=12.0),
)

# Stage 1: Markdown Source
rectangle((28, 25), width=40, height=32, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_md((14.5, 35.5), width=4.5, style=Styles.PrimaryBold)
text((30.5, 35.5), "1. Markdown Source", style=Styles.DarkBold.patch(text_size=10.8))
text(
    (28, 21.5),
    "jupyter_src/<lang>/*.md\n• Narrative + ```drawlib\n• Executable ```python\n• Shared styles.py",
    style=Styles.Dark.patch(text_size=9.8),
)

line((48.5, 25), (56.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 2: In-Process AI Dry-Run Engine
rectangle((78, 25), width=42, height=32, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.play_circle((63.5, 35.5), width=4.5, style=Styles.WhiteBold)
text((80.5, 35.5), "2. AI Dry-Run Engine", style=Styles.WhiteBold.patch(text_size=10.8))
text(
    (78, 21.5),
    "Sequential shared globals\n• Captures stdout & expr\n• Captures show() / save()\n• Fails on Geometry Warn",
    style=Styles.White.patch(text_size=9.8),
)

line((99.5, 25), (107.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 3: Bundled Output Directory (jupyter_jupyter/ or jupyter_html/)
rectangle((128, 25), width=40, height=32, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.folder_open((113.5, 35.5), width=4.5, style=Styles.PrimaryBold)
text((130.5, 35.5), "3. Unified Web Bundle", style=Styles.DarkBold.patch(text_size=10.8))
text(
    (128, 21.5),
    "jupyter_jupyter/<lang>/\n• *.ipynb (Colab/Jupyter)\n• *.html (In[n]/Out[n])\n• ../images/ (Shared PNG)",
    style=Styles.Dark.patch(text_size=9.8),
)

save()
```

---

## 2. Deterministic Path Resolution in Notebooks (`setup(..., cwd=True)`)

In standard `.py` scripts, `setup(width=..., height=...)` defaults to `cwd=False`, resolving relative paths (`save("chart.png")`, `image("logo.png")`, `Dimage("photo.png")`) relative to the directory of the calling Python script.

In interactive **JupyterLab** or **Google Colab** notebooks, code cells execute inside a temporary kernel frame rather than a file on disk. To make relative path resolution 100% deterministic without fragile call-stack guessing, pass **`cwd=True`** to `setup()`:

```python
from drawlib.canvas import save, setup, show
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# Deterministically resolve all relative paths (save(), image(), Dimage()) against os.getcwd():
setup(width=100, height=40, cwd=True)
rectangle((50, 20), width=70, height=22, style=Styles.PrimaryNeutral, text="Notebook Cell")
show()  # Displays inline in Jupyter/Colab and is captured by drawlib build jupyter
```

- When `setup(..., cwd=True)` is active:
  - `save("out.png")` writes to `<os.getcwd()>/out.png`.
  - `save()` with no filename writes to `<os.getcwd()>/output.png`.
  - `image("data/pic.png")` and `Dimage("data/pic.png")` read from `<os.getcwd()>/data/pic.png`.
- Calling `clear()` resets `cwd` back to `False`.

---

## 3. Project Structure & `[jupyter]` Configuration in `drawlib.toml`

Scaffold a new `jupyter` project (single-locale or multi-locale `-l en,ja`) with:

```bash
uv run drawlib init project jupyter [target] [-l <lang[,lang...]>] [-s <style>]
```

```text
jupyter_src/
├── drawlib.toml               # [MANDATORY] Project manifest (type = "jupyter", [i18n], [jupyter])
├── en/                        # Locale notebook source directory (e.g. en/, ja/)
│   ├── 01_sample_notebook.md  # Notebook 1: Markdown narrative + drawlib + python cells
│   └── README.md              # Authoring guide (excluded from notebook compilation)
├── _assets/                   # Static images/logos copied to output _assets/
├── styles.py                  # Shared Drawlib Style / Color overrides
├── utils.py                   # Reusable Python helpers imported across notebooks
├── style.css                  # Notebook HTML preview stylesheet (includes In[n]/Out[n] cells)
├── template.html              # 2-column HTML preview layout with Open in Colab & .ipynb download bar
├── build.sh                   # Master build script (compiles bundled .ipynb + HTML into jupyter_jupyter/)
├── build_jupyter.sh           # Compile bundled .ipynb + HTML preview (jupyter_jupyter/)
├── build_html.sh              # Alias for building bundled .ipynb + HTML preview (jupyter_jupyter/)
└── serve.sh                   # Local HTTP preview server (drawlib serve jupyter_jupyter/)
```

Both `drawlib build jupyter` and `drawlib build html` on a `jupyter` project output **`.ipynb` notebooks and `.html` preview pages side-by-side** in the same output directory (`<out_dir>/<lang>/*.ipynb` and `<out_dir>/<lang>/*.html` + `<out_dir>/images/`), so deploying the output directory to any web host or custom domain serves both the HTML preview and downloadable `.ipynb` files without requiring GitHub.

### 3.1. `[jupyter]` Manifest Options (`drawlib.toml`)

```toml
[project]
name = "jupyter"
type = "jupyter"
title = ""
description = "Interactive Jupyter & Google Colab notebooks with Drawlib diagrams."
style = "google"

[i18n]
default_lang = "en"
langs = ["en", "ja"]

[jupyter]
# colab_base_url = "https://colab.research.google.com/github/owner/repo/blob/main/jupyter_jupyter"
setup_packages = ["drawlib"]         # Prepends an auto-generated `!pip install -q drawlib` cell when non-empty
drawlib_cell_mode = "markdown"       # Default for ```drawlib fences: "markdown" | "code"
image_mode = "attachment"            # "attachment" (self-contained .ipynb) | "url" ([seo].site_url) | "relative"
execute = true                       # Sequentially dry-run all code cells during build and render Out[n] in HTML preview
```

- **Configuring `colab_base_url`**:
  - **Base URL Prefix**: When set to a prefix URL such as `"https://colab.research.google.com/github/owner/repo/blob/main/docs/jupyter"`, Drawlib automatically appends `/<lang>/<stem>.ipynb`.
  - **`{path}` URL Template (Non-GitHub / Custom Colab)**: Include `{path}` (e.g. `"https://colab.example.com/open?notebook={path}"`) to substitute `<lang>/<stem>.ipynb` anywhere in the URL.
  - Leave empty (`""`) when serving exclusively from a custom domain without Google Colab (the **⬇ Download .ipynb** button remains active on all HTML pages).
- **Choosing `image_mode`**:
  - `"attachment"` *(default)*: Embeds rendered `cell=markdown` diagrams directly into `.ipynb` Markdown cell `attachments` (`attachment:<file>.png`) as base64 data so every `.ipynb` file is 100% self-contained when downloaded or uploaded to Google Colab.
  - `"url"`: Rewrites image URLs in `.ipynb` Markdown cells to `<[seo].site_url>/images/<stem>/<file>.png`—ideal when hosting the output directory on a public domain (or GitHub Pages) to keep `.ipynb` file sizes small and Git diffs clean without depending on GitHub raw URLs.
  - `"relative"`: Uses relative `../images/<stem>/<file>.png` links for local JupyterLab workspaces where `images/` sits alongside `<lang>/*.ipynb`.

---

## 4. Autonomous AI Dry-Run & Verification Workflow

Never deliver an untested notebook. `drawlib build jupyter` includes a built-in **AI Dry-Run Engine** that executes every notebook top-to-bottom in-process:

```bash
# 1. Fast AI Dry-Run verification (executes all cells, checks [Geometry Warning], writes no files):
uv run drawlib build jupyter jupyter_src/ --dry-run

# 2. Full build (bundled .ipynb notebooks + HTML preview site in jupyter_jupyter/):
./jupyter_src/build.sh

# 3. Link & asset integrity check on the compiled site:
uv run drawlib serve jupyter_jupyter/ --check
```

### What the Dry-Run Engine Verifies Automatically:
1. **Shared State Across Cells**: Cell 1's variables, functions, and imports are live in Cell 2, Cell 3, etc., matching real Jupyter/Colab kernel behavior (`styles.py` and `utils.py` are pre-loaded into the notebook namespace).
2. **Zero Unhandled Exceptions**: Any `SyntaxError`, `NameError`, `TypeError`, or Drawlib validation error halts the build and reports the exact notebook path, cell number (`In [n]`), and traceback.
3. **Zero `[Geometry Warning]`**: Any canvas clipping, out-of-bounds artist, or overlap warning emitted during either `cell=markdown` diagram rendering or `cell=code` execution fails the dry-run (`NotebookExecutionError`).
4. **HTML-Only Execution Outputs (`.ipynb` Kept Clean)**: Standard output (`print(...)`), final cell expressions, and `show()` / `save()` figures are rendered into the HTML preview page (`In [n]` / `Out[n]`), while `.ipynb` code cells remain clean and unexecuted (`outputs: []`, `execution_count: null`) for hands-on Colab/Jupyter execution.
