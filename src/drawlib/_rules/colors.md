# Drawlib Colors Guidelines

Color in Drawlib is defined through declarative RGB/RGBA tuples, standardized color constant catalogs, and ergonomic helper utilities.  
Drawlib enforces visual harmony across diagrams through curated theme palettes while permitting complete customization via hex codes and grayscale ramps.

---

## 1. Imports & Core Architecture

All public color classes and conversion utilities are imported from `drawlib.colors`:

```python
from drawlib.colors import (
    # Standard Color Constant Classes
    Colors,                  # 16 basic web colors + Transparent
    Colors140,               # Full CSS / W3C 140 standard named colors
    ColorsDefault,           # Palette used by preset style 'default'
    ColorsEssentials,        # Clean corporate palette used by 'essentials'
    ColorsMonochrome,        # Grayscale palette used by 'monochrome'
    ColorsThemeDefault,      # Palette model class for default theme
    ColorsThemeEssentials,   # Palette model class for essentials theme
    ColorsThemeMonochrome,   # Palette model class for monochrome theme

    # Conversion & Adjustment Utilities
    from_hex,                # Parse "#RRGGBB" or "#RGB" hex string with alpha
    from_grayscale,          # Create grayscale color from single integer/float
    with_alpha,              # Return a color tuple updated with a new alpha value
)
```

---

## 2. Color Representation Formats

Drawlib accepts colors in two standard tuple formats:

1. **RGB Tuple**: `(r, g, b)`
   - Integer values ranging from `0` to `255`.
   - Example: `(255, 0, 0)` is pure red; `(240, 240, 240)` is light gray.
2. **RGBA Tuple**: `(r, g, b, alpha)`
   - `r`, `g`, `b`: Integers `0` to `255`.
   - `alpha`: Float ranging from `0.0` (completely transparent) to `1.0` (fully opaque).
   - Example: `(0, 100, 200, 0.5)` is semi-transparent blue.

> **Validation Rule**:  
> Drawlib validates color tuples strictly. Values `< 0` or `> 255` for RGB, or `< 0.0` or `> 1.0` for alpha will raise a validation `ValueError`.

---

## 3. Color Catalogs

### 3.1. `Colors` (16 Basic Web Colors + Transparent)
The standard set for quick prototyping and basic geometric annotations:

```python
Colors.Black       # (0, 0, 0)
Colors.White       # (255, 255, 255)
Colors.Gray        # (128, 128, 128)
Colors.Silver      # (192, 192, 192)
Colors.Red         # (255, 0, 0)
Colors.Maroon      # (128, 0, 0)
Colors.Yellow      # (255, 255, 0)
Colors.Olive       # (128, 128, 0)
Colors.Lime        # (0, 255, 0)
Colors.Green       # (0, 128, 0)
Colors.Aqua        # (0, 255, 255)
Colors.Teal        # (0, 128, 128)
Colors.Blue        # (0, 0, 255)
Colors.Navy        # (0, 0, 128)
Colors.Fuchsia     # (255, 0, 255)
Colors.Purple      # (128, 0, 128)
Colors.Transparent # (0, 0, 0, 0.0)
```

### 3.2. `Colors140` (CSS 140 Color Catalog)
Contains all 140 standardized CSS color definitions for precise styling:

```python
Colors140.AliceBlue          # (240, 248, 255)
Colors140.CornflowerBlue     # (100, 149, 237)
Colors140.DarkSlateGray      # (47, 79, 79)
Colors140.LightCoral         # (240, 128, 128)
Colors140.MediumSeaGreen     # (60, 179, 113)
Colors140.MidnightBlue       # (25, 25, 112)
Colors140.SteelBlue          # (70, 130, 180)
# ... and 133 more standardized web color attributes
```

### 3.3. Theme Palette Catalogs
Curated color schemes designed to work harmoniously across complex architectures:

- **`ColorsDefault`**: Standard palette for default themes (`Red`, `Green`, `Blue`, `Black`, `White`).
- **`ColorsEssentials`**: Comprehensive 25-color palette including `Orange`, `Purple`, `Teal`, `Navy`, `Aqua`, `Silver`, `Charcoal`, and light/dark variants.
- **`ColorsMonochrome`**: Multi-tier grayscale tones (`Black`, `Charcoal`, `Graphite`, `Gray`, `Silver`, `Snow`, `White`) for printer-friendly publications and patent drawings.

