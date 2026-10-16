# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native icon: containerd (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
draw_compound_polygon([[(21.85, 90.38), (21.85, 9.52), (78.27, 9.52), (78.27, 90.38)], [(68.9, 18.92), (31.26, 18.92), (31.26, 54.65), (57.58, 54.65), (57.58, 67.83), (68.86, 67.83), (68.86, 18.92)]], color="#000000")
polygon([(42.54, 45.25), (57.58, 45.25), (57.58, 28.33), (42.54, 28.33)], style=fill_style("#000000"))
save()
# fmt: on
