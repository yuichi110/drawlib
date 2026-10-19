# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud icon: coolify (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(32.75, 67.25), (18.2, 67.25), (18.2, 23.56), (32.75, 23.56)], style=Icon.fill_style('#8C52FF'))
polygon([(32.75, 9.0), (91.0, 9.0), (91.0, 23.56), (32.75, 23.56)], style=Icon.fill_style('#8C52FF'))
polygon([(32.75, 67.25), (91.0, 67.25), (91.0, 81.8), (32.75, 81.8)], style=Icon.fill_style('#8C52FF'))
polygon([(28.15, 71.84), (13.59, 71.84), (13.59, 28.16), (28.15, 28.16)], style=Icon.fill_style('#8C52FF'))
polygon([(28.15, 13.61), (86.39, 13.61), (86.39, 28.16), (28.15, 28.16)], style=Icon.fill_style('#8C52FF'))
polygon([(28.15, 71.84), (86.39, 71.84), (86.39, 86.39), (28.15, 86.39)], style=Icon.fill_style('#8C52FF'))
polygon([(23.56, 76.44), (9.0, 76.44), (9.0, 32.75), (23.56, 32.75)], style=Icon.fill_style('#8C52FF'))
polygon([(23.56, 18.2), (81.8, 18.2), (81.8, 32.75), (23.56, 32.75)], style=Icon.fill_style('#8C52FF'))
polygon([(23.56, 76.44), (81.8, 76.44), (81.8, 91.0), (23.56, 91.0)], style=Icon.fill_style('#8C52FF'))
save()
# fmt: on
