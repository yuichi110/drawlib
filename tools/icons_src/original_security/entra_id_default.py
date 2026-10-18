# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: entra_id."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 2.0
w_inner = 1.7
s = 40.0 / 42.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


outer_pyramid = _sc([
    (90.35, 45.49), (55.35, 84.97), (54.2, 86.01), (52.89, 86.75), (51.48, 87.19),
    (50.0, 87.34), (48.53, 87.19), (47.11, 86.75), (45.8, 86.01), (44.65, 84.97),
    (9.65, 45.49), (8.79, 44.28), (8.25, 42.97), (8.01, 41.61), (8.07, 40.24),
    (8.43, 38.91), (9.06, 37.67), (9.97, 36.56), (11.15, 35.64), (46.15, 13.76),
    (47.05, 13.28), (48.01, 12.94), (48.99, 12.73), (50.0, 12.66), (51.0, 12.73),
    (51.98, 12.94), (52.94, 13.28), (53.84, 13.76), (88.84, 35.64), (90.02, 36.56),
    (90.93, 37.67), (91.57, 38.91), (91.92, 40.24), (91.98, 41.61), (91.74, 42.97),
    (91.2, 44.28), (90.34, 45.49),
])

base_left = _sc([
    (50.0, 87.34), (48.53, 87.19), (47.11, 86.75), (45.8, 86.01), (44.65, 84.97),
    (9.65, 45.49), (8.79, 44.28), (8.25, 42.97), (8.01, 41.61), (8.07, 40.24),
    (8.43, 38.91), (9.06, 37.67), (9.97, 36.56), (11.15, 35.64), (46.15, 13.76),
    (47.05, 13.28), (48.01, 12.94), (48.99, 12.73), (50.0, 12.66),
])

base_right = _sc([
    (50.0, 12.66), (51.0, 12.73), (51.98, 12.94), (52.94, 13.28), (53.84, 13.76),
    (88.84, 35.64), (90.02, 36.56), (90.93, 37.67), (91.57, 38.91), (91.92, 40.24),
    (91.98, 41.61), (91.74, 42.97), (91.2, 44.28), (90.35, 45.49), (55.35, 84.97),
    (54.2, 86.01), (52.89, 86.75), (51.48, 87.19), (50.0, 87.34),
])

ribbon_left = _sc([
    (50.0, 87.34), (48.53, 87.19), (47.11, 86.75), (45.8, 86.01), (44.65, 84.97),
    (9.65, 45.49), (8.8, 44.28), (8.25, 42.97), (8.02, 41.61), (8.08, 40.24),
    (8.43, 38.91), (9.07, 37.67), (9.98, 36.56), (11.16, 35.64), (11.72, 35.29),
    (13.21, 34.35), (15.34, 33.02), (17.84, 31.46), (20.41, 29.85), (22.78, 28.37),
    (24.65, 27.2), (25.75, 26.52), (26.48, 26.09), (27.31, 25.67), (28.24, 25.27),
    (29.23, 24.9), (30.3, 24.59), (31.41, 24.35), (32.57, 24.19), (33.75, 24.13),
    (34.83, 24.17), (35.88, 24.29), (36.91, 24.47), (37.91, 24.73), (38.88, 25.06),
    (39.81, 25.45), (40.71, 25.9), (41.58, 26.41), (50.0, 31.67), (29.63, 44.4),
    (50.0, 67.39),
])

ribbon_right = _sc([
    (50.0, 87.34), (50.0, 67.39), (50.51, 67.96), (51.53, 69.0), (52.67, 69.94),
    (53.9, 70.76), (55.23, 71.45), (56.64, 72.0), (58.12, 72.41), (59.66, 72.66),
    (61.26, 72.75), (62.08, 72.72), (62.88, 72.65), (63.68, 72.54), (64.45, 72.39),
    (65.21, 72.19), (65.96, 71.96), (66.68, 71.69), (67.39, 71.38), (55.35, 84.97),
    (54.2, 86.01), (52.89, 86.75), (51.48, 87.19),
])

diamond_left = _sc([(50.0, 67.39), (29.63, 44.4), (50.0, 31.67)])
diamond_right = _sc([(50.0, 67.39), (70.37, 44.4), (50.0, 31.67)])

curve_bl = _sc([
    (25.75, 26.52), (26.48, 26.09), (27.31, 25.67), (28.24, 25.27),
    (29.23, 24.9), (30.3, 24.59), (31.41, 24.35), (32.57, 24.19),
    (33.75, 24.13), (34.83, 24.17), (35.88, 24.29), (36.91, 24.47),
    (37.91, 24.73), (38.88, 25.06), (39.81, 25.45), (40.71, 25.9),
    (41.58, 26.41), (50.0, 31.67),
])

curve_tr = _sc([
    (50.0, 67.39), (50.51, 67.96), (51.53, 69.0), (52.67, 69.94),
    (53.9, 70.76), (55.23, 71.45), (56.64, 72.0), (58.12, 72.41),
    (59.66, 72.66), (61.26, 72.75), (62.08, 72.72), (62.88, 72.65),
    (63.68, 72.54), (64.45, 72.39), (65.21, 72.19), (65.96, 71.96),
    (66.68, 71.69), (67.39, 71.38),
])

inner_diamond = _sc([(50.0, 67.39), (29.63, 44.4), (50.0, 31.67), (70.37, 44.4)])
center_axis = _sc([(50.0, 12.66), (50.0, 87.34)])
# fmt: on

# 1. Flat pastel multi-facet fills (cyan / blue / indigo)
polygon(base_left, style=no_border_fill(Colors.Blue3))
polygon(base_right, style=no_border_fill(Colors.Blue4))
polygon(ribbon_left, style=no_border_fill(Colors.Teal2))
polygon(ribbon_right, style=no_border_fill(Colors.Blue2))
polygon(diamond_left, style=no_border_fill(Colors.Blue2))
polygon(diamond_right, style=no_border_fill(Colors.Blue3))

# 2. Internal facet DARK outlines
draw_round_polyline(curve_bl, width_units=w_inner, color=DARK)
draw_round_polyline(curve_tr, width_units=w_inner, color=DARK)
draw_round_polyline(inner_diamond, width_units=w_inner, color=DARK, closed=True)
draw_round_polyline(center_axis, width_units=w_inner, color=DARK)

# 3. Outer pyramid DARK outline
draw_round_polyline(outer_pyramid, width_units=w_outer, color=DARK, closed=True)

save()
