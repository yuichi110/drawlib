# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: bastions (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_LIGHT_BLUE, AZURE_PALE_BLUE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(85.64, 35.5), (81.9, 31.75), (81.55, 31.48), (81.14, 31.31), (80.7, 31.25), (80.26, 31.3), (79.85, 31.47), (79.5, 31.74), (51.8, 59.36), (51.33, 59.96), (51.0, 60.64), (50.83, 61.38), (50.83, 62.14), (51.0, 62.88), (51.32, 63.57), (51.8, 64.16), (55.54, 67.91), (85.64, 37.9), (85.88, 37.6), (86.04, 37.26), (86.13, 36.89), (86.13, 36.51), (86.04, 36.14), (85.88, 35.8)], style=fill_style(AZURE_PALE_BLUE))
polygon([(81.34, 91.51), (85.09, 87.76), (85.36, 87.41), (85.53, 87.0), (85.59, 86.57), (85.54, 86.13), (85.37, 85.72), (85.1, 85.37), (55.52, 55.71), (51.77, 59.45), (51.29, 60.04), (50.96, 60.73), (50.79, 61.47), (50.79, 62.23), (50.96, 62.97), (51.29, 63.65), (51.76, 64.25), (78.94, 91.5), (79.29, 91.77), (79.7, 91.94), (80.14, 92.0), (80.57, 91.94), (80.98, 91.78), (81.33, 91.51)], style=fill_style(AZURE_LIGHT_BLUE))
polygon([(44.46, 44.66), (48.2, 40.91), (48.68, 40.32), (49.0, 39.63), (49.17, 38.89), (49.17, 38.13), (49.0, 37.39), (48.67, 36.71), (48.2, 36.11), (20.5, 8.49), (20.15, 8.22), (19.74, 8.06), (19.3, 8.0), (18.86, 8.06), (18.45, 8.23), (18.1, 8.5), (14.36, 12.25), (14.09, 12.6), (13.92, 13.01), (13.86, 13.45), (13.92, 13.89), (14.09, 14.3), (14.36, 14.65)], style=fill_style(AZURE_PALE_BLUE))
polygon([(48.23, 36.2), (44.48, 32.46), (14.9, 62.11), (14.64, 62.47), (14.47, 62.87), (14.41, 63.31), (14.47, 63.75), (14.64, 64.16), (14.91, 64.51), (18.66, 68.25), (19.01, 68.52), (19.42, 68.69), (19.86, 68.75), (20.3, 68.69), (20.71, 68.52), (21.06, 68.25), (48.24, 40.99), (48.71, 40.4), (49.04, 39.71), (49.21, 38.97), (49.2, 38.21), (49.03, 37.47), (48.7, 36.79)], style=fill_style(AZURE_LIGHT_BLUE))
save()
# fmt: on
