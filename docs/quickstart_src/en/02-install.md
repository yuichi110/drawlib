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
# Output: 0.3.2

# Or execute via Python module launcher
python3 -m drawlib --version
```

## Built-in PDF, Office & Image Export

A standard `uv add drawlib` or `pip install drawlib` installation includes every output engine out of the box—no optional `[pdf]` package extras or manual browser setup steps are needed:

- **Raster & Vector Images (PNG, WebP, SVG)**: Supported out of the box via Pillow and Matplotlib backends.
- **Headless PDF & 16:9 PowerPoint (`drawlib build pdf`, `drawlib build pptx`)**: Drawlib uses Playwright with headless Chromium to compile print-ready vector PDFs and measure 16:9 slide layouts for editable `.pptx` decks. On your first PDF or PPTX build, Drawlib **automatically downloads and caches** headless Chromium.
- **Editable MS Word (`drawlib build docx`)**: Generates editable `.docx` technical specifications directly in pure Python without requiring a browser.
- **Offline / CI Pre-fetching & Minimal Linux Containers**: Pre-download all fonts, icons, maps, and headless Chromium ahead of time for air-gapped CI runners via `uv run drawlib cache download --all` (or `uv run drawlib cache download --browser` for Chromium only). On minimal Linux Docker containers missing OS shared libraries, install system packages once with:
  ```bash
  uv run playwright install-deps chromium
  ```
- **Universal Typography**: Drawlib automatically fetches and caches CJK-ready Google Noto Sans and Roboto fonts, ensuring Chinese, Japanese, Korean, and Latin typography renders consistently across Linux, macOS, and Windows without missing glyph boxes (`tofu`).

```drawlib align=center file=install_toolchain.png caption="Figure 2.1: Drawlib Environment & Toolchain Architecture"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=48)

layers = [
    (19.5, phosphor.terminal, "Dev Environment", "Python 3.11+\nuv / pip / git", Styles.Neutral, Styles.Primary, Styles.DarkBold, Styles.Dark),
    (51.8, phosphor.package, "Drawlib Core", "Shapes, Icons\nSmartArts, Charts", Styles.PrimaryNeutral, Styles.Primary, Styles.DarkBold, Styles.Dark),
    (84.2, phosphor.gear, "Build Engine", "Auto Chromium\nSQLite Cache", Styles.SecondaryNeutral, Styles.Secondary, Styles.DarkBold, Styles.Dark),
    (116.5, phosphor.file_arrow_down, "Built-in Outputs", "HTML / MD / PNG\nPDF / DOCX / PPTX", Styles.PrimaryFlat, Styles.White, Styles.WhiteBold, Styles.White),
]

for idx, (x, icon_fn, title, desc, card_st, icon_st, title_st, desc_st) in enumerate(layers):
    rectangle(xy=(x, 24), width=27, height=38, style=card_st.patch(shape_r=2.5))
    icon_fn(xy=(x, 36), width=5.5, style=icon_st)
    text(xy=(x, 26.5), text=title, style=title_st.patch(text_size=10.5))
    text(xy=(x, 14), text=desc, style=desc_st.patch(text_size=10.0))
    if idx < len(layers) - 1:
        next_x = layers[idx + 1][0]
        line((x + 13.5, 24), (next_x - 13.5, 24), arrow_head="->", style=Styles.DarkBold)

save()
```
