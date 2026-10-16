# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco classic 3D icon: ise (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    CISCO_BLUE,
    CISCO_DARK_BLUE,
    WHITE,
    draw_cisco_3d_box,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

x0 = 18.0
y0 = 11.0
w_front = 48.0
h_front = 63.0
dx = 16.0
dy = 14.0

draw_cisco_3d_box(x0, y0, w_front, h_front, dx, dy)

# Top server chassis bezel slot and status indicator
draw_round_segment((23.0, 66.5), (61.0, 66.5), width_units=1.8, color=WHITE)
circle((26.0, 70.0), radius=1.5, style=no_border_fill(WHITE))

# User profile silhouette on upper-left of front panel
u_cx = 36.5
circle((u_cx, 50.5), radius=6.2, style=no_border_fill(WHITE))

shoulder_pts: list[tuple[float, float]] = []
sh_rx = 11.2
sh_ry = 11.5
sh_y0 = 31.0
for i in range(25):
    ang = math.radians(180.0 * (i / 24.0))
    shoulder_pts.append((u_cx + sh_rx * math.cos(ang), sh_y0 + sh_ry * math.sin(ang)))
polygon(shoulder_pts, style=no_border_fill(WHITE))

# Verification checkmark badge overlapping right side of user silhouette
chk_cx, chk_cy = 52.5, 34.5
circle((chk_cx, chk_cy), radius=9.4, style=no_border_fill(CISCO_BLUE))
circle((chk_cx, chk_cy), radius=7.8, style=no_border_fill(WHITE))
draw_round_polyline(
    [(48.8, 34.2), (51.5, 31.3), (56.6, 37.3)],
    width_units=2.2,
    color=CISCO_DARK_BLUE,
)

# Horizontal identity key emblem along bottom of front panel
key_y = 20.0
circle((30.0, key_y), radius=3.6, style=stroke_style(WHITE, width_units=2.0))
draw_round_segment((33.6, key_y), (53.5, key_y), width_units=2.2, color=WHITE)
draw_round_segment((48.5, key_y), (48.5, key_y - 3.2), width_units=2.0, color=WHITE)
draw_round_segment((52.5, key_y), (52.5, key_y - 3.2), width_units=2.0, color=WHITE)

save()
