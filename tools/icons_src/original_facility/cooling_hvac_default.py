# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: cooling_hvac."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. HVAC cabinet unit on the left (WHITE body + PASTEL_BLUE top header)
# x=11..62, y=18..80
rectangle(
    (36.5, 49.0),
    width=51.0,
    height=62.0,
    style=no_border_fill(WHITE, shape_r=6.0),
)
draw_rounded_corner_block(
    11.0,
    68.0,
    62.0,
    80.0,
    r=6.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)
draw_round_segment((11.0, 68.0), (62.0, 68.0), width_units=w_inner, color=DARK)
rectangle(
    (36.5, 49.0),
    width=51.0,
    height=62.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w_outer, shape_r=6.0),
)

# Small control dots on top header bar
for dx in (19.0, 26.0):
    circle(
        (dx, 74.0),
        radius=2.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
    )

# 2. Circular fan shroud and 4 impeller blades inside HVAC body
fan_cx, fan_cy = 36.5, 43.0
circle(
    (fan_cx, fan_cy),
    radius=17.8,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner),
)

for k in range(4):
    base_ang = math.radians(k * 90.0 + 25.0)
    a1 = base_ang - 0.35
    a2 = base_ang + 0.35
    r_in = 4.0
    r_out = 14.6
    blade_pts = [
        (fan_cx + r_in * math.cos(a1), fan_cy + r_in * math.sin(a1)),
        (fan_cx + r_out * math.cos(a1 - 0.12), fan_cy + r_out * math.sin(a1 - 0.12)),
        (fan_cx + r_out * math.cos(a2 + 0.08), fan_cy + r_out * math.sin(a2 + 0.08)),
        (fan_cx + r_in * math.cos(a2), fan_cy + r_in * math.sin(a2)),
    ]
    polygon(blade_pts, style=no_border_fill(PASTEL_BLUE))
    draw_round_polyline(blade_pts, width_units=w_inner, color=DARK, closed=True)

circle(
    (fan_cx, fan_cy),
    radius=4.6,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
)

# 3. PASTEL_GREEN snowflake badge at top-right (clean clearance from x=62.0)
sf_cx, sf_cy = 77.0, 65.0
circle(
    (sf_cx, sf_cy),
    radius=11.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer),
)
for i in range(3):
    ang = math.radians(i * 60.0)
    dx = 7.0 * math.cos(ang)
    dy = 7.0 * math.sin(ang)
    draw_round_segment((sf_cx - dx, sf_cy - dy), (sf_cx + dx, sf_cy + dy), width_units=w_inner, color=DARK)

# 4. Two PASTEL_GREEN cool air waves flowing right (x=66.5..87.5)
for wy in (41.0, 28.0):
    wave_pts: list[tuple[float, float]] = []
    steps = 20
    for s in range(steps + 1):
        t = s / steps
        wx = 66.5 + 21.0 * t
        wy_val = wy + 3.0 * math.sin(t * 2.0 * math.pi)
        wave_pts.append((wx, wy_val))
    draw_round_polyline(wave_pts, width_units=5.4, color=DARK)
    draw_round_polyline(wave_pts, width_units=2.5, color=PASTEL_GREEN)

save()
