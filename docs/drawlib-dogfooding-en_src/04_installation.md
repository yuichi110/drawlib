# Chapter 4: Installation and Environment Setup

Drawlib (`v0.3.2`) is published on the official Python Package Index (PyPI) and can be installed in seconds using `uv` or `pip`.

## 4.1 Prerequisites

- **Python**: 3.11 or higher (supports Python 3.11, 3.12, and 3.13)
- **Operating Systems**: Linux, macOS, and Windows
- **Package Manager**: `uv` (recommended) or `pip`

## 4.2 Installing from PyPI (`uv` / `pip` / `uvx`)

A standard `drawlib` installation includes every output target out of the box—standalone diagrams, multi-page HTML sites, 16:9 HTML slide decks, GitHub Markdown, **vector PDF (`drawlib build pdf`)**, **editable MS Word (`drawlib build docx`)**, and **editable 16:9 MS PowerPoint (`drawlib build pptx`)**—with no optional package extras required:

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

## 4.3 Built-in PDF & Office (Word / PowerPoint) Export

Drawlib handles document and presentation compilation without manual browser installation steps:

- **Vector PDF & 16:9 PowerPoint (`drawlib build pdf`, `drawlib build pptx`)**:
  On the first `drawlib build pdf` or `drawlib build pptx` execution, Drawlib **automatically downloads and caches** a managed headless Chromium binary via Playwright—no manual browser setup is needed.
- **Editable MS Word (`drawlib build docx`)**:
  Runs in pure Python (`python-docx`) without requiring a browser, compiling `doc` projects directly into editable `.docx` documents (including `--generate-index` Table of Contents support).

> **Note (Minimal Linux Docker Containers)**:  
> On minimal Ubuntu or Debian container images where OS shared libraries required by Chromium are not pre-installed, install system dependencies once via:  
> `uv run playwright install-deps chromium`

## 4.4 Managing Asset & Build Caches (`drawlib cache`)

To keep the core PyPI package lightweight and builds fast, Drawlib uses a two-tier caching architecture:

1. **External Asset & Headless Browser Cache**:
   Multilingual fonts (Roboto, Noto Sans JP, etc.), vector icon packs (Phosphor, FontAwesome, official GCP icons), offline map geometry (`GeoMap`), and the headless Chromium browser for PDF / PPTX builds are automatically downloaded on demand upon first use and cached locally.
2. **Incremental Build Cache (`.drawlib/cache.db`)**:
   During `drawlib build` and `drawlib show`, Drawlib hashes each code block along with `styles.py`, `utils.py`, and referenced local assets in a SQLite database, skipping unchanged diagrams to make incremental rebuilds near-instantaneous.

Use the `drawlib cache` CLI to pre-download assets and headless Chromium for offline/air-gapped CI environments or clear cached artifacts:

```bash
# Inspect cached asset packages and status
uv run drawlib cache list

# Pre-download all assets (fonts, icons, maps, and headless Chromium) for offline or CI builds
uv run drawlib cache download --all
# Or download specific categories: --fonts / --icons / --maps / --browser

# Clear only the incremental image build cache (.drawlib/cache.db) to force re-rendering
uv run drawlib cache clear --images

# Clear both downloaded assets and the incremental build cache
uv run drawlib cache clear --all
```

## 4.5 Verifying the Installation

Once installed, verify that the CLI and project templates are available:

```bash
# Check installed version (0.3.2)
uv run drawlib --version

# List available project templates
uv run drawlib init list
```

When the four project archetypes—`doc`, `site`, `slide`, and `images`—are displayed, your environment is ready.
