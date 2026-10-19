# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: influencer (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
circle((46.0, 50.0), radius=34.0, style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w))
circle((46.0, 58.0), radius=11.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
arc(
    (46.0, 28.0),
    width=34.0,
    height=28.0,
    angle_start=0.0,
    angle_end=180.0,
    style=Icon.stroke_style(Icon.DARK, width_units=w * 1.4),
)
# Verified / Star badge on bottom-right
circle((74.0, 28.0), radius=14.0, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
star_pts = [
    (74.0, 37.0),
    (76.5, 31.0),
    (83.0, 31.0),
    (77.8, 27.0),
    (79.8, 20.5),
    (74.0, 24.5),
    (68.2, 20.5),
    (70.2, 27.0),
    (65.0, 31.0),
    (71.5, 31.0),
]
polygon(star_pts, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.7))
save()
