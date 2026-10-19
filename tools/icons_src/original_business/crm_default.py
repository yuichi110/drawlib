# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: crm."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, heart, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Customer profile card (WHITE body, x=12.0..81.0, y=22.0..83.0)
rectangle(
    (46.5, 52.5),
    width=69.0,
    height=61.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.0),
)

# 2. Top PASTEL_BLUE header bar (y=69.5..83.0)
Gcp.draw_rounded_corner_block(
    12.0,
    69.5,
    81.0,
    83.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 3. Header divider and outer card border
Icon.draw_round_segment((12.0, 69.5), (81.0, 69.5), width_units=w_outer, color=Icon.DARK)
rectangle(
    (46.5, 52.5),
    width=69.0,
    height=61.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_outer, shape_r=6.0),
)

# 4. Header window dots
for x_dot in (20.0, 27.5):
    circle(
        (x_dot, 76.2),
        radius=2.1,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
    )

# 5. Left user avatar (PASTEL_BLUE_LIGHT head circle & shoulders dome)
circle(
    (30.5, 52.5),
    radius=6.8,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)
dome_pts = [
    (
        30.5 + 11.2 * math.cos(math.radians(deg)),
        33.0 + 10.2 * math.sin(math.radians(deg)),
    )
    for deg in range(0, 181, 6)
]
polygon(dome_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(dome_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 6. Customer info lines on right side of card
Icon.draw_round_segment((47.5, 56.0), (72.0, 56.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((47.5, 46.5), (67.0, 46.5), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((47.5, 37.0), (59.0, 37.0), width_units=w_inner, color=Icon.DARK)

# 7. PASTEL_GREEN heart badge at bottom-right
circle(
    (74.0, 26.5),
    radius=13.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)
heart(
    (74.0, 26.0),
    width=14.5,
    height=13.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)

save()
