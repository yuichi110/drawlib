# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: lacework."""

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

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.9

upper_shield = [(85.82, 87.58), (85.81, 87.75), (85.78, 87.9), (85.74, 88.05), (85.69, 88.2), (85.63, 88.34), (85.55, 88.48), (85.47, 88.61), (85.37, 88.74), (85.26, 88.85), (85.15, 88.96), (85.02, 89.05), (84.89, 89.14), (84.75, 89.22), (84.61, 89.27), (84.45, 89.32), (84.3, 89.36), (15.61, 89.36), (15.46, 89.33), (15.31, 89.28), (15.15, 89.23), (15.02, 89.15), (14.88, 89.06), (14.75, 88.98), (14.63, 88.87), (14.53, 88.75), (14.43, 88.62), (14.35, 88.5), (14.27, 88.35), (14.21, 88.21), (14.15, 88.05), (14.12, 87.9), (14.1, 87.75), (14.09, 87.58), (14.09, 50.97), (14.1, 50.34), (14.11, 49.7), (14.13, 49.09), (14.16, 48.46), (14.2, 47.85), (14.26, 47.24), (14.32, 46.63), (14.39, 46.03), (14.47, 45.43), (14.57, 44.84), (14.67, 44.25), (14.78, 43.66), (14.91, 43.08), (15.05, 42.51), (15.19, 41.94), (15.35, 41.37), (15.53, 40.8), (15.71, 40.25), (15.91, 39.7), (16.11, 39.15), (85.91, 78.3), (85.91, 87.58)]
lower_shield = [(49.96, 10.64), (51.43, 10.76), (53.14, 11.12), (55.05, 11.71), (57.12, 12.53), (59.33, 13.56), (61.64, 14.81), (64.04, 16.27), (66.44, 17.92), (68.86, 19.76), (71.24, 21.8), (73.56, 24.0), (75.78, 26.39), (77.85, 28.95), (79.77, 31.66), (81.48, 34.53), (82.95, 37.55), (84.16, 40.71), (85.06, 44.0), (85.63, 47.43), (85.82, 50.98), (85.82, 63.37), (16.46, 37.72), (17.56, 35.34), (18.84, 33.05), (20.27, 30.84), (21.83, 28.72), (23.51, 26.69), (25.28, 24.76), (27.14, 22.94), (29.05, 21.23), (31.01, 19.63), (32.99, 18.14), (34.97, 16.77), (36.94, 15.53), (38.87, 14.42), (40.76, 13.44), (42.58, 12.61), (44.31, 11.91), (45.92, 11.36), (47.42, 10.97), (48.77, 10.72), (49.96, 10.64)]
white_ray = [(16.11, 39.15), (85.91, 78.3), (85.82, 63.37), (16.46, 37.72)]
# fmt: on

polygon(white_ray, style=no_border_fill(WHITE))
draw_round_polyline(white_ray, width_units=w, color=DARK, closed=True)

for pts in (upper_shield, lower_shield):
    polygon(pts, style=no_border_fill(Colors.Blue3))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
