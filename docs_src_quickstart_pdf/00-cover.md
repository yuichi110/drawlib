# Drawlib Quickstart Guide

**Illustration as Code & Documentation as Code in Pure Python**

Drawlib is a modern Python library for creating technical diagrams, architecture blueprints, charts, SmartArts, and publication-ready documentation directly from code.

```drawlib 620px center caption:"Drawlib: Illustration as Code in Pure Python"
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=50)

# Left card: Python Code
rectangle(
    xy=(22, 25),
    width=30,
    height=32,
    r=3,
    style=Style(fill_color=Colors140.AliceBlue, line_color=Colors140.RoyalBlue, line_width=2),
)
phosphor.code(xy=(22, 31), width=10, style="blue")
text(xy=(22, 16), text="Python Code", style=Style(text_color=Colors.Navy, text_size=12))

# Arrow 1
line((39, 25), (49, 25), arrowhead="->", style="blue")

# Center card: Drawlib Engine
circle(
    xy=(62, 25),
    radius=14,
    style=Style(fill_color=Colors140.Turquoise, line_color=Colors.Navy, line_width=2),
)
text(xy=(62, 27), text="drawlib", style=Style(text_color=Colors.Navy, text_size=14))
text(xy=(62, 21), text="Engine", style=Style(text_color=Colors.Navy, text_size=10))

# Arrow 2
line((78, 25), (88, 25), arrowhead="->", style="blue")

# Right card: Output Formats
rectangle(
    xy=(102, 25),
    width=26,
    height=32,
    r=3,
    style=Style(fill_color=Colors140.LavenderBlush, line_color=Colors140.Crimson, line_width=2),
)
gcp.cloud_run(xy=(102, 31), width=10)
text(xy=(102, 16), text="PNG / HTML / PDF", style=Style(text_color=Colors.Navy, text_size=10))
```

---

### About This Document

This quickstart guide introduces the core workflows of **Drawlib**, from basic canvas coordinates and preset styling to icons, SmartArts, declarative charts, software diagrams, and the unified CLI document builder.

- **Repository**: `https://github.com/yuichi110/drawlib`
- **Author**: Yuichi Ito
- **License**: Apache License, Version 2.0
