# Installation Guide

Drawlib is published on PyPI and can be installed using `uv` (recommended) or standard `pip`.

---

## Requirements

- **Python**: Version 3.11 or higher.
- **Operating System**: Linux, macOS, or Windows.

---

## 1. Using `uv` (Recommended)

Add Drawlib to your current project dependencies:

```bash
# Add to active project
$ uv add drawlib

# Verify installation and CLI version
$ uv run drawlib --version
```

### Standalone CLI Execution (`uvx`)
If you want to run the Drawlib CLI tool without adding it to a project:

```bash
$ uvx drawlib --version
$ uvx drawlib init site
```

---

## 2. Using `pip`

Install Drawlib into your virtual environment:

```bash
$ pip install drawlib

# Verify installation
$ drawlib --version
```

---

## 3. Optional PDF Export Support

Drawlib includes built-in support for compiling Markdown documents into standalone PDF publications via headless Chromium.

To enable PDF generation (`drawlib build pdf`):

```bash
# When using uv:
$ uv add "drawlib[pdf]"
$ uv run playwright install chromium

# When using pip:
$ pip install "drawlib[pdf]"
$ playwright install chromium
```

---

## 4. On-Demand Asset Downloads

To maintain a minimal PyPI package size, high-resolution icon sets (Phosphor, FontAwesome, and official Google Cloud icons) and multilingual fonts are downloaded on demand upon first use and cached in your user data directory (`~/.drawlib/` or platform equivalent).

To pre-fetch and warm the cache ahead of time (e.g. for offline builds or CI/CD pipelines):

```bash
# Warm asset caches
$ uv run drawlib cache update
```

---

## 5. Verifying Installation

Verify that the Drawlib CLI commands and rule guides are accessible:

```bash
$ uv run drawlib --help
$ uv run drawlib rules list
```
