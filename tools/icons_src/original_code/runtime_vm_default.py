# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: runtime_vm."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

b = 2.0

# Outer PASTEL_BLUE engine/VM frame
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=66.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=b, shape_r=6.0),
)

# Top VM header status dots
for x_dot, col in ((23.0, PASTEL_GREEN), (31.0, WHITE)):
    circle(
        (x_dot, 76.5),
        radius=2.4,
        style=fill_style(col, border_color=DARK, border_units=b),
    )

# Inner WHITE execution area
rectangle(
    (50.0, 47.0),
    width=62.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=b, shape_r=3.0),
)

# 3 stacked horizontal bytecode instruction bars
bars = [
    (55.0, 59.0, 38.0, PASTEL_GREEN),
    (52.0, 47.0, 32.0, PASTEL_BLUE_LIGHT),
    (54.0, 35.0, 36.0, PASTEL_BLUE),
]
for bx, by, bw, col in bars:
    rectangle(
        (bx, by),
        width=bw,
        height=7.5,
        style=fill_style(col, border_color=DARK, border_units=b, shape_r=2.5),
    )

# Left DARK execution pointer triangle pointing at top instruction bar
ptr_pts = [(24.5, 62.5), (24.5, 55.5), (31.5, 59.0)]
polygon(ptr_pts, style=no_border_fill(DARK))
draw_round_polyline(ptr_pts, width_units=b, color=DARK, closed=True)

save()
