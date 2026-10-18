# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: new_relic."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
cx, cy = 50.0, 50.0

# Isometric outer radius and ribbon step (transparent center hole)
r_out = 39.0
d_step = 15.0
r_in = r_out - d_step

cos30 = math.cos(math.radians(30.0))
sin30 = math.sin(math.radians(30.0))

dx_out = r_out * cos30
dy_out = r_out * sin30
dx_in = r_in * cos30
dy_in = r_in * sin30
dx_step = d_step * cos30
dy_step = d_step * sin30

# 1. Right / bottom-right ribbon bar (Colors.Teal3)
bar_right: list[tuple[float, float]] = [
    (cx + dx_in, cy + dy_in),
    (cx + dx_in, cy - dy_in),
    (cx, cy - r_in),
    (cx, cy - r_out),
    (cx + dx_out, cy - dy_out),
    (cx + dx_out, cy + dy_out),
]

# 2. Top ribbon bar (Colors.Green2)
bar_top: list[tuple[float, float]] = [
    (cx, cy + r_in),
    (cx + dx_in, cy + dy_in),
    (cx + dx_out, cy + dy_out),
    (cx, cy + r_out),
    (cx - dx_out, cy + dy_out),
    (cx - dx_in, cy + dy_in),
]

# 3. Bottom-left ribbon bar (Colors.Gray6)
bar_left: list[tuple[float, float]] = [
    (cx - dx_step, cy - dy_step),
    (cx - dx_step, cy - r_out + dy_step),
    (cx, cy - r_out),
    (cx, cy),
    (cx - dx_out, cy + dy_out),
    (cx - dx_out, cy + dy_out - d_step),
]

facets = [
    (bar_right, Colors.Teal3),
    (bar_top, Colors.Green2),
    (bar_left, Colors.Gray6),
]

for pts, col in facets:
    polygon(pts, style=no_border_fill(col))

for pts, _ in facets:
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
