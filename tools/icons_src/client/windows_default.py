# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Client icon: windows (default variant)."""

from drawlib.canvas import save
from drawlib.utils import draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(52.13, 47.87), (91.0, 47.87), (91.0, 9.0), (52.13, 9.0)], [(9.0, 47.87), (47.87, 47.87), (47.87, 9.0), (9.0, 9.0)], [(52.13, 91.0), (91.0, 91.0), (91.0, 52.13), (52.13, 52.13)], [(9.0, 91.0), (47.87, 91.0), (47.87, 52.13), (9.0, 52.13)]], color='#0078D4')
save()
# fmt: on
