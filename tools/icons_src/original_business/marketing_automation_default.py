# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: marketing_automation."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle, regularpolygon
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Megaphone handle (PASTEL_BLUE_LIGHT) and cone (PASTEL_BLUE)
rectangle(
    (26.0, 35.0),
    width=9.0,
    height=18.0,
    style=Icon.fill_style(
        Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0, angle=-18.0
    ),
)
cone_pts = [(22.0, 46.0), (62.0, 28.0), (62.0, 78.0), (22.0, 60.0)]
polygon(cone_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(cone_pts, width_units=w_outer, color=Icon.DARK, closed=True)
rectangle(
    (18.0, 53.0),
    width=8.0,
    height=18.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)

# 2. Broadcast wave arcs
for r_w in (10.0, 18.0):
    w_pts = [
        (64.0 + r_w * math.cos(math.radians(a)), 55.0 + r_w * math.sin(math.radians(a))) for a in range(-35, 36, 10)
    ]
    Icon.draw_round_polyline(w_pts, width_units=w_inner, color=Icon.DARK)

# 3. PASTEL_GREEN automation gear badge at bottom-right
regularpolygon(
    (74.0, 26.0),
    radius=13.5,
    num_vertex=8,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer, shape_r=2.0),
)
circle((74.0, 26.0), radius=5.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
save()
