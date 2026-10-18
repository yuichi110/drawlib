# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client vendor icon: bluetooth (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

PASTEL_BLUE = "#7BAEF7"
w = 2.0

oval_pts: list[tuple[float, float]] = [(50.0, 9.0), (52.64, 9.07), (55.19, 9.27), (57.65, 9.63), (60.01, 10.14), (62.27, 10.84), (64.41, 11.71), (66.45, 12.79), (68.37, 14.07), (70.16, 15.58), (71.82, 17.32), (73.35, 19.3), (74.74, 21.53), (75.99, 24.03), (77.09, 26.81), (78.03, 29.89), (78.81, 33.26), (79.43, 36.95), (79.88, 40.96), (80.15, 45.3), (80.24, 50.0), (80.15, 54.7), (79.88, 59.04), (79.43, 63.05), (78.81, 66.74), (78.03, 70.11), (77.09, 73.19), (76.0, 75.97), (74.75, 78.47), (73.36, 80.7), (71.84, 82.68), (70.17, 84.42), (68.38, 85.93), (66.46, 87.21), (64.43, 88.29), (62.28, 89.16), (60.02, 89.86), (57.66, 90.37), (55.2, 90.73), (52.64, 90.93), (50.0, 91.0), (47.36, 90.93), (44.8, 90.73), (42.34, 90.37), (39.98, 89.86), (37.72, 89.16), (35.57, 88.29), (33.54, 87.21), (31.62, 85.93), (29.83, 84.42), (28.16, 82.68), (26.64, 80.7), (25.25, 78.47), (24.0, 75.97), (22.91, 73.19), (21.97, 70.11), (21.19, 66.74), (20.57, 63.05), (20.12, 59.04), (19.85, 54.7), (19.76, 50.0), (19.85, 45.3), (20.12, 40.96), (20.57, 36.95), (21.19, 33.26), (21.97, 29.89), (22.91, 26.81), (24.01, 24.03), (25.26, 21.53), (26.65, 19.3), (28.18, 17.32), (29.84, 15.58), (31.63, 14.07), (33.55, 12.79), (35.59, 11.71), (37.73, 10.84), (39.99, 10.14), (42.35, 9.63), (44.81, 9.27), (47.36, 9.07)]
rune_rings: list[list[tuple[float, float]]] = [[(46.08, 50.0), (31.41, 64.69), (35.66, 68.98), (47.35, 57.26), (47.35, 85.25), (68.59, 64.02), (54.56, 50.0), (68.59, 35.98), (47.35, 14.75), (47.35, 42.74), (35.7, 31.05), (31.46, 35.34)], [(53.32, 29.27), (60.09, 36.05), (53.32, 42.82)], [(53.32, 70.78), (60.09, 63.99), (53.32, 57.22)]]

polygon(oval_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(oval_pts, width_units=w, color=DARK, closed=True)

draw_compound_polygon(rune_rings, color=WHITE)
for ring in rune_rings:
    draw_round_polyline(ring, width_units=w, color=DARK, closed=True)

save()
# fmt: on
