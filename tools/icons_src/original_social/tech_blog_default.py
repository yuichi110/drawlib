# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: tech_blog (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=68.0,
    height=78.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
rectangle(
    (50.0, 64.0),
    width=52.0,
    height=28.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
lines([(41.0, 70.0), (34.0, 64.0), (41.0, 58.0)], style=Icon.stroke_style(Icon.WHITE, width_units=w * 1.2))
lines([(59.0, 70.0), (66.0, 64.0), (59.0, 58.0)], style=Icon.stroke_style(Icon.WHITE, width_units=w * 1.2))
line((47.0, 57.0), (53.0, 71.0), style=Icon.stroke_style(Colors.Green3, width_units=w * 1.2))
line((26.0, 38.0), (74.0, 38.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.2))
line((26.0, 29.0), (74.0, 29.0), style=Icon.stroke_style(Icon.DARK, width_units=w))
line((26.0, 20.0), (56.0, 20.0), style=Icon.stroke_style(Icon.DARK, width_units=w))
save()
