# Drawlib PDF Report Project

This directory contains multi-chapter documents compiled into a unified, print-ready vector PDF report using Drawlib and headless Chromium.

> [!TIP]
> **Need Comprehensive Rules & Deep Guides?**  
> For complete architectural guidelines, drawing syntax, and developer APIs, run:
> - `uv run drawlib rules show overview` : Full drawing manual & workflow feedback loop
> - `uv run drawlib rules show styles`    : Dynamic theming, `styles.py`, and `utils.py`
> - `uv run drawlib rules show docs_build`: Document structure, PDF options & cover pages
> - `uv run drawlib rules list`          : List all available rule topics

---

## 1. Directory Structure

- `drawlib-dogfooding-en_src/`: Source Markdown chapters and drawing code (**Source of Truth**).
  - `build.sh`: Build script to compile chapters into a single PDF document.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `style.css`: PDF report print stylesheet (paged media, `@page` rules).
  - `template.html`: Jinja2 HTML layout used for PDF rendering.
  - `README.md`: This customization guide.
  - `00_cover.md`: Report title/cover page.
  - `01_overview.md`: Overview chapter.
  - `02_design.md`: Technical design chapter.
- `drawlib-dogfooding-en.pdf`: Generated PDF document (**Do not edit directly**).

---

## 2. Building PDF

### Using the Build Script
Run the automated build script from the project root or inside this directory:
```bash
./build.sh
```

### Using the Drawlib CLI Directly
```bash
# Compile chapters into a unified PDF report with table of contents
drawlib build pdf drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en.pdf --generate-index
```

---

## 3. Customization Guide

### 3.1. Themes & Global Styles (`styles.py`)
Configure drawing styles, color palettes, and fonts for all embedded illustrations:
```python
from drawlib.fonts import FontRoboto
from drawlib.styles import Styles

Styles = Styles.patch_font(
    regular=FontRoboto.REGULAR,
    bold=FontRoboto.BOLD,
)
```

### 3.2. Reusable Helpers & Macros (`utils.py`)
Define reusable drawing functions and constants in `utils.py`:
```python
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

REPORT_VERSION = "v1.0.0"

def chapter_banner(xy: tuple[float, float], title: str) -> None:
    rectangle(xy, width=100, height=12, style=Styles.BlueFlat)
    text(xy, title, style=Styles.WhiteBold)
```
Consume inside embedded ````drawlib```` blocks:
```python
from drawlib.utils import REPORT_VERSION, chapter_banner
chapter_banner((60, 20), f"System Design ({REPORT_VERSION})")
```

### 3.3. Document Flow & Chapters
- Files are compiled in alphabetical order by filename (`00_cover.md`, `01_overview.md`, etc.).
- Use page breaks where needed via `<div class="page-break"></div>` or CSS `page-break-before: always;`.
- The `--generate-index` option automatically injects a Table of Contents based on your Markdown headings.

### 3.4. Paged Media Styles (`style.css` & `template.html`)
- **`style.css`**: Configure `@page` rules (margins, page orientation, headers, footers):
  ```css
  @page {
      size: A4 portrait;
      margin: 20mm 15mm;
  }
  ```
- **`template.html`**: Customize document structure, header/footer branding, and page number displays.

### 3.5. Fast Developer Verification
Test individual drawing blocks with alignment grid (`-g`):
```bash
drawlib export drawlib-dogfooding-en_src/01_overview.md 1 -g -o preview.png
```
Rebuild without cache:
```bash
drawlib build pdf drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en.pdf --no-cache
```
