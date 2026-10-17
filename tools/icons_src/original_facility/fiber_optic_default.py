# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: fiber_optic."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6


def _bezier_pts(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 24,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


# 1. Three fanning glass fiber strands from jacket collar (x=41.5) to right tips
top_strand = _bezier_pts((41.5, 55.5), (53.5, 56.5), (60.5, 74.0), (73.5, 76.0))
mid_strand = [(41.5, 50.0), (77.0, 50.0)]
bot_strand = _bezier_pts((41.5, 44.5), (53.5, 43.5), (60.5, 26.0), (73.5, 24.0))

for strand in (top_strand, mid_strand, bot_strand):
    draw_round_polyline(strand, width_units=6.4, color=DARK)
    draw_round_polyline(strand, width_units=3.2, color=WHITE)

# 2. Outer fiber bundle jacket on the left (PASTEL_BLUE, x=11.5..37.5)
rectangle(
    (24.5, 50.0),
    width=26.0,
    height=22.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=4.5),
)

# Subtle cable grip ribs on jacket
for rx in (18.0, 24.5):
    draw_round_segment((rx, 43.0), (rx, 57.0), width_units=w_inner, color=DARK)

# 3. Stripped cable collar / boot ring (PASTEL_BLUE_LIGHT)
rectangle(
    (39.0, 50.0),
    width=8.0,
    height=26.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=3.0),
)

# 4. Glowing PASTEL_GREEN / WHITE glass core tips
tips = [
    (73.5, 76.0),
    (77.0, 50.0),
    (73.5, 24.0),
]
for cx, cy in tips:
    circle(
        (cx, cy),
        radius=6.8,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer),
    )
    circle(
        (cx, cy),
        radius=2.8,
        style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
    )

# Small light-pulse rays around the middle tip (within x <= 88.0)
for ang_deg in (-38.0, 0.0, 38.0):
    rad = math.radians(ang_deg)
    draw_round_segment(
        (77.0 + 9.0 * math.cos(rad), 50.0 + 9.0 * math.sin(rad)),
        (77.0 + 11.0 * math.cos(rad), 50.0 + 11.0 * math.sin(rad)),
        width_units=w_inner,
        color=DARK,
    )

save()
