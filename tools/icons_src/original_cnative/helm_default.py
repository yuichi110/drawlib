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
    draw_compound_polygon,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0
r_ring_outer = 27.5
r_ring_inner = 18.0
r_hub_outer = 8.5
r_hub_inner = 3.0


def _circle_pts(r: float, steps: int = 64) -> list[tuple[float, float]]:
    """Sample a circle polygon centered at (cx, cy)."""
    return [
        (cx + r * math.cos(math.radians(360.0 * i / steps)), cy + r * math.sin(math.radians(360.0 * i / steps)))
        for i in range(steps)
    ]


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

# 2. 8 inner radial spokes across the transparent interior (r=8.5..18.0)
for k in range(8):
    theta = math.radians(k * 45.0)
    x_start = cx + r_hub_outer * math.cos(theta)
    y_start = cy + r_hub_outer * math.sin(theta)
    x_end = cx + r_ring_inner * math.cos(theta)
    y_end = cy + r_ring_inner * math.sin(theta)
    draw_round_segment((x_start, y_start), (x_end, y_end), width_units=2.6, color=DARK)

# 3. Main ship's wheel ring (PASTEL_BLUE annulus r=18.0..27.5)
draw_compound_polygon([_circle_pts(r_ring_outer), _circle_pts(r_ring_inner)], color=PASTEL_BLUE)
circle((cx, cy), radius=r_ring_outer, style=stroke_style(DARK, width_units=w))
circle((cx, cy), radius=r_ring_inner, style=stroke_style(DARK, width_units=2.4))

# 4. Central hub ring (PASTEL_GREEN annulus r=3.0..8.5 with transparent pin hole)
draw_compound_polygon([_circle_pts(r_hub_outer), _circle_pts(r_hub_inner)], color=PASTEL_GREEN)
circle((cx, cy), radius=r_hub_outer, style=stroke_style(DARK, width_units=2.4))
circle((cx, cy), radius=r_hub_inner, style=stroke_style(DARK, width_units=2.0))

save()
