# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: hospital."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
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

w_outer = 2.0
w_inner = 1.6

# 1. Side medical wings (PASTEL_BLUE_LIGHT, x=15..85, y=16..60)
rectangle(
    (50.0, 38.0),
    width=70.0,
    height=44.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.0),
)
# Side wing roof caps (PASTEL_BLUE)
for wx in (21.5, 78.5):
    rectangle(
        (wx, 61.5),
        width=15.0,
        height=3.5,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.0),
    )

# 2. Central multi-story tower (WHITE, x=28..72, y=16..74)
rectangle(
    (50.0, 45.0),
    width=44.0,
    height=58.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)
# Central tower roof cap (PASTEL_BLUE)
rectangle(
    (50.0, 75.5),
    width=48.0,
    height=4.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

# 3. Side wing windows (WHITE, x=21.5 and x=78.5, 3 floors)
for wx in (21.5, 78.5):
    for wy in (50.0, 38.0, 26.0):
        rectangle(
            (wx, wy),
            width=6.5,
            height=7.5,
            style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
        )

# 4. Central tower windows (PASTEL_BLUE_LIGHT, 2 rows of 3)
for wy in (54.0, 41.5):
    for wx in (36.5, 50.0, 63.5):
        rectangle(
            (wx, wy),
            width=7.5,
            height=8.0,
            style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.0),
        )

# 5. Ground-floor emergency entrance doors (PASTEL_BLUE)
rectangle(
    (50.0, 24.5),
    width=18.0,
    height=17.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.5),
)
draw_round_segment((50.0, 16.0), (50.0, 33.0), width_units=w_inner, color=DARK)

# 6. Top circular badge with PASTEL_GREEN medical cross at (50.0, 75.5)
cx, cy = 50.0, 75.5
circle(
    (cx, cy),
    radius=12.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)

# 12-vertex medical cross polygon
a = 3.2  # half arm width
b = 8.0  # half cross length
cross_pts = [
    (cx - a, cy + b),
    (cx + a, cy + b),
    (cx + a, cy + a),
    (cx + b, cy + a),
    (cx + b, cy - a),
    (cx + a, cy - a),
    (cx + a, cy - b),
    (cx - a, cy - b),
    (cx - a, cy - a),
    (cx - b, cy - a),
    (cx - b, cy + a),
    (cx - a, cy + a),
]
polygon(cross_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(cross_pts, width_units=w_inner, color=DARK, closed=True)

# 7. Ground foundation plinth
rectangle(
    (50.0, 14.5),
    width=76.0,
    height=3.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

save()
