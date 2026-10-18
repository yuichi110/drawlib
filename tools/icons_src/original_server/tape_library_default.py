# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: tape_library."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Classic horizontal LTO tape cassette housing
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=54.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Top white label strip
rectangle(
    (50.0, 68.0),
    width=62.0,
    height=9.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.5),
)

# Bottom trapezoid tape guide recess at bottom edge
recess_pts = [
    (26.0, 23.0),
    (74.0, 23.0),
    (69.0, 32.0),
    (31.0, 32.0),
]
polygon(recess_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(recess_pts, width_units=2.0, color=DARK, closed=True)

# Horizontal dark tape line linking the top of the two reels
draw_round_segment((33.0, 57.5), (67.0, 57.5), width_units=2.0, color=DARK)

# Two symmetric tape reels
for x_reel in (33.0, 67.0):
    circle(
        (x_reel, 46.0),
        radius=11.5,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )
    circle(
        (x_reel, 46.0),
        radius=4.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

save()
