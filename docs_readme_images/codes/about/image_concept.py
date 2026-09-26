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
from drawlib.preset_styles import default_styles
from drawlib.shapes import arrow, circle
from drawlib.text import text

config(width=100, height=60)
ps = default_styles


def left():
    x = 18
    circle(
        (x, 30),
        radius=8,
        text="Circle",
        style=ps.flat.patch(
            shape_fill_color=Colors.Transparent,
            shape_line_color=Colors.Black,
            shape_line_width=1,
        ),
        textstyle=ps.primary.patch(text_size=18),
    )
    text((x, 15), text="Content", style=ps.primary.patch(text_size=24))


def center():
    x = 50
    length = 30
    arrow(
        (x - length / 2, 30),
        (x + length / 2, 30),
        tail_width=6,
        head_width=14,
        head_length=10,
        style=ps.green,
        text="Apply Styles",
        textsize=20,
        textstyle=ps.white,
    )


def right():
    x = 82
    circle((x, 49), radius=8, style=ps.primary, text="Circle", textstyle=ps.primary.patch(text_size=18))
    circle(
        (x, 30),
        radius=8,
        text="Circle",
        style=ps.blue_flat,
        textstyle=ps.primary.patch(text_color=Colors.White, text_size=18),
    )
    circle(
        (x, 11),
        radius=8,
        text="Circle",
        style=ps.red_bold,
        textstyle=ps.primary.patch(text_color=Colors.Red, text_size=18),
    )


left()
center()
right()
save()

