# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: npm."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w_outer = 2.0
w_inner = 1.5

outer_sq = [(10.0, 85.59), (10.02, 85.94), (10.06, 86.29), (10.13, 86.63), (10.22, 86.97), (10.35, 87.29), (10.5, 87.6), (10.67, 87.89), (10.86, 88.18), (11.07, 88.44), (11.31, 88.69), (11.56, 88.93), (11.82, 89.14), (12.11, 89.33), (12.4, 89.5), (12.71, 89.65), (13.03, 89.78), (13.37, 89.87), (13.71, 89.94), (14.06, 89.98), (14.41, 90.0), (85.59, 90.0), (85.94, 89.98), (86.29, 89.94), (86.63, 89.87), (86.97, 89.78), (87.29, 89.65), (87.6, 89.5), (87.89, 89.33), (88.18, 89.14), (88.44, 88.93), (88.69, 88.69), (88.93, 88.44), (89.14, 88.18), (89.33, 87.89), (89.5, 87.6), (89.65, 87.29), (89.78, 86.97), (89.87, 86.63), (89.94, 86.29), (89.98, 85.94), (90.0, 85.59), (90.0, 14.41), (89.98, 14.06), (89.94, 13.71), (89.87, 13.37), (89.78, 13.03), (89.65, 12.71), (89.5, 12.4), (89.33, 12.11), (89.14, 11.82), (88.93, 11.56), (88.69, 11.31), (88.44, 11.07), (88.18, 10.86), (87.89, 10.67), (87.6, 10.5), (87.29, 10.35), (86.97, 10.22), (86.63, 10.13), (86.29, 10.06), (85.94, 10.02), (85.59, 10.0), (14.41, 10.0), (14.06, 10.02), (13.71, 10.06), (13.37, 10.13), (13.03, 10.22), (12.71, 10.35), (12.4, 10.5), (12.11, 10.67), (11.82, 10.86), (11.56, 11.07), (11.31, 11.31), (11.07, 11.56), (10.86, 11.82), (10.67, 12.11), (10.5, 12.4), (10.35, 12.71), (10.22, 13.03), (10.13, 13.37), (10.06, 13.71), (10.02, 14.06), (10.0, 14.41)]
n_hole = [(25.69, 73.43), (74.45, 73.43), (74.45, 24.67), (62.27, 24.67), (62.27, 61.26), (50.03, 61.26), (50.03, 24.67), (25.69, 24.67)]
# fmt: on

# Flat pastel red square with transparent 'n' cutout
polygon(outer_sq, holes=[n_hole], style=Icon.fill_style("#E75353"))
Icon.draw_round_polyline(outer_sq, width_units=w_outer, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(n_hole, width_units=w_inner, color=Icon.DARK, closed=True)

save()
