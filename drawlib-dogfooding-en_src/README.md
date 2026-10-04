# Drawlib Document Project (doc)

This directory contains multi-chapter documents compiled into **HTML, PDF, Markdown, and standalone images** using Drawlib.

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
  - `build.sh`: Master build script to compile all targets (HTML, PDF, Markdown, Images).
  - `build_html.sh`: Build standalone HTML document.
  - `build_pdf.sh`: Build vector PDF report.
  - `build_markdown.sh`: Build GitHub-browsable Markdown.
  - `build_image.sh`: Extract embedded diagram images.
  - `serve.sh`: Local preview web server for generated HTML.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `style.css`: Document stylesheet.
  - `template.html`: Jinja2 HTML layout used for HTML / PDF rendering.
  - `README.md`: This customization guide.
  - `00_cover.md`: Cover page.
  - `01_ai_challenges.md`: Chapter Markdown files.
- `drawlib-dogfooding-en_html/`: Generated HTML document (**Do not edit directly**).
- `drawlib-dogfooding-en.pdf`: Generated PDF document (**Do not edit directly**).
- `drawlib-dogfooding-en_markdown/`: Generated Markdown document (**Do not edit directly**).
- `drawlib-dogfooding-en_images/`: Extracted standalone diagram images (**Do not edit directly**).

---

## 2. Building

### Using the Build Scripts
Run the desired build script from the project root or inside this directory:
```bash
./build_html.sh       # Generate standalone HTML document (drawlib-dogfooding-en_html/)
./build_pdf.sh        # Generate vector PDF report (drawlib-dogfooding-en.pdf)
./build_markdown.sh   # Generate GitHub-browsable Markdown (drawlib-dogfooding-en_markdown/)
./build_image.sh      # Extract embedded diagram images (drawlib-dogfooding-en_images/)
./build.sh            # Build all targets above sequentially
```

### Starting the Preview Server
```bash
./serve.sh            # Preview at http://localhost:8000
```

### Using the Drawlib CLI Directly
```bash
drawlib build html drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en_html/
drawlib build pdf drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en.pdf --generate-index
drawlib build markdown drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en_markdown/
drawlib build image drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en_images/
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
drawlib show drawlib-dogfooding-en_src/01_ai_challenges.md 1 -g -o preview.png
```
Rebuild without cache:
```bash
drawlib build pdf drawlib-dogfooding-en_src/ -o drawlib-dogfooding-en.pdf --no-cache
```
