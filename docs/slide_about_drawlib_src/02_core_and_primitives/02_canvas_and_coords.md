::: block (80, 50) (1760, 120)
# Cartesian Canvas & Coordinate System (`drawlib.canvas`)
An intuitive, resolution-independent 2D mathematical coordinate space with `(0, 0)` at the bottom-left.
:::

::: block (80, 190) (760, 770) compact
### 1. Canvas Lifecycle

```python
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=100, height=70)
rectangle((50, 35), width=40, height=20,
          style=Styles.PrimaryFlat,
          text="Centered at (50, 35)",
          text_style=Styles.WhiteBold)
save("diagram.svg")
```

### 2. Core Spatial Rules
- **Bottom-Left Origin `(0, 0)`**: `X` increases rightward (`0 → width`); `Y` increases upward (`0 → height`).
- **Center-Anchored Primitives `(cx, cy)`**: Shapes (`rectangle`, `circle`, `cylinder`, `rhombus`, etc.) and icons are anchored at their geometric center `(cx, cy)`, making horizontal (`cy` equal) and vertical (`cx` equal) alignment trivial.
- **Z-Order Layering Discipline**: Draw background containers first, entity shapes second, connector lines third, and foreground badges/text last.
- **10–15% Safe Perimeter Margin**: Keep outer margins clear so labels and arrowheads never clip.
:::

::: block (880, 180) (960, 780)
```drawlib file:cartesian_canvas.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=110, height=88)

# Outer Canvas Frame
rectangle((58, 46), width=92, height=72, style=Styles.LightFlat)

# Safe Perimeter Margin Box (10-15% inset)
rectangle(
    (58, 46),
    width=76,
    height=56,
    r=2,
    style=Styles.MutedDashed,
)
text((58, 70.5), "10-15% Safe Perimeter Margin Zone", style=Styles.MutedBold.patch(text_size=8.5))

# X and Y Axes
line((12, 10), (106, 10), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
line((12, 10), (12, 84), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))

text((104, 5), "+X Axis (width)", style=Styles.DarkBold.patch(text_size=9.5, halign="right"))
text((15, 83), "+Y Axis (height)", style=Styles.DarkBold.patch(text_size=9.5, halign="left"))

# Origin (0, 0) Badge
circle((12, 10), radius=2.0, style=Styles.AccentFlat)
text((16, 6), "Origin (0, 0)\nBottom-Left", style=Styles.AccentBold.patch(text_size=8.5, halign="left"))

# Center-Anchored Hero Shape at (cx, cy)
cx, cy = 58, 44
rectangle(
    (cx, cy),
    width=40,
    height=22,
    r=2.5,
    style=Styles.PrimaryFlat,
    text="Shape Center\n(cx, cy)",
    text_style=Styles.WhiteBold.patch(text_size=10, xy_shift=(0, 3.5)),
)
circle((cx, cy - 4.5), radius=1.6, style=Styles.WhiteFlat)

# Dashed coordinate projection lines
line((12, cy - 4.5), (cx, cy - 4.5), style=Styles.PrimaryDashed)
line((cx, 10), (cx, cy - 4.5), style=Styles.PrimaryDashed)
text((9, cy - 4.5), "cy", style=Styles.PrimaryBold.patch(text_size=9, halign="right"))
text((cx, 6.5), "cx", style=Styles.PrimaryBold.patch(text_size=9))

save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Every Drawlib canvas uses a clean Cartesian coordinate system where `(0, 0)` is at the bottom-left corner, `X` grows to the right, and `Y` grows upward.
- Because primitives are anchored at their geometric center `(cx, cy)` by default, aligning three services horizontally means simply giving them the same `cy` coordinate—regardless of each shape's width or height.
:::
