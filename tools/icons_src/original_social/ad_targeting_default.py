# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: ad_targeting (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
circle((46.0, 46.0), radius=34.0, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))
circle((46.0, 46.0), radius=22.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
circle((46.0, 46.0), radius=10.0, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
line((46.0, 46.0), (82.0, 82.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.4))
polygon(
    [(72.0, 84.0), (86.0, 86.0), (84.0, 72.0)],
    style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w),
)
save()
