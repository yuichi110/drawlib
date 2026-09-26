# Advanced Preset Styles Topics

In this section, we cover advanced topics for working with preset styles in `drawlib.preset_styles` and `drawlib.config`.

# Accessing Styles via `drawlib.config` or Official Catalogs

Drawlib provides style presets as catalog objects (`BasePresetStyles`) containing strongly-typed `Style` objects for key roles and colors.
The recommended way to access styles in drawing code is via `drawlib.config`:

```python
from drawlib.config import styles
```

This provides direct access to the active project styles (defaulting to `EssentialsStyles`) and allows styles to be themed dynamically across the entire project via configuration files.

## Standard Style Roles

You can access standard preset styles directly by attribute or key:

- `styles.primary`: The default primary style.
- `styles.light`: Light line/font weight style.
- `styles.bold`: Bold line/font weight style.
- `styles.flat`: Filled shape with no border line.
- `styles.solid`: Outlined shape with no fill color.
- `styles.dashed`: Outlined shape with dashed line style.

Example:

```python
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle, rectangle
from drawlib.text import text

setup(width=100, height=40)

style_primary = styles.primary
style_bold = styles.bold

circle((25, 20), radius=10, style=style_primary)
rectangle((75, 20), width=20, height=20, style=style_bold)
text((50, 20), "Preset Styles", style=styles.bold)
```

Executing this code produces the following output:



<div class="drawlib-image" style="text-align: center;">
  <img src="advanced_topics_images/1.png" alt="advanced_topics_1" style="width: 600px; max-width: 100%;" />
</div>



## Using Color Names and Combinations

You can also access color-specific styles (e.g., `styles.red_flat`, `styles.blue_solid`, `styles.red_bold`):

```python
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle, rectangle
from drawlib.text import text

setup(width=100, height=40)

circle((25, 20), radius=10, style=styles.red_flat)
rectangle((75, 20), width=20, height=20, style=styles.blue_solid)
text((50, 20), "Combined Style", style=styles.red_bold)
```

Executing this code produces:



<div class="drawlib-image" style="text-align: center;">
  <img src="advanced_topics_images/2.png" alt="advanced_topics_2" style="width: 600px; max-width: 100%;" />
</div>




# Accessing Official Style Presets

# Accessing Official Style Catalogs Directly

Drawlib includes three official immutable style catalogs: `default_styles`, `essentials_styles`, and `monochrome_styles`.
You can import them directly from `drawlib.preset_styles`:

- `from drawlib.preset_styles import default_styles`
- `from drawlib.preset_styles import essentials_styles`
- `from drawlib.preset_styles import monochrome_styles`

Each `BasePresetStyles` instance contains `primary`, `light`, `bold`, `flat`, `solid`, and `dashed` `Style` attributes.

Example:

```python
from drawlib.canvas import setup
from drawlib.preset_styles import essentials_styles, monochrome_styles
from drawlib.shapes import circle, rectangle

setup(width=100, height=40)

circle((25, 20), radius=10, style=essentials_styles.primary)
rectangle((75, 20), width=20, height=20, style=monochrome_styles.bold)
```

Output:



<div class="drawlib-image" style="text-align: center;">
  <img src="advanced_topics_images/3.png" alt="advanced_topics_3" style="width: 600px; max-width: 100%;" />
</div>




# Customizing Style Objects with `.patch()`

Because `Style` objects in Drawlib are immutable (`frozen=True`), styles are customized using the `.patch()` method to create new derived `Style` instances safely:

```python
from drawlib.canvas import setup
from drawlib.colors import ColorsDefault
from drawlib.config import styles
from drawlib.text import text

custom_style = styles.blue.patch(text_size=28, text_color=ColorsDefault.Red)

setup(width=100, height=40)
text((50, 20), "Customized Style", style=custom_style)
```

Output:



<div class="drawlib-image" style="text-align: center;">
  <img src="advanced_topics_images/4.png" alt="advanced_topics_4" style="width: 600px; max-width: 100%;" />
</div>




# Patching Typography Globally with `styles.patch_font()`

When creating illustrations or documentation in Japanese, Chinese, or specialized brand typefaces, setting fonts individually on each shape or text call is tedious and prone to missing glyphs (e.g. tofu boxes on bold text).

You can patch all font definitions across the entire active style catalog using `styles.patch_font()`:

```python
from drawlib.config import styles
from drawlib.fonts import FontJapanese

# Patch regular and bold fonts for all styles in the active catalog
styles.patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
)
```

### Parameter Resolution:
- **`regular`**: Serves as the fallback default font for all styles in the catalog (including bold and light if not overridden).
- **`bold`** (keyword-only): Overrides all bold styles (such as `styles.bold`, `styles.blue_bold`, etc.).
- **`light`** (keyword-only): Overrides all light styles (such as `styles.light`, `styles.red_light`, etc.).
- **`sourcecode`** (keyword-only): Updates the default monospace font used by source code rendering components (`styles.sourcecode_font`).

This method is commonly configured in your project's `config.py` so that all diagrams automatically render with the appropriate font.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
