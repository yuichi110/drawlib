# Drawlib Quickstart Guide

**Illustration as Code & Documentation as Code in Pure Python**

Drawlib is a modern Python library for creating technical diagrams, architecture blueprints, charts, SmartArts, and publication-ready documentation directly from code.

```drawlib 620px center caption:"Drawlib: Illustration as Code in Pure Python"
from drawlib.canvas import setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=50)

# Left card: Python Code
rectangle(
    xy=(22, 25),
    width=30,
    height=32,
    r=3,
    style=Styles.PrimaryOutline,
)
phosphor.code(xy=(22, 31), width=10, style=Styles.Primary)
text(xy=(22, 16), text="Python Code", style=Styles.PrimaryBold, size=12)

# Arrow 1
line((39, 25), (49, 25), arrowhead="->", style=Styles.PrimaryBold)

# Center card: Drawlib Engine
circle(
    xy=(62, 25),
    radius=14,
    style=Styles.SecondaryOutline,
)
text(xy=(62, 27), text="drawlib", style=Styles.SecondaryBold, size=14)
text(xy=(62, 21), text="Engine", style=Styles.Secondary, size=10)

# Arrow 2
line((78, 25), (88, 25), arrowhead="->", style=Styles.SecondaryBold)

# Right card: Output Formats
rectangle(
    xy=(102, 25),
    width=26,
    height=32,
    r=3,
    style=Styles.AccentOutline,
)
gcp.cloud_run(xy=(102, 31), width=10, style=Styles.Accent)
text(xy=(102, 16), text="PNG / HTML / PDF", style=Styles.AccentBold, size=10)
```

---

### About This Document

This quickstart guide introduces the core workflows of **Drawlib**, from basic canvas coordinates and preset styling to icons, SmartArts, declarative charts, software diagrams, and the unified CLI document builder.

- **Repository**: `https://github.com/yuichi110/drawlib`
- **Author**: Yuichi Ito
- **License**: Apache License, Version 2.0
