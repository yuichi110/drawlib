# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: blockchain_ledger."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
radius = 15.0

blocks = [
    (25.0, 31.0, PASTEL_BLUE, PASTEL_BLUE_LIGHT),
    (50.0, 50.0, PASTEL_GREEN, PASTEL_BLUE),
    (75.0, 69.0, PASTEL_BLUE, PASTEL_GREEN),
]

# 1. Draw the 3 isometric 3D ledger blocks
for cx, cy, left_col, right_col in blocks:
    draw_iso_cube(
        cx,
        cy,
        radius=radius,
        top_color=WHITE,
        left_color=left_col,
        right_color=right_col,
        border_color=DARK,
        border_units=w,
    )

# 2. Connect blocks diagonally with bold cryptographic chain links and anchor nodes
links = [
    ((32.5, 36.7), (42.5, 44.3)),
    ((57.5, 55.7), (67.5, 63.3)),
]
for p1, p2 in links:
    for pt_node in (p1, p2):
        circle(
            pt_node,
            radius=3.2,
            style=fill_style(WHITE, border_color=DARK, border_units=2.0),
        )
    draw_round_segment(p1, p2, width_units=5.0, color=DARK)
    draw_round_segment(p1, p2, width_units=1.8, color=PASTEL_GREEN)

save()
