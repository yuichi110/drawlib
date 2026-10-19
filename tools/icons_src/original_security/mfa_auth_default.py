# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: mfa_auth."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Vertical smartphone bezel (x=20..68, y=14..88)
rectangle(
    (44.0, 51.0),
    width=48.0,
    height=74.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_shape, shape_r=7.0),
)

# 2. Inner screen (x=26..62, y=22..78)
rectangle(
    (44.0, 50.0),
    width=36.0,
    height=56.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape, shape_r=3.5),
)

# 3. Top speaker line
Icon.draw_round_segment((39.0, 83.0), (49.0, 83.0), width_units=w_line, color=Icon.DARK)

# 4. Three DARK PIN dots across upper screen
for x_dot in (34.0, 44.0, 54.0):
    circle((x_dot, 65.0), radius=2.8, style=Icon.fill_style(Icon.DARK))

# 5. Bottom-right overlapping heraldic shield (cx=68, y_bot=12, y_top=54, half_w=18)
cx = 68.0
y_bot, y_top = 12.0, 54.0
half_w = 18.0

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(full_outline, width_units=w_shape, color=Icon.DARK, closed=True)

# 6. Inner WHITE circle and DARK checkmark
circle(
    (cx, 35.0),
    radius=8.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)
Icon.draw_round_polyline(
    [(64.2, 34.8), (67.2, 31.8), (72.0, 37.8)],
    width_units=w_line,
    color=Icon.DARK,
)

save()
