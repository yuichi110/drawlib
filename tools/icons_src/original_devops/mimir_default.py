# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps icon: mimir (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 90.0), (85.56, 69.63), (50.0, 49.26), (14.44, 69.63)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(14.44, 69.63), (50.0, 49.26), (50.0, 10.0), (14.44, 30.37)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(85.56, 69.63), (85.56, 30.37), (50.0, 10.0), (50.0, 49.26)], style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8))
Icon.draw_round_polyline([(26.3, 52.22), (38.15, 61.11), (50.0, 47.04), (61.85, 61.11), (73.7, 52.22)], width_units=5.04, color=Icon.DARK)
save()
# fmt: on
