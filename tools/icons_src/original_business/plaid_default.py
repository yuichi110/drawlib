# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business brand icon: plaid."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
p_0_outer = [(42.05, 88.8), (18.27, 82.57), (11.71, 58.66), (19.92, 50.25), (11.59, 41.97), (17.75, 17.95), (41.43, 11.33), (49.75, 19.61), (57.95, 11.2), (81.73, 17.43), (88.28, 41.34), (80.08, 49.75), (88.41, 58.03), (82.25, 82.05), (58.57, 88.67), (50.25, 80.39)]
p_0_holes = [[(29.41, 50.17), (37.39, 58.11), (45.26, 50.04), (37.26, 42.1)], [(41.98, 37.27), (49.96, 45.2), (57.82, 37.14), (49.83, 29.2)], [(54.75, 49.96), (62.74, 57.9), (70.59, 49.83), (62.61, 41.89)], [(42.17, 62.86), (50.17, 70.8), (58.02, 62.73), (50.04, 54.8)], [(27.01, 22.4), (37.19, 32.51), (45.05, 24.45), (39.48, 18.91)], [(27.46, 77.97), (39.98, 81.26), (45.46, 75.63), (37.47, 67.7)], [(67.31, 37.06), (75.31, 44.99), (80.78, 39.37), (77.33, 26.78)], [(67.52, 62.65), (77.7, 72.77), (80.95, 60.12), (75.38, 54.59)], [(54.54, 24.37), (62.53, 32.3), (72.54, 22.03), (60.01, 18.74)], [(54.95, 75.56), (60.52, 81.09), (72.99, 77.6), (62.81, 67.49)], [(19.05, 39.88), (24.62, 45.41), (32.48, 37.35), (22.3, 27.23)], [(19.22, 60.62), (22.67, 73.21), (32.68, 62.94), (24.69, 55.0), (19.22, 60.63)]]
polygon(p_0_outer, holes=p_0_holes, style=Icon.no_border_fill('#64748B'))
Icon.draw_round_polyline(p_0_outer, width_units=2.0, color=Icon.DARK, closed=True)
for h_ring in p_0_holes:
    Icon.draw_round_polyline(h_ring, width_units=1.5, color=Icon.DARK, closed=True)
save()
# fmt: on
