# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: identity_auth."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
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

w = ORIG_STROKE

# Outer ID badge card
rectangle(
    (50.0, 46.0),
    width=76.0,
    height=54.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Top lanyard clip
rectangle(
    (50.0, 74.0),
    width=20.0,
    height=12.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=3.5),
)

# Left user avatar: head + shoulder dome
circle(
    (32.0, 52.0),
    radius=7.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0),
)

dome_pts = [
    (
        32.0 + 12.0 * math.cos(math.radians(deg)),
        32.0 + 10.0 * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
polygon(dome_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(dome_pts, width_units=2.0, color=DARK, closed=True)

# Right credential lines
draw_round_segment((52.0, 52.0), (76.0, 52.0), width_units=2.0, color=DARK)
draw_round_segment((52.0, 38.0), (70.0, 38.0), width_units=2.0, color=DARK)

save()
