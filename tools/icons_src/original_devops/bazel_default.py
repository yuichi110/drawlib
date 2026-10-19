# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps icon: bazel (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(30.0, 90.0), (50.0, 70.0), (30.0, 50.0), (10.0, 70.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(10.0, 70.0), (10.0, 50.0), (30.0, 30.0), (30.0, 50.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(70.0, 90.0), (90.0, 70.0), (70.0, 50.0), (50.0, 70.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(90.0, 70.0), (90.0, 50.0), (70.0, 30.0), (70.0, 50.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 70.0), (70.0, 50.0), (50.0, 30.0), (30.0, 50.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 30.0), (50.0, 10.0), (30.0, 30.0), (30.0, 50.0)], style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 30.0), (70.0, 50.0), (70.0, 30.0), (50.0, 10.0)], style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
