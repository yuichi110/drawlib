# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: xml_markup."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
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

b = 2.0
w_line = 2.0

# WHITE document card base + top PASTEL_BLUE header bar
rectangle(
    (50.0, 50.0),
    width=72.0,
    height=68.0,
    style=fill_style(WHITE, shape_r=5.0),
)
draw_rounded_corner_block(
    14.0,
    72.0,
    86.0,
    84.0,
    r=5.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)
rectangle(
    (50.0, 50.0),
    width=72.0,
    height=68.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=b, shape_r=5.0),
)
draw_round_segment((14.0, 72.0), (86.0, 72.0), width_units=b, color=DARK)

# Central '<' '/' '>' geometric polygons
left_chevron = [
    (36.5, 64.5),
    (26.0, 55.0),
    (36.5, 45.5),
    (39.8, 48.6),
    (32.5, 55.0),
    (39.8, 61.4),
]
polygon(left_chevron, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(left_chevron, width_units=b, color=DARK, closed=True)

slash_pts = [
    (46.0, 45.0),
    (50.5, 45.0),
    (54.0, 65.0),
    (49.5, 65.0),
]
polygon(slash_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(slash_pts, width_units=b, color=DARK, closed=True)

right_chevron = [
    (63.5, 64.5),
    (74.0, 55.0),
    (63.5, 45.5),
    (60.2, 48.6),
    (67.5, 55.0),
    (60.2, 61.4),
]
polygon(right_chevron, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(right_chevron, width_units=b, color=DARK, closed=True)

# 2-child DOM tree branch below
draw_round_segment((50.0, 41.0), (50.0, 34.0), width_units=w_line, color=DARK)
draw_round_polyline(
    [(36.0, 28.0), (36.0, 34.0), (64.0, 34.0), (64.0, 28.0)],
    width_units=w_line,
    color=DARK,
)
circle(
    (36.0, 24.5),
    radius=3.8,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=b),
)
circle(
    (64.0, 24.5),
    radius=3.8,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=b),
)

save()
