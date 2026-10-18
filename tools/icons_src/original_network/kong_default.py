# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: kong."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

setup_icon()

w = 2.0

facets = [
    (
        [
            (34.86, 24.39),
            (36.82, 26.91),
            (51.31, 26.91),
            (58.87, 17.26),
            (57.52, 13.99),
            (38.83, 13.99),
            (39.28, 17.26),
        ],
        Colors.Teal3,
    ),
    (
        [
            (39.29, 57.30),
            (46.29, 69.39),
            (54.44, 69.39),
            (91.00, 26.93),
            (88.17, 13.99),
            (72.49, 13.99),
            (73.47, 17.62),
        ],
        Colors.Teal3,
    ),
    (
        [
            (47.78, 71.69),
            (51.13, 77.89),
            (61.19, 86.01),
            (78.41, 72.51),
            (76.18, 70.23),
            (79.18, 66.08),
            (79.18, 61.64),
            (70.60, 54.62),
            (56.19, 71.69),
        ],
        Colors.Green3,
    ),
    (
        [
            (21.16, 44.68),
            (25.71, 44.68),
            (37.59, 54.62),
            (53.32, 36.33),
            (48.89, 29.67),
            (34.36, 29.67),
            (24.33, 16.92),
            (22.03, 13.99),
            (9.00, 13.99),
            (9.00, 29.62),
        ],
        Colors.Teal2,
    ),
]

for pts, col in facets:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
