# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: private_endpoint."""

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

# Horizontal connection conduit between endpoint socket and target service
draw_round_segment((20.0, 46.0), (80.0, 46.0), width_units=w, color=DARK)

# Left endpoint socket node
circle(
    (20.0, 46.0),
    radius=7.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

# Padlock shackle above the shielded private tunnel
tx = 50.0
shackle_w = 16.0
shackle_r = shackle_w / 2.0
draw_round_segment((tx - shackle_r, 56.0), (tx - shackle_r, 65.5), width_units=w, color=DARK)
draw_round_segment((tx + shackle_r, 56.0), (tx + shackle_r, 65.5), width_units=w, color=DARK)
arc(
    (tx, 65.5),
    width=shackle_w,
    height=shackle_w,
    angle_start=0.0,
    angle_end=180.0,
    style=stroke_style(DARK, width_units=w),
)

# Shielded private tunnel body
rectangle(
    (tx, 46.0),
    width=30.0,
    height=24.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=5.0),
)

# Keyhole inside the tunnel body
draw_round_segment((tx, 45.0), (tx, 39.5), width_units=2.4, color=DARK)
circle(
    (tx, 48.5),
    radius=3.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Target service node on the right
circle(
    (80.0, 46.0),
    radius=10.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (80.0, 46.0),
    radius=3.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
