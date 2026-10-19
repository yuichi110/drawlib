# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: podcast_mic (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import arc, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 60.0),
    width=24.0,
    height=38.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=12.0),
)
arc(
    (50.0, 56.0),
    width=38.0,
    height=38.0,
    angle_start=180.0,
    angle_end=360.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w * 1.3),
)
line((50.0, 37.0), (50.0, 18.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.3))
rectangle(
    (50.0, 16.0),
    width=30.0,
    height=7.0,
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w, shape_r=3.0),
)
arc(
    (24.0, 60.0),
    width=18.0,
    height=30.0,
    angle_start=120.0,
    angle_end=240.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w * 1.1),
)
arc(
    (76.0, 60.0),
    width=18.0,
    height=30.0,
    angle_start=-60.0,
    angle_end=60.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w * 1.1),
)
save()
