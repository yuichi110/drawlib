# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud icon: microsoft (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(9.0, 91.0), (47.95, 91.0), (47.95, 52.05), (9.0, 52.05)], style=fill_style('#F25022'))
polygon([(52.05, 91.0), (91.0, 91.0), (91.0, 52.05), (52.05, 52.05)], style=fill_style('#7FBA00'))
polygon([(9.0, 47.95), (47.95, 47.95), (47.95, 9.0), (9.0, 9.0)], style=fill_style('#00A4EF'))
polygon([(52.05, 47.95), (91.0, 47.95), (91.0, 9.0), (52.05, 9.0)], style=fill_style('#FFB900'))
save()
# fmt: on
