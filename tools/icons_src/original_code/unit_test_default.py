# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: unit_test."""

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

b = 2.0
w_line = 2.0

# WHITE clipboard / test card
rectangle(
    (44.0, 52.0),
    width=56.0,
    height=66.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=5.0),
)

# Top PASTEL_BLUE clip
rectangle(
    (44.0, 83.0),
    width=26.0,
    height=10.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=3.0),
)

# 3 horizontal test rows (small dot + DARK line)
rows = [
    (65.0, 62.0),
    (51.0, 58.0),
    (37.0, 48.0),
]
for y_row, x_end in rows:
    circle(
        (25.0, y_row),
        radius=3.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=b),
    )
    draw_round_segment((33.0, y_row), (x_end, y_row), width_units=w_line, color=DARK)

# Bottom-right overlapping PASTEL_GREEN circle badge
circle(
    (70.0, 28.0),
    radius=17.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=b),
)

# Crisp WHITE / DARK checkmark polygon inside badge
check_pts = [
    (60.2, 27.2),
    (67.8, 19.6),
    (79.6, 31.4),
    (76.6, 34.4),
    (67.8, 25.6),
    (63.2, 30.2),
]
polygon(check_pts, style=no_border_fill(WHITE))
draw_round_polyline(check_pts, width_units=b, color=DARK, closed=True)

save()
