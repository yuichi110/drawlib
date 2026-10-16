# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_nexus_switch (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    CISCO_BLUE,
    CISCO_LIGHT_BLUE,
    WHITE,
    draw_cisco_3d_box,
    draw_cisco_arrow,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

x0, y0 = 10.0, 22.0
w_front, h_front = 62.0, 28.0
dx, dy = 18.0, 16.0

draw_cisco_3d_box(x0, y0, w_front, h_front, dx, dy)


def _top_pt(u: float, v: float) -> tuple[float, float]:
    return (x0 + w_front * u + dx * v, y0 + h_front + dy * v)


# 1. Top face: 4 alternating left/right oblique switch arrows
tsw, thl, thw = 1.7, 5.5, 4.0
draw_cisco_arrow(_top_pt(0.50, 0.20), _top_pt(0.14, 0.20), shaft_w=tsw, head_len=thl, head_w=thw, color=WHITE)
draw_cisco_arrow(_top_pt(0.47, 0.39), _top_pt(0.83, 0.39), shaft_w=tsw, head_len=thl, head_w=thw, color=WHITE)
draw_cisco_arrow(_top_pt(0.50, 0.58), _top_pt(0.14, 0.58), shaft_w=tsw, head_len=thl, head_w=thw, color=WHITE)
draw_cisco_arrow(_top_pt(0.47, 0.76), _top_pt(0.83, 0.76), shaft_w=tsw, head_len=thl, head_w=thw, color=WHITE)

# 2. Front face Data Center port/vent slots on left and right sides
vent_style = no_border_fill(CISCO_LIGHT_BLUE)
for vy in (29.5, 36.0, 42.5):
    rectangle((15.5, vy), width=5.0, height=2.2, style=vent_style)
    rectangle((66.5, vy), width=5.0, height=2.2, style=vent_style)

# 3. Front face signature Nexus crossing X-fabric arrows with horizontal tips
fsw, fhl, fhw = 2.4, 5.2, 6.8
draw_round_segment((32.5, 43.0), (49.5, 29.0), width_units=fsw, color=WHITE)
draw_round_segment((32.5, 29.0), (49.5, 43.0), width_units=fsw, color=WHITE)
draw_cisco_arrow((32.5, 43.0), (22.5, 43.0), shaft_w=fsw, head_len=fhl, head_w=fhw, color=WHITE)
draw_cisco_arrow((49.5, 29.0), (59.5, 29.0), shaft_w=fsw, head_len=fhl, head_w=fhw, color=WHITE)
draw_cisco_arrow((32.5, 29.0), (22.5, 29.0), shaft_w=fsw, head_len=fhl, head_w=fhw, color=WHITE)
draw_cisco_arrow((49.5, 43.0), (59.5, 43.0), shaft_w=fsw, head_len=fhl, head_w=fhw, color=WHITE)
circle((41.0, 36.0), radius=3.8, style=fill_style(WHITE, border_color=CISCO_BLUE, border_units=1.2))

save()
