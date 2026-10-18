# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: qradar."""

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

w = 2.0

left_shield: list[tuple[float, float]] = [(50.03, 11.02), (50.04, 15.9), (48.06, 15.97), (46.27, 16.19), (43.89, 16.66), (42.07, 17.22), (40.27, 17.9), (38.4, 18.8), (36.89, 19.72), (35.12, 20.97), (33.59, 22.23), (32.05, 23.8), (30.89, 25.15), (29.62, 26.91), (28.67, 28.5), (27.72, 30.4), (27.01, 32.27), (26.4, 34.31), (26.0, 36.31), (25.75, 38.64), (25.69, 39.9), (25.69, 71.42), (50.04, 83.53), (50.04, 88.96), (20.81, 74.41), (20.81, 39.83), (20.88, 37.72), (21.21, 35.31), (21.81, 32.6), (22.36, 30.69), (23.26, 28.44), (24.37, 26.2), (25.53, 24.27), (26.95, 22.3), (28.46, 20.5), (30.48, 18.51), (32.12, 17.14), (34.14, 15.69), (36.07, 14.55), (37.69, 13.76), (40.64, 12.54), (42.86, 11.91), (45.21, 11.41), (47.63, 11.12)]
right_shield: list[tuple[float, float]] = [(49.97, 11.02), (52.55, 11.12), (55.32, 11.52), (57.53, 11.99), (59.97, 12.78), (61.29, 13.31), (62.26, 13.73), (64.64, 14.95), (66.41, 16.09), (68.71, 17.8), (70.47, 19.41), (72.38, 21.51), (73.94, 23.49), (75.29, 25.65), (76.66, 28.29), (77.47, 30.34), (78.24, 32.85), (78.64, 34.6), (79.06, 37.58), (79.17, 39.48), (79.17, 74.41), (49.99, 88.96), (49.99, 83.5), (74.28, 71.42), (74.27, 62.3), (49.97, 74.41), (49.99, 68.95), (74.28, 56.88), (74.28, 47.77), (49.99, 59.87), (49.97, 54.47), (74.27, 42.34), (74.28, 39.66), (74.07, 36.84), (73.76, 35.15), (73.37, 33.69), (49.97, 45.34), (49.99, 39.92), (71.62, 29.16), (70.22, 26.75), (69.25, 25.44), (67.63, 23.56), (66.57, 22.55), (49.99, 30.81), (49.99, 25.38), (62.22, 19.29), (60.68, 18.43), (59.04, 17.69), (57.12, 17.01), (55.42, 16.5), (53.6, 16.19), (51.79, 15.97), (49.93, 15.9)]
# fmt: on

# 1. Left shield frame in pastel purple
polygon(left_shield, style=no_border_fill(Colors.Purple3))
draw_round_polyline(left_shield, width_units=w, color=DARK, closed=True)

# 2. Right shield frame and diagonal slats in pastel blue
polygon(right_shield, style=no_border_fill(Colors.Blue3))
draw_round_polyline(right_shield, width_units=w, color=DARK, closed=True)

save()
