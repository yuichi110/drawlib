# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: calendar."""

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


x0, y0, x1, y1 = 16.0, 14.0, 84.0, 78.0
y_hdr = 60.0
r_card = 5.5

# 1. WHITE calendar card body
card_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_card, y0 + r_card, r_card, 180.0, 270.0),
    *_arc_pts(x1 - r_card, y0 + r_card, r_card, 270.0, 360.0),
    *_arc_pts(x1 - r_card, y1 - r_card, r_card, 0.0, 90.0),
    *_arc_pts(x0 + r_card, y1 - r_card, r_card, 90.0, 180.0),
]
polygon(card_pts, style=no_border_fill(WHITE))

# 2. PASTEL_BLUE top header bar
hdr_pts: list[tuple[float, float]] = [
    (x0, y_hdr),
    (x1, y_hdr),
    *_arc_pts(x1 - r_card, y1 - r_card, r_card, 0.0, 90.0),
    *_arc_pts(x0 + r_card, y1 - r_card, r_card, 90.0, 180.0),
]
polygon(hdr_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(card_pts, width_units=w_outer, color=DARK, closed=True)
draw_round_segment((x0, y_hdr), (x1, y_hdr), width_units=w_outer, color=DARK)

# 3. Two top binding rings
for rx in (33.5, 66.5):
    rectangle(
        (rx, 78.5),
        width=7.0,
        height=14.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=3.5),
    )

# 4. Date grid (3 columns x 2 rows) with one PASTEL_GREEN highlighted cell
for cy in (46.5, 29.0):
    for cx in (30.0, 50.0, 70.0):
        is_highlight = cx == 70.0 and cy == 46.5
        col = PASTEL_GREEN if is_highlight else PASTEL_BLUE_LIGHT
        rectangle(
            (cx, cy),
            width=13.5,
            height=10.5,
            style=fill_style(col, border_color=DARK, border_units=w_inner, shape_r=2.2),
        )

save()
