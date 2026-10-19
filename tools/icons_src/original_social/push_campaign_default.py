# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: push_campaign (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
polygon(
    [(22.0, 56.0), (62.0, 76.0), (62.0, 24.0), (22.0, 44.0)],
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (18.0, 50.0),
    width=10.0,
    height=18.0,
    style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w, shape_r=2.0),
)
rectangle(
    (28.0, 31.0),
    width=9.0,
    height=16.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=2.0),
)
circle((76.0, 66.0), radius=10.0, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
circle((78.0, 38.0), radius=8.0, style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w))
save()
