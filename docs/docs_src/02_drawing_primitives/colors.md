# Color Palettes & Color Model

Drawlib represents colors through an immutable RGBA **`Color`** model backed by curated theme palettes (`DefaultColors`, `GoogleColors`, `MonochromeColors`, and `CssColors`) and linear color interpolation utilities.

---

## 1. Overview of Semantic Color Roles & Shade Tiers

```drawlib fold-code center file:colors_overview.png caption:"Drawlib 7 Semantic Color Roles and 6-Tone Shade Ramps"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=130, height=62)

roles = [
    ("Primary", [Colors.Primary1, Colors.Primary2, Colors.Primary3, Colors.Primary4, Colors.Primary5, Colors.Primary6]),
    ("Secondary", [Colors.Secondary1, Colors.Secondary2, Colors.Secondary3, Colors.Secondary4, Colors.Secondary5, Colors.Secondary6]),
    ("Accent", [Colors.Accent1, Colors.Accent2, Colors.Accent3, Colors.Accent4, Colors.Accent5, Colors.Accent6]),
    ("Success", [Colors.Success1, Colors.Success2, Colors.Success3, Colors.Success4, Colors.Success5, Colors.Success6]),
    ("Warning", [Colors.Warning1, Colors.Warning2, Colors.Warning3, Colors.Warning4, Colors.Warning5, Colors.Warning6]),
    ("Danger", [Colors.Danger1, Colors.Danger2, Colors.Danger3, Colors.Danger4, Colors.Danger5, Colors.Danger6]),
    ("Muted", [Colors.Muted1, Colors.Muted2, Colors.Muted3, Colors.Muted4, Colors.Muted5, Colors.Muted6]),
]

for col_idx, (role_name, shades) in enumerate(roles):
    cx = 13.5 + col_idx * 17.2
    text((cx, 55.5), role_name, style=Styles.DarkBold.patch(text_size=10.0))
    for row_idx, shade in enumerate(shades):
        cy = 45.5 - row_idx * 7.5
        txt_st = Styles.DarkBold if row_idx < 3 else Styles.WhiteBold
        rectangle(
            (cx, cy),
            width=15.4,
            height=6.6,
            style=Styles.NeutralFlat.patch(shape_fill_color=shade, shape_r=1),
            text=f"{role_name[0]}{row_idx + 1}",
            text_style=txt_st.patch(text_size=10.0),
        )

save()
```

---

## 2. The `Color` Class (`drawlib.preset_colors.Color`)

All color constants in Drawlib are instances of `Color` (imported from `drawlib.styles` or `drawlib.preset_colors`). `Color` is an immutable RGBA model that also behaves like a 4-tuple `(r, g, b, alpha)`:

```drawlib show-code center file:colors_alpha_and_hex.png caption:"Constructing Custom RGB/Hex Colors and Alpha Opacity Layering"
from drawlib.canvas import save, setup
from drawlib.preset_colors import Color
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=126, height=50)

# Left Panel: Custom RGB and Hex Color construction
rectangle((26, 25), width=42, height=40, style=Styles.Neutral.patch(shape_r=2))
text((26, 40), "Custom RGB & Hex", style=Styles.DarkBold.patch(text_size=10.5))

c_rgb = Color(37, 99, 235)
c_hex = Color("#10B981")

rectangle(
    (26, 29),
    width=36,
    height=11,
    style=Styles.NeutralFlat.patch(shape_fill_color=c_rgb, shape_r=1.5),
    text="Color(37, 99, 235)",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rectangle(
    (26, 14),
    width=36,
    height=11,
    style=Styles.NeutralFlat.patch(shape_fill_color=c_hex, shape_r=1.5),
    text='Color("#10B981")',
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

# Right Panel: Alpha opacity patching on Colors.Blue4
rectangle((87, 25), width=68, height=40, style=Styles.Neutral.patch(shape_r=2))
text((87, 40), "Colors.Blue4.patch(alpha=...)", style=Styles.DarkBold.patch(text_size=10.5))

for i, a_val in enumerate([0.2, 0.5, 0.8, 1.0]):
    cx = 62.2 + i * 16.5
    col = Colors.Blue4.patch(alpha=a_val)
    lbl_st = Styles.DarkBold if a_val <= 0.5 else Styles.WhiteBold
    rectangle(
        (cx, 22),
        width=14.8,
        height=22,
        style=Styles.Neutral.patch(shape_fill_color=col, shape_line_width=0.8, shape_r=1.5),
        text=f"alpha\n{a_val}",
        text_style=lbl_st.patch(text_size=10.0),
    )

save()
```

