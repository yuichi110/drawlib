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
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Back/left web globe
gx, gy = 40.0, 56.0
gr = 26.0
circle(
    (gx, gy),
    radius=gr,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)
ellipse(
    (gx, gy),
    width=24.0,
    height=52.0,
    style=stroke_style(DARK, width_units=2.2),
)
draw_round_segment(
    (14.0, gy),
    (66.0, gy),
    width_units=2.2,
    color=DARK,
)

# Foreground bottom-right heraldic shield
cx = 64.0
y_bot, y_top = 16.0, 64.0
half_w = 20.0

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(full_outline, width_units=w, color=DARK, closed=True)

circle(
    (cx, 42.0),
    radius=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
