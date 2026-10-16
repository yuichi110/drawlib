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
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)


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

# 2. Center rounded diamond (Colors.Teal2) + inner WHITE diamond core
rectangle(
    (cx, cy),
    width=14.8,
    height=14.8,
    style=fill_style(Colors.Teal2, border_color=DARK, border_units=w, shape_r=2.6, angle=45.0),
)
rectangle(
    (cx, cy),
    width=6.0,
    height=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=1.5, shape_r=1.0, angle=45.0),
)

save()
