# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: customer_data_platform."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Database cylinder body (PASTEL_BLUE, x=20..72, y=20..76)
rectangle((46.0, 48.0), width=52.0, height=44.0, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
ellipse(
    (46.0, 26.0),
    width=52.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer),
)
ellipse(
    (46.0, 70.0),
    width=52.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer),
)
Icon.draw_round_segment((20.0, 26.0), (20.0, 70.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_segment((72.0, 26.0), (72.0, 70.0), width_units=w_outer, color=Icon.DARK)

# 2. User avatar on cylinder front (WHITE)
circle((46.0, 50.0), radius=6.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
dome_pts = [
    (46.0 + 11.0 * math.cos(math.radians(a)), 32.5 + 9.5 * math.sin(math.radians(a))) for a in range(0, 181, 10)
]
polygon(dome_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(dome_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 3. Connected data node badge at bottom-right (PASTEL_GREEN)
circle(
    (77.0, 28.0), radius=12.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
)
circle((77.0, 28.0), radius=4.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))
save()
