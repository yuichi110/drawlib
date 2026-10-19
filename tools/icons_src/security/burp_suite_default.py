# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: burp_suite (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(52.31, 91.0), (91.0, 91.0), (91.0, 9.0), (52.31, 9.0), (52.31, 13.8), (80.62, 41.93), (52.31, 41.93), (52.31, 64.16), (31.61, 64.16), (52.31, 85.04)], style=Icon.fill_style('#EB5E32'))
polygon([(9.0, 91.0), (48.59, 91.0), (48.59, 86.0), (20.98, 59.67), (48.59, 59.67), (48.59, 37.38), (71.14, 37.38), (48.59, 15.02), (48.59, 9.0), (9.0, 9.0)], style=Icon.fill_style('#303030'))
save()
# fmt: on
