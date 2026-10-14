# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: ddos_protection."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_cap,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Right-side heraldic shield
cx = 62.0
y_bot, y_top = 18.0, 82.0
half_w = 22.0

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(full_outline, width_units=w, color=DARK, closed=True)

circle(
    (cx, 51.0),
    radius=9.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)
circle(
    (cx, 51.0),
    radius=4.0,
    style=fill_style(PASTEL_GREEN),
)

# Vertical curved deflection barrier with round end caps
arc_cx, arc_cy = 52.0, 50.0
rx, ry = 21.0, 34.0
arc(
    (arc_cx, arc_cy),
    width=rx * 2.0,
    height=ry * 2.0,
    angle_start=125.0,
    angle_end=235.0,
    style=stroke_style(DARK, width_units=w),
)
for deg in (125.0, 235.0):
    rad = math.radians(deg)
    t = math.atan2(rx * math.sin(rad), ry * math.cos(rad))
    draw_cap((arc_cx + rx * math.cos(t), arc_cy + ry * math.sin(t)), width_units=w, color=DARK)

# 3 incoming horizontal attack arrows on the left
for y in (68.0, 50.0, 32.0):
    draw_round_segment((12.0, y), (27.0, y), width_units=w, color=DARK)
    draw_round_polyline(
        [(21.0, y + 5.0), (27.0, y), (21.0, y - 5.0)],
        width_units=w,
        color=DARK,
    )

save()
