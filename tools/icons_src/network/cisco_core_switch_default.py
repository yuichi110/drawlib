# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: core switch (classic 3D default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
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
    stroke_style,
)

setup_icon()

# Tall modular chassis switch (x in [18, 82], y in [10, 88])
x0, y0 = 18.0, 10.0
w_front, h_front = 52.0, 66.0
dx, dy = 12.0, 12.0

draw_cisco_3d_box(x0, y0, w_front, h_front, dx, dy)

# Horizontal line-card / supervisor bay divider across front and right side face
y_div = 52.0
draw_round_segment((x0 + 1.0, y_div), (x0 + w_front, y_div), width_units=1.6, color=WHITE)
draw_round_segment(
    (x0 + w_front, y_div),
    (x0 + w_front + dx - 1.0, y_div + dy - 1.0),
    width_units=1.4,
    color=WHITE,
)

# Subtle lower line-card slot tick marks on the right side face
for y_slot in (24.0, 38.0):
    draw_round_segment(
        (x0 + w_front + 2.5, y_slot + 2.5),
        (x0 + w_front + dx - 2.0, y_slot + dy - 2.0),
        width_units=1.0,
        color=CISCO_LIGHT_BLUE,
    )

# Upper bay: dual supervisor / crossbar switching fabric (center=(44.0, 64.0))
cx = x0 + w_front / 2.0
x_left, x_right = cx - 14.0, cx + 14.0
y_top_blk, y_bot_blk = 69.0, 59.0

draw_round_segment((x_left, y_top_blk), (x_right, y_top_blk), width_units=1.5, color=WHITE)
draw_round_segment((x_left, y_bot_blk), (x_right, y_bot_blk), width_units=1.5, color=WHITE)
draw_round_segment((x_left, y_top_blk), (x_right, y_bot_blk), width_units=1.5, color=WHITE)
draw_round_segment((x_left, y_bot_blk), (x_right, y_top_blk), width_units=1.5, color=WHITE)

for bx in (x_left, x_right):
    for by in (y_top_blk, y_bot_blk):
        rectangle((bx, by), width=9.0, height=4.6, style=no_border_fill(WHITE))

# Lower bay: orbital switching rings + 4 cardinal switching arrows (center=(44.0, 31.0))
cy_lower = 31.0
for angle in (45.0, 135.0):
    ellipse(
        (cx, cy_lower),
        width=33.0,
        height=10.5,
        style=fill_style(
            "#00000000",
            border_color=WHITE,
            border_units=1.5,
            angle=angle,
        ),
    )

for dx_dir, dy_dir in ((0.0, 1.0), (0.0, -1.0), (-1.0, 0.0), (1.0, 0.0)):
    draw_cisco_arrow(
        (cx + dx_dir * 4.5, cy_lower + dy_dir * 4.5),
        (cx + dx_dir * 17.5, cy_lower + dy_dir * 17.5),
        shaft_w=3.2,
        head_len=5.2,
        head_w=7.6,
        color=WHITE,
    )

circle(
    (cx, cy_lower),
    radius=6.2,
    style=fill_style(CISCO_LIGHT_BLUE, border_color=WHITE, border_units=1.6),
)

save()
