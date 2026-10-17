# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: dotnet."""

from drawlib.canvas import save
from drawlib.shapes import polygon
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
w_letter = 1.1
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


INDIGO_PURPLE = "#7E68E6"

badge = _sc([(9.0, 91.0), (91.0, 91.0), (91.0, 9.0), (9.0, 9.0)])

dot_pts = _sc([(23.62, 38.61), (23.2, 38.65), (22.81, 38.76), (22.46, 38.94), (22.14, 39.19), (21.87, 39.5), (21.68, 39.84), (21.57, 40.21), (21.53, 40.6), (21.57, 41.0), (21.68, 41.38), (21.87, 41.72), (22.14, 42.03), (22.46, 42.29), (22.81, 42.48), (23.2, 42.59), (23.62, 42.62), (24.04, 42.59), (24.43, 42.48), (24.79, 42.29), (25.11, 42.03), (25.38, 41.72), (25.58, 41.38), (25.69, 41.0), (25.73, 40.6), (25.69, 40.21), (25.58, 39.84), (25.38, 39.5), (25.11, 39.19), (24.79, 38.94), (24.43, 38.76), (24.04, 38.65)])
n_pts = _sc([(46.79, 38.94), (43.02, 38.94), (33.1, 54.6), (32.97, 54.8), (32.86, 55.0), (32.75, 55.2), (32.65, 55.41), (32.56, 55.62), (32.47, 55.84), (32.39, 55.84), (32.43, 55.5), (32.46, 55.04), (32.48, 54.45), (32.5, 53.74), (32.5, 52.91), (32.5, 38.94), (29.17, 38.94), (29.17, 60.25), (33.18, 60.25), (42.78, 44.96), (43.06, 44.52), (43.28, 44.15), (43.45, 43.86), (43.56, 43.65), (43.62, 43.65), (43.57, 44.04), (43.53, 44.51), (43.5, 45.09), (43.48, 45.76), (43.47, 46.52), (43.47, 60.25), (46.79, 60.25)])
e_pts = _sc([(63.03, 38.94), (51.36, 38.94), (51.36, 60.25), (62.56, 60.25), (62.56, 57.25), (54.81, 57.25), (54.81, 51.21), (61.96, 51.21), (61.96, 48.23), (54.81, 48.23), (54.81, 41.93), (63.03, 41.93)])
t_pts = _sc([(79.61, 57.25), (73.64, 57.25), (73.64, 38.94), (70.19, 38.94), (70.19, 57.25), (64.23, 57.25), (64.23, 60.25), (79.61, 60.25)])
# fmt: on

# 1. Flat pastel indigo-purple square fill
polygon(badge, style=no_border_fill(INDIGO_PURPLE))

# 2. WHITE '.NET' letters with DARK w=1.1 outlines
for pts in (dot_pts, n_pts, e_pts, t_pts):
    polygon(pts, style=no_border_fill(WHITE))
    draw_round_polyline(pts, width_units=w_letter, color=DARK, closed=True)

# 3. Crisp DARK w=1.9 outer border
draw_round_polyline(badge, width_units=w_outer, color=DARK, closed=True)

save()
