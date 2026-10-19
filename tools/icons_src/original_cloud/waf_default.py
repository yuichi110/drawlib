# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: waf."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Back/left web globe
gx, gy = 40.0, 56.0
gr = 26.0
circle(
    (gx, gy),
    radius=gr,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)
ellipse(
    (gx, gy),
    width=24.0,
    height=52.0,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)
Icon.draw_round_segment(
    (14.0, gy),
    (66.0, gy),
    width_units=2.0,
    color=Icon.DARK,
)

# Foreground bottom-right heraldic shield
cx = 64.0
y_bot, y_top = 16.0, 64.0
half_w = 20.0

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

circle(
    (cx, 42.0),
    radius=6.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
