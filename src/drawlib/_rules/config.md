# Drawlib Configuration Architecture Guidelines

Drawlib operates on an **"Illustration as Code"** philosophy, treating technical drawings, architectural schemas, and documentation diagrams as maintainable software artifacts.  
A cornerstone of this design is centralized configuration management: rather than hardcoding colors, fonts, theme styles, or project constants into every individual script, Drawlib provides a unified, deterministic configuration module: `drawlib.config`.

---

## 1. The Dynamic Configuration Overlay Model

Drawlib utilizes a **Dynamic Configuration Overlay** architecture.
The runtime configuration represents a set-theoretic union of default parameters and custom user settings, where user-supplied definitions take precedence:

```drawlib show-code caption:"Dynamic Configuration & Theme Merging Model"
from drawlib.canvas import save, setup
from drawlib.colors import ColorsDefault, ColorsEssentials, with_alpha
from drawlib.config import styles
from drawlib.shapes import circle, rectangle
from drawlib.text import text

# Canvas setup
setup(width=140, height=90)

# Outer container representing drawlib.config unified scope
outer_style = styles.primary.patch(
    shape_fill_color=(250, 252, 255),
    shape_line_color=ColorsEssentials.Silver,
    shape_line_width=1.5,
    shape_line_style="dashed",
)
rectangle((70, 45), width=134, height=84, r=4, style=outer_style)

# Title banner
text(
    (70, 82),
    "drawlib.config: Dynamic Configuration & Theme Merging",
    style=styles.bold.patch(text_size=14, text_color=ColorsEssentials.Graphite),
)
text(
    (70, 77),
    "User custom configuration seamlessly overlays and merges onto default configuration at runtime",
    style=styles.primary.patch(text_size=8.5, text_color=ColorsEssentials.Charcoal),
)

# Venn Circles
# Left Circle: Default Config (center x=52, y=48, radius=24)
left_circle_style = styles.primary.patch(
    shape_fill_color=with_alpha(ColorsDefault.Blue, 0.18),
    shape_line_color=ColorsDefault.Blue,
    shape_line_width=2.5,
)
circle((52, 48), radius=24, style=left_circle_style)

# Right Circle: Custom Config (center x=88, y=48, radius=24)
right_circle_style = styles.primary.patch(
    shape_fill_color=with_alpha(ColorsDefault.Green, 0.18),
    shape_line_color=ColorsDefault.Green,
    shape_line_width=2.5,
)
circle((88, 48), radius=24, style=right_circle_style)

# --- Left Set: Default Config ---
text(
    (38, 62),
    "Default Config",
    style=styles.bold.patch(text_size=11, text_color=ColorsDefault.Blue),
)
text(
    (38, 57.5),
    "(drawlib/config.py)",
    style=styles.primary.patch(text_size=7.5, text_color=ColorsEssentials.Charcoal),
)
text(
    (38, 48),
    "• styles = essentials_styles\n• a = 1\n• c = 1",
    style=styles.primary.patch(text_size=8.5, text_halign="center"),
)
text(
    (38, 36),
    "Base palette, fonts &\ndefault project styles",
    style=styles.primary.patch(text_size=7.5, text_color=ColorsEssentials.Charcoal),
)

# --- Right Set: Custom Config ---
text(
    (102, 62),
    "Custom Config",
    style=styles.bold.patch(text_size=11, text_color=ColorsDefault.Green),
)
text(
    (102, 57.5),
    "(--config my_config.py)",
    style=styles.primary.patch(text_size=7.5, text_color=ColorsEssentials.Charcoal),
)
text(
    (102, 48),
    "• d = 2\n• PROJECT_NAME\n• API_ENDPOINT",
    style=styles.primary.patch(text_size=8.5, text_halign="center"),
)
text(
    (102, 36),
    "Project extensions &\ncustom business constants",
    style=styles.primary.patch(text_size=7.5, text_color=ColorsEssentials.Charcoal),
)

# --- Center Overlap: Overrides / Overlays ---
text(
    (70, 58),
    "Overlay / Override",
    style=styles.bold.patch(text_size=9, text_color=ColorsEssentials.Purple),
)
text(
    (70, 48),
    "• b = 2\n(overwrites b=1)\n• styles.patch(...)\n(custom theme)",
    style=styles.bold.patch(text_size=7.5, text_halign="center", text_color=ColorsEssentials.Graphite),
)
text(
    (70, 34),
    "Custom values overwrite\nmatching defaults",
    style=styles.primary.patch(text_size=7, text_color=ColorsEssentials.Charcoal),
)

# --- Bottom Unified Result Banner ---
result_style = styles.primary.patch(
    shape_fill_color=ColorsEssentials.White,
    shape_line_color=ColorsDefault.Blue,
    shape_line_width=1.5,
)
rectangle((70, 14), width=126, height=14, r=2, style=result_style)

text(
    (24, 16),
    "Unified Runtime Module: drawlib.config",
    style=styles.bold.patch(text_size=8.5, text_color=ColorsDefault.Blue),
)
text(
    (24, 11),
    "Accessible anywhere via standard Python import:",
    style=styles.primary.patch(text_size=7.5, text_color=ColorsEssentials.Charcoal),
)
text(
    (80, 13.5),
    "from drawlib.config import a, b, c, d, styles, PROJECT_NAME",
    style=styles.bold.patch(text_size=8, text_color=ColorsEssentials.Charcoal),
)
text(
    (121, 13.5),
    "a=1, b=2\nc=1, d=2",
    style=styles.bold.patch(text_size=7.5, text_color=ColorsDefault.Green),
)

save()
```

