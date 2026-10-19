# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: subscription_billing."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Calendar/subscription card (x=13..79, y=18..82)
rectangle((46.0, 50.0), width=66.0, height=64.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0))
Gcp.draw_rounded_corner_block(13.0, 66.0, 79.0, 82.0, r=6.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((13.0, 66.0), (79.0, 66.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (46.0, 50.0),
    width=66.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)
for rx in (28.0, 64.0):
    Icon.draw_round_segment((rx, 77.0), (rx, 87.0), width_units=w_outer, color=Icon.DARK)

# 2. Recurring cycle arc inside card
arc_pts = [
    (46.0 + 15.0 * math.cos(math.radians(a)), 43.0 + 15.0 * math.sin(math.radians(a))) for a in range(35, 315, 10)
]
Icon.draw_round_polyline(arc_pts, width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline([(54.0, 57.5), (58.5, 51.5), (51.5, 49.5)], width_units=w_outer, color=Icon.DARK)
circle(
    (46.0, 43.0),
    radius=6.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)

# 3. PASTEL_GREEN badge at bottom-right
circle(
    (74.5, 26.5), radius=13.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((74.5, 19.5), (74.5, 33.5), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((70.0, 26.5), (79.0, 26.5), width_units=w_inner, color=Icon.DARK)
save()
