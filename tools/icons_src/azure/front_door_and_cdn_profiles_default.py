# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: front_door_and_cdn_profiles (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_BLUE, AZURE_CYAN, AZURE_PALE_GRAY, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(92.0, 46.13), (91.33, 50.46), (89.67, 54.52), (87.11, 58.08), (83.78, 60.95), (79.88, 62.96), (75.62, 64.0), (74.61, 70.12), (72.05, 75.77), (68.12, 80.57), (63.09, 84.19), (57.29, 86.38), (51.12, 87.01), (45.14, 86.38), (39.5, 84.31), (34.54, 80.92), (30.55, 76.43), (27.79, 71.09), (22.63, 69.83), (17.91, 67.4), (13.89, 63.93), (10.79, 59.61), (8.79, 54.69), (8.0, 49.44), (9.0, 43.57), (11.49, 38.15), (15.29, 33.56), (20.14, 30.11), (25.73, 28.03), (31.66, 27.46), (33.71, 27.46), (72.03, 27.46), (72.28, 27.43), (72.54, 27.42), (72.8, 27.43), (73.05, 27.46), (77.9, 28.12), (82.42, 29.99), (86.31, 32.95), (89.33, 36.8), (91.27, 41.29)], style=fill_style(AZURE_BLUE))
polygon([(38.94, 60.17), (62.55, 60.17), (62.55, 27.51), (38.94, 27.51)], style=fill_style(AZURE_PALE_GRAY))
polygon([(66.85, 62.27), (50.56, 71.61), (50.27, 71.66), (49.98, 71.64), (49.7, 71.55), (49.45, 71.38), (49.25, 71.17), (49.11, 70.91), (49.11, 70.89), (49.11, 70.86), (49.11, 70.81), (49.11, 70.75), (49.11, 70.69), (49.11, 70.63), (49.11, 70.58), (49.11, 70.53), (49.11, 14.16), (49.15, 13.87), (49.26, 13.59), (49.44, 13.35), (49.67, 13.16), (49.94, 13.04), (50.23, 12.99), (50.61, 12.99), (66.89, 22.61), (67.15, 22.73), (67.37, 22.91), (67.54, 23.14), (67.64, 23.4), (67.69, 23.68), (67.69, 61.01), (67.68, 61.29), (67.61, 61.55), (67.49, 61.79), (67.31, 62.0), (67.09, 62.16)], style=fill_style(AZURE_CYAN))
save()
# fmt: on
