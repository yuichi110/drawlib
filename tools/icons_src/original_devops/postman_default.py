# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: postman."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_in = 1.6


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


# 1. Circular badge (Colors.Orange3)
circle(
    (50.0, 50.0),
    radius=40.0,
    style=Icon.fill_style(Colors.Orange3, border_color=Icon.DARK, border_units=w),
)

# 2. Simplified WHITE astronaut silhouette launching up-right at 45 deg
# 2a. Legs and space boot (bottom-left)
legs_boot = [
    (43.9, 45.9),
    (29.2, 31.2),
    (25.6, 27.5),
    (26.0, 26.4),
    (34.5, 26.2),
    (34.5, 30.8),
    *_cubic((34.5, 30.8), (40.5, 34.0), (46.8, 38.0), (52.4, 42.4), 14),
    (49.0, 45.8),
]
polygon(legs_boot, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(legs_boot, width_units=w_in, color=Icon.DARK, closed=True)
# Boot ankle seam
Icon.draw_round_segment((29.2, 31.2), (34.4, 26.3), width_units=1.5, color=Icon.DARK)

# 2b. Jetpack side fin (left of waist)
fin_pts = [
    (42.6, 52.2),
    (38.2, 47.8),
    (38.8, 46.8),
    (46.2, 48.5),
]
polygon(fin_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(fin_pts, width_units=w_in, color=Icon.DARK, closed=True)

# 2c. Sleek torso and arms (middle-right)
torso_pts = [
    (42.6, 52.2),
    *_cubic((42.6, 52.2), (50.5, 60.2), (57.8, 65.8), (61.5, 66.6), 14),
    *_cubic((61.5, 66.6), (63.2, 66.6), (64.2, 65.6), (65.6, 63.8), 8),
    *_cubic((65.6, 63.8), (66.6, 62.4), (66.8, 60.5), (65.8, 58.0), 8),
    *_cubic((65.8, 58.0), (63.8, 54.0), (58.8, 48.6), (52.4, 42.4), 14),
    (47.5, 47.3),
]
polygon(torso_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(torso_pts, width_units=w_in, color=Icon.DARK, closed=True)

# Diagonal suit seam lines on torso
Icon.draw_round_segment((47.5, 47.3), (64.7, 64.5), width_units=1.5, color=Icon.DARK)
Icon.draw_round_segment((49.2, 45.8), (65.5, 60.2), width_units=1.5, color=Icon.DARK)

# 2d. Space helmet (top-right)
hcx, hcy = 69.4, 69.5
hr = 6.7
circle(
    (hcx, hcy),
    radius=hr,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_in),
)

# V-shaped visor outline on helmet
p_visor_bot = (hcx + hr * math.cos(math.radians(-56.0)), hcy + hr * math.sin(math.radians(-56.0)))
p_visor_mid = (68.0, 68.5)
p_visor_top = (hcx + hr * math.cos(math.radians(45.0)), hcy + hr * math.sin(math.radians(45.0)))
Icon.draw_round_polyline([p_visor_bot, p_visor_mid, p_visor_top], width_units=1.6, color=Icon.DARK)

# Small curved visor reflection arc
visor_arc = [
    (hcx + 4.2 * math.cos(math.radians(a)), hcy - 0.3 + 4.2 * math.sin(math.radians(a)))
    for a in (-22.0, -10.0, 2.0, 14.0)
]
Icon.draw_round_polyline(visor_arc, width_units=1.5, color=Icon.DARK)

save()
