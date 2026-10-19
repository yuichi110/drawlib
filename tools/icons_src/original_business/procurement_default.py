# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: procurement."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Purchase order sheet (x=14..70, y=18..86)
rectangle((42.0, 52.0), width=56.0, height=68.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=5.0))
Gcp.draw_rounded_corner_block(14.0, 72.0, 70.0, 86.0, r=5.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((14.0, 72.0), (70.0, 72.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (42.0, 52.0),
    width=56.0,
    height=68.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0),
)
for y_l in (60.0, 50.0, 40.0):
    Icon.draw_round_segment((22.0, y_l), (54.0, y_l), width_units=w_inner, color=Icon.DARK)

# 2. PASTEL_GREEN procurement cart badge at bottom-right
circle(
    (73.0, 30.0), radius=16.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
cart_pts = [(63.0, 37.0), (66.5, 37.0), (69.0, 27.0), (80.0, 27.0), (82.5, 34.5), (67.5, 34.5)]
Icon.draw_round_polyline(cart_pts, width_units=w_inner, color=Icon.DARK)
circle((70.5, 22.5), radius=2.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.2))
circle((78.5, 22.5), radius=2.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.2))
save()
