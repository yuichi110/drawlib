# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: pnpm (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(9.0, 91.0), (9.0, 65.38), (34.62, 65.38), (34.62, 91.0)], style=Icon.fill_style('#F8AB00'))
polygon([(37.18, 91.0), (37.18, 65.38), (62.81, 65.38), (62.81, 91.0)], style=Icon.fill_style('#F8AB00'))
polygon([(65.38, 91.0), (65.38, 65.38), (91.0, 65.38), (91.0, 91.0)], style=Icon.fill_style('#F8AB00'))
polygon([(65.38, 62.81), (65.38, 37.19), (91.0, 37.19), (91.0, 62.81)], style=Icon.fill_style('#F8AB00'))
polygon([(37.18, 62.81), (37.18, 37.19), (62.81, 37.19), (62.81, 62.81)], style=Icon.fill_style('#4C4C4C'))
polygon([(9.0, 34.63), (9.0, 9.0), (34.62, 9.0), (34.62, 34.63)], style=Icon.fill_style('#4C4C4C'))
polygon([(37.18, 34.63), (37.18, 9.0), (62.81, 9.0), (62.81, 34.63)], style=Icon.fill_style('#4C4C4C'))
polygon([(65.38, 34.63), (65.38, 9.0), (91.0, 9.0), (91.0, 34.63)], style=Icon.fill_style('#4C4C4C'))
save()
# fmt: on
