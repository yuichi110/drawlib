# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client brand icon: safari (default variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import DARK, WHITE, draw_round_polyline, draw_round_segment, fill_style, no_border_fill, setup_icon

setup_icon()

w_outer = 2.0
w_face = 1.6
w_tick = 1.4
w_needle = 1.6

# 1. White outer bezel ring and pastel blue compass face
circle((50.0, 50.0), radius=41.0, style=fill_style(WHITE, border_color=DARK, border_units=w_outer))
circle((50.0, 50.0), radius=35.8, style=fill_style("#7BAEF7", border_color=DARK, border_units=w_face))

# 2. 16 crisp compass ticks (8 major + 8 minor)
for i in range(16):
    angle_rad = math.radians(i * 22.5)
    r_in = 28.2 if i % 2 == 0 else 30.6
    r_out = 33.0
    p1 = (round(50.0 + r_in * math.cos(angle_rad), 2), round(50.0 + r_in * math.sin(angle_rad), 2))
    p2 = (round(50.0 + r_out * math.cos(angle_rad), 2), round(50.0 + r_out * math.sin(angle_rad), 2))
    draw_round_segment(p1, p2, width_units=w_tick, color=DARK)

# 3. Two-tone diamond compass needle (pastel red NE + white SW)
needle_ne = [(78.01, 78.21), (46.52, 53.48), (53.87, 46.13)]
needle_sw = [(21.79, 21.99), (53.87, 46.13), (46.52, 53.48)]
needle_outline = [(78.01, 78.21), (53.87, 46.13), (21.79, 21.99), (46.52, 53.48)]

polygon(needle_ne, style=no_border_fill("#F28B82"))
polygon(needle_sw, style=no_border_fill(WHITE))
draw_round_segment((46.52, 53.48), (53.87, 46.13), width_units=w_needle, color=DARK)
draw_round_polyline(needle_outline, width_units=w_needle, color=DARK, closed=True)
circle((50.0, 50.0), radius=2.0, style=fill_style(WHITE, border_color=DARK, border_units=1.3))

save()
