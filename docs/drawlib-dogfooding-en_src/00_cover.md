# Automated Documentation with Drawlib & AI

Illustrated Documentation as Code in the AI Era

```drawlib 640px center file:fig_cover_autonomous_loop.png caption:"Autonomous AI Visual Self-Correction Loop"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=52)

ts = Styles.WhiteBold.patch(text_size=9.5)

# 1. Inspect Context
rectangle((20.5, 18), width=25, height=20, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.file_code(xy=(20.5, 23.5), width=5.5, style=Styles.White)
text((20.5, 13.5), text="1. Inspect Context\n(Code & Architecture)", style=ts)

# 2. Generate Code
rectangle((51.0, 18), width=25, height=20, style=Styles.AccentFlat.patch(shape_r=2.0))
phosphor.code(xy=(51.0, 23.5), width=5.5, style=Styles.White)
text((51.0, 13.5), text="2. Generate Code\n(Declarative Python)", style=ts)

# 3. Render with Grid
rectangle((81.5, 18), width=25, height=20, style=Styles.SecondaryFlat.patch(shape_r=2.0))
phosphor.image(xy=(81.5, 23.5), width=5.5, style=Styles.White)
text((81.5, 13.5), text="3. Render with Grid\n(drawlib show -g)", style=ts)

# 4. Autonomous Review
rectangle((112.0, 18), width=25, height=20, style=Styles.SuccessFlat.patch(shape_r=2.0))
phosphor.eye(xy=(112.0, 23.5), width=5.5, style=Styles.White)
text((112.0, 13.5), text="4. Autonomous Review\n(Visual Inspection)", style=ts)

# Forward arrows
line((33.0, 18), (38.5, 18), arrow_head="->", style=Styles.DarkBold)
line((63.5, 18), (69.0, 18), arrow_head="->", style=Styles.DarkBold)
line((94.0, 18), (99.5, 18), arrow_head="->", style=Styles.DarkBold)

# Autonomous feedback loop
line((112.0, 28.0), (112.0, 42.0), style=Styles.DangerBold)
line((112.0, 42.0), (51.0, 42.0), style=Styles.DangerBold)
line((51.0, 42.0), (51.0, 28.0), arrow_head="->", style=Styles.DangerBold)

# Feedback label and icon
phosphor.arrows_clockwise(xy=(57.0, 46.0), width=4.0, style=Styles.Danger)
text((84.0, 46.0), text="Self-correct coordinates & retry upon visual defects (Feedback Loop)", style=Styles.DangerBold.patch(text_size=8.5))
```

**Author**: Drawlib Core Team  
**Audience**: Software Engineers, Architects, and AI Pair Programmers  
**Version**: 0.3.0  
**Date**: October 2026
