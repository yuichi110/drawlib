# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco modern 2D icon: ise (modern variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    CISCO_BLUE,
    WHITE,
    draw_cisco_modern_badge,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()
draw_cisco_modern_badge()

# User profile silhouette inside badge
u_cx = 44.0
circle((u_cx, 65.0), radius=9.2, style=no_border_fill(WHITE))

shoulder_pts: list[tuple[float, float]] = []
sh_rx = 17.5
sh_ry = 16.0
sh_y0 = 38.0
for i in range(29):
    ang = math.radians(180.0 * (i / 28.0))
    shoulder_pts.append((u_cx + sh_rx * math.cos(ang), sh_y0 + sh_ry * math.sin(ang)))
polygon(shoulder_pts, style=no_border_fill(WHITE))

# Verification checkmark badge with blue knockout halo
chk_cx, chk_cy = 64.5, 42.5
circle((chk_cx, chk_cy), radius=12.2, style=no_border_fill(CISCO_BLUE))
circle((chk_cx, chk_cy), radius=10.0, style=no_border_fill(WHITE))
draw_round_polyline(
    [(59.8, 42.2), (63.2, 38.6), (69.6, 46.2)],
    width_units=2.8,
    color=CISCO_BLUE,
)

# Identity access key below user silhouette
key_y = 28.0
circle((33.5, key_y), radius=4.6, style=stroke_style(WHITE, width_units=2.6))
draw_round_segment((38.1, key_y), (61.5, key_y), width_units=2.8, color=WHITE)
draw_round_segment((55.0, key_y), (55.0, key_y - 4.2), width_units=2.6, color=WHITE)
draw_round_segment((60.0, key_y), (60.0, key_y - 4.2), width_units=2.6, color=WHITE)

save()
