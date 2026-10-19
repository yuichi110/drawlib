# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: ory (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 70.5), (46.0, 70.11), (42.15, 68.94), (38.61, 67.05), (35.5, 64.5), (32.95, 61.39), (31.06, 57.85), (29.89, 54.0), (29.5, 50.0), (29.89, 46.0), (31.06, 42.15), (32.95, 38.61), (35.5, 35.5), (38.61, 32.95), (42.16, 31.06), (46.0, 29.89), (50.0, 29.5), (54.0, 29.89), (57.85, 31.06), (61.39, 32.95), (64.5, 35.5), (67.05, 38.61), (68.94, 42.15), (70.11, 46.0), (70.5, 50.0), (70.11, 54.0), (68.94, 57.85), (67.05, 61.39), (64.5, 64.5), (61.39, 67.05), (57.84, 68.94), (54.0, 70.11)], style=Icon.fill_style('#5D45FD'))
polygon([(29.5, 73.06), (29.5, 80.75), (50.0, 91.0), (70.5, 80.75), (70.5, 73.06), (50.0, 83.31)], style=Icon.fill_style('#5D45FD'))
polygon([(70.5, 26.94), (70.5, 19.25), (50.0, 9.0), (29.5, 19.25), (29.5, 26.94), (50.0, 16.69)], style=Icon.fill_style('#5D45FD'))
save()
# fmt: on
