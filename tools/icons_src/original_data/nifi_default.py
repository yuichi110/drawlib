# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: nifi."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 20,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


def _arc_points(cx: float, cy: float, r: float, deg1: float, deg2: float, steps: int = 12) -> list[tuple[float, float]]:
    """Sample circular arc from deg1 to deg2."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(deg1 + (deg2 - deg1) * (i / steps))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


setup_icon()

w = 2.0

cx, cy = 49.0, 39.5
r_drop = 28.5
p_top = (49.0, 90.0)
p_left = (cx - r_drop, cy)  # (20.5, 39.5)
p_right = (cx + r_drop, cy)  # (77.5, 39.5)

# 1. Main water droplet with bottom-right stepped cutout (Colors.Gray3)
drop_pts: list[tuple[float, float]] = [
    p_top,
    *_bezier(p_top, (36.5, 68.5), (20.5, 53.5), p_left, 22),
    *_arc_points(cx, cy, r_drop, 180.0, 269.0, 20)[1:],
    (48.5, 27.5),
    (60.5, 27.5),
    (60.5, 39.5),
    p_right,
    *_bezier(p_right, (77.5, 53.5), (61.5, 68.5), p_top, 22),
]

polygon(drop_pts, style=no_border_fill(Colors.Gray3))
draw_round_polyline(drop_pts, width_units=w, color=DARK, closed=True)

# 2. Inner flow highlight arc on left side of droplet (WHITE)
p_hl_top_l = (38.8, 66.0)
p_hl_top_r = (42.2, 63.5)
p_hl_bot = (35.8, 21.5)
hl_pts = [
    p_hl_top_l,
    *_bezier(p_hl_top_l, (27.2, 50.0), (25.2, 32.5), p_hl_bot, 20),
    *_bezier(p_hl_bot, (29.5, 32.5), (31.5, 49.5), p_hl_top_r, 20),
]
polygon(hl_pts, style=no_border_fill(WHITE))
draw_round_polyline(hl_pts, width_units=1.5, color=DARK, closed=True)

# 3. Three substantial stepped flow tiles in bottom-right quadrant
# Tile 1: bottom-left vertical arc tile (x=52.8..61.2, top y=23.2, bottom on droplet arc)
x1_l, x1_r, y1_t = 52.8, 61.2, 23.2
y1_bl = cy - math.sqrt(max(0.0, r_drop**2 - (x1_l - cx) ** 2))
y1_br = cy - math.sqrt(max(0.0, r_drop**2 - (x1_r - cx) ** 2))
a1_l = math.degrees(math.atan2(y1_bl - cy, x1_l - cx))
a1_r = math.degrees(math.atan2(y1_br - cy, x1_r - cx))
tile1_pts = [(x1_r, y1_t), (x1_l, y1_t), *_arc_points(cx, cy, r_drop, a1_l, a1_r, 10)]
polygon(tile1_pts, style=no_border_fill(Colors.Teal3))
draw_round_polyline(tile1_pts, width_units=1.7, color=DARK, closed=True)

# Tile 2: top-right horizontal arc tile (x_left=64.8, y=27.2..35.2, right on droplet arc)
x2_l, y2_b, y2_t = 64.8, 27.2, 35.2
x2_br = cx + math.sqrt(max(0.0, r_drop**2 - (y2_b - cy) ** 2))
x2_tr = cx + math.sqrt(max(0.0, r_drop**2 - (y2_t - cy) ** 2))
a2_b = math.degrees(math.atan2(y2_b - cy, x2_br - cx))
a2_t = math.degrees(math.atan2(y2_t - cy, x2_tr - cx))
tile2_pts = [(x2_l, y2_t), (x2_l, y2_b), *_arc_points(cx, cy, r_drop, a2_b, a2_t, 10)]
polygon(tile2_pts, style=no_border_fill(Colors.Teal3))
draw_round_polyline(tile2_pts, width_units=1.7, color=DARK, closed=True)

# Tile 3: bottom-right corner arc tile (top-left=(64.8, 23.2), outer edge on droplet arc)
x3_l, y3_t = 64.8, 23.2
y3_bl = cy - math.sqrt(max(0.0, r_drop**2 - (x3_l - cx) ** 2))
x3_tr = cx + math.sqrt(max(0.0, r_drop**2 - (y3_t - cy) ** 2))
a3_b = math.degrees(math.atan2(y3_bl - cy, x3_l - cx))
a3_t = math.degrees(math.atan2(y3_t - cy, x3_tr - cx))
tile3_pts = [(x3_l, y3_t), *_arc_points(cx, cy, r_drop, a3_b, a3_t, 12)]
polygon(tile3_pts, style=no_border_fill(Colors.Teal4))
draw_round_polyline(tile3_pts, width_units=1.7, color=DARK, closed=True)

save()
