# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: cost_management."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Background analytics card: (44, 54), width=56, height=52, shape_r=6.0 -> x=16..72, y=28..80
rectangle(
    (44.0, 54.0),
    width=56.0,
    height=52.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)

# 3 bar chart columns inside the analytics card
bars = [
    (28.0, 18.0, Icon.PASTEL_BLUE_LIGHT),
    (41.5, 28.0, Icon.PASTEL_BLUE),
    (55.0, 36.0, Icon.PASTEL_BLUE),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, 35.0 + bh / 2.0),
        width=9.0,
        height=bh,
        style=Icon.fill_style(bcol, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
    )

# Bottom-right financial coin badge at (68, 34), radius=18.0 -> x=50..86, y=16..52
coin_cx, coin_cy = 68.0, 34.0
circle(
    (coin_cx, coin_cy),
    radius=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    (coin_cx, coin_cy),
    radius=13.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# Currency symbol (vertical bar + S-curve) inside coin
Icon.draw_round_segment((coin_cx, 24.5), (coin_cx, 43.5), width_units=2.0, color=Icon.DARK)

s_pts: list[tuple[float, float]] = []
rx, ry = 4.2, 3.2
# Upper loop of S from 30 deg to 270 deg around (coin_cx, coin_cy + ry)
for deg in range(35, 271, 15):
    rad = math.radians(deg)
    s_pts.append((coin_cx + rx * math.cos(rad), (coin_cy + ry) + ry * math.sin(rad)))
# Lower loop of S from 90 deg down to -145 deg around (coin_cx, coin_cy - ry)
for deg in range(90, -146, -15):
    rad = math.radians(deg)
    s_pts.append((coin_cx + rx * math.cos(rad), (coin_cy - ry) + ry * math.sin(rad)))

Icon.draw_round_polyline(s_pts, width_units=2.0, color=Icon.DARK)

save()
