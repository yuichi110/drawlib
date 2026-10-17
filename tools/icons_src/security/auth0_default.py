# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: auth0 (default variant)."""

from drawlib.canvas import save
from drawlib.utils import draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(71.79, 24.67), (63.47, 50.0), (85.26, 65.66), (58.33, 65.66), (50.01, 91.0), (76.96, 91.0), (85.29, 65.66), (85.94, 63.44), (86.44, 61.2), (86.81, 58.94), (87.02, 56.68), (87.09, 54.39), (87.03, 52.13), (86.81, 49.87), (86.46, 47.64), (85.98, 45.43), (85.36, 43.25), (84.59, 41.1), (83.7, 38.99), (82.67, 36.96), (81.51, 34.97), (80.21, 33.05), (78.79, 31.19), (77.23, 29.42), (75.55, 27.74), (73.74, 26.16)], [(28.21, 24.67), (50.0, 9.0), (71.79, 24.67), (50.01, 40.33)], [(14.73, 65.67), (14.05, 63.34), (13.52, 60.99), (13.16, 58.65), (12.96, 56.32), (12.91, 54.0), (13.0, 51.69), (13.24, 49.4), (13.63, 47.14), (14.15, 44.93), (14.8, 42.75), (15.6, 40.62), (16.52, 38.55), (17.57, 36.53), (18.75, 34.59), (20.03, 32.72), (21.44, 30.92), (22.97, 29.21), (24.61, 27.59), (26.34, 26.07), (28.18, 24.66), (28.18, 24.67), (36.52, 50.0), (14.73, 65.67), (41.67, 65.66), (50.0, 91.0), (23.06, 91.0)]], color='#EB5424')
save()
# fmt: on
