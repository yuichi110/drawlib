# Drawlib Colors Guidelines

Color in Drawlib is defined through declarative RGB/RGBA tuples, standardized color constant catalogs, and ergonomic helper utilities.  
Drawlib enforces visual harmony across diagrams through curated theme palettes while permitting complete customization via hex codes and grayscale ramps.

---

## 1. Imports & Core Architecture

All public color classes and conversion utilities are imported from `drawlib.preset_colors` (or active theme colors from `drawlib.styles`):

```python
from drawlib.preset_colors import (
    # First-class Color model
    Color,

    # Standard Color Constant Classes
    CssColors,               # Full CSS / W3C 140 standard named colors
    DefaultColors,           # Palette class used by preset style 'default'
    MonochromeColors,        # Grayscale palette class used by 'monochrome'
    GoogleColors,            # Palette class used by 'google' theme
)

# Or access active theme colors dynamically as PascalCase tokens:
from drawlib.styles import Colors
```

---

## 2. Color Representation Formats

Drawlib accepts colors in multiple convenient formats:

1. **`Color` Model**: `Color(r, g, b, alpha=1.0)` or `Color("#3498db")`
   - An immutable 4-tuple subclass `(r, g, b, alpha)` providing channel accessors (`.r`, `.g`, `.b`, `.alpha`, `.hex`) and the `.patch()` derivation method.
   - Transparently satisfies standard Python tuple operations and passes seamlessly to drawing primitives.
2. **RGB Tuple**: `(r, g, b)`
   - Integer values ranging from `0` to `255`.
   - Example: `(255, 0, 0)` is pure red; `(240, 240, 240)` is light gray.
3. **RGBA Tuple**: `(r, g, b, alpha)`
   - `r`, `g`, `b`: Integers `0` to `255`.
   - `alpha`: Float ranging from `0.0` (completely transparent) to `1.0` (fully opaque).
   - Example: `(0, 100, 200, 0.5)` is semi-transparent blue.
4. **Hex String**: `"#3498db"` or `"#3498db80"`
   - 3, 4, 6, or 8-digit hexadecimal notation automatically parsed into `Color`.

> **Validation Rule**:  
> Drawlib validates colors strictly. Values `< 0` or `> 255` for RGB channels, or `< 0.0` or `> 1.0` for alpha will raise a validation `ValueError`.

---

## 3. Color Catalogs

### 3.1. `Colors` / `DefaultColors`
The standard set for rapid prototyping, architecture diagrams, and geometric styling:

- **6-Tone Chromatic Scales (Levels 1 to 6)**: `Blue1..6`, `Green1..6`, `Red1..6`, `Orange1..6`, `Amber1..6`, `Purple1..6`, `Teal1..6`, `Pink1..6`
- **Neutrals (Light to Dark)**: `White`, `Gray1` through `Gray8`, `Black`
- **Classic Primaries**: `Red`, `Green`, `Blue`, `Yellow`, `Orange`, `Purple`, `Pink`, `Cyan`, `Magenta`, `Lime`, `Teal`, `Navy`, `Olive`, `Brown`, `Gold`, `Aqua`, `GreenYellow`, `Ivory`, `Steel`
- **Semantic Roles**: `Primary`, `Secondary`, `Accent`, `Muted`, `Light`, `Dark`, `Danger`, `Success`, `Canvas`, and numbered `Primary1..6`, `Secondary1..6`, `Accent1..6`, `Muted1..6`, `Danger1..6`, `Success1..6`

### 3.2. `CssColors` (W3C CSS Named Colors Catalog)
Contains all 140 standardized CSS color definitions for precise styling:

```python
CssColors.AliceBlue          # (240, 248, 255)
CssColors.CornflowerBlue     # (100, 149, 237)
CssColors.DarkSlateGray      # (47, 79, 79)
CssColors.LightCoral         # (240, 128, 128)
CssColors.MediumSeaGreen     # (60, 179, 113)
CssColors.MidnightBlue       # (25, 25, 112)
CssColors.SteelBlue          # (70, 130, 180)
# ... and 133 more standardized web color attributes
```

### 3.3. Theme Palette Catalogs
Curated color schemes designed to work harmoniously across complex architectures:

