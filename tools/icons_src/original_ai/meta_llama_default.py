# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: meta_llama."""

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
scale = 0.96


def _s(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in pts]


# Left loop ribbon (Colors.Blue3): from top-left seam around left & bottom-left to center tuck
left_ribbon = _s(
    [
        (32.48, 77.33),
        (30.06, 77.13),
        (27.71, 76.55),
        (25.45, 75.61),
        (23.30, 74.35),
        (21.26, 72.79),
        (19.34, 70.95),
        (17.55, 68.84),
        (15.90, 66.50),
        (14.38, 63.92),
        (13.06, 61.22),
        (11.91, 58.35),
        (10.94, 55.34),
        (10.15, 52.21),
        (9.61, 49.30),
        (9.24, 46.34),
        (9.02, 42.75),
        (9.03, 40.07),
        (9.28, 37.24),
        (9.77, 34.56),
        (10.50, 32.20),
        (11.45, 30.07),
        (12.61, 28.18),
        (13.81, 26.74),
        (15.42, 25.31),
        (17.24, 24.17),
        (19.26, 23.34),
        (21.48, 22.84),
        (23.88, 22.67),
        (26.32, 22.83),
        (28.65, 23.40),
        (30.93, 24.46),
        (33.23, 26.13),
        (35.63, 28.51),
        (38.17, 31.69),
        (40.94, 35.78),
        (43.99, 40.88),
        (50.02, 51.57),
        (45.83, 58.02),
        (43.97, 55.15),
        (40.88, 50.35),
        (37.45, 44.95),
        (35.04, 41.23),
        (32.99, 38.24),
        (31.23, 35.91),
        (29.68, 34.16),
        (28.27, 32.92),
        (26.94, 32.12),
        (25.61, 31.69),
        (24.22, 31.56),
        (23.09, 31.66),
        (22.01, 31.99),
        (21.02, 32.54),
        (20.17, 33.29),
        (18.81, 35.51),
        (18.15, 37.90),
        (17.88, 40.76),
        (18.03, 44.94),
        (18.59, 49.10),
        (19.44, 52.78),
        (20.57, 56.24),
        (21.95, 59.42),
        (23.57, 62.24),
        (25.55, 64.81),
        (27.14, 66.30),
        (28.81, 67.42),
        (30.57, 68.14),
        (32.45, 68.40),
    ]
)

# Right crossover ribbon (Colors.Blue3): from top-left seam across center, around right loop, to top-right tuck
right_ribbon = _s(
    [
        (32.48, 77.33),
        (34.97, 77.18),
        (37.30, 76.71),
        (39.58, 75.89),
        (41.84, 74.70),
        (44.10, 73.12),
        (46.38, 71.12),
        (48.71, 68.69),
        (51.11, 65.80),
        (53.17, 63.05),
        (55.13, 60.23),
        (58.88, 54.38),
        (64.36, 45.25),
        (67.29, 40.59),
        (69.64, 37.08),
        (71.56, 34.57),
        (72.81, 33.26),
        (74.31, 32.19),
        (75.64, 31.71),
        (77.06, 31.57),
        (78.39, 31.71),
        (79.72, 32.20),
        (80.93, 33.14),
        (81.89, 34.49),
        (82.48, 35.88),
        (82.94, 37.87),
        (83.16, 40.19),
        (83.16, 42.74),
        (82.92, 46.51),
        (82.43, 50.11),
        (81.70, 53.52),
        (80.75, 56.70),
        (79.60, 59.63),
        (78.26, 62.27),
        (76.75, 64.59),
        (75.10, 66.56),
        (73.26, 68.17),
        (71.37, 69.33),
        (69.37, 70.04),
        (67.29, 70.28),
        (65.36, 70.05),
        (63.50, 69.33),
        (61.68, 68.13),
        (59.85, 66.46),
        (57.22, 63.28),
        (55.13, 60.22),
        (51.11, 65.79),
        (53.31, 68.61),
        (55.83, 71.42),
        (58.00, 73.40),
        (60.27, 75.03),
        (62.66, 76.27),
        (65.18, 77.06),
        (67.85, 77.33),
        (70.43, 77.11),
        (72.92, 76.45),
        (75.33, 75.39),
        (77.62, 73.95),
        (79.78, 72.15),
        (81.65, 70.20),
        (83.75, 67.47),
        (85.63, 64.39),
        (87.26, 60.99),
        (88.63, 57.31),
        (89.71, 53.38),
        (90.48, 49.25),
        (90.91, 44.95),
        (91.00, 41.81),
        (90.88, 38.81),
        (90.54, 36.02),
        (89.96, 33.46),
        (89.17, 31.15),
        (88.15, 29.08),
        (86.62, 26.91),
        (84.27, 24.81),
        (82.17, 23.67),
        (79.86, 22.97),
        (77.49, 22.69),
        (75.21, 22.75),
        (73.05, 23.10),
        (71.08, 23.73),
        (68.99, 24.84),
        (66.96, 26.38),
        (64.80, 28.56),
        (62.32, 31.67),
        (59.67, 35.56),
        (56.76, 40.28),
        (52.75, 47.06),
        (49.28, 52.77),
        (46.23, 57.44),
        (43.53, 61.15),
        (41.09, 63.99),
        (38.84, 66.05),
        (36.70, 67.41),
        (34.60, 68.17),
        (32.45, 68.40),
    ]
)

# 1. Fill both left loop and right crossover ribbon in unified Colors.Blue3
seam_patch = _s([(31.8, 77.28), (33.2, 77.30), (33.2, 68.36), (31.8, 68.36)])
polygon(seam_patch, style=no_border_fill(Colors.Blue3))
polygon(left_ribbon, style=no_border_fill(Colors.Blue3))
polygon(right_ribbon, style=no_border_fill(Colors.Blue3))

# 3. Crisp w = 1.9 DARK borders (open at top-left join so loop has no vertical seam)
draw_round_polyline(left_ribbon, width_units=w, color=DARK, closed=False)
draw_round_polyline(right_ribbon, width_units=w, color=DARK, closed=False)

save()
