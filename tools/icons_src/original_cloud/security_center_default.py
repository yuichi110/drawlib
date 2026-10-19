# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: security_center."""

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

# Split shield: WHITE left half, PASTEL_BLUE right half
polygon(left_pts, style=Icon.no_border_fill(Icon.WHITE))
polygon(right_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_segment((cx, y_bot), (cx, y_top), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

# Central PASTEL_GREEN circular badge with DARK checkmark
circle(
    (cx, 52.0),
    radius=16.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_polyline(
    [(42.5, 51.5), (48.0, 46.0), (58.5, 57.5)],
    width_units=3.2,
    color=Icon.DARK,
)

save()
