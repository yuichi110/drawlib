# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: notification_gateway."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Bell clapper and top ring
circle(
    (44.0, 82.0),
    radius=4.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner),
)
circle(
    (44.0, 22.0),
    radius=6.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer),
)

# 2. Bell dome (PASTEL_BLUE)
bell_pts: list[tuple[float, float]] = [(16.0, 28.0), (72.0, 28.0), (64.0, 38.0), (64.0, 56.0)]
for a in range(0, 181, 10):
    bell_pts.append((44.0 + 20.0 * math.cos(math.radians(a)), 56.0 + 22.0 * math.sin(math.radians(a))))
bell_pts.extend([(24.0, 38.0)])
polygon(bell_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(bell_pts, width_units=w_outer, color=Icon.DARK, closed=True)
rectangle(
    (44.0, 28.0),
    width=58.0,
    height=7.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0),
)

# 3. PASTEL_GREEN notification count/routing badge at top-right
circle(
    (73.0, 68.0), radius=14.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
Icon.draw_round_segment((67.0, 68.0), (79.0, 68.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_polyline([(74.5, 72.5), (79.5, 68.0), (74.5, 63.5)], width_units=w_inner, color=Icon.DARK)
save()
