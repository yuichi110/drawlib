# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: voice gateway (default classic 3D variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    WHITE,
    draw_cisco_3d_cylinder,
    draw_cisco_router_top_arrows,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

# 3D router/gateway cylinder (bottom at y=15, top ellipse centered at y=68)
draw_cisco_3d_cylinder(50.0, 30.0, 76.0, 38.0, 15.0)

# Classic 4 Cisco router arrows on top ellipse
draw_cisco_router_top_arrows(50.0, 68.0, 36.0, 14.0, color=WHITE)

# Crisp white telephone handset emblem on the front face (centered at (50.0, 34.5))
cx, cy = 50.0, 34.5
scale = 1.05

# Build arched telephone handset in local coordinates (top arch + two ear/mouth pads)
handset_pts: list[tuple[float, float]] = []

# Top convex arch from left (-13.6, -0.5) over (0, +6.6) to right (+13.6, -0.5)
for i in range(25):
    ang = math.radians(158.0 - 136.0 * (i / 24))
    ux = 14.8 * math.cos(ang)
    uy = -5.6 + 12.2 * math.sin(ang)
    handset_pts.append((cx + ux * scale, cy + uy * scale))

# Right mouthpiece pad bottom contour
handset_pts.extend(
    [
        (cx + 13.8 * scale, cy - 4.8 * scale),
        (cx + 12.0 * scale, cy - 6.2 * scale),
        (cx + 7.2 * scale, cy - 5.2 * scale),
        (cx + 6.4 * scale, cy + 1.4 * scale),
    ]
)

# Inner concave grip bridge from right (+6.0, +1.8) across (0, +2.8) to left (-6.0, +1.8)
for i in range(1, 12):
    t = i / 12
    ux = 6.4 * (1.0 - 2.0 * t)
    uy = 1.4 + 1.5 * math.sin(math.pi * t)
    handset_pts.append((cx + ux * scale, cy + uy * scale))

# Left earpiece pad bottom contour
handset_pts.extend(
    [
        (cx - 6.4 * scale, cy + 1.4 * scale),
        (cx - 7.2 * scale, cy - 5.2 * scale),
        (cx - 12.0 * scale, cy - 6.2 * scale),
        (cx - 13.8 * scale, cy - 4.8 * scale),
    ]
)

polygon(handset_pts, style=no_border_fill(WHITE))
draw_round_polyline(handset_pts, width_units=1.4, color=WHITE, closed=True)

save()
