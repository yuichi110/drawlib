# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: nicovideo (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
line((50.0, 66.0), (33.0, 84.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.8))
line((50.0, 66.0), (67.0, 84.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.8))
rectangle(
    (50.0, 44.0),
    width=76.0,
    height=48.0,
    style=Icon.fill_style(Colors.Gray6, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
polygon(
    [(26.0, 20.0), (34.0, 20.0), (31.5, 13.0), (28.5, 13.0)],
    style=Icon.fill_style(Colors.Gray5, border_color=Icon.DARK, border_units=w * 0.8),
)
polygon(
    [(66.0, 20.0), (74.0, 20.0), (71.5, 13.0), (68.5, 13.0)],
    style=Icon.fill_style(Colors.Gray5, border_color=Icon.DARK, border_units=w * 0.8),
)
rectangle(
    (50.0, 45.0),
    width=60.0,
    height=34.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
rectangle((38.0, 48.0), width=5.5, height=11.0, style=Icon.fill_style(Icon.DARK, shape_r=1.5))
rectangle((62.0, 48.0), width=5.5, height=11.0, style=Icon.fill_style(Icon.DARK, shape_r=1.5))
line((43.0, 35.0), (57.0, 35.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.4))
save()
