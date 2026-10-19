# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: appsflyer (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
polygon(
    [(50.0, 86.0), (86.0, 64.0), (61.0, 48.0), (50.0, 63.0)],
    style=Icon.fill_style(Colors.Teal3, border_color=Icon.DARK, border_units=w),
)
polygon(
    [(50.0, 63.0), (61.0, 48.0), (82.0, 22.0), (46.0, 35.0)],
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w),
)
polygon(
    [(50.0, 86.0), (16.0, 52.0), (46.0, 35.0), (50.0, 63.0)],
    style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w),
)
polygon(
    [(46.0, 35.0), (26.0, 14.0), (54.0, 18.0)],
    style=Icon.fill_style(Colors.Green2, border_color=Icon.DARK, border_units=w),
)
save()
