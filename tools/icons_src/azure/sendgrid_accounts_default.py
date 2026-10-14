# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: sendgrid_accounts (default variant)."""

from drawlib.canvas import save
from drawlib.utils import AZURE_BLUE, AZURE_DARK_BLUE, draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(37.03, 36.79), (11.13, 36.79), (11.13, 60.59), (11.23, 61.27), (11.5, 61.9), (11.92, 62.44), (12.47, 62.86), (13.11, 63.12), (13.79, 63.21), (37.12, 63.21)], [(62.97, 36.79), (37.03, 36.79), (37.03, 10.33), (60.36, 10.33), (60.95, 10.4), (61.51, 10.6), (62.02, 10.91), (62.44, 11.33), (62.76, 11.84), (62.95, 12.4), (63.02, 12.99)]], color=AZURE_DARK_BLUE)
draw_compound_polygon([[(62.97, 36.79), (37.03, 36.79), (37.03, 63.21), (62.97, 63.21)], [(37.03, 36.79), (11.13, 36.79), (11.13, 12.99), (11.19, 12.4), (11.39, 11.84), (11.71, 11.33), (12.13, 10.91), (12.63, 10.6), (13.19, 10.4), (13.79, 10.33), (37.12, 10.33)]], color=AZURE_BLUE)
draw_compound_polygon([[(62.97, 63.21), (37.03, 63.21), (37.03, 87.01), (37.09, 87.6), (37.29, 88.16), (37.61, 88.67), (38.03, 89.09), (38.53, 89.4), (39.09, 89.6), (39.69, 89.67), (63.02, 89.67)], [(88.87, 63.21), (62.97, 63.21), (62.97, 36.79), (86.73, 36.79), (87.27, 36.86), (87.79, 37.07), (88.23, 37.41), (88.57, 37.84), (88.79, 38.35), (88.87, 38.89)]], color=AZURE_BLUE)
draw_compound_polygon([[(88.87, 63.21), (62.97, 63.21), (62.97, 89.67), (86.73, 89.67), (87.27, 89.6), (87.79, 89.39), (88.23, 89.05), (88.57, 88.62), (88.79, 88.11), (88.87, 87.57)], [(62.97, 63.21), (37.03, 63.21), (37.03, 39.41), (37.13, 38.73), (37.4, 38.1), (37.82, 37.56), (38.37, 37.14), (39.01, 36.88), (39.69, 36.79), (63.02, 36.79)]], color="#32D4F5")
save()
# fmt: on
