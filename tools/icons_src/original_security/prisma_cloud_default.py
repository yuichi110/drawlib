# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: prisma_cloud (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 90.0), (85.64, 65.27), (50.0, 47.09)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 90.0), (14.36, 65.27), (50.0, 47.09)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(14.36, 65.27), (50.0, 47.09), (50.0, 10.0)], style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8))
polygon([(85.64, 65.27), (50.0, 47.09), (50.0, 10.0)], style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 74.0), (68.18, 60.91), (50.0, 28.91), (31.82, 60.91)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
