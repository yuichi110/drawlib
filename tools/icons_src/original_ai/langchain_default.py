# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: langchain."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
SCALE = 0.94
SKY_BLUE = "#8AC8FA"


def _scale_pt(x: float, y: float, dx: float = 0.0, dy: float = 0.0) -> tuple[float, float]:
    """Scale point toward canvas center (50, 50) with optional separation offset."""
    return (50.0 + SCALE * (x - 50.0) + dx, 50.0 + SCALE * (y - 50.0) + dy)


def _arc_pts(
    cx: float,
    cy: float,
    radius: float,
    deg_start: float,
    deg_end: float,
    dx: float = 0.0,
    dy: float = 0.0,
    steps: int = 28,
) -> list[tuple[float, float]]:
    """Sample circular arc points in raw icon coordinates and scale to canvas."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
        pts.append(_scale_pt(cx + radius * math.cos(ang), cy + radius * math.sin(ang), dx, dy))
    return pts


# 1. Top-left leaf petal (SKY_BLUE), shifted slightly up-left for clean border gap
top_left_leaf = [
    *_arc_pts(16.54, 54.61, 25.4, -45.0, 45.0, dx=-0.6, dy=0.8),
    *_arc_pts(34.73, 72.80, 25.4, 135.0, 225.0, dx=-0.6, dy=0.8),
]

# 2. Bottom-right leaf petal (SKY_BLUE), shifted slightly down-right
bottom_right_leaf = [
    *_arc_pts(54.61, 16.53, 25.4, 135.0, 45.0, dx=0.8, dy=-0.6),
    *_arc_pts(72.80, 34.73, 25.4, -45.0, -135.0, dx=0.8, dy=-0.6),
]

# 3. Bottom-left quarter-circle sector (SKY_BLUE), shifted slightly down-left
bottom_left_sector = [
    _scale_pt(34.78, 34.77, dx=-0.8, dy=-0.8),
    *_arc_pts(34.78, 34.77, 25.2, 180.0, 270.0, dx=-0.8, dy=-0.8),
]

# 4. Top-right pie sector (SKY_BLUE), shifted slightly up-right
top_right_sector = [
    _scale_pt(61.63, 43.43, dx=0.6, dy=0.6),
    *_arc_pts(61.63, 43.43, 25.2, 45.0, 135.0, dx=0.6, dy=0.6),
]

for pts in (top_left_leaf, bottom_right_leaf, bottom_left_sector, top_right_sector):
    polygon(pts, style=no_border_fill(SKY_BLUE))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
