# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco modern 2D icon: firewall (modern variant)."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

x_left = 23.0
y_bot = 31.0
wall_w = 54.0
wall_h = 38.0
gap = 2.0
num_rows = 6

brick_h = (wall_h - (num_rows - 1) * gap) / num_rows
full_w = (wall_w - 2.0 * gap) / 3.0
half_w = (wall_w - 3.0 * gap - 2.0 * full_w) / 2.0
brick_style = Icon.no_border_fill(Icon.WHITE, shape_r=0.7)

for row in range(num_rows):
    cy = y_bot + row * (brick_h + gap) + brick_h / 2.0
    if row % 2 == 1:
        # Three full bricks (top row = row 5)
        for col in range(3):
            cx = x_left + col * (full_w + gap) + full_w / 2.0
            rectangle((cx, cy), width=full_w, height=brick_h, style=brick_style)
    else:
        # Half + two full + half bricks
        widths = [half_w, full_w, full_w, half_w]
        x_cur = x_left
        for bw in widths:
            cx = x_cur + bw / 2.0
            rectangle((cx, cy), width=bw, height=brick_h, style=brick_style)
            x_cur += bw + gap

save()
