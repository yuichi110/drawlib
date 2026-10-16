# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: tensorflow (default variant)."""

from drawlib.canvas import save
from drawlib.utils import draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(48.43, 9.0), (34.44, 17.12), (34.44, 65.02), (13.36, 52.84), (13.41, 70.99), (48.43, 91.0)], [(51.58, 91.0), (51.58, 9.0), (65.57, 17.12), (65.57, 40.19), (76.13, 34.09), (76.07, 49.87), (65.57, 55.86), (65.57, 65.02), (86.64, 52.84), (86.59, 70.99)]], color='#FF6F00')
save()
# fmt: on
