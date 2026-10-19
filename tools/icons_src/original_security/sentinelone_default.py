# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: sentinelone."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


bars: list[list[tuple[float, float]]] = [
    _sc([(44.49, 91.0), (55.53, 91.0), (55.53, 24.96), (44.49, 24.96)]),
    _sc([(58.21, 9.03), (69.24, 15.87), (69.24, 73.05), (67.57, 74.19), (65.82, 75.22), (63.99, 76.11), (62.11, 76.86), (60.18, 77.47), (58.21, 77.94)]),
    _sc([(30.74, 15.84), (41.78, 9.0), (41.78, 77.9), (39.81, 77.44), (37.88, 76.83), (35.99, 76.09), (34.17, 75.2), (32.42, 74.19), (30.74, 73.05)]),
    _sc([(71.92, 87.86), (71.92, 17.07), (77.05, 20.25), (77.94, 20.89), (78.77, 21.6), (79.54, 22.38), (80.24, 23.22), (80.86, 24.11), (81.42, 25.05), (81.89, 26.04), (82.27, 27.06), (82.58, 28.12), (82.78, 29.18), (82.9, 30.27), (82.94, 31.36), (82.94, 64.8), (82.86, 66.27), (82.64, 67.79), (82.28, 69.34), (81.8, 70.9), (81.23, 72.47), (80.57, 74.03), (79.84, 75.58), (79.07, 77.08), (78.26, 78.54), (77.44, 79.95), (76.61, 81.28), (75.81, 82.52), (75.03, 83.67), (74.3, 84.7), (73.65, 85.61), (73.06, 86.39), (72.59, 87.02), (72.23, 87.48), (72.0, 87.76)]),
    _sc([(17.06, 31.39), (17.09, 30.3), (17.21, 29.21), (17.42, 28.14), (17.72, 27.09), (18.1, 26.06), (18.58, 25.08), (19.13, 24.13), (19.76, 23.24), (20.46, 22.4), (21.23, 21.63), (22.06, 20.92), (22.95, 20.28), (28.08, 17.1), (28.08, 87.86), (28.0, 87.76), (27.77, 87.48), (27.41, 87.02), (26.94, 86.39), (26.36, 85.61), (25.7, 84.7), (24.98, 83.67), (24.2, 82.52), (23.4, 81.28), (22.58, 79.95), (21.75, 78.54), (20.94, 77.08), (20.16, 75.58), (19.44, 74.03), (18.78, 72.47), (18.21, 70.9), (17.73, 69.34), (17.37, 67.79), (17.14, 66.27), (17.06, 64.8)]),
]
# fmt: on

for bar_pts in bars:
    polygon(bar_pts, style=Icon.no_border_fill(Colors.Purple3))
    Icon.draw_round_polyline(bar_pts, width_units=w, color=Icon.DARK, closed=True)

save()
