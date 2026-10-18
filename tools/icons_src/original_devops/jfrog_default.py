# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: jfrog."""

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


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 18,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve from p0 to p3 (excluding p0)."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        by = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((bx, by))
    return pts


def _oval_pts(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    angle_deg: float = 0.0,
    steps: int = 28,
) -> list[tuple[float, float]]:
    """Sample a tilted oval droplet centered at (cx, cy)."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    pts: list[tuple[float, float]] = []
    for i in range(steps):
        a = 2.0 * math.pi * (i / steps)
        lx, ly = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + lx * ca - ly * sa, cy + lx * sa + ly * ca))
    return pts


def _crescent_ripple(
    cx: float,
    cy: float,
    rx_out: float,
    ry_out: float,
    rx_in: float,
    ry_in: float,
    deg_start: float,
    deg_end: float,
    *,
    dx_in: float = 0.0,
    dy_in: float = 0.0,
    steps: int = 36,
) -> list[tuple[float, float]]:
    """Build a smooth crescent ripple arc with rounded tips."""
    out_pts: list[tuple[float, float]] = []
    in_pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        out_pts.append((cx + rx_out * math.cos(ang), cy + ry_out * math.sin(ang)))
        in_pts.append((cx + dx_in + rx_in * math.cos(ang), cy + dy_in + ry_in * math.sin(ang)))

    p_oe = out_pts[-1]
    p_ie = in_pts[-1]
    cap_end: list[tuple[float, float]] = []
    mx_e, my_e = (p_oe[0] + p_ie[0]) / 2.0, (p_oe[1] + p_ie[1]) / 2.0
    vx_e, vy_e = (p_oe[0] - mx_e), (p_oe[1] - my_e)
    rad_e = math.radians(deg_end)
    tx_e, ty_e = -math.sin(rad_e), math.cos(rad_e)
    if deg_end < deg_start:
        tx_e, ty_e = -tx_e, -ty_e
    r_e = math.hypot(vx_e, vy_e)
    for k in range(1, 8):
        a = math.pi * (k / 8.0)
        ca, sa = math.cos(a), math.sin(a)
        cap_end.append((mx_e + vx_e * ca + tx_e * r_e * sa, my_e + vy_e * ca + ty_e * r_e * sa))

    p_os = out_pts[0]
    p_is = in_pts[0]
    cap_start: list[tuple[float, float]] = []
    mx_s, my_s = (p_os[0] + p_is[0]) / 2.0, (p_os[1] + p_is[1]) / 2.0
    vx_s, vy_s = (p_is[0] - mx_s), (p_is[1] - my_s)
    rad_s = math.radians(deg_start)
    tx_s, ty_s = math.sin(rad_s), -math.cos(rad_s)
    if deg_end < deg_start:
        tx_s, ty_s = -tx_s, -ty_s
    r_s = math.hypot(vx_s, vy_s)
    for k in range(1, 8):
        a = math.pi * (k / 8.0)
        ca, sa = math.cos(a), math.sin(a)
        cap_start.append((mx_s + vx_s * ca + tx_s * r_s * sa, my_s + vy_s * ca + ty_s * r_s * sa))

    return [*out_pts, *cap_end, *reversed(in_pts), *cap_start]


setup_icon()

w = 2.0

# 1. Three base ripple arcs with clean transparent separation
# Left small ripple crescent (Colors.Green2)
left_ripple = _crescent_ripple(
    cx=47.5,
    cy=44.5,
    rx_out=33.5,
    ry_out=11.0,
    rx_in=30.4,
    ry_in=9.4,
    deg_start=146.0,
    deg_end=204.0,
    dx_in=0.8,
    dy_in=0.2,
)

# Main wide front ripple crescent (Colors.Green3)
main_ripple = _crescent_ripple(
    cx=53.0,
    cy=44.0,
    rx_out=27.2,
    ry_out=11.8,
    rx_in=24.2,
    ry_in=8.6,
    deg_start=192.0,
    deg_end=348.0,
    dy_in=1.0,
)

# Right outer ripple crescent (Colors.Green2)
right_ripple = _crescent_ripple(
    cx=53.5,
    cy=42.2,
    rx_out=35.0,
    ry_out=15.0,
    rx_in=32.0,
    ry_in=13.0,
    deg_start=304.0,
    deg_end=356.0,
    dx_in=-0.5,
    dy_in=0.3,
)

# 2. Back splash crown rim (Colors.Green2, behind hollow bowl)
p_b0 = (33.5, 53.5)
back_crown: list[tuple[float, float]] = [
    p_b0,
    *_bezier(p_b0, (34.5, 58.0), (29.2, 62.5), (30.5, 65.8)),
    *_bezier((30.5, 65.8), (31.2, 67.5), (33.0, 67.2), (33.8, 65.2)),
    *_bezier((33.8, 65.2), (37.5, 58.5), (53.5, 59.0), (56.2, 65.2)),
    *_bezier((56.2, 65.2), (57.0, 67.4), (59.2, 67.4), (59.6, 65.0)),
    *_bezier((59.6, 65.0), (60.8, 57.5), (72.0, 56.5), (79.5, 63.8)),
    *_bezier((79.5, 63.8), (81.5, 65.8), (83.5, 64.5), (81.8, 62.5)),
    *_bezier((81.8, 62.5), (76.5, 56.5), (71.5, 52.5), (63.5, 53.5)),
    *_bezier((63.5, 53.5), (54.0, 55.0), (42.0, 55.5), p_b0),
]

# 3. Front splash crown body (Colors.Green3)
p_f0 = (37.0, 42.5)
front_crown: list[tuple[float, float]] = [
    p_f0,
    *_bezier(p_f0, (31.2, 47.8), (24.5, 56.5), (17.2, 63.5)),
    *_bezier((17.2, 63.5), (15.0, 65.5), (16.5, 68.0), (19.2, 66.0)),
    *_bezier((19.2, 66.0), (23.0, 63.0), (26.0, 58.2), (28.5, 58.8)),
    *_bezier((28.5, 58.8), (30.2, 59.2), (31.0, 57.5), (34.5, 52.0)),
    *_bezier((34.5, 52.0), (39.5, 45.4), (48.5, 45.4), (55.5, 49.0)),
    *_bezier((55.5, 49.0), (58.5, 50.6), (62.0, 47.6), (69.5, 50.0)),
    *_bezier((69.5, 50.0), (74.0, 51.5), (77.0, 54.5), (78.8, 57.0)),
    *_bezier((78.8, 57.0), (80.5, 59.0), (82.8, 57.2), (80.8, 55.0)),
    *_bezier((80.8, 55.0), (76.5, 50.5), (74.2, 46.2), (71.0, 42.2)),
    *_bezier((71.0, 42.2), (64.5, 37.2), (43.5, 37.2), p_f0),
]

# 4. Splash droplets floating cleanly in free space
droplets = [
    (_oval_pts(12.8, 70.4, 2.4, 1.7, -32.0), Colors.Green3),
    (_oval_pts(27.8, 71.2, 1.8, 1.4, 20.0), Colors.Green2),
    (_oval_pts(24.6, 65.8, 1.4, 1.2, 0.0), Colors.Green2),
    (_oval_pts(58.0, 71.5, 1.5, 1.9, 0.0), Colors.Green2),
    (_oval_pts(85.8, 69.2, 2.2, 1.7, 35.0), Colors.Green3),
    (_oval_pts(85.5, 59.0, 1.6, 1.4, 15.0), Colors.Green2),
]

shapes_list = [
    (left_ripple, Colors.Green2),
    (right_ripple, Colors.Green2),
    (main_ripple, Colors.Green3),
    (back_crown, Colors.Green2),
    (front_crown, Colors.Green3),
    *droplets,
]

for pts, col in shapes_list:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
