# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: email_security."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 2.0

# 1. WHITE rounded mail envelope body: (45, 54), width=66, height=46, shape_r=5.0 -> x=12..78, y=31..77
x0, y0, x1, y1 = 12.0, 31.0, 78.0, 77.0
r = 5.0
rectangle(
    (45.0, 54.0),
    width=66.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=r),
)

# 2. Subtle DARK bottom corner fold lines
draw_round_segment((14.5, 33.5), (34.0, 51.0), width_units=2.0, color=DARK)
draw_round_segment((75.5, 33.5), (56.0, 51.0), width_units=2.0, color=DARK)

# 3. Top PASTEL_BLUE_LIGHT V-flap triangle ((13, 75) -> (45, 50) -> (77, 75))
#    Follows the rounded top corners from (13, 75) over y=77 to (77, 75) for a flush edge.
flap_pts: list[tuple[float, float]] = []
steps = 12
start_left = math.degrees(math.atan2(75.0 - (y1 - r), 13.0 - (x0 + r)))
for i in range(steps + 1):
    ang = math.radians(start_left - (start_left - 90.0) * (i / steps))
    flap_pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
end_right = math.degrees(math.atan2(75.0 - (y1 - r), 77.0 - (x1 - r)))
for i in range(steps + 1):
    ang = math.radians(90.0 - (90.0 - end_right) * (i / steps))
    flap_pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
flap_pts.append((45.0, 50.0))

polygon(flap_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(flap_pts, width_units=w_shape, color=DARK, closed=True)

# 4. Bottom-right overlapping PASTEL_GREEN shield (cx=70, y_bot=12, y_top=56, half_w=18)
cx = 70.0
y_bot, y_top = 12.0, 56.0
half_w = 18.0
left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
shield_pts = left_pts + list(reversed(right_pts[1:-1]))

polygon(shield_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(shield_pts, width_units=w_shape, color=DARK, closed=True)

# 5. WHITE circle (r=7.5) and DARK checkmark (w_line=2.5)
circle(
    (cx, 36.0),
    radius=7.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)
draw_round_polyline(
    [(66.3, 35.8), (69.1, 33.0), (74.0, 39.2)],
    width_units=2.0,
    color=DARK,
)

save()
