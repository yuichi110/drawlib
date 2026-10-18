# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: opentofu."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
cx, cy = 50.0, 50.0
r = 39.0

dx = r * math.cos(math.radians(30.0))
dy = r * math.sin(math.radians(30.0))

v_center = (cx, cy)
v_top = (cx, cy + r)
v_tr = (cx + dx, cy + dy)
v_br = (cx + dx, cy - dy)
v_bot = (cx, cy - r)
v_bl = (cx - dx, cy - dy)
v_tl = (cx - dx, cy + dy)

# 1. Cube faces: Amber3 top, Amber2 left, WHITE right
polygon([v_center, v_tl, v_top, v_tr], style=no_border_fill(Colors.Amber3))
polygon([v_center, v_bot, v_bl, v_tl], style=no_border_fill(Colors.Amber2))
polygon([v_center, v_tr, v_br, v_bot], style=no_border_fill(WHITE))

# 2. Outer isometric hexagon border + 3 inner Y-seams in DARK
outer_hex = [v_top, v_tr, v_br, v_bot, v_bl, v_tl]
draw_round_polyline(outer_hex, width_units=w, color=DARK, closed=True)
for v in (v_tl, v_tr, v_bot):
    draw_round_segment(v_center, v, width_units=w, color=DARK)

# 3. Cute DARK semicircular eyes on the left face
ux, uy = math.cos(math.radians(-30.0)), math.sin(math.radians(-30.0))
vx, vy = 0.0, 1.0
r_eye = 4.1

eye_centers = [
    (26.0, 41.2),
    (36.8, 35.0),
]

for ex, ey in eye_centers:
    eye_pts: list[tuple[float, float]] = []
    steps = 24
    for i in range(steps + 1):
        ang = math.pi * (i / steps)
        ca, sa = math.cos(ang), math.sin(ang)
        px = ex + r_eye * ca * ux + r_eye * sa * vx
        py = ey + r_eye * ca * uy + r_eye * sa * vy
        eye_pts.append((px, py))
    polygon(eye_pts, style=no_border_fill(DARK))
    draw_round_polyline(eye_pts, width_units=1.2, color=DARK, closed=True)

save()
