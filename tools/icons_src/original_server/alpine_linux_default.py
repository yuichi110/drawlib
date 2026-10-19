# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: alpine_linux."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

hex_outer = [(70.5, 85.49), (91.0, 49.97), (70.51, 14.48), (29.5, 14.48), (9.0, 49.99), (29.5, 85.52)]
wedge_hole = [(38.79, 41.27), (38.79, 49.9), (32.57, 43.68), (33.5, 43.06), (34.64, 42.42), (36.05, 41.81), (37.32, 41.43), (38.22, 41.29)]
left_mountain_hole = [(52.33, 57.11), (43.06, 66.65), (19.82, 43.68), (20.75, 43.06), (22.35, 42.19), (23.34, 41.78), (24.39, 41.47), (25.7, 41.27), (26.68, 41.28), (27.53, 41.43), (28.25, 41.69), (28.75, 42.01), (39.26, 52.51), (43.0, 56.11), (53.39, 45.71), (57.02, 41.98), (57.36, 41.75), (58.07, 41.47), (58.82, 41.29), (59.96, 41.24), (60.9, 41.34), (61.87, 41.57), (63.22, 42.07), (64.05, 42.47), (64.94, 42.97), (65.97, 43.65), (57.63, 51.81)]
right_mountain_hole = [(70.61, 41.98), (71.2, 41.63), (71.97, 41.37), (72.68, 41.25), (73.5, 41.24), (74.48, 41.34), (75.46, 41.57), (76.22, 41.83), (77.83, 42.57), (79.56, 43.65), (74.83, 48.26), (59.18, 63.97), (53.87, 58.65)]
# fmt: on

polygon(hex_outer, holes=[wedge_hole, left_mountain_hole, right_mountain_hole], style=Icon.fill_style("#4D88A8"))

for ring in (hex_outer, wedge_hole, left_mountain_hole, right_mountain_hole):
    Icon.draw_round_polyline(ring, width_units=w, color=Icon.DARK, closed=True)

save()
