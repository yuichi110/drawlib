# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: risc_v."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

amber_piece: list[tuple[float, float]] = [(54.36, 64.14), (54.31, 62.51), (54.13, 60.88), (53.9, 59.31), (53.55, 57.74), (53.08, 56.23), (52.56, 54.71), (51.92, 53.26), (51.16, 51.86), (50.29, 50.52), (49.36, 49.24), (48.31, 48.02), (47.21, 46.92), (45.98, 45.81), (44.65, 44.82), (43.19, 43.95), (41.68, 43.13), (40.11, 42.38), (38.36, 41.74), (36.56, 41.27), (34.64, 40.81), (52.97, 19.16), (54.66, 21.49), (87.65, 68.16), (87.65, 87.83), (34.0, 87.83), (35.98, 87.59), (37.9, 87.13), (39.64, 86.6), (41.33, 85.91), (42.96, 85.15), (44.41, 84.22), (45.81, 83.23), (47.03, 82.12), (48.2, 80.9), (49.3, 79.62), (50.23, 78.28), (51.11, 76.89), (51.86, 75.43), (52.5, 73.86), (53.08, 72.35), (53.55, 70.72), (53.9, 69.09), (54.13, 67.46), (54.31, 65.83)]
blue_left: list[tuple[float, float]] = [(16.66, 50.81), (29.34, 50.81), (30.68, 50.87), (31.96, 51.05), (33.18, 51.28), (34.35, 51.57), (35.45, 51.98), (36.44, 52.44), (37.43, 53.03), (38.3, 53.61), (39.06, 54.31), (39.82, 55.0), (40.51, 55.76), (41.1, 56.58), (41.62, 57.45), (42.09, 58.32), (42.43, 59.25), (42.78, 60.24), (43.02, 61.17), (43.19, 62.16), (43.31, 63.15), (43.31, 64.14), (43.31, 65.19), (43.19, 66.18), (43.02, 67.11), (42.78, 68.1), (42.43, 69.03), (42.09, 69.9), (41.62, 70.77), (41.1, 71.65), (40.51, 72.4), (39.82, 73.16), (39.06, 73.86), (38.3, 74.5), (37.43, 75.08), (36.44, 75.6), (35.45, 76.07), (34.35, 76.48), (33.18, 76.77), (31.96, 77.0), (30.68, 77.12), (29.34, 77.18), (12.0, 77.18), (12.0, 12.17), (44.36, 12.17), (16.66, 45.52)]
blue_right: list[tuple[float, float]] = [(63.68, 15.55), (88.0, 49.53), (88.0, 12.23), (61.29, 12.23)]

polygon(amber_piece, style=Icon.no_border_fill("#F1B447"))
Icon.draw_round_polyline(amber_piece, width_units=w, color=Icon.DARK, closed=True)

for pts in (blue_left, blue_right):
    polygon(pts, style=Icon.no_border_fill("#5C78B0"))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
# fmt: on
