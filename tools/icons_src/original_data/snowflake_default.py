# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: snowflake."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _rounded_diamond(
    cx: float,
    cy: float,
    side: float,
    r: float,
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Build a 45-degree rotated square (diamond) polygon with rounded corners."""
    d = side / math.sqrt(2.0)
    vertices = [
        (cx, cy + d),
        (cx - d, cy),
        (cx, cy - d),
        (cx + d, cy),
    ]
    n = len(vertices)
    pts: list[tuple[float, float]] = []
    for i in range(n):
        v_prev = vertices[(i - 1) % n]
        v_curr = vertices[i]
        v_next = vertices[(i + 1) % n]

        dx_in = v_prev[0] - v_curr[0]
        dy_in = v_prev[1] - v_curr[1]
        d_in = math.hypot(dx_in, dy_in)

        dx_out = v_next[0] - v_curr[0]
        dy_out = v_next[1] - v_curr[1]
        d_out = math.hypot(dx_out, dy_out)

        r_eff = min(r, d_in / 2.0, d_out / 2.0)
        p_in = (v_curr[0] + (dx_in / d_in) * r_eff, v_curr[1] + (dy_in / d_in) * r_eff)
        p_out = (v_curr[0] + (dx_out / d_out) * r_eff, v_curr[1] + (dy_out / d_out) * r_eff)

        for s in range(steps + 1):
            t = s / steps
            mt = 1.0 - t
            bx = (mt**2) * p_in[0] + 2.0 * mt * t * v_curr[0] + (t**2) * p_out[0]
            by = (mt**2) * p_in[1] + 2.0 * mt * t * v_curr[1] + (t**2) * p_out[1]
            pts.append((bx, by))
    return pts


def _chevron_branch_polygon(
    cx: float,
    cy: float,
    theta_deg: float,
    r_apex: float,
    arm_len: float,
    half_w: float,
) -> list[tuple[float, float]]:
    """Build exact rounded V-chevron polygon with parallel +-30 deg arms."""
    theta = math.radians(theta_deg)
    ux, uy = math.cos(theta), math.sin(theta)
    vx, vy = -uy, ux

    def _to_world(lx: float, ly: float) -> tuple[float, float]:
        return (cx + lx * ux + ly * vx, cy + lx * uy + ly * vy)

    c30 = math.cos(math.radians(30.0))
    s30 = math.sin(math.radians(30.0))

    tip_u = (r_apex + arm_len * c30, arm_len * s30)
    tip_l = (r_apex + arm_len * c30, -arm_len * s30)

    pts_local: list[tuple[float, float]] = []
    steps_arc = 14

    # 1. Inner nose arc around (r_apex, 0) from 240 deg through 180 deg to 120 deg
    for i in range(steps_arc + 1):
        ang = math.radians(240.0 - 120.0 * (i / steps_arc))
        pts_local.append((r_apex + half_w * math.cos(ang), half_w * math.sin(ang)))

    # 2. Upper arm (+30 deg) semicircular tip cap from 120 deg to -60 deg
    for i in range(steps_arc + 1):
        ang = math.radians(120.0 - 180.0 * (i / steps_arc))
        pts_local.append((tip_u[0] + half_w * math.cos(ang), tip_u[1] + half_w * math.sin(ang)))

    # 3. Inner V-valley vertex for +-30 deg arms: r_apex + half_w / sin(30 deg) = r_apex + 2 * half_w
    valley_x = r_apex + 2.0 * half_w
    pts_local.append((valley_x, 0.0))

    # 4. Lower arm (-30 deg) semicircular tip cap from +60 deg to -120 deg
    for i in range(steps_arc + 1):
        ang = math.radians(60.0 - 180.0 * (i / steps_arc))
        pts_local.append((tip_l[0] + half_w * math.cos(ang), tip_l[1] + half_w * math.sin(ang)))

    return [_to_world(lx, ly) for lx, ly in pts_local]


setup_icon()

w = 1.9
cx, cy = 50.0, 50.0

# 1. Six symmetrical V-chevron crystal branches at 0, 60, 120, 180, 240, 300 deg
for idx in range(6):
    theta_deg = idx * 60.0
    col = Colors.Teal3 if idx % 2 == 0 else Colors.Blue2
    branch_pts = _chevron_branch_polygon(
        cx=cx,
        cy=cy,
        theta_deg=theta_deg,
        r_apex=17.8,
        arm_len=19.5,
        half_w=4.3,
    )
    polygon(branch_pts, style=no_border_fill(col))
    draw_round_polyline(branch_pts, width_units=w, color=DARK, closed=True)

# 2. Center rounded diamond (Colors.Teal2) with transparent inner diamond hole
outer_diamond_pts = _rounded_diamond(cx, cy, side=14.8, r=2.6)
inner_diamond_pts = _rounded_diamond(cx, cy, side=6.0, r=1.0)
draw_compound_polygon([outer_diamond_pts, inner_diamond_pts], color=Colors.Teal2)
draw_round_polyline(outer_diamond_pts, width_units=w, color=DARK, closed=True)
draw_round_polyline(inner_diamond_pts, width_units=1.5, color=DARK, closed=True)

save()
