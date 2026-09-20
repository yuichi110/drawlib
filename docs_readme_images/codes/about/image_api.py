# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

textstyle_bold = Style(text_font=FontRoboto.ROBOTO_BOLD, text_size=20)
shapetextstyle_bold = Style(text_font=FontRoboto.ROBOTO_BOLD, text_size=20)
config(width=100, height=60)


def bottom():
    rectangle(
        (50, 7),
        width=90,
        height=10,
        r=2,
        style=Style(fill_color=Colors.Transparent),
        text="Canvas and coordinate system, theme etc.",
        textstyle=shapetextstyle_bold,
    )


def middle(x, width, name, functions, styles):
    rectangle(
        (x, 30),
        width=width,
        height=30,
        r=2,
        style=Style(text_halign="left", fill_color=Colors.Transparent),
    )
    tx = x + width / 2
    text((tx, 42), name, style=textstyle_bold)

    for i, function in enumerate(functions):
        text(
            (x + 1, 36 - i * 3),
            f"- {function}",
            style=Style(text_halign="left", text_size=12),
        )

    line((x + 1, 26), (x + width - 1, 26), style=Style(line_style="dashed"))

    for i, style in enumerate(styles):
        text(
            (x + 1, 22 - i * 3),
            f"- {style}",
            style=Style(text_halign="left", text_size=12),
        )


def top():
    rectangle(
        (50, 53),
        width=90,
        height=10,
        r=2,
        style=Style(fill_color=Colors.Transparent),
        text="Advanced topics, handle many files etc.",
        textstyle=shapetextstyle_bold,
    )


bottom()

for i, t in enumerate(
    [
        ("icon", ["icon()", "icon_phosphor()"], ["Style"]),
        ("image", ["image()"], ["Style"]),
        ("line", ["line()", "line_curved()", "..."], ["Style"]),
        ("shape", ["circle()", "rectangle()", "..."], ["Style"]),
        ("text", ["text()"], ["Style"]),
    ]
):
    start = 5
    width = 16.5
    space = (90 - (width * 5)) / 4
    x = start + (width + space) * i
    name = t[0]
    functions = t[1]
    styles = t[2]
    middle(x, width, name, functions, styles)

top()

save()
