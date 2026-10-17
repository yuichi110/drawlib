# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: nixos (default variant)."""

from drawlib.canvas import save
from drawlib.utils import draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(41.21, 64.3), (21.25, 27.27), (16.59, 35.73), (21.97, 45.66), (11.27, 45.69), (9.0, 49.92), (11.34, 54.24), (26.57, 54.2), (32.05, 64.29)], [(42.76, 34.71), (82.7, 34.71), (78.19, 26.15), (67.47, 26.18), (72.79, 16.26), (70.52, 12.01), (65.86, 12.01), (58.28, 26.14), (47.37, 26.15)], [(66.02, 50.93), (46.04, 87.96), (55.22, 88.05), (60.55, 78.11), (65.92, 88.01), (70.48, 88.01), (72.81, 83.68), (65.15, 69.6), (70.58, 59.48)]], color='#7EBAE4')
draw_compound_polygon([[(34.02, 49.06), (53.99, 12.03), (44.81, 11.93), (39.48, 21.89), (34.11, 11.99), (29.55, 11.99), (27.21, 16.32), (34.87, 30.38), (29.44, 40.5)], [(57.22, 65.38), (17.26, 65.38), (21.78, 73.93), (32.49, 73.9), (27.18, 83.82), (29.45, 88.07), (34.11, 88.07), (41.69, 73.94), (52.59, 73.93)], [(58.79, 35.68), (78.76, 72.71), (83.42, 64.25), (78.03, 54.34), (88.73, 54.31), (91.0, 50.06), (88.66, 45.74), (73.43, 45.79), (67.95, 35.7)]], color='#5277C3')
save()
# fmt: on
