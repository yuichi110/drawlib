# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud icon: xserver (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(68.17, 9.0), (89.24, 9.0), (72.15, 34.09), (57.28, 25.66)], style=Icon.fill_style('#000000'))
polygon([(60.66, 50.96), (88.06, 91.0), (67.35, 91.0), (50.12, 64.41), (33.01, 91.0), (11.94, 91.0), (39.34, 50.71), (21.76, 25.05), (62.51, 48.22)], style=Icon.fill_style('#000000'))
polygon([(62.51, 48.22), (21.76, 25.05), (10.76, 9.0), (31.26, 9.0), (49.77, 37.12), (57.28, 25.66), (72.15, 34.09)], style=Icon.fill_style('#1B5FA6'))
save()
# fmt: on
