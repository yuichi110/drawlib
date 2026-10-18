# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: dagster."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0


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


def _semi_cap(p_start: tuple[float, float], p_end: tuple[float, float], steps: int = 12) -> list[tuple[float, float]]:
    """Build semicircular cap from p_start to p_end bulging outward (CCW)."""
    mx = 0.5 * (p_start[0] + p_end[0])
    my = 0.5 * (p_start[1] + p_end[1])
    dx = p_start[0] - mx
    dy = p_start[1] - my
    r = math.hypot(dx, dy)
    ang0 = math.atan2(dy, dx)
    pts: list[tuple[float, float]] = []
    for i in range(1, steps):
        a = ang0 + math.pi * (i / steps)
        pts.append((mx + r * math.cos(a), my + r * math.sin(a)))
    return pts


# 1. Shaded underside pockets inside the 3 tentacle valleys (Colors.Purple2)
# Drawn behind the main body; Valley 2 and 3 fill completely down to where the tentacle borders meet.
pocket1 = [
    (34.0, 32.0),
    *_cubic((34.0, 32.0), (39.5, 29.8), (44.5, 29.5), (49.5, 30.8), 14),
    (63.0, 50.0),
    (58.5, 56.0),
    (34.0, 48.0),
]
pocket2 = [
    (48.5, 21.8),
    (53.0, 21.8),
    (62.0, 25.5),
    (69.0, 34.0),
    (71.5, 54.0),
    (61.5, 54.0),
    (48.5, 28.0),
]
pocket3 = [
    (67.5, 23.5),
    (70.5, 24.0),
    (75.5, 28.0),
    (80.0, 36.0),
    (82.0, 51.0),
    (73.0, 51.0),
    (67.5, 30.0),
]
for pk in (pocket1, pocket2, pocket3):
    polygon(pk, style=no_border_fill(Colors.Purple2))

draw_round_polyline(pocket1[:15], width_units=1.8, color=DARK)

# 2. Main Dagster octopus head dome & 3 curling right-to-left tentacles (Colors.Purple3)
p_left = (11.5, 52.5)
p_top = (49.5, 88.5)
p_right = (88.5, 51.0)

# Tentacle 3 (outer right)
p_t3_out = (72.5, 19.5)
p_t3_in = (65.8, 22.8)
p_v3_top = (80.5, 43.5)
p_v3_in = (74.5, 45.2)

# Tentacle 2 (middle)
p_t2_out = (38.5, 12.2)
p_t2_in = (38.5, 19.6)
p_v2_top = (70.0, 46.5)
p_v2_in = (63.8, 48.0)

# Tentacle 1 (upper-leftmost tentacle)
p_t1_out = (20.5, 22.2)
p_t1_in = (23.2, 28.8)
p_v1_top = (58.5, 52.0)

# Left cheek bottom curve
p_cheek_bot = (34.0, 32.0)

body_pts: list[tuple[float, float]] = [
    p_left,
    *_cubic(p_left, (11.5, 38.5), (21.5, 32.0), p_cheek_bot, 18),
    *_cubic(p_cheek_bot, (46.5, 32.0), (52.5, 43.5), p_v1_top, 18),
    *_cubic(p_v1_top, (62.5, 55.0), (65.0, 50.0), (62.0, 44.0), 10),
    *_cubic((62.0, 44.0), (54.0, 29.0), (38.0, 23.0), p_t1_in, 20),
    *_semi_cap(p_t1_in, p_t1_out, 12),
    p_t1_out,
    *_cubic(p_t1_out, (38.0, 15.0), (58.0, 22.0), p_v2_in, 20),
    *_cubic(p_v2_in, (65.5, 52.0), (70.5, 51.0), p_v2_top, 10),
    *_cubic(p_v2_top, (66.5, 29.0), (54.5, 19.6), p_t2_in, 20),
    *_semi_cap(p_t2_in, p_t2_out, 12),
    p_t2_out,
    *_cubic(p_t2_out, (58.5, 12.2), (71.5, 25.0), p_v3_in, 20),
    *_cubic(p_v3_in, (76.0, 49.0), (80.5, 48.0), p_v3_top, 10),
    *_cubic(p_v3_top, (78.5, 34.0), (73.0, 26.5), p_t3_in, 16),
    *_semi_cap(p_t3_in, p_t3_out, 12),
    p_t3_out,
    *_cubic(p_t3_out, (83.0, 28.5), (88.5, 39.0), p_right, 18),
    *_cubic(p_right, (88.5, 72.5), (71.5, 88.5), p_top, 24),
    *_cubic(p_top, (28.0, 88.5), (11.5, 72.5), p_left, 24),
]

polygon(body_pts, style=no_border_fill(Colors.Purple3))
draw_round_polyline(body_pts, width_units=w, color=DARK, closed=True)

# 3. Expressive eye on upper-right (WHITE dome + DARK pie-cut pupil)
p_eye_l = (47.5, 63.5)
p_eye_r = (65.5, 62.0)
eye_pts = [
    p_eye_l,
    *_cubic(p_eye_l, (45.0, 72.5), (50.5, 79.5), (56.5, 79.0), 16),
    *_cubic((56.5, 79.0), (62.5, 78.5), (67.0, 71.0), p_eye_r, 16),
    *_cubic(p_eye_r, (60.0, 64.5), (53.0, 65.0), p_eye_l, 12),
]
polygon(eye_pts, style=no_border_fill(WHITE))
draw_round_polyline(eye_pts, width_units=1.7, color=DARK, closed=True)

# Pie-cut dark pupil inside eye
px, py = 57.5, 68.5
r_pup = 5.4
pupil_pts: list[tuple[float, float]] = [(px, py)]
for i in range(29):
    ang = math.radians(155.0 + 325.0 * (i / 28))
    pupil_pts.append((px + r_pup * math.cos(ang), py + r_pup * math.sin(ang)))
polygon(pupil_pts, style=fill_style(DARK))

# 4. Three circular node spots on left cheek (Colors.Teal2)
for sx, sy in ((26.8, 57.5), (20.5, 51.0), (26.8, 44.5)):
    circle(
        (sx, sy),
        radius=3.4,
        style=fill_style(Colors.Teal2, border_color=DARK, border_units=1.5),
    )

save()
