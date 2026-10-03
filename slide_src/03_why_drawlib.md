---
layout: split-right
ratio: "4:6"
header: "Why Drawlib?"
footer: "Drawlib: Illustration as Code"
paginate: true
---

# From Fragile Drawings to Code

Traditional technical diagramming approaches face severe friction:

- **GUI Tools (Visio, Draw.io)**
  Binary files break Git diffs and code reviews. Diagrams quickly fall out of sync with code.
- **Text DSLs (Mermaid, PlantUML)**
  Unpredictable layouts, line crossing disasters, and difficult styling overrides.
- **Matplotlib & Graphviz**
  Heavy low-level boilerplate and unintuitive coordinate systems.

### The Drawlib Solution
Pure Python declarative syntax, unified Google semantic palettes, and pixel-perfect coordinate math.

```drawlib 100% center file:feature_matrix.svg slot:right
from drawlib.canvas import clear, save, setup
from drawlib.fonts import FontRoboto
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Colors, Style, Styles
from drawlib.text import text

clear()
setup(width=130, height=85)
rectangle((65, 42.5), width=126, height=80, style=Styles.WhiteSolid)
text((65, 76), "Illustration Approach Comparison",
     style=Style(text_size=15, text_color=Colors.Blue6, text_font=FontRoboto.ROBOTO_BOLD))

cell_style = Style(text_size=9, text_color=Colors.Black, text_font=FontRoboto.ROBOTO_REGULAR)
table = Table(cell_style=Styles.WhiteFlat, text_style=cell_style,
              header_cell_style=Styles.PrimaryFlat, header_text_style=Styles.WhiteBold,
              border_style=Styles.MutedLight)
table.set_style_cell_evenodd(even_color=Colors.Gray1, even_text_style=cell_style,
                             odd_color=Colors.White, odd_text_style=cell_style)
data = [
    ["Capability", "GUI Tools", "Text DSLs", "Drawlib"],
    ["Git & Code Review", "Binary diffs (poor)", "Text-based (good)", "Pure Python (native)"],
    ["Layout Precision", "Manual dragging", "Rigid & unpredictable", "Pixel-perfect math"],
    ["Rich Components", "Unstandardized", "Limited primitives", "22 Shapes + Diagrams"],
    ["CI/CD Automation", "Manual export", "CLI supported", "Native CLI & cache"],
    ["Design System", "Drifts over time", "Hard to customize", "Global Style Tokens"],
]
table.draw_flexible((7.0, 70.0), [26.0, 28.0, 30.0, 32.0], [8.0]*6, data)
save()
```
