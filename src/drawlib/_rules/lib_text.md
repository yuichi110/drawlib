# Drawlib Text Guidelines

Drawlib provides a comprehensive text rendering engine designed for technical diagrams, architecture schemas, statistical charts, and document illustrations.  
It supports multi-line formatting, precise anchor alignment, arbitrary rotation angles, customizable font families, pre-defined style palettes, background bounding boxes, and vertical text rendering.

---

## 1. Imports & Core Architecture

All public text functions and types are imported from standard Drawlib modules:

```python
# Primary text rendering functions
from drawlib.text import text, text_vertical

# Style and color types
from drawlib.preset_colors import (
    CssColors,
    DefaultColors,
    GoogleColors,
    MonochromeColors,
)
from drawlib.types import Style

# Built-in font collections
from drawlib.fonts import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)
```

---

## 2. Core Functions: `text()` and `text_vertical()`

### 2.1. `text()` Specification
`text()` draws horizontal or rotated text at an anchor coordinate `(x, y)`.

```python
text(
    xy: tuple[float, float],
    text: str,
    *,
    style: Style,
    angle: float = 0.0,
) -> None
```

#### Parameter Breakdown:
- **`xy` (tuple[float, float])**: The anchor point `(x, y)` on the canvas.
- **`text` (str)**: The string content to render. Supports newline characters (`\n`) for multi-line blocks.
- **`style` (Style)**: Required keyword-only `Style` instance (e.g. `Styles.PrimaryBold`, `Styles.Primary`, `Styles.BlueBold` or custom `Style(...)`).
  Alignment is controlled via `Style(halign="...", valign="...")` (`halign`: `"left"`, `"center"`, `"right"`; `valign`: `"bottom"`, `"center"`, `"top"`). Font size is controlled via `Style(text_size=...)` or `style.patch(text_size=...)`.
- **`angle` (float)**: Counter-clockwise rotation angle in degrees around the anchor point `xy` (default: 0.0).

### 2.2. `text_vertical()` Specification
Vertical text layout stacks glyphs vertically from top to bottom.

```python
text_vertical(
    xy: tuple[float, float],
    text: str,
    *,
    style: Style,
    angle: float = 0.0,
) -> None
```

> **Rule for Vertical Text**: `style.halign` must be `"center"`. If another alignment is specified, Drawlib will issue a warning and automatically patch it to `"center"` to ensure glyph centerlines remain aligned.

> [!TIP]
> ### Best Practice: Adjusting Font Size and Text Attributes via `style.patch()`
> Drawlib text primitives keep geometric positioning purely separate from typography styling.
> Rather than passing ad-hoc size or color arguments, use `.patch()` on preset styles to override font size, alignment, or colors while maintaining design consistency:
>
> ```python
> from drawlib.styles import Colors, Styles
> from drawlib.text import text
>
> # 1. Inherit from preset style and adjust font size
> text((50, 30), "Important Metric", style=Styles.PrimaryBold.patch(text_size=18))
>
> # 2. Fine-tune secondary text size, alignment, and color for annotations
> text(
>     (50, 15),
>     "Supplementary description",
>     style=Styles.Secondary.patch(
>         text_size=10,
>         halign="left",
>         text_color=Colors.Gray5,
>     ),
> )
> ```

---

## 3. Coordinate Alignment System (`halign` & `valign`)

Text positioning is governed by the anchor point `xy` and the combination of `halign` and `valign`.

```text
                  valign="top"
        ┌──────────────────────────────┐
        │                              │
halign  │     (x, y) anchor point      │  halign
="left" │       valign="center"        │  ="right"
        │                              │
        └──────────────────────────────┘
                 valign="bottom"
```

### 3.1. Alignment Combinations
| `halign` | `valign` | Visual Effect | Common Use Case |
| :--- | :--- | :--- | :--- |
| `"center"` | `"center"` | Anchor `(x, y)` is the exact bounding box midpoint. | Shape labels, diagram node titles, badge text. |
| `"left"` | `"center"` | Text begins at `x` and extends to the right; centered vertically. | Key-value labels, list items, timeline milestones. |
| `"left"` | `"bottom"` | Text begins at `x` and sits above baseline `y`. | Section headers, chart X-axis labels. |
| `"right"` | `"center"` | Text ends at `x` and extends to the left. | Right-aligned numeric metrics, table values. |
| `"center"` | `"top"` | Text hangs downward from `y`; centered horizontally. | Captions placed directly underneath shapes or icons. |

