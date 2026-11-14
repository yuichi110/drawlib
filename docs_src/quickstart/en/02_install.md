# 2. Installation & Zero-Config Toolchain

Drawlib `v0.3.10` is packaged as a self-contained pure-Python toolchain for **Python `3.11+` (`3.11`, `3.12`, `3.13`, and `3.14`)** across Linux, macOS, and Windows—requiring zero external Graphviz binaries, LaTeX distributions, or Node.js bundlers.

Whether you are adding visual documentation to an existing Python package with `uv add drawlib` or authoring architecture specs inside a Go, Rust, TypeScript, or Java repository via zero-install `uvx drawlib`, the identical CLI and asset cache work out of the box.

```drawlib align=center code=fold file=install_workflows.png caption="Figure 2.1: Two Execution Workflows — Project Dependency (uv add) vs. Zero-Install Polyglot Runner (uvx)"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=148, height=62)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.8),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

g_py = d.add(
    NodeGroup(
        title="1. Python Project Repo (uv add)",
        width=50.0,
        height=23.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(3.0, 31.0),
)
g_py.add(
    Node(
        "pyproject.toml + .venv\nuv run drawlib ...",
        width=44.0,
        height=12.0,
        icon=PhosphorIcon.PACKAGE,
        icon_size=5.0,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(25.0, 8.8),
)

g_uvx = d.add(
    NodeGroup(
        title="2. Polyglot / Docs Repo (uvx)",
        width=50.0,
        height=23.0,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(3.0, 4.0),
)
g_uvx.add(
    Node(
        "Go / Rust / TS / Java\nuvx drawlib ... (Zero Config)",
        width=44.0,
        height=12.0,
        icon=PhosphorIcon.TERMINAL_WINDOW,
        icon_size=5.0,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(25.0, 8.8),
)

cli_node = d.add(
    Node(
        "Drawlib v0.3.10\nCLI & Compiler",
        width=31.0,
        height=20.0,
        icon=PhosphorIcon.CPU,
        icon_size=5.8,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=11.2),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(78.5, 29.0),
)

cache_node = d.add(
    Node(
        "Auto Asset Cache\n(Fonts / Icons / Chromium)",
        width=39.0,
        height=15.0,
        icon=PhosphorIcon.DATABASE,
        icon_size=5.0,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(122.5, 42.5),
)

out_node = d.add(
    Node(
        "Multi-Target Outputs\n(HTML / PDF / DOCX / PPTX)",
        width=39.0,
        height=15.0,
        icon=PhosphorIcon.EXPORT,
        icon_size=5.0,
        card_style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    ),
    xy=(122.5, 15.5),
)

j_in_top = d.junction((58.0, 42.5))
j_in_mid = d.junction((58.0, 29.0))
j_in_bot = d.junction((58.0, 15.5))
d.connect(g_py, j_in_top, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(g_uvx, j_in_bot, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_in_top, j_in_mid, arrow="-", routing="direct")
d.connect(j_in_bot, j_in_mid, arrow="-", routing="direct")
d.connect(j_in_mid, cli_node, arrow="->", routing="direct", padding=(0.0, 0.8))

j_out_mid = d.junction((98.5, 29.0))
j_out_top = d.junction((98.5, 42.5))
j_out_bot = d.junction((98.5, 15.5))
d.connect(cli_node, j_out_mid, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_out_mid, j_out_top, arrow="-", routing="direct")
d.connect(j_out_mid, j_out_bot, arrow="-", routing="direct")
d.connect(j_out_top, cache_node, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_out_bot, out_node, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(2.0, 2.0))
save()
```

---

## 2.1 System Requirements & Execution Modes

Drawlib targets modern CPython releases and pairs naturally with Astral's `uv` package manager for deterministic lockfiles and instant CLI execution:

| Requirement | Supported Specification | Notes |
| :--- | :--- | :--- |
| **Python Runtime** | **Python `3.11+` (`3.11`, `3.12`, `3.13`, `3.14`)** | Verified across Linux (`x86_64` / `aarch64`), macOS, and Windows |
| **Recommended Runner** | **`uv` (`uv add` / `uv run` / `uvx`)** | Instant virtual environments and zero-install polyglot execution |
| **Standard Fallback** | **`pip` (`venv` + `pip install drawlib`)** | Standard PyPI wheel installation without optional extra flags |

### 2.1.1 Workflow 1: Python Project Dependency (`uv add drawlib`)

For Python services, data science repositories, or dedicated documentation repos where you want `drawlib` pinned inside `pyproject.toml` and `uv.lock`:

```bash
# Initialize a new uv project (or run inside an existing Python repository)
uv init my_project
uv add drawlib
uv run drawlib --version

# Standard pip + venv fallback when uv is unavailable
python3 -m venv .venv
.venv/bin/pip install drawlib
.venv/bin/drawlib --version
```

Pinning `drawlib` in `pyproject.toml` gives IDEs (`Pyright`, `Pylance`, `Ruff`) full autocomplete and static type checking across `drawlib.shapes`, `drawlib.smartarts`, `drawlib.charts`, and `drawlib.diagrams`, while guaranteeing reproducible CI builds via `uv sync --frozen`.

### 2.1.2 Workflow 2: Zero-Install Polyglot Runner (`uvx drawlib`)

For **Go, Rust, TypeScript, Java, C++, or pure Markdown repositories**, you do not need to pollute the repository root with a `pyproject.toml` or `.venv/` folder. Prefix any CLI command with `uvx` to run Drawlib inside an isolated, automatically cached tool environment:

