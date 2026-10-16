# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco classic 3D icon: vpn_gateway (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, ellipse, polygon, rectangle
from drawlib.utils import (
    CISCO_BLUE,
    CISCO_DARK_BLUE,
    WHITE,
    draw_cisco_3d_box,
    draw_cisco_arrow,
    draw_round_segment,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

x0 = 12.0
y0 = 15.0
w_front = 58.0
h_front = 52.0
dx = 16.0
dy = 14.0
x1 = x0 + w_front

draw_cisco_3d_box(x0, y0, w_front, h_front, dx, dy)

# Cylindrical tunnel outline across the front face + port on right side face
tun_cy = 41.0
tun_half_h = 12.5
tun_x_left = 20.0
arc(
    (tun_x_left, tun_cy),
    width=9.0,
    height=tun_half_h * 2.0,
    angle_start=90.0,
    angle_end=270.0,
    style=stroke_style(WHITE, width_units=1.8),
)
draw_round_segment(
    (tun_x_left, tun_cy + tun_half_h),
    (x1 - 0.3, tun_cy + tun_half_h),
    width_units=1.8,
    color=WHITE,
)
draw_round_segment(
    (tun_x_left, tun_cy - tun_half_h),
    (x1 - 0.3, tun_cy - tun_half_h),
    width_units=1.8,
    color=WHITE,
)
ellipse(
    (x1 + dx * 0.52, tun_cy + dy * 0.52),
    width=6.5,
    height=tun_half_h * 1.75,
    style=stroke_style(WHITE, width_units=1.7),
)

# Left and right tunnel arrows flanking the center padlock
draw_cisco_arrow((19.0, tun_cy + 4.2), (30.5, tun_cy + 4.2), shaft_w=2.4, head_len=4.8, head_w=6.2, color=WHITE)
draw_cisco_arrow((65.5, tun_cy - 4.2), (54.0, tun_cy - 4.2), shaft_w=2.4, head_len=4.8, head_w=6.2, color=WHITE)

# Form-fitting blue halo behind padlock (narrower at shackle, wider at body)
lock_cx = 42.0
circle((lock_cx, 49.5), radius=8.2, style=no_border_fill(CISCO_BLUE))
rectangle((lock_cx, 46.0), width=16.4, height=8.0, style=no_border_fill(CISCO_BLUE))
rectangle((lock_cx, 35.0), width=23.5, height=19.5, style=no_border_fill(CISCO_BLUE, shape_r=3.2))

# Crisp white padlock shackle
shackle_w = 11.5
shackle_y_bot = 43.0
shackle_y_arc = 49.5
arc(
    (lock_cx, shackle_y_arc),
    width=shackle_w,
    height=11.0,
    angle_start=0.0,
    angle_end=180.0,
    style=stroke_style(WHITE, width_units=2.7),
)
draw_round_segment(
    (lock_cx - shackle_w / 2.0, shackle_y_bot),
    (lock_cx - shackle_w / 2.0, shackle_y_arc),
    width_units=2.7,
    color=WHITE,
)
draw_round_segment(
    (lock_cx + shackle_w / 2.0, shackle_y_bot),
    (lock_cx + shackle_w / 2.0, shackle_y_arc),
    width_units=2.7,
    color=WHITE,
)

# Crisp white padlock body + keyhole
rectangle((lock_cx, 35.0), width=19.5, height=15.5, style=no_border_fill(WHITE, shape_r=2.4))
circle((lock_cx, 37.0), radius=2.3, style=no_border_fill(CISCO_DARK_BLUE))
polygon(
    [
        (lock_cx - 1.1, 36.2),
        (lock_cx + 1.1, 36.2),
        (lock_cx + 1.8, 30.8),
        (lock_cx - 1.8, 30.8),
    ],
    style=no_border_fill(CISCO_DARK_BLUE),
)

save()
