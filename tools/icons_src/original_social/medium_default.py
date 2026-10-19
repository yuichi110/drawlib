# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: medium (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=78.0,
    style=Icon.fill_style(Colors.Gray6, border_color=Icon.DARK, border_units=w, shape_r=16.0),
)
circle((35.0, 50.0), radius=15.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
ellipse(
    (61.5, 50.0),
    width=15.0,
    height=29.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)
ellipse(
    (75.5, 50.0),
    width=5.5,
    height=25.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8),
)
save()
