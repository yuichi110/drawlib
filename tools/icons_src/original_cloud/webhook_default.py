# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: webhook."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx, cy = 50.0, 44.5
r_tri = 20.5
r_hook = 14.5
angles_deg = (90.0, 210.0, 330.0)

centers: list[tuple[float, float]] = []
for ang_deg in angles_deg:
    ang = math.radians(ang_deg)
    centers.append((cx + r_tri * math.cos(ang), cy + r_tri * math.sin(ang)))

# Draw 3 tangent-continuous hook arms: each starts at centers[i] and wraps around centers[(i - 1) % 3]
dist = math.sqrt(3.0) * r_tri
alpha_deg = math.degrees(math.acos(r_hook / dist))

for i in range(3):
    p_start = centers[i]
    target_idx = (i - 1) % 3
    tx, ty = centers[target_idx]
    target_ang = angles_deg[target_idx]

    # Direction from target center to p_start is target_ang + 150 deg
    psi_deg = target_ang + 150.0
    phi_start_deg = psi_deg - alpha_deg
    phi_end_deg = phi_start_deg - 195.0

    arm_pts: list[tuple[float, float]] = [p_start]
    steps = 32
    for s in range(steps + 1):
        ang = math.radians(phi_start_deg + (phi_end_deg - phi_start_deg) * (s / steps))
        arm_pts.append((tx + r_hook * math.cos(ang), ty + r_hook * math.sin(ang)))

    Icon.draw_round_polyline(arm_pts, width_units=w, color=Icon.DARK)

node_colors = (Icon.PASTEL_GREEN, Icon.PASTEL_BLUE, Icon.PASTEL_BLUE)
for (nx, ny), col in zip(centers, node_colors, strict=True):
    circle(
        (nx, ny),
        radius=8.8,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w),
    )
    circle(
        (nx, ny),
        radius=3.2,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )

save()
