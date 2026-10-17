# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: amd (default variant)."""

from drawlib.canvas import save
from drawlib.utils import draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(32.03, 68.66), (9.69, 91.0), (91.0, 91.0), (91.0, 9.69), (68.66, 32.01), (68.66, 68.66)], [(32.0, 64.19), (9.0, 41.19), (9.0, 9.0), (41.19, 9.0), (64.19, 32.0), (32.0, 32.0)]], color='#000000')
save()
# fmt: on
