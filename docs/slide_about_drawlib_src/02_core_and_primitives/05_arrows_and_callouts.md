::: block (80, 50) (1760, 120)
# Block Arrows & Callouts (`arrow`, `arrow_l`, `arrow_u`, `arrow_arc`)
2D filled planar block arrows and speech callouts for prominent phase transitions and annotations.
:::

::: block (80, 190) (780, 770) compact
### 5 Directed Block Arrows + Speech Callouts

```python
from drawlib.shapes import (
    arrow, arrow_arc, arrow_l, arrow_polyline, arrow_u, bubblespeech,
)
from drawlib.styles import Styles

# 1. Straight block arrow (supports embedded shaft text)
arrow((10, 66), (48, 66), tail_width=4, head_width=9,
      head_length=6, style=Styles.PrimaryFlat,
      text="Data Transfer", text_style=Styles.WhiteBold)

# 2. L-shaped & U-turn block arrows (with rounded elbow r)
arrow_l((25, 42), width=26, height=18, tail_width=3.5,
        head_width=8, head_length=6, r=4, style=Styles.SecondaryNeutral)
arrow_u((68, 42), width=24, height=20, tail_width=3.5,
        head_width=8, head_length=6, r=4, style=Styles.BlueNeutral)

# 3. Circular arc & multi-segment polyline block arrows
arrow_arc((25, 16), width=22, height=18, angle_start=180,
          angle_end=20, tail_width=3, head_width=7, style=Styles.PrimaryNeutral)
arrow_polyline([(52, 10), (66, 10), (66, 22), (88, 22)],
               tail_width=3, head_width=7, head_length=5, r=3,
               style=Styles.Neutral)
```

- **Note**: `arrow()` supports embedded `text`; for `arrow_l`, `arrow_u`, `arrow_arc`, and `arrow_polyline`, place external `text()` labels alongside the shaft.
:::

::: block (900, 180) (940, 780)
```drawlib file:block_arrows.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import (
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    bubblespeech,
    rectangle,
)
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=82)

# Row 1: Straight Block Arrow + Speech Callout
rectangle((50, 68), width=90, height=22, r=2.5, style=Styles.LightFlat)
arrow(
    (12, 68),
    (52, 68),
    tail_width=5.5,
    head_width=11,
    head_length=7,
    style=Styles.PrimaryFlat,
    text="arrow() with shaft text",
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)
bubblespeech(
    xy=(62, 61),
    width=28,
    height=14,
    tail_edge="left",
    tail_start_ratio=0.3,
    tail_vertex_xy=(55, 68),
    tail_end_ratio=0.7,
    style=Styles.SecondaryNeutral,
    text="bubblespeech()\ncallout tail",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

# Row 2: L-Arrow and U-Arrow
rectangle((27, 41), width=42, height=24, r=2.5, style=Styles.LightFlat)
arrow_l(
    (27, 43),
    width=26,
    height=15,
    tail_width=3.5,
    head_width=8,
    head_length=6,
    r=4,
    style=Styles.PrimaryNeutral,
)
text((27, 32.5), "arrow_l(r=4)", style=Styles.DarkBold.patch(text_size=8.5))

rectangle((73, 41), width=42, height=24, r=2.5, style=Styles.LightFlat)
arrow_u(
    (73, 43),
    width=24,
    height=15,
    tail_width=3.5,
    head_width=8,
    head_length=6,
    r=4,
    style=Styles.BlueNeutral,
)
text((73, 32.5), "arrow_u(r=4)", style=Styles.DarkBold.patch(text_size=8.5))

# Row 3: Arc Arrow and Polyline Arrow
rectangle((27, 14), width=42, height=24, r=2.5, style=Styles.LightFlat)
arrow_arc(
    (27, 16),
    width=24,
    height=14,
    angle_start=200,
    angle_end=20,
    tail_width=3.2,
    head_width=7.5,
    style=Styles.SecondaryNeutral,
)
text((27, 5.5), "arrow_arc()", style=Styles.DarkBold.patch(text_size=8.5))

rectangle((73, 14), width=42, height=24, r=2.5, style=Styles.LightFlat)
arrow_polyline(
    [(57, 11), (71, 11), (71, 21), (88, 21)],
    tail_width=3.2,
    head_width=7.5,
    head_length=5.5,
    r=3.0,
    style=Styles.Neutral,
)
text((73, 5.5), "arrow_polyline(r=3)", style=Styles.DarkBold.patch(text_size=8.5))

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
- Beyond standard geometric shapes, `drawlib.shapes` includes five specialized 2D block arrows (`arrow`, `arrow_l`, `arrow_u`, `arrow_arc`, `arrow_polyline`) and `bubblespeech` callouts.
- Notice how `arrow_l`, `arrow_u`, and `arrow_polyline` accept a corner fillet radius `r` to create smooth, rounded bends automatically.
:::
