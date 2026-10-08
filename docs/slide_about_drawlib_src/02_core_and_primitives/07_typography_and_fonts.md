::: block (80, 50) (1760, 120)
# Typography, Alignments & Embedded Fonts (`drawlib.text`, `drawlib.fonts`)
Universal multilingual fonts, explicit anchor alignments, and automatic `@font-face` SVG bundling.
:::

::: block (80, 190) (780, 770) compact
### 1. Horizontal & Vertical Text Primitives

```python
from drawlib.fonts import Font, FontFile, FontMonoSpace, FontRoboto, FontSourceCode
from drawlib.styles import Styles
from drawlib.text import text, text_vertical

# Anchor alignment via text_halign & text_valign
text((20, 60), "Left Anchor",
     style=Styles.DarkBold.patch(text_halign="left"))
text((80, 60), "Right Anchor",
     style=Styles.DarkBold.patch(text_halign="right"))

# Built-in font families & custom TTF/OTF files
text((50, 40), "Roboto Bold",
     style=Styles.PrimaryBold.patch(text_font=FontRoboto.ROBOTO_BOLD))
text((50, 25), "Custom FontFile(.ttf)",
     style=Styles.AccentBold.patch(text_font=FontFile("brand.ttf")))

# Vertically stacked characters
text_vertical((12, 30), "TIER", style=Styles.MutedBold)
```

### 2. Automatic SVG `@font-face` Bundling
- When compiling slides or docs with `.svg` diagrams, Drawlib automatically copies required `.ttf`/`.otf` font files into `_assets/fonts/` and injects `@font-face` rules so browsers and PDF exports render identically anywhere.
:::

::: block (900, 180) (940, 780)
```drawlib file:typography_showcase.svg
from drawlib.canvas import clear, save, setup
from drawlib.fonts import Font, FontMonoSpace, FontRoboto, FontSourceCode
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text, text_vertical

clear()
setup(width=100, height=82)

# Top Card: Anchor Alignment Precision (text_halign & text_valign)
rectangle((50, 65), width=90, height=26, r=2.5, style=Styles.LightFlat)
text((10, 74), "1. Explicit Anchor Alignment (text_halign)", style=Styles.DarkBold.patch(text_size=9.5, text_halign="left"))

line((50, 54), (50, 71), style=Styles.PrimaryDashed.patch(line_width=1.5))

circle((50, 68), radius=1.0, style=Styles.AccentFlat)
text((50, 68), '  halign="left"', style=Styles.DarkBold.patch(text_size=9.0, text_halign="left"))

circle((50, 62), radius=1.0, style=Styles.AccentFlat)
text((50, 62), 'halign="center"', style=Styles.PrimaryBold.patch(text_size=9.0, text_halign="center"))

circle((50, 56), radius=1.0, style=Styles.AccentFlat)
text((50, 56), 'halign="right"  ', style=Styles.DarkBold.patch(text_size=9.0, text_halign="right"))

# Bottom Card: Font Families & Vertical Text
rectangle((50, 26), width=90, height=44, r=2.5, style=Styles.Neutral)

# Vertical text badge on left
rectangle((13, 26), width=9, height=36, r=2.0, style=Styles.PrimaryFlat)
text_vertical((13, 26), "FONTS", style=Styles.WhiteBold.patch(text_size=9.5))

# Font family specimens
text(
    (22, 41),
    "Font.SANSSERIF_BOLD — Universal Latin + CJK",
    style=Styles.DarkBold.patch(text_font=Font.SANSSERIF_BOLD, text_size=9.5, text_halign="left"),
)
text(
    (22, 33),
    "FontRoboto.ROBOTO_REGULAR — Clean Western UI",
    style=Styles.PrimaryBold.patch(text_font=FontRoboto.ROBOTO_REGULAR, text_size=9.5, text_halign="left"),
)
text(
    (22, 25),
    "FontMonoSpace.ROBOTO_MONO_REGULAR — 10.0.0.1:443",
    style=Styles.Dark.patch(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=9.0, text_halign="left"),
)
text(
    (22, 17),
    "FontSourceCode.SOURCECODEPRO — def draw():",
    style=Styles.SecondaryBold.patch(text_font=FontSourceCode.SOURCECODEPRO, text_size=9.0, text_halign="left"),
)
text(
    (22, 9),
    "Line Spacing & Rotation (angle=0..360, text_line_spacing)",
    style=Styles.MutedBold.patch(text_size=8.5, text_halign="left"),
)

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
- Typography in Drawlib is handled through `drawlib.text` and `drawlib.fonts`.
- `text()` and `text_vertical()` support exact horizontal (`left`, `center`, `right`) and vertical (`bottom`, `center`, `top`) anchor alignment.
- Built-in font families include `Font` (universal Noto Sans/Serif with CJK), `FontRoboto`, `FontMonoSpace`, `FontSourceCode`, regional scripts, and `FontFile` for custom `.ttf`/`.otf` assets—all automatically bundled into `_assets/fonts/` for SVG rendering.
:::
