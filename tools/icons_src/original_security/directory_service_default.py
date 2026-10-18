# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: directory_service."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w_shape = 2.0
w_line = 2.0

# 1. Orthogonal T-branch hierarchy connectors (drawn behind nodes)
# Root to middle OUs
draw_round_segment((50.0, 70.0), (50.0, 58.0), width_units=w_line, color=DARK)
draw_round_polyline(
    [(28.0, 50.0), (28.0, 58.0), (72.0, 58.0), (72.0, 50.0)],
    width_units=w_line,
    color=DARK,
)

# Left OU to left two bottom user circles
draw_round_segment((28.0, 34.5), (28.0, 31.0), width_units=w_line, color=DARK)
draw_round_polyline(
    [(17.0, 27.0), (17.0, 31.0), (39.0, 31.0), (39.0, 27.0)],
    width_units=w_line,
    color=DARK,
)

# Right OU to right two bottom user circles
draw_round_segment((72.0, 34.5), (72.0, 31.0), width_units=w_line, color=DARK)
draw_round_polyline(
    [(61.0, 27.0), (61.0, 31.0), (83.0, 31.0), (83.0, 27.0)],
    width_units=w_line,
    color=DARK,
)

# 2. Top PASTEL_GREEN root rounded square at (50, 78) (16x16)
rectangle(
    (50.0, 78.0),
    width=16.0,
    height=16.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape, shape_r=3.5),
)

# 3. Two middle PASTEL_BLUE OU rounded squares at (28, 42) and (72, 42) (15x15)
for ou_x in (28.0, 72.0):
    rectangle(
        (ou_x, 42.0),
        width=15.0,
        height=15.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape, shape_r=3.5),
    )

# 4. Four bottom WHITE user circles at x = 17, 39, 61, 83, y = 20
for user_x in (17.0, 39.0, 61.0, 83.0):
    circle(
        (user_x, 20.0),
        radius=7.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
    )
    circle(
        (user_x, 20.0),
        radius=2.5,
        style=fill_style(PASTEL_BLUE),
    )

save()
