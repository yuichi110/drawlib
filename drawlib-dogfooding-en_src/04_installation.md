# Chapter 4: Installation Guide

Drawlib is packaged as a pure-Python library and managed with `uv`.

## 4.1 Prerequisites

- **Python**: Version 3.11 or higher.
- **Package Manager**: [uv](https://github.com/astral-sh/uv) is highly recommended for speed and deterministic virtual environments.

## 4.2 Standard Installation (CLI & Standalone Drawing)

To install Drawlib directly from the official Git repository into your project:

```bash
uv add "drawlib @ git+https://github.com/yuichi110/drawlib.git"
```

## 4.3 PDF Compilation Installation (Full Documentation Suite)

To build publication-ready PDF documents via headless Chromium, install Drawlib with the `[pdf]` extra and install the Chromium browser binary:

```bash
# 1. Install Drawlib with PDF dependencies (Playwright)
uv add "drawlib[pdf] @ git+https://github.com/yuichi110/drawlib.git"

# 2. Install the Playwright Chromium binary
uv run playwright install chromium
```

## 4.4 Verification

Verify that the Drawlib CLI is properly installed:

```bash
uv run drawlib --version
```
