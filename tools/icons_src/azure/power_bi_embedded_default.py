# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: power_bi_embedded (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(79.84, 89.79), (79.84, 10.21), (53.31, 10.21), (53.31, 89.79)], style=Icon.fill_style("#E6AD10"))
polygon([(63.26, 66.58), (63.26, 10.21), (36.74, 10.21), (36.74, 69.89), (59.94, 69.89), (60.68, 69.81), (61.38, 69.57), (62.01, 69.17), (62.54, 68.64), (62.93, 68.02), (63.18, 67.31)], style=Icon.fill_style("#F6D751"))
polygon([(20.16, 50.0), (20.16, 10.21), (46.69, 10.21), (46.69, 46.69), (46.57, 47.54), (46.24, 48.34), (45.71, 49.03), (45.03, 49.56), (44.23, 49.89), (43.37, 50.0)], style=Icon.fill_style("#F9E589"))
save()
# fmt: on
