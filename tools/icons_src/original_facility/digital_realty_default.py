# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: digital_realty (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_compound_polygon, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 1.8
w_inner = 1.3
left_face = [(14.31, 75.15), (42.33, 89.76), (42.33, 11.2), (14.31, 25.8)]
right_outer = [(46.89, 90.0), (51.74, 88.15), (51.74, 74.51), (56.59, 73.34), (56.59, 86.28), (71.14, 80.72), (71.14, 72.26), (75.99, 70.94), (75.99, 78.86), (85.69, 75.15), (85.69, 25.8), (56.59, 13.95), (56.59, 23.36), (51.74, 21.87), (51.74, 11.98), (46.89, 10.0)]
right_holes = [[(51.74, 65.22), (56.59, 64.52), (56.59, 56.56), (51.74, 56.84)], [(51.74, 40.16), (56.59, 40.71), (56.59, 32.32), (51.74, 31.33)], [(56.59, 52.51), (61.43, 52.44), (61.43, 45.32), (56.59, 44.99)], [(61.43, 76.49), (66.28, 75.07), (66.28, 67.18), (61.43, 68.13)], [(61.43, 45.18), (66.28, 45.52), (66.28, 31.03), (61.43, 29.83)], [(66.28, 59.87), (71.14, 59.37), (71.14, 52.3), (66.28, 52.37)], [(71.14, 35.27), (75.99, 36.28), (75.99, 29.27), (71.14, 27.79)], [(75.99, 72.25), (80.84, 70.84), (80.84, 64.35), (75.99, 65.3)], [(75.99, 55.89), (80.84, 55.58), (80.84, 37.4), (75.99, 36.39)]]

polygon(left_face, style=no_border_fill("#6488D4"))
draw_round_polyline(left_face, width_units=w_outer, color=DARK, closed=True)

draw_compound_polygon([right_outer, *right_holes], color="#82B4E8")
draw_round_polyline(right_outer, width_units=w_outer, color=DARK, closed=True)
for hole in right_holes:
    draw_round_polyline(hole, width_units=w_inner, color=DARK, closed=True)

save()
# fmt: on
