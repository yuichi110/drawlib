# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: cohere."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cx, cy = 50.0, 50.0
scale = 0.95


def _s(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in pts]


# 1. Top-wide forest-sage capsule pebble ("#4D6E60")
top_pebble = _s(
    [
        (35.57, 42.17),
        (37.85, 42.24),
        (41.05, 42.65),
        (45.09, 43.65),
        (49.79, 45.43),
        (55.45, 47.70),
        (62.14, 50.42),
        (69.27, 53.47),
        (75.13, 56.19),
        (79.52, 58.42),
        (82.75, 60.42),
        (85.33, 62.64),
        (87.29, 65.10),
        (88.67, 67.80),
        (89.47, 70.76),
        (89.74, 74.00),
        (89.44, 77.18),
        (88.54, 80.26),
        (87.09, 83.11),
        (85.13, 85.63),
        (82.73, 87.75),
        (79.97, 89.38),
        (76.96, 90.46),
        (73.80, 90.96),
        (72.74, 90.99),
        (33.41, 90.99),
        (30.22, 90.79),
        (27.09, 90.16),
        (24.07, 89.13),
        (21.20, 87.72),
        (18.55, 85.95),
        (16.15, 83.84),
        (14.04, 81.44),
        (12.27, 78.79),
        (10.86, 75.92),
        (9.83, 72.90),
        (9.21, 69.77),
        (9.00, 66.58),
        (9.19, 63.44),
        (9.75, 60.42),
        (10.67, 57.54),
        (11.93, 54.84),
        (13.53, 52.32),
        (15.45, 50.03),
        (17.68, 47.98),
        (20.20, 46.20),
        (23.02, 44.71),
        (26.10, 43.55),
        (29.45, 42.72),
        (33.04, 42.26),
    ]
)

# 2. Bottom-right lilac capsule pebble (Colors.Purple2)
right_pebble = _s(
    [
        (42.22, 25.36),
        (42.53, 28.55),
        (43.46, 31.61),
        (44.97, 34.44),
        (47.00, 36.91),
        (49.48, 38.95),
        (52.30, 40.46),
        (64.69, 45.60),
        (67.75, 46.59),
        (70.82, 47.04),
        (73.83, 46.98),
        (76.76, 46.46),
        (79.54, 45.49),
        (82.13, 44.12),
        (84.48, 42.37),
        (86.55, 40.28),
        (88.28, 37.87),
        (89.62, 35.19),
        (90.54, 32.26),
        (90.97, 29.12),
        (91.00, 28.03),
        (90.73, 24.84),
        (89.93, 21.75),
        (88.63, 18.83),
        (86.85, 16.17),
        (84.65, 13.84),
        (82.10, 11.92),
        (79.25, 10.45),
        (76.21, 9.48),
        (73.04, 9.04),
        (71.97, 9.01),
        (58.57, 9.01),
        (55.38, 9.32),
        (52.31, 10.25),
        (49.48, 11.77),
        (47.00, 13.80),
        (44.97, 16.28),
        (43.46, 19.10),
        (42.53, 22.17),
    ]
)

# 3. Bottom-left coral pebble ("#F2826B")
left_pebble = _s(
    [
        (23.07, 38.95),
        (19.94, 38.60),
        (16.97, 37.56),
        (14.30, 35.88),
        (12.07, 33.66),
        (10.39, 30.99),
        (9.35, 28.01),
        (9.00, 24.88),
        (9.00, 23.06),
        (9.41, 19.89),
        (10.53, 16.90),
        (12.30, 14.23),
        (14.62, 12.04),
        (17.37, 10.42),
        (20.42, 9.46),
        (23.61, 9.22),
        (26.76, 9.71),
        (29.73, 10.89),
        (32.36, 12.71),
        (34.50, 15.08),
        (36.06, 17.87),
        (36.95, 20.93),
        (37.14, 23.06),
        (37.14, 24.88),
        (36.79, 28.01),
        (35.75, 30.99),
        (34.07, 33.66),
        (31.85, 35.88),
        (29.18, 37.56),
        (26.21, 38.60),
    ]
)

FOREST_SAGE = "#4D6E60"
CORAL = "#F2826B"

for pts, col in (
    (top_pebble, FOREST_SAGE),
    (right_pebble, Colors.Purple2),
    (left_pebble, CORAL),
):
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
