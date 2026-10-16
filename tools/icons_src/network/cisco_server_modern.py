# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: server (modern 2D SAFE variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    CISCO_BLUE,
    WHITE,
    draw_cisco_modern_badge,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

draw_cisco_modern_badge()

# 3 stacked horizontal server rack blades with drive slots and LED dots
for blade_y in (66.5, 50.0, 33.5):
    rectangle(
        (50.0, blade_y),
        width=52.0,
        height=12.5,
        style=no_border_fill(WHITE, shape_r=3.2),
    )
    draw_round_segment((30.0, blade_y), (53.5, blade_y), width_units=2.8, color=CISCO_BLUE)
    circle((63.0, blade_y), radius=2.1, style=no_border_fill(CISCO_BLUE))
    circle((69.8, blade_y), radius=2.1, style=no_border_fill(CISCO_BLUE))

save()
