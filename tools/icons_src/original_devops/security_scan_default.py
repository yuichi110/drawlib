# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: security_scan."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Heraldic security shield on the left/center
cx = 44.0
y_bottom, y_top = 18.0, 82.0
half_w = 26.0

left_pts = Icon.build_shield_half_points(cx, y_bottom, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bottom, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(left_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
polygon(right_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_segment((cx, y_bottom), (cx, y_top), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

# Overlapping magnifying glass on bottom-right
Icon.draw_round_segment((76.5, 27.5), (86.0, 18.0), width_units=4.5, color=Icon.DARK)
circle(
    (66.0, 38.0),
    radius=16.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)
circle(
    (66.0, 38.0),
    radius=10.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
