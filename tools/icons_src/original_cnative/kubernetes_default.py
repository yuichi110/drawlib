# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: kubernetes."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon, K8s

Icon.setup()

cx, cy = 50.0, 48.0
r_ring_outer = 22.0
r_ring_inner = 15.0
r_hub = 6.5

# 1. Drawlib Original Kubernetes heptagon plate
K8s.draw_original_heptagon()


def _build_k8s_handle(angle_deg: float) -> list[tuple[float, float]]:
    """Build a crisp bulbous outer handle from r=20.0 to r=32.5."""
    theta = math.radians(angle_deg)
    ux, uy = math.cos(theta), math.sin(theta)
    nx, ny = -uy, ux

    r_base = 20.0
    r_tip_center = 29.8
    r_tip = 2.6
    w_base = 1.65

    pts: list[tuple[float, float]] = [
        (cx + r_base * ux - w_base * nx, cy + r_base * uy - w_base * ny),
    ]
    steps = 14
    for i in range(steps + 1):
        ang = theta - math.pi / 2.0 + math.pi * (i / steps)
        tx = cx + r_tip_center * ux + r_tip * math.cos(ang)
        ty = cy + r_tip_center * uy + r_tip * math.sin(ang)
        pts.append((tx, ty))
    pts.append((cx + r_base * ux + w_base * nx, cy + r_base * uy + w_base * ny))
    return pts


def _build_k8s_inner_spoke(angle_deg: float) -> list[tuple[float, float]]:
    """Build an inner spoke bar from r=5.0 to exact circular arc r=15.0."""
    theta = math.radians(angle_deg)
    ux, uy = math.cos(theta), math.sin(theta)
    nx, ny = -uy, ux
    w_half = 1.85
    r0 = 5.0
    half_ang = math.asin(w_half / r_ring_inner)

    pts: list[tuple[float, float]] = [
        (cx + r0 * ux - w_half * nx, cy + r0 * uy - w_half * ny),
    ]
    steps = 8
    for i in range(steps + 1):
        a = theta - half_ang + 2.0 * half_ang * (i / steps)
        pts.append((cx + r_ring_inner * math.cos(a), cy + r_ring_inner * math.sin(a)))
    pts.append((cx + r0 * ux + w_half * nx, cy + r0 * uy + w_half * ny))
    return pts


# 2. 7 outer handles aligned with heptagon vertices
spoke_angles = [90.0 + i * (360.0 / 7.0) for i in range(7)]
for ang in spoke_angles:
    polygon(
        _build_k8s_handle(ang),
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )

# 3. Ship's wheel outer and inner circles (creating the WHITE wheel ring)
circle(
    (cx, cy),
    radius=r_ring_outer,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
circle(
    (cx, cy),
    radius=r_ring_inner,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=2.0),
)

# 4. 7 inner spokes flush with r=15.0 + re-stroke inner ring border
for ang in spoke_angles:
    polygon(
        _build_k8s_inner_spoke(ang),
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )
circle(
    (cx, cy),
    radius=r_ring_inner,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)

# 5. Center PASTEL_GREEN hub circle
circle(
    (cx, cy),
    radius=r_hub,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
