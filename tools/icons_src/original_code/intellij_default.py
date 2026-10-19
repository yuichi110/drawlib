# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: intellij."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w_outer = 2.0
w_inner = 1.2
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


shard_orange = _sc([(9.92, 42.69), (17.02, 55.83), (27.69, 52.26), (21.99, 33.17)])
shard_blue_bot = _sc([(91.0, 69.14), (89.52, 21.65), (57.94, 9.0), (40.73, 20.1)])
shard_blue_top = _sc([(55.3, 78.52), (65.2, 89.66), (91.0, 69.14), (75.37, 53.9)])
shard_pink = _sc([(20.88, 91.0), (47.71, 87.83), (75.37, 53.9), (40.73, 20.1), (15.61, 11.03), (27.69, 52.26), (9.0, 58.51)])

inner_square = _sc([(24.75, 75.62), (75.99, 75.62), (75.99, 24.38), (24.75, 24.38)])
ij_bar = _sc([(31.13, 34.06), (50.35, 34.06), (50.35, 30.86), (31.13, 30.86)])
ij_i = _sc([(40.73, 65.7), (40.73, 69.2), (31.17, 69.2), (31.17, 65.7), (33.85, 65.7), (33.85, 53.61), (31.17, 53.61), (31.17, 50.1), (40.73, 50.1), (40.73, 53.61), (38.05, 53.61), (38.05, 65.7)])
ij_j = _sc([(49.89, 49.83), (49.33, 49.83), (48.78, 49.88), (48.23, 49.96), (47.69, 50.08), (47.16, 50.25), (46.64, 50.45), (46.14, 50.68), (45.67, 50.95), (45.23, 51.25), (44.8, 51.58), (44.39, 51.93), (44.01, 52.3), (43.65, 52.7), (46.29, 55.65), (46.36, 55.57), (46.43, 55.49), (46.51, 55.41), (46.58, 55.33), (46.66, 55.25), (46.74, 55.18), (46.82, 55.1), (46.9, 55.03), (46.98, 54.96), (47.06, 54.89), (47.15, 54.82), (47.23, 54.75), (47.32, 54.68), (47.4, 54.62), (47.49, 54.55), (47.58, 54.49), (47.67, 54.42), (47.76, 54.36), (47.85, 54.3), (47.94, 54.25), (48.18, 54.11), (48.43, 53.99), (48.69, 53.9), (48.96, 53.82), (49.23, 53.77), (49.5, 53.74), (49.78, 53.73), (49.97, 53.73), (50.16, 53.74), (50.34, 53.77), (50.53, 53.81), (50.71, 53.87), (50.88, 53.94), (51.05, 54.02), (51.21, 54.12), (51.37, 54.22), (51.51, 54.34), (51.65, 54.48), (51.81, 54.71), (51.95, 54.96), (52.07, 55.22), (52.17, 55.48), (52.25, 55.76), (52.3, 56.04), (52.34, 56.32), (52.35, 56.61), (52.33, 56.89), (52.33, 69.22), (56.6, 69.22), (56.6, 56.71), (56.6, 56.2), (56.56, 55.7), (56.5, 55.19), (56.41, 54.7), (56.28, 54.21), (56.13, 53.73), (55.96, 53.3), (55.76, 52.89), (55.52, 52.5), (55.25, 52.13), (54.95, 51.78), (54.62, 51.46), (54.27, 51.16), (53.9, 50.9), (53.5, 50.67), (53.09, 50.47), (52.66, 50.31), (52.2, 50.17), (51.73, 50.05), (51.26, 49.96), (50.79, 49.9), (50.31, 49.87), (49.83, 49.86)])
# fmt: on

# 1. Flat pastel orange, blue, and pink outer shards
polygon(shard_orange, style=Icon.no_border_fill("#F1AC47"))
Icon.draw_round_polyline(shard_orange, width_units=w_outer, color=Icon.DARK, closed=True)

polygon(shard_blue_bot, style=Icon.no_border_fill("#4DA8F2"))
Icon.draw_round_polyline(shard_blue_bot, width_units=w_outer, color=Icon.DARK, closed=True)

polygon(shard_blue_top, style=Icon.no_border_fill("#4DA8F2"))
Icon.draw_round_polyline(shard_blue_top, width_units=w_outer, color=Icon.DARK, closed=True)

polygon(shard_pink, style=Icon.no_border_fill("#F14982"))
Icon.draw_round_polyline(shard_pink, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Flat dark slate inner square
polygon(inner_square, style=Icon.no_border_fill("#3E4756"))
Icon.draw_round_polyline(inner_square, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. WHITE 'IJ' and '_' shapes
for glyph in (ij_bar, ij_i, ij_j):
    polygon(glyph, style=Icon.no_border_fill(Icon.WHITE))
    Icon.draw_round_polyline(glyph, width_units=w_inner, color=Icon.DARK, closed=True)

save()
