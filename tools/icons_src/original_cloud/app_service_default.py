# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: app_service."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Outer application window base fill
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=64.0,
    style=fill_style(WHITE, shape_r=7.0),
)

# Top window header bar
draw_rounded_corner_block(
    13.0,
    65.0,
    87.0,
    82.0,
    r=7.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)

# Outer window border and header divider
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=64.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=7.0),
)
draw_round_segment((13.0, 65.0), (87.0, 65.0), width_units=w, color=DARK)

# Window control dots
for x_dot, col in ((23.0, PASTEL_GREEN), (32.0, WHITE), (41.0, WHITE)):
    circle(
        (x_dot, 73.5),
        radius=2.8,
        style=fill_style(col, border_color=DARK, border_units=1.8),
    )

# Code brackets flanking the central launch badge
draw_round_polyline(
    [(29.0, 49.5), (21.5, 41.5), (29.0, 33.5)],
    width_units=2.5,
    color=DARK,
)
draw_round_polyline(
    [(71.0, 49.5), (78.5, 41.5), (71.0, 33.5)],
    width_units=2.5,
    color=DARK,
)

# Central launch/deploy badge
circle(
    (50.0, 41.5),
    radius=14.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4),
)
play_pts = [(46.0, 48.0), (46.0, 35.0), (57.5, 41.5)]
polygon(play_pts, style=no_border_fill(WHITE))
draw_round_polyline(play_pts, width_units=2.0, color=DARK, closed=True)

save()
