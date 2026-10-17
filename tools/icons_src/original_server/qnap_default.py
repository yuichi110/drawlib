# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: qnap (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.5
s = 0.95


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


q_outer = _sc(
    [(67.1, 80.36), (67.1, 80.41), (28.02, 80.41), (26.16, 80.37), (24.4, 80.26), (22.74, 80.06), (21.17, 79.8), (19.69, 79.45), (18.32, 79.03), (17.03, 78.53), (15.84, 77.95), (14.75, 77.3), (13.75, 76.57), (12.85, 75.76), (12.04, 74.88), (11.33, 73.92), (10.71, 72.89), (10.19, 71.77), (9.76, 70.58), (9.43, 69.32), (9.19, 67.97), (9.05, 66.56), (9.0, 65.06), (9.0, 36.88), (9.05, 35.39), (9.19, 33.98), (9.43, 32.65), (9.76, 31.39), (10.19, 30.2), (10.71, 29.1), (11.33, 28.07), (12.04, 27.12), (12.85, 26.24), (13.75, 25.44), (14.75, 24.71), (15.84, 24.07), (17.03, 23.5), (18.32, 23.0), (19.69, 22.58), (21.17, 22.24), (22.74, 21.97), (24.4, 21.78), (26.16, 21.67), (28.02, 21.63), (65.11, 21.63), (66.96, 21.67), (68.72, 21.79), (70.37, 21.98), (71.94, 22.25), (73.41, 22.59), (74.78, 23.01), (76.06, 23.51), (77.25, 24.08), (78.34, 24.73), (79.34, 25.45), (80.24, 26.25), (81.04, 27.12), (81.76, 28.08), (82.37, 29.1), (82.89, 30.21), (83.32, 31.39), (83.65, 32.64), (83.89, 33.97), (84.04, 35.38), (84.08, 36.87), (84.08, 65.06), (84.04, 66.48), (83.91, 67.83), (83.7, 69.11), (83.4, 70.32), (83.02, 71.46), (82.56, 72.53), (82.0, 73.54), (81.37, 74.47), (80.65, 75.34), (79.84, 76.14), (78.95, 76.87), (77.97, 77.53), (76.91, 78.12), (75.76, 78.65), (74.53, 79.11), (73.22, 79.49), (71.82, 79.81), (70.33, 80.06), (68.76, 80.25)]
)

q_hole = _sc([(63.06, 35.93), (32.28, 35.93), (32.28, 66.43), (63.06, 66.43)])

q_tail = _sc(
    [(44.46, 43.78), (44.63, 43.68), (45.12, 43.39), (45.9, 42.93), (46.93, 42.3), (48.19, 41.52), (49.64, 40.59), (51.26, 39.54), (53.0, 38.37), (54.84, 37.1), (56.75, 35.74), (58.7, 34.29), (60.65, 32.78), (62.58, 31.21), (64.45, 29.6), (66.23, 27.96), (67.89, 26.3), (69.4, 24.63), (70.72, 22.97), (71.83, 21.32), (72.69, 19.71), (90.88, 19.71), (90.6, 20.33), (90.2, 21.13), (89.66, 22.07), (88.96, 23.15), (88.1, 24.34), (87.05, 25.62), (85.8, 26.99), (84.34, 28.41), (82.65, 29.88), (80.71, 31.37), (78.51, 32.87), (76.03, 34.36), (73.27, 35.82), (70.2, 37.24), (66.8, 38.59), (63.07, 39.86), (58.99, 41.03), (54.53, 42.09), (49.7, 43.01)]
)
# fmt: on

# 1. Rounded Q block with transparent center square hole
draw_compound_polygon([q_outer, q_hole], color="#5C78B0")
draw_round_polyline(q_outer, width_units=w, color=DARK, closed=True)
draw_round_polyline(q_hole, width_units=w, color=DARK, closed=True)

# 2. Sweeping Q tail in pastel red on top
polygon(q_tail, style=no_border_fill("#E56B6F"))
draw_round_polyline(q_tail, width_units=w, color=DARK, closed=True)

save()
