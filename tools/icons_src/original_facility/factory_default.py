# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: factory."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Smokestack (rear left, x=19..31, y=50..84)
stack_pts = [
    (19.0, 50.0),
    (31.0, 50.0),
    (29.5, 81.0),
    (20.5, 81.0),
]
polygon(stack_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(stack_pts, width_units=w_outer, color=DARK, closed=True)

# Smokestack top collar band (PASTEL_BLUE)
rectangle(
    (25.0, 83.0),
    width=12.0,
    height=4.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=1.5),
)
draw_round_segment((20.8, 73.0), (29.2, 73.0), width_units=w_inner, color=DARK)

# 2. Main factory hall wall (WHITE, x=14..86, y=16..52)
rectangle(
    (50.0, 34.0),
    width=72.0,
    height=36.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)

# 3. Sawtooth industrial roof (3 teeth across x=14..86, y=52..68, PASTEL_BLUE)
for x0 in (14.0, 38.0, 62.0):
    tooth_pts = [
        (x0, 52.0),
        (x0 + 24.0, 68.0),
        (x0 + 24.0, 52.0),
    ]
    polygon(tooth_pts, style=no_border_fill(PASTEL_BLUE))
    draw_round_polyline(tooth_pts, width_units=w_outer, color=DARK, closed=True)

# 4. Left factory windows (2 industrial paned windows)
for wx in (25.0, 41.0):
    rectangle(
        (wx, 36.0),
        width=11.0,
        height=15.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.5),
    )
    draw_round_segment((wx - 5.5, 36.0), (wx + 5.5, 36.0), width_units=w_inner, color=DARK)
    draw_round_segment((wx, 28.5), (wx, 43.5), width_units=w_inner, color=DARK)

# 5. Foundation ground plinth
rectangle(
    (50.0, 14.5),
    width=78.0,
    height=4.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=1.5),
)

# 6. Foreground PASTEL_GREEN 8-tooth automation gear at (68.0, 34.0)
gx, gy = 68.0, 34.0
r_root = 11.2
r_tip = 15.2
n_teeth = 8
gear_pts: list[tuple[float, float]] = []
for i in range(n_teeth):
    base_deg = i * (360.0 / n_teeth)
    for offset_deg, rad in (
        (-13.0, r_root),
        (-8.0, r_tip),
        (8.0, r_tip),
        (13.0, r_root),
    ):
        ang = math.radians(base_deg + offset_deg)
        gear_pts.append((gx + rad * math.cos(ang), gy + rad * math.sin(ang)))

polygon(gear_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(gear_pts, width_units=w_outer, color=DARK, closed=True)
circle(
    (gx, gy),
    radius=5.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer),
)

save()