```bash
# Verify Drawlib immediately with zero local Python configuration
uvx drawlib --version

# Scaffold and build multi-locale documentation inside any Go / Rust / TS repo
uvx drawlib init project site docs -l en,ja -s google
uvx drawlib build html docs_src/ -o docs_html/
```

---

## 2.2 Built-In Batteries & Asset Caching

Unlike fragmented documentation stacks that require separate plugins for diagrams, Word exports, slide decks, and PDF printing, **`drawlib v0.3.10` ships with every rendering and publishing dependency built in**—no `drawlib[pdf]` or `drawlib[office]` extras required.

```drawlib align=center code=fold file=toolchain_batteries.png caption="Figure 2.2: Drawlib v0.3.10 Zero-Config Runtime Stack & Automated Cache Architecture"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import KpiCards
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=66)

rectangle((74.0, 56.5), width=136.0, height=8.6, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.package((13.5, 56.5), width=5.0, style=Styles.WhiteBold)
text(
    (18.5, 56.5),
    "drawlib v0.3.10 — Single PyPI Install, All Batteries Included (Python 3.11–3.14)",
    style=Styles.WhiteBold.patch(text_size=11.5, halign="left"),
)

stack = KpiCards(
    style=Styles.White.patch(shape_r=1.8),
    metric_style=Styles.DarkBold.patch(text_size=13.0),
    text_style=Styles.DarkBold.patch(text_size=11.2),
    description_style=Styles.Dark.patch(text_size=10.0),
    accent_style=Styles.Neutral,
    icon_style=Styles.PrimaryBold,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.23,
    spacing=3.5,
)
stack.add(
    "Core",
    "Declarative Python API",
    "Shapes, 18 SmartArts, 10 Charts,\n6 Diagrams & 5 Graph Solvers",
    icon=phosphor.code,
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
)
stack.add(
    "Pillow",
    "Raster & Animation Engine",
    "Crisp PNG/WebP output, Dimage\ntransforms & APNG/GIF frames",
    icon=phosphor.images,
    style=Styles.Neutral.patch(shape_r=1.8),
)
stack.add(
    "Cache",
    "Google/CJK Fonts & Icons",
    "Auto-cached Noto CJK fonts, 34 icon\nsuites & SQLite .drawlib/cache.db",
    icon=phosphor.database,
    style=Styles.Neutral.patch(shape_r=1.8),
)
stack.add(
    "Export",
    "Chromium & Office Exporters",
    "Auto-downloaded Playwright Chromium\n+ python-docx & python-pptx",
    icon=phosphor.file_pdf,
    style=Styles.SecondaryNeutral.patch(shape_r=1.8),
)
stack.draw((6.0, 5.5), width=136.0, height=43.0, columns=2)

save()
```

Every `pip install drawlib` or `uv add drawlib` installation provisions four integrated subsystems:

- **Pillow Raster & Animation Engine (`pillow`)**: Powers high-DPI `PNG` and `WebP` rasterization, `Dimage` cropping/compositing transforms, and multi-frame animation encoding (`APNG`, animated `WebP`, and `GIF`) alongside Drawlib's vector geometry renderer.
- **Playwright Headless Chromium (`playwright`)**: Bundled as a standard dependency for pixel-accurate vector `PDF` (`drawlib build pdf`) and `16:9` slide rendering (`drawlib build pptx`). On your first PDF or PPTX build, Drawlib automatically downloads `chromium-headless-shell` with zero manual setup.
- **Native Microsoft Office Builders (`python-docx` & `python-pptx`)**: Compiles linear `doc` projects into editable `.docx` specifications and `16:9` `slide` decks into editable `.pptx` presentations out of the box.
- **On-Demand Font, Icon & SQLite Build Caches**: Standardized Google Fonts, **Noto Sans CJK** multilingual fonts (eliminating tofu boxes across Linux/macOS/Windows), and all 34 icon suites download automatically on first use, while `.drawlib/cache.db` hashes rendered blocks so unchanged diagrams skip re-execution.

For offline environments, air-gapped runners, or minimal Docker CI images (such as `python:3.12-slim`), pre-warm the asset cache ahead of time:

```bash
# Inspect local font, icon, map, and browser cache status
uv run drawlib cache list

# Pre-download all fonts (including CJK), 34 icon suites, maps & headless Chromium
uv run drawlib cache download --all

# Pre-download only headless Chromium for PDF / PPTX builds
uv run drawlib cache download --browser

# On minimal Linux CI containers missing OS shared libs (libnss3, libgbm1, etc.)
uv run playwright install-deps chromium
```

---

## 2.3 Quick-Test Project Scaffolding

Never hand-craft bare `.py` files or ad-hoc folders from scratch—always start with `drawlib init project` so `drawlib.toml`, `styles.py`, `utils.py`, `_assets/`, and modular `build*.sh` scripts are configured cleanly:

```bash
# 1. Confirm CLI version
uv run drawlib --version

# 2. Scaffold a bilingual (en + ja) linear document project with the Google theme
uv run drawlib init project doc my_docs -l en,ja -s google

# 3. Compile HTML, vector PDFs, GitHub Markdown, and extracted images
./my_docs_src/build.sh
```

Running `drawlib init project doc my_docs -l en,ja -s google` creates `my_docs_src/` containing `drawlib.toml` (`[project]` + `[i18n]`), `styles.py` (`GoogleStyles`), `ja/styles.py` (`FontJapanese` override), `utils.py`, `_assets/`, starter chapters under `en/` and `ja/`, and ready-to-run build scripts (`build.sh`, `build_html.sh`, `build_pdf.sh`, `build_docx.sh`, and `serve.sh`).
