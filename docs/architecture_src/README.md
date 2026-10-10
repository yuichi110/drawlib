# Drawlib Documentation Site

This directory contains the source Markdown files, drawing code, and configuration assets for a multi-page documentation website.

> [!TIP]
> **Need Comprehensive Rules & Deep Guides?**  
> For complete architectural guidelines, drawing syntax, and developer APIs, run:
> - `uv run drawlib rules show overview` : Full drawing manual & workflow feedback loop
> - `uv run drawlib rules show docs_build`: Multi-page documentation, navbar rules & scaffolding
> - `uv run drawlib rules show styles`    : Dynamic theming, `styles.py`, and `utils.py`
> - `uv run drawlib rules list`          : List all 20+ specialized rule topics

---

## 1. Directory Structure

- `docs/architecture_src/`: Source documents and drawing code (**Source of Truth**).
  - `build.sh`: Master build script (runs HTML, Markdown, and Image builds).
  - `build_html.sh`: Static HTML website build script.
  - `build_markdown.sh`: Rendered Markdown build script.
  - `build_image.sh`: Batch diagram image extraction script.
  - `serve.sh`: Local preview server script.
  - `styles.py`: Global drawing themes, style palettes, and font presets.
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `style.css`: Custom CSS stylesheet for HTML pages.
  - `template.html`: Jinja2 HTML layout template.
  - `navbar.md`: Navigation sidebar hierarchy definition.
  - `README.md`: This customization guide.
  - `index.md`: Root landing page.
  - `architecture/index.md`: Architecture chapter page.
  - `workflow/index.md`: Workflow chapter page.
- `docs/architecture_markdown/`: Generated Markdown site (**Do not edit directly**).
- `docs/architecture_html/`: Generated static HTML website (**Do not edit directly**).
- `docs/architecture_images/`: Generated standalone diagram images (**Do not edit directly**).

---

## 2. Building & Previewing

### Using the Build Scripts
```bash
./build_html.sh       # Compile standalone HTML website
./build_markdown.sh   # Compile Markdown for GitHub browsing
./build_image.sh      # Extract standalone diagram images
./build.sh            # Run all builds sequentially
```

### Using the Drawlib CLI Directly
```bash
# Compile to responsive static HTML website
drawlib build html docs/architecture_src/ -o docs/architecture_html/

# Compile to GitHub-friendly Markdown with linked images
drawlib build markdown docs/architecture_src/ -o docs/architecture_markdown/

# Extract diagram images
drawlib build image docs/architecture_src/ -o docs/architecture_images/
```

### Previewing the HTML Site Locally
Start the built-in development HTTP server to preview your site:
```bash
./serve.sh
# Or using drawlib directly:
drawlib serve docs/architecture_html/
```

---

## 3. Customization Guide

### 3.1. Themes & Global Styles (`styles.py`)
`styles.py` controls the visual appearance of all diagrams across the site. Drawlib automatically detects this file when building.

```python
from drawlib.fonts import FontRoboto
from drawlib.styles import Styles

# Patch default fonts or colors across all diagrams
Styles = Styles.patch_font(
    regular=FontRoboto.REGULAR,
    bold=FontRoboto.BOLD,
)
```

To switch themes across different builds, pass an alternate style file via `--styles` / `-s`:
```bash
drawlib build html docs/architecture_src/ -o docs/architecture_html/ -s custom_styles.py
```

### 3.2. Reusable Helpers & Macros (`utils.py`)
`utils.py` contains project-wide drawing macros, component generators, and shared constants. All top-level symbols defined here are automatically loaded into `drawlib.utils`.

```python
# In utils.py:
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

PROJECT_NAME = "Enterprise Platform"

def service_card(xy: tuple[float, float], title: str) -> None:
    rectangle(xy, width=32, height=18, style=Styles.BlueFlat.patch(shape_r=2))
    text(xy, title, style=Styles.WhiteBold)
```

Import and use these components inside your embedded ````drawlib```` blocks:
```python
from drawlib.utils import PROJECT_NAME, service_card

service_card((50, 25), "Auth Gateway")
```

### 3.3. Navigation Sidebar (`navbar.md`)
`navbar.md` defines the navigation structure of the compiled HTML website:

1. **Brand Title**: The first `# Heading 1` sets the top-left site brand name.
2. **Category Groups**: Each `## Heading 2` defines a sidebar category section.
3. **Links**: Markdown bullets `- [Page Title](path/to/file.md)` link to documents.

```markdown
# My Project Docs

- [Home](index.md)

## 1. Architecture
- [System Architecture](architecture/index.md)

## 2. Workflow
- [Development Workflow](workflow/index.md)
```

> **Strict Link Validation**: Every link in `navbar.md` must point to an existing file. If a file is missing, the build halts with an informative error.

### 3.4. CSS Styling & Layout (`style.css` & `template.html`)
- **`style.css`**: Customize colors, fonts, margins, or responsive breakpoints by overriding CSS variables:
  ```css
  :root {
      --dl-color-primary: #1a73e8;
      --dl-sidebar-width: 280px;
  }
  ```
- **`template.html`**: Customize the Jinja2 HTML layout. You can add custom headers, footers, favicons, analytics scripts, or navigation elements.

### 3.5. Adding New Chapters & Pages
To add a new documentation page:
1. Create a Markdown file or subdirectory with `index.md` under `docs/architecture_src/`.
2. Add an entry for the new file in `navbar.md`.
3. Embed illustrations using ````drawlib```` code blocks.
4. Run `./build.sh` to compile.

### 3.6. Fast Developer Verification
When designing diagrams, test individual blocks quickly with a coordinate grid (`-g`):
```bash
# Export block 1 of a Markdown document to an image with alignment grid:
drawlib export docs/architecture_src/index.md 1 -g -o preview.png
```
To force a complete rebuild bypassing the cache:
```bash
drawlib build html docs/architecture_src/ -o docs/architecture_html/ --no-cache
```
