# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: instagram (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=Icon.fill_style(Colors.Pink3, border_color=Icon.DARK, border_units=w, shape_r=20.0),
)
rectangle(
    (50.0, 50.0),
    width=52.0,
    height=52.0,
    style=Icon.fill_style(Colors.Pink2, border_color=Icon.DARK, border_units=w, shape_r=14.0),
)
circle((50.0, 50.0), radius=13.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
circle((64.0, 64.0), radius=4.2, style=Icon.fill_style(Colors.Amber2, border_color=Icon.DARK, border_units=w * 0.8))
save()
