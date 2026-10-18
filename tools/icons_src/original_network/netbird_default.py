# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: netbird."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
s = 0.95


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


_RAW_RIGHT_WING: list[tuple[float, float]] = [
    (67.29, 79.81),
    (65.84, 79.63),
    (64.47, 79.4),
    (63.17, 79.1),
    (61.93, 78.74),
    (60.77, 78.34),
    (59.68, 77.9),
    (58.65, 77.41),
    (57.68, 76.9),
    (56.78, 76.36),
    (55.94, 75.8),
    (55.16, 75.22),
    (54.44, 74.63),
    (53.77, 74.05),
    (53.17, 73.46),
    (52.61, 72.88),
    (52.11, 72.32),
    (51.66, 71.77),
    (51.27, 71.26),
    (50.92, 70.77),
    (50.61, 70.32),
    (49.68, 68.67),
    (21.68, 20.19),
    (56.58, 20.19),
    (91.0, 79.81),
]

_RAW_LEFT_WING: list[tuple[float, float]] = [
    (56.58, 20.19),
    (9.0, 70.68),
    (10.51, 71.04),
    (12.29, 71.4),
    (14.64, 71.82),
    (17.49, 72.23),
    (20.77, 72.58),
    (24.39, 72.81),
    (28.28, 72.88),
    (32.37, 72.71),
    (36.57, 72.26),
    (40.81, 71.48),
    (45.01, 70.3),
    (49.09, 68.67),
    (52.99, 66.53),
    (56.62, 63.84),
    (59.91, 60.53),
    (62.77, 56.55),
    (65.13, 51.84),
    (66.92, 46.34),
    (68.06, 40.02),
]

right_wing = _sc(_RAW_RIGHT_WING)
left_wing = _sc(_RAW_LEFT_WING)
crease_bot, crease_top = _sc([(34.94, 43.16), (49.54, 68.45)])

# 1. Right wing in Colors.Orange4
polygon(right_wing, style=no_border_fill(Colors.Orange4))
draw_round_polyline(right_wing, width_units=w, color=DARK, closed=True)

# 2. Left wing in Colors.Orange3
polygon(left_wing, style=no_border_fill(Colors.Orange3))
draw_round_polyline(left_wing, width_units=w, color=DARK, closed=True)

# 3. Inner wing overlap line
draw_round_segment(crease_bot, crease_top, width_units=1.6, color=DARK)

save()
