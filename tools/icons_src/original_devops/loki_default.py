# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: loki."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.5
s = 0.935

# Tilted 'L' axis basis (~8.78 degrees counter-clockwise)
ang = math.radians(8.78)
ca, sa = math.cos(ang), math.sin(ang)
ox, oy = 25.4, 9.2


def _uv_rect(u0: float, v0: float, u1: float, v1: float) -> list[tuple[float, float]]:
    """Map an axis-aligned rectangle in tilted (u, v) space into scaled canvas coords."""
    raw = [
        (ox + u0 * ca - v0 * sa, oy + u0 * sa + v0 * ca),
        (ox + u1 * ca - v0 * sa, oy + u1 * sa + v0 * ca),
        (ox + u1 * ca - v1 * sa, oy + u1 * sa + v1 * ca),
        (ox + u0 * ca - v1 * sa, oy + u0 * sa + v1 * ca),
    ]
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in raw]


sq_size = 7.10
pitch = 10.65

# 1. Six bottom grid squares (3 cols x 2 rows) and two right horizontal bars in Colors.Amber2
amber_blocks: list[list[tuple[float, float]]] = []
for row in range(2):
    v0 = row * pitch
    v1 = v0 + sq_size
    for col in range(3):
        u0 = col * pitch
        amber_blocks.append(_uv_rect(u0, v0, u0 + sq_size, v1))
    # Right horizontal bar for this row
    u_bar0 = 3 * pitch
    amber_blocks.append(_uv_rect(u_bar0, v0, u_bar0 + 28.8, v1))

# 2. Six upper vertical bars (3 twin pairs) in Colors.Orange3 with clear transparent gaps
v_upper0 = 2 * pitch
bar_w = 2.60
pair_gap = sq_size - 2.0 * bar_w  # 1.90 units -> clear gap with w=1.5 stroke

upper_heights = [
    (52.5, 56.9),
    (59.8, 54.9),
    (48.5, 50.3),
]

orange_bars: list[list[tuple[float, float]]] = []
for col, (h_left, h_right) in enumerate(upper_heights):
    u_base = col * pitch
    orange_bars.append(_uv_rect(u_base, v_upper0, u_base + bar_w, v_upper0 + h_left))
    u_right = u_base + bar_w + pair_gap
    orange_bars.append(_uv_rect(u_right, v_upper0, u_right + bar_w, v_upper0 + h_right))

for pts in amber_blocks:
    polygon(pts, style=no_border_fill(Colors.Amber2))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

for pts in orange_bars:
    polygon(pts, style=no_border_fill(Colors.Orange3))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
