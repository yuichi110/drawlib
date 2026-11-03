# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Minimal Frameless 3-Column Social Preview (1280x640): Git Repo -> AI Agent + Drawlib -> Site, Doc, Slide."""

from __future__ import annotations

from drawlib.canvas import save
from drawlib.fonts import FontRoboto, FontSansSerif
from drawlib.icons import ai, devops, phosphor, workspace
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Style, Styles
from drawlib.text import text
from drawlib.utils import (
    draw_flow_arrow,
    draw_folded_file_icon,
    draw_mini_docs_browser,
    draw_soft_card,
    draw_top_brand_bar,
    setup_ogp,
)

setup_ogp(is_dark=False)
draw_top_brand_bar("Illustration & Docs as Code for AI Agents", top_y=55.0)

# 1. Left Card: Git Repo (.md & .py)
draw_soft_card((22.0, 24.5), 29.5, 36.0)
devops.github((15.9, 37.0), width=4.6, style=Styles.Dark)
text(
    (19.3, 37.0),
    "Git Repo",
    style=Styles.DarkBold.patch(
        text_font=FontSansSerif.POPPINS_BOLD,
        text_size=14.8,
        text_color=(15, 23, 42),
        halign="left",
        valign="center",
    ),
)
draw_folded_file_icon((16.0, 23.7), width=10.0, height=13.0, label=".md")
draw_folded_file_icon((28.0, 23.7), width=10.0, height=13.0, label=".py")
rectangle(
    (22.0, 11.2),
    width=24.4,
    height=4.8,
    style=Style(
        shape_fill_color=(241, 245, 249),
        shape_line_color=(203, 213, 225),
        shape_line_width=1.1,
        shape_r=2.4,
    ),
)
text(
    (22.0, 11.2),
    "Single Source of Truth",
    style=Styles.DarkBold.patch(
        text_font=FontRoboto.ROBOTO_BOLD,
        text_size=10.5,
        text_color=(51, 65, 85),
    ),
)

# 2. Center Hero Card: AI Agent + Drawlib
draw_soft_card(
    (63.8, 24.5),
    32.0,
    36.0,
    fill=(45, 98, 237),
    border=(37, 84, 212),
)
for bx, icon_fn in zip([54.6, 63.8, 73.0], [ai.claude, ai.openai, ai.gemini], strict=True):
    circle(
        (bx + 0.2, 35.0 - 0.35),
        radius=3.7,
        style=Styles.Neutral.patch(shape_fill_color=(20, 52, 150, 0.28), shape_line_width=0.0),
    )
    circle(
        (bx, 35.0),
        radius=3.6,
        style=Styles.Neutral.patch(
            shape_fill_color=Colors.White,
            shape_line_color=(219, 234, 254),
            shape_line_width=0.9,
        ),
    )
    icon_fn((bx, 35.0), width=4.5, style=Styles.Primary)

rectangle(
    (63.8 + 0.2, 22.8 - 0.35),
    width=25.6,
    height=10.8,
    style=Styles.Neutral.patch(shape_fill_color=(20, 52, 150, 0.28), shape_line_width=0.0, shape_r=2.4),
)
rectangle(
    (63.8, 22.8),
    width=25.6,
    height=10.8,
    style=Styles.Neutral.patch(
        shape_fill_color=Colors.White,
        shape_line_color=(219, 234, 254),
        shape_line_width=0.9,
        shape_r=2.4,
    ),
)
phosphor.check_circle((56.6, 25.2), width=3.5, style=Styles.Success.patch(icon_style="fill"))
text(
    (59.2, 25.2),
    "Best Practices",
    style=Styles.DarkBold.patch(
        text_font=FontRoboto.ROBOTO_BOLD,
        text_size=11.8,
        text_color=(15, 23, 42),
        halign="left",
        valign="center",
    ),
)
phosphor.arrows_clockwise((56.6, 20.4), width=3.5, style=Styles.Primary.patch(icon_style="bold"))
text(
    (59.2, 20.4),
    "Check/Fix Loop",
    style=Styles.DarkBold.patch(
        text_font=FontRoboto.ROBOTO_BOLD,
        text_size=11.8,
        text_color=(15, 23, 42),
        halign="left",
        valign="center",
    ),
)
text(
    (63.8, 11.2),
    "AI Agent + Drawlib",
    style=Styles.DarkBold.patch(
        text_font=FontSansSerif.POPPINS_BOLD,
        text_size=13.8,
        text_color=Colors.White,
    ),
)

# 3. Right Fanned Outputs: Site, Doc, Slide
draw_mini_docs_browser((101.2, 31.4), width=23.5, height=19.5)

draw_soft_card((116.5, 36.4), 11.6, 6.6, border=(148, 163, 184), r=1.5)
workspace.adobe_acrobat((113.3, 36.4), width=3.9, style=Styles.Primary)
text(
    (116.0, 36.4),
    "PDF",
    style=Styles.DarkBold.patch(
        text_font=FontRoboto.ROBOTO_BOLD,
        text_size=11.0,
        text_color=(15, 23, 42),
        halign="left",
        valign="center",
    ),
)

draw_soft_card((116.6, 28.4), 12.2, 6.6, border=(148, 163, 184), r=1.5)
workspace.word((113.1, 28.4), width=3.9, style=Styles.Primary)
text(
    (115.7, 28.4),
    "DOCX",
    style=Styles.DarkBold.patch(
        text_font=FontRoboto.ROBOTO_BOLD,
        text_size=10.8,
        text_color=(15, 23, 42),
        halign="left",
        valign="center",
    ),
)

draw_soft_card((111.0, 19.6), 17.4, 8.4, border=(100, 116, 139), r=1.6)
workspace.powerpoint((105.8, 19.6), width=4.5, style=Styles.Primary)
text(
    (108.9, 19.6),
    "16:9 PPTX",
    style=Styles.DarkBold.patch(
        text_font=FontRoboto.ROBOTO_BOLD,
        text_size=11.5,
        text_color=(15, 23, 42),
        halign="left",
        valign="center",
    ),
)

text(
    (105.2, 11.2),
    "Site, Doc, Slide",
    style=Styles.DarkBold.patch(
        text_font=FontSansSerif.POPPINS_BOLD,
        text_size=14.5,
        text_color=(15, 23, 42),
    ),
)

draw_flow_arrow(39.0, 45.6, 24.5)
draw_flow_arrow(82.0, 87.8, 24.5)

save()
