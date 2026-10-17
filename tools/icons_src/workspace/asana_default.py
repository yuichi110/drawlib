# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Workspace icon: asana (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
circle((73.17, 29.94), radius=17.83, style=fill_style('#F06A6A'))
circle((26.83, 29.94), radius=17.83, style=fill_style('#F06A6A'))
circle((50.0, 70.06), radius=17.83, style=fill_style('#F06A6A'))
save()
# fmt: on
