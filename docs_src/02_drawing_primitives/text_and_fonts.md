# Text & Typography

Clear typography and precise alignment are essential for readable technical diagrams. 
Drawlib provides horizontal text, vertical CJK text, arbitrary rotation, multiline wrapping, and built-in universal typography.

---

## 1. Overview of Text Rendering

```drawlib 650px center caption:"Text Alignment, Rotation, and Vertical Typography"
from drawlib.canvas import setup
from drawlib.text import text, text_vertical
from drawlib.shapes import circle
from drawlib.styles import Styles

setup(width=120, height=50)

# 1. Alignment anchors (red dots mark coordinate anchor xy)
circle((30, 35), radius=1.5, style=Styles.danger_flat)
text((30, 35), "Left-Aligned", style=Styles.primary_bold.patch(text_halign="left", text_valign="center"))

circle((30, 20), radius=1.5, style=Styles.danger_flat)
text((30, 20), "Center-Aligned", style=Styles.primary_bold.patch(text_halign="center", text_valign="center"))

circle((30, 5), radius=1.5, style=Styles.danger_flat)
text((30, 5), "Right-Aligned", style=Styles.primary_bold.patch(text_halign="right", text_valign="center"))

# 2. Rotated text
text((75, 25), "Rotated 45°", angle=45, style=Styles.accent_bold)

# 3. Japanese Vertical text
text_vertical((105, 40), "縦書き日本語", style=Styles.secondary_bold)
```

---

## 2. Text Functions

### 2.1. Standard Horizontal Text (`text`)

```python
text(
    xy: tuple[float, float],
    text: str,
    angle: float = 0.0,
    style: Style | str | None = None,
)
```

- **`xy`**: Coordinate anchor point `(x, y)`.
- **`text`**: The string content. Use `\n` to insert line breaks.
- **`angle`**: Counter-clockwise rotation angle around `xy`.
- **`style`**: Text styling (color, font size, weight, alignment).

### 2.2. Vertical CJK Text (`text_vertical`)

Renders East Asian characters (Japanese, Chinese) in traditional top-to-bottom vertical layout:

```python
from drawlib.text import text_vertical
from drawlib.styles import Styles

text_vertical((10, 80), "設計仕様書", style=Styles.primary_bold)
```

---

## 3. Alignment Engines (`halign` & `valign`)

By default, text is centered horizontally and vertically at `xy`. You can alter the alignment using style attributes:

- **`text_halign`**:
  - `"center"` *(default)*: Centered horizontally at `x`.
  - `"left"`: Left edge starts at `x`.
  - `"right"`: Right edge ends at `x`.
- **`text_valign`**:
  - `"center"` *(default)*: Centered vertically at `y`.
  - `"top"`: Top edge touches `y`.
  - `"bottom"`: Baseline touches `y`.

```python
# Align text neatly to the right of an icon or pin
text(
    (55, 30),
    "Aligned Label",
    style=Styles.bold.patch(text_halign="left", text_valign="center"),
)
```

---

## 4. Built-in Font System (`drawlib.fonts`)

Drawlib bundles high-quality, open-source Google Noto and Roboto fonts with universal multilingual CJK fallback:

| Font Class | Family | Ideal Use Case |
| :--- | :--- | :--- |
| `FontRoboto` | Roboto | Standard UI labels, titles, clean sans-serif typography. |
| `FontSourceCode` | Source Code Pro | Monospace code blocks, ASCII schemas, hex values. |
| `FontSansSerif` | Noto Sans | Universal sans-serif with fallback. |
| `FontSerif` | Noto Serif | Formal editorial publications and academic prints. |
| `FontJapanese` | Noto Sans JP | Optimized Japanese typography with Kanji/Kana balance. |
| `FontChinese` | Noto Sans SC | Simplified Chinese typography. |
| `FontKorean` | Noto Sans KR | Hangul typography. |
| `FontFile` | Custom TTF/OTF | Load external brand fonts from arbitrary file paths. |

### Applying Fonts to Styles

```python
from drawlib.fonts import FontSourceCode
from drawlib.text import text
from drawlib.styles import Styles

# Monospace code label
text(
    (50, 20),
    "SELECT * FROM users;",
    style=Styles.bold.patch(text_font=FontSourceCode.SOURCECODEPRO_REGULAR, text_size=14),
)
```
