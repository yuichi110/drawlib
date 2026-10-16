# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: ollama."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
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
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


def _oval_pts(cx: float, cy: float, rx: float, ry: float, steps: int = 36) -> list[tuple[float, float]]:
    """Sample axis-aligned oval polygon."""
    return [
        (cx + rx * math.cos(2.0 * math.pi * i / steps), cy + ry * math.sin(2.0 * math.pi * i / steps))
        for i in range(steps)
    ]


# 1. Cute fluffy llama head/torso front portrait silhouette (WHITE wool body)
left_half: list[tuple[float, float]] = [
    # Top head crown center
    (50.0, 77.5),
    # Crown slope to left ear inner base
    *_cubic((50.0, 77.5), (44.8, 77.5), (41.2, 75.2), (39.5, 72.0), 10),
    # Left ear up to rounded tip and down outer ear
    *_cubic((39.5, 72.0), (39.2, 82.5), (36.2, 89.2), (32.2, 89.2), 12),
    *_cubic((32.2, 89.2), (27.5, 89.2), (25.2, 80.5), (25.5, 69.0), 12),
    # Upper cheek puff
    *_cubic((25.5, 69.0), (19.5, 64.5), (17.5, 53.5), (22.5, 45.8), 14),
    # Middle torso wool puff
    *_cubic((22.5, 45.8), (18.2, 39.5), (18.2, 29.5), (22.8, 23.8), 14),
    # Lower torso side down to rounded base corner
    *_cubic((22.8, 23.8), (20.2, 18.8), (20.5, 13.5), (24.5, 11.8), 10),
]

right_half = [(100.0 - x, y) for x, y in reversed(left_half[1:])]
body_pts: list[tuple[float, float]] = [
    *left_half,
    *_cubic((24.5, 11.8), (36.0, 10.2), (64.0, 10.2), (75.5, 11.8), 14),
    *right_half,
]

polygon(body_pts, style=no_border_fill(WHITE))
draw_round_polyline(body_pts, width_units=w, color=DARK, closed=True)

# 2. Inner ear pads (WHITE)
left_ear_pad: list[tuple[float, float]] = [
    (36.2, 71.5),
    *_cubic((36.2, 71.5), (36.0, 79.5), (34.2, 84.5), (32.2, 84.5), 10),
    *_cubic((32.2, 84.5), (30.0, 84.5), (28.8, 78.8), (29.2, 71.2), 10),
    *_cubic((29.2, 71.2), (31.5, 72.0), (34.0, 72.0), (36.2, 71.5), 8),
]
right_ear_pad = [(100.0 - x, y) for x, y in left_ear_pad]

for pad in (left_ear_pad, right_ear_pad):
    polygon(pad, style=no_border_fill(WHITE))
    draw_round_polyline(pad, width_units=1.6, color=DARK, closed=True)

# 3. Rounded snout oval (WHITE)
snout_pts = _oval_pts(50.0, 46.8, rx=12.2, ry=9.2, steps=40)
polygon(snout_pts, style=no_border_fill(WHITE))
draw_round_polyline(snout_pts, width_units=1.8, color=DARK, closed=True)

# 4. Round dark eyes (DARK)
circle((33.8, 52.8), radius=3.3, style=fill_style(DARK))
circle((66.2, 52.8), radius=3.3, style=fill_style(DARK))

# 5. Cute Y-shaped nose/mouth inside snout (DARK)
draw_round_polyline(
    [(47.6, 48.8), (50.0, 46.8), (52.4, 48.8)],
    width_units=2.0,
    color=DARK,
)
draw_round_segment((50.0, 46.8), (50.0, 44.0), width_units=2.0, color=DARK)

save()
