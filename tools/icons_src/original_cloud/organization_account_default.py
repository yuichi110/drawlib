# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: organization_account."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Orthogonal org tree lines
draw_round_segment((50.0, 67.0), (50.0, 36.0), width_units=w, color=DARK)
draw_round_polyline(
    [(22.0, 36.0), (22.0, 52.0), (78.0, 52.0), (78.0, 36.0)],
    width_units=w,
    color=DARK,
    corner_r=4.0,
)

# Top root management account card
rectangle(
    (50.0, 76.0),
    width=36.0,
    height=18.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=4.0),
)
circle(
    (39.5, 76.0),
    radius=3.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)
draw_round_segment((47.5, 76.0), (61.5, 76.0), width_units=2.0, color=DARK)

# 3 child account/subscription cards
child_configs = [
    (22.0, PASTEL_BLUE),
    (50.0, WHITE),
    (78.0, PASTEL_BLUE),
]
for cx, fill_col in child_configs:
    rectangle(
        (cx, 26.0),
        width=22.0,
        height=20.0,
        style=fill_style(fill_col, border_color=DARK, border_units=w, shape_r=3.5),
    )
    draw_round_segment((cx - 5.5, 26.0), (cx + 5.5, 26.0), width_units=2.0, color=DARK)

save()
