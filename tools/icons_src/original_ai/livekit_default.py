# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI icon: livekit (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(74.0, 74.0), (58.0, 74.0), (58.0, 58.0), (74.0, 58.0), (74.0, 74.0)], holes=[[(58.0, 58.0), (42.0, 58.0), (42.0, 42.0), (58.0, 42.0)]], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(74.0, 42.0), (58.0, 42.0), (58.0, 26.0), (74.0, 26.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(90.0, 90.0), (74.0, 90.0), (74.0, 74.0), (90.0, 74.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(90.0, 26.0), (74.0, 26.0), (74.0, 10.0), (90.0, 10.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(26.0, 26.0), (26.0, 90.0), (10.0, 90.0), (10.0, 10.0), (58.0, 10.0), (58.0, 26.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
