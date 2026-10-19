# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Facility icon: iron_mountain (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(38.73, 65.29), (53.47, 41.29), (68.34, 17.29), (38.73, 17.29), (9.0, 17.29), (23.86, 41.29)], style=Icon.fill_style('#13487D', alpha=0.75))
polygon([(61.27, 82.71), (76.14, 49.94), (91.0, 17.29), (61.27, 17.29), (31.54, 17.29), (46.41, 49.94)], style=Icon.fill_style('#1C75BC', alpha=0.75))
polygon([(49.94, 73.33), (64.8, 45.31), (79.67, 17.29), (49.94, 17.29), (20.33, 17.29), (35.2, 45.31)], style=Icon.fill_style('#6DCFF6', alpha=0.75))
save()
# fmt: on
