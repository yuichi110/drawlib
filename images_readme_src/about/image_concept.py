# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import save, setup
from drawlib.shapes import arrow, circle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=100, height=60, color=Colors.canvas)


def left():
    x = 18
    circle(
        (x, 30),
        radius=8,
        text="Circle",
        style=Styles.MutedOutline,
        textstyle=Styles.Primary.patch(text_size=18),
    )
    text((x, 15), text="Content", style=Styles.Primary.patch(text_size=24))


def center():
    x = 50
    length = 30
    arrow(
        (x - length / 2, 30),
        (x + length / 2, 30),
        tail_width=6,
        head_width=14,
        head_length=10,
        style=Styles.Green,
        text="Apply Styles",
        textsize=20,
        textstyle=Styles.White,
    )


def right():
    x = 82
    circle(
        (x, 49),
        radius=8,
        style=Styles.Primary,
        text="Circle",
        textstyle=Styles.White.patch(text_size=18),
    )
    circle(
        (x, 30),
        radius=8,
        text="Circle",
        style=Styles.BlueFlat,
        textstyle=Styles.White.patch(text_size=18),
    )
    circle(
        (x, 11),
        radius=8,
        text="Circle",
        style=Styles.RedBold,
        textstyle=Styles.White.patch(text_size=18),
    )


left()
center()
right()
save()
