# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: metasploit."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
setup_icon()

w = 2.0
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# fmt: off
shield_left = _sc([
    (50.0, 91.0), (44.62, 90.8), (39.56, 90.34), (34.37, 89.46),
    (26.7, 87.66), (22.91, 86.56), (19.08, 85.18), (19.08, 40.28),
    (19.39, 39.12), (20.03, 37.72), (20.9, 35.75), (22.03, 34.3),
    (24.31, 31.23), (28.66, 26.75), (32.7, 23.17), (40.35, 16.59),
    (50.0, 9.0),
])

shield_right = _sc([
    (50.0, 91.0), (55.38, 90.8), (60.44, 90.34), (65.63, 89.46),
    (73.3, 87.66), (77.09, 86.56), (80.92, 85.18), (80.92, 40.28),
    (80.61, 39.12), (79.97, 37.72), (79.1, 35.75), (77.97, 34.3),
    (75.69, 31.23), (71.34, 26.75), (67.3, 23.17), (59.65, 16.59),
    (50.0, 9.0),
])

shield_outer = shield_left + list(reversed(shield_right[1:-1]))

m_mark = _sc([
    (24.7, 80.71), (34.88, 80.71), (49.99, 66.56), (65.11, 80.71),
    (75.28, 80.71), (75.28, 46.3), (75.1, 44.34), (74.75, 41.65),
    (74.11, 39.12), (73.32, 37.33), (72.2, 35.47), (70.03, 32.77),
    (67.66, 30.16), (65.11, 27.56), (65.11, 65.29), (54.41, 56.2),
    (54.41, 40.49), (45.12, 40.49), (45.12, 56.2), (34.88, 65.29),
    (34.88, 27.56), (32.33, 30.16), (29.96, 32.77), (27.78, 35.47),
    (26.67, 37.33), (25.89, 39.05), (25.24, 41.65), (24.88, 44.34),
    (24.7, 46.3),
])
# fmt: on

# 1. Two-tone pastel blue shield fill (Colors.Blue3 left, Colors.Blue4 right)
polygon(shield_left, style=no_border_fill(Colors.Blue3))
polygon(shield_right, style=no_border_fill(Colors.Blue4))

# 2. Outer shield DARK w=1.8 outline
draw_round_polyline(shield_outer, width_units=w, color=DARK, closed=True)

# 3. Bold WHITE 'M' mark with DARK w=1.8 outline
polygon(m_mark, style=no_border_fill(WHITE))
draw_round_polyline(m_mark, width_units=w, color=DARK, closed=True)

save()
