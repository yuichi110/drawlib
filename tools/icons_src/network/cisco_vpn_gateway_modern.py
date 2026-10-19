# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco modern 2D icon: vpn_gateway (modern variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

# Horizontal encrypted tunnel pipe walls extending left and right
pipe_y_top = 61.5
pipe_y_bot = 38.5
Icon.draw_round_segment((21.5, pipe_y_top), (78.5, pipe_y_top), width_units=2.8, color=Icon.WHITE)
Icon.draw_round_segment((21.5, pipe_y_bot), (78.5, pipe_y_bot), width_units=2.8, color=Icon.WHITE)

# Left/right bidirectional encrypted tunnel arrows inside the pipe ends
Cisco.draw_arrow((19.5, 53.5), (31.0, 53.5), shaft_w=2.8, head_len=5.2, head_w=7.0, color=Icon.WHITE)
Cisco.draw_arrow((80.5, 46.5), (69.0, 46.5), shaft_w=2.8, head_len=5.2, head_w=7.0, color=Icon.WHITE)

# Central encrypted tunnel circle hub
circle((50.0, 50.0), radius=17.0, style=Icon.fill_style(Cisco.BLUE, border_color=Icon.WHITE, border_units=3.0))

# Crisp white padlock inside the central circle
shackle_w = 8.8
arc(
    (50.0, 54.5),
    width=shackle_w,
    height=8.6,
    angle_start=0.0,
    angle_end=180.0,
    style=Icon.stroke_style(Icon.WHITE, width_units=2.3),
)
Icon.draw_round_segment(
    (50.0 - shackle_w / 2.0, 50.5), (50.0 - shackle_w / 2.0, 54.5), width_units=2.3, color=Icon.WHITE
)
Icon.draw_round_segment(
    (50.0 + shackle_w / 2.0, 50.5), (50.0 + shackle_w / 2.0, 54.5), width_units=2.3, color=Icon.WHITE
)

rectangle((50.0, 45.2), width=14.6, height=11.4, style=Icon.no_border_fill(Icon.WHITE, shape_r=2.0))
circle((50.0, 46.6), radius=1.7, style=Icon.no_border_fill(Cisco.BLUE))
polygon(
    [
        (49.2, 46.0),
        (50.8, 46.0),
        (51.3, 42.0),
        (48.7, 42.0),
    ],
    style=Icon.no_border_fill(Cisco.BLUE),
)

save()
