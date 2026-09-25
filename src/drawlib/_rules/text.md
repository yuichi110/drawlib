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
from drawlib.colors import Colors, ColorsDefault, ColorsEssentials, ColorsMonochrome
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
    size: float | None = None,
    angle: float = 0,
    style: Style | str | None = None,
    halign: str = "center",
    valign: str = "center",
)
```

#### Parameter Breakdown:
- **`xy` (tuple[float, float])**: The anchor point `(x, y)` on the canvas.
- **`text` (str)**: The string content to render. Supports newline characters (`\n`) for multi-line blocks.
- **`size` (float | None)**: Font size in typographical points (default: 16). Can also be controlled via `style`.
- **`angle` (float)**: Counter-clockwise rotation angle in degrees around the anchor point `xy` (default: 0).
- **`style` (Style | str | None)**: Predefined style name (e.g. `"bold"`, `"blue_bold"`, `"white"`) or a custom `Style` instance.
- **`halign` (str)**: Horizontal alignment relative to `xy`. Options: `"left"`, `"center"`, `"right"`. Default is `"center"`.
- **`valign` (str)**: Vertical alignment relative to `xy`. Options: `"bottom"`, `"center"`, `"top"`. Default is `"center"`.

### 2.2. `text_vertical()` Specification
While uncommon in Western languages, vertical text layout is standard in East Asian typography (Japanese, Chinese). `text_vertical()` stacks glyphs vertically from top to bottom.

```python
text_vertical(
    xy: tuple[float, float],
    text: str,
    size: float | None = None,
    angle: float = 0,
    style: Style | str | None = None,
    halign: str = "center",
    valign: str = "center",
)
```

> **Rule for Vertical Text**: Always use `halign="center"` with `text_vertical()`. Left or right alignments will cause glyph centerlines to drift unevenly across non-monospaced fonts.

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
```python
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=60)

# Anchor point reference marker
anchor = (50, 30)
circle(anchor, radius=0.8, style="red_flat")

# Text aligned left-bottom from the anchor
text(anchor, "Left-Bottom", halign="left", valign="bottom", style="blue_bold")

# Text aligned right-top from the anchor
text(anchor, "Right-Top", halign="right", valign="top", style="green_bold")

save()
```

---

## 4. Pre-defined Text Styles

Drawlib provides systematic pre-defined text style strings based on the active theme palette (`ColorsDefault`, `ColorsMonochrome`, `ColorsEssentials`).

### 4.1. Style Naming Syntax
Text styles follow the convention:
```text
[<color>_]<weight>
```
- If `<color>` is omitted, the theme's primary text color (typically dark charcoal `#222222`) is used.
- Available weight variants:
  - `light`: Thin, delicate typography.
  - `regular` (or color name alone, e.g. `"blue"`): Standard regular weight.
  - `bold`: Emphasized bold weight.

### 4.2. Common Built-in Style Strings
| Style Name | Description | Typical Use |
| :--- | :--- | :--- |
| `"regular"` | Default text color, regular font weight | General body text, descriptions |
| `"bold"` | Default text color, bold font weight | Headings, emphasized terms |
| `"light"` | Default text color, light font weight | Subtitles, secondary captions |
| `"white"` | White text, regular weight | Inverted dark backgrounds |
| `"white_bold"` | White text, bold weight | Primary container labels (buttons, colored boxes) |
| `"white_light"`| White text, light weight | Subordinate text inside dark containers |
| `"blue"`, `"blue_bold"`, `"blue_light"` | Blue palette variations | Interactive elements, links, primary highlights |
| `"green"`, `"green_bold"`, `"green_light"` | Green palette variations | Success states, active services, approvals |
| `"red"`, `"red_bold"`, `"red_light"` | Red palette variations | Errors, failure alerts, deletion warnings |
| `"purple"`, `"purple_bold"` | Purple palette variations | Middleware, specialized engines |
| `"gray"`, `"gray_bold"`, `"gray_light"` | Muted gray variations | Disabled elements, metadata, timestamps |

