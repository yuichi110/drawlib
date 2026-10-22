# Automated Documentation with Drawlib & AI

Illustrated Documentation as Code in the AI Era

```drawlib align=center file=fig_cover_autonomous_loop.png caption="Autonomous AI Visual Self-Correction Loop"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=48)

ts_dark = Styles.DarkBold.patch(text_size=10.5)
ts_white = Styles.WhiteBold.patch(text_size=10.5)

# 1. Inspect Context (Neutral)
rectangle((18.0, 16.5), width=25, height=21, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_code(xy=(18.0, 21.5), width=5.2, style=Styles.Dark)
text((18.0, 12.5), text="1. Inspect Context\n(Code & Design)", style=ts_dark)

# 2. Generate Code (PrimaryFlat — Focal)
rectangle((48.0, 16.5), width=25, height=21, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.code(xy=(48.0, 21.5), width=5.2, style=Styles.White)
text((48.0, 12.5), text="2. Generate Code\n(Declarative Python)", style=ts_white)

# 3. Render with Grid (PrimaryNeutral)
rectangle((78.0, 16.5), width=25, height=21, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.image(xy=(78.0, 21.5), width=5.2, style=Styles.Primary)
text((78.0, 12.5), text="3. Render with Grid\n(drawlib show -g)", style=ts_dark)

# 4. Autonomous Review (SecondaryNeutral)
rectangle((108.0, 16.5), width=25, height=21, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.eye(xy=(108.0, 21.5), width=5.2, style=Styles.Secondary)
text((108.0, 12.5), text="4. Autonomous Review\n(Visual Inspection)", style=ts_dark)

# Forward arrows
line((30.5, 16.5), (35.5, 16.5), arrow_head="->", style=Styles.DarkBold)
line((60.5, 16.5), (65.5, 16.5), arrow_head="->", style=Styles.DarkBold)
line((90.5, 16.5), (95.5, 16.5), arrow_head="->", style=Styles.DarkBold)

# Autonomous feedback loop
line((108.0, 27.0), (108.0, 38.5), style=Styles.DangerBold)
line((108.0, 38.5), (48.0, 38.5), style=Styles.DangerBold)
line((48.0, 38.5), (48.0, 27.0), arrow_head="->", style=Styles.DangerBold)

# Feedback label and icon
phosphor.arrows_clockwise(xy=(49.0, 43.0), width=4.0, style=Styles.Danger)
text((52.5, 43.0), text="Self-correct coordinates & retry on defects (Feedback Loop)", style=Styles.DangerBold.patch(text_size=10.5, halign="left"))

save()
```

**Author**: Drawlib Core Team  
**Audience**: Software Engineers, Architects, and AI Pair Programmers  
**Version**: 0.3.0  
**Date**: October 2026
