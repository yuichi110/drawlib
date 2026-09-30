# 2. Installation & Environment Setup

Drawlib is a modern, pure-Python library requiring **Python 3.11 or higher**. It integrates seamlessly with modern Python tooling like `uv` or standard `pip`.

## Package Installation

```bash
# Recommended: Using uv (fast, isolated virtual environment)
uv add drawlib

# Or using standard pip
pip install drawlib
```

## Verifying the Installation

After installation, verify that both the Python library and the CLI tool are accessible:

```bash
# Check installed CLI version
uv run drawlib --version
# Output: Drawlib version: 0.2.0

# Or execute via Python module launcher
python3 -m drawlib --version
```

## System Dependencies for PDF & Image Export

- **Raster Image Output (PNG, WebP)**: Supported out of the box via Pillow and Matplotlib backends.
- **Headless PDF Compilation (`drawlib build pdf`)**: Drawlib uses Playwright with headless Chromium to render HTML and CSS print stylesheets into high-fidelity PDF documents:
  ```bash
  # Install Playwright browser binaries for PDF builds
  uv run playwright install chromium
  ```
- **Universal Typography**: Drawlib bundles CJK-ready Google Noto Sans and Roboto fonts, ensuring Chinese, Japanese, Korean, and Latin typography renders consistently across Linux, macOS, and Windows without missing glyph boxes (`tofu`).

```drawlib 620px center caption:"Figure 2.1: Drawlib Environment & Toolchain Architecture"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

layers = [
    (18, phosphor.terminal, "Developer Environment", "Python 3.11+\nuv / pip / git", Styles.primary_flat),
    (52, phosphor.package, "Drawlib Core", "Prims, Styles, Icons\nSmartArts, Diagrams", Styles.secondary_flat),
    (86, phosphor.gear, "Compilation Engine", "HTML Builder\nPlaywright PDF\nSQLite Cache", Styles.accent_flat),
    (110, phosphor.file_arrow_down, "Outputs", "PNG / WebP\nHTML Site\nPrint PDF", Styles.success_flat),
]

for idx, (x, icon_fn, title, desc, st) in enumerate(layers):
    rectangle(xy=(x, 22), width=22, height=36, r=2.5, style=Styles.muted_dashed)
    icon_fn(xy=(x, 34), width=6, style=st)
    text(xy=(x, 26), text=title, style=Styles.bold, size=8)
    text(xy=(x, 14), text=desc, style=Styles.primary, size=7)
    if idx < len(layers) - 1:
        next_x = layers[idx + 1][0]
        line((x + 11, 22), (next_x - 11, 22), arrowhead="->", style=Styles.bold)
```
