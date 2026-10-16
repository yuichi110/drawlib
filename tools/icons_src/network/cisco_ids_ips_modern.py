# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco modern 2D icon: ids_ips (modern variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    WHITE,
    build_shield_half_points,
    draw_cisco_arrow,
    draw_cisco_modern_badge,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()
draw_cisco_modern_badge()

# Central inspection circle barrier (matching Arch_63_Intrusion Prevention.png)
circle((50.0, 50.0), radius=18.0, style=stroke_style(WHITE, width_units=3.4))

# Top rightward arrow and bottom leftward arrow across the barrier
draw_cisco_arrow((22.0, 59.5), (78.0, 59.5), shaft_w=3.2, head_len=6.8, head_w=9.0, color=WHITE)
draw_cisco_arrow((78.0, 40.5), (22.0, 40.5), shaft_w=3.2, head_len=6.8, head_w=9.0, color=WHITE)

# Crisp inner protective shield emblem at center
left_sh = build_shield_half_points(50.0, 43.2, 56.8, 5.6, side="left")
right_sh = build_shield_half_points(50.0, 43.2, 56.8, 5.6, side="right")
polygon(left_sh + list(reversed(right_sh[1:-1])), style=no_border_fill(WHITE))

save()
