# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: pagerduty."""

from drawlib.canvas import save
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    setup_icon,
)

setup_icon()

w = 1.9
s = 38.8 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale points around (50, 50) to fit safely within [10, 90]."""
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


stem_ring = _sc([(33.79, 30.84), (33.79, 9.0), (21.75, 9.0), (21.75, 30.84)])

outer_p_ring = _sc(
    [
        (45.82, 91.0),
        (51.37, 90.91),
        (55.89, 90.57),
        (59.75, 89.87),
        (63.31, 88.71),
        (66.96, 86.97),
        (69.92, 85.04),
        (72.48, 82.65),
        (74.61, 79.83),
        (76.29, 76.63),
        (77.47, 73.08),
        (78.13, 69.22),
        (78.25, 66.49),
        (78.02, 62.7),
        (77.31, 59.1),
        (76.14, 55.73),
        (74.52, 52.64),
        (72.44, 49.84),
        (69.92, 47.4),
        (67.06, 45.38),
        (64.17, 43.9),
        (61.13, 42.82),
        (57.9, 42.08),
        (54.45, 41.62),
        (50.76, 41.38),
        (45.41, 41.29),
        (21.75, 41.29),
        (21.75, 91.0),
    ]
)

inner_p_hole = _sc(
    [
        (47.38, 80.46),
        (33.79, 80.36),
        (33.79, 51.69),
        (48.17, 51.69),
        (51.12, 51.81),
        (53.89, 52.19),
        (56.45, 52.85),
        (58.78, 53.79),
        (60.83, 55.03),
        (62.58, 56.6),
        (64.0, 58.49),
        (65.05, 60.74),
        (65.71, 63.36),
        (65.93, 66.35),
        (65.75, 69.15),
        (65.19, 71.63),
        (64.26, 73.78),
        (62.96, 75.62),
        (61.29, 77.15),
        (59.25, 78.38),
        (56.84, 79.32),
        (54.05, 79.98),
        (50.9, 80.35),
    ]
)

draw_compound_polygon([stem_ring, outer_p_ring, inner_p_hole], color=Colors.Green3)

for ring in (stem_ring, outer_p_ring, inner_p_hole):
    draw_round_polyline(ring, width_units=w, color=DARK, closed=True)

save()
