# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: nexus."""

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

w = 1.9

t30 = math.tan(math.radians(30.0))
x_out_l = 13.5
x_out_r = 86.5
x_in_l = 22.0
x_in_r = 78.0

dy_full = (50.0 - x_out_l) * t30  # 21.07
dy_inner = (50.0 - x_in_l) * t30  # 16.17
t_v = 9.8
gap_v = 5.8

# 1. Bottom chevron (Colors.Gray6)
y_b0 = 11.2
bot_chevron = [
    (x_out_l, y_b0 + dy_full),
    (50.0, y_b0),
    (x_out_r, y_b0 + dy_full),
    (x_out_r, y_b0 + dy_full + t_v),
    (50.0, y_b0 + t_v),
    (x_out_l, y_b0 + dy_full + t_v),
]

# 2. Middle chevron (Colors.Green3)
y_m0 = y_b0 + t_v + gap_v
mid_chevron = [
    (x_out_l, y_m0 + dy_full),
    (50.0, y_m0),
    (x_out_r, y_m0 + dy_full),
    (x_out_r, y_m0 + dy_full + t_v),
    (50.0, y_m0 + t_v),
    (x_out_l, y_m0 + dy_full + t_v),
]

# 3. Top U-chevron (Colors.Gray6)
y_t0 = y_m0 + t_v + gap_v
y_top_wall = 82.8
top_chevron = [
    (x_out_l, y_top_wall),
    (x_out_l, y_t0 + dy_full),
    (50.0, y_t0),
    (x_out_r, y_t0 + dy_full),
    (x_out_r, y_top_wall),
    (x_in_r, y_top_wall),
    (x_in_r, y_t0 + t_v + dy_inner),
    (50.0, y_t0 + t_v),
    (x_in_l, y_t0 + t_v + dy_inner),
    (x_in_l, y_top_wall),
]

# 4. Geometric 'r' stem above top chevron valley (Colors.Green3)
r_stem = [
    (45.0, 65.5),
    (51.2, 65.5),
    (51.2, 80.2),
    (54.8, 82.8),
    (58.8, 82.8),
    (58.8, 89.0),
    (54.6, 88.0),
    (51.2, 85.1),
    (51.2, 88.4),
    (45.0, 88.4),
]

polygon(bot_chevron, style=no_border_fill(Colors.Gray6))
polygon(mid_chevron, style=no_border_fill(Colors.Green3))
polygon(top_chevron, style=no_border_fill(Colors.Gray6))
polygon(r_stem, style=no_border_fill(Colors.Green3))

for pts in (bot_chevron, mid_chevron, top_chevron, r_stem):
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
