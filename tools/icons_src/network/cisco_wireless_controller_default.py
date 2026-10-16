# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: wireless LAN controller (classic 3D default variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    CISCO_LIGHT_BLUE,
    WHITE,
    draw_cisco_3d_box,
    draw_cisco_arrow,
    draw_cisco_sine_waves,
    draw_round_segment,
    setup_icon,
)

setup_icon()

# 3D wireless controller appliance box (x in [10, 90], y in [22, 74])
x0, y0 = 10.0, 22.0
w_front, h_front = 64.0, 30.0
dx, dy = 16.0, 22.0

draw_cisco_3d_box(x0, y0, w_front, h_front, dx, dy)

# Top-face converging switch/controller arrows
draw_cisco_arrow(
    (22.0, 55.0),
    (44.5, 62.0),
    shaft_w=2.4,
    head_len=5.0,
    head_w=6.8,
    color=WHITE,
)
draw_cisco_arrow(
    (45.0, 54.5),
    (49.5, 61.5),
    shaft_w=2.4,
    head_len=4.5,
    head_w=6.8,
    color=WHITE,
)
draw_cisco_arrow(
    (71.5, 55.0),
    (54.5, 62.0),
    shaft_w=2.4,
    head_len=5.0,
    head_w=6.8,
    color=WHITE,
)
draw_cisco_arrow(
    (50.5, 63.0),
    (57.0, 72.0),
    shaft_w=4.4,
    head_len=5.2,
    head_w=10.0,
    color=WHITE,
)

# Front-face vertical blade dividers on the right modular bay
x_bay = 58.0
draw_round_segment((x_bay, y0 + 2.0), (x_bay, y0 + h_front - 2.0), width_units=1.5, color=WHITE)
for x_blade in (63.3, 68.7):
    draw_round_segment(
        (x_blade, y0 + 3.5),
        (x_blade, y0 + h_front - 3.5),
        width_units=1.3,
        color=CISCO_LIGHT_BLUE,
    )

# Front-face intertwined dual sine wave in the left wireless bay
draw_cisco_sine_waves(
    34.0,
    37.0,
    38.0,
    5.2,
    cycles=1.5,
    stroke_w=2.5,
    color=WHITE,
    steps=120,
)

save()