- **`DefaultColors` (`from drawlib.preset_colors import DefaultColors`)**: Standard 6-tone chromatic scales, 8-level grayscale, and semantic roles.
- **`MonochromeColors`**: 8-level grayscale tones (`White`, `Gray1..8`, `Black`) for printer-friendly publications and patent drawings.
- **`GoogleColors`**: Google Workspace and Presentation palette matching `GoogleStyles`.


---

## 4. Color Manipulation & Derivation

All preset colors (`Colors`, `DefaultColors`, `MonochromeColors`, `CssColors`, `GoogleColors`) are `Color` instances.

### 4.1. The `.patch()` Method
Derives a new `Color` instance by modifying specific channels while preserving immutability (analogous to `Style.patch()`):

```python
from drawlib.styles import Colors

# Adjust transparency (alpha)
glass_blue = Colors.Blue.patch(alpha=0.2)  # (31, 31, 255, 0.2)
subtle_orange = Colors.Orange.patch(alpha=0.15)

# Adjust RGB channels
custom_red = Colors.Red.patch(g=50, b=50)
```

### 4.2. `Color.from_hex()` & Hex Initialization
Parse hexadecimal color notation with optional alpha override:

```python
from drawlib.preset_colors import Color

# 6-digit hex string
c1 = Color.from_hex("#3498db")             # (52, 152, 219, 1.0)

# Direct instantiation
c2 = Color("#3498db")

# With explicit alpha parameter
c3 = Color.from_hex("#2ecc71", alpha=0.5)  # (46, 204, 113, 0.5)
c4 = Color("#2ecc71", alpha=0.5)

# 3-digit shorthand
c5 = Color("#f00")                         # (255, 0, 0, 1.0)
```

### 4.3. Channel Properties & Conversions
`Color` instances provide read-only properties for channel inspection:

```python
from drawlib.styles import Colors

c = Colors.Blue.patch(alpha=0.5)
print(c.r)     # 31
print(c.g)     # 31
print(c.b)     # 255
print(c.alpha) # 0.5 (alias: c.a)
print(c.rgb)   # (31, 31, 255)
print(c.rgba)  # (31, 31, 255, 0.5)
print(c.hex)   # '#1f1fff80'
```

---

## 5. Practical Code Examples

### 5.1. Multi-Tier Architecture with Curated Palettes

```drawlib fold-code 600px center caption:"Color Palette Applied to Multi-Tier Architecture"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=140, height=60)

# Define custom semantic styles
cloud_style = Styles.Primary.patch(
    shape_fill_color=Colors.Blue.patch(alpha=0.15),
    shape_line_color=Colors.Blue,
    shape_line_width=2,
)
db_style = Styles.Primary.patch(
    shape_fill_color=Colors.Orange.patch(alpha=0.2),
    shape_line_color=Colors.Orange,
    shape_line_width=2,
)

# Background cluster zone
rectangle(
    (70, 30),
    width=130,
    height=50,
    style=cloud_style,
    text="Kubernetes Cluster",
    text_style=Styles.Primary.patch(text_valign="top", text_color=Colors.Blue),
)

# Service nodes
rectangle((40, 26), width=32, height=18, style=Styles.BlueFlat, text="Web Service", text_style=Styles.WhiteBold)
rectangle((100, 26), width=32, height=18, style=db_style, text="Database", text_style=Styles.WhiteBold)

# Data connection
line((56, 26), (84, 26), arrow_head="->", style=Styles.PrimaryBold)
save()
```

### 5.2. Monochrome Print-Ready Diagram

```drawlib fold-code 600px center caption:"Monochrome Architectural Print Layout"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.preset_colors import MonochromeColors
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=120, height=50)

box_style = Styles.Primary.patch(
    shape_fill_color=MonochromeColors.Gray3,
    shape_line_color=MonochromeColors.Black,
    shape_line_width=2,
)

rectangle((30, 25), width=30, height=18, style=box_style, text="Module Alpha", text_style=Styles.PrimaryBold)
rectangle((90, 25), width=30, height=18, style=box_style, text="Module Beta", text_style=Styles.PrimaryBold)
line((45, 25), (75, 25), arrow_head="->", style=Styles.PrimaryBold)
save()
```

---

## 6. Related Rules
- Preset Styles & Naming: `uv run drawlib rules show lib-preset-styles`
- Shapes Drawing Primitives: `uv run drawlib rules show lib-shapes`
- Text Formatting & Fonts: `uv run drawlib rules show lib-text`
