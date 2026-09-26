# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.config import styles
from drawlib.shapes import rectangle
from drawlib.text import text

textstyle_bold = styles.primary.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=20)
shapetextstyle_bold = styles.primary.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=20)
setup(width=100, height=60)


def bottom():
    rectangle(
        (50, 7),
        width=90,
        height=10,
        r=2,
        style=styles.flat.patch(
            shape_fill_color=Colors.Transparent,
            shape_line_color=Colors.Black,
            shape_line_width=1,
        ),
        text="Canvas and coordinate system, theme etc.",
        textstyle=shapetextstyle_bold,
    )


def middle(x, width, name, functions, style_items):
    rectangle(
        (x, 30),
        width=width,
        height=30,
        r=2,
        style=styles.flat.patch(
            shape_fill_color=Colors.Transparent,
            shape_line_color=Colors.Black,
            shape_line_width=1,
            text_halign="left",
        ),
    )
    tx = x + width / 2
    text((tx, 42), name, style=textstyle_bold)

    for i, function in enumerate(functions):
        text(
            (x + 1, 36 - i * 3),
            f"- {function}",
            style=styles.primary.patch(text_halign="left", text_size=12),
        )

    line((x + 1, 26), (x + width - 1, 26), style=styles.dashed)

    for i, style in enumerate(style_items):
        text(
            (x + 1, 22 - i * 3),
            f"- {style}",
            style=styles.primary.patch(text_halign="left", text_size=12),
        )


def top():
    rectangle(
        (50, 53),
        width=90,
        height=10,
        r=2,
        style=styles.flat.patch(
            shape_fill_color=Colors.Transparent,
            shape_line_color=Colors.Black,
            shape_line_width=1,
        ),
        text="Advanced topics, handle many files etc.",
        textstyle=shapetextstyle_bold,
    )


bottom()

for i, t in enumerate(
    [
        ("icon", ["font_icon()", "phosphor.*()"], ["Style"]),
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
    style_items = t[2]
    middle(x, width, name, functions, style_items)

top()

save()
