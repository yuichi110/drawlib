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
# Multilingual Typography & Raster Assets
:::

::: block xy=(80, 145) width=680 height=790
## Universal Scripts & Dimage

- **CJK + Latin Default**: `Font` renders English and Japanese together.
- **Regional Packs**: `FontJapanese`, `FontArabic`, and `FontSourceCode`.
- **Exact Text Anchors**: Control alignment via `halign` and `valign`.
- **Raster `Dimage`**: Crop, resize, sepia, mosaic, plus font caching.
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=typography_i18n.svg
from drawlib.canvas import clear, setup
from drawlib.fonts import Font, FontJapanese, FontSourceCode
from drawlib.images import Dimage, image
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

# Top Panel: Multilingual Typography Cards
Panel(
    "Multilingual Font Families & On-Demand Cache",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    header_height=7.6,
).draw(xy=(2.0, 42.5), width=100.0, height=35.5)

cards = [
    (18.5, Styles.White, "Font.SANSSERIF_BOLD", "English & 日本語", Font.SANSSERIF_BOLD, "Default Latin + CJK"),
    (52.0, Styles.PrimaryNeutral, "FontJapanese.SERIF", "美しい明朝体表現", FontJapanese.SERIF_BOLD, "Regional CJK & RTL"),
    (85.5, Styles.SecondaryNeutral, "FontSourceCode", "setup(104, 80)", FontSourceCode.SOURCECODEPRO, "Monospace Code"),
]
for cx, card_st, badge, sample, fnt, desc in cards:
    rectangle((cx, 56.2), width=30.2, height=22.6, style=card_st.patch(shape_r=1.6))
    text((cx, 63.4), badge, style=Styles.PrimaryBold.patch(text_size=13.5))
    text((cx, 56.2), sample, style=Styles.DarkBold.patch(text_font=fnt, text_size=14.8))
    text((cx, 49.0), desc, style=Styles.Muted.patch(text_size=13.5))

# Bottom Panel: halign Anchor Control + Raster Image / Dimage
Panel(
    "Anchor Alignment (halign) & Raster Assets (Dimage)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    header_height=7.6,
).draw(xy=(2.0, 2.0), width=100.0, height=38.0)

# Left Sub-card: halign (left / center / right) with clear vertical offset above dot
rectangle((29.5, 17.0), width=49.0, height=25.0, style=Styles.White.patch(shape_r=1.6))
ax = 29.5
line((ax, 5.6), (ax, 15.2), style=Styles.PrimaryDashed.patch(line_width=1.4))
line((ax, 19.2), (ax, 28.0), style=Styles.PrimaryDashed.patch(line_width=1.4))

anchors = [
    (22.5, "left", "halign='left'", Styles.DarkBold),
    (14.5, "center", "halign='center'", Styles.PrimaryBold),
    (6.5, "right", "halign='right'", Styles.DarkBold),
]
for ay, ha, lbl, st_txt in anchors:
    circle((ax, ay), radius=0.85, style=Styles.DangerFlat)
    text((ax, ay + 1.5), lbl, style=st_txt.patch(text_size=13.8, halign=ha, valign="bottom"))

# Right Sub-card: _assets/linux.png via image() & Dimage.sepia()
rectangle((78.0, 17.0), width=42.0, height=25.0, style=Styles.White.patch(shape_r=1.6))
text((78.0, 26.5), "_assets/linux.png", style=Styles.SecondaryBold.patch(text_size=13.5))
image((68.5, 17.2), width=8.4, image="_assets/linux.png")
text((68.5, 8.2), "image()", style=Styles.DarkBold.patch(text_size=13.5))

sepia_img = Dimage("_assets/linux.png").sepia()
image((87.5, 17.2), width=8.4, image=sepia_img)
text((87.5, 8.2), ".sepia()", style=Styles.DarkBold.patch(text_size=13.5))
```
:::

::: note
Internationalized documentation often breaks when vector diagram tools lack CJK or right-to-left font coverage. Drawlib's default `Font` family renders Latin and CJK glyphs simultaneously out of the box, while optional regional packs (`FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, `FontThai`, `FontBrahmic`, and `FontSourceCode`) download automatically on demand into `~/.cache/drawlib`. For text placement, `halign` and `valign` give exact anchor control relative to `(x, y)`. Finally, `drawlib.images.image()` and the immutable `Dimage` wrapper let you embed and transform raster assets (`_assets/linux.png`) with crop, resize, sepia, grayscale, or mosaic filters directly in Python.
:::
