# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: mongodb."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
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


setup_icon()

w = 2.0

p_top = (50.0, 90.5)
p_base_l = (46.8, 19.8)
p_base_c = (50.0, 18.8)
p_base_r = (53.2, 19.8)

# 1. Bottom tapered leaf stem (Colors.Amber3) capped along the leaf base
stem_pts = [
    p_base_l,
    (47.6, 9.5),
    (52.4, 9.5),
    p_base_r,
    p_base_c,
]
polygon(stem_pts, style=no_border_fill(Colors.Amber3))
draw_round_polyline(stem_pts, width_units=1.8, color=DARK, closed=True)

# 2. Central tapered vein cutout vertices
vein_bot = (50.0, 19.8)
vein_l = (46.6, 25.0)
vein_top = (50.0, 56.5)
vein_r = (53.4, 25.0)
vein_pts = [vein_bot, vein_l, vein_top, vein_r]

# 3. Left and right leaf blade halves routed around vein_pts
left_edge = [
    p_top,
    *_bezier(p_top, (35.5, 74.0), (28.0, 58.0), (28.8, 44.5), 20),
    *_bezier((28.8, 44.5), (29.5, 32.0), (37.5, 23.8), p_base_l, 18),
    p_base_c,
]
right_edge = [
    p_base_c,
    p_base_r,
    *_bezier(p_base_r, (62.5, 23.8), (70.5, 32.0), (71.2, 44.5), 18),
    *_bezier((71.2, 44.5), (72.0, 58.0), (64.5, 74.0), p_top, 20),
]

left_poly = [*left_edge, vein_bot, vein_l, vein_top]
right_poly = [*right_edge, vein_top, vein_r, vein_bot]

polygon(left_poly, style=no_border_fill(Colors.Green3))
polygon(right_poly, style=no_border_fill(Colors.Green2))

# 4. Upper center fold line above central vein
draw_round_segment((50.0, 56.0), p_top, width_units=1.6, color=DARK)

# 5. Outer leaf blade border and transparent central vein border
outer_leaf = [*left_edge[:-1], p_base_c, *right_edge[1:]]
draw_round_polyline(outer_leaf, width_units=w, color=DARK, closed=True)
draw_round_polyline(vein_pts, width_units=1.5, color=DARK, closed=True)

save()
