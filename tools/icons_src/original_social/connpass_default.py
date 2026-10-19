# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: connpass (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
circle((50.0, 50.0), radius=39.0, style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w))
circle((50.0, 50.0), radius=30.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
polygon(
    [(50.0, 76.0), (60.0, 50.0), (50.0, 55.0), (40.0, 50.0)],
    style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w * 0.8),
)
polygon(
    [(50.0, 24.0), (60.0, 50.0), (50.0, 45.0), (40.0, 50.0)],
    style=Icon.fill_style(Colors.Gray6, border_color=Icon.DARK, border_units=w * 0.8),
)
circle((50.0, 50.0), radius=4.2, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
save()
