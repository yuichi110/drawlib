# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: mlflow."""

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
scale = 0.945
MLFLOW_CYAN = "#4CCCF1"
MLFLOW_BLUE = "#45A4E5"


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale points around canvas center (50.0, 50.0)."""
    return [(50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale) for x, y in pts]


# 1. Left sweeping bright cyan crescent arrow (#6AD0EE, softened #43C9ED)
left_arrow_raw = [
    (73.75, 83.57),
    (70.55, 85.59),
    (67.23, 87.30),
    (63.82, 88.68),
    (60.32, 89.73),
    (56.78, 90.47),
    (53.19, 90.89),
    (49.60, 91.00),
    (46.02, 90.79),
    (42.46, 90.28),
    (38.96, 89.46),
    (35.54, 88.33),
    (32.21, 86.89),
    (29.00, 85.16),
    (25.93, 83.12),
    (23.02, 80.79),
    (20.29, 78.17),
    (17.81, 75.30),
    (15.64, 72.27),
    (13.77, 69.10),
    (12.21, 65.80),
    (10.95, 62.40),
    (10.01, 58.92),
    (9.37, 55.38),
    (9.04, 51.80),
    (9.03, 48.21),
    (9.33, 44.63),
    (9.94, 41.08),
    (10.86, 37.57),
    (12.10, 34.14),
    (13.66, 30.80),
    (15.54, 27.58),
    (17.73, 24.49),
    (30.27, 33.69),
    (29.16, 35.17),
    (28.17, 36.71),
    (27.29, 38.31),
    (26.54, 39.95),
    (25.90, 41.63),
    (25.39, 43.35),
    (24.99, 45.10),
    (24.72, 46.87),
    (24.57, 48.65),
    (24.54, 50.44),
    (24.64, 52.23),
    (24.86, 54.01),
    (25.21, 55.79),
    (25.68, 57.54),
    (26.28, 59.27),
    (27.01, 60.97),
    (27.86, 62.62),
    (28.82, 64.18),
    (29.87, 65.66),
    (31.02, 67.06),
    (32.26, 68.37),
    (33.58, 69.58),
    (34.98, 70.70),
    (36.45, 71.71),
    (37.99, 72.62),
    (39.58, 73.43),
    (41.24, 74.12),
    (42.94, 74.70),
    (44.69, 75.16),
    (46.48, 75.50),
    (48.30, 75.72),
    (50.14, 75.80),
    (50.14, 66.01),
]
left_arrow = _sc(left_arrow_raw)
polygon(left_arrow, style=no_border_fill(MLFLOW_CYAN))
draw_round_polyline(left_arrow, width_units=w, color=DARK, closed=True)

# 2. Right sweeping cerulean-blue crescent arrow (180-degree symmetric, #45A4E5, softened #0194E2)
right_arrow = [(100.0 - x, 100.0 - y) for x, y in left_arrow]
polygon(right_arrow, style=no_border_fill(MLFLOW_BLUE))
draw_round_polyline(right_arrow, width_units=w, color=DARK, closed=True)

save()
