# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: oidc."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# ID badge
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=58.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)
# User avatar on left
circle((33.0, 55.0), radius=9.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
arc(
    (33.0, 31.0),
    width=24.0,
    height=22.0,
    angle_start=0.0,
    angle_end=180.0,
    style=Icon.stroke_style(Icon.WHITE, width_units=w * 1.6),
)
# OpenID key ring on right
circle((66.0, 50.0), radius=13.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
circle((66.0, 50.0), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
save()
