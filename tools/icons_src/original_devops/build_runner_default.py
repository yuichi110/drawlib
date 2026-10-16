# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: build_runner."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_capsule,
    draw_round_polyline,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Worker box base fill
rectangle(
    (46.0, 50.0),
    width=60.0,
    height=56.0,
    style=fill_style(WHITE, shape_r=8.0),
)

# Top header bar
draw_rounded_corner_block(
    16.0,
    62.0,
    76.0,
    78.0,
    r=8.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)

# Outer worker box border and header divider
rectangle(
    (46.0, 50.0),
    width=60.0,
    height=56.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=8.0),
)
draw_round_segment((16.0, 62.0), (76.0, 62.0), width_units=w, color=DARK)

# Header status dots
for x_dot, col in ((25.0, PASTEL_GREEN), (34.0, WHITE)):
    circle(
        (x_dot, 70.0),
        radius=2.8,
        style=fill_style(col, border_color=DARK, border_units=1.8),
    )

# 8-tooth worker gear at (38.0, 42.0)
gx, gy = 38.0, 42.0
r_tooth = 13.8
for deg in (0.0, 45.0, 90.0, 135.0):
    rad = math.radians(deg)
    dx = r_tooth * math.cos(rad)
    dy = r_tooth * math.sin(rad)
    draw_capsule((gx - dx, gy - dy), (gx + dx, gy + dy), width_units=5.6, color=DARK)

circle(
    (gx, gy),
    radius=10.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.4),
)
circle(
    (gx, gy),
    radius=4.2,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Bottom-right play/run circular badge
circle(
    (70.0, 32.0),
    radius=16.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
play_pts = [(65.5, 39.0), (65.5, 25.0), (77.5, 32.0)]
polygon(play_pts, style=no_border_fill(WHITE))
draw_round_polyline(play_pts, width_units=2.2, color=DARK, closed=True)

save()