### 3.2. Alignment Code Example
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.fonts import Font
from drawlib.shapes import circle
from drawlib.styles import Colors, Styles
from drawlib.text import text
from drawlib.types import Style

setup(width=100, height=60)

# Anchor point reference marker
anchor = (50, 30)
circle(anchor, radius=0.8, style=Styles.RedFlat)

# Text aligned left-bottom from the anchor
style_lb = Styles.Primary.patch(
    halign="left", valign="bottom", text_color=Colors.Blue, text_font=Font.SANSSERIF_BOLD
)
text(anchor, "Left-Bottom", style=style_lb)

# Text aligned right-top from the anchor
style_rt = Styles.Primary.patch(
    halign="right", valign="top", text_color=Colors.Green, text_font=Font.SANSSERIF_BOLD
)
text(anchor, "Right-Top", style=style_rt)

save()
```

---

## 4. Pre-defined Text Styles

Drawlib provides systematic pre-defined text styles on the active theme styles object (`styles`).

### 4.1. Style Preset Attributes
Preset styles provide pre-configured typography, weight, and color:
- Semantic roles:
  - `Styles.Primary`: Default text color, regular font weight.
  - `Styles.PrimaryBold`: Default text color, bold font weight.
  - `Styles.Light`: Default text color, light font weight.
  - `Styles.White`: White text, regular weight.
  - `Styles.WhiteBold`: White text, bold weight.
- Color variations:
  - `Styles.Blue`, `Styles.BlueBold`: Blue typography.
  - `Styles.Green`, `Styles.GreenBold`: Green typography.
  - `Styles.Red`, `Styles.RedBold`: Red typography.
  - `Styles.Muted`, `Styles.MutedBold`: Muted gray typography.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=40)
text((20, 30), "Standard Regular", style=Styles.Primary)
text((20, 20), "Primary Bold", style=Styles.PrimaryBold)
text((20, 10), "Muted Gray", style=Styles.Muted)

text((70, 30), "Active Feature", style=Styles.BlueBold)
text((70, 20), "Success Status", style=Styles.GreenBold)
text((70, 10), "Critical Warning", style=Styles.RedBold)
save()
```

---

## 5. Advanced Styling with the `Style` Class

When pre-defined styles are insufficient, pass a custom `Style` instance to control color, typography, and background framing.

### 5.1. Text Typography Attributes in `Style`
- **`text_color` (tuple | str | Color)**: Color of the glyphs (e.g. `Colors.Blue`, `"#1a73e8"`).
- **`text_size` (float)**: Font size in points (e.g. `12`, `18`, `28`).
- **`text_font` (Font | FontFile)**: Font family definition.
- **`halign` (str)**: `"left"`, `"center"`, `"right"`.
- **`valign` (str)**: `"bottom"`, `"center"`, `"top"`.
- **`text_line_spacing` (float)**: Line spacing multiplier for multi-line text (default: `1.2`).

### 5.2. Text Background Box Attributes in `Style`
Drawlib can automatically render a padded background rectangle behind the text block (useful for overlaying readable text across busy diagram lines):
- **`text_bg_fill_color` (tuple | str | Color)**: Background fill color.
- **`text_bg_fill_alpha` (float)**: Transparency of background fill (`0.0` transparent to `1.0` opaque).
- **`text_bg_line_color` (tuple | str | Color)**: Border color of the background box.
- **`text_bg_line_width` (float)**: Border stroke width (set to `0` for borderless background).
- **`text_bg_line_style` (str)**: Border line pattern (`"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`).

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.fonts import FontSerif
from drawlib.styles import Colors
from drawlib.text import text
from drawlib.types import Style

setup(width=120, height=60)

# Custom typography with background framing
badge_style = Style(
    text_color=Colors.White,
    text_size=14,
    text_font=FontSerif.MERRIWEATHER_REGULAR,
    halign="center",
    valign="center",
    text_bg_fill_color=Colors.Navy,
    text_bg_fill_alpha=0.9,
    text_bg_line_color=CssColors.LightBlue,
    text_bg_line_width=1.5,
    text_bg_line_style="solid",
)

