# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: logistics_shipping."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
w_outer, w_inner = 2.0, 1.6

# 1. Cargo box (PASTEL_BLUE, x=12..60, y=32..74)
rectangle(
    (36.0, 53.0),
    width=48.0,
    height=42.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)

# 2. Truck cab (PASTEL_BLUE_LIGHT, x=60..88, y=32..62)
cab_pts = [(60.0, 32.0), (88.0, 32.0), (88.0, 48.0), (78.0, 62.0), (60.0, 62.0)]
polygon(cab_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(cab_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. Cab window (WHITE)
win_pts = [(65.0, 48.0), (82.0, 48.0), (75.0, 57.5), (65.0, 57.5)]
polygon(win_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(win_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 4. Wheels (DARK outer, WHITE hub)
for wx in (28.0, 74.0):
    circle(
        (wx, 28.0), radius=8.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer)
    )
    circle((wx, 28.0), radius=3.2, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner))

# 5. Speed lines on cargo box
Icon.draw_round_segment((20.0, 58.0), (46.0, 58.0), width_units=w_inner, color=Icon.WHITE)
Icon.draw_round_segment((20.0, 49.0), (38.0, 49.0), width_units=w_inner, color=Icon.WHITE)
save()
