# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: vpn_gateway."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, ellipse, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cisco_arrow,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w_shape = 1.8
w_line = 2.7

# 1. Outer horizontal tunnel pipe card
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=40.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape, shape_r=18.0),
)

# 2. Inner WHITE tunnel channel
rectangle(
    (50.0, 50.0),
    width=64.0,
    height=24.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=11.0),
)

# 3. Left & right horizontal tunnel arrows
draw_cisco_arrow(
    (21.0, 50.0),
    (35.0, 50.0),
    shaft_w=w_line,
    head_len=5.5,
    head_w=7.5,
    color=DARK,
)
draw_cisco_arrow(
    (65.0, 50.0),
    (79.0, 50.0),
    shaft_w=w_line,
    head_len=5.5,
    head_w=7.5,
    color=DARK,
)

# 4. Central padlock shackle (with white interior backing)
shackle_w = 14.0
shackle_h = 16.0
shackle_r = shackle_w / 2.0
shackle_cy = 56.5

rectangle((50.0, 54.0), width=shackle_w, height=5.0, style=no_border_fill(WHITE))
ellipse((50.0, shackle_cy), width=shackle_w, height=shackle_h, style=no_border_fill(WHITE))

draw_round_segment((50.0 - shackle_r, 52.0), (50.0 - shackle_r, shackle_cy), width_units=w_line, color=DARK)
draw_round_segment((50.0 + shackle_r, 52.0), (50.0 + shackle_r, shackle_cy), width_units=w_line, color=DARK)
arc(
    (50.0, shackle_cy),
    width=shackle_w,
    height=shackle_h,
    angle_start=0.0,
    angle_end=180.0,
    style=stroke_style(DARK, width_units=w_line),
)

# 5. Lock body in PASTEL_GREEN
rectangle(
    (50.0, 44.0),
    width=22.0,
    height=18.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape, shape_r=4.0),
)

# 6. Keyhole dot + stem
circle((50.0, 45.6), radius=2.1, style=fill_style(DARK))
draw_round_segment((50.0, 45.6), (50.0, 41.2), width_units=w_line, color=DARK)

save()
