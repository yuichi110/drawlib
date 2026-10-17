# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: netapp (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(9.0, 83.98), (9.0, 16.02), (41.18, 16.02), (41.18, 56.67), (58.76, 56.67), (58.76, 16.02), (91.0, 16.02), (91.0, 83.98)], style=fill_style('#000000'))
save()
# fmt: on
