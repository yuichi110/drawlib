# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: live_streaming (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 44.0),
    width=74.0,
    height=52.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)
polygon(
    [(42.0, 55.0), (42.0, 33.0), (62.0, 44.0)],
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (30.0, 76.0),
    width=32.0,
    height=14.0,
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
circle((21.0, 76.0), radius=3.2, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.7))
arc(
    (68.0, 74.0),
    width=18.0,
    height=18.0,
    angle_start=20.0,
    angle_end=110.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w * 1.2),
)
arc(
    (68.0, 74.0),
    width=30.0,
    height=30.0,
    angle_start=20.0,
    angle_end=110.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w * 1.2),
)
save()
