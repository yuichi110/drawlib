# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: airbyte."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cx, cy = 57.5, 58.8

# Unit basis vectors for the -120 deg comet tail direction (u) and -30 deg normal (n)
ang_u = math.radians(-120.0)
ux, uy = math.cos(ang_u), math.sin(ang_u)
nx, ny = math.cos(math.radians(-30.0)), math.sin(math.radians(-30.0))


def _pt(d_n: float, s_u: float) -> tuple[float, float]:
    """Convert (normal offset d_n, tail distance s_u) around (cx, cy) to canvas (x, y)."""
    return (cx + d_n * nx + s_u * ux, cy + d_n * ny + s_u * uy)


def _arc_pts(r: float, deg_start: float, deg_end: float, steps: int) -> list[tuple[float, float]]:
    """Sample circular arc around (cx, cy) from deg_start to deg_end."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _round_tail_cap(d_left: float, d_right: float, s_end: float, steps: int = 14) -> list[tuple[float, float]]:
    """Build a smooth semicircular cap from left edge (d_left, s_end) to right edge (d_right, s_end)."""
    d_mid = 0.5 * (d_left + d_right)
    r_cap = 0.5 * abs(d_right - d_left)
    c_xy = _pt(d_mid, s_end)
    pts: list[tuple[float, float]] = []
    for i in range(1, steps):
        a = math.radians(150.0 + 180.0 * (i / steps))
        pts.append((c_xy[0] + r_cap * math.cos(a), c_xy[1] + r_cap * math.sin(a)))
    return pts


# Radii for concentric head & outer comet arch
r_hole = 4.0
r_head = 11.7
r_arch_in = 20.3
r_arch_out = 28.0
rib_w = r_arch_out - r_arch_in  # 7.7

# ------------------------------------------------------------------------------
# 1. Outer 3-legged comet arch (Colors.Purple3)
# ------------------------------------------------------------------------------
s_leg1_end = 33.0
s_crotch = math.sqrt(r_arch_out**2 - r_arch_in**2)  # ~19.29
deg_crotch = 150.0 + math.degrees(math.acos(r_arch_in / r_arch_out))  # ~193.5 deg

d_leg2_in = -5.1
d_leg2_out = d_leg2_in - rib_w  # -12.8
s_leg2_end = 45.2
deg_leg2_out = 150.0 + math.degrees(math.acos(abs(d_leg2_out) / r_arch_out))  # ~212.8 deg
deg_leg2_in = 150.0 + math.degrees(math.acos(abs(d_leg2_in) / r_arch_in))  # ~225.5 deg

# Leg 4 ends at the same horizontal baseline (y ~ 16.5) as Leg 3
s_leg4_end = 35.0

outer_pts: list[tuple[float, float]] = [
    _pt(-r_arch_out, 0.0),
    _pt(-r_arch_out, s_leg1_end),
    *_round_tail_cap(-r_arch_out, -r_arch_in, s_leg1_end),
    _pt(-r_arch_in, s_leg1_end),
    _pt(-r_arch_in, s_crotch),
    *_arc_pts(r_arch_out, deg_crotch, deg_leg2_out, 6)[1:],
    _pt(d_leg2_out, s_leg2_end),
    *_round_tail_cap(d_leg2_out, d_leg2_in, s_leg2_end),
    _pt(d_leg2_in, s_leg2_end),
    *_arc_pts(r_arch_in, deg_leg2_in, -30.0, 36),
    _pt(r_arch_in, s_leg4_end),
    *_round_tail_cap(r_arch_in, r_arch_out, s_leg4_end),
    _pt(r_arch_out, s_leg4_end),
    *_arc_pts(r_arch_out, -30.0, 150.0, 32),
]

polygon(outer_pts, style=no_border_fill(Colors.Purple3))
draw_round_polyline(outer_pts, width_units=w, color=DARK, closed=True)

# ------------------------------------------------------------------------------
# 2. Inner comet head + Leg 3 (Colors.Purple2)
# ------------------------------------------------------------------------------
s_leg3_end = 44.4
deg_leg3_join = -30.0 - math.degrees(math.acos(r_hole / r_head))

inner_pts: list[tuple[float, float]] = [
    _pt(r_hole, s_leg3_end),
    *_round_tail_cap(r_hole, r_head, s_leg3_end),
    _pt(r_head, s_leg3_end),
    *_arc_pts(r_head, -30.0, 360.0 + deg_leg3_join, 36),
]

polygon(inner_pts, style=no_border_fill(Colors.Purple2))
draw_round_polyline(inner_pts, width_units=w, color=DARK, closed=True)

# ------------------------------------------------------------------------------
# 3. Inner circular hole cutout (WHITE)
# ------------------------------------------------------------------------------
circle(
    (cx, cy),
    radius=r_hole,
    style=fill_style(WHITE, border_color=DARK, border_units=1.7),
)

save()
