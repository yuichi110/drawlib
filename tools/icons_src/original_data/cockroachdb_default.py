# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: cockroachdb."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


def _mirror_x(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(100.0 - x, y) for x, y in pts]


# 1. Crossed curved antennae ribbons at top (Colors.Purple2)
# Base roots sit cleanly inside the top shoulders (x=35..40, y=61) so outer transition is flush
ant_l_to_r = [
    (34.2, 63.5),
    *_cubic((34.2, 63.5), (42.5, 79.5), (64.0, 90.0), (86.5, 84.5), 24),
    (84.5, 79.5),
    *_cubic((84.5, 79.5), (64.5, 84.5), (46.0, 74.5), (39.0, 61.0), 24),
]
ant_r_to_l = _mirror_x(ant_l_to_r)

for ant_pts in (ant_r_to_l, ant_l_to_r):
    polygon(ant_pts, style=no_border_fill(Colors.Purple2))
    draw_round_polyline(ant_pts, width_units=1.8, color=DARK, closed=True)

# 2. White triangular window between head collar and crossing antennae
window_pts = [
    (38.5, 63.8),
    *_cubic((38.5, 63.8), (45.0, 62.5), (55.0, 62.5), (61.5, 63.8), 12),
    *_cubic((61.5, 63.8), (57.2, 69.5), (53.5, 73.2), (50.0, 75.5), 12),
    *_cubic((50.0, 75.5), (46.5, 73.2), (42.8, 69.5), (38.5, 63.8), 12),
]
polygon(window_pts, style=no_border_fill(WHITE))
draw_round_polyline(window_pts, width_units=1.7, color=DARK, closed=True)

# 3. Main oval beetle shield body (Colors.Gray6)
p_bot = (50.0, 12.0)
p_sh_l = (34.0, 64.5)
p_sh_r = (66.0, 64.5)

body_pts = [
    p_bot,
    *_cubic(p_bot, (33.5, 22.0), (26.5, 44.5), p_sh_l, 26),
    *_cubic(p_sh_l, (43.5, 62.5), (56.5, 62.5), p_sh_r, 14),
    *_cubic(p_sh_r, (73.5, 44.5), (66.5, 22.0), p_bot, 26),
]
polygon(body_pts, style=no_border_fill(Colors.Gray6))

# 4. Two symmetric leaf-shaped wing covers on left and right sides (Colors.Green3)
left_wing = [
    (44.5, 19.5),
    *_cubic((44.5, 19.5), (32.5, 29.0), (30.5, 44.5), (35.5, 56.5), 20),
    *_cubic((35.5, 56.5), (44.0, 48.0), (47.5, 34.5), (44.5, 19.5), 20),
]
right_wing = _mirror_x(left_wing)

for wing_pts in (left_wing, right_wing):
    polygon(wing_pts, style=no_border_fill(Colors.Green3))
    draw_round_polyline(wing_pts, width_units=1.7, color=DARK, closed=True)

# 5. Outer shield body outline
draw_round_polyline(body_pts, width_units=w, color=DARK, closed=True)

save()
