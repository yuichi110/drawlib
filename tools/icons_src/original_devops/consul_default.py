# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: consul."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
w_dot = 2.0

cx, cy = 50.0, 50.0
r_out = 39.0
r_in = 25.6
ang_open = 47.5

# 1. Colors.Pink3 C-ring (transparent interior)
steps = 64
outer_arc: list[tuple[float, float]] = []
for i in range(steps + 1):
    deg = ang_open + (360.0 - 2.0 * ang_open) * (i / steps)
    rad = math.radians(deg)
    outer_arc.append((cx + r_out * math.cos(rad), cy + r_out * math.sin(rad)))

inner_arc: list[tuple[float, float]] = []
for i in range(steps + 1):
    deg = (360.0 - ang_open) - (360.0 - 2.0 * ang_open) * (i / steps)
    rad = math.radians(deg)
    inner_arc.append((cx + r_in * math.cos(rad), cy + r_in * math.sin(rad)))

c_ring_pts = [*outer_arc, *inner_arc]
polygon(c_ring_pts, style=no_border_fill(Colors.Pink3))
draw_round_polyline(c_ring_pts, width_units=w, color=DARK, closed=True)

# 2. Central circle (Colors.Pink3, w=1.9 DARK border)
circle(
    (cx, cy),
    radius=8.5,
    style=fill_style(Colors.Pink3, border_color=DARK, border_units=w),
)

# 3. Six outer dots in the right opening (Colors.Pink3, 1.6 DARK border)
# Two inner-arc dots (radius 25.8 from center) and four outer-arc dots (radius 35.4)
dot_r1 = 25.8
dot_r2 = 35.4
dot_specs = [
    (dot_r1, 11.2),
    (dot_r1, -11.2),
    (dot_r2, 27.0),
    (dot_r2, 8.8),
    (dot_r2, -8.8),
    (dot_r2, -27.0),
]

for r_pos, deg in dot_specs:
    rad = math.radians(deg)
    dx = cx + r_pos * math.cos(rad)
    dy = cy + r_pos * math.sin(rad)
    circle(
        (dx, dy),
        radius=3.2,
        style=fill_style(Colors.Pink3, border_color=DARK, border_units=w_dot),
    )

save()
