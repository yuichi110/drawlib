# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: poetry."""

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

w_outer = 2.0
w_inner = 1.4

bottom_skirt = [(33.96, 10.0), (40.61, 11.63), (47.11, 13.81), (53.4, 16.53), (59.44, 19.77), (65.19, 23.5), (70.6, 27.7), (75.64, 32.34), (17.99, 90.0), (17.99, 25.98)]
left_facet = [(17.99, 89.99), (17.98, 25.98), (20.92, 26.05), (23.81, 26.23), (26.67, 26.56), (29.49, 27.0), (32.27, 27.58), (35.0, 28.26), (37.69, 29.06), (40.33, 29.98), (42.91, 31.0), (45.43, 32.14), (47.89, 33.38), (50.3, 34.71), (52.63, 36.16), (54.91, 37.69), (57.11, 39.32), (59.15, 40.96)]
fold_wedge = [(17.99, 90.0), (17.99, 89.99), (59.15, 40.96), (59.24, 41.03), (61.29, 42.84), (63.26, 44.72)]
top_facet = [(63.26, 44.73), (65.15, 46.7), (66.96, 48.75), (68.67, 50.88), (70.29, 53.07), (71.83, 55.35), (73.27, 57.69), (74.6, 60.09), (75.84, 62.56), (76.98, 65.07), (78.0, 67.66), (78.92, 70.29), (79.73, 72.98), (80.41, 75.71), (80.98, 78.49), (81.42, 81.31), (81.75, 84.18), (81.95, 87.06), (82.02, 90.0), (17.99, 90.0)]
outer_silhouette = [(17.99, 90.0), (82.01, 90.0), (81.98, 87.9), (81.87, 85.81), (81.71, 83.73), (81.46, 81.64), (81.16, 79.57), (80.78, 77.51), (80.34, 75.46), (79.83, 73.42), (79.26, 71.41), (78.61, 69.41), (77.91, 67.44), (77.14, 65.5), (76.3, 63.58), (75.4, 61.68), (74.45, 59.81), (73.43, 57.99), (72.36, 56.2), (71.22, 54.43), (70.03, 52.7), (68.78, 51.02), (67.48, 49.39), (66.13, 47.79), (64.71, 46.23), (63.26, 44.73), (75.64, 32.34), (70.6, 27.7), (65.19, 23.5), (59.44, 19.77), (53.4, 16.53), (47.11, 13.81), (40.61, 11.63), (33.96, 10.0), (17.99, 25.98)]
# fmt: on

# 1. Four flat pastel origami cone facets
polygon(bottom_skirt, style=no_border_fill("#7986CB"))
polygon(left_facet, style=no_border_fill("#64B5F6"))
polygon(fold_wedge, style=no_border_fill("#5C7CE6"))
polygon(top_facet, style=no_border_fill("#4FC3F7"))

# 2. Internal DARK facet borders
for facet in (left_facet, fold_wedge, top_facet):
    draw_round_polyline(facet, width_units=w_inner, color=DARK, closed=True)

# 3. Crisp DARK outer silhouette border
draw_round_polyline(outer_silhouette, width_units=w_outer, color=DARK, closed=True)

save()
