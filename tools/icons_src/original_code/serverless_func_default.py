# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: serverless_func."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

b = 1.8

# Rounded WHITE function card
rectangle(
    (46.0, 50.0),
    width=64.0,
    height=64.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=7.0),
)

# Left PASTEL_BLUE '<' and '>' code brackets
left_bracket = [
    (28.5, 61.5),
    (19.0, 50.0),
    (28.5, 38.5),
    (32.5, 41.8),
    (25.7, 50.0),
    (32.5, 58.2),
]
polygon(left_bracket, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(left_bracket, width_units=b, color=DARK, closed=True)

right_bracket = [
    (40.0, 61.5),
    (49.5, 50.0),
    (40.0, 38.5),
    (36.0, 41.8),
    (42.8, 50.0),
    (36.0, 58.2),
]
polygon(right_bracket, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(right_bracket, width_units=b, color=DARK, closed=True)

# Overlapping PASTEL_GREEN lightning bolt on the right
bolt_pts = [
    (82.0, 76.0),
    (66.5, 76.0),
    (58.0, 47.0),
    (70.5, 47.0),
    (62.5, 15.0),
    (88.5, 52.0),
    (75.0, 52.0),
]
polygon(bolt_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(bolt_pts, width_units=b, color=DARK, closed=True)

save()
