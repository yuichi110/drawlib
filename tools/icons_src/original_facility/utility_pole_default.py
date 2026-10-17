# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: utility_pole."""

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


# 1. Diagonal crossarm braces (drawn behind pole and crossarms)
draw_round_segment((34.0, 74.0), (47.0, 65.0), width_units=w_inner, color=DARK)
draw_round_segment((66.0, 74.0), (53.0, 65.0), width_units=w_inner, color=DARK)

# 2. PASTEL_GREEN fiber/service drop line from pole tap to right side
drop_pts = _bezier_pts((57.4, 48.0), (65.0, 39.0), (75.0, 35.0), (85.0, 36.0))
draw_round_polyline(drop_pts, width_units=5.6, color=DARK)
draw_round_polyline(drop_pts, width_units=2.6, color=PASTEL_GREEN)
circle(
    (85.0, 36.0),
    radius=3.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner),
)

# 3. Main roadside utility pole mast (PASTEL_BLUE, x=45.8..54.2)
rectangle(
    (50.0, 50.0),
    width=8.4,
    height=72.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=2.5),
)

# Ground baseline
draw_round_segment((26.0, 14.0), (74.0, 14.0), width_units=w_outer, color=DARK)

# 4. Upper and lower horizontal crossarms (WHITE)
rectangle(
    (50.0, 76.5),
    width=62.0,
    height=5.6,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=2.0),
)
rectangle(
    (50.0, 62.5),
    width=48.0,
    height=5.4,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=2.0),
)

# Ceramic insulators on top of upper crossarm (PASTEL_BLUE_LIGHT)
for ix in (24.0, 37.0, 63.0, 76.0):
    rectangle(
        (ix, 81.2),
        width=4.6,
        height=4.2,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.4),
    )

# 5. Pole-mounted transformer can on left side (WHITE + PASTEL_BLUE_LIGHT cap)
tx_cx = 35.5
rectangle(
    (tx_cx, 41.5),
    width=14.0,
    height=19.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_outer, shape_r=2.8),
)
rectangle(
    (tx_cx, 48.8),
    width=14.0,
    height=4.4,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.8),
)
# Transformer mounting brackets to pole
draw_round_segment((42.5, 45.5), (45.8, 45.5), width_units=w_inner, color=DARK)
draw_round_segment((42.5, 37.5), (45.8, 37.5), width_units=w_inner, color=DARK)
# Small bushing on top of transformer
draw_round_segment((tx_cx, 51.0), (tx_cx, 54.2), width_units=w_inner, color=DARK)

# 6. PASTEL_GREEN fiber tap / splice box mounted flush on right edge of pole (x=54.2..60.6)
rectangle(
    (57.4, 48.0),
    width=6.4,
    height=9.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_inner, shape_r=1.8),
)

save()
