# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: firewall."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx = 50.0
y_bot, y_top = 14.0, 86.0
half_w = 30.0

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

circle(
    (cx, 51.0),
    radius=16.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_polyline(
    [(42.0, 50.5), (48.0, 44.5), (59.0, 56.5)],
    width_units=3.4,
    color=Icon.PASTEL_GREEN,
)

save()
