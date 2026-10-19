# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data icon: arrow (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(9.0, 84.17), (43.17, 50.0), (9.0, 15.83), (9.0, 29.5), (29.5, 50.0), (9.0, 70.5)], style=Icon.fill_style('#0284C7'))
polygon([(32.92, 84.17), (67.08, 50.0), (32.92, 15.83), (32.92, 29.5), (53.42, 50.0), (32.92, 70.5)], style=Icon.fill_style('#0284C7'))
polygon([(56.83, 84.17), (91.0, 50.0), (56.83, 15.83), (56.83, 29.5), (77.33, 50.0), (56.83, 70.5)], style=Icon.fill_style('#0284C7'))
save()
# fmt: on
