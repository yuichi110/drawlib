# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: x (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(57.07, 55.82), (84.76, 88.0), (78.2, 88.0), (54.16, 60.06), (34.96, 88.0), (12.82, 88.0), (41.85, 45.75), (12.82, 12.0), (19.38, 12.0), (44.76, 41.51), (65.04, 12.0), (87.18, 12.0)], holes=[[(48.09, 45.37), (45.15, 49.58), (21.74, 83.06), (31.82, 83.06), (50.71, 56.04), (53.65, 51.83), (78.2, 16.72), (68.13, 16.72)]], style=Icon.fill_style(Colors.Gray6, border_color=Icon.DARK, border_units=Icon.ORIG_STROKE))
save()
# fmt: on
