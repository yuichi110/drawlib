# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: veeam (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(9.0, 91.0), (9.0, 34.62), (9.0, 34.44), (9.02, 33.9), (9.09, 33.08), (9.23, 31.96), (9.43, 30.62), (9.73, 29.09), (10.14, 27.4), (10.71, 25.61), (11.41, 23.74), (12.28, 21.8), (13.35, 19.89), (14.63, 18.02), (16.13, 16.22), (17.88, 14.54), (19.91, 13.01), (22.21, 11.67), (24.81, 10.55), (27.72, 9.71), (31.0, 9.18), (34.62, 9.0), (91.0, 9.0), (91.0, 27.22), (38.61, 27.22), (38.47, 27.22), (38.11, 27.24), (37.5, 27.29), (36.72, 27.4), (35.76, 27.54), (34.67, 27.77), (33.49, 28.06), (32.19, 28.47), (30.87, 28.98), (29.5, 29.61), (28.13, 30.37), (26.81, 31.28), (25.51, 32.35), (24.33, 33.6), (23.24, 35.03), (22.28, 36.65), (21.51, 38.5), (20.89, 40.57), (20.53, 42.89), (20.39, 45.44), (20.39, 91.0)], style=Icon.fill_style('#4CAF50'))
polygon([(29.5, 91.0), (43.17, 91.0), (60.25, 50.0), (77.33, 91.0), (91.0, 91.0), (68.22, 36.33), (52.28, 36.33)], style=Icon.fill_style('#455A64'))
save()
# fmt: on
