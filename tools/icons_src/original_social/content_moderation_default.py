# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social concept icon: content_moderation (default variant)."""

from drawlib.canvas import save
from drawlib.lines import lines
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
shield_pts = [(50.0, 86.0), (82.0, 72.0), (78.0, 38.0), (50.0, 14.0), (22.0, 38.0), (18.0, 72.0)]
polygon(shield_pts, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))
inner_pts = [(50.0, 76.0), (72.0, 65.0), (69.0, 41.0), (50.0, 24.0), (31.0, 41.0), (28.0, 65.0)]
polygon(inner_pts, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.9))
lines([(39.0, 50.0), (47.0, 41.0), (63.0, 59.0)], style=Icon.stroke_style(Colors.Green3, width_units=w * 2.0))
save()
