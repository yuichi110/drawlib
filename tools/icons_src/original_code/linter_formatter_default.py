# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: linter_formatter."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

b = 2.0

# WHITE code panel
rectangle(
    (45.0, 50.0),
    width=62.0,
    height=66.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=b, shape_r=5.0),
)

# 4 horizontal pill bars (neatly left-indented)
bars = [
    (35.0, 70.0, 26.0, Icon.PASTEL_BLUE),
    (45.0, 57.0, 30.0, Icon.PASTEL_BLUE_LIGHT),
    (42.0, 44.0, 24.0, Icon.PASTEL_BLUE_LIGHT),
    (34.0, 31.0, 24.0, Icon.PASTEL_BLUE),
]
for bx, by, bw, col in bars:
    rectangle(
        (bx, by),
        width=bw,
        height=7.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=b, shape_r=3.5),
    )

# Diagonal PASTEL_GREEN magic wand on the right with WHITE tip
x0, y0 = 83.0, 22.0
x1, y1 = 67.0, 68.0
dx, dy = x1 - x0, y1 - y0
length = math.hypot(dx, dy)
ux, uy = dx / length, dy / length
nx, ny = -uy * 3.8, ux * 3.8

xm, ym = x0 + 0.76 * dx, y0 + 0.76 * dy

shaft_pts = [
    (x0 - nx, y0 - ny),
    (x0 + nx, y0 + ny),
    (xm + nx, ym + ny),
    (xm - nx, ym - ny),
]
tip_pts = [
    (xm - nx, ym - ny),
    (xm + nx, ym + ny),
    (x1 + nx, y1 + ny),
    (x1 - nx, y1 - ny),
]

polygon(shaft_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(shaft_pts, width_units=b, color=Icon.DARK, closed=True)
polygon(tip_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(tip_pts, width_units=b, color=Icon.DARK, closed=True)

# 2 small 4-point star sparkles near wand tip
for sx, sy, sr_out, sr_in, scol in (
    (62.0, 74.5, 5.2, 1.8, Icon.PASTEL_GREEN),
    (83.5, 67.5, 5.2, 1.8, Icon.PASTEL_BLUE_LIGHT),
):
    sp_pts = Icon.build_sparkle_4pt_polygon(sx, sy, outer_r=sr_out, inner_r=sr_in)
    polygon(sp_pts, style=Icon.no_border_fill(scol))
    Icon.draw_round_polyline(sp_pts, width_units=b, color=Icon.DARK, closed=True)

save()
