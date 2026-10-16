# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_core_router (modern 2D badge variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    WHITE,
    draw_cisco_arrow,
    draw_cisco_modern_badge,
    draw_round_segment,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

draw_cisco_modern_badge()

# 1. Tall carrier chassis outline and horizontal section divider
rectangle(
    (50.0, 50.0),
    width=48.0,
    height=58.0,
    style=stroke_style(WHITE, width_units=3.2),
)
draw_round_segment((26.0, 48.0), (74.0, 48.0), width_units=2.8, color=WHITE)

# 2. Upper routing section: 4-arrow routing cross around (50, 63.5)
ry = 63.5
draw_cisco_arrow((30.5, ry), (46.0, ry), shaft_w=2.8, head_len=5.5, head_w=7.2, color=WHITE)
draw_cisco_arrow((69.5, ry), (54.0, ry), shaft_w=2.8, head_len=5.5, head_w=7.2, color=WHITE)
draw_cisco_arrow((50.0, ry + 3.0), (50.0, 76.0), shaft_w=2.8, head_len=5.0, head_w=7.0, color=WHITE)
draw_cisco_arrow((50.0, ry - 3.0), (50.0, 51.0), shaft_w=2.8, head_len=5.0, head_w=7.0, color=WHITE)

# 3. Lower chassis section: 4 vertical carrier blade slots
for div_x in (38.0, 50.0, 62.0):
    draw_round_segment((div_x, 21.0), (div_x, 48.0), width_units=2.4, color=WHITE)

for slot_x in (32.0, 44.0, 56.0, 68.0):
    circle((slot_x, 41.5), radius=1.8, style=no_border_fill(WHITE))
    draw_round_segment((slot_x, 27.0), (slot_x, 35.5), width_units=2.2, color=WHITE)

save()
