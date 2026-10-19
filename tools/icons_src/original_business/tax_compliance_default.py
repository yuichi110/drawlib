# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: tax_compliance."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Tax document sheet (x=15..73, y=16..86)
rectangle((44.0, 51.0), width=58.0, height=70.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=5.0))
Gcp.draw_rounded_corner_block(15.0, 72.0, 73.0, 86.0, r=5.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((15.0, 72.0), (73.0, 72.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (44.0, 51.0),
    width=58.0,
    height=70.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0),
)

# 2. Percentage (%) symbol inside document
Icon.draw_round_segment((30.0, 36.0), (54.0, 60.0), width_units=w_outer, color=Icon.DARK)
circle(
    (33.5, 56.5),
    radius=4.8,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)
circle(
    (50.5, 39.5),
    radius=4.8,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)

# 3. PASTEL_GREEN compliance shield with checkmark
shield_pts = [(61.0, 40.0), (75.0, 44.0), (89.0, 40.0), (89.0, 26.0), (75.0, 14.0), (61.0, 26.0)]
polygon(shield_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(shield_pts, width_units=w_outer, color=Icon.DARK, closed=True)
Icon.draw_round_polyline([(69.0, 29.0), (73.5, 24.0), (81.5, 34.0)], width_units=w_outer, color=Icon.DARK)
save()
