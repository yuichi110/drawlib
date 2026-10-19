# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: contract_management."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Contract sheet (x=15..73, y=16..86)
rectangle((44.0, 51.0), width=58.0, height=70.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=5.0))
Gcp.draw_rounded_corner_block(15.0, 72.0, 73.0, 86.0, r=5.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((15.0, 72.0), (73.0, 72.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (44.0, 51.0),
    width=58.0,
    height=70.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0),
)

# 2. Clauses and signature line
for y_c in (61.0, 51.0, 41.0):
    Icon.draw_round_segment((24.0, y_c), (62.0, y_c), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((24.0, 28.0), (48.0, 28.0), width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN ribbon seal rosette at bottom-right
rib_l = [(69.0, 28.0), (65.0, 12.0), (71.5, 16.0), (74.0, 12.0), (74.0, 28.0)]
rib_r = [(75.0, 28.0), (75.0, 12.0), (77.5, 16.0), (84.0, 12.0), (80.0, 28.0)]
for r_pts in (rib_l, rib_r):
    polygon(r_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
    Icon.draw_round_polyline(r_pts, width_units=w_inner, color=Icon.DARK, closed=True)
circle(
    (74.5, 31.0), radius=12.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
circle((74.5, 31.0), radius=5.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
save()