---

## 4. Color Helper Utilities

### 4.1. `from_hex()`
Converts hexadecimal color notation (with optional alpha) to an RGBA tuple:

```python
from drawlib.colors import from_hex

# 6-digit hex string
c1 = from_hex("#3498db")         # (52, 152, 219, 1.0)

# With explicit alpha parameter
c2 = from_hex("#2ecc71", alpha=0.5) # (46, 204, 113, 0.5)

# 3-digit shorthand
c3 = from_hex("#f00")            # (255, 0, 0, 1.0)
```

### 4.2. `from_grayscale()`
Generates neutral grayscale colors from a single luminance value:

```python
from drawlib.colors import from_grayscale

# Integer 0-255
g1 = from_grayscale(240)         # (240, 240, 240, 1.0) - Off-white canvas background
g2 = from_grayscale(50)          # (50, 50, 50, 1.0)     - Dark charcoal text

# With transparency
g3 = from_grayscale(0, alpha=0.3) # (0, 0, 0, 0.3)        - Drop shadow tint
```

### 4.3. `with_alpha()`
Creates a copy of an existing color tuple with its opacity altered:

```python
from drawlib.colors import Colors, with_alpha

# Add 20% opacity to standard Blue
glass_blue = with_alpha(Colors.Blue, 0.2)  # (0, 0, 255, 0.2)
```

---

## 5. Practical Code Examples

### 5.1. Multi-Tier Architecture with Curated Palettes

```drawlib fold-code 600px center caption:"Color Palette Applied to Multi-Tier Architecture"
from drawlib.canvas import save, setup
from drawlib.colors import ColorsDefault, ColorsEssentials, from_hex, with_alpha
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.types import Style
from drawlib.config import styles

setup(width=140, height=60)

# Define custom semantic styles
cloud_style = styles.primary.patch(
    shape_fill_color=with_alpha(ColorsDefault.Blue, 0.15),
    shape_line_color=ColorsDefault.Blue,
    shape_line_width=2,
)
db_style = styles.primary.patch(
    shape_fill_color=with_alpha(ColorsEssentials.Orange, 0.2),
    shape_line_color=ColorsEssentials.Orange,
    shape_line_width=2,
)

# Background cluster zone
rectangle(
    (70, 30),
    width=130,
    height=50,
    style=cloud_style,
    text="Kubernetes Cluster",
    textstyle=styles.primary.patch(text_valign="top", text_color=ColorsDefault.Blue),
)

# Service nodes
rectangle((40, 26), width=32, height=18, style=styles.blue_flat, text="Web Service", textstyle=styles.white_bold)
rectangle((100, 26), width=32, height=18, style=styles.green_flat, text="Database", textstyle=styles.white_bold)

# Data connection
line((56, 26), (84, 26), arrowhead="->", style=styles.bold)
save()
```

### 5.2. Monochrome Print-Ready Diagram

```drawlib fold-code 600px center caption:"Monochrome Architectural Print Layout"
from drawlib.canvas import save, setup
from drawlib.colors import ColorsMonochrome
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.types import Style
from drawlib.config import styles

setup(width=120, height=50)

box_style = styles.primary.patch(
    shape_fill_color=ColorsMonochrome.Silver,
    shape_line_color=ColorsMonochrome.Black,
    shape_line_width=2,
)

rectangle((30, 25), width=30, height=18, style=box_style, text="Module Alpha", textstyle=styles.bold)
rectangle((90, 25), width=30, height=18, style=box_style, text="Module Beta", textstyle=styles.bold)
line((45, 25), (75, 25), arrowhead="->", style=styles.bold)
save()
```

---

## 6. Related Rules
- Preset Styles & Naming: `uv run drawlib rules show preset_styles`
- Shapes Drawing Primitives: `uv run drawlib rules show shapes`
- Text Formatting & Fonts: `uv run drawlib rules show text`
