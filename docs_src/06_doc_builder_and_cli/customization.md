# Customization & Theming: Templates, CSS & Injected Code

Drawlib is designed to integrate seamlessly into corporate design languages and custom developer workflows. You can customize HTML layout structures, modify stylesheets, and inject project-wide Python drawing helpers and style definitions.

---

## 1. Customizing HTML Templates (`template.html`)

Every Drawlib site and PDF project contains a Jinja2 template (`template.html`) in its source directory. You can edit this file to:
- Inject corporate branding, header navigation bars, or company logos.
- Add external web analytics (Google Analytics, Plausible) or telemetry scripts.
- Include custom Google Fonts or CSS frameworks.

### Template Variables Provided by Drawlib:
- `{{ title }}`: The title of the current document or site brand.
- `{{ body }}`: The compiled HTML content parsed from Markdown and embedded diagrams.
- `{{ nav_sections }}` / `{{ nav_items }}`: Structured navigation tree for the sidebar (in `site` projects).
- `{{ css_href }}`: Relative path to `style.css` (or `slide.css`).
- `{{ custom_css }}`: Injected inline CSS overrides.

---

## 2. Customizing CSS Stylesheets (`style.css`)

Drawlib projects include a local `style.css` in the source folder built with a 3-layer architecture (themes, components, targets). You can edit this stylesheet directly to alter colors, typography, or spacing.

### Exporting Built-In CSS Themes:
You can overwrite your local `style.css` with any built-in Drawlib theme preset using `drawlib css export`:

```bash
# Export the Google theme to your project:
drawlib css export html google -o docs_src/style.css --force

# Export the GitHub theme:
drawlib css export html github -o docs_src/style.css --force

# Export the Monochrome dark theme:
drawlib css export html monochrome -o docs_src/style.css --force
```

---

## 3. Injected Project Styles (`styles.py`)

Rather than re-declaring custom colors and font styles in every single diagram, create a `styles.py` file in your source directory:

```python
# docs_src/styles.py
from drawlib.fonts import FontRoboto
from drawlib.styles import Styles
from drawlib.types import Style

# Project-wide custom styles
CARD_STYLE = Style(
    shape_fill_color=(245, 247, 250, 1.0),
    shape_line_color=(200, 210, 225, 1.0),
    shape_line_width=1.5,
    text_font=FontRoboto.REGULAR,
)

HIGHLIGHT_STYLE = Styles.AccentFlat
```

Pass `-s docs_src/styles.py` during build. Drawlib automatically makes your styles accessible in every embedded ````drawlib```` block:

```python
# Inside your Markdown drawing code:
from drawlib.canvas import setup
from drawlib.shapes import rectangle
import styles

setup(width=80, height=40)
rectangle((40, 20), width=50, height=25, style=styles.CARD_STYLE, text="Custom Branded Card")
```

---

## 4. Injected Helper Functions (`utils.py`)

For reusable composite drawing elements (such as specialized server racks, status badges, or complex icons), author custom functions in `utils.py`:

```python
# docs_src/utils.py
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

def draw_server_node(xy, name: str, is_active: bool = True):
    x, y = xy
    # Container
    style = Styles.PrimaryFlat if is_active else Styles.Neutral
    t_style = Styles.WhiteBold if is_active else Styles.DarkBold
    rectangle((x, y), width=28, height=14, style=style, text=name, text_style=t_style)
    # Status indicator light
    indicator_style = Styles.SuccessFlat if is_active else Styles.DangerFlat
    circle((x + 10, y + 4), radius=1.5, style=indicator_style)
```

Pass `-u docs_src/utils.py` during build. In your Markdown documents, simply import and call the helper:

```python
# Inside your Markdown drawing code:
from drawlib.canvas import setup
import utils

setup(width=100, height=40)
utils.draw_server_node((25, 20), "Primary App", is_active=True)
utils.draw_server_node((75, 20), "Replica App", is_active=False)
```