| Property / Method | Return Type | Description |
| :--- | :--- | :--- |
| `color.r`, `color.g`, `color.b` | `int` (`0..255`) | Red, Green, and Blue channel values. |
| `color.alpha` / `color.a` | `float` (`0.0..1.0`) | Opacity channel (`0.0` = transparent, `1.0` = opaque). |
| `color.rgb` | `tuple[int, int, int]` | Standard 3-tuple `(r, g, b)`. |
| `color.rgba` | `tuple[int, int, int, float]` | Standard 4-tuple `(r, g, b, alpha)`. |
| `color.hex` | `str` | Lowercase hex string (`"#rrggbb"` or `"#rrggbbaa"` when `alpha < 1.0`). |
| `Color.from_hex(hexcode, alpha=None)` | `Color` | Parses 3-, 4-, 6-, or 8-digit hex strings with optional `alpha` override. |
| `color.patch(r=..., g=..., b=..., alpha=...)` | `Color` | Returns a new `Color` with updated channel(s) or opacity. |
| `color.to_mplot_rgba()` | `tuple[float, float, float, float]` | Normalized `0.0..1.0` RGBA tuple for Matplotlib backends. |

---

## 3. Preset Color Palettes & Shade Tiers

All color catalogs are imported from `drawlib.preset_colors` (with the active palette exposed as `Colors` in `drawlib.styles`):

```python
from drawlib.preset_colors import (
    CssColors,
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
    GoogleColors,
    MonochromeColors,
)
```

### 3.1. Shade Tiers & Surface Tokens

Within `DefaultColors` and `GoogleColors`, every semantic role (`Primary`, `Secondary`, `Accent`, `Warning`, `Danger`, `Success`, `Muted`) and chromatic hue (`Blue`, `Green`, `Red`, `Orange`, `Amber`, `Purple`, `Teal`, `Pink`) is organized into **6 shade tiers** plus surface tokens:

| Tier / Token | Example Attributes | Visual Role |
| :--- | :--- | :--- |
| **Tone `1` (Pale / Pastel)** | `Colors.Primary1`, `Colors.Blue1`, `Colors.PrimaryNeutral` | Ultra-light tinted card fills (`Styles.*Neutral`). |
| **Tone `2` (Light)** | `Colors.Primary2`, `Colors.Gray2`, `Colors.Neutral` | Calm neutral card surfaces (`Styles.Neutral`). |
| **Tone `3` (Medium Soft)** | `Colors.Primary3`, `Colors.Blue3`, `Colors.Gray3` | Tinted neutral card borders and soft dividers. |
| **Tone `4` (Normal / Base)** | `Colors.Primary` (`Primary4`), `Colors.Blue4` | Standard saturated hero fill (`Styles.PrimaryFlat`). |
| **Tone `5` (Deep)** | `Colors.Primary5`, `Colors.Blue5`, `Colors.Gray5` | Emphasized borders and active states. |
| **Tone `6` (Darkest Shade)** | `Colors.Primary6`, `Colors.Blue6` | High-contrast text inside tinted neutral cards. |
| **Surface & Charcoal** | `Colors.Canvas`, `Colors.Light` (`White`), `Colors.Dark` (`Gray7`), `Colors.Gray1`..`Gray8`, `Colors.Black` | Canvas background, card surfaces, borders, and body charcoal text. |

```drawlib fold-code center file:colors_chromatic_and_surface_swatches.png caption:"8 Chromatic Hue Families (Tiers 1–6) and Grayscale Surface Ramp"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=134, height=74)

hues = ["Blue", "Green", "Red", "Orange", "Amber", "Purple", "Teal", "Pink"]

for col_idx, hue in enumerate(hues):
    cx = 12.2 + col_idx * 15.6
    text((cx, 68.5), hue, style=Styles.DarkBold.patch(text_size=10.0))
    for tier in range(1, 7):
        cy = 60.0 - (tier - 1) * 6.8
        col = getattr(Colors, f"{hue}{tier}")
        txt_st = Styles.DarkBold if tier <= 3 else Styles.WhiteBold
        rectangle(
            (cx, cy),
            width=14.2,
            height=6.0,
            style=Styles.NeutralFlat.patch(shape_fill_color=col, shape_r=1),
            text=f"{hue[0]}{tier}",
            text_style=txt_st.patch(text_size=10.0),
        )

# Bottom row: Grayscale & Surface Ramp (Light, Gray1..Gray8, Dark)
text((67, 17.5), "Surface & Grayscale Ramp (Light, Gray1..Gray8, Dark)", style=Styles.DarkBold.patch(text_size=10.5))
surfaces = [
    ("L", Colors.Light),
    *[(f"G{i}", getattr(Colors, f"Gray{i}")) for i in range(1, 9)],
    ("D", Colors.Dark),
]
for s_idx, (s_lbl, s_col) in enumerate(surfaces):
    sx = 11.8 + s_idx * 12.3
    s_txt = Styles.DarkBold if s_idx < 5 else Styles.WhiteBold
    rectangle(
        (sx, 9.0),
        width=11.2,
        height=8.0,
        style=Styles.Neutral.patch(shape_fill_color=s_col, shape_line_width=0.6, shape_r=1),
        text=s_lbl,
        text_style=s_txt.patch(text_size=10.0),
    )

save()
```

