# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_wan_router (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse
from drawlib.utils import (
    WHITE,
    draw_cisco_3d_cylinder,
    draw_cisco_arrow,
    draw_cisco_router_top_arrows,
    draw_round_segment,
    setup_icon,
    stroke_style,
)

setup_icon()

# 1. 3D cylinder router body and classic 4 top arrows
draw_cisco_3d_cylinder(50.0, 28.0, 78.0, 30.0, 14.0)
draw_cisco_router_top_arrows(50.0, 58.0, 39.0, 14.0)

# 2. Front WAN globe emblem centered on the front cylinder face
gx, gy = 50.0, 29.0
gr = 10.5
circle((gx, gy), radius=gr, style=stroke_style(WHITE, width_units=2.1))
ellipse((gx, gy), width=10.5, height=gr * 2.0, style=stroke_style(WHITE, width_units=1.8))
draw_round_segment((gx - gr, gy), (gx + gr, gy), width_units=1.8, color=WHITE)
draw_round_segment((gx - 8.8, gy + 5.2), (gx + 8.8, gy + 5.2), width_units=1.5, color=WHITE)
draw_round_segment((gx - 8.8, gy - 5.2), (gx + 8.8, gy - 5.2), width_units=1.5, color=WHITE)

# 3. Flanking outward WAN link arrows on the front face
draw_cisco_arrow((35.5, gy), (20.5, gy), shaft_w=2.6, head_len=5.5, head_w=7.0, color=WHITE)
draw_cisco_arrow((64.5, gy), (79.5, gy), shaft_w=2.6, head_len=5.5, head_w=7.0, color=WHITE)

save()
