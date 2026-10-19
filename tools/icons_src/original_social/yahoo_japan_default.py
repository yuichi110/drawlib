# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: yahoo_japan (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=78.0,
    style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w, shape_r=16.0),
)
polygon(
    [
        (19.0, 71.0),
        (31.0, 71.0),
        (42.5, 52.0),
        (54.0, 71.0),
        (66.0, 71.0),
        (48.0, 43.0),
        (48.0, 26.0),
        (37.0, 26.0),
        (37.0, 43.0),
    ],
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8),
)
polygon(
    [(70.0, 73.0), (82.0, 73.0), (78.5, 43.0), (71.5, 43.0)],
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8),
)
circle((75.0, 31.0), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
save()
