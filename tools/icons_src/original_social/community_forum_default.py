# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: community_forum (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (40.0, 62.0),
    width=52.0,
    height=34.0,
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
polygon(
    [(22.0, 45.0), (18.0, 33.0), (32.0, 45.0)],
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (62.0, 38.0),
    width=48.0,
    height=32.0,
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)
polygon(
    [(78.0, 22.0), (84.0, 12.0), (68.0, 22.0)],
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w),
)
save()
