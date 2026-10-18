# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: grafana."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0
r_base = 30.5
r_outer = 41.5
num_fins = 7

# 7-fin spiral sun-gear outer contour
gear_pts: list[tuple[float, float]] = []
for k in range(num_fins):
    a_start = 90.0 + k * (360.0 / num_fins) - 20.0
    a_peak = a_start + 17.0
    a_end = a_start + 34.0
    a_next = 90.0 + (k + 1) * (360.0 / num_fins) - 20.0

    # Smooth curved fin rise
    steps_rise = 8
    for i in range(steps_rise):
        t = i / steps_rise
        ang = math.radians(a_start + t * (a_peak - a_start))
        rad = r_base + (r_outer - r_base) * math.sin(t * math.pi / 2.0)
        gear_pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))

    # Smooth curved fin fall
    steps_fall = 8
    for i in range(steps_fall + 1):
        t = i / steps_fall
        ang = math.radians(a_peak + t * (a_end - a_peak))
        rad = r_base + (r_outer - r_base) * math.cos(t * math.pi / 2.0)
        gear_pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))

    # Base valley arc to next fin
    steps_val = 6
    for i in range(1, steps_val):
        t = i / steps_val
        ang = math.radians(a_end + t * (a_next - a_end))
        gear_pts.append((cx + r_base * math.cos(ang), cy + r_base * math.sin(ang)))

r_hole = 25.5
hole_pts = [
    (cx + r_hole * math.cos(math.radians(360.0 * i / 64)), cy + r_hole * math.sin(math.radians(360.0 * i / 64)))
    for i in range(64)
]

draw_compound_polygon([gear_pts, hole_pts], color=PASTEL_BLUE)
draw_round_polyline(gear_pts, width_units=w, color=DARK, closed=True)
circle((cx, cy), radius=r_hole, style=stroke_style(DARK, width_units=2.0))

# Clean pastel green spiral coil inside the white circle (center fixed at 50.0, 49.0)
spiral_cx, spiral_cy = 50.0, 49.0
theta_start = math.radians(-100.0)
theta_end = math.radians(495.0)
steps_sp = 80

outer_wall: list[tuple[float, float]] = []
inner_wall: list[tuple[float, float]] = []

for i in range(steps_sp + 1):
    t = i / steps_sp
    th = theta_start + t * (theta_end - theta_start)
    # Center stays anchored at t=0; slight outer offset keeps left/right/top/bottom margins even
    cx_t = spiral_cx - 0.8 * t
    cy_t = spiral_cy - 0.8 * t
    r_mid = 3.0 + 15.2 * t
    half_thick = 2.0 + 0.8 * t
    ux, uy = math.cos(th), math.sin(th)
    outer_wall.append((cx_t + (r_mid + half_thick) * ux, cy_t + (r_mid + half_thick) * uy))
    inner_wall.append((cx_t + (r_mid - half_thick) * ux, cy_t + (r_mid - half_thick) * uy))

# Semicircular end caps for the spiral ribbon
cap_inner: list[tuple[float, float]] = []
c0_x = (outer_wall[0][0] + inner_wall[0][0]) / 2.0
c0_y = (outer_wall[0][1] + inner_wall[0][1]) / 2.0
r0 = math.hypot(outer_wall[0][0] - c0_x, outer_wall[0][1] - c0_y)
ang0 = math.atan2(inner_wall[0][1] - c0_y, inner_wall[0][0] - c0_x)
for i in range(1, 9):
    a = ang0 + math.pi * (i / 9)
    cap_inner.append((c0_x + r0 * math.cos(a), c0_y + r0 * math.sin(a)))

cap_outer: list[tuple[float, float]] = []
c1_x = (outer_wall[-1][0] + inner_wall[-1][0]) / 2.0
c1_y = (outer_wall[-1][1] + inner_wall[-1][1]) / 2.0
r1 = math.hypot(outer_wall[-1][0] - c1_x, outer_wall[-1][1] - c1_y)
ang1 = math.atan2(outer_wall[-1][1] - c1_y, outer_wall[-1][0] - c1_x)
for i in range(1, 9):
    a = ang1 + math.pi * (i / 9)
    cap_outer.append((c1_x + r1 * math.cos(a), c1_y + r1 * math.sin(a)))

spiral_poly = [*outer_wall, *cap_outer, *reversed(inner_wall), *cap_inner]
polygon(spiral_poly, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(spiral_poly, width_units=2.0, color=DARK, closed=True)

save()
