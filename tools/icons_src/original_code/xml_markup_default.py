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
from drawlib.utils import Gcp, Icon

Icon.setup()

b = 2.0
w_line = 2.0

# WHITE document card base + top PASTEL_BLUE header bar
rectangle(
    (50.0, 50.0),
    width=72.0,
    height=68.0,
    style=Icon.fill_style(Icon.WHITE, shape_r=5.0),
)
Gcp.draw_rounded_corner_block(
    14.0,
    72.0,
    86.0,
    84.0,
    r=5.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)
rectangle(
    (50.0, 50.0),
    width=72.0,
    height=68.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=b, shape_r=5.0),
)
Icon.draw_round_segment((14.0, 72.0), (86.0, 72.0), width_units=b, color=Icon.DARK)

# Central '<' '/' '>' geometric polygons
left_chevron = [
    (36.5, 64.5),
    (26.0, 55.0),
    (36.5, 45.5),
    (39.8, 48.6),
    (32.5, 55.0),
    (39.8, 61.4),
]
polygon(left_chevron, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(left_chevron, width_units=b, color=Icon.DARK, closed=True)

slash_pts = [
    (46.0, 45.0),
    (50.5, 45.0),
    (54.0, 65.0),
    (49.5, 65.0),
]
polygon(slash_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(slash_pts, width_units=b, color=Icon.DARK, closed=True)

right_chevron = [
    (63.5, 64.5),
    (74.0, 55.0),
    (63.5, 45.5),
    (60.2, 48.6),
    (67.5, 55.0),
    (60.2, 61.4),
]
polygon(right_chevron, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(right_chevron, width_units=b, color=Icon.DARK, closed=True)

# 2-child DOM tree branch below
Icon.draw_round_segment((50.0, 41.0), (50.0, 34.0), width_units=w_line, color=Icon.DARK)
Icon.draw_round_polyline(
    [(36.0, 28.0), (36.0, 34.0), (64.0, 34.0), (64.0, 28.0)],
    width_units=w_line,
    color=Icon.DARK,
)
circle(
    (36.0, 24.5),
    radius=3.8,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=b),
)
circle(
    (64.0, 24.5),
    radius=3.8,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=b),
)

save()
