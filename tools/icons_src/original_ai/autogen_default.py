# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: autogen."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0


def _rounded_rect_pts(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    r: float,
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Generate smooth rounded rectangle vertices."""
    corners = [
        (x1 - r, y1 - r, 0.0, 90.0),
        (x0 + r, y1 - r, 90.0, 180.0),
        (x0 + r, y0 + r, 180.0, 270.0),
        (x1 - r, y0 + r, 270.0, 360.0),
    ]
    pts: list[tuple[float, float]] = []
    for cx, cy, deg0, deg1 in corners:
        for i in range(steps + 1):
            ang = math.radians(deg0 + (deg1 - deg0) * (i / steps))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# 1. Rounded square badge (Colors.Gray6)
badge_pts = _rounded_rect_pts(10.0, 14.5, 90.0, 85.5, r=6.5)
polygon(badge_pts, style=no_border_fill(Colors.Gray6))
draw_round_polyline(badge_pts, width_units=w, color=DARK, closed=True)

# 2. Geometric "A" polygon (WHITE) with triangular inner cutout
a_outer = [
    (22.6, 37.6),
    (29.0, 37.6),
    (31.0, 43.8),
    (41.4, 43.8),
    (43.5, 37.6),
    (49.9, 37.6),
    (39.0, 66.8),
    (33.4, 66.8),
]
a_hole = [
    (32.5, 48.5),
    (36.2, 59.8),
    (39.9, 48.5),
]
draw_compound_polygon([a_outer, a_hole], color=WHITE)
draw_round_polyline(a_outer, width_units=1.6, color=DARK, closed=True)
draw_round_polyline(a_hole, width_units=1.6, color=DARK, closed=True)

# 3. Geometric "G" polygon (WHITE)
g_pts = [
    (75.32, 52.85),
    (75.32, 41.30),
    (74.32, 40.33),
    (72.85, 39.29),
    (71.13, 38.44),
    (69.28, 37.81),
    (67.08, 37.38),
    (64.53, 37.22),
    (62.09, 37.34),
    (59.88, 37.82),
    (57.87, 38.66),
    (56.10, 39.84),
    (54.58, 41.34),
    (53.36, 43.16),
    (52.42, 45.28),
    (51.81, 47.72),
    (51.54, 50.44),
    (51.52, 53.09),
    (51.74, 56.27),
    (52.28, 58.74),
    (53.15, 60.93),
    (54.30, 62.80),
    (55.73, 64.35),
    (57.41, 65.57),
    (59.32, 66.46),
    (61.43, 67.00),
    (63.73, 67.18),
    (65.98, 67.06),
    (68.32, 66.60),
    (70.28, 65.79),
    (72.13, 64.48),
    (73.54, 62.81),
    (74.54, 60.83),
    (75.16, 58.60),
    (75.30, 57.57),
    (69.48, 57.57),
    (69.10, 59.12),
    (68.39, 60.55),
    (67.27, 61.63),
    (65.90, 62.26),
    (64.12, 62.50),
    (62.47, 62.34),
    (60.93, 61.72),
    (59.67, 60.65),
    (58.70, 59.13),
    (58.03, 57.17),
    (57.69, 55.04),
    (57.61, 53.13),
    (57.61, 50.98),
    (57.82, 48.38),
    (58.36, 46.19),
    (59.24, 44.43),
    (60.47, 43.14),
    (62.01, 42.30),
    (63.87, 41.92),
    (65.80, 41.96),
    (67.62, 42.37),
    (69.32, 43.40),
    (69.32, 48.57),
    (63.83, 48.57),
    (63.83, 52.85),
]
polygon(g_pts, style=no_border_fill(WHITE))
draw_round_polyline(g_pts, width_units=1.6, color=DARK, closed=True)

save()
