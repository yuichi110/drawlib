# Icons Guide

Drawlib includes over 1,500 embedded Phosphor icons accessible via `icon_phosphor`, available in 5 weights (`thin`, `light`, `regular`, `bold`, `fill`).

---

## 1. Phosphor Icons (`icon_phosphor`)



```python
from drawlib.canvas import config
from drawlib.colors import Colors140
from drawlib.icons import icon_phosphor
from drawlib.types import IconStyle

config(width=120, height=40)

# Rocket icon (bold style)
icon_phosphor.rocket(
    xy=(20, 20),
    width=16,
    style=IconStyle(text_color=Colors140.MediumVioletRed, icon_style="bold")
)

# Heart icon (fill style)
icon_phosphor.heart(
    xy=(50, 20),
    width=16,
    style=IconStyle(text_color=Colors140.Crimson, icon_style="fill")
)

# Terminal icon (regular style)
icon_phosphor.terminal(
    xy=(80, 20),
    width=16,
    style=IconStyle(text_color=Colors140.DodgerBlue, icon_style="regular")
)
```

![icons_1](icons_1.png)



---

## Navigation

- [Back to Index](./index.md)
- [Next: Images Guide](./images.md)
