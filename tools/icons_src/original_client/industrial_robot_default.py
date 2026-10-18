# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: industrial_robot."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE


def _draw_arm_link(x1: float, y1: float, x2: float, y2: float, half_w: float, color: str) -> None:
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    nx = -dy / length * half_w
    ny = dx / length * half_w
    pts = [
        (x1 + nx, y1 + ny),
        (x2 + nx, y2 + ny),
        (x2 - nx, y2 - ny),
        (x1 - nx, y1 - ny),
    ]
    polygon(pts, style=no_border_fill(color))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)


# 1. Precision gripper claw (PASTEL_GREEN) at end of wrist
claw_pts = [
    (68.5, 58.0),
    (77.5, 55.5),
    (86.0, 47.0),
    (82.0, 43.0),
    (76.5, 48.5),
    (72.5, 50.5),
    (69.5, 45.0),
    (72.5, 39.5),
    (66.5, 41.0),
    (65.0, 50.5),
]
polygon(claw_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(claw_pts, width_units=2.0, color=DARK, closed=True)

# 2. Wrist link, upper forearm, and lower arm segments (PASTEL_BLUE / PASTEL_BLUE_LIGHT)
_draw_arm_link(64.0, 72.0, 73.5, 56.5, half_w=3.6, color=PASTEL_BLUE_LIGHT)
_draw_arm_link(25.0, 64.0, 64.0, 72.0, half_w=4.6, color=PASTEL_BLUE)
_draw_arm_link(33.0, 34.0, 25.0, 64.0, half_w=5.2, color=PASTEL_BLUE)

# 3. Pedestal base and floor plate (PASTEL_BLUE + PASTEL_BLUE_LIGHT)
rectangle(
    (33.0, 25.0),
    width=22.0,
    height=13.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=3.0),
)
rectangle(
    (33.0, 16.5),
    width=36.0,
    height=7.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=2.5),
)

# 4. Circular rotary joints (WHITE) with center pins
for jx, jy, jr in ((33.0, 34.0, 7.5), (25.0, 64.0, 7.0), (64.0, 72.0, 6.0)):
    circle(
        (jx, jy),
        radius=jr,
        style=fill_style(WHITE, border_color=DARK, border_units=w),
    )
    circle(
        (jx, jy),
        radius=2.2,
        style=fill_style(DARK),
    )

save()
