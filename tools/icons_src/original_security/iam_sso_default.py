# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: iam_sso."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8
w_line = 2.7

# 1. Horizontal ID badge card (x=12..88, y=18..74)
rectangle(
    (50.0, 46.0),
    width=76.0,
    height=56.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=7.0),
)

# 2. Top lanyard clip at (50, 74)
rectangle(
    (50.0, 74.0),
    width=20.0,
    height=12.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape, shape_r=3.5),
)

# 3. Left user avatar (head circle + shoulder dome)
circle(
    (31.0, 51.5),
    radius=7.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape),
)

dome_pts = [
    (
        31.0 + 12.0 * math.cos(math.radians(deg)),
        30.5 + 10.5 * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
polygon(dome_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(dome_pts, width_units=w_shape, color=DARK, closed=True)

# 4. Right credential lines in upper-right of badge
draw_round_segment((50.0, 54.0), (77.0, 54.0), width_units=w_line, color=DARK)
draw_round_segment((50.0, 44.0), (69.0, 44.0), width_units=w_line, color=DARK)

# 5. Bottom-right overlapping key badge (circular bow + horizontal shaft with 2 downward teeth)
bow_cx, bow_cy = 56.0, 20.25
bow_r = 10.0
shaft_y_top = 23.5
shaft_y_bot = 17.0
join_deg = math.degrees(math.asin((shaft_y_top - bow_cy) / bow_r))

bow_arc_pts = [
    (
        bow_cx + bow_r * math.cos(math.radians(deg)),
        bow_cy + bow_r * math.sin(math.radians(deg)),
    )
    for deg in [join_deg + (360.0 - 2.0 * join_deg) * (i / 36) for i in range(37)]
]
key_pts = [
    *bow_arc_pts,
    (73.5, shaft_y_bot),
    (73.5, 12.5),
    (79.0, 12.5),
    (79.0, shaft_y_bot),
    (83.5, shaft_y_bot),
    (83.5, 11.5),
    (89.0, 11.5),
    (89.0, shaft_y_top),
]
polygon(key_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(key_pts, width_units=w_shape, color=DARK, closed=True)

circle(
    (54.5, bow_cy),
    radius=3.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)

save()
