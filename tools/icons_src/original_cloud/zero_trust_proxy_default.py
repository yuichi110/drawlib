# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: zero_trust_proxy."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Horizontal connection bar across gate pillars
Icon.draw_round_segment((26.0, 50.0), (74.0, 50.0), width_units=w, color=Icon.DARK)

# Left and right vertical gate pillars
rectangle(
    (20.0, 50.0),
    width=12.0,
    height=64.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
rectangle(
    (80.0, 50.0),
    width=12.0,
    height=64.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)

# Center verification shield
cx = 50.0
y_bot, y_top = 24.0, 76.0
half_w = 17.5

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

circle(
    (cx, 52.0),
    radius=8.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
