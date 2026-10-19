# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: pytorch."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w = 2.0
VERMILION = "#F15F40"
cx, cy = 50.0, 43.2
r_out = 32.5
r_in = 24.1


def _arc(r: float, deg0: float, deg1: float, steps: int = 36) -> list[tuple[float, float]]:
    """Sample circular arc around (cx, cy) from deg0 to deg1."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = math.radians(deg0 + (deg1 - deg0) * (i / steps))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# 1. Circular flame-loop ring ("#F15F40") with pointed upper-left flame tip
inv_s2 = 1.0 / math.sqrt(2.0)
x_tl_out = cx - r_out * inv_s2
y_tl_out = cy + r_out * inv_s2
y_tip_out = y_tl_out + (cx - x_tl_out)  # +45 deg tangent up to x = 50.0

x_tl_in = cx - r_in * inv_s2
y_tl_in = cy + r_in * inv_s2
y_tip_in = y_tl_in + (cx - x_tl_in)  # +45 deg tangent up to x = 50.0

flame_ring_pts: list[tuple[float, float]] = [
    # Outer arc from +45 deg clockwise (-315 deg) to +135 deg (-225 deg)
    *_arc(r_out, 45.0, -225.0, 42),
    # Straight +45 deg outer flame slope up to vertical tip at x = 50.0
    (cx, y_tip_out),
    # Vertical cut down to inner flame edge at x = 50.0
    (cx, y_tip_in),
    # Straight -135 deg inner flame slope down-left to +135 deg on inner circle
    *_arc(r_in, -225.0, 45.0, 42),
]

polygon(flame_ring_pts, style=Icon.no_border_fill(VERMILION))
Icon.draw_round_polyline(flame_ring_pts, width_units=w, color=Icon.DARK, closed=True)

# 2. Top-right circular flame dot ("#F15F40")
circle(
    (61.6, 72.2),
    radius=4.3,
    style=Icon.fill_style(VERMILION, border_color=Icon.DARK, border_units=w),
)

save()
