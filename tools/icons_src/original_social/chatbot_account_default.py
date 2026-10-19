# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: chatbot_account (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
line((50.0, 72.0), (50.0, 84.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.3))
circle((50.0, 86.0), radius=4.5, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
rectangle(
    (50.0, 48.0),
    width=64.0,
    height=46.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=10.0),
)
polygon(
    [(28.0, 25.0), (20.0, 13.0), (40.0, 25.0)],
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (50.0, 48.0),
    width=46.0,
    height=28.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
circle((40.0, 50.0), radius=4.2, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w * 0.8))
circle((60.0, 50.0), radius=4.2, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w * 0.8))
save()
