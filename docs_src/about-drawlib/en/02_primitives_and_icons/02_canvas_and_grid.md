::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Cartesian Canvas & Visual Grid (-g)
:::

::: block xy=(80, 145) width=680 height=790
## Predictable Math Geometry

- **Bottom-Left Origin**: `(0, 0)` starts bottom-left (`+X` right, `+Y` up).
- **Center Anchor**: `(x, y)` centers every shape, text, and icon.
- **Visual Grid (`-g`)**: Overlay coordinate ticks for exact verification.

```python
setup(width=100, height=60)
st = Styles.PrimaryFlat
rectangle((50, 30), 36, 22, style=st)
save()
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=canvas_coords.svg
from drawlib.canvas import clear, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

panel = Panel(
    "Cartesian Stage: setup(width=100, height=60) + Grid (-g)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    header_height=8.0,
)
panel.draw(xy=(2.0, 2.0), width=100.0, height=76.0)

# Simulated (0..100, 0..60) canvas mapped to ox=15.0..93.0 (w=78.0), oy=12.5..60.5 (h=48.0)
ox, oy = 15.0, 12.5
sx, sy = 0.78, 0.80
cw, ch = 100 * sx, 60 * sy

rectangle((ox + cw / 2, oy + ch / 2), width=cw, height=ch, style=Styles.White.patch(shape_r=0.6))

# Simulated -g 10-unit grid lines & center crosshair
for gx in range(10, 100, 10):
    px = ox + gx * sx
    st_g = Styles.SecondaryDashed.patch(line_width=1.2) if gx == 50 else Styles.MutedDotted.patch(line_width=0.8)
    line((px, oy), (px, oy + ch), style=st_g)
for gy in range(10, 60, 10):
    py = oy + gy * sy
    st_g = Styles.SecondaryDashed.patch(line_width=1.2) if gy == 30 else Styles.MutedDotted.patch(line_width=0.8)
    line((ox, py), (ox + cw, py), style=st_g)

# X & Y tick labels
for gx in (20, 40, 60, 80, 100):
    text((ox + gx * sx, oy - 3.3), str(gx), style=Styles.Muted.patch(text_size=13.5))
for gy in (20, 40, 60):
    text((ox - 2.2, oy + gy * sy), str(gy), style=Styles.Muted.patch(text_size=13.5, halign="right"))

# +X and +Y Cartesian axes + Origin (0, 0)
line((ox, oy), (ox + cw + 4.2, oy), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
line((ox, oy), (ox, oy + ch + 3.8), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
text((ox + cw + 6.4, oy), "+X", style=Styles.DarkBold.patch(text_size=14.5))
text((ox, oy + ch + 6.2), "+Y", style=Styles.DarkBold.patch(text_size=14.5))
circle((ox, oy), radius=1.0, style=Styles.DangerFlat)
text((ox + 1.5, oy - 5.2), "Origin (0, 0)", style=Styles.DangerBold.patch(text_size=13.5))

# Center-anchored rectangle at virtual (38, 30), width=36, height=24
rx, ry = ox + 38 * sx, oy + 30 * sy
rw, rh = 36 * sx, 24 * sy
rectangle((rx, ry), width=rw, height=rh, style=Styles.PrimaryNeutral.patch(shape_r=1.5, shape_line_width=2.2))
line((rx - 2.2, ry), (rx + 2.2, ry), style=Styles.PrimaryBold.patch(line_width=1.6))
line((rx, ry - 2.2), (rx, ry + 2.2), style=Styles.PrimaryBold.patch(line_width=1.6))
circle((rx, ry), radius=0.95, style=Styles.PrimaryFlat)
text((rx, ry + 4.3), "(x, y) = (38, 30)", style=Styles.PrimaryBold.patch(text_size=13.8))
text((rx, ry - 4.3), "Center Anchor", style=Styles.Dark.patch(text_size=13.5))

# Width & Height dimension arrows
line((rx - rw / 2, ry + rh / 2 + 3.0), (rx + rw / 2, ry + rh / 2 + 3.0), arrow_head="<->", style=Styles.SecondaryBold)
text((rx, ry + rh / 2 + 6.2), "width = 36", style=Styles.SecondaryBold.patch(text_size=13.5))
line((rx - rw / 2 - 3.0, ry - rh / 2), (rx - rw / 2 - 3.0, ry + rh / 2), arrow_head="<->", style=Styles.SecondaryBold)
text((rx - rw / 2 - 6.2, ry), "height = 24", style=Styles.SecondaryBold.patch(text_size=13.5, angle=90))

# Center-anchored focal circle at virtual (79, 34), radius=13
cx, cy, cr = ox + 79 * sx, oy + 34 * sy, 13 * sx
circle((cx, cy), radius=cr, style=Styles.PrimaryFlat)
circle((cx, cy), radius=0.95, style=Styles.WhiteFlat)
line((cx, cy), (cx + cr, cy), arrow_head="->", style=Styles.WhiteBold.patch(line_width=1.8))
text((cx + cr / 2, cy + 3.0), "r = 13", style=Styles.WhiteBold.patch(text_size=13.5))
text((cx, cy - cr - 3.6), "(79, 34)", style=Styles.PrimaryBold.patch(text_size=13.8))
```
:::

::: note
Unlike browser DOM or SVG viewports that put `(0, 0)` at the top-left corner and invert the Y axis, Drawlib uses standard textbook Cartesian coordinates inside every canvas: `(0, 0)` sits at the bottom-left, `+X` grows rightward, and `+Y` grows upward. Equally important, every primitive shape, text call, and icon uses center-anchor `(x, y)` coordinates by default, making alignment math trivial—two shapes with the same `y` are guaranteed to align horizontally regardless of their heights. Passing `-g` to `drawlib build` or `drawlib show` overlays a 10-unit coordinate grid and center crosshair for rapid visual QA.
:::
