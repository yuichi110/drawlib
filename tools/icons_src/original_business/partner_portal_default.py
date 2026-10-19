# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: partner_portal."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Portal window frame (x=12..88, y=18..82)
rectangle((50.0, 50.0), width=76.0, height=64.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0))
Gcp.draw_rounded_corner_block(12.0, 68.0, 88.0, 82.0, r=6.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((12.0, 68.0), (88.0, 68.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)

# 2. Overlapping partner rings inside portal
circle(
    (41.0, 43.0),
    radius=15.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer),
)
circle(
    (59.0, 43.0), radius=15.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
circle((50.0, 43.0), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
save()
