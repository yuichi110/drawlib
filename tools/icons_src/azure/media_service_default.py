# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: media_service (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Azure, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(51.13, 73.67), (71.54, 61.94), (85.76, 70.15), (80.19, 77.82), (73.02, 84.0), (64.61, 88.38), (55.43, 90.7), (45.95, 90.86), (36.69, 88.85), (28.15, 84.76), (20.76, 78.82), (28.57, 79.48), (36.38, 78.82), (43.98, 76.87)], style=Icon.fill_style(Azure.DARK_BLUE))
polygon([(71.27, 61.94), (70.95, 33.78), (85.73, 29.81), (89.72, 39.6), (91.07, 50.09), (89.69, 60.57), (85.68, 70.36), (79.3, 78.79), (70.98, 85.32), (61.27, 89.5), (65.33, 83.27), (68.39, 76.49), (70.39, 69.32)], style=Icon.fill_style(Azure.BLUE))
polygon([(71.24, 37.65), (50.0, 25.38), (50.33, 9.05), (60.93, 10.48), (70.79, 14.6), (79.26, 21.13), (85.76, 29.63), (89.84, 39.51), (91.23, 50.11), (91.12, 52.58), (90.86, 55.03), (90.45, 57.46), (89.89, 59.87), (86.68, 53.23), (82.42, 47.2), (77.23, 41.97)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(50.0, 25.38), (28.74, 37.65), (14.65, 29.2), (21.11, 20.85), (29.5, 14.43), (39.24, 10.37), (49.69, 8.93), (60.17, 10.21), (69.98, 14.13), (78.45, 20.42), (71.13, 19.94), (63.83, 20.62), (56.73, 22.45)], style=Icon.fill_style(Azure.DARK_BLUE))
polygon([(28.73, 37.65), (29.05, 66.76), (14.51, 70.59), (12.1, 65.76), (10.35, 60.67), (9.29, 55.38), (8.93, 50.0), (10.37, 39.38), (14.5, 29.48), (21.03, 20.98), (29.53, 14.45), (39.43, 10.33), (35.17, 16.45), (31.92, 23.15), (29.76, 30.27)], style=Icon.fill_style(Azure.BLUE))
polygon([(29.47, 62.6), (50.0, 74.47), (43.46, 77.43), (36.56, 79.4), (29.45, 80.36), (22.27, 80.28), (16.62, 73.93), (12.4, 66.55), (9.8, 58.46), (8.93, 50.0), (9.03, 47.26), (9.31, 44.54), (9.77, 41.84), (10.4, 39.17), (13.68, 46.11), (18.03, 52.43), (23.34, 57.98)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(71.24, 37.65), (71.24, 62.2), (49.99, 74.47), (28.73, 62.2), (28.73, 37.65), (49.99, 25.38)], style=Icon.fill_style(Azure.PALE_CYAN))
polygon([(50.01, 49.67), (50.01, 25.38), (28.73, 37.65), (28.73, 62.11)], style=Icon.fill_style(Azure.CYAN))
polygon([(49.99, 49.67), (49.99, 25.38), (71.27, 37.65), (71.27, 62.11)], style=Icon.fill_style(Azure.CYAN))
save()
# fmt: on
