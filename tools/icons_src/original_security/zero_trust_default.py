# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: zero_trust."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Main PASTEL_BLUE shield on left/center
sh_cx = 44.0
y_bot, y_top = 14.0, 86.0
half_w = 30.0
left_pts = Icon.build_shield_half_points(sh_cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(sh_cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))
polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(full_outline, width_units=w_shape, color=Icon.DARK, closed=True)

# 2. Inner WHITE circle with user silhouette inside shield
circle(
    (sh_cx, 54.0),
    radius=17.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)

user_scale = 0.92
user_cy = 53.0
head_r = 7.0 * user_scale
head_cy = user_cy + 6.5 * user_scale
circle(
    (sh_cx, head_cy),
    radius=head_r,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_shape),
)

sh_w = 24.0 * user_scale
sh_h = 13.0 * user_scale
sh_bot = user_cy - 11.5 * user_scale
shoulder_pts: list[tuple[float, float]] = []
for i in range(25):
    ang = math.pi * (1.0 - i / 24.0)
    px = sh_cx + (sh_w / 2.0) * math.cos(ang)
    py = sh_bot + sh_h * math.sin(ang)
    shoulder_pts.append((px, py))
polygon(shoulder_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(shoulder_pts, width_units=w_shape, color=Icon.DARK, closed=True)

# 3. Magnifying glass overlapping bottom-right inspecting the user
lx, ly = 65.0, 34.0
lens_outer_r = 15.5
lens_inner_r = 11.5
hx0 = lx + lens_outer_r * math.cos(math.radians(-45.0))
hy0 = ly + lens_outer_r * math.sin(math.radians(-45.0))
Icon.draw_round_segment((hx0, hy0), (87.0, 12.0), width_units=4.2, color=Icon.DARK)

circle(
    (lx, ly),
    radius=lens_outer_r,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)
circle(
    (lx, ly),
    radius=lens_inner_r,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape),
)

# 4. Checkmark inside magnifying glass lens
Icon.draw_round_polyline(
    [(lx - 4.8, ly - 0.3), (lx - 1.2, ly - 3.9), (lx + 5.2, ly + 3.6)],
    width_units=w_line,
    color=Icon.DARK,
)

save()
