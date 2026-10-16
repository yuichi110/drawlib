# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: ids_ips."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_cisco_arrow,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Outer 1U horizontal rack appliance body
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=52.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)

# 2. Inner WHITE front panel
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=40.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.1, shape_r=5.0),
)

# 3. Left status LEDs on the panel
for y_led in (56.0, 44.0):
    circle(
        (24.0, y_led),
        radius=2.6,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

# 4. Long bidirectional traffic arrows spanning across the panel
# Top arrow: left -> right (--- | shield | -->)
draw_cisco_arrow(
    (32.0, 56.0),
    (78.5, 56.0),
    shaft_w=2.8,
    head_len=5.6,
    head_w=7.6,
    color=DARK,
)
# Bottom arrow: right -> left (<-- | shield | ---)
draw_cisco_arrow(
    (78.5, 44.0),
    (32.0, 44.0),
    shaft_w=2.8,
    head_len=5.6,
    head_w=7.6,
    color=DARK,
)

# 5. Central PASTEL_GREEN shield sitting across the middle of both arrows
cx = 55.25
y_bot, y_top = 34.5, 65.5
half_w = 11.8

left_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(full_outline, width_units=2.3, color=DARK, closed=True)

# 6. Almond eye symbol inside the central shield
ey = 51.2
eye_a = 7.6
eye_b = 4.4
arc_r = (eye_a * eye_a + eye_b * eye_b) / (2.0 * eye_b)
half_ang = math.asin(eye_a / arc_r)
steps = 20

eye_pts: list[tuple[float, float]] = []
yc_top = ey - (arc_r - eye_b)
for i in range(steps + 1):
    ang = (math.pi / 2.0 + half_ang) - (2.0 * half_ang) * (i / steps)
    eye_pts.append((cx + arc_r * math.cos(ang), yc_top + arc_r * math.sin(ang)))
yc_bot = ey + (arc_r - eye_b)
for i in range(1, steps):
    ang = (-math.pi / 2.0 + half_ang) - (2.0 * half_ang) * (i / steps)
    eye_pts.append((cx + arc_r * math.cos(ang), yc_bot + arc_r * math.sin(ang)))

polygon(eye_pts, style=no_border_fill(WHITE))
draw_round_polyline(eye_pts, width_units=1.9, color=DARK, closed=True)
circle((cx, ey), radius=2.3, style=fill_style(DARK))

save()
