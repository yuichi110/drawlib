# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: opnsense."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 4 interlocking L-bracket segments around a transparent center square (27.04..72.96)
top_seg = [
    (27.04, 91.0),
    (27.04, 72.96),
    (83.18, 72.96),
    (65.13, 91.0),
]

right_seg = [
    (72.96, 72.96),
    (72.96, 27.04),
    (91.0, 27.04),
    (91.0, 65.14),
    (83.18, 72.96),
]

bottom_seg = [
    (72.96, 9.0),
    (72.96, 27.04),
    (17.2, 27.04),
    (35.24, 9.0),
]

left_seg = [
    (27.04, 27.04),
    (27.04, 72.96),
    (9.0, 72.96),
    (9.0, 35.24),
    (17.2, 27.04),
]

for pts, col in [
    (top_seg, Colors.Orange3),
    (right_seg, Colors.Red3),
    (bottom_seg, Colors.Orange3),
    (left_seg, Colors.Red3),
]:
    polygon(pts, style=Icon.no_border_fill(col))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
