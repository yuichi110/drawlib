# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: pub_sub."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE
hub_xy = (28.0, 50.0)
subscribers = [(76.0, 78.0), (80.0, 50.0), (76.0, 22.0)]

for sub_xy in subscribers:
    draw_round_segment(hub_xy, sub_xy, width_units=w, color=DARK)

r_wave = 23.0
arc(
    hub_xy,
    width=r_wave * 2.0,
    height=r_wave * 2.0,
    angle_start=-40.0,
    angle_end=40.0,
    style=stroke_style(DARK, width_units=2.4),
)
for ang_deg in (-40.0, 40.0):
    ang = math.radians(ang_deg)
    draw_cap(
        (hub_xy[0] + r_wave * math.cos(ang), hub_xy[1] + r_wave * math.sin(ang)),
        width_units=2.4,
        color=DARK,
    )

circle(
    hub_xy,
    radius=15.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    hub_xy,
    radius=5.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

for sub_xy in subscribers:
    rectangle(
        sub_xy,
        width=16.0,
        height=16.0,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=4.0),
    )

save()
