# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Workflow diagram showing Illustrated Documentation & Slide as Code in Drawlib v0.3."""

from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58, dpi=200, color=Colors.Canvas)

# Outer Git Repository Container
rectangle((60, 29), width=114, height=50, r=3, style=Styles.MutedDashed)
phosphor.git_branch((14, 50.5), width=4.0, style=Styles.Muted)
text((43, 50.5), "Version-Controlled Repository (Single Source of Truth)", style=Styles.MutedBold.patch(text_size=9.5))

# 1. Left Column: Authoring & Source Files (Neutral cards)
rectangle((22, 37), width=28, height=14, r=2, style=Styles.Neutral)
phosphor.file_md((12, 37), width=5.5, style=Styles.Primary)
text((24.5, 39), "docs_src/*.md", style=Styles.DarkBold.patch(text_size=9))
text((24.5, 34.5), "Markdown + ```drawlib", style=Styles.Muted.patch(text_size=7.5))

rectangle((22, 18), width=28, height=14, r=2, style=Styles.SecondaryNeutral)
phosphor.robot((12, 18), width=5.5, style=Styles.Secondary)
text((24.5, 20), "AI Coding Agent", style=Styles.DarkBold.patch(text_size=9))
text((24.5, 15.5), "drawlib rules & show -g", style=Styles.Muted.patch(text_size=7.5))

# Connectors to Compiler
line((36, 37), (47, 31), arrow_head="->", style=Styles.DarkBold)
line((36, 18), (47, 24), arrow_head="->", style=Styles.DarkBold)

# 2. Center Focal Point: Drawlib Compiler (PrimaryFlat hero node)
rectangle((60, 27.5), width=26, height=22, r=2.5, style=Styles.PrimaryFlat)
phosphor.gear_six((60, 33), width=7.0, style=Styles.White)
text((60, 23.5), "drawlib build", style=Styles.WhiteBold.patch(text_size=10.5))
text((60, 19.5), "Unified Compiler", style=Styles.White.patch(text_size=8))

# Connectors to Outputs (distributed start y-coordinates along right edge)
for start_y, target_y in [(33.5, 43.0), (29.5, 32.5), (25.5, 22.0), (21.5, 11.5)]:
    line((73, start_y), (84, target_y), arrow_head="->", style=Styles.DarkBold)

# 3. Right Column: Publication Outputs (Neutral & SuccessNeutral cards)
outputs = [
    (43.0, "HTML Doc Site", "docs_html/ (Search & Nav)", Styles.Neutral, phosphor.globe),
    (32.5, "GitHub Markdown", "docs/ (Markdown + PNG)", Styles.Neutral, phosphor.file_md),
    (22.0, "Publication PDF", "docs.pdf (Vector Print)", Styles.SuccessNeutral, phosphor.file_pdf),
    (11.5, "16:9 Slide Deck", "slide/ (HTML & PDF Deck)", Styles.SecondaryNeutral, phosphor.presentation_chart),
]

for y_pos, title, desc, card_style, icon_fn in outputs:
    rectangle((99, y_pos), width=30, height=8.5, r=1.5, style=card_style)
    icon_fn((87.5, y_pos), width=4.5, style=Styles.Primary)
    text((101.5, y_pos + 1.5), title, style=Styles.DarkBold.patch(text_size=8.5))
    text((101.5, y_pos - 1.8), desc, style=Styles.Muted.patch(text_size=7.0))

save()
