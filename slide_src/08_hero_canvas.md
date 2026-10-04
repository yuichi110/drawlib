---
layout: canvas
---

```drawlib (0, 0) (1920, 1080) file:full_hero_canvas.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle, circle
from drawlib.lines import line
from drawlib.styles import Styles, Colors
from drawlib.text import text

clear()
setup(width=192, height=108)

# Full-bleed backdrop
rectangle((96, 54), width=192, height=108, style=Styles.WhiteFlat)

# Outer boundary box
rectangle((96, 54), width=182, height=98, style=Styles.MutedDashed)

# Top Hero Banner
rectangle((96, 90), width=172, height=14, style=Styles.PrimaryFlat,
          text="FULL CANVAS MODE (layout: canvas) — 1920 × 1080 PURE DRAWING STAGE", text_style=Styles.WhiteBold)

# 4 Architectural Pillars
pillars = [
    (29, "1. Deterministic", "Cartesian geometry\nVersion-controlled\nReproducible builds", Styles.PrimaryBold),
    (74, "2. Native SVG", "Ctrl+F Searchable text\nInfinite resolution\nClean DOM integration", Styles.SecondaryBold),
    (119, "3. Multi-Target", "Images, PDF Books\nDocumentation sites\nInteractive HTML decks", Styles.AccentBold),
    (164, "4. AI Autonomous", "Clean token hierarchy\nMulti-modal review loop\nStructured container syntax", Styles.DarkBold),
]

for x, title, desc, title_style in pillars:
    rectangle((x, 50), width=39, height=48, style=Styles.MutedFlat)
    text((x, 66), title, style=title_style)
    text((x, 48), desc, style=Styles.Dark)

# Bottom Feature Callout
rectangle((96, 14), width=172, height=10, style=Styles.PrimaryLight,
          text="Zero Header • Zero Footer • Zero CSS Slot Limits • 100% Code-Driven Visualization", text_style=Styles.PrimaryBold)

save()
```
