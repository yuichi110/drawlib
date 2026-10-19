# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: minio."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 20,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


Icon.setup()

w = 2.0

# 1. Lower standing leg tucked behind the wing crossbar (Colors.Pink3)
leg_pts = [
    (50.6, 43.5),
    (50.6, 16.5),
    (56.6, 10.5),
    (56.6, 46.2),
]
polygon(leg_pts, style=Icon.no_border_fill(Colors.Pink3))
Icon.draw_round_polyline(leg_pts, width_units=1.8, color=Icon.DARK, closed=True)

# 2. Pointed flamingo beak (WHITE with DARK tip border)
cx_h, cy_h = 53.6, 81.8
r_h_in = 2.8
r_h_out = 7.6
beak_ang = math.radians(42.0)

p_beak_bot = (cx_h + r_h_in * math.cos(beak_ang), cy_h + r_h_in * math.sin(beak_ang))
p_beak_top = (cx_h + r_h_out * math.cos(beak_ang), cy_h + r_h_out * math.sin(beak_ang))
beak_pts = [
    p_beak_bot,
    p_beak_top,
    (71.5, 68.8),
]
polygon(beak_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(beak_pts, width_units=1.8, color=Icon.DARK, closed=True)

# 3. Main continuous S-curve neck, head, upper wing, and crossbar (Colors.Red3)
p_wing_tip = (28.0, 30.2)
p_wing_top = (56.6, 65.5)
p_neck_low_in = (56.6, 50.0)
p_neck_mid_in = (59.6, 65.06)
p_neck_low_out = (59.4, 45.8)

# Outer head arc from 225 deg (bottom-left of head) CW over top (90 deg) to 42 deg (beak top)
head_out_arc: list[tuple[float, float]] = []
for i in range(19):
    ang = math.radians(225.0 - 183.0 * (i / 18.0))
    head_out_arc.append((cx_h + r_h_out * math.cos(ang), cy_h + r_h_out * math.sin(ang)))

# Inner head arc from 42 deg (beak bottom) CCW over top (90 deg) to 225 deg (bottom-left of head)
head_in_arc: list[tuple[float, float]] = []
for i in range(15):
    ang = math.radians(42.0 + 183.0 * (i / 14.0))
    head_in_arc.append((cx_h + r_h_in * math.cos(ang), cy_h + r_h_in * math.sin(ang)))

p_neck_mid_out = (63.0, 68.44)

body_pts = [
    p_wing_tip,
    *_bezier(p_wing_tip, (33.5, 48.0), (44.0, 59.5), p_wing_top, 22),
    p_neck_low_in,
    *_bezier(p_neck_low_in, (63.2, 53.5), (62.8, 61.86), p_neck_mid_in, 16),
    *head_out_arc,
    *head_in_arc,
    p_neck_mid_out,
    *_bezier(p_neck_mid_out, (67.8, 63.64), (68.8, 52.0), p_neck_low_out, 20),
    p_wing_tip,
]

# 4. Inner triangular wing cutout (transparent hole inside body_pts)
hole_pts = [
    (36.8, 39.8),
    *_bezier((36.8, 39.8), (40.5, 48.2), (45.5, 53.8), (50.6, 57.4), 14),
    (50.6, 47.0),
]
polygon(body_pts, holes=[hole_pts], style=Icon.fill_style(Colors.Red3))
Icon.draw_round_polyline(body_pts, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(hole_pts, width_units=1.7, color=Icon.DARK, closed=True)

save()
