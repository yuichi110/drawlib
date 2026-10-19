# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud icon: coolify (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(33.17, 66.83), (18.97, 66.83), (18.97, 24.2), (33.17, 24.2)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(33.17, 10.0), (90.0, 10.0), (90.0, 24.2), (33.17, 24.2)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(33.17, 66.83), (90.0, 66.83), (90.0, 81.03), (33.17, 81.03)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(28.68, 71.3), (14.48, 71.3), (14.48, 28.7), (28.68, 28.7)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(28.68, 14.49), (85.51, 14.49), (85.51, 28.7), (28.68, 28.7)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(28.68, 71.3), (85.51, 71.3), (85.51, 85.51), (28.68, 85.51)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(24.2, 75.8), (10.0, 75.8), (10.0, 33.17), (24.2, 33.17)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(24.2, 18.97), (81.03, 18.97), (81.03, 33.17), (24.2, 33.17)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(24.2, 75.8), (81.03, 75.8), (81.03, 90.0), (24.2, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
