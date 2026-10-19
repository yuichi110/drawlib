# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: zig (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(33.65, 75.73), (24.01, 63.93), (19.18, 71.44)], style=Icon.fill_style('#F7A41D'))
polygon([(33.65, 75.73), (26.69, 69.83), (24.01, 63.93), (20.79, 63.93), (20.79, 36.6), (25.61, 36.6), (19.72, 33.92), (15.43, 24.81), (9.0, 24.81), (9.0, 75.73)], style=Icon.fill_style('#F7A41D'))
polygon([(25.61, 36.6), (15.43, 24.81), (11.14, 30.71)], style=Icon.fill_style('#F7A41D'))
polygon([(39.01, 75.73), (42.23, 68.22), (28.83, 63.93)], style=Icon.fill_style('#F7A41D'))
polygon([(39.01, 75.73), (68.49, 75.73), (68.49, 63.93), (28.83, 63.93), (39.01, 70.37)], style=Icon.fill_style('#F7A41D'))
polygon([(71.17, 36.6), (60.99, 24.81), (57.24, 31.78)], style=Icon.fill_style('#F7A41D'))
polygon([(71.17, 36.6), (62.59, 31.78), (60.99, 24.81), (31.51, 24.81), (31.51, 36.6)], style=Icon.fill_style('#F7A41D'))
polygon([(89.39, 87.52), (36.87, 24.81), (10.61, 12.48), (63.13, 75.73)], style=Icon.fill_style('#F7A41D'))
polygon([(84.57, 75.73), (84.03, 66.08), (74.39, 63.4)], style=Icon.fill_style('#F7A41D'))
polygon([(91.0, 75.73), (91.0, 24.81), (65.81, 24.81), (73.31, 31.24), (75.99, 36.6), (79.21, 36.6), (79.21, 63.4), (74.39, 63.4), (79.74, 68.22), (84.57, 75.73)], style=Icon.fill_style('#F7A41D'))
polygon([(75.99, 36.6), (78.67, 28.56), (65.81, 24.81)], style=Icon.fill_style('#F7A41D'))
save()
# fmt: on
