# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: drone."""

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


def _draw_arm(x1: float, y1: float, x2: float, y2: float, half_w: float) -> None:
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
    polygon(pts, style=no_border_fill(PASTEL_BLUE))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)


# 1. Four diagonal quadcopter arms (PASTEL_BLUE)
rotor_centers = [
    (24.5, 75.5),
    (75.5, 75.5),
    (24.5, 24.5),
    (75.5, 24.5),
]
for rx, ry in rotor_centers:
    _draw_arm(50.0, 50.0, rx, ry, half_w=4.2)

# 2. Four rotor discs (PASTEL_GREEN) with motor hubs (WHITE)
for rx, ry in rotor_centers:
    circle(
        (rx, ry),
        radius=12.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
    )
    circle(
        (rx, ry),
        radius=3.5,
        style=fill_style(WHITE, border_color=DARK, border_units=1.8),
    )

# 3. Front gimbal camera lens at top of central body
circle(
    (50.0, 68.5),
    radius=5.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)
circle(
    (50.0, 69.5),
    radius=2.6,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.5),
)

# 4. Central quadcopter fuselage body (PASTEL_BLUE + PASTEL_BLUE_LIGHT top shell)
rectangle(
    (50.0, 49.0),
    width=26.0,
    height=34.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=9.0),
)
rectangle(
    (50.0, 48.0),
    width=14.0,
    height=18.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=4.5),
)

save()
