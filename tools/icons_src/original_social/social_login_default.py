# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: social_login (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=56.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=9.0),
)
rectangle(
    (50.0, 63.0),
    width=62.0,
    height=16.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=5.0),
)
circle((30.0, 36.0), radius=8.5, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
circle((50.0, 36.0), radius=8.5, style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w))
circle((70.0, 36.0), radius=8.5, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))
save()
