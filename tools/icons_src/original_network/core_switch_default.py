# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: core_switch."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer modular core switch chassis
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=78.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Upper fabric switching bay
rectangle(
    (50.0, 68.0),
    width=54.0,
    height=30.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# Crossing X-fabric lines with central hub dot
Icon.draw_round_segment((30.0, 60.0), (70.0, 76.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((30.0, 76.0), (70.0, 60.0), width_units=2.0, color=Icon.DARK)

for end_pt in [(30.0, 60.0), (70.0, 76.0), (30.0, 76.0), (70.0, 60.0)]:
    circle(end_pt, radius=2.2, style=Icon.fill_style(Icon.DARK))

circle(
    (50.0, 68.0),
    radius=4.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# Lower L3 routing/switching bay
rectangle(
    (50.0, 32.0),
    width=54.0,
    height=30.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# 8 radial outward L3 arrows around center dot
cx, cy = 50.0, 32.0
for k in range(8):
    ang = math.radians(k * 45.0)
    ux = math.cos(ang)
    uy = math.sin(ang)
    Cisco.draw_arrow(
        (cx + ux * 5.5, cy + uy * 5.5),
        (cx + ux * 12.5, cy + uy * 12.5),
        shaft_w=2.0,
        head_len=4.2,
        head_w=5.6,
        color=Icon.DARK,
    )

circle(
    (cx, cy),
    radius=5.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
