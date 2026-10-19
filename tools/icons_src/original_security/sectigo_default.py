# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: sectigo."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
Icon.setup()

w_badge = 2.0
w_leaf = 1.5
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# fmt: off
badge_outer = _sc([
    (73.74, 91.0), (78.21, 90.41), (82.37, 88.69), (85.94, 85.94),
    (88.69, 82.37), (90.41, 78.21), (91.0, 73.74), (91.0, 26.26),
    (90.41, 21.79), (88.69, 17.63), (85.94, 14.06), (82.37, 11.31),
    (78.21, 9.59), (73.74, 9.0), (26.26, 9.0), (21.79, 9.59),
    (17.63, 11.31), (14.06, 14.06), (11.31, 17.63), (9.59, 21.79),
    (9.0, 26.26), (9.0, 73.74), (9.59, 78.21), (11.31, 82.37),
    (14.06, 85.94), (17.63, 88.69), (21.79, 90.41), (26.26, 91.0),
])

leaf_right = _sc([
    (75.65, 37.41), (62.59, 37.41), (62.54, 38.44), (62.42, 39.45),
    (62.22, 40.43), (61.94, 41.39), (61.6, 42.31), (61.18, 43.19),
    (60.7, 44.04), (60.15, 44.84), (59.55, 45.6), (58.89, 46.31),
    (58.19, 46.97), (57.43, 47.57), (56.62, 48.11), (55.78, 48.59),
    (54.89, 49.01), (53.97, 49.36), (53.02, 49.63), (52.04, 49.83),
    (51.03, 49.96), (50.0, 50.0), (50.0, 63.07), (52.1, 62.98),
    (54.16, 62.73), (56.16, 62.32), (58.1, 61.76), (59.98, 61.05),
    (61.78, 60.2), (63.5, 59.22), (65.14, 58.11), (66.68, 56.88),
    (68.13, 55.54), (69.47, 54.1), (70.7, 52.55), (71.8, 50.92),
    (72.78, 49.19), (73.63, 47.39), (74.34, 45.51), (74.9, 43.57),
    (75.31, 41.57), (75.57, 39.51),
])

leaf_left = _sc([
    (24.35, 62.59), (37.41, 62.59), (37.46, 61.56), (37.58, 60.55),
    (37.78, 59.57), (38.06, 58.61), (38.4, 57.69), (38.82, 56.81),
    (39.3, 55.96), (39.85, 55.16), (40.45, 54.4), (41.11, 53.69),
    (41.81, 53.03), (42.57, 52.43), (43.38, 51.89), (44.22, 51.41),
    (45.11, 50.99), (46.03, 50.64), (46.98, 50.37), (47.96, 50.17),
    (48.97, 50.04), (50.0, 50.0), (50.0, 36.93), (47.9, 37.02),
    (45.84, 37.27), (43.84, 37.68), (41.9, 38.24), (40.02, 38.95),
    (38.22, 39.8), (36.5, 40.78), (34.86, 41.89), (33.32, 43.12),
    (31.87, 44.46), (30.53, 45.9), (29.3, 47.45), (28.2, 49.08),
    (27.22, 50.81), (26.37, 52.61), (25.66, 54.49), (25.1, 56.43),
    (24.69, 58.43), (24.43, 60.49),
])
# fmt: on

# 1. Dark teal rounded square badge (Colors.Teal6 + DARK w=1.9 border)
polygon(badge_outer, style=Icon.no_border_fill(Colors.Teal6))
Icon.draw_round_polyline(badge_outer, width_units=w_badge, color=Icon.DARK, closed=True)

# 2. Two pastel green/mint curved leaves (Colors.Teal3, Colors.Green3 + DARK 1.5 outlines)
polygon(leaf_left, style=Icon.no_border_fill(Colors.Teal3))
Icon.draw_round_polyline(leaf_left, width_units=w_leaf, color=Icon.DARK, closed=True)

polygon(leaf_right, style=Icon.no_border_fill(Colors.Green3))
Icon.draw_round_polyline(leaf_right, width_units=w_leaf, color=Icon.DARK, closed=True)

save()
