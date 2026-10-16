# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: prometheus."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0


def _quad_curve(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 12,
) -> list[tuple[float, float]]:
    """Sample a quadratic Bezier curve from p0 to p2."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0]
        by = (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1]
        pts.append((bx, by))
    return pts


# 1. Circular medallion (PASTEL_BLUE outer ring + WHITE inner circle)
circle(
    (cx, cy),
    radius=40.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (cx, cy),
    radius=31.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.3),
)

# 2. Lower torch dish (PASTEL_BLUE_LIGHT semicircular bowl at bottom)
dish_pts: list[tuple[float, float]] = [(41.0, 27.8)]
steps_dish = 16
for i in range(steps_dish + 1):
    ang = math.radians(180.0 + 180.0 * (i / steps_dish))
    dish_pts.append((cx + 9.0 * math.cos(ang), 27.8 + 5.6 * math.sin(ang)))
polygon(dish_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(dish_pts, width_units=2.2, color=DARK, closed=True)

# 3. Horizontal torch base bar (PASTEL_BLUE) with clear separation above dish
rectangle(
    (cx, 33.8),
    width=30.0,
    height=4.8,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.2, shape_r=1.4),
)

# 4. Stylized 3-tip Prometheus flame with side wing flares (PASTEL_GREEN)
flame_pts: list[tuple[float, float]] = [(36.5, 40.0)]
# Left lower flare wing
flame_pts += _quad_curve((36.5, 40.0), (32.5, 42.5), (30.5, 45.8), steps=8)
flame_pts += _quad_curve((30.5, 45.8), (34.5, 45.2), (37.5, 44.5), steps=8)
# Left upward curve to left flame tip
flame_pts += _quad_curve((37.5, 44.5), (33.5, 53.0), (38.5, 65.5))
# Left valley between left tip and center tip
flame_pts += _quad_curve((38.5, 65.5), (42.5, 59.0), (44.2, 55.0))
# Tall center flame tip
flame_pts += _quad_curve((44.2, 55.0), (45.8, 67.5), (50.0, 75.5))
flame_pts += _quad_curve((50.0, 75.5), (54.2, 67.0), (55.8, 54.5))
# Right flame tip
flame_pts += _quad_curve((55.8, 54.5), (57.8, 58.5), (61.5, 64.5))
# Right downward curve to right lower flare wing
flame_pts += _quad_curve((61.5, 64.5), (66.5, 53.0), (62.5, 44.5))
flame_pts += _quad_curve((62.5, 44.5), (65.5, 45.2), (69.5, 45.8), steps=8)
flame_pts += _quad_curve((69.5, 45.8), (67.5, 42.5), (63.5, 40.0), steps=8)

polygon(flame_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(flame_pts, width_units=2.3, color=DARK, closed=True)

save()
