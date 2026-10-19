# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: timeline_feed (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=68.0,
    height=78.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)
circle((30.0, 76.0), radius=5.5, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w * 0.9))
line((40.0, 78.0), (68.0, 78.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.1))
line((40.0, 73.0), (58.0, 73.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 0.9))
rectangle(
    (50.0, 51.0),
    width=54.0,
    height=28.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
circle((31.0, 26.0), radius=4.5, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w * 0.8))
circle(
    (45.0, 26.0),
    radius=4.5,
    style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w * 0.8),
)
line((56.0, 26.0), (74.0, 26.0), style=Icon.stroke_style(Icon.DARK, width_units=w))
save()
