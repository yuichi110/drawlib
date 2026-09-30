# Drawlib Styles & Utilities Architecture Guidelines

Drawlib operates on an **"Illustration as Code"** philosophy, treating technical drawings, architectural schemas, and documentation diagrams as maintainable software artifacts.  
Rather than hardcoding colors, fonts, theme styles, or reusable helper functions into every individual script, Drawlib provides two decoupled, deterministic runtime modules:
1. `drawlib.styles`: Dynamic styling and theme presets (`Styles`, `Colors`).
2. `drawlib.utils`: Dynamic container for project-wide helper functions, components, and business constants.

> [!IMPORTANT]
> **Always Use PascalCase `Styles` and `Colors`**:
> In drawing scripts and Markdown blocks, **always import and use uppercase `Styles` and `Colors`** (`from drawlib.styles import Colors, Styles` and `style=Styles.primary_flat`, `color=Colors.Blue`).
> **Never use lowercase `styles` or `colors`**. Uppercase naming avoids variable shadowing with the `drawlib.styles` module and ensures deterministic AI code generation.

---

## 1. Dual Runtime Architecture: `styles` vs `utils`

Drawlib separates visual presentation (themes, palettes, typography) from diagram logic and project constants:

| Concept | `drawlib.styles` | `drawlib.utils` |
| :--- | :--- | :--- |
| **Primary File** | `styles.py` (or custom file via `--styles` / `-s`) | `utils.py` (or custom file via `--utils` / `-u`) |
| **Core Exports** | `Styles` (active preset styles), `Colors` (active color palette) | User-defined functions, classes, and constants |
| **Default Fallback** | `Styles = DefaultStyles()`, `Colors = DefaultColors()` | Empty container (raises actionable `AttributeError`) |
| **Typical Usage** | `from drawlib.styles import Colors, Styles` (Mandatory) | `from drawlib.utils import draw_service_box, API_PORT` |

---

## 2. Defining `styles.py`

A `styles.py` file defines project-wide visual themes and color palettes. It is a standard Python script:

```python
# styles.py
from drawlib.preset_colors import DefaultColors
from drawlib.preset_styles import DefaultStyles

# 1. Customize or replace theme presets
Styles = DefaultStyles.patch(
    primary=DefaultStyles.primary.patch(
        shape_fill_color=DefaultColors.Blue.patch(alpha=0.1),
        shape_line_color=DefaultColors.Blue,
        shape_line_width=2.0,
    ),
    bold=DefaultStyles.bold.patch(
        shape_line_width=2.5,
    ),
)
```

### Auto-Detection & CLI Overrides
- **Auto-Detection**: If a `styles.py` file is present in your input directory, Drawlib automatically loads it.
- **Custom Files**: Use `--styles` (or `-s`) to supply any custom styles file:
  ```bash
  uv run drawlib build html docs_src/ -o docs_html/ --styles theme_dark.py
  ```

---

## 3. Defining `utils.py`

A `utils.py` file houses user-defined helper functions, diagram macro components, and project constants:

```python
# utils.py
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

PROJECT_NAME = "Enterprise Cloud Architecture"
API_BASE_URL = "https://api.internal.net"
DATABASE_PORT = 5432

def draw_service_card(center: tuple[float, float], title: str, subtitle: str) -> None:
    """Reusable diagram component for microservice nodes."""
    x, y = center
    rectangle((x, y), width=36, height=20, r=2, style=Styles.primary)
    text((x, y + 4), title, style=Styles.bold)
    text((x, y - 4), subtitle, style=Styles.light)
```

### Auto-Detection & CLI Overrides
- **Auto-Detection**: If a `utils.py` file is present in your input directory, Drawlib automatically loads all top-level attributes into `drawlib.utils`.
- **Custom Files**: Use `--utils` (or `-u`) to supply any custom utilities file:
  ```bash
  uv run drawlib build html docs_src/ -o docs_html/ --utils project_helpers.py
  ```

---

## 4. Consuming in Drawing Scripts

### Explicit Import Paradigm

Drawlib strictly avoids blackbox magic, hidden global variables, and implicit wildcard imports. Drawing code explicitly imports from `drawlib.styles` and `drawlib.utils`:

```python
from drawlib.canvas import save, setup
from drawlib.styles import Colors, Styles
from drawlib.utils import API_BASE_URL, PROJECT_NAME, draw_service_card

setup(width=140, height=70)

# Reusable component from utils.py
draw_service_card((40, 35), "API Gateway", f"Port: {API_BASE_URL}")
draw_service_card((100, 35), "Database", f"Port: 5432")

save("service_architecture.png")
```

### Best Practice: Prefer `drawlib.styles` over `drawlib.preset_styles`

Drawlib provides two ways to reference style presets:
1. `drawlib.preset_styles`: Static, immutable factory presets (e.g. `DefaultStyles`, `MonochromeStyles`, `GoogleStyles`).
2. `drawlib.styles`: Dynamic, project-level styles and palettes (`Styles`, `Colors`) that can be replaced or patched at runtime via `styles.py` or `--styles`.

> **Crucial Rule**:
> If there is any scenario where you may want to theme, customize, or patch styles across documents and scripts without editing drawing code, **always reference styles from `drawlib.styles` (`from drawlib.styles import Colors, Styles`) rather than importing from `drawlib.preset_styles`**.

| Dimension | `from drawlib.styles import Colors, Styles` (Recommended) | `from drawlib.preset_styles import ...` |
| :--- | :--- | :--- |
| **Customizability** | Fully customizable & replaceable via `--styles` / `styles.py` | Fixed, static default values only |
| **Theme Switching** | Dynamic (one `styles.py` restyles all diagrams) | Manual (must edit every drawing script) |
| **Project Decoupling** | High (diagrams decouple from concrete palettes) | Low (tightly coupled to built-in presets) |
| **Usage** | `from drawlib.styles import Styles, Colors`<br>`style=Styles.primary_flat` | `from drawlib.preset_styles import DefaultStyles`<br>`style=DefaultStyles.primary_flat` |

### Helpful `AttributeError` Diagnostics

If a drawing script attempts to import or access an attribute from `drawlib.utils` that has not been defined, Drawlib raises a clear diagnostic error:

```text
AttributeError: module 'drawlib.utils' has no attribute 'UNKNOWN_HELPER'.
If this is a custom utility function or constant, ensure it is defined in your utils file
and passed via the '--utils' / '-u' option, or located in 'utils.py'.
```

---

## 5. CLI & Tools Integration

```bash
# 1. Build documentation site with custom styles and utils
uv run drawlib build html docs_src/ -o docs_html/ -s custom_styles.py -u custom_utils.py

# 2. Build GitHub Markdown documentation
uv run drawlib build markdown docs_src/ -o docs/ --styles my_theme.py

# 3. Export a single script using custom styles and grid overlay
uv run drawlib show diagram.py -s styles.py -g -o diagram.png
```

---

## 6. Related Rules

- Canvas Geometry & Sizing: `uv run drawlib rules show lib-canvas`
- Preset Styles & Color Palettes: `uv run drawlib rules show lib-preset-styles`
- Style Model Customization: `uv run drawlib rules show lib-types`
- Project Scaffolding & Structure: `uv run drawlib rules show project`
- Developer CLI Reference: `uv run drawlib rules show cli`
