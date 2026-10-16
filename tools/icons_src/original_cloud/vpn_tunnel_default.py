# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: vpn_tunnel."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, ellipse, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

cy = 41.0
cyl_h = 34.0
cyl_r = cyl_h / 2.0
rx = 8.5
x_left = 24.0
x_right = 70.0
aw = 3.2

# 1. Left incoming arrow shaft entering the tunnel
draw_round_segment((6.0, cy), (20.0, cy), width_units=aw, color=DARK)

# 2. 3D horizontal cylinder tunnel body (PASTEL_BLUE, smooth without rib dividers)
ellipse(
    (x_left, cy),
    width=rx * 2.0,
    height=cyl_h,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
rectangle(
    ((x_left + x_right) / 2.0, cy),
    width=x_right - x_left,
    height=cyl_h,
    style=no_border_fill(PASTEL_BLUE),
)
draw_round_segment((x_left, cy + cyl_r), (x_right, cy + cyl_r), width_units=w, color=DARK)
draw_round_segment((x_left, cy - cyl_r), (x_right, cy - cyl_r), width_units=w, color=DARK)

# 3. Right elliptical tunnel mouth (WHITE opening)
ellipse(
    (x_right, cy),
    width=rx * 2.0,
    height=cyl_h,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 4. Arrow emerging from the center of the right tunnel mouth
draw_round_segment((x_right - 1.0, cy), (93.0, cy), width_units=aw, color=DARK)
draw_round_polyline([(85.5, cy + 6.5), (93.0, cy), (85.5, cy - 6.5)], width_units=aw, color=DARK)

# 5. VPN padlock badge (~1.25x size: 22.5x18.8) at top-center of cylinder
lock_cx = 45.0
lock_cy = 59.5
shackle_w = 13.6
shackle_r = shackle_w / 2.0
shackle_top_y = 74.2

rectangle((lock_cx, 70.5), width=shackle_w, height=8.0, style=no_border_fill(WHITE))
ellipse((lock_cx, shackle_top_y), width=shackle_w, height=shackle_w, style=no_border_fill(WHITE))
draw_round_segment((lock_cx - shackle_r, 66.5), (lock_cx - shackle_r, shackle_top_y), width_units=2.7, color=DARK)
draw_round_segment((lock_cx + shackle_r, 66.5), (lock_cx + shackle_r, shackle_top_y), width_units=2.7, color=DARK)
arc(
    (lock_cx, shackle_top_y),
    width=shackle_w,
    height=shackle_w,
    angle_start=0.0,
    angle_end=180.0,
    style=stroke_style(DARK, width_units=2.7),
)
rectangle(
    (lock_cx, lock_cy),
    width=22.5,
    height=18.8,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.7, shape_r=4.2),
)
draw_round_segment((lock_cx, lock_cy - 0.5), (lock_cx, lock_cy - 4.6), width_units=2.2, color=DARK)
circle(
    (lock_cx, lock_cy + 1.8),
    radius=2.9,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