```python
from drawlib.canvas import config, save
from drawlib.text import text

config(width=100, height=40)
text((20, 30), "Standard Regular", style="regular")
text((20, 20), "Primary Bold", style="bold")
text((20, 10), "Muted Gray", style="gray_light")

text((70, 30), "Active Feature", style="blue_bold")
text((70, 20), "Success Status", style="green_bold")
text((70, 10), "Critical Warning", style="red_bold")
save()
```

---

## 5. Advanced Styling with the `Style` Class

When pre-defined style strings are insufficient, pass a custom `Style` instance to control color, typography, and background framing.

### 5.1. Text Typography Attributes in `Style`
- **`text_color` (tuple | str | Color)**: Color of the glyphs (e.g. `Colors.Blue`, `"#1a73e8"`).
- **`text_size` (float)**: Font size in points (e.g. `12`, `18`, `28`).
- **`text_font` (Font | FontFile)**: Font family definition.
- **`text_halign` (str)**: `"left"`, `"center"`, `"right"`.
- **`text_valign` (str)**: `"bottom"`, `"center"`, `"top"`.

### 5.2. Text Background Box Attributes in `Style`
Drawlib can automatically render a padded background rectangle behind the text block (useful for overlaying readable text across busy diagram lines):
- **`text_bg_fill_color` (tuple | str | Color)**: Background fill color.
- **`text_bg_fill_alpha` (float)**: Transparency of background fill (`0.0` transparent to `1.0` opaque).
- **`text_bg_line_color` (tuple | str | Color)**: Border color of the background box.
- **`text_bg_line_width` (float)**: Border stroke width (set to `0` for borderless background).
- **`text_bg_line_style` (str)**: Border line pattern (`"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`).

```python
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.fonts import FontSerif
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=60)

# Custom typography with background framing
badge_style = Style(
    text_color=Colors.White,
    text_size=14,
    text_font=FontSerif.MERRIWEATHER_REGULAR,
    text_halign="center",
    text_valign="center",
    text_bg_fill_color=Colors.Navy,
    text_bg_fill_alpha=0.9,
    text_bg_line_color=Colors.LightBlue,
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
   - `Font.SANSSERIF_LIGHT`, `Font.SANSSERIF_REGULAR`, `Font.SANSSERIF_BOLD`
   - `Font.SERIF_LIGHT`, `Font.SERIF_REGULAR`, `Font.SERIF_BOLD`
   - Default family: **Noto Sans CJK Japanese** (universal multilingual sans-serif).
2. **`FontSansSerif`**:
   - `FontSansSerif.ROBOTO_REGULAR`, `ROBOTO_BOLD`
   - `FontSansSerif.RALEWAY_REGULAR`, `RALEWAY_BOLD`
   - `FontSansSerif.LATO_REGULAR`, `LATO_BOLD`
3. **`FontSerif`**:
   - `FontSerif.MERRIWEATHER_REGULAR`, `MERRIWEATHER_BOLD`
   - `FontSerif.NOTO_SERIF_REGULAR`, `NOTO_SERIF_BOLD`
4. **`FontMonoSpace` / `FontSourceCode`**:
   - `FontMonoSpace.SOURCECODEPRO_REGULAR`, `SOURCECODEPRO_BOLD`
   - Essential for code blocks, terminal outputs, JSON keys, and monospaced tables.

### 6.2. International & Local Language Fonts
For non-Latin languages requiring specialized typographies:
- **`FontJapanese`**: `FontJapanese.MPLUS1P_REGULAR`, `NOTO_SANS_JP_BOLD`
- **`FontChinese`**: `FontChinese.NOTO_SANS_SC_REGULAR`, `NOTO_SANS_TC_REGULAR`
- **`FontKorean`**: `FontKorean.NOTO_SANS_KR_REGULAR`
- **`FontThai`**: `FontThai.NOTO_SANS_THAI_REGULAR`, `SERIF_REGULAR`
- **`FontArabic`**: `FontArabic.NOTO_SANS_ARABIC_REGULAR`
- **`FontBrahmic`**: Devanagari and Indic font sets.

### 6.3. External Custom Font Files (`FontFile`)
To use custom corporate fonts (TTF/OTF), use `FontFile`:

```python
from drawlib.fonts import FontFile
from drawlib.text import text
from drawlib.types import Style

