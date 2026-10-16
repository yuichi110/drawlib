# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: l3_switch."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cisco_arrow,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Outer square multilayer switch card
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=12.0),
)

# Inner white switching plate
rectangle(
    (50.0, 50.0),
    width=60.0,
    height=60.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, shape_r=8.0),
)

# 8 radial outward arrows every 45 degrees
for k in range(8):
    ang = math.radians(k * 45.0)
    ux = math.cos(ang)
    uy = math.sin(ang)
    draw_cisco_arrow(
        (50.0 + ux * 10.0, 50.0 + uy * 10.0),
        (50.0 + ux * 26.0, 50.0 + uy * 26.0),
        shaft_w=2.6,
        head_len=5.5,
        head_w=7.2,
        color=DARK,
    )

# Center L3 hub circle (smaller diameter leaving clear space before arrow tails at r=10.0)
circle(
    (50.0, 50.0),
    radius=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
)

save()
