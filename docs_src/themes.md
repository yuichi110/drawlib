# Themes & Color Palettes Guide

Drawlib encourages separating content (coordinates, item types) from visual presentation (colors, line weights, themes).

---

## 1. Color Palettes (`Colors` & `Colors140`)

Drawlib provides predefined color constants:
- **`Colors`**: Standard primary colors (`Red`, `Blue`, `Green`, `Black`, `White`, `Silver`, `Transparent`).
- **`Colors140`**: 140 CSS named colors (`Turquoise`, `Coral`, `DodgerBlue`, `SlateGray`, etc.).
- **Utility functions**: `from_hex("#6366f1")`, `from_grayscale(0.8)`, `with_alpha(color, 0.5)`.

```drawlib
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140, from_hex, with_alpha
from drawlib.shapes import circle, rectangle
from drawlib.types import ShapeStyle

config(width=100, height=40)

# Custom hex color
circle(
    xy=(25, 20),
    radius=12,
    style=ShapeStyle(fill_color=from_hex("#6366f1"))
)

# Color with transparency (alpha)
rectangle(
    xy=(75, 20),
    width=24,
    height=24,
    style=ShapeStyle(fill_color=with_alpha(Colors140.Tomato, 0.6), line_color=Colors.Navy)
)
```

---

## 2. Using Themes and Preset Styles

Theme styles allow referencing predefined visual classes by string names (e.g., `"blue"`, `"red_fill"`):

```drawlib
from drawlib.canvas import config
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=30)

circle(xy=(30, 15), radius=10, style="blue")
text(xy=(30, 15), text="Theme Blue", style="white")

circle(xy=(70, 15), radius=10, style="red")
text(xy=(70, 15), text="Theme Red", style="white")
```

---

## Navigation

- [Back to Index](./index.md)
- [Next: SmartArts Guide](./smartarts.md)
