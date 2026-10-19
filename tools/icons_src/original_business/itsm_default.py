# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: itsm."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle, regularpolygon
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Monitor screen (x=13..81, y=28..82)
rectangle((47.0, 55.0), width=68.0, height=54.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=5.0))
Gcp.draw_rounded_corner_block(13.0, 69.0, 81.0, 82.0, r=5.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((13.0, 69.0), (81.0, 69.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (47.0, 55.0),
    width=68.0,
    height=54.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=5.0),
)
Icon.draw_round_segment((47.0, 28.0), (47.0, 18.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((34.0, 18.0), (60.0, 18.0), width_units=w_outer, color=Icon.DARK)

# 2. Service gear inside monitor (PASTEL_BLUE_LIGHT)
regularpolygon(
    (42.0, 48.0),
    radius=12.5,
    num_vertex=8,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.8),
)
circle((42.0, 48.0), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))

# 3. PASTEL_GREEN ticket/check badge at bottom-right
circle(
    (76.0, 29.0), radius=13.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_polyline([(70.5, 29.0), (74.5, 24.5), (82.0, 33.5)], width_units=w_outer, color=Icon.DARK)
save()
