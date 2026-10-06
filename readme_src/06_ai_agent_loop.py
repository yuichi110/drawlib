# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI Inner Loop and Human Outer Loop visual self-improvement workflow."""

from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines_curved
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=70, dpi=200, color=Colors.Canvas)

# AI Inner Loop Container (Autonomous Zone: x=19..85, y=11..67.5)
rectangle((52, 39.25), width=66, height=56.5, r=3, style=Styles.MutedDashed)
phosphor.arrows_clockwise((24.5, 64.2), width=3.8, style=Styles.Primary)
text(
    (53.5, 64.2),
    "AI Inner Loop (Autonomous Visual Self-Correction)",
    style=Styles.PrimaryBold.patch(text_size=8.6),
)

# 1. Left: Human Developer (x=1.5..15.5, y=27.5..44.5)
rectangle((8.5, 36), width=14, height=17, r=2, style=Styles.Neutral)
phosphor.user((8.5, 40.5), width=5.2, style=Styles.Dark)
text((8.5, 33.7), "Developer", style=Styles.DarkBold.patch(text_size=8.2))
text((8.5, 30.0), "High-Level\nGoal / Prompt", style=Styles.Muted.patch(text_size=6.5))

line((15.5, 36), (22, 36), arrow_head="->", style=Styles.DarkBold)

# 2. Center-Left: AI Coding Agent (Hero Focal Point: x=22..48, y=27.5..44.5)
rectangle((35, 36), width=26, height=17, r=2.5, style=Styles.PrimaryFlat)
phosphor.robot((26.5, 36), width=5.6, style=Styles.White)
text((38, 38.5), "AI Coding Agent", style=Styles.WhiteBold.patch(text_size=8.8))
text((38, 33.5), "Write / Fix Python\n& Markdown Code", style=Styles.White.patch(text_size=7.2))

# 3. Above Agent: On-Demand Rules, Specs & Best Practices (x=22..48, y=50.25..60.75)
rectangle((35, 55.5), width=26, height=10.5, r=2, style=Styles.PrimaryNeutral)
phosphor.book_open_text((26.5, 55.5), width=4.8, style=Styles.Primary)
text((38, 57.2), "Specs & Best Practices", style=Styles.DarkBold.patch(text_size=7.6))
text((38, 53.5), "drawlib rules show", style=Styles.PrimaryBold.patch(text_size=7.0))

# Agent autonomously queries Specs & Best Practices (<->)
line((35, 44.5), (35, 50.25), arrow_head="<->", style=Styles.PrimaryBold)
text((40.5, 47.4), "Lookup", style=Styles.PrimaryBold.patch(text_size=7.2))

# 4. Center-Right: Headless Render Preview with Coordinate Grid (x=55.5..81.5, y=27.5..44.5)
line((48, 36), (55.5, 36), arrow_head="->", style=Styles.DarkBold)

rectangle((68.5, 36), width=26, height=17, r=2, style=Styles.Neutral)
phosphor.grid_four((60, 36), width=5.6, style=Styles.Primary)
text((71.5, 38.5), "Render Preview", style=Styles.DarkBold.patch(text_size=8.5))
text((71.5, 33.5), "drawlib show -g\n(Coordinate Grid)", style=Styles.Muted.patch(text_size=7.2))

# 5. Bottom of Inner Loop: Multimodal Visual Inspection (x=35..69, y=14.25..24.75)
rectangle((52, 19.5), width=34, height=10.5, r=2, style=Styles.SecondaryNeutral)
phosphor.eye((39.5, 19.5), width=5.2, style=Styles.Secondary)
text((55, 21.2), "Visual Inspection", style=Styles.DarkBold.patch(text_size=8.5))
text((55, 17.5), "Check layout, overlap & style rules", style=Styles.Muted.patch(text_size=6.8))

# Inner Loop feedback path: Render (bottom) -> Visual Inspection (right) -> AI Agent (bottom)
lines_curved(
    [(74, 27.5), (74, 19.5), (69, 19.5)],
    r=2.5,
    arrow_head="->",
    style=Styles.SecondaryBold,
)
lines_curved(
    [(35, 19.5), (28, 19.5), (28, 27.5)],
    r=2.5,
    arrow_head="->",
    style=Styles.WarningBold,
)
text((27.5, 13.0), "Self-Repair", style=Styles.WarningBold.patch(text_size=7.2))

# 6. Right: Published Docs (x=91.5..118.5, y=26.5..45.5)
line((81.5, 36), (91.5, 36), arrow_head="->", style=Styles.SuccessBold)
text((88.2, 38.7), "Pass", style=Styles.SuccessBold.patch(text_size=7.8))

rectangle((105, 36), width=27, height=19, r=2, style=Styles.SuccessNeutral)
phosphor.seal_check((105, 41), width=6.0, style=Styles.Success.patch(icon_style="fill"))
text((105, 33.7), "Published Docs", style=Styles.DarkBold.patch(text_size=8.8))
text((105, 29.3), "HTML Site / PDF /\nGitHub MD / Slide", style=Styles.Muted.patch(text_size=7.0))

# 7. Human Outer Loop: Published Docs (bottom) -> Developer (bottom)
lines_curved(
    [(105, 26.5), (105, 5.2), (8.5, 5.2), (8.5, 27.5)],
    r=3.5,
    arrow_head="->",
    style=Styles.DarkBold,
)
rectangle((53, 5.2), width=52, height=5.2, r=2.2, style=Styles.Neutral)
text(
    (53, 5.2),
    "Human Outer Loop: Review Docs & Refine Direction",
    style=Styles.DarkBold.patch(text_size=7.4),
)

save()
