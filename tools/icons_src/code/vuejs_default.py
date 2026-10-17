# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: vuejs (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(25.31, 85.13), (40.25, 85.12), (50.02, 68.9), (59.76, 85.12), (74.69, 85.12), (50.1, 42.46)], style=fill_style('#35495E'))
polygon([(9.0, 85.01), (25.29, 85.12), (50.08, 42.45), (74.68, 85.12), (91.0, 85.1), (50.08, 14.87)], style=fill_style('#41B883'))
save()
# fmt: on