text((60, 30), "Protected Security Zone", style=badge_style)
save()
```

---

## 6. Font Library & Typography Management

Drawlib does **not** rely on uncontrolled operating system fonts. Using host OS fonts risks layout breakage across Linux, macOS, and Windows.  
Instead, Drawlib bundles and manages standardized open-source font collections ensuring pixel-perfect parity on all systems.

### 6.1. General Purpose Font Collections
Imported from `drawlib.fonts`:

1. **`Font`**: Core standard weights
   - `Font.SANSSERIF_THIN`, `Font.SANSSERIF_REGULAR`, `Font.SANSSERIF_BOLD`
   - `Font.SERIF_THIN`, `Font.SERIF_REGULAR`, `Font.SERIF_BOLD`
   - Default family: **Noto Sans CJK Japanese** (universal multilingual sans-serif).
2. **`FontRoboto`**:
   - `FontRoboto.ROBOTO_THIN`, `FontRoboto.ROBOTO_REGULAR`, `FontRoboto.ROBOTO_BOLD`
   - `FontRoboto.SERIF_THIN`, `FontRoboto.SERIF_REGULAR`, `FontRoboto.SERIF_BOLD`
   - `FontRoboto.MONO_THIN`, `FontRoboto.MONO_REGULAR`, `FontRoboto.MONO_BOLD`
3. **`FontSansSerif`**:
   - `FontSansSerif.LATO_THIN`, `LATO_REGULAR`, `LATO_BOLD`
   - `FontSansSerif.MONTSERRAT_THIN`, `MONTSERRAT_REGULAR`, `MONTSERRAT_BOLD`
   - `FontSansSerif.OSWALD_THIN`, `OSWALD_REGULAR`, `OSWALD_BOLD`
   - `FontSansSerif.POPPINS_THIN`, `POPPINS_REGULAR`, `POPPINS_BOLD`
   - `FontSansSerif.RALEWAYS_THIN`, `RALEWAYS_REGULAR`, `RALEWAYS_BOLD`
4. **`FontSerif`**:
   - `FontSerif.COURIER_REGULAR`, `COURIER_BOLD`
   - `FontSerif.MERRIWEATHER_THIN`, `MERRIWEATHER_REGULAR`, `MERRIWEATHER_BOLD`
   - `FontSerif.PLATYPI_THIN`, `PLATYPI_REGULAR`, `PLATYPI_BOLD`
   - `FontSerif.PLAYFAIRDISPLAY_REGULAR`, `PLAYFAIRDISPLAY_BOLD`
5. **`FontMonoSpace` / `FontSourceCode`**:
   - `FontMonoSpace.ROBOTO_MONO_REGULAR`, `FontMonoSpace.COURIER_REGULAR`, `FontMonoSpace.SOURCECODEPRO_REGULAR`, `FontMonoSpace.SOURCEHANCODEJP_REGULAR`
   - Essential for code blocks, terminal outputs, JSON keys, and monospaced tables.

### 6.2. International & Local Language Fonts
For non-Latin languages requiring specialized typographies:
- **`FontJapanese`**: `FontJapanese.SANSSERIF_REGULAR`, `SERIF_REGULAR`, `MPLUS1P_REGULAR`, `MPLUSROUNDED1C_REGULAR`, `SAWARABI_GOTHIC`, `SAWARABI_MINCHO`
- **`FontChinese`**: `FontChinese.SIMPLIFIED_SANSSERIF_REGULAR`, `TRADITIONAL_SANSSERIF_REGULAR`, `HONGKONG_SANSSERIF_REGULAR`
- **`FontKorean`**: `FontKorean.SANSSERIF_REGULAR`, `SERIF_REGULAR`
- **`FontThai`**: `FontThai.SANSSERIF_REGULAR`, `SERIF_REGULAR`
- **`FontArabic`**: `FontArabic.SANSSERIF_REGULAR`, `KUFI_REGULAR`, `NASKH_REGULAR`
- **`FontBrahmic`**: `FontBrahmic.BENGALI_SANSSERIF_REGULAR`, `DEVANAGARI_SANSSERIF_REGULAR`, `TAMIL_SANSSERIF_REGULAR`, `TELUGU_SANSSERIF_REGULAR`

### 6.3. External Custom Font Files (`FontFile`)
To use custom corporate fonts (TTF/OTF), use `FontFile`:

```python
from drawlib.fonts import FontFile
from drawlib.text import text
from drawlib.types import Style

