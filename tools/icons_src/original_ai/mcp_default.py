# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: mcp."""

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

# 45-degree rotated basis centered at top-left arch C1
c1_x, c1_y = 55.8, 74.1
inv_s2 = 1.0 / math.sqrt(2.0)

r_arch = 10.8
hw = 2.75
r_out = r_arch + hw
r_in = r_arch - hw

l_leg = 31.8
u_left = -43.2
u_hook = -41.0
l_hook = 9.8
r_turn_in = 1.2
r_turn_out = r_turn_in + 2.0 * hw


def _uv(u: float, v: float) -> tuple[float, float]:
    """Convert rotated (u, v) coordinates around C1 to canvas (x, y)."""
    return (
        c1_x + (u + v) * inv_s2,
        c1_y + (u - v) * inv_s2,
    )


def _arc_uv(cu: float, cv: float, rad: float, deg0: float, deg1: float, steps: int = 20) -> list[tuple[float, float]]:
    """Sample circular arc in (u, v) plane from deg0 to deg1 (0 deg = +u, 90 deg = +v)."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(deg0 + (deg1 - deg0) * (i / steps))
        pts.append(_uv(cu + rad * math.cos(ang), cv + rad * math.sin(ang)))
    return pts


# 1. Outer double-arch + bottom hook ribbon (Colors.Gray6)
u_cusp = math.sqrt(r_out * r_out - r_arch * r_arch)
deg_cusp_c1 = math.degrees(math.atan2(r_arch, u_cusp))
deg_cusp_c3 = math.degrees(math.atan2(-r_arch, u_cusp))

c_turn_u = u_hook + hw + r_turn_in
c_turn_v = 3.0 * r_arch + hw + r_turn_in

outer_ribbon: list[tuple[float, float]] = [
    # Left end cap (at u = u_left, v = -r_arch)
    *_arc_uv(u_left, -r_arch, hw, 90.0, 270.0, 14),
    # Outer top-left leg up to C1 outer arch
    *_arc_uv(0.0, 0.0, r_out, -90.0, deg_cusp_c1, 22),
    # C3 outer arch around to v = 3*r_arch + hw (+90 deg)
    *_arc_uv(0.0, 2.0 * r_arch, r_out, deg_cusp_c3, 90.0, 22)[1:],
    # Down +v edge of right leg to inner 90-degree hook fillet
    *_arc_uv(c_turn_u, c_turn_v, r_turn_in, -90.0, -180.0, 8),
    # Hook end cap at (u_hook, 3*r_arch + l_hook)
    *_arc_uv(u_hook, 3.0 * r_arch + l_hook, hw, 0.0, 180.0, 14),
    # Outer 90-degree hook fillet back to -v edge of right leg
    *_arc_uv(c_turn_u, c_turn_v, r_turn_out, -180.0, -90.0, 12),
    # Up -v edge of right leg and around C3 inner arch
    *_arc_uv(0.0, 2.0 * r_arch, r_in, 90.0, -90.0, 22),
    # Down middle leg to inner round cap at (-l_leg, r_arch)
    *_arc_uv(-l_leg, r_arch, hw, 90.0, 270.0, 14),
    # Up middle leg and around C1 inner arch
    *_arc_uv(0.0, 0.0, r_in, 90.0, -90.0, 22),
]

polygon(outer_ribbon, style=no_border_fill(Colors.Gray6))
draw_round_polyline(outer_ribbon, width_units=w, color=DARK, closed=True)

# 2. Inner U-loop ribbon (Colors.Gray6)
inner_ribbon: list[tuple[float, float]] = [
    # Top-left cap at C1 center (0, 0) from +v (+90) to -v (-90)
    *_arc_uv(0.0, 0.0, hw, 90.0, -90.0, 14),
    # Down to C2 outer arch (centered at u = -l_leg, v = r_arch)
    *_arc_uv(-l_leg, r_arch, r_out, -90.0, -270.0, 26),
    # Up to top-right cap at C3 center (0, 2*r_arch) from +v (+90) to -v (-90)
    *_arc_uv(0.0, 2.0 * r_arch, hw, 90.0, -90.0, 14),
    # Down to C2 inner arch from +v (+90) through -u (180) to -v (270)
    *_arc_uv(-l_leg, r_arch, r_in, 90.0, 270.0, 22),
]

polygon(inner_ribbon, style=no_border_fill(Colors.Gray6))
draw_round_polyline(inner_ribbon, width_units=w, color=DARK, closed=True)

save()
