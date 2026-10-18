# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: compiler_build."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

b = 2.0
w_line = 2.0

# 1. Top-left WHITE source code mini-card
rectangle(
    (25.0, 76.0),
    width=26.0,
    height=22.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=3.0),
)
draw_round_segment((17.5, 79.5), (32.5, 79.5), width_units=w_line, color=DARK)
draw_round_segment((17.5, 72.5), (28.5, 72.5), width_units=w_line, color=DARK)

# 2. Arrow from source card into top of compiler box
draw_round_polyline(
    [(38.0, 76.0), (50.0, 76.0), (50.0, 66.5)],
    width_units=w_line,
    color=DARK,
)
draw_round_polyline(
    [(46.5, 70.0), (50.0, 66.0), (53.5, 70.0)],
    width_units=w_line,
    color=DARK,
)

# 3. Central PASTEL_BLUE trapezoid/funnel compiler box
funnel_pts = [
    (36.0, 62.0),
    (64.0, 62.0),
    (59.0, 36.0),
    (41.0, 36.0),
]
polygon(
    funnel_pts,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=4.0),
)

# Inner gear/wheel inside compiler box
for deg in range(0, 360, 60):
    rad = math.radians(deg)
    draw_round_segment(
        (50.0 + 4.5 * math.cos(rad), 50.0 + 4.5 * math.sin(rad)),
        (50.0 + 8.0 * math.cos(rad), 50.0 + 8.0 * math.sin(rad)),
        width_units=w_line,
        color=DARK,
    )
circle(
    (50.0, 50.0),
    radius=5.2,
    style=fill_style(WHITE, border_color=DARK, border_units=b),
)

# 4. Arrow from compiler box to bottom-right binary cube
draw_round_polyline(
    [(50.0, 36.0), (50.0, 26.0), (59.5, 26.0)],
    width_units=w_line,
    color=DARK,
)
draw_round_polyline(
    [(56.0, 29.5), (60.0, 26.0), (56.0, 22.5)],
    width_units=w_line,
    color=DARK,
)

# 5. Bottom-right isometric PASTEL_GREEN binary cube
draw_iso_cube(
    76.0,
    26.0,
    radius=13.5,
    top_color=PASTEL_GREEN,
    left_color=PASTEL_GREEN,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=b,
)

save()
