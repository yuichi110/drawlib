# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: nixos."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0

lambdas_blue2: list[list[tuple[float, float]]] = [
    [(41.65, 63.58), (22.69, 28.41), (18.26, 36.44), (23.37, 45.88), (13.21, 45.91), (11.05, 49.92), (13.27, 54.03), (27.74, 53.99), (32.95, 63.58)],
    [(43.12, 35.47), (81.06, 35.47), (76.78, 27.34), (66.6, 27.37), (71.65, 17.95), (69.49, 13.91), (65.07, 13.91), (57.87, 27.33), (47.5, 27.34)],
    [(65.22, 50.88), (46.24, 86.06), (54.96, 86.15), (60.02, 76.7), (65.12, 86.11), (69.46, 86.11), (71.67, 82.0), (64.39, 68.62), (69.55, 59.01)],
]

lambdas_blue3: list[list[tuple[float, float]]] = [
    [(34.82, 49.11), (53.79, 13.93), (45.07, 13.83), (40.01, 23.3), (34.9, 13.89), (30.57, 13.89), (28.35, 18.0), (35.63, 31.36), (30.47, 40.98)],
    [(56.86, 64.61), (18.9, 64.61), (23.19, 72.73), (33.37, 72.71), (28.32, 82.13), (30.48, 86.17), (34.9, 86.17), (42.11, 72.74), (52.46, 72.73)],
    [(58.35, 36.4), (77.32, 71.57), (81.75, 63.54), (76.63, 54.12), (86.79, 54.09), (88.95, 50.06), (86.73, 45.95), (72.26, 46.0), (67.05, 36.42)],
]
# fmt: on

for pts in lambdas_blue2:
    polygon(pts, style=no_border_fill(Colors.Blue2))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

for pts in lambdas_blue3:
    polygon(pts, style=no_border_fill(Colors.Blue3))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
