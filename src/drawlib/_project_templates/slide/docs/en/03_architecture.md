---
header: "Architecture"
layout: split-right
ratio: "4:6"
---

# Scalable Microservices in Code

- **Declarative Python**: Pure code, version-controlled with clean git diffs
- **Vector Native SVG**: Crisp scaling, Ctrl+F searchable text
- **Interactive Deck**: Fullscreen, keyboard shortcuts, overview modal

```drawlib 100% center file:microservices.svg slot:right
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

clear()
setup(width=100, height=60)
rectangle((25, 30), width=30, height=20, style=Styles.PrimaryFlat, text="Client SPA", text_style=Styles.WhiteBold)
rectangle((75, 30), width=30, height=20, style=Styles.SecondaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
line((40, 30), (60, 30), arrow_head="->", style=Styles.PrimaryBold)
save()
```
