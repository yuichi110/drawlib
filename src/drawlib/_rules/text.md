# Drawlib Text Guidelines

Render text labels, headers, and multi-line descriptions with font, size, and alignment controls.

## 1. Imports
```python
from drawlib.colors import Colors, ColorsDefault
from drawlib.fonts import Font, FontRoboto, FontSourceCodePro
from drawlib.text import text, text_vertical
from drawlib.types import Style
```

## 2. Core Functions
- `text(xy, text, size=None, color=None, font=None, angle=0, style=None, halign="center", valign="center")`
  - `xy`: Position `(x, y)` of text anchor point.
  - `text`: String content (supports `\n` for multi-line text).
  - `size`: Font size in points (default: 16).
  - `color`: Text color tuple `(r, g, b)` or `Colors.*`.
  - `font`: Font constant (e.g. `Font.SANSSERIF_BOLD`) or path. Default is Noto Sans CJK Japanese.
  - `angle`: Counter-clockwise rotation angle in degrees.
  - `halign`: Horizontal anchor (`"left"`, `"center"`, `"right"`).
  - `valign`: Vertical anchor (`"bottom"`, `"center"`, `"top"`).
- `text_vertical(xy, text, ...)`: Draw vertically aligned CJK / Japanese text.

## 3. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.text import text

config(width=100, height=50)
text((50, 35), "Architecture Overview", size=20, style="bold", halign="center")
text((50, 18), "Microservices\nEvent Bus & Storage", size=14, color=Colors.Gray, halign="center")
save()
```
