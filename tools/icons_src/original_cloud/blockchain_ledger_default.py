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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
radius = 15.0

blocks = [
    (25.0, 31.0, Icon.PASTEL_BLUE, Icon.PASTEL_BLUE_LIGHT),
    (50.0, 50.0, Icon.PASTEL_GREEN, Icon.PASTEL_BLUE),
    (75.0, 69.0, Icon.PASTEL_BLUE, Icon.PASTEL_GREEN),
]

# 1. Draw the 3 isometric 3D ledger blocks
for cx, cy, left_col, right_col in blocks:
    Icon.draw_iso_cube(
        cx,
        cy,
        radius=radius,
        top_color=Icon.WHITE,
        left_color=left_col,
        right_color=right_col,
        border_color=Icon.DARK,
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
            style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
        )
    Icon.draw_round_segment(p1, p2, width_units=5.0, color=Icon.DARK)
    Icon.draw_round_segment(p1, p2, width_units=1.8, color=Icon.PASTEL_GREEN)

save()
