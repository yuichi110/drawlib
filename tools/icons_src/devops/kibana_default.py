# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: kibana (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(82.03, 91.0), (17.97, 91.0), (17.97, 17.23)], style=fill_style('#F04E98'))
polygon([(17.97, 60.25), (17.97, 17.23), (48.55, 52.44), (47.17, 53.17), (45.78, 53.86), (44.37, 54.53), (42.94, 55.16), (41.49, 55.75), (40.03, 56.31), (38.55, 56.84), (37.05, 57.33), (35.53, 57.79), (34.0, 58.21), (32.46, 58.59), (30.9, 58.93), (29.33, 59.23), (27.74, 59.5), (26.14, 59.73), (24.53, 59.91), (22.91, 60.06), (21.27, 60.16), (19.63, 60.23), (17.97, 60.25)], style=fill_style('#343741'))
polygon([(55.15, 48.32), (23.77, 12.19), (21.0, 9.0), (80.75, 9.0), (80.21, 11.4), (79.58, 13.78), (78.87, 16.11), (78.07, 18.4), (77.18, 20.66), (76.22, 22.87), (75.17, 25.04), (74.05, 27.16), (72.85, 29.23), (71.57, 31.25), (70.22, 33.22), (68.81, 35.14), (67.32, 37.0), (65.77, 38.8), (64.15, 40.55), (62.47, 42.23), (60.73, 43.85), (58.93, 45.41), (57.07, 46.9), (55.15, 48.32)], style=fill_style('#00BFB3'))
save()
# fmt: on
