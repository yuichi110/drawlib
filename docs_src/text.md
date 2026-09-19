# Text & Typography Guide

Drawlib provides `text()` and `text_vertical()` for rendering crisp text with custom fonts, alignment options, and background formatting.

---

## 1. Basic Text Rendering

```drawlib
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140
from drawlib.text import text
from drawlib.types import TextStyle

config(width=100, height=40)

text(
    xy=(50, 20),
    text="Hello Drawlib Typography!",
    style=TextStyle(
        text_color=Colors140.DarkSlateBlue,
        text_size=18,
        text_halign="center",
        text_valign="center"
    )
)
```

---

## 2. Text Background Formatting

You can specify background fill and border styles directly within `TextStyle`:

```drawlib
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140
from drawlib.text import text
from drawlib.types import TextStyle

config(width=100, height=40)

text(
    xy=(50, 20),
    text="Highlighted Text Box",
    style=TextStyle(
        text_color=Colors.White,
        text_size=16,
        text_bg_fill_color=Colors140.DarkCyan,
        text_bg_line_color=Colors.Navy,
        text_bg_line_width=2
    )
)
```

---

## Navigation

- [Back to Index](./index.md)
- [Next: Icons Guide](./icons.md)
