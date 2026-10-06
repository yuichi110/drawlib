# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Autonomous AI Coding Agent visual self-improvement loop illustration."""

from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines_curved
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=64, dpi=200, color=Colors.Canvas)

# Outer Loop Container (Autonomous AI Zone: x=19..85, y=2.5..61.5)
rectangle((52, 32), width=66, height=59, r=3, style=Styles.MutedDashed)
phosphor.arrows_clockwise((29.5, 58.2), width=3.8, style=Styles.Primary)
text(
    (54, 58.2),
    "Autonomous AI Self-Improvement Loop",
    style=Styles.PrimaryBold.patch(text_size=9.2),
)

# 1. Left: Human Developer (x=1.5..15.5, y=21..38)
rectangle((8.5, 29.5), width=14, height=17, r=2, style=Styles.Neutral)
phosphor.user((8.5, 34), width=5.2, style=Styles.Dark)
text((8.5, 27.2), "Developer", style=Styles.DarkBold.patch(text_size=8.2))
text((8.5, 23.5), "High-Level\nGoal / Prompt", style=Styles.Muted.patch(text_size=6.5))

line((15.5, 29.5), (22, 29.5), arrow_head="->", style=Styles.DarkBold)

# 2. Center-Left: AI Coding Agent (Hero Focal Point: x=22..48, y=21..38)
rectangle((35, 29.5), width=26, height=17, r=2.5, style=Styles.PrimaryFlat)
phosphor.robot((26.5, 29.5), width=5.6, style=Styles.White)
text((38, 32.0), "AI Coding Agent", style=Styles.WhiteBold.patch(text_size=8.8))
text((38, 27.0), "Write / Fix Python\n& Markdown Code", style=Styles.White.patch(text_size=7.2))

# 3. Above Agent: On-Demand Rules, Specs & Best Practices (x=22..48, y=44..54.5)
rectangle((35, 49.25), width=26, height=10.5, r=2, style=Styles.PrimaryNeutral)
phosphor.book_open_text((26.5, 49.25), width=4.8, style=Styles.Primary)
text((38, 51.0), "Specs & Best Practices", style=Styles.DarkBold.patch(text_size=7.6))
text((38, 47.2), "drawlib rules show", style=Styles.PrimaryBold.patch(text_size=7.0))

# Agent autonomously queries Specs & Best Practices (<->)
line((35, 38), (35, 44), arrow_head="<->", style=Styles.PrimaryBold)
text((40.5, 41), "Lookup", style=Styles.PrimaryBold.patch(text_size=7.2))

# 4. Center-Right: Headless Render Preview with Coordinate Grid (x=55.5..81.5, y=21..38)
line((48, 29.5), (55.5, 29.5), arrow_head="->", style=Styles.DarkBold)

rectangle((68.5, 29.5), width=26, height=17, r=2, style=Styles.Neutral)
phosphor.grid_four((60, 29.5), width=5.6, style=Styles.Primary)
text((71.5, 32.0), "Render Preview", style=Styles.DarkBold.patch(text_size=8.5))
text((71.5, 27.0), "drawlib show -g\n(Coordinate Grid)", style=Styles.Muted.patch(text_size=7.2))

# 5. Bottom: Multimodal Visual Inspection (x=35..69, y=6.5..17.5)
rectangle((52, 12), width=34, height=11, r=2, style=Styles.SecondaryNeutral)
phosphor.eye((39.5, 12), width=5.2, style=Styles.Secondary)
text((55, 13.8), "Visual Inspection", style=Styles.DarkBold.patch(text_size=8.5))
text((55, 10.0), "Check layout, overlap & style rules", style=Styles.Muted.patch(text_size=6.8))

# Curved feedback path: Render (bottom) -> Visual Inspection (right) -> AI Agent (bottom)
lines_curved(
    [(74, 21), (74, 12), (69, 12)],
    r=2.5,
    arrow_head="->",
    style=Styles.SecondaryBold,
)
lines_curved(
    [(35, 12), (28, 12), (28, 21)],
    r=2.5,
    arrow_head="->",
    style=Styles.WarningBold,
)
text((31.5, 4.8), "Self-Repair Coordinates & Styles", style=Styles.WarningBold.patch(text_size=7.0))

# 6. Right: Published Docs (x=91.5..118.5, y=20..39)
line((81.5, 29.5), (91.5, 29.5), arrow_head="->", style=Styles.SuccessBold)
text((86.5, 32.2), "Pass", style=Styles.SuccessBold.patch(text_size=7.8))

rectangle((105, 29.5), width=27, height=19, r=2, style=Styles.SuccessNeutral)
phosphor.seal_check((105, 34.5), width=6.0, style=Styles.Success.patch(icon_style="fill"))
text((105, 27.2), "Published Docs", style=Styles.DarkBold.patch(text_size=8.8))
text((105, 22.8), "HTML Site / PDF /\nGitHub MD / Slide", style=Styles.Muted.patch(text_size=7.0))

save()
