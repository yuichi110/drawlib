# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: viral_share (default variant)."""

from drawlib.canvas import save
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
line((24.0, 50.0), (72.0, 76.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.4))
line((24.0, 50.0), (72.0, 24.0), style=Icon.stroke_style(Icon.DARK, width_units=w * 1.4))
circle((24.0, 50.0), radius=13.0, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))
circle((72.0, 76.0), radius=12.0, style=Icon.fill_style(Colors.Green3, border_color=Icon.DARK, border_units=w))
circle((72.0, 24.0), radius=12.0, style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w))
circle((24.0, 50.0), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
circle((72.0, 76.0), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
circle((72.0, 24.0), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
save()
