# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps icon: honeycomb (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(26.79, 48.94), (32.39, 39.27), (26.79, 29.57), (15.61, 29.57), (10.0, 39.27), (15.61, 48.94)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(50.64, 66.37), (57.46, 54.57), (50.64, 42.78), (37.05, 42.78), (30.23, 54.58), (37.05, 66.37)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(50.4, 35.83), (57.19, 24.04), (50.4, 12.25), (36.78, 12.25), (29.96, 24.04), (36.78, 35.83)], style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8))
polygon([(81.04, 87.75), (90.0, 72.23), (81.04, 56.69), (63.09, 56.69), (54.12, 72.23), (63.09, 87.75)], style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
