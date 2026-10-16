# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: helm."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0
r_ring_outer = 27.5
r_ring_inner = 18.0


def _build_handle_points(angle_deg: float) -> list[tuple[float, float]]:
    """Build a rounded bulbous ship's wheel handle from r=25.5 to r=40.5."""
    theta = math.radians(angle_deg)
    ux, uy = math.cos(theta), math.sin(theta)
    nx, ny = -uy, ux

    r_base = 25.5
    r_tip_center = 37.3
    r_tip = 3.2
    w_base = 2.1

    pts: list[tuple[float, float]] = [
        (cx + r_base * ux - w_base * nx, cy + r_base * uy - w_base * ny),
    ]
    steps = 16
    for i in range(steps + 1):
        ang = theta - math.pi / 2.0 + math.pi * (i / steps)
        tx = cx + r_tip_center * ux + r_tip * math.cos(ang)
        ty = cy + r_tip_center * uy + r_tip * math.sin(ang)
        pts.append((tx, ty))
    pts.append((cx + r_base * ux + w_base * nx, cy + r_base * uy + w_base * ny))
    return pts


# 1. 8 radial outer handles
for k in range(8):
    ang = k * 45.0
    polygon(
        _build_handle_points(ang),
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.4),
    )

# 2. Main ship's wheel ring (PASTEL_BLUE outer circle + WHITE inner circle)
circle(
    (cx, cy),
    radius=r_ring_outer,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (cx, cy),
    radius=r_ring_inner,
    style=fill_style(WHITE, border_color=DARK, border_units=2.4),
)

# 3. 8 inner radial spokes across the white interior
for k in range(8):
    theta = math.radians(k * 45.0)
    x_end = cx + r_ring_inner * math.cos(theta)
    y_end = cy + r_ring_inner * math.sin(theta)
    draw_round_segment((cx, cy), (x_end, y_end), width_units=2.6, color=DARK)

# 4. Central hub circle (PASTEL_GREEN + small WHITE center pin)
circle(
    (cx, cy),
    radius=8.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4),
)
circle(
    (cx, cy),
    radius=3.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
