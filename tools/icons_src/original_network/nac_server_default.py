# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: nac_server."""

import math

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

# 1. Tall server appliance chassis
rectangle(
    (44.0, 50.0),
    width=54.0,
    height=76.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)

# 2. Upper WHITE identity badge panel
rectangle(
    (44.0, 58.0),
    width=40.0,
    height=42.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, shape_r=5.0),
)

# 3. User avatar inside badge panel (head + shoulder dome)
circle(
    (44.0, 66.0),
    radius=7.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0),
)

dome_pts = [
    (
        44.0 + 12.0 * math.cos(math.radians(deg)),
        44.0 + 11.0 * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
polygon(dome_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(dome_pts, width_units=2.0, color=DARK, closed=True)

# 4. Lower server slot line
draw_round_segment((28.0, 24.0), (52.0, 24.0), width_units=2.4, color=DARK)

# 5. Foreground bottom-right verification badge circle
circle(
    (70.0, 30.0),
    radius=15.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
draw_round_polyline(
    [(63.5, 29.5), (68.5, 24.5), (77.0, 35.0)],
    width_units=3.2,
    color=DARK,
)

save()
