# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: presentation."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
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


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 10,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Tripod stand legs and top mount peg
draw_round_segment((50.0, 36.0), (50.0, 16.0), width_units=w_outer, color=DARK)
draw_round_segment((43.5, 36.0), (29.0, 16.0), width_units=w_outer, color=DARK)
draw_round_segment((56.5, 36.0), (71.0, 16.0), width_units=w_outer, color=DARK)

draw_round_segment((50.0, 80.0), (50.0, 85.5), width_units=w_outer, color=DARK)
draw_round_segment((45.5, 85.5), (54.5, 85.5), width_units=w_outer, color=DARK)

# 2. 16:9 presentation board (WHITE screen + PASTEL_BLUE top bar)
x0, y0, x1, y1 = 14.0, 36.0, 86.0, 80.0
y_bar = 70.0
r_board = 4.0

board_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_board, y0 + r_board, r_board, 180.0, 270.0),
    *_arc_pts(x1 - r_board, y0 + r_board, r_board, 270.0, 360.0),
    *_arc_pts(x1 - r_board, y1 - r_board, r_board, 0.0, 90.0),
    *_arc_pts(x0 + r_board, y1 - r_board, r_board, 90.0, 180.0),
]
polygon(board_pts, style=no_border_fill(WHITE))

bar_pts: list[tuple[float, float]] = [
    (x0, y_bar),
    (x1, y_bar),
    *_arc_pts(x1 - r_board, y1 - r_board, r_board, 0.0, 90.0),
    *_arc_pts(x0 + r_board, y1 - r_board, r_board, 90.0, 180.0),
]
polygon(bar_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(board_pts, width_units=w_outer, color=DARK, closed=True)
draw_round_segment((x0, y_bar), (x1, y_bar), width_units=w_outer, color=DARK)

# 3. Rising bar chart inside screen (PASTEL_BLUE_LIGHT & PASTEL_GREEN)
y_base = 43.0
bars = [
    (34.0, 9.0, PASTEL_BLUE_LIGHT),
    (50.0, 14.5, PASTEL_BLUE_LIGHT),
    (66.0, 20.5, PASTEL_GREEN),
]
for bx, bh, col in bars:
    rectangle(
        (bx, y_base + bh / 2.0),
        width=10.5,
        height=bh,
        style=fill_style(col, border_color=DARK, border_units=w_inner, shape_r=1.5),
    )

draw_round_segment((24.5, y_base), (75.5, y_base), width_units=w_inner, color=DARK)

save()
