# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: wireless router (modern 2D variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

# Dual vertical antennas with rounded tips and wireless wave arcs
for ax in (33.0, 67.0):
    Icon.draw_round_segment((ax, 49.0), (ax, 74.0), width_units=3.2, color=Icon.WHITE)
    circle((ax, 74.5), radius=2.6, style=Icon.no_border_fill(Icon.WHITE))

# Subtle wireless signal arcs between / around the antenna tips
for r_arc in (6.5, 11.0):
    arc(
        (33.0, 74.5),
        width=r_arc * 2.0,
        height=r_arc * 2.0,
        angle_start=-35.0,
        angle_end=35.0,
        style=Icon.stroke_style(Cisco.LIGHT_BLUE, width_units=1.8),
    )
    arc(
        (67.0, 74.5),
        width=r_arc * 2.0,
        height=r_arc * 2.0,
        angle_start=145.0,
        angle_end=215.0,
        style=Icon.stroke_style(Cisco.LIGHT_BLUE, width_units=1.8),
    )

# Router base chassis in lower half of badge
cx, cy = 50.0, 35.5
rectangle(
    (cx, cy),
    width=56.0,
    height=29.0,
    style=Icon.fill_style(Cisco.DARK_BLUE, border_color=Icon.WHITE, border_units=2.4, shape_r=6.0),
)

# 4 routing cross arrows inside router base (horizontal inward, vertical outward)
Cisco.draw_arrow(
    (cx - 22.0, cy),
    (cx - 4.5, cy),
    shaft_w=2.8,
    head_len=5.5,
    head_w=7.2,
    color=Icon.WHITE,
)
Cisco.draw_arrow(
    (cx + 22.0, cy),
    (cx + 4.5, cy),
    shaft_w=2.8,
    head_len=5.5,
    head_w=7.2,
    color=Icon.WHITE,
)
Cisco.draw_arrow(
    (cx, cy + 2.5),
    (cx, cy + 11.5),
    shaft_w=2.8,
    head_len=4.5,
    head_w=7.0,
    color=Icon.WHITE,
)
Cisco.draw_arrow(
    (cx, cy - 2.5),
    (cx, cy - 11.5),
    shaft_w=2.8,
    head_len=4.5,
    head_w=7.0,
    color=Icon.WHITE,
)

save()
