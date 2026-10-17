# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: cloud_drive."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
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

w_outer = 2.0
w_inner = 1.6


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 14,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


def _upper_intersect(
    c1: tuple[float, float],
    r1: float,
    c2: tuple[float, float],
    r2: float,
) -> tuple[float, float]:
    """Return the upper intersection point of two circles."""
    x1, y1 = c1
    x2, y2 = c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    mx = x1 + a * dx / d
    my = y1 + a * dy / d
    pa = (mx - h * dy / d, my + h * dx / d)
    pb = (mx + h * dy / d, my - h * dx / d)
    return pa if pa[1] >= pb[1] else pb


def _deg_pos(center: tuple[float, float], pt: tuple[float, float]) -> float:
    """Return angle in [0, 360) degrees from center to pt."""
    return math.degrees(math.atan2(pt[1] - center[1], pt[0] - center[0])) % 360.0


# 1. Folder back tab (PASTEL_BLUE_LIGHT)
x0, y0, x1 = 13.0, 19.0, 87.0
y_tab_top = 82.0
y_back_top = 73.0
r_f = 4.5

back_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_f, y0 + r_f, r_f, 180.0, 270.0),
    *_arc_pts(x1 - r_f, y0 + r_f, r_f, 270.0, 360.0),
    *_arc_pts(x1 - r_f, y_back_top - r_f, r_f, 0.0, 90.0),
    (49.0, y_back_top),
    (42.0, y_tab_top),
    *_arc_pts(x0 + r_f, y_tab_top - r_f, r_f, 90.0, 180.0),
]
polygon(back_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(back_pts, width_units=w_outer, color=DARK, closed=True)

# 2. Folder front pocket (PASTEL_BLUE)
rectangle(
    (50.0, 42.5),
    width=74.0,
    height=47.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=r_f),
)

# 3. WHITE cloud centered on front pocket
c_left = (35.5, 36.5)
r_left = 8.0
c_mid = (49.0, 44.5)
r_mid = 12.0
c_right = (63.5, 37.5)
r_right = 9.0

p_lm = _upper_intersect(c_left, r_left, c_mid, r_mid)
p_mr = _upper_intersect(c_mid, r_mid, c_right, r_right)

ang_left_end = _deg_pos(c_left, p_lm)
ang_mid_start = _deg_pos(c_mid, p_lm)
ang_mid_end = _deg_pos(c_mid, p_mr)
ang_right_start = _deg_pos(c_right, p_mr)

cloud_pts: list[tuple[float, float]] = [
    # Left puff from bottom (270 deg) clockwise through 180 deg to p_lm (~80 deg)
    *_arc_pts(c_left[0], c_left[1], r_left, 270.0, ang_left_end, 16),
    # Center puff from p_lm (~182 deg) clockwise over top (90 deg) down to p_mr (~25 deg)
    *_arc_pts(c_mid[0], c_mid[1], r_mid, ang_mid_start, ang_mid_end, 24),
    # Right puff from p_mr (~105 deg) clockwise through 0 deg to bottom (-90 deg)
    *_arc_pts(c_right[0], c_right[1], r_right, ang_right_start, -90.0, 16),
]
polygon(cloud_pts, style=no_border_fill(WHITE))
draw_round_polyline(cloud_pts, width_units=w_inner, color=DARK, closed=True)

# 4. PASTEL_GREEN up arrow inside cloud
arrow_pts: list[tuple[float, float]] = [
    (46.8, 32.5),
    (53.2, 32.5),
    (53.2, 41.5),
    (57.2, 41.5),
    (50.0, 49.8),
    (42.8, 41.5),
    (46.8, 41.5),
]
polygon(arrow_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(arrow_pts, width_units=w_inner, color=DARK, closed=True)

save()
