# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: webassembly."""

from drawlib.canvas import save
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 1.8
w_inner = 1.3
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


outer_notched = _sc([(9.0, 91.0), (9.0, 9.0), (91.0, 9.0), (91.0, 91.0), (59.38, 91.0), (59.38, 90.98), (59.38, 90.96), (59.39, 90.93), (59.39, 90.91), (59.39, 90.89), (59.39, 90.87), (59.39, 90.85), (59.39, 90.82), (59.4, 90.8), (59.4, 90.78), (59.4, 90.76), (59.4, 90.74), (59.4, 90.71), (59.4, 90.69), (59.4, 90.67), (59.4, 90.65), (59.4, 90.63), (59.4, 90.6), (59.4, 90.58), (59.4, 90.56), (59.37, 89.79), (59.28, 89.03), (59.13, 88.3), (58.93, 87.59), (58.67, 86.9), (58.35, 86.24), (58.0, 85.61), (57.59, 85.01), (57.14, 84.44), (56.65, 83.91), (56.12, 83.42), (55.55, 82.97), (54.95, 82.56), (54.32, 82.21), (53.66, 81.9), (52.97, 81.64), (52.26, 81.43), (51.53, 81.28), (50.77, 81.19), (50.0, 81.16), (49.23, 81.19), (48.47, 81.28), (47.74, 81.43), (47.03, 81.64), (46.34, 81.9), (45.68, 82.21), (45.05, 82.56), (44.45, 82.97), (43.88, 83.42), (43.35, 83.91), (42.86, 84.44), (42.41, 85.01), (42.01, 85.61), (41.65, 86.24), (41.34, 86.9), (41.08, 87.59), (40.87, 88.3), (40.72, 89.03), (40.63, 89.79), (40.6, 90.56), (40.6, 90.58), (40.6, 90.6), (40.6, 90.63), (40.6, 90.65), (40.6, 90.67), (40.6, 90.69), (40.6, 90.71), (40.6, 90.74), (40.6, 90.76), (40.61, 90.78), (40.61, 90.8), (40.61, 90.82), (40.61, 90.85), (40.61, 90.87), (40.61, 90.89), (40.61, 90.91), (40.61, 90.93), (40.62, 90.96), (40.62, 90.98), (40.62, 91.0)])
w_hole = _sc([(28.03, 46.81), (33.45, 46.81), (37.17, 27.05), (37.24, 27.05), (41.72, 46.81), (46.8, 46.81), (50.83, 26.8), (50.9, 26.8), (55.14, 46.81), (60.47, 46.81), (53.55, 17.78), (48.15, 17.78), (44.15, 37.54), (44.09, 37.54), (39.78, 17.78), (34.28, 17.78)])
a_outer_hole = _sc([(66.59, 46.81), (75.17, 46.81), (83.7, 17.78), (78.07, 17.78), (76.22, 24.24), (66.45, 24.24), (65.03, 17.78), (59.56, 17.78)])
a_inner_island = _sc([(69.86, 39.65), (67.49, 29.0), (74.87, 29.0), (72.14, 39.65)])
# fmt: on

# 1. Flat pastel purple notched square with transparent WA holes
draw_compound_polygon(
    [outer_notched, w_hole, a_outer_hole, a_inner_island],
    color="#8274F0",
)

# 2. Inner letter hole outlines and outer border
for hole in (w_hole, a_outer_hole, a_inner_island):
    draw_round_polyline(hole, width_units=w_inner, color=DARK, closed=True)
draw_round_polyline(outer_notched, width_units=w_outer, color=DARK, closed=True)

save()
