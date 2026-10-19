# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI icon: replicate (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(90.0, 55.79), (90.0, 46.75), (58.27, 46.75), (58.27, 10.0), (48.16, 10.0), (48.16, 55.79)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(90.0, 90.0), (90.0, 80.94), (20.11, 80.94), (20.11, 10.0), (10.0, 10.0), (10.0, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(90.0, 72.9), (90.0, 63.84), (39.18, 63.84), (39.18, 10.0), (29.07, 10.0), (29.07, 72.9)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
