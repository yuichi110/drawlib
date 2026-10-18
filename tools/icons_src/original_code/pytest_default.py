# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: pytest."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_border = 2.0

divider = [(18.16, 83.69), (81.84, 83.69), (82.12, 83.68), (82.39, 83.64), (82.64, 83.58), (82.91, 83.49), (83.16, 83.4), (83.4, 83.27), (83.63, 83.12), (83.85, 82.96), (84.05, 82.77), (84.23, 82.58), (84.4, 82.35), (84.55, 82.13), (84.67, 81.88), (84.77, 81.63), (84.86, 81.37), (84.92, 81.11), (84.96, 80.84), (84.97, 80.57), (84.96, 80.28), (84.92, 80.02), (84.86, 79.76), (84.77, 79.49), (84.67, 79.25), (84.55, 79.0), (84.4, 78.77), (84.23, 78.56), (84.05, 78.35), (83.85, 78.17), (83.63, 78.0), (83.4, 77.85), (83.16, 77.73), (82.91, 77.63), (82.64, 77.54), (82.39, 77.49), (82.12, 77.45), (81.84, 77.44), (18.16, 77.44), (17.88, 77.45), (17.61, 77.49), (17.35, 77.54), (17.08, 77.63), (16.84, 77.73), (16.6, 77.85), (16.37, 78.0), (16.15, 78.17), (15.95, 78.35), (15.77, 78.56), (15.6, 78.77), (15.45, 79.0), (15.33, 79.24), (15.23, 79.49), (15.14, 79.76), (15.08, 80.02), (15.04, 80.28), (15.03, 80.56), (15.04, 80.84), (15.08, 81.11), (15.14, 81.37), (15.23, 81.63), (15.33, 81.87), (15.45, 82.13), (15.6, 82.35), (15.77, 82.58), (15.95, 82.77), (16.15, 82.96), (16.37, 83.12), (16.6, 83.27), (16.84, 83.4), (17.08, 83.49), (17.35, 83.58), (17.61, 83.64), (17.88, 83.68)]
cap_cyan = [(18.71, 90.0), (31.51, 90.0), (31.51, 87.05), (18.71, 87.05)]
cap_lime = [(35.46, 90.0), (48.26, 90.0), (48.26, 87.05), (35.46, 87.05)]
cap_orange = [(51.98, 90.0), (64.79, 90.0), (64.79, 87.05), (51.98, 87.05)]
cap_red = [(68.43, 90.0), (81.23, 90.0), (81.23, 87.05), (68.43, 87.05)]
bar_cyan = [(18.71, 74.19), (31.51, 74.19), (31.51, 10.0), (18.71, 10.0)]
bar_lime = [(35.46, 74.19), (48.26, 74.19), (48.26, 21.52), (35.46, 21.52)]
bar_orange = [(51.98, 74.19), (64.81, 74.19), (64.81, 39.02), (51.98, 39.02)]
bar_red = [(68.43, 74.19), (81.23, 74.19), (81.23, 52.54), (68.43, 52.54)]
# fmt: on

# 1. Pastel 4-color top caps, bottom bars, and slate-gray divider
shapes = (
    (divider, "#90A4AE"),
    (cap_cyan, "#44BCF1"),
    (cap_lime, "#D7E54A"),
    (cap_orange, "#F1AC47"),
    (cap_red, "#E65757"),
    (bar_cyan, "#44BCF1"),
    (bar_lime, "#D7E54A"),
    (bar_orange, "#F1AC47"),
    (bar_red, "#E65757"),
)

for pts, col in shapes:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w_border, color=DARK, closed=True)

save()
