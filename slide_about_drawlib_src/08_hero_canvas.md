::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (0, 0) (1920, 1080)
```drawlib file:full_hero_canvas.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle, circle
from drawlib.lines import line
from drawlib.styles import Style, Styles, Colors
from drawlib.text import text

clear()
setup(width=192, height=108)

# Full-bleed backdrop
rectangle((96, 54), width=192, height=108, style=Styles.WhiteFlat)

# Outer boundary box
rectangle((96, 54), width=182, height=98, style=Styles.MutedDashed)

# Top Hero Banner
rectangle((96, 90), width=172, height=14, style=Styles.PrimaryFlat,
          text="FULL CANVAS STAGE — 1920 × 1080 PURE DRAWING STAGE", text_style=Styles.WhiteBold)

# 4 Architectural Pillars
pillars = [
    (29, phosphor.compass, "1. Deterministic", "Cartesian geometry\nVersion-controlled\nReproducible builds", Styles.PrimaryBold, Styles.Primary),
    (74, phosphor.file_svg, "2. Native SVG", "Ctrl+F Searchable text\nInfinite resolution\nClean DOM integration", Styles.SecondaryBold, Styles.Secondary),
    (119, phosphor.stack, "3. Multi-Target", "Images, PDF Books\nDocumentation sites\nInteractive HTML decks", Styles.AccentBold, Styles.Accent),
    (164, phosphor.robot, "4. AI Autonomous", "Clean token hierarchy\nMulti-modal review loop\nStructured container syntax", Styles.DarkBold, Styles.Dark),
]

desc_style = Styles.Dark.patch(text_size=11, text_line_spacing=1.45)
for x, icon_fn, title, desc, title_style, icon_style in pillars:
    rectangle((x, 50), width=39, height=48, style=Styles.Neutral)
    icon_fn((x, 66.5), width=7.5, style=icon_style)
    text((x, 57), title, style=title_style.patch(text_size=13.5))
    text((x, 40), desc, style=desc_style)

# Bottom Feature Callout
rectangle((96, 14), width=172, height=10, style=Styles.PrimaryNeutral,
          text="Zero Injected Chrome • Full Stage Freedom • 100% Code-Driven Visualization", text_style=Styles.PrimaryBold)

save()
```
:::
