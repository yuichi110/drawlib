# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Business icon: netsuite (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(63.28, 85.4), (87.13, 85.4), (87.3, 32.28), (71.19, 32.28), (71.19, 70.59), (63.28, 70.59)], style=Icon.fill_style('#B1C2D2'))
polygon([(59.99, 45.51), (59.99, 89.51), (9.0, 89.51), (9.0, 70.74), (39.65, 70.74)], style=Icon.fill_style('#014372'))
polygon([(36.72, 14.6), (12.87, 14.6), (12.7, 67.72), (28.82, 67.72), (28.82, 29.41), (36.72, 29.41)], style=Icon.fill_style('#B1C2D2'))
polygon([(40.01, 54.49), (40.01, 10.49), (91.0, 10.49), (91.0, 29.26), (60.35, 29.26)], style=Icon.fill_style('#014372'))
save()
# fmt: on
