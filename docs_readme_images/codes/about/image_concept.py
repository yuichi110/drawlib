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
from drawlib.shapes import arrow, circle
from drawlib.text import text
from drawlib.types import ShapeStyle, ShapeTextStyle, TextStyle

config(width=100, height=60)


def left():
    x = 18
    circle(
        (x, 30),
        radius=8,
        text="Circle",
        style=ShapeStyle(fill_color=Colors.Transparent),
        textstyle=ShapeTextStyle(text_size=18),
    )
    text((x, 15), text="Content", style=TextStyle(text_size=24))


def center():
    x = 50
    length = 30
    arrow(
        (x - length / 2, 30),
        (x + length / 2, 30),
        tail_width=6,
        head_width=14,
        head_length=10,
        style="green",
        text="Apply Styles",
        textsize=20,
        textstyle="white",
    )


def right():
    x = 82
    circle((x, 49), radius=8, text="Circle", textstyle=ShapeTextStyle(text_size=18))
    circle(
        (x, 30),
        radius=8,
        text="Circle",
        style="blue_flat",
        textstyle=ShapeTextStyle(text_color=Colors.White, text_size=18),
    )
    circle(
        (x, 11),
        radius=8,
        text="Circle",
        style="red_solid_bold",
        textstyle=ShapeTextStyle(text_color=Colors.Red, text_size=18),
    )


left()
center()
right()
save()