### 3.2. Comparing Theme Palettes (`DefaultColors1..6`, `GoogleColors`, `MonochromeColors`, `CssColors`)

- **`DefaultColors` (`DefaultColors1`..`DefaultColors6`)**: `DefaultColors` centers semantic roles on Tone 4 (`DefaultColors4`), while `DefaultColors1` through `DefaultColors6` shift the default `Primary`/`Secondary`/`Accent` tokens across Tones 1–6.
- **`GoogleColors`**: Official Google Workspace / Material tones (`GoogleBlue`, `GoogleRed`, `GoogleYellow`, `GoogleGreen`, `GoogleOrange`, `GooglePurple`, `CornflowerBlue1..6`, `RedBerry1..6`).
- **`MonochromeColors`**: 10-step pure grayscale ramp (`White`, `Gray1`..`Gray8`, `Black`) for print and academic publications.
- **`CssColors`**: All 140 W3C CSS named colors (`CssColors.AliceBlue`, `CssColors.CornflowerBlue`, `CssColors.DarkSlateGray`, etc.).

```drawlib show-code center file:colors_theme_palettes.png caption:"Swatches of DefaultColors, GoogleColors, and MonochromeColors"
from drawlib.canvas import save, setup
from drawlib.preset_colors import DefaultColors, GoogleColors, MonochromeColors
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=56)

palettes = [
    (44, "DefaultColors", [DefaultColors.Primary, DefaultColors.Secondary, DefaultColors.Accent, DefaultColors.Success, DefaultColors.Warning, DefaultColors.Danger]),
    (28, "GoogleColors", [GoogleColors.Primary, GoogleColors.Secondary, GoogleColors.Accent, GoogleColors.Success, GoogleColors.Warning, GoogleColors.Danger]),
    (12, "Monochrome", [MonochromeColors.Gray1, MonochromeColors.Gray2, MonochromeColors.Gray4, MonochromeColors.Gray6, MonochromeColors.Gray8, MonochromeColors.Black]),
]

headers = ["Primary", "Secondary", "Accent", "Success", "Warning", "Danger"]
for idx, h in enumerate(headers):
    text((44 + idx * 15.5, 52), h, style=Styles.DarkBold.patch(text_size=10.0))

for y, label, swatch_list in palettes:
    text((6, y), label, style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
    for idx, col in enumerate(swatch_list):
        cx = 44 + idx * 15.5
        rectangle(
            (cx, y),
            width=13.5,
            height=10,
            style=Styles.Neutral.patch(shape_fill_color=col, shape_line_width=0.8, shape_r=1.5),
        )

save()
```

---

## 4. Color Interpolation (`get_intermediate_color` & `get_intermediate_colors`)

When building heatmaps, multi-stage pipelines, or smooth animation transitions, use `get_intermediate_color` and `get_intermediate_colors` from `drawlib.styles` (or `drawlib.preset_colors`):

- **`get_intermediate_color(color1, color2) -> Color`**: Returns the exact 50% midpoint `Color` between `color1` and `color2`.
- **`get_intermediate_colors(color1, color2, num=1, *, include_ends=False) -> list[Color]`**: Divides the linear RGBA transition from `color1` to `color2` into `num + 1` equal intervals and returns `num` interior colors (or `num + 2` colors including both endpoints when `include_ends=True`).

```drawlib show-code center file:colors_interpolation.png caption:"Smooth Color Gradient Generated with get_intermediate_colors()"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors
from drawlib.text import text

setup(width=130, height=44)

# Generate 7 steps including endpoints from Primary1 (light pastel) to Primary6 (dark shade)
steps = get_intermediate_colors(Colors.Primary1, Colors.Primary6, num=5, include_ends=True)

text((65, 36.5), "get_intermediate_colors(Colors.Primary1, Colors.Primary6, num=5, include_ends=True)", style=Styles.DarkBold.patch(text_size=10.5))

for i, col in enumerate(steps):
    cx = 13.5 + i * 17.2
    label_style = Styles.DarkBold if i < 3 else Styles.WhiteBold
    rectangle(
        (cx, 18.5),
        width=15.5,
        height=18,
        style=Styles.NeutralFlat.patch(shape_fill_color=col, shape_r=1.5),
        text=col.hex,
        text_style=label_style.patch(text_size=10.0),
    )

save()
```
