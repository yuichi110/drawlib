# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: openai."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cx, cy = 50.0, 50.0


def _rot(pt: tuple[float, float], deg: float) -> tuple[float, float]:
    """Rotate point around (50, 50) by deg degrees counter-clockwise."""
    rad = math.radians(deg)
    ca, sa = math.cos(rad), math.sin(rad)
    dx, dy = pt[0] - cx, pt[1] - cy
    return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)


def _rot_list(pts: list[tuple[float, float]], deg: float) -> list[tuple[float, float]]:
    return [_rot(p, deg) for p in pts]


# Exact 6-fold interlocking knot parameters
d = 10.4
s1 = 14.2
s2 = 19.5
r_arc = 17.5

r_hex = d / math.cos(math.radians(30.0))

# Base Petal 0 (top-right lobe, between 150-deg and 90-deg hexagon vertices)
v0 = (cx - d, cy + d * math.tan(math.radians(30.0)))
v1 = (cx, cy + r_hex)
e0 = (v0[0], v0[1] + s1)
p0 = (
    e0[0] + s2 * math.cos(math.radians(30.0)),
    e0[1] + s2 * math.sin(math.radians(30.0)),
)
c0 = (
    p0[0] + r_arc * math.cos(math.radians(-60.0)),
    p0[1] + r_arc * math.sin(math.radians(-60.0)),
)
e1 = _rot(e0, -60.0)

# Intersection of circle (c0, r_arc) with ray from e1 at -30 deg
ux = math.cos(math.radians(-30.0))
uy = math.sin(math.radians(-30.0))
dx_ce = e1[0] - c0[0]
dy_ce = e1[1] - c0[1]
b_proj = dx_ce * ux + dy_ce * uy
c_quad = dx_ce * dx_ce + dy_ce * dy_ce - r_arc * r_arc
t_hit = -b_proj + math.sqrt(max(0.0, b_proj * b_proj - c_quad))
q1 = (e1[0] + t_hit * ux, e1[1] + t_hit * uy)

ang_start = math.atan2(p0[1] - c0[1], p0[0] - c0[0])
ang_end = math.atan2(q1[1] - c0[1], q1[0] - c0[0])
if ang_end > ang_start:
    ang_end -= 2.0 * math.pi

arc_steps = 28
arc_pts: list[tuple[float, float]] = []
for i in range(1, arc_steps):
    ang = ang_start + (ang_end - ang_start) * (i / arc_steps)
    arc_pts.append((c0[0] + r_arc * math.cos(ang), c0[1] + r_arc * math.sin(ang)))

base_petal: list[tuple[float, float]] = [
    v0,
    e0,
    p0,
    *arc_pts,
    q1,
    e1,
    v1,
]

# 1. Central hollow hexagon (transparent cutout)
hex_pts = [_rot(v1, -k * 60.0) for k in range(6)]

# 2. Six interlocking knot petals in uniform Colors.Gray6
for k in range(6):
    pts = _rot_list(base_petal, -k * 60.0)
    polygon(pts, style=no_border_fill(Colors.Gray6))

# 3. Crisp w = 1.9 DARK borders on every loop petal and central hexagon
for k in range(6):
    pts = _rot_list(base_petal, -k * 60.0)
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

draw_round_polyline(hex_pts, width_units=w, color=DARK, closed=True)

save()