custom_style = Style(
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
- Line spacing is automatically calculated relative to `size` (or `text_size`).
- The entire multi-line block conforms to the specified `halign` and `valign`.
  - With `halign="center"`, each line is individually centered.
  - With `halign="left"`, all lines align flush to the left boundary.
  - With `halign="right"`, all lines align flush to the right boundary.

```python
from drawlib.canvas import config, save
from drawlib.text import text

config(width=100, height=60)

summary = (
    "Database Cluster (Primary)\n"
    "Status: Healthy (99.99%)\n"
    "Replication: Synchronous (2 Replicas)\n"
    "Region: us-central1"
)

text((50, 30), summary, size=12, halign="center", style="bold")
save()
```

---

## 8. Rotated Text (`angle`)

The `angle` parameter rotates text counter-clockwise around the specified anchor coordinate `xy`.

```python
from drawlib.canvas import config, save
from drawlib.text import text

config(width=100, height=60)

# Vertical axis label (-90 degrees or 90 degrees)
text((10, 30), "Request Throughput (req/sec)", size=12, angle=90, halign="center", style="bold")

# Diagonal watermark / status label (45 degrees)
text((50, 30), "INTERNAL DRAFT ONLY", size=22, angle=45, halign="center", style="gray_light")

save()
```

---

## 9. Embedding Text in Shapes

In Drawlib, you rarely need to call `text()` manually to place labels inside boxes or circles.  
All shape functions (`rectangle`, `circle`, `donuts`, `chevron`, `polygon`, etc.) accept direct text attributes:

```python
from drawlib.shapes import circle, rectangle

# Text centered automatically inside shapes
rectangle(
    (30, 25),
    width=28,
    height=16,
    style="blue_flat",
    text="Gateway API",
    textstyle="white_bold",
)

circle(
    (75, 25),
    radius=10,
    style="green_flat",
    text="Worker Node\n(Active)",
    textstyle="white_bold",
)
```

### Shape Text Parameters:
- **`text` (str)**: Content string (supports `\n`).
- **`textstyle` (str | Style)**: Pre-defined style name (e.g. `"white_bold"`, `"black"`) or custom `Style`.
- **`fontsize` (float | None)**: Direct font size override.
- **`fontcolor` (tuple | str | None)**: Direct font color override.

---

## 10. Agent Practical Implementation Checklist

When adding text to Drawlib illustrations:

1. **Hierarchy First**:
   - Diagram titles: `size=20–24`, `style="bold"`, `halign="center"` at canvas top.
   - Container / node headers: `size=12–14`, `style="white_bold"` (or `"bold"`).
   - Metadata / annotations: `size=9–11`, `style="gray"` or `style="gray_light"`.
2. **Avoid Hardcoding Hex Colors**:
   - Prefer style strings (`"bold"`, `"blue_bold"`, `"white_bold"`) over explicit `#RRGGBB` strings to maintain harmony across light/dark themes.
3. **Prevent Text Collision**:
   - Allow at least 2 coordinate units of margin between shape boundaries and text borders.
   - For long labels, insert explicit `\n` line breaks rather than letting text overflow the shape width.
4. **Use Shape Text Integration**:
   - Embed labels directly into `rectangle(..., text="...", textstyle="white_bold")` instead of manually calculating midpoints for a separate `text()` call.
