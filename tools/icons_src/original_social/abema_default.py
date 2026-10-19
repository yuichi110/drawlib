# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: abema (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=78.0,
    style=Icon.fill_style(Colors.Gray6, border_color=Icon.DARK, border_units=w, shape_r=16.0),
)
outer_a = [
    (21.0, 32.0),
    (31.5, 68.0),
    (41.5, 68.0),
    (52.0, 32.0),
    (43.5, 32.0),
    (41.2, 41.0),
    (31.8, 41.0),
    (29.5, 32.0),
]
hole_a = [(33.8, 48.5), (39.2, 48.5), (36.5, 58.5)]
polygon(outer_a, holes=[hole_a], style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
rectangle(
    (67.5, 64.0),
    width=21.0,
    height=8.0,
    style=Icon.fill_style(Colors.Red3, border_color=Icon.DARK, border_units=w * 0.8, shape_r=1.2),
)
rectangle(
    (67.5, 50.0),
    width=21.0,
    height=8.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8, shape_r=1.2),
)
rectangle(
    (67.5, 36.0),
    width=21.0,
    height=8.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8, shape_r=1.2),
)
save()
