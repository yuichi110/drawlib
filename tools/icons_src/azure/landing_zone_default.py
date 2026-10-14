# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: landing_zone (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_LIGHT_BLUE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(73.95, 67.71), (77.12, 66.95), (80.03, 65.66), (82.63, 63.91), (84.88, 61.75), (86.73, 59.24), (88.13, 56.43), (89.02, 53.38), (89.37, 50.14), (89.0, 46.64), (87.99, 43.36), (86.41, 40.38), (84.33, 37.76), (81.8, 35.57), (78.9, 33.87), (75.68, 32.73), (72.22, 32.2), (63.17, 51.79), (62.86, 52.34), (62.48, 52.84), (62.04, 53.28), (61.54, 53.65), (61.0, 53.95), (60.42, 54.16), (59.8, 54.3), (59.17, 54.34), (40.84, 54.34), (40.2, 54.3), (39.59, 54.16), (39.0, 53.94), (38.46, 53.64), (37.96, 53.27), (37.52, 52.83), (37.14, 52.32), (36.83, 51.76), (28.11, 32.57), (24.53, 33.57), (21.22, 35.14), (18.24, 37.23), (15.65, 39.76), (13.5, 42.7), (11.86, 45.98), (10.77, 49.55), (10.31, 53.35), (10.7, 57.26), (11.76, 60.94), (13.45, 64.32), (15.68, 67.34), (18.41, 69.92), (21.57, 71.99), (25.09, 73.49), (28.93, 74.35), (30.42, 77.67), (32.37, 80.67), (34.73, 83.3), (37.46, 85.53), (40.49, 87.32), (43.77, 88.63), (47.26, 89.43), (50.89, 89.68), (55.43, 89.32), (59.68, 88.1), (63.55, 86.11), (66.94, 83.45), (69.77, 80.19), (71.94, 76.42), (73.37, 72.24), (73.95, 67.72)], style=fill_style(AZURE_LIGHT_BLUE))
polygon([(47.78, 10.31), (47.78, 50.01), (41.24, 50.01), (23.55, 10.31)], style=fill_style("#A7A9A9"))
polygon([(52.15, 10.31), (52.15, 50.01), (58.69, 50.01), (76.38, 10.31)], style=fill_style("#A7A9A9"))
save()
# fmt: on
