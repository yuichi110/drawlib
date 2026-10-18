# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: disaster_recovery."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, ellipse, polygon, rectangle
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
width = 32.0
w_half = width / 2.0
ry = 6.0
eh = ry * 2.0
tier_h = 14.5
tier_bottoms = [33.0, 47.5]
y_bot = tier_bottoms[0]
y_top = tier_bottoms[-1] + tier_h

# 1. Left primary database cylinder (PASTEL_BLUE)
cx_left = 30.0
for yb in tier_bottoms:
    ellipse(
        (cx_left, yb),
        width=width,
        height=eh,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx_left, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(PASTEL_BLUE),
    )

draw_round_segment((cx_left - w_half, y_bot), (cx_left - w_half, y_top), width_units=w, color=DARK)
draw_round_segment((cx_left + w_half, y_bot), (cx_left + w_half, y_top), width_units=w, color=DARK)

ellipse(
    (cx_left, y_top),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 2. Right standby recovery cylinder (PASTEL_GREEN)
cx_right = 70.0
for yb in tier_bottoms:
    ellipse(
        (cx_right, yb),
        width=width,
        height=eh,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx_right, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(PASTEL_GREEN),
    )

draw_round_segment((cx_right - w_half, y_bot), (cx_right - w_half, y_top), width_units=w, color=DARK)
draw_round_segment((cx_right + w_half, y_bot), (cx_right + w_half, y_top), width_units=w, color=DARK)

ellipse(
    (cx_right, y_top),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 3. Curved top failover arrow (from left primary to right standby)
arc_cx, arc_cy = 50.0, 71.0
arc_rx, arc_ry = 19.5, 13.5
ang_start, ang_end = 30.0, 158.0
arc(
    (arc_cx, arc_cy),
    width=arc_rx * 2.0,
    height=arc_ry * 2.0,
    angle_start=ang_start,
    angle_end=ang_end,
    style=stroke_style(DARK, width_units=w),
)

for deg in (ang_start, ang_end):
    rad = math.radians(deg)
    t_param = math.atan2(arc_rx * math.sin(rad), arc_ry * math.cos(rad))
    draw_cap((arc_cx + arc_rx * math.cos(t_param), arc_cy + arc_ry * math.sin(t_param)), width_units=w, color=DARK)

arrow_pts = [
    (61.5, 76.5),
    (70.5, 72.5),
    (71.0, 82.0),
]
polygon(arrow_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(arrow_pts, width_units=2.0, color=DARK, closed=True)

# 4. Bottom protective shield with heartbeat badge at (50, 26)
sh_cx = 50.0
sh_bot, sh_top = 12.0, 41.0
sh_half_w = 13.5

left_pts = build_shield_half_points(sh_cx, sh_bot, sh_top, sh_half_w, side="left")
right_pts = build_shield_half_points(sh_cx, sh_bot, sh_top, sh_half_w, side="right")
full_shield = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_shield, style=no_border_fill(WHITE))
draw_round_polyline(full_shield, width_units=w, color=DARK, closed=True)

heartbeat_pts = [
    (41.0, 26.5),
    (45.5, 26.5),
    (48.0, 33.0),
    (51.5, 20.0),
    (54.0, 26.5),
    (59.0, 26.5),
]
draw_round_polyline(heartbeat_pts, width_units=2.0, color=DARK)

save()
