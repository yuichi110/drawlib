# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: loyalty_points."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Loyalty card body (x=12..78, y=24..78)
rectangle((45.0, 51.0), width=66.0, height=54.0, style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0))
Gcp.draw_rounded_corner_block(12.0, 63.0, 78.0, 78.0, r=6.0, round_tl=True, round_tr=True, color=Icon.PASTEL_BLUE)
Icon.draw_round_segment((12.0, 63.0), (78.0, 63.0), width_units=w_outer, color=Icon.DARK)
rectangle(
    (45.0, 51.0),
    width=66.0,
    height=54.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)

# 2. Stamp circles on card
for sx in (26.0, 42.0):
    circle(
        (sx, 44.0),
        radius=5.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
    )

# 3. PASTEL_GREEN 5-pointed star badge at bottom-right
star_pts: list[tuple[float, float]] = []
for i in range(10):
    ang = math.radians(90.0 + i * 36.0)
    r = 16.5 if i % 2 == 0 else 7.2
    star_pts.append((72.0 + r * math.cos(ang), 30.0 + r * math.sin(ang)))
polygon(star_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(star_pts, width_units=w_outer, color=Icon.DARK, closed=True)
save()
