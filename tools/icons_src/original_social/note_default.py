# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: note (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

w = Icon.ORIG_STROKE
Icon.setup()
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=Icon.fill_style(Colors.Teal3, border_color=Icon.DARK, border_units=w, shape_r=18.0),
)
n_pts = [
    (29.0, 31.0),
    (29.0, 66.0),
    (40.0, 66.0),
    (40.0, 60.0),
    (44.0, 65.0),
    (50.0, 67.0),
    (57.0, 67.0),
    (64.0, 64.0),
    (68.0, 57.0),
    (68.0, 31.0),
    (57.0, 31.0),
    (57.0, 53.0),
    (55.0, 57.0),
    (50.0, 58.0),
    (44.0, 56.0),
    (40.0, 51.0),
    (40.0, 31.0),
]
polygon(n_pts, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
save()
