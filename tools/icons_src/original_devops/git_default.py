# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: git."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
w_inner = 1.7
CORAL_RED = "#F26B4E"


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 16) -> list[tuple[float, float]]:
    """Sample circular arc from deg0 to deg1."""
    return [
        (
            xc + r * math.cos(math.radians(deg0 + (deg1 - deg0) * (i / steps))),
            yc + r * math.sin(math.radians(deg0 + (deg1 - deg0) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Rounded coral-red diamond centered at (50, 50), spanning [11.0, 89.0]
r_corner = 5.2
d_center = 33.8
diamond_pts: list[tuple[float, float]] = [
    *_arc(50.0, 50.0 + d_center, r_corner, 45.0, 135.0),
    *_arc(50.0 - d_center, 50.0, r_corner, 135.0, 225.0),
    *_arc(50.0, 50.0 - d_center, r_corner, 225.0, 315.0),
    *_arc(50.0 + d_center, 50.0, r_corner, -45.0, 45.0),
]
polygon(diamond_pts, style=no_border_fill(CORAL_RED))

# 2. Branch bars (WHITE fill + DARK side borders)
# Top-left diamond edge satisfies y - x = d_center * sqrt(2) - r_corner * (sqrt(2) - 2)?
# At 135 deg on top arc: x = 50 - r_corner*cos(45), y = 50 + d_center + r_corner*sin(45)
# y - x = d_center + r_corner*sqrt(2) = 33.8 + 5.2*1.41421356 = 41.1539
node_top = (50.0, 66.0)
node_bot = (50.0, 33.0)
node_right = (66.5, 49.5)
r_node = 6.2
half_bar = 2.6
inv_sqrt2 = 1.0 / math.sqrt(2.0)

# Intersection of x + y = 116.0 with y - x = 41.1539
edge_cx = (116.0 - 41.1539) / 2.0
edge_cy = (116.0 + 41.1539) / 2.0
nx = half_bar * inv_sqrt2
ny = half_bar * inv_sqrt2

diag_bar = [
    (edge_cx + nx, edge_cy + ny),
    (node_right[0] + nx, node_right[1] + ny),
    (node_right[0] - nx, node_right[1] - ny),
    (edge_cx - nx, edge_cy - ny),
]
vert_bar = [
    (node_top[0] - half_bar, node_top[1]),
    (node_top[0] + half_bar, node_top[1]),
    (node_bot[0] + half_bar, node_bot[1]),
    (node_bot[0] - half_bar, node_bot[1]),
]

polygon(diag_bar, style=no_border_fill(WHITE))
polygon(vert_bar, style=no_border_fill(WHITE))

# Draw DARK side borders on both bars
draw_round_segment(diag_bar[0], diag_bar[1], width_units=w_inner, color=DARK)
draw_round_segment(diag_bar[3], diag_bar[2], width_units=w_inner, color=DARK)
draw_round_segment(vert_bar[0], vert_bar[3], width_units=w_inner, color=DARK)
draw_round_segment(vert_bar[1], vert_bar[2], width_units=w_inner, color=DARK)

# 3. Three WHITE circle nodes with DARK outlines on top of bar ends
for nxy in (node_top, node_bot, node_right):
    circle(nxy, radius=r_node, style=fill_style(WHITE, border_color=DARK, border_units=w_inner))

# 4. Crisp outer diamond DARK outline
draw_round_polyline(diamond_pts, width_units=w, color=DARK, closed=True)

save()
