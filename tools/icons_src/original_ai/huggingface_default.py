# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: huggingface."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 12) -> list[tuple[float, float]]:
    """Sample circular arc from deg0 to deg1."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = math.radians(deg0 + (deg1 - deg0) * (i / steps))
        pts.append((xc + r * math.cos(a), yc + r * math.sin(a)))
    return pts


def _quad(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Sample quadratic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0],
                (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1],
            )
        )
    return pts


# 1. Cheerful round face (Colors.Amber2)
circle(
    (50.0, 52.5),
    radius=34.5,
    style=fill_style(Colors.Amber2, border_color=DARK, border_units=w),
)

# 2. Cute rosy cheeks (Colors.Amber3)
circle((28.0, 58.0), radius=3.3, style=no_border_fill(Colors.Amber3))
circle((72.0, 58.0), radius=3.3, style=no_border_fill(Colors.Amber3))

# 3. Smiling arched eyes (DARK)
for ex in (37.5, 62.5):
    eye_pts = [
        *_arc(ex, 61.8, 4.8, 195.0, -15.0, 16),
        *_quad((ex + 4.6, 60.6), (ex, 63.8), (ex - 4.6, 60.6), 12),
    ]
    polygon(eye_pts, style=no_border_fill(DARK))
    draw_round_polyline(eye_pts, width_units=1.2, color=DARK, closed=True)

# 4. Smiling open mouth (DARK) + cute heart-notched tongue (Colors.Red3)
mouth_l = (37.5, 51.5)
mouth_r = (62.5, 51.5)
mouth_pts = [
    mouth_l,
    *_quad(mouth_l, (50.0, 47.5), mouth_r, 14),
    *_quad(mouth_r, (59.5, 37.5), (50.0, 37.5), 12),
    *_quad((50.0, 37.5), (40.5, 37.5), mouth_l, 12),
]
polygon(mouth_pts, style=no_border_fill(DARK))

tongue_pts = [
    (42.2, 40.2),
    *_quad((42.2, 40.2), (45.2, 45.2), (48.8, 44.2), 8),
    (50.0, 42.3),
    (51.2, 44.2),
    *_quad((51.2, 44.2), (54.8, 45.2), (57.8, 40.2), 8),
    *_quad((57.8, 40.2), (50.0, 37.0), (42.2, 40.2), 12),
]
polygon(tongue_pts, style=no_border_fill(Colors.Red3))
draw_round_polyline(mouth_pts, width_units=1.7, color=DARK, closed=True)

# 5. Two cute open hands in front (Colors.Amber3)
# Build left hand polygon with 4 splayed fingers + inward thumb + rounded palm
left_hand: list[tuple[float, float]] = [
    # Thumb tip (inner top)
    *_arc(33.2, 39.2, 3.0, 10.0, 175.0, 10),
    # Crotch between thumb and index finger
    (30.4, 34.0),
    # Index finger (top-left)
    *_arc(21.8, 39.8, 3.1, 45.0, 215.0, 10),
    (24.0, 33.0),
    # Middle finger
    *_arc(15.2, 35.2, 3.1, 65.0, 240.0, 10),
    (21.2, 28.5),
    # Ring finger
    *_arc(13.5, 28.8, 3.0, 85.0, 260.0, 10),
    (20.5, 24.0),
    # Pinky finger (bottom-left)
    *_arc(14.5, 22.5, 2.8, 100.0, 280.0, 10),
    # Smooth palm bottom and inner wrist up to thumb
    *_quad((15.2, 19.8), (26.0, 12.8), (37.5, 14.5), 14),
    *_quad((37.5, 14.5), (46.5, 17.5), (44.8, 26.8), 12),
    *_quad((44.8, 26.8), (43.5, 32.5), (36.2, 39.5), 10),
]
right_hand = [(100.0 - x, y) for x, y in left_hand]

for hand in (left_hand, right_hand):
    polygon(hand, style=no_border_fill(Colors.Amber3))
    draw_round_polyline(hand, width_units=w, color=DARK, closed=True)

# Finger crease lines on left and right hands
left_creases = [
    ((30.4, 34.0), (32.8, 30.8)),
    ((24.0, 33.0), (28.0, 29.5)),
    ((21.2, 28.5), (25.5, 26.0)),
    ((20.5, 24.0), (24.5, 22.2)),
]
for p1, p2 in left_creases:
    draw_round_segment(p1, p2, width_units=1.6, color=DARK)
    draw_round_segment((100.0 - p1[0], p1[1]), (100.0 - p2[0], p2[1]), width_units=1.6, color=DARK)

save()
