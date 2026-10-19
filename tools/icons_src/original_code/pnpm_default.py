# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: pnpm (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(10.0, 90.0), (10.0, 65.0), (35.0, 65.0), (35.0, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(37.5, 90.0), (37.5, 65.0), (62.5, 65.0), (62.5, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(65.0, 90.0), (65.0, 65.0), (90.0, 65.0), (90.0, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(65.0, 62.5), (65.0, 37.5), (90.0, 37.5), (90.0, 62.5)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(37.5, 62.5), (37.5, 37.5), (62.5, 37.5), (62.5, 62.5)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(10.0, 35.0), (10.0, 10.0), (35.0, 10.0), (35.0, 35.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(37.5, 35.0), (37.5, 10.0), (62.5, 10.0), (62.5, 35.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(65.0, 35.0), (65.0, 10.0), (90.0, 10.0), (90.0, 35.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
