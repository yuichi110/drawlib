# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Network icon: opnsense (default variant)."""

from drawlib.canvas import save
from drawlib.utils import draw_compound_polygon, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(27.04, 91.0), (27.04, 72.96), (72.96, 72.96), (72.96, 27.04), (91.0, 27.04), (91.0, 65.14), (65.13, 91.0)], [(72.96, 27.04), (27.04, 27.04), (27.04, 72.96), (9.0, 72.96), (9.0, 35.24), (35.24, 9.0), (72.96, 9.0)]], color='#C03E14')
save()
# fmt: on
