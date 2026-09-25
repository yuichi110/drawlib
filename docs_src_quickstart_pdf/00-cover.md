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

config(width=120, height=50)

# Left card: Python Code
rectangle(
    xy=(22, 25),
    width=30,
    height=32,
    r=3,
    style=styles.primary.patch(
        shape_fill_color=Colors140.AliceBlue,
        shape_line_color=Colors140.RoyalBlue,
        shape_line_width=2,
    ),
)
phosphor.code(xy=(22, 31), width=10, style=styles.blue)
text(xy=(22, 16), text="Python Code", style=styles.primary.patch(text_color=Colors.Navy, text_size=12))

# Arrow 1
line((39, 25), (49, 25), arrowhead="->", style=styles.blue)

# Center card: Drawlib Engine
circle(
    xy=(62, 25),
    radius=14,
    style=styles.primary.patch(
        shape_fill_color=Colors140.Turquoise,
        shape_line_color=Colors.Navy,
        shape_line_width=2,
    ),
)
text(xy=(62, 27), text="drawlib", style=styles.primary.patch(text_color=Colors.Navy, text_size=14))
text(xy=(62, 21), text="Engine", style=styles.primary.patch(text_color=Colors.Navy, text_size=10))

# Arrow 2
line((78, 25), (88, 25), arrowhead="->", style=styles.blue)

# Right card: Output Formats
rectangle(
    xy=(102, 25),
    width=26,
    height=32,
    r=3,
    style=styles.primary.patch(
        shape_fill_color=Colors140.LavenderBlush,
        shape_line_color=Colors140.Crimson,
        shape_line_width=2,
    ),
)
gcp.cloud_run(xy=(102, 31), width=10, style=styles.primary)
text(xy=(102, 16), text="PNG / HTML / PDF", style=styles.primary.patch(text_color=Colors.Navy, text_size=10))
```

---

### About This Document

This quickstart guide introduces the core workflows of **Drawlib**, from basic canvas coordinates and preset styling to icons, SmartArts, declarative charts, software diagrams, and the unified CLI document builder.

- **Repository**: `https://github.com/yuichi110/drawlib`
- **Author**: Yuichi Ito
- **License**: Apache License, Version 2.0
