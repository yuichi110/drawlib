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
- `{{ css_href }}`: Relative path to `style.css`.
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

Rather than re-declaring custom colors and font styles in every single diagram or scattering ad-hoc style variables, Drawlib allows you to define a `styles.py` file in your source directory.

When placed in the project root or source directory (or injected via `-s docs_src/styles.py`), Drawlib uses `styles.py` to customize the project-wide `Colors` and `Styles` design tokens:

```python
# docs_src/styles.py
from drawlib.fonts import FontRoboto
from drawlib.preset_colors import GoogleColors
from drawlib.preset_styles import GoogleStyles

# 1. Initialize project-wide color palette and style catalog
Colors = GoogleColors()
Styles = GoogleStyles().patch_font(
    regular=FontRoboto.REGULAR,
    bold=FontRoboto.BOLD,
    thin=FontRoboto.THIN,
)

# 2. Derive reusable custom component tokens
CustomCard = Styles.PrimaryNeutral.patch(
    shape_line_width=1.5,
    text_size=10.0,
)
```

### Seamless Theming with `from drawlib.styles import Styles, Colors`
When `styles.py` is present, all embedded ````drawlib```` blocks automatically inherit these settings when importing standard tokens:

```python
# Inside your Markdown drawing code:
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=80, height=40)
# Automatically rendered using the GoogleStyles theme and Roboto fonts configured in styles.py
rectangle((40, 20), width=50, height=25, style=Styles.PrimaryFlat, text="Unified Themed Card", text_style=Styles.WhiteBold)
```

### Cohesive Design with `style.css`
When scaffolding projects using `drawlib init --style google` (or `monochrome`, `default`), Drawlib automatically synchronizes both `styles.py` (for Python illustrations) and `style.css` (for HTML/PDF typography and card backgrounds). This ensures that **editorial prose and embedded architectural diagrams share a 100% unified visual identity**.

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
