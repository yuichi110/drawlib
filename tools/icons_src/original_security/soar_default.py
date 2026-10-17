# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: soar."""

import math

from drawlib.canvas import save
from drawlib.lines import lines
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
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

w_shape = 1.8
w_line = 2.7

# 1. Left PASTEL_BLUE heraldic shield
cx_s = 32.0
y_bot, y_top = 24.0, 76.0
half_w = 19.0
left_pts = build_shield_half_points(cx_s, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx_s, y_bot, y_top, half_w, side="right")
shield_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(shield_outline, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(shield_outline, width_units=w_shape, color=DARK, closed=True)

# 2. Orthogonal workflow branches from gear (67, 50) to 3 right-side playbook nodes
draw_round_polyline(
    [(75.0, 72.0), (71.0, 72.0), (71.0, 28.0), (75.0, 28.0)],
    width_units=w_line,
    color=DARK,
    corner_r=2.5,
)
draw_round_segment((67.0, 50.0), (75.0, 50.0), width_units=w_line, color=DARK)

# 3. 3 right-side WHITE rounded square playbook nodes
for y_node in (72.0, 50.0, 28.0):
    rectangle(
        (81.0, y_node),
        width=12.0,
        height=12.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=3.0),
    )

# 4. Central overlapping 8-tooth PASTEL_GREEN automation gear at (52, 50)
gx, gy = 52.0, 50.0
outer_r = 15.0
inner_r = 11.5
teeth = 8
step_deg = 360.0 / teeth
half_root = step_deg * 0.23
half_tip = step_deg * 0.145
gear_pts: list[tuple[float, float]] = []
corner_pts: list[tuple[float, float]] = []
arc_steps = 6

for i in range(teeth):
    center_deg = i * step_deg
    a_rl = math.radians(center_deg - half_root)
    a_tl = math.radians(center_deg - half_tip)
    a_tr = math.radians(center_deg + half_tip)
    a_rr = math.radians(center_deg + half_root)

    p_rl = (gx + inner_r * math.cos(a_rl), gy + inner_r * math.sin(a_rl))
    p_tl = (gx + outer_r * math.cos(a_tl), gy + outer_r * math.sin(a_tl))
    p_tr = (gx + outer_r * math.cos(a_tr), gy + outer_r * math.sin(a_tr))
    p_rr = (gx + inner_r * math.cos(a_rr), gy + inner_r * math.sin(a_rr))

    gear_pts.extend([p_rl, p_tl, p_tr, p_rr])
    corner_pts.extend([p_rl, p_tl, p_tr, p_rr])

    next_rl_deg = (i + 1) * step_deg - half_root
    start_valley_deg = center_deg + half_root
    for s in range(1, arc_steps):
        ang = math.radians(start_valley_deg + (next_rl_deg - start_valley_deg) * (s / arc_steps))
        gear_pts.append((gx + inner_r * math.cos(ang), gy + inner_r * math.sin(ang)))

polygon(gear_pts, style=no_border_fill(PASTEL_GREEN))
lines([*gear_pts, gear_pts[0]], style=stroke_style(DARK, width_units=w_shape))
for cp in corner_pts:
    draw_cap(cp, width_units=w_shape, color=DARK)

circle(
    (gx, gy),
    radius=5.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)

save()