### Venn Diagram Mechanics

The Venn diagram above illustrates the runtime namespace merging behavior:

1. **Default Configuration (Left Set $A$)**:
   - Defined internally in `drawlib/config.py`.
   - Ships with standard theme presets (`styles = essentials_styles`) and baseline properties (`a = 1`, `c = 1`).
   - Active whenever no custom configuration is supplied, ensuring scripts always run out-of-the-box.
2. **Custom Configuration (Right Set $B$)**:
   - Defined in any user-specified Python file (e.g. `docs_config.py`, `my_theme.py`) passed via the `--config` (`-c`) CLI option.
   - Introduces project-specific business constants (`d = 2`, `PROJECT_NAME = "Enterprise Docs"`, `API_URL = "https://..."`).
3. **The Overlap / Override Region (Intersection $A \cap B$)**:
   - When a user defines a variable with the same name as a default attribute (such as `b = 2` or customizing `styles`), the custom value **strictly overwrites** the default value.
4. **The Unified Namespace (Union $A \cup B$)**:
   - The entire combined set is accessible through the canonical module: `drawlib.config`.
   - Unmodified defaults (`a = 1`, `c = 1`) remain available.
   - Overridden values (`b = 2`) reflect the user's custom specification.
   - New custom variables (`d = 2`, `PROJECT_NAME`) are seamlessly exported.

---

## 2. Defining a Custom Configuration File

A custom configuration file is a standard Python script. Any top-level variable defined in this file is merged into `drawlib.config`.

### Example: `docs_config.py`

```python
# docs_config.py
from drawlib.colors import ColorsDefault, with_alpha
from drawlib.preset_styles import essentials_styles

# 1. Customize or replace theme presets
# Note: Existing default attributes (like `styles`) are already pre-populated in scope
styles = essentials_styles.patch(
    primary=styles.primary.patch(
        shape_fill_color=with_alpha(ColorsDefault.Blue, 0.1),
        shape_line_color=ColorsDefault.Blue,
        shape_line_width=2.0,
    ),
    bold=styles.bold.patch(
        shape_line_width=2.5,
    ),
)

# 2. Define custom project constants and parameters
PROJECT_NAME = "Cloud Architecture V2"
DATABASE_PORT = 5432
API_BASE_URL = "https://api.internal.net"
CLUSTER_REGION = "us-central1"
```

> **Execution Context**:
> When Drawlib executes your configuration script, `drawlib.config` defaults are already injected into the script's global namespace. This allows you to directly inspect or call `.patch()` on existing styles without needing to re-import baseline presets.

---

## 3. Consuming Configuration in Drawing Scripts

### Explicit Import Paradigm

Drawlib strictly avoids blackbox magic, hidden global variables, and implicit wildcard imports (such as `from drawlib.colors import *`).  
Drawing code must explicitly import the required configuration attributes directly from `drawlib.config`:

```python
from drawlib.canvas import save, setup
from drawlib.config import styles, PROJECT_NAME, API_BASE_URL
from drawlib.shapes import rectangle
from drawlib.text import text

setup(width=120, height=50)

# Utilize project-wide styling and constants
rectangle((60, 25), width=80, height=24, style=styles.primary)
text((60, 29), PROJECT_NAME, style=styles.bold)
text((60, 21), f"Endpoint: {API_BASE_URL}", style=styles.primary)

save("service_overview.png")
```

