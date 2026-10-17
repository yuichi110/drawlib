# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: knowledge_base."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 8,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


def _page_arch(x_start: float, x_end: float, y_base: float, bump: float, steps: int = 16) -> list[tuple[float, float]]:
    """Sample a smooth arch from x_start to x_end with peak offset `bump`."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        x = x_start + (x_end - x_start) * t
        y = y_base + bump * math.sin(math.pi * t)
        pts.append((x, y))
    return pts


# 1. Outer book cover (PASTEL_BLUE, x=12..88, y=22..76)
r_cov = 4.0
cover_pts: list[tuple[float, float]] = [
    *_arc_pts(12.0 + r_cov, 22.0 + r_cov, r_cov, 180.0, 270.0),
    (46.0, 22.0),
    (50.0, 19.5),
    (54.0, 22.0),
    *_arc_pts(88.0 - r_cov, 22.0 + r_cov, r_cov, 270.0, 360.0),
    *_arc_pts(88.0 - r_cov, 76.0 - r_cov, r_cov, 0.0, 90.0),
    (54.0, 76.0),
    (50.0, 73.5),
    (46.0, 76.0),
    *_arc_pts(12.0 + r_cov, 76.0 - r_cov, r_cov, 90.0, 180.0),
]
polygon(cover_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(cover_pts, width_units=w_outer, color=DARK, closed=True)

# 2. PASTEL_GREEN ribbon bookmark hanging from under right page
ribbon_pts: list[tuple[float, float]] = [
    (63.5, 32.0),
    (73.5, 32.0),
    (73.5, 13.0),
    (68.5, 18.0),
    (63.5, 13.0),
]
polygon(ribbon_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(ribbon_pts, width_units=w_outer, color=DARK, closed=True)

# 3. WHITE left and right open pages (x=17..50 and x=50..83)
left_page_pts: list[tuple[float, float]] = [
    *_page_arch(17.0, 50.0, 26.5, 4.0),
    *_page_arch(50.0, 17.0, 77.5, 4.0),
]
right_page_pts: list[tuple[float, float]] = [
    *_page_arch(50.0, 83.0, 26.5, 4.0),
    *_page_arch(83.0, 50.0, 77.5, 4.0),
]
polygon(left_page_pts, style=no_border_fill(WHITE))
polygon(right_page_pts, style=no_border_fill(WHITE))
draw_round_polyline(left_page_pts, width_units=w_outer, color=DARK, closed=True)
draw_round_polyline(right_page_pts, width_units=w_outer, color=DARK, closed=True)

# Center spine crease
draw_round_segment((50.0, 26.5), (50.0, 77.5), width_units=w_outer, color=DARK)

# 4. Crisp DARK text lines on left and right pages
for y_line in (65.0, 53.5, 42.0):
    draw_round_polyline(_page_arch(23.5, 43.5, y_line, 2.2, 10), width_units=w_inner, color=DARK)
    draw_round_polyline(_page_arch(56.5, 76.5, y_line, 2.2, 10), width_units=w_inner, color=DARK)

save()