custom_style = Styles.Primary.patch(
    text_font=FontFile("assets/fonts/Inter-SemiBold.ttf"),
    text_size=16,
    text_color="#111827",
)
text((50, 25), "Corporate Brand Typography", style=custom_style)
```

---

## 7. Multi-Line Text & Layout

`text()` natively parses newline characters (`\n`) to generate multi-line paragraphs.

### 7.1. Behavior & Line Spacing
- Line spacing is calculated relative to `text_size` (default multiplier: `1.2`). You can customize the vertical spacing between lines via `style.patch(text_line_spacing=1.6)`.
- The entire multi-line block conforms to the specified `halign` and `valign`.
  - With `halign="center"` (default), each line is individually centered.
  - With `halign="left"`, all lines align flush to the left boundary.
  - With `halign="right"`, all lines align flush to the right boundary.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=60)

summary = (
    "Database Cluster (Primary)\n"
    "Status: Healthy (99.99%)\n"
    "Replication: Synchronous (2 Replicas)\n"
    "Region: us-central1"
)

text((50, 30), summary, style=Styles.PrimaryBold.patch(text_size=12, text_line_spacing=1.5))
save()
```

---

## 8. Rotated Text (`angle`)

The `angle` parameter rotates text counter-clockwise around the specified anchor coordinate `xy`.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=60)

# Vertical axis label (-90 degrees or 90 degrees)
text((10, 30), "Request Throughput (req/sec)", angle=90, style=Styles.PrimaryBold.patch(text_size=12))

# Diagonal watermark / status label (45 degrees)
text((50, 30), "INTERNAL DRAFT ONLY", angle=45, style=Styles.Muted.patch(text_size=22))

save()
```

---

## 9. Embedding Text in Shapes

In Drawlib, you rarely need to call `text()` manually to place labels inside boxes or circles.  
All shape functions (`rectangle`, `circle`, `donuts`, `chevron`, `polygon`, etc.) accept direct text attributes:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

setup(width=110, height=50)

# Text centered automatically inside shapes
rectangle(
    (30, 25),
    width=28,
    height=16,
    style=Styles.PrimaryFlat,
    text="Gateway API",
    text_style=Styles.WhiteBold,
)

circle(
    (75, 25),
    radius=10,
    style=Styles.SecondaryNeutral,
    text="Worker Node\n(Active)",
)

save()
```

### Shape Text Parameters:
- **`text` (str)**: Content string (supports `\n`).
- **`text_style` (Style | None)**: Pre-defined style (e.g. `Styles.WhiteBold`, `Styles.PrimaryBold`) or custom `Style` (override font size via `text_style=Styles.WhiteBold.patch(text_size=12)`).

---

## 10. Agent Practical Implementation Checklist

When adding text to Drawlib illustrations:

1. **Hierarchy & Neutral Text Colors**:
   - Diagram titles: `text_size=20–24` via `Styles.DarkBold.patch(text_size=22)`, `halign="center"` at canvas top.
   - Container / node headers: `text_size=12–14` via `text_style=Styles.WhiteBold` (on dark/colored fill) or `Styles.DarkBold` (on light fill).
   - Metadata / annotations: `text_size=9–11` via `Styles.Muted.patch(text_size=10)` or `Styles.Dark`.
   - **Neutral Text Rule**: Never use `Styles.Primary` or `Styles.Secondary` for general text, titles, or body labels without deliberate reason. Default to `Styles.Dark` on light backgrounds and `Styles.Light` / `Styles.White` on dark backgrounds.
2. **Avoid Hardcoding Hex Colors**:
   - Prefer style presets (`Styles.DarkBold`, `Styles.WhiteBold`, `Styles.Muted`) over explicit `#RRGGBB` strings to maintain harmony across light/dark themes.
3. **Prevent Text Collision**:
   - Allow at least 2 coordinate units of margin between shape boundaries and text borders.
   - For long labels, insert explicit `\n` line breaks rather than letting text overflow the shape width.
4. **Use Shape Text Integration**:
   - Embed labels directly into `rectangle(..., text="...", text_style=Styles.WhiteBold)` instead of manually calculating midpoints for a separate `text()` call.
