# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Business icon: magento (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.03, 91.0), (14.5, 70.49), (14.5, 29.5), (24.65, 23.64), (24.58, 64.62), (49.97, 79.29), (75.35, 64.62), (75.35, 23.66), (85.5, 29.5), (85.5, 70.52)], style=Icon.fill_style('#F26322'))
polygon([(55.07, 23.64), (50.0, 20.71), (44.91, 23.63), (44.91, 64.62), (34.76, 58.76), (34.78, 17.79), (50.0, 9.0), (65.22, 17.79), (65.22, 58.76), (55.07, 64.62)], style=Icon.fill_style('#F26322'))
save()
# fmt: on
