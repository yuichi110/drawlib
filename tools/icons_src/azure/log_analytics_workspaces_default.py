# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: log_analytics_workspaces (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_DARK_TEAL, WHITE, draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(34.09, 30.73), (54.25, 30.73), (54.25, 10.57), (34.09, 10.57)], [(13.37, 10.57), (30.73, 10.57), (30.73, 30.73), (10.57, 30.73), (10.57, 13.37), (10.66, 12.64), (10.94, 11.97), (11.39, 11.39), (11.97, 10.94), (12.64, 10.66)], [(10.57, 33.9), (30.73, 33.9), (30.73, 54.25), (10.57, 54.25)]], color="#1988D9")
polygon([(61.67, 89.43), (67.9, 88.78), (73.83, 86.74), (79.13, 83.4), (83.55, 78.95), (86.84, 73.62), (88.84, 67.67), (89.43, 61.43), (88.79, 55.23), (86.76, 49.33), (83.46, 44.05), (79.05, 39.64), (73.77, 36.34), (67.87, 34.31), (61.67, 33.67), (33.9, 33.67), (33.9, 61.67), (34.54, 67.87), (36.57, 73.77), (39.87, 79.05), (44.28, 83.46), (49.57, 86.76), (55.47, 88.79)], style=fill_style(AZURE_DARK_TEAL))
polygon([(43.42, 65.63), (49.77, 65.63), (49.77, 46.59), (43.42, 46.59)], style=fill_style(WHITE))
polygon([(56.11, 59.29), (62.46, 59.29), (62.46, 46.59), (56.11, 46.59)], style=fill_style(WHITE))
polygon([(68.81, 71.98), (75.15, 71.98), (75.15, 46.59), (68.81, 46.59)], style=fill_style(WHITE))
save()
# fmt: on
