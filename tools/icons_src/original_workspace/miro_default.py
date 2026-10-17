# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: miro."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
w_outer = 1.9
w_inner = 1.8

bg_sq = [(11.2, 69.4), (11.27, 70.99), (11.46, 72.55), (11.77, 74.07), (12.19, 75.53), (12.72, 76.95), (13.37, 78.31), (14.11, 79.62), (14.95, 80.86), (15.87, 82.02), (16.88, 83.12), (17.98, 84.13), (19.14, 85.05), (20.38, 85.89), (21.69, 86.63), (23.05, 87.28), (24.47, 87.81), (25.93, 88.23), (27.45, 88.54), (29.01, 88.73), (30.6, 88.8), (69.4, 88.8), (70.99, 88.73), (72.55, 88.54), (74.07, 88.23), (75.53, 87.81), (76.95, 87.28), (78.31, 86.63), (79.62, 85.89), (80.86, 85.05), (82.02, 84.13), (83.12, 83.12), (84.13, 82.02), (85.05, 80.86), (85.89, 79.62), (86.63, 78.31), (87.28, 76.95), (87.81, 75.53), (88.23, 74.07), (88.54, 72.55), (88.73, 70.99), (88.8, 69.4), (88.8, 30.6), (88.73, 29.01), (88.54, 27.45), (88.23, 25.93), (87.81, 24.47), (87.28, 23.05), (86.63, 21.69), (85.89, 20.38), (85.05, 19.14), (84.13, 17.98), (83.12, 16.88), (82.02, 15.87), (80.86, 14.95), (79.62, 14.11), (78.31, 13.37), (76.95, 12.72), (75.53, 12.19), (74.07, 11.77), (72.55, 11.46), (70.99, 11.27), (69.4, 11.2), (30.6, 11.2), (29.01, 11.27), (27.45, 11.46), (25.93, 11.77), (24.47, 12.19), (23.05, 12.72), (21.69, 13.37), (20.38, 14.11), (19.14, 14.95), (17.98, 15.87), (16.88, 16.88), (15.87, 17.98), (14.95, 19.14), (14.11, 20.38), (13.37, 21.69), (12.72, 23.05), (12.19, 24.47), (11.77, 25.93), (11.46, 27.45), (11.27, 29.01), (11.2, 30.6)]
m_glyph = [(62.79, 74.01), (55.74, 74.01), (61.61, 63.69), (48.7, 74.01), (41.65, 74.01), (48.12, 61.4), (34.61, 74.01), (27.57, 74.01), (34.61, 57.96), (27.57, 25.87), (34.61, 25.87), (48.12, 60.25), (41.65, 25.87), (48.7, 25.87), (61.61, 62.55), (55.74, 25.87), (62.79, 25.87), (75.7, 65.98)]

polygon(bg_sq, style=no_border_fill("#FFE46B"))
draw_round_polyline(bg_sq, width_units=w_outer, color=DARK, closed=True)

polygon(m_glyph, style=no_border_fill("#4A5262"))
draw_round_polyline(m_glyph, width_units=w_inner, color=DARK, closed=True)

save()
# fmt: on
