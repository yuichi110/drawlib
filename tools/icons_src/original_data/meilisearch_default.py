# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: meilisearch."""

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


def _corner_fillet(
    p_prev: tuple[float, float],
    p_corner: tuple[float, float],
    p_next: tuple[float, float],
    radius: float,
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Compute exact circular arc points rounding p_corner between p_prev and p_next."""
    v1x, v1y = p_prev[0] - p_corner[0], p_prev[1] - p_corner[1]
    v2x, v2y = p_next[0] - p_corner[0], p_next[1] - p_corner[1]
    l1 = math.hypot(v1x, v1y)
    l2 = math.hypot(v2x, v2y)
    u1x, u1y = v1x / l1, v1y / l1
    u2x, u2y = v2x / l2, v2y / l2

    dot = max(-1.0, min(1.0, u1x * u2x + u1y * u2y))
    half_angle = 0.5 * math.acos(dot)
    tan_dist = radius / math.tan(half_angle)

    t1 = (p_corner[0] + u1x * tan_dist, p_corner[1] + u1y * tan_dist)
    t2 = (p_corner[0] + u2x * tan_dist, p_corner[1] + u2y * tan_dist)

    bx, by = u1x + u2x, u1y + u2y
    bl = math.hypot(bx, by)
    center_dist = radius / math.sin(half_angle)
    cx = p_corner[0] + (bx / bl) * center_dist
    cy = p_corner[1] + (by / bl) * center_dist

    a1 = math.atan2(t1[1] - cy, t1[0] - cx)
    a2 = math.atan2(t2[1] - cy, t2[0] - cx)
    diff = (a2 - a1 + math.pi) % (2.0 * math.pi) - math.pi

    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = a1 + diff * (i / steps)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts


def _build_speed_pill(x_bl: float) -> list[tuple[float, float]]:
    """Build one slanted Meilisearch speed pill with bottom-left at x_bl."""
    y_bot = 25.0
    y_top = 75.0
    w_bar = 17.5
    dx = 16.0

    c_bl = (x_bl, y_bot)
    c_tl = (x_bl + dx, y_top)
    c_tr = (x_bl + dx + w_bar, y_top)
    c_br = (x_bl + w_bar, y_bot)

    r_small = 2.0
    r_large = 12.5

    return [
        *_corner_fillet(c_br, c_bl, c_tl, r_small, steps=8),
        *_corner_fillet(c_bl, c_tl, c_tr, r_large, steps=18),
        *_corner_fillet(c_tl, c_tr, c_br, r_small, steps=8),
        *_corner_fillet(c_tr, c_br, c_bl, r_large, steps=18),
    ]


setup_icon()

w = 2.0

# 3 slanted parallel speed pills centered at (50, 50)
pills = [
    (10.25, Colors.Pink2),
    (33.25, Colors.Pink3),
    (56.25, Colors.Red3),
]

for x_start, color in pills:
    pts = _build_speed_pill(x_start)
    polygon(pts, style=no_border_fill(color))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
