# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: voice gateway (modern 2D SAFE variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    WHITE,
    draw_cisco_arrow,
    draw_cisco_modern_badge,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

draw_cisco_modern_badge()

# 4 Cisco routing/gateway cross arrows around the center (2 horizontal inward, 2 vertical outward)
draw_cisco_arrow(
    (16.5, 50.0),
    (31.5, 50.0),
    shaft_w=4.0,
    head_len=6.0,
    head_w=9.4,
    color=WHITE,
)
draw_cisco_arrow(
    (83.5, 50.0),
    (68.5, 50.0),
    shaft_w=4.0,
    head_len=6.0,
    head_w=9.4,
    color=WHITE,
)
draw_cisco_arrow(
    (50.0, 68.5),
    (50.0, 83.5),
    shaft_w=4.0,
    head_len=6.0,
    head_w=9.4,
    color=WHITE,
)
draw_cisco_arrow(
    (50.0, 31.5),
    (50.0, 16.5),
    shaft_w=4.0,
    head_len=6.0,
    head_w=9.4,
    color=WHITE,
)

# Central telephone handset icon rotated at +135 degrees (spine bowing bottom-left)
scale = 0.96
rot = math.radians(135.0)
cos_r = math.cos(rot)
sin_r = math.sin(rot)


def _rot_raw(ux: float, uy: float) -> tuple[float, float]:
    sx = ux * scale
    sy = uy * scale
    return (sx * cos_r - sy * sin_r, sx * sin_r + sy * cos_r)


local_pts: list[tuple[float, float]] = []
for i in range(25):
    ang = math.radians(158.0 - 136.0 * (i / 24))
    local_pts.append((14.8 * math.cos(ang), -5.6 + 12.2 * math.sin(ang)))

local_pts.extend(
    [
        (13.8, -4.8),
        (12.0, -6.2),
        (7.2, -5.2),
        (6.4, 1.4),
    ]
)

for i in range(1, 12):
    t = i / 12
    local_pts.append((6.4 * (1.0 - 2.0 * t), 1.4 + 1.5 * math.sin(math.pi * t)))

local_pts.extend(
    [
        (-6.4, 1.4),
        (-7.2, -5.2),
        (-12.0, -6.2),
        (-13.8, -4.8),
    ]
)

raw_pts = [_rot_raw(ux, uy) for ux, uy in local_pts]
min_x = min(p[0] for p in raw_pts)
max_x = max(p[0] for p in raw_pts)
min_y = min(p[1] for p in raw_pts)
max_y = max(p[1] for p in raw_pts)
off_x = 50.0 - (min_x + max_x) / 2.0
off_y = 50.0 - (min_y + max_y) / 2.0

handset_pts = [(px + off_x, py + off_y) for px, py in raw_pts]
polygon(handset_pts, style=no_border_fill(WHITE))
draw_round_polyline(handset_pts, width_units=1.5, color=WHITE, closed=True)

save()
