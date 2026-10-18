# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: data_lake."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx = 50.0
width = 68.0
w_half = width / 2.0
ry = 10.0
eh = ry * 2.0
y_bot = 20.0
y_top = 74.0
body_h = y_top - y_bot

ellipse(
    (cx, y_bot),
    width=width,
    height=eh,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
rectangle(
    (cx, y_bot + body_h / 2.0),
    width=width,
    height=body_h,
    style=fill_style(PASTEL_BLUE),
)

draw_round_segment((cx - w_half, y_bot), (cx - w_half, y_top), width_units=w, color=DARK)
draw_round_segment((cx + w_half, y_bot), (cx + w_half, y_top), width_units=w, color=DARK)

ellipse(
    (cx, y_top),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

steps = 36
x_start = 24.0
x_end = 76.0
span = x_end - x_start
for y_wave in (46.0, 32.0):
    pts = [
        (
            x_start + span * (i / steps),
            y_wave + 2.6 * math.sin(2.0 * math.pi * 1.5 * (i / steps)),
        )
        for i in range(steps + 1)
    ]
    draw_round_polyline(pts, width_units=2.0, color=DARK)

circle(
    (68.0, 58.0),
    radius=4.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
