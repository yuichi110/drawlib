# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: dynatrace."""

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

w = 2.0
s = 38.8 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale points around (50, 50) to fit safely within [10, 90]."""
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# 1. Left ribbon facet (Colors.Blue2)
left_facet = _sc(
    [
        (36.83, 84.13),
        (36.17, 80.49),
        (35.34, 75.22),
        (34.55, 69.38),
        (33.89, 63.2),
        (33.47, 57.67),
        (33.19, 51.87),
        (33.09, 46.89),
        (33.1, 42.85),
        (33.18, 39.83),
        (33.31, 37.29),
        (12.53, 17.56),
        (12.27, 19.49),
        (11.78, 23.4),
        (11.17, 28.93),
        (10.54, 35.61),
        (10.13, 41.1),
        (9.83, 46.69),
        (9.63, 51.77),
        (9.52, 56.17),
        (9.48, 59.72),
        (9.66, 60.87),
        (9.99, 62.07),
        (10.59, 63.38),
        (11.58, 64.88),
        (12.64, 66.04),
        (15.08, 68.15),
        (19.23, 71.5),
        (24.24, 75.43),
        (29.31, 79.28),
        (33.61, 82.39),
        (36.72, 84.24),
    ]
)

# 2. Top ribbon facet (Colors.Green2) - overlaps top-left fold of left facet
top_facet = _sc(
    [
        (9.48, 60.48),
        (9.48, 59.19),
        (9.8, 60.16),
        (10.41, 61.23),
        (11.21, 62.31),
        (12.37, 63.35),
        (13.63, 64.07),
        (15.14, 64.61),
        (16.51, 64.87),
        (20.18, 65.34),
        (25.49, 65.9),
        (31.37, 66.38),
        (37.56, 66.71),
        (45.13, 66.85),
        (52.32, 66.74),
        (57.9, 66.46),
        (63.41, 65.98),
        (84.19, 85.71),
        (81.51, 86.2),
        (77.2, 86.92),
        (71.4, 87.82),
        (64.56, 88.77),
        (58.48, 89.51),
        (52.8, 90.11),
        (47.77, 90.55),
        (43.59, 90.86),
        (41.1, 91.0),
        (39.86, 90.9),
        (38.49, 90.53),
        (36.93, 89.73),
        (35.71, 88.76),
        (32.69, 85.87),
        (27.8, 81.22),
        (22.05, 75.76),
        (16.43, 70.42),
        (11.94, 66.16),
        (10.65, 64.6),
        (9.91, 63.12),
        (9.53, 61.57),
    ]
)

# 3. Bottom ribbon facet (Colors.Purple2)
bottom_facet = _sc(
    [
        (83.43, 35.24),
        (79.76, 34.77),
        (74.45, 34.18),
        (68.57, 33.67),
        (61.12, 33.25),
        (54.81, 33.15),
        (49.27, 33.21),
        (43.24, 33.46),
        (39.0, 33.76),
        (36.48, 34.02),
        (15.69, 14.23),
        (18.4, 13.72),
        (22.75, 12.97),
        (28.58, 12.05),
        (35.44, 11.1),
        (41.36, 10.4),
        (46.7, 9.87),
        (52.36, 9.41),
        (57.55, 9.07),
        (59.07, 9.38),
        (60.63, 9.89),
        (62.45, 10.84),
        (64.46, 12.41),
        (67.72, 15.88),
        (72.88, 21.71),
        (78.31, 28.09),
        (82.37, 33.21),
        (83.54, 35.12),
    ]
)

# 4. Right ribbon facet (Colors.Green2) - overlaps bottom-right fold of bottom facet
right_facet = _sc(
    [
        (58.37, 9.02),
        (57.09, 9.07),
        (58.23, 9.39),
        (59.48, 10.08),
        (60.86, 11.2),
        (61.96, 12.7),
        (62.75, 14.5),
        (63.12, 15.86),
        (63.75, 19.5),
        (64.58, 24.78),
        (65.36, 30.62),
        (66.0, 36.8),
        (66.4, 42.33),
        (66.67, 48.12),
        (66.77, 53.08),
        (66.74, 58.24),
        (66.57, 62.65),
        (87.35, 82.44),
        (87.71, 79.72),
        (88.22, 75.37),
        (88.85, 69.53),
        (89.47, 62.64),
        (89.9, 56.55),
        (90.23, 49.79),
        (90.42, 44.03),
        (90.52, 39.57),
        (90.37, 37.94),
        (89.95, 36.59),
        (89.08, 35.07),
        (88.06, 33.9),
        (85.04, 31.01),
        (80.15, 26.34),
        (74.4, 20.86),
        (68.8, 15.51),
        (64.34, 11.24),
        (62.67, 10.02),
        (61.11, 9.34),
        (59.51, 9.03),
    ]
)

# Draw each facet in interlocking Z-order so fold seams and transparent center hole are crisp
for pts, col in [
    (left_facet, Colors.Blue2),
    (top_facet, Colors.Green2),
    (bottom_facet, Colors.Purple2),
    (right_facet, Colors.Green2),
]:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
