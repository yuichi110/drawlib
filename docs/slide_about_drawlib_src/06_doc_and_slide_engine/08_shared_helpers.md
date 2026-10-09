::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Project-Wide Consistency with `styles.py` & `utils.py`
:::

::: block (80, 140) (740, 840) font:20px
## DRY Presentation Engineering at Scale

Maintaining visual consistency across a 60+ slide deck in GUI tools is tedious and error-prone. Drawlib solves this with two shared Python modules in `slide_src/`:

### 1. `styles.py` — Global Design Tokens
```python
from drawlib.preset_colors import DefaultColors
from drawlib.preset_styles import DefaultStyles

Colors = DefaultColors()   # Or GoogleColors, MonochromeColors
Styles = DefaultStyles()   # Or GoogleStyles, MonochromeStyles
```
Switching a 64-slide presentation from `DefaultStyles` to `GoogleStyles` or `MonochromeStyles` is a **two-line change** in `styles.py`.

### 2. `utils.py` — Reusable Slide Macros
- **`utils.draw_page_number()`**: Renders `current_slide.text` (`"42 / 64"`) on a transparent canvas (`alpha=0.0`).
- **`utils.draw_chapter_divider(...)`**: Full-bleed 16:9 chapter cover with progress dots and topic cards.
- **`utils.draw_kpi_cards(...)` & `utils.draw_curved_agenda(...)`**: Data-driven visual macros callable in 3 lines of Python.
:::

::: block (860, 140) (980, 840)
```drawlib file:shared_helpers.svg
import utils
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75), "Centralized Theme & Helper Architecture (Zero Copy-Paste)", style=Styles.DarkBold.patch(text_size=11.5))

# Top Left: styles.py box
rectangle(
    (27.0, 61.5),
    width=40.0,
    height=17.0,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    text="slide_src/styles.py\n• DefaultStyles / GoogleStyles\n• Injected into drawlib.styles\n• Automatic SQLite cache invalidation",
    text_style=Styles.WhiteBold.patch(text_size=8.2),
)

# Top Right: utils.py box
rectangle(
    (71.0, 61.5),
    width=40.0,
    height=17.0,
    style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    text="slide_src/utils.py\n• draw_page_number()\n• draw_chapter_divider()\n• draw_kpi_cards() / draw_curved_agenda()",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)

# Fan-out arrows to 64 slides
for tx in [22.0, 49.0, 76.0]:
    line((27.0, 53.0), (tx, 45.5), arrow_head="->", style=Styles.PrimaryBold)
    line((71.0, 53.0), (tx, 45.5), arrow_head="->", style=Styles.DarkBold)

slide_cards = [
    (22.0, "01_section.md\nutils.draw_chapter_divider(...)"),
    (49.0, "02..08 Content Slides\nfrom drawlib.styles import Styles"),
    (76.0, "Page Counter Block\nutils.draw_page_number()"),
]
for sx, s_txt in slide_cards:
    rectangle(
        (sx, 41.0),
        width=25.0,
        height=8.5,
        style=Styles.White.patch(shape_r=1.2),
        text=s_txt,
        text_style=Styles.DarkBold.patch(text_size=7.6),
    )

# Bottom Live Demo: Calling utils.draw_kpi_cards() inside a sub-region or showing KPI card anatomy
rectangle((49.0, 19.5), width=84.0, height=25.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text(
    (49.0, 29.0),
    "Live Reusable Component Pattern: One Call Updates All 64 Slides",
    style=Styles.PrimaryBold.patch(text_size=9.2),
)

demo_badges = [
    (22.0, "2 Lines", "Switch Entire Deck Theme\nin styles.py", Styles.PrimaryFlat, Styles.WhiteBold),
    (49.0, "3 Lines", "Embed Dynamic Page Counter\nvia current_slide.text", Styles.White, Styles.DarkBold),
    (76.0, "100% DRY", "Shared Chapter Dividers &\nService Card Macros", Styles.White, Styles.DarkBold),
]
for bx, b_num, b_desc, b_st, b_tst in demo_badges:
    rectangle((bx, 16.5), width=24.0, height=14.5, style=b_st.patch(shape_r=1.5))
    text((bx, 19.8), b_num, style=b_tst.patch(text_size=10.5))
    sub_c = Styles.White.patch(text_size=7.5) if b_st == Styles.PrimaryFlat else Styles.Muted.patch(text_size=7.5)
    text((bx, 13.0), b_desc, style=sub_c)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 6: Documentation & Slide Engine — Project-Wide Consistency (styles.py & utils.py)*
:::

::: note
- Notice how every single slide in this 64-slide deck shares the exact same page number counter (`utils.draw_page_number()`) and chapter divider (`utils.draw_chapter_divider()`).
- Furthermore, Drawlib hashes `styles.py`, `utils.py`, and `total_slides` into the SQLite build cache key—so editing a helper in `utils.py` or changing a theme in `styles.py` automatically invalidates and rebuilds affected diagrams!
:::
