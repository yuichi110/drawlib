# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: openhands."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
SCALE = 0.95


def _s(x: float, y: float) -> tuple[float, float]:
    """Scale point toward (50, 50) so outer border stays inside [9, 91]."""
    return (50.0 + SCALE * (x - 50.0), 50.0 + SCALE * (y - 50.0))


def _mirror_x(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Mirror scaled points across x = 50.0."""
    return [(100.0 - x, y) for x, y in pts]


def _draw_ray_capsule(
    p1: tuple[float, float],
    p2: tuple[float, float],
    width_units: float,
    fill_color: Any,
) -> None:
    """Draw a rounded celebration ray capsule with DARK border."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    r = width_units / 2.0
    ang_base = math.atan2(dy, dx)
    pts: list[tuple[float, float]] = []
    steps = 12
    for i in range(steps + 1):
        ang = ang_base + math.pi / 2.0 + math.pi * (i / steps)
        pts.append((x1 + r * math.cos(ang), y1 + r * math.sin(ang)))
    for i in range(steps + 1):
        ang = ang_base - math.pi / 2.0 + math.pi * (i / steps)
        pts.append((x2 + r * math.cos(ang), y2 + r * math.sin(ang)))
    polygon(pts, style=no_border_fill(fill_color))
    draw_round_polyline(pts, width_units=1.7, color=DARK, closed=True)


# Left open hand silhouette in raw coordinates
raw_left_hand = [
    (25.23, 66.62),
    (26.88, 66.34),
    (28.03, 65.33),
    (28.71, 63.31),
    (28.93, 59.99),
    (29.20, 62.80),
    (29.93, 64.40),
    (31.01, 65.12),
    (32.32, 65.29),
    (33.58, 64.98),
    (34.53, 63.94),
    (35.09, 62.04),
    (35.21, 59.96),
    (35.02, 56.12),
    (34.67, 52.03),
    (34.27, 47.78),
    (34.09, 44.09),
    (34.08, 40.72),
    (34.27, 38.57),
    (34.77, 37.10),
    (35.38, 37.06),
    (36.06, 37.99),
    (37.03, 40.00),
    (38.67, 42.59),
    (40.40, 44.61),
    (42.01, 45.93),
    (43.63, 46.51),
    (44.86, 46.25),
    (45.85, 45.20),
    (46.09, 44.31),
    (45.67, 43.33),
    (44.60, 41.52),
    (43.24, 38.97),
    (41.93, 35.97),
    (40.95, 33.11),
    (39.76, 30.64),
    (38.32, 28.43),
    (36.42, 26.30),
    (34.37, 24.94),
    (31.14, 23.86),
    (27.40, 23.38),
    (23.52, 23.48),
    (19.86, 24.15),
    (16.80, 25.38),
    (14.54, 27.10),
    (12.97, 29.10),
    (11.73, 31.79),
    (11.05, 34.38),
    (10.75, 36.94),
    (10.78, 39.41),
    (11.04, 42.88),
    (10.92, 46.02),
    (10.64, 49.71),
    (10.33, 53.26),
    (10.34, 55.12),
    (10.91, 56.67),
    (12.07, 57.43),
    (13.24, 57.52),
    (14.59, 57.01),
    (15.62, 55.66),
    (15.93, 53.82),
    (15.93, 59.94),
    (16.27, 61.50),
    (17.36, 62.72),
    (18.86, 63.28),
    (20.25, 63.13),
    (21.46, 62.35),
    (22.07, 60.97),
    (22.16, 59.94),
    (22.20, 63.68),
    (22.90, 65.49),
    (24.16, 66.44),
]

left_hand_pts = [_s(x, y) for x, y in raw_left_hand]
right_hand_pts = _mirror_x(left_hand_pts)

PALE_YELLOW = "#F3E060"

# 1. Fill left and right hands (PALE_YELLOW)
polygon(left_hand_pts, style=no_border_fill(PALE_YELLOW))
polygon(right_hand_pts, style=no_border_fill(PALE_YELLOW))

# 2. Inner finger dividers and knuckle crease lines
left_seams = [
    (_s(15.93, 53.82), _s(16.45, 44.45)),
    (_s(22.16, 59.94), _s(22.20, 45.25)),
    (_s(28.93, 59.99), _s(28.90, 46.15)),
    (_s(14.60, 44.20), _s(29.80, 46.20)),
]
for p1, p2 in left_seams:
    draw_round_segment(p1, p2, width_units=1.7, color=DARK)
    draw_round_segment((100.0 - p1[0], p1[1]), (100.0 - p2[0], p2[1]), width_units=1.7, color=DARK)

# 3. Outer hand outlines (w = 1.9)
draw_round_polyline(left_hand_pts, width_units=w, color=DARK, closed=True)
draw_round_polyline(right_hand_pts, width_units=w, color=DARK, closed=True)

# 4. Three celebration rays at top center (Colors.Gray6)
_draw_ray_capsule(_s(50.0, 68.8), _s(50.0, 77.2), width_units=3.2, fill_color=Colors.Gray6)
_draw_ray_capsule(_s(44.0, 67.0), _s(39.8, 74.3), width_units=3.2, fill_color=Colors.Gray6)
_draw_ray_capsule(_s(56.0, 67.0), _s(60.2, 74.3), width_units=3.2, fill_color=Colors.Gray6)

save()
