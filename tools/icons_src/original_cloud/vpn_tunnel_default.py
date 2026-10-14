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
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Horizontal tunnel pipe
rectangle(
    (50.0, 44.0),
    width=74.0,
    height=30.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.0),
)
for rib_x in (26.0, 74.0):
    draw_round_segment((rib_x, 29.0), (rib_x, 59.0), width_units=2.3, color=DARK)

# Padlock shackle above the lock body
shackle_w = 18.0
shackle_r = shackle_w / 2.0
draw_round_segment((50.0 - shackle_r, 56.0), (50.0 - shackle_r, 67.0), width_units=w, color=DARK)
draw_round_segment((50.0 + shackle_r, 56.0), (50.0 + shackle_r, 67.0), width_units=w, color=DARK)
arc(
    (50.0, 67.0),
    width=shackle_w,
    height=shackle_w,
    angle_start=0.0,
    angle_end=180.0,
    style=stroke_style(DARK, width_units=w),
)

# Foreground padlock body
rectangle(
    (50.0, 44.0),
    width=28.0,
    height=26.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=5.0),
)

# Keyhole inside lock body (draw stem before circle so circle border is clean)
draw_round_segment((50.0, 43.0), (50.0, 37.5), width_units=2.4, color=DARK)
circle(
    (50.0, 46.5),
    radius=4.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
