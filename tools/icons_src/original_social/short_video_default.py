# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: short_video (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=50.0,
    height=80.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=9.0),
)
polygon(
    [(43.0, 62.0), (43.0, 38.0), (63.0, 50.0)],
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)
circle((67.0, 42.0), radius=3.5, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w * 0.7))
circle((67.0, 31.0), radius=3.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.7))
circle(
    (67.0, 20.0),
    radius=3.5,
    style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w * 0.7),
)
save()
