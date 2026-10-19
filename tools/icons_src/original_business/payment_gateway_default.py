# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: payment_gateway."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Credit card body (WHITE, x=11..81, y=28..78)
rectangle((46.0, 53.0), width=70.0, height=50.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0))
Gcp.draw_rounded_corner_block(11.0, 62.0, 81.0, 78.0, r=6.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((11.0, 62.0), (81.0, 62.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (46.0, 53.0),
    width=70.0,
    height=50.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)

# 2. EMV chip and card lines
rectangle(
    (25.0, 48.0),
    width=14.0,
    height=10.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0),
)
Icon.draw_round_segment((18.0, 36.5), (50.0, 36.5), width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN gateway shield/arrow badge at bottom-right
circle(
    (74.0, 29.0), radius=15.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((66.5, 29.0), (80.5, 29.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline([(75.0, 34.5), (81.0, 29.0), (75.0, 23.5)], width_units=w_outer, color=Icon.DARK)
save()
