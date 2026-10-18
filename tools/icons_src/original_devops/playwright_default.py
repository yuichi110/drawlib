# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: playwright."""

from drawlib.canvas import save
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    setup_icon,
)

setup_icon()

w = 2.0
w_in = 1.7


def _s(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale point list by 0.96 around (50, 50) to keep comfortable margins."""
    return [(50.0 + (x - 50.0) * 0.96, 50.0 + (y - 50.0) * 0.96) for x, y in pts]


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
                (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


# Shared seam curve along the green mask's left cheek from top-left intersection down to bottom-left
# This ensures the red mask never extends behind the green mask's transparent eye or mouth holes.
seam_top_to_frown = [
    (40.1, 71.0),
    *_cubic((40.1, 71.0), (38.0, 64.0), (36.4, 55.0), (36.5, 46.1), 12),
]
seam_frown_to_bot = [
    (37.3, 40.3),
    *_cubic((37.3, 40.3), (38.0, 36.8), (39.1, 34.0), (40.5, 32.1), 8),
]

# 1. Left tilted sad theater mask (Colors.Red3)
# Outer contour incorporates the frown notch on its right side so the frown is 100% transparent
red_outer = _s(
    [
        (40.1, 71.0),
        *_cubic((40.1, 71.0), (34.5, 67.5), (27.0, 64.8), (18.5, 64.8), 12),
        *_cubic((18.5, 64.8), (13.5, 65.0), (10.3, 66.2), (10.2, 64.0), 8),
        *_cubic((10.2, 64.0), (10.5, 58.0), (12.5, 49.5), (16.9, 42.0), 12),
        *_cubic((16.9, 42.0), (22.0, 33.5), (28.5, 29.5), (34.5, 29.5), 12),
        *_cubic((34.5, 29.5), (36.8, 29.5), (38.8, 30.4), (40.5, 32.1), 8),
        *reversed(seam_frown_to_bot[:-1]),
        # Bottom edge of frowning mouth inward to left corner
        (27.2, 37.5),
        # Upper arch of frowning mouth up-right back to seam
        *_cubic((27.2, 37.5), (28.5, 42.8), (32.2, 45.2), (36.5, 46.1), 12),
        *reversed(seam_top_to_frown[1:-1]),
    ]
)

red_eye_hole = _s(
    [
        (18.1, 53.9),
        (29.5, 56.9),
        *_cubic((29.5, 56.9), (29.2, 53.5), (26.5, 51.2), (23.1, 51.2), 10),
        *_cubic((23.1, 51.2), (20.8, 51.2), (19.0, 52.5), (18.1, 53.9), 8),
    ]
)

draw_compound_polygon([red_outer, red_eye_hole], color=Colors.Red3)

# Outline red mask outer contour (excluding the seam behind green mask) and eye/mouth holes
red_visible_outer = _s(
    [
        (40.1, 71.0),
        *_cubic((40.1, 71.0), (34.5, 67.5), (27.0, 64.8), (18.5, 64.8), 12),
        *_cubic((18.5, 64.8), (13.5, 65.0), (10.3, 66.2), (10.2, 64.0), 8),
        *_cubic((10.2, 64.0), (10.5, 58.0), (12.5, 49.5), (16.9, 42.0), 12),
        *_cubic((16.9, 42.0), (22.0, 33.5), (28.5, 29.5), (34.5, 29.5), 12),
        *_cubic((34.5, 29.5), (36.8, 29.5), (38.8, 30.4), (40.5, 32.1), 8),
    ]
)
red_frown_arc = _s(
    [
        (37.3, 40.3),
        (27.2, 37.5),
        *_cubic((27.2, 37.5), (28.5, 42.8), (32.2, 45.2), (36.5, 46.1), 12),
    ]
)
draw_round_polyline(red_visible_outer, width_units=w, color=DARK)
draw_round_polyline(red_eye_hole, width_units=w_in, color=DARK, closed=True)
draw_round_polyline(red_frown_arc, width_units=w_in, color=DARK)

# 2. Right tilted happy theater mask (Colors.Green3)
green_outer = _s(
    [
        (44.6, 80.7),
        *_cubic((44.6, 80.7), (43.5, 80.7), (43.0, 79.5), (42.0, 77.1), 8),
        *_cubic((42.0, 77.1), (38.2, 66.8), (36.3, 55.5), (36.4, 48.0), 14),
        *_cubic((36.4, 48.0), (36.6, 35.5), (43.2, 24.5), (53.5, 22.4), 14),
        *_cubic((53.5, 22.4), (62.5, 20.5), (72.5, 24.5), (79.5, 33.5), 14),
        *_cubic((79.5, 33.5), (86.0, 42.0), (90.0, 55.5), (91.0, 66.9), 14),
        *_cubic((91.0, 66.9), (91.0, 68.8), (89.2, 68.8), (85.4, 68.1), 8),
        *_cubic((85.4, 68.1), (75.5, 67.2), (64.5, 68.8), (54.3, 74.0), 14),
        *_cubic((54.3, 74.0), (49.5, 76.5), (46.5, 80.7), (44.6, 80.7), 10),
    ]
)

green_left_eye = _s(
    [
        (43.2, 57.6),
        *_cubic((43.2, 57.6), (45.5, 60.8), (48.8, 61.8), (52.0, 61.1), 10),
        *_cubic((52.0, 61.1), (55.5, 60.2), (57.6, 57.2), (57.9, 53.4), 10),
    ]
)

green_right_eye = _s(
    [
        (65.9, 50.8),
        *_cubic((65.9, 50.8), (68.2, 53.8), (71.5, 54.8), (74.7, 54.3), 10),
        *_cubic((74.7, 54.3), (78.2, 53.4), (80.4, 50.4), (80.7, 46.6), 10),
    ]
)

green_mouth = _s(
    [
        (45.4, 45.4),
        (71.6, 38.1),
        *_cubic((71.6, 38.1), (68.5, 34.5), (62.5, 33.5), (56.7, 34.8), 12),
        *_cubic((56.7, 34.8), (50.8, 36.2), (46.5, 40.5), (45.4, 45.4), 12),
    ]
)

draw_compound_polygon(
    [green_outer, green_left_eye, green_right_eye, green_mouth],
    color=Colors.Green3,
)

draw_round_polyline(green_outer, width_units=w, color=DARK, closed=True)
draw_round_polyline(green_left_eye, width_units=w_in, color=DARK, closed=True)
draw_round_polyline(green_right_eye, width_units=w_in, color=DARK, closed=True)
draw_round_polyline(green_mouth, width_units=w_in, color=DARK, closed=True)

save()
