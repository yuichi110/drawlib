# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: langgraph."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
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
FOREST_TEAL = "#2D5252"


def _arc(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 24,
) -> list[tuple[float, float]]:
    """Sample circular arc points."""
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


def _draw_link_bar(
    p1: tuple[float, float],
    p2: tuple[float, float],
    width_units: float,
    fill_color: Any,
) -> None:
    """Draw a clean rectangular link bar between two node centers."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    nx = -dy / dist * (width_units / 2.0)
    ny = dx / dist * (width_units / 2.0)
    pts = [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny),
    ]
    polygon(pts, style=no_border_fill(fill_color))
    draw_round_polyline(pts, width_units=1.4, color=DARK, closed=True)


# 1. Outer stadium pill badge (FOREST_TEAL)
pill_pts = [
    *_arc(30.0, 50.0, 20.0, 90.0, 270.0, 28),
    *_arc(70.0, 50.0, 20.0, -90.0, 90.0, 28),
]
polygon(pill_pts, style=no_border_fill(FOREST_TEAL))
draw_round_polyline(pill_pts, width_units=w, color=DARK, closed=True)

# 2. Smooth stylized parrot silhouette on the left (WHITE)
bird_pts = [
    (29.4, 64.0),
    (28.2, 63.9),
    (27.1, 63.4),
    (26.3, 62.7),
    (25.8, 61.5),
    (25.1, 60.8),
    (24.3, 59.9),
    (23.9, 58.7),
    (23.8, 57.6),
    (24.4, 56.3),
    (25.0, 57.5),
    (26.2, 57.0),
    (27.9, 57.1),
    (28.8, 55.3),
    (29.5, 52.6),
    (30.1, 49.9),
    (31.0, 47.4),
    (32.5, 45.2),
    (34.5, 43.3),
    (34.6, 41.2),
    (35.1, 39.6),
    (33.8, 38.7),
    (31.4, 38.7),
    (30.4, 37.9),
    (32.2, 37.2),
    (35.4, 37.8),
    (38.6, 36.4),
    (42.2, 37.2),
    (40.7, 38.6),
    (41.4, 41.6),
    (44.6, 40.3),
    (47.0, 38.5),
    (50.2, 38.5),
    (49.1, 39.9),
    (47.4, 42.1),
    (45.6, 46.2),
    (43.3, 50.0),
    (40.5, 53.1),
    (36.8, 56.9),
    (35.1, 59.6),
    (33.8, 61.9),
    (32.5, 63.1),
    (30.7, 63.8),
]
polygon(bird_pts, style=no_border_fill(WHITE))
draw_round_polyline(bird_pts, width_units=1.4, color=DARK, closed=True)

# 3. Four-node diamond graph on the right (WHITE links + WHITE nodes)
n_left = (58.6, 50.8)
n_top = (65.7, 60.6)
n_bot = (65.7, 41.0)
n_right = (72.8, 50.8)

_draw_link_bar(n_left, n_top, width_units=2.4, fill_color=WHITE)
_draw_link_bar(n_left, n_bot, width_units=2.4, fill_color=WHITE)
_draw_link_bar(n_left, n_right, width_units=2.4, fill_color=WHITE)
_draw_link_bar(n_right, n_top, width_units=2.4, fill_color=WHITE)

for node_xy in (n_left, n_top, n_bot, n_right):
    circle(
        node_xy,
        radius=3.8,
        style=fill_style(WHITE, border_color=DARK, border_units=1.6),
    )

save()