### Best Practice: Prefer `drawlib.config.styles` over `drawlib.preset_styles`

Drawlib provides two ways to reference style presets:
1. `drawlib.preset_styles`: Static, factory-instantiated presets (e.g. `DefaultStyles`, `EssentialsStyles`).
2. `drawlib.config.styles`: Dynamic, project-level styles that can be overridden and customized at runtime.

> **Crucial Rule**:
> If there is any scenario where you may want to change, theme, or customize styles via options (such as `--config my_theme.py` or build parameters), **always reference styles from `drawlib.config` (`from drawlib.config import styles`) rather than importing from `drawlib.preset_styles`**.

#### Why `drawlib.config.styles` is Preferred:
- **Replaceable at Runtime**: `drawlib.config` is dynamically overlaid by whatever custom configuration file is provided via `--config`. When drawing code accesses `styles.blue_flat`, `styles.primary`, or `styles.bold`, it automatically resolves to the custom-themed styles without changing a single line in your diagram files.
- **`preset_styles` is Static & Immutable**: Presets imported directly from `drawlib.preset_styles` cannot be replaced or patched by the CLI or documentation build tools. If you use `preset_styles` directly, your diagrams become rigid and ignore project-wide theme options.
- **Safe Fallback**: If no custom config is provided, `from drawlib.config import styles` defaults cleanly to `EssentialsStyles`, guaranteeing identical out-of-the-box behavior.

| Dimension | `from drawlib.config import styles` (Recommended) | `from drawlib.preset_styles import ...` |
| :--- | :--- | :--- |
| **Customizability** | Fully customizable & replaceable via `--config` | Fixed, static default values only |
| **Theme Switching** | Dynamic (one config file restyles all diagrams) | Manual (must edit every drawing script) |
| **Project Decoupling** | High (diagrams decouple from concrete palettes) | Low (tightly coupled to built-in presets) |
| **Usage** | `from drawlib.config import styles`<br>`style=styles.blue_flat` | `from drawlib.preset_styles import essentials_styles`<br>`styles = essentials_styles` |

### Helpful `AttributeError` Diagnostics

If a drawing script attempts to import or access a variable that is not defined in either default or custom configuration, `drawlib.config` raises a descriptive error explaining how to supply it:

```text
AttributeError: module 'drawlib.config' has no attribute 'UNKNOWN_SETTING'.
If this is a custom configuration variable, ensure it is defined in your config file
and passed via the '--config' option.
```

---

## 4. CLI & Tools Integration

Custom configuration files can have any filename or location. Pass them via the `--config` (or `-c`) option:

### CLI Commands

```bash
# 1. Build documentation site with custom theme and constants
uv run drawlib build html docs_src/ -o docs_html/ --config docs_config.py

# 2. Build GitHub Markdown documentation with custom config
uv run drawlib build markdown docs_src/ -o docs/ -c custom_theme.py

# 3. Export a single script using custom configuration
uv run drawlib export diagram.py -c docs_config.py -o diagram.png
```

### Python Developer Tools API (`drawlib.tools`)

```python
from drawlib.tools import build_html, export_block

# Build documentation using custom config
build_html("docs_src/", "docs_html/", config="docs_config.py")

# Export an individual Markdown code block using custom config
export_block("docs_src/architecture.md", 1, "output.png", config="docs_config.py")
```

---

## 5. Architectural Distinction: `drawlib.config` vs. `canvas.setup()`

To maintain clean module boundaries and avoid namespace collisions, Drawlib clearly separates global configuration from per-canvas layout:

| Aspect | `drawlib.config` (Module) | `canvas.setup()` (Function) |
| :--- | :--- | :--- |
| **Scope** | Global / Project-wide | Local / Per-canvas drawing session |
| **Purpose** | Theme presets (`styles`), business constants, environment flags | Canvas virtual dimensions (`width`, `height`), resolution (`dpi`), background color, grid |
| **Invocation** | Loaded via `--config <path>` before drawing execution | Called explicitly in drawing script: `setup(width=140, height=70)` |
| **Import** | `from drawlib.config import styles, MY_CONST` | `from drawlib.canvas import setup` or `canvas.setup()` |

---

## 6. Related Rules

- Canvas Geometry & Sizing: `uv run drawlib rules show canvas`
- Preset Styles & Color Palettes: `uv run drawlib rules show preset_styles`
- Style Model Customization: `uv run drawlib rules show types`
- Documentation Build & Scaffolding: `uv run drawlib rules show docs_build`
- Developer CLI Reference: `uv run drawlib rules show cli`
