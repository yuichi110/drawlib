# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data icon: planetscale (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(91.0, 49.99), (90.46, 43.34), (88.91, 37.03), (86.42, 31.15), (83.09, 25.78), (78.99, 21.01), (74.22, 16.91), (68.85, 13.58), (62.97, 11.09), (56.66, 9.54), (50.01, 9.0)], style=Icon.fill_style('#18181B'))
polygon([(50.0, 91.0), (54.92, 90.71), (59.67, 89.85), (64.21, 88.47), (68.51, 86.59), (72.54, 84.26), (76.26, 81.49), (79.64, 78.33), (82.64, 74.81), (85.24, 70.96), (87.4, 66.82), (33.18, 12.6), (32.48, 12.92), (31.8, 13.25), (31.12, 13.6), (30.44, 13.96), (29.78, 14.33), (29.12, 14.71), (28.47, 15.1), (27.83, 15.51), (27.19, 15.92), (26.57, 16.35), (60.22, 50.0), (50.0, 50.0), (21.01, 21.01), (18.87, 23.32), (16.91, 25.79), (15.14, 28.4), (13.58, 31.16), (12.22, 34.04), (11.09, 37.04), (10.19, 40.15), (9.54, 43.35), (9.14, 46.64), (9.0, 50.0), (9.54, 56.65), (11.09, 62.96), (13.58, 68.84), (16.91, 74.21), (21.01, 78.99), (25.79, 83.09), (31.16, 86.42), (37.04, 88.91), (43.35, 90.46)], style=Icon.fill_style('#18181B'))
save()
# fmt: on
