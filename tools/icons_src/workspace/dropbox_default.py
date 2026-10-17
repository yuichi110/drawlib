# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Workspace icon: dropbox (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(29.5, 84.84), (9.0, 71.78), (29.5, 58.72), (50.0, 71.78)], style=fill_style('#0061FF'))
polygon([(70.5, 84.84), (50.0, 71.78), (70.5, 58.72), (91.0, 71.78)], style=fill_style('#0061FF'))
polygon([(9.0, 45.66), (29.5, 32.6), (50.0, 45.66), (29.5, 58.72)], style=fill_style('#0061FF'))
polygon([(70.5, 58.72), (50.0, 45.66), (70.5, 32.6), (91.0, 45.66)], style=fill_style('#0061FF'))
polygon([(29.5, 28.22), (50.0, 15.16), (70.5, 28.22), (50.0, 41.28)], style=fill_style('#0061FF'))
save()
# fmt: on
