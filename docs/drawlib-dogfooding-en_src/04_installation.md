# Chapter 4: Installation and Environment Setup

Drawlib (`v0.3.0`) is published on the official Python Package Index (PyPI) and can be installed in seconds using `uv` or `pip`.

## 4.1 Prerequisites

- **Python**: 3.11 or higher (supports Python 3.11, 3.12, and 3.13)
- **Operating Systems**: Linux, macOS, and Windows
- **Package Manager**: `uv` (recommended) or `pip`

## 4.2 Installing from PyPI (`uv` / `pip` / `uvx`)

For standard diagram rendering, multi-page HTML sites, slide decks, and Markdown builds, install `drawlib` directly from PyPI:

```bash
# Using uv (recommended)
uv add drawlib
uv run drawlib --version

# Run ephemerally without adding to a project (uvx)
uvx drawlib --version
uvx drawlib init site

# Using pip
pip install drawlib
```

## 4.3 Enabling PDF Export (Optional)

To export vector A4 PDFs in `doc` projects (technical specifications and whitepapers) or 16:9 PDFs in `slide` projects via headless Chromium (`playwright`), install the `[pdf]` extra and download the Chromium browser binary:

```bash
# 1. Install drawlib with the PDF extra
uv add "drawlib[pdf]"

# 2. Download the headless Chromium binary required for PDF rendering
uv run playwright install chromium
```

> **Note (Using `pip`)**:  
> Run `pip install "drawlib[pdf]"` followed by `playwright install chromium`.

> **Note (Linux Headless Servers & CI Containers)**:  
> On Ubuntu/Debian server environments where OS shared libraries may be missing, pass `--with-deps` when installing Chromium:  
> `uv run playwright install --with-deps chromium`

## 4.4 Managing Asset & Build Caches (`drawlib cache`)

To keep the core PyPI package lightweight and builds fast, Drawlib uses a two-tier caching architecture:

1. **External Asset Cache (`drawlib/_cached_assets/`)**:
   Multilingual fonts (Roboto, Noto Sans JP, etc.), vector icon packs (Phosphor, FontAwesome, official GCP icons), and offline map geometry (`GeoMap`) are automatically downloaded on demand from GitHub Releases upon first use and cached locally.
2. **Incremental Build Cache (`.drawlib/cache.db`)**:
   During `drawlib build` and `drawlib show`, Drawlib hashes each code block along with `styles.py`, `utils.py`, and referenced local assets in a SQLite database, skipping unchanged diagrams to make incremental rebuilds near-instantaneous.

Use the `drawlib cache` CLI to pre-download assets for offline/air-gapped CI environments or clear cached artifacts:

```bash
# Inspect cached asset packages and status
uv run drawlib cache list

# Pre-download all assets (fonts, icons, maps) for offline or CI builds
uv run drawlib cache download --all
# Or download specific categories: --fonts / --icons / --maps

# Clear only the incremental image build cache (.drawlib/cache.db) to force re-rendering
uv run drawlib cache clear --images

# Clear both downloaded assets and the incremental build cache
uv run drawlib cache clear --all
```

## 4.5 Verifying the Installation

Once installed, verify that the CLI and project templates are available:

```bash
# Check installed version (drawlib 0.3.0)
uv run drawlib --version

# List available project templates
uv run drawlib init list
```

When the four project archetypes—`doc`, `site`, `slide`, and `images`—are displayed, your environment is ready.
