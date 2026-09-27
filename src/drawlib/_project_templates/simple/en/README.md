# Drawlib Simple Document

This directory contains a single Markdown document with embedded Drawlib illustrations, compilable into standalone HTML and GitHub-ready Markdown.

> [!TIP]
> **Need Comprehensive Rules & Deep Guides?**  
> For complete architectural guidelines, drawing syntax, and developer APIs, run:
> - `uv run drawlib rules show overview` : Full drawing manual & workflow feedback loop
> - `uv run drawlib rules show styles`    : Dynamic theming, `styles.py`, and `utils.py`
> - `uv run drawlib rules show cli`       : CLI commands & export options
> - `uv run drawlib rules list`          : List all available rule topics

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source Markdown document and illustrations (**Source of Truth**).
  - `build.sh`: Build script to compile documents into Markdown and HTML.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `style.css`: Custom CSS stylesheet for standalone HTML output.
  - `template.html`: Custom Jinja2 HTML layout template.
  - `README.md`: This customization guide.
  - `doc.md`: Sample document with embedded illustrations.
- `__OUT_DIR__/`: Compiled Markdown output (**Do not edit directly**).
- `__OUT_HTML_DIR__/`: Compiled HTML output (**Do not edit directly**).

---

## 2. Building Documents

### Using the Build Script
Run the automated build script from the project root or inside this directory:
```bash
./build.sh
```

### Using the Drawlib CLI Directly
```bash
# Compile to GitHub-friendly Markdown with relative image links
drawlib build markdown __SRC_DIR__/doc.md -o __OUT_DIR__/doc.md

# Compile to standalone HTML
drawlib build html __SRC_DIR__/doc.md -o __OUT_HTML_DIR__/doc.html
```

---

## 3. Customization Guide

### 3.1. Themes & Global Styles (`styles.py`)
Configure drawing styles, color palettes, and fonts for all embedded illustrations:
```python
from drawlib.fonts import FontRoboto
from drawlib.styles import styles

# Patch default fonts or themes
styles = styles.patch_font(
    regular=FontRoboto.REGULAR,
    bold=FontRoboto.BOLD,
)
```

### 3.2. Reusable Helpers & Macros (`utils.py`)
Define reusable drawing functions and constants in `utils.py`:
```python
from drawlib.shapes import rectangle
from drawlib.text import text

PROJECT_NAME = "System Architecture Document"

def node(xy: tuple[float, float], label: str) -> None:
    rectangle(xy, width=24, height=14, r=1, style="blue_flat")
    text(xy, label, style="white_bold")
```
Consume inside embedded ````drawlib```` blocks:
```python
from drawlib.utils import PROJECT_NAME, node
node((40, 20), "Core Engine")
```

### 3.3. Document & HTML Styling (`style.css` & `template.html`)
- **`style.css`**: Customize colors, margins, and typography of the generated HTML.
- **`template.html`**: Adjust the HTML wrapper, headers, footers, or embed custom CSS/JS.

### 3.4. Fast Developer Verification
Test individual drawing blocks with alignment grid (`-g`):
```bash
drawlib export __SRC_DIR__/doc.md 1 -g -o preview.png
```
Rebuild without cache:
```bash
drawlib build html __SRC_DIR__/doc.md -o __OUT_HTML_DIR__/doc.html --no-cache
```
