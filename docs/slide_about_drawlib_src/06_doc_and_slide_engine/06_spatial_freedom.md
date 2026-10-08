::: block (1700, 1010) (140, 30) z:20
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (800, 60) z:10
# Spatial Freedom: Full-Bleed & Z-Index Layering
:::

::: block (80, 140) (760, 820) font:20px z:10
## Breaking Free from Rigid Slide Templates

Traditional Markdown-to-slide tools lock you into centered bullet lists. Drawlib gives you **absolute pixel coordinates** plus **`z:<layer>`** stacking:

````markdown
<!-- Layer 1: Right-half full-bleed diagram (Y: 0..1080) -->
::: block (920, 0) (1000, 1080) z:2
```drawlib file:spatial_freedom.svg
setup(width=100, height=108)
```
:::

<!-- Layer 2: Floating glass callout box overlapping the seam! -->
::: box (780, 760) (460, 150) z:15 style:"background: ..."
**Floating Callout (`::: box ... z:15`)**
:::
````

### Container Options Cheat Sheet
- **`z:1` .. `z:20`**: Explicit `z-index` stacking order across overlapping blocks.
- **`::: box` & `style:"..."`**: Apply custom CSS backgrounds, shadows, or glassmorphism cards directly over vector diagrams.
- **`compact` & `font:18px`**: Fine-tune typography density per container.
:::

::: block (920, 0) (1000, 1080) z:2
```drawlib file:spatial_freedom.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=108)

# Full-bleed soft slate backdrop filling right half of 1920x1080 stage (Y: 0..1080)
rectangle(
    (50, 54),
    width=100,
    height=108,
    style=Styles.WhiteFlat.patch(shape_fill_color=(241, 245, 249)),
)
# Left accent border along X=920 seam
rectangle(
    (1.0, 54),
    width=2.0,
    height=108,
    style=Styles.PrimaryFlat,
)

text(
    (52, 99),
    "Right-Half Full-Bleed Canvas  —  ::: block (920, 0) (1000, 1080) z:2",
    style=Styles.PrimaryBold.patch(text_size=9.5),
)

# Multi-layer Z-stack visual diagram inside the full-bleed canvas
# Base Layer card (z:1)
rectangle(
    (46, 68),
    width=68,
    height=38,
    r=2.5,
    style=Styles.White,
)
text((16, 83), "Layer z:1 — Base Architecture Canvas", style=Styles.MutedBold.patch(text_size=8.5, text_halign="left"))
rectangle((28, 65), width=22, height=14, r=1.5, style=Styles.PrimaryNeutral, text="Ingress Edge", text_style=Styles.DarkBold.patch(text_size=8.5))
rectangle((62, 65), width=22, height=14, r=1.5, style=Styles.SecondaryNeutral, text="Core Mesh", text_style=Styles.DarkBold.patch(text_size=8.5))
line((39, 65), (51, 65), arrow_head="->", style=Styles.DarkBold)

# Middle Overlapping Layer card (z:5)
rectangle(
    (58, 44),
    width=66,
    height=30,
    r=2.5,
    style=Styles.BlueNeutral,
)
text((29, 55), "Layer z:5 — Overlapping Telemetry Overlay", style=Styles.PrimaryBold.patch(text_size=8.5, text_halign="left"))
rectangle(
    (45, 41),
    width=26,
    height=12,
    r=1.5,
    style=Styles.PrimaryFlat,
    text="99.99% SLA\nZero Drift",
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)
rectangle(
    (75, 41),
    width=24,
    height=12,
    r=1.5,
    style=Styles.White,
    text="P99: 4.2 ms\nAuto-Scaled",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

# Pointer towards the live HTML floating ::: box at (780, 760)
circle((38, 22), radius=3.0, style=Styles.AccentFlat, text="z:15", text_style=Styles.WhiteBold.patch(text_size=7.5))
line((35, 22), (24, 22), arrow_head="<-", style=Styles.PrimaryBold)
text(
    (43, 22),
    "Live HTML ::: box (z:15) overlaps across X=920 boundary!",
    style=Styles.DarkBold.patch(text_size=8.5, text_halign="left"),
)

save()
```
:::

::: box (760, 740) (520, 165) font:17px z:15 compact style:"background: rgba(15, 23, 42, 0.94); color: #f8fafc; padding: 20px 26px; border-radius: 16px; border: 2px solid #6366f1; box-shadow: 0 20px 40px rgba(15, 23, 42, 0.28);"
**Live Floating Overlay (`::: box (760, 740) (520, 165) z:15`)**

- Bridges the left Markdown column (`X: 80..840`) and right full-bleed SVG (`X: 920..1920`).
- Styled with inline CSS (`rgba` slate background, indigo border, and drop shadow).
:::

::: block (80, 1010) (800, 30) font:14px z:10
*Chapter 6: Documentation & Slide Engine — Spatial Freedom & Z-Index Layering*
:::

::: note
- Look at the right half of this slide: the SVG diagram (`::: block (920, 0) (1000, 1080) z:2`) bleeds all the way from `Y=0` at the top edge to `Y=1080` at the bottom edge.
- And look at the dark indigo card near the bottom center: that is a real `::: box (760, 740) (520, 165) z:15` HTML container floating right across the seam between the left text column and the right full-bleed SVG canvas!
:::
