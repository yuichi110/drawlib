# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: auth0."""

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
# fmt: off
setup_icon()

w_outer = 1.9
w_inner = 1.8
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


shield_outer = _sc([
    (23.06, 91.0),
    (50.0, 91.0),
    (76.96, 91.0),
    (85.29, 65.66), (85.94, 63.44), (86.44, 61.2), (86.81, 58.94),
    (87.02, 56.68), (87.09, 54.39), (87.03, 52.13), (86.81, 49.87),
    (86.46, 47.64), (85.98, 45.43), (85.36, 43.25), (84.59, 41.1),
    (83.7, 38.99), (82.67, 36.96), (81.51, 34.97), (80.21, 33.05),
    (78.79, 31.19), (77.23, 29.42), (75.55, 27.74), (73.74, 26.16),
    (71.79, 24.67),
    (50.0, 9.0),
    (28.21, 24.67), (26.34, 26.07), (24.61, 27.59), (22.97, 29.21),
    (21.44, 30.92), (20.03, 32.72), (18.75, 34.59), (17.57, 36.53),
    (16.52, 38.55), (15.6, 40.62), (14.8, 42.75), (14.15, 44.93),
    (13.63, 47.14), (13.24, 49.4), (13.0, 51.69), (12.91, 54.0),
    (12.96, 56.32), (13.16, 58.65), (13.52, 60.99), (14.05, 63.34),
    (14.73, 65.67),
])

star_pts = _sc([
    (50.0, 91.0),
    (58.33, 65.66),
    (85.28, 65.66),
    (63.47, 50.0),
    (71.79, 24.67),
    (50.01, 40.33),
    (28.20, 24.67),
    (36.52, 50.0),
    (14.73, 65.67),
    (41.67, 65.66),
])
# fmt: on

# 1. Pastel orange shield base
polygon(shield_outer, style=no_border_fill(Colors.Orange3))

# 2. White internal 5-pointed star + DARK facet outlines
polygon(star_pts, style=no_border_fill(WHITE))
draw_round_polyline(star_pts, width_units=w_inner, color=DARK, closed=True)

# 3. Outer shield DARK border
draw_round_polyline(shield_outer, width_units=w_outer, color=DARK, closed=True)

save()
