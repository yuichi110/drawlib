# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: freebsd."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

left_horn_pts: list[tuple[float, float]] = [
    (34.5, 75.71), (30.35, 82.33), (29.4, 82.86), (28.42, 83.4), (27.4, 83.92), (26.37, 84.44), (25.33, 84.95), (24.27, 85.43), (23.21, 85.89), (22.17, 86.31), (21.12, 86.7), (20.11, 87.05), (19.11, 87.34), (18.15, 87.58), (17.24, 87.77), (16.36, 87.89), (15.54, 87.95), (14.77, 87.93), (14.07, 87.83), (13.44, 87.64), (12.89, 87.36), (12.42, 86.98), (12.04, 86.51), (11.76, 85.95), (11.57, 85.31), (11.48, 84.59), (11.46, 83.81), (11.52, 82.98), (11.65, 82.08), (11.85, 81.14), (12.1, 80.16), (12.4, 79.16), (12.76, 78.12), (13.16, 77.07), (13.59, 76.01), (14.06, 74.94), (14.56, 73.88), (15.07, 72.81), (15.6, 71.77), (16.14, 70.75), (16.68, 69.75), (17.21, 68.8), (22.25, 63.02),
]

right_horn_pts: list[tuple[float, float]] = [
    (87.66, 86.65), (88.15, 85.94), (88.45, 85.04), (88.54, 83.98), (88.46, 82.78), (88.22, 81.45), (87.84, 80.04), (87.35, 78.55), (86.75, 77.01), (86.07, 75.44), (85.33, 73.86), (84.54, 72.31), (83.73, 70.78), (82.91, 69.32), (82.1, 67.94), (81.31, 66.68), (80.58, 65.53), (79.92, 64.54), (79.33, 63.72), (78.86, 63.1), (78.5, 62.7), (78.19, 62.44), (77.84, 62.23), (77.46, 62.08), (77.03, 61.98), (76.57, 61.93), (76.08, 61.94), (75.57, 61.98), (75.02, 62.08), (74.47, 62.22), (73.89, 62.42), (73.28, 62.65), (72.67, 62.93), (72.05, 63.25), (71.42, 63.62), (70.79, 64.02), (70.15, 64.47), (69.51, 64.96), (68.88, 65.47), (68.25, 66.04), (67.63, 66.63), (67.04, 67.25), (66.49, 67.88), (65.96, 68.51), (65.48, 69.15), (65.03, 69.78), (64.63, 70.42), (64.26, 71.05), (63.94, 71.67), (63.66, 72.28), (63.42, 72.88), (63.23, 73.45), (63.08, 74.02), (62.99, 74.56), (62.94, 75.07), (62.94, 75.57), (62.99, 76.02), (63.08, 76.45), (63.24, 76.84), (63.45, 77.18), (63.71, 77.5), (64.11, 77.85), (64.73, 78.32), (65.55, 78.91), (66.53, 79.57), (67.68, 80.31), (68.95, 81.1), (70.33, 81.9), (71.79, 82.72), (73.31, 83.54), (74.86, 84.33), (76.44, 85.06), (78.01, 85.75), (79.55, 86.34), (81.05, 86.84), (82.46, 87.21), (83.78, 87.45), (84.99, 87.53), (86.05, 87.44), (86.94, 87.15),
]
# fmt: on

# 1. Left horn tucked behind top-left of sphere
polygon(left_horn_pts, style=Icon.no_border_fill(Colors.Red2))
Icon.draw_round_polyline(left_horn_pts, width_units=w, color=Icon.DARK, closed=True)

# 2. Main flat Red3 sphere body
circle(
    (50.5, 48.0),
    radius=36.5,
    style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w),
)

# 3. Right horn seated on upper-right of sphere
polygon(right_horn_pts, style=Icon.no_border_fill(Colors.Red2))
Icon.draw_round_polyline(right_horn_pts, width_units=w, color=Icon.DARK, closed=True)

save()
