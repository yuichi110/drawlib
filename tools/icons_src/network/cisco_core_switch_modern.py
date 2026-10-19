# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: core switch (modern 2D variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

# Upper crossbar fabric blocks and X-switching links
x_left, x_right = 34.0, 66.0
y_top, y_bot = 73.0, 62.5

Icon.draw_round_segment((x_left, y_top), (x_right, y_top), width_units=1.8, color=Icon.WHITE)
Icon.draw_round_segment((x_left, y_bot), (x_right, y_bot), width_units=1.8, color=Icon.WHITE)
Icon.draw_round_segment((x_left, y_top), (x_right, y_bot), width_units=1.8, color=Icon.WHITE)
Icon.draw_round_segment((x_left, y_bot), (x_right, y_top), width_units=1.8, color=Icon.WHITE)

for bx in (x_left, x_right):
    for by in (y_top, y_bot):
        rectangle((bx, by), width=11.0, height=5.2, style=Icon.no_border_fill(Icon.WHITE))

# Chassis bay divider line across the badge interior
Icon.draw_round_segment((22.0, 54.0), (78.0, 54.0), width_units=2.2, color=Cisco.LIGHT_BLUE)

# Lower core switching emblem: crossed orbital rings + 4 cardinal arrows
cx, cy = 50.0, 34.5
for angle in (45.0, 135.0):
    ellipse(
        (cx, cy),
        width=34.0,
        height=11.0,
        style=Icon.fill_style(
            "#00000000",
            border_color=Icon.WHITE,
            border_units=1.8,
            angle=angle,
        ),
    )

for dx_dir, dy_dir in ((0.0, 1.0), (0.0, -1.0), (-1.0, 0.0), (1.0, 0.0)):
    Cisco.draw_arrow(
        (cx + dx_dir * 4.5, cy + dy_dir * 4.5),
        (cx + dx_dir * 18.2, cy + dy_dir * 18.2),
        shaft_w=3.4,
        head_len=5.5,
        head_w=8.0,
        color=Icon.WHITE,
    )

circle((cx, cy), radius=5.6, style=Icon.no_border_fill(Icon.WHITE))

save()
