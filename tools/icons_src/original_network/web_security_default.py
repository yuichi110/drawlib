# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: web_security."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Large 2D wireframe web globe
gx, gy = 44.0, 54.0
gr = 32.0

circle(
    (gx, gy),
    radius=gr,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)

# 2. Inner globe meridians and parallels
ellipse(
    (gx, gy),
    width=32.0,
    height=64.0,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)
Icon.draw_round_segment((gx, gy - gr), (gx, gy + gr), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((gx - gr, gy), (gx + gr, gy), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((gx - 28.7, 68.0), (gx + 28.7, 68.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((gx - 28.7, 40.0), (gx + 28.7, 40.0), width_units=2.0, color=Icon.DARK)

# Clean outer globe ring over line endpoints
circle(
    (gx, gy),
    radius=gr,
    style=Icon.stroke_style(Icon.DARK, width_units=w),
)

# 3. Foreground bottom-right security shield
cx = 68.0
y_bot, y_top = 12.0, 56.0
half_w = 18.0

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

# 4. Inner WHITE badge circle with DARK checkmark
circle(
    (cx, 36.0),
    radius=7.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_polyline(
    [(64.3, 35.8), (67.1, 33.0), (72.0, 39.2)],
    width_units=2.0,
    color=Icon.DARK,
)

save()
