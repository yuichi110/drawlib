# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud icon: vercel (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.0, 85.5), (91.0, 14.5), (9.0, 14.5)], style=fill_style('#000000'))
save()
# fmt: on
