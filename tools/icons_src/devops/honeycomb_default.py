# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: honeycomb (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(26.21, 48.92), (31.95, 39.0), (26.21, 29.05), (14.75, 29.05), (9.0, 39.0), (14.75, 48.92)], style=Icon.fill_style('#F7941E'))
polygon([(50.65, 66.77), (57.64, 54.69), (50.65, 42.6), (36.72, 42.6), (29.73, 54.69), (36.72, 66.78)], style=Icon.fill_style('#8DC63F'))
polygon([(50.41, 35.48), (57.37, 23.39), (50.41, 11.3), (36.45, 11.3), (29.46, 23.39), (36.45, 35.48)], style=Icon.fill_style('#FDB913'))
polygon([(81.81, 88.7), (91.0, 72.79), (81.81, 56.86), (63.41, 56.86), (54.23, 72.79), (63.41, 88.7)], style=Icon.fill_style('#25BDBE'))
save()
# fmt: on
