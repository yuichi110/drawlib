# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: rook."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Tapered tower shaft (PASTEL_BLUE, y=26..66) with arched transparent window cutout
shaft_pts = [
    (29.5, 25.5),
    (70.5, 25.5),
    (66.5, 66.5),
    (33.5, 66.5),
]
win_pts: list[tuple[float, float]] = [(43.0, 35.0), (57.0, 35.0), (57.0, 48.0)]
steps_arch = 16
for i in range(steps_arch + 1):
    ang = math.radians(180.0 * (i / steps_arch))
    win_pts.append((50.0 + 7.0 * math.cos(ang), 48.0 + 7.0 * math.sin(ang)))

draw_compound_polygon([shaft_pts, win_pts], color=PASTEL_BLUE)
draw_round_polyline(shaft_pts, width_units=w, color=DARK, closed=True)
draw_round_polyline(win_pts, width_units=2.3, color=DARK, closed=True)

# 2. Stepped base (y=14..26)
# Upper base step (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 23.0),
    width=45.0,
    height=5.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.5, shape_r=1.8),
)
# Lower wider plinth (PASTEL_BLUE)
rectangle(
    (50.0, 17.0),
    width=52.0,
    height=6.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=2.2),
)

# 4. Top crenellations / battlements crown (PASTEL_GREEN, y=66..84)
crown_pts = [
    (26.5, 66.0),
    (73.5, 66.0),
    (73.5, 84.0),
    (61.5, 84.0),
    (61.5, 74.5),
    (56.0, 74.5),
    (56.0, 84.0),
    (44.0, 84.0),
    (44.0, 74.5),
    (38.5, 74.5),
    (38.5, 84.0),
    (26.5, 84.0),
]
polygon(crown_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(crown_pts, width_units=w, color=DARK, closed=True)

save()
