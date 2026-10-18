# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: google_sheets."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()
w = 2.0
w_grid = 1.5

page_pts = [
    (58.82, 88.80),
    (27.07, 88.80),
    (26.38, 88.75),
    (25.70, 88.62),
    (25.05, 88.40),
    (24.43, 88.09),
    (23.85, 87.71),
    (23.33, 87.25),
    (22.87, 86.73),
    (22.49, 86.15),
    (22.18, 85.53),
    (21.96, 84.88),
    (21.83, 84.20),
    (21.78, 83.51),
    (21.78, 16.49),
    (21.83, 15.80),
    (21.96, 15.12),
    (22.18, 14.47),
    (22.49, 13.85),
    (22.87, 13.27),
    (23.33, 12.75),
    (23.85, 12.29),
    (24.43, 11.91),
    (25.05, 11.60),
    (25.70, 11.38),
    (26.38, 11.25),
    (27.07, 11.20),
    (72.93, 11.20),
    (73.62, 11.25),
    (74.30, 11.38),
    (74.95, 11.60),
    (75.57, 11.91),
    (76.15, 12.29),
    (76.67, 12.75),
    (77.13, 13.27),
    (77.51, 13.85),
    (77.82, 14.47),
    (78.04, 15.12),
    (78.17, 15.80),
    (78.22, 16.49),
    (78.22, 69.40),
]
fold_pts = [
    (58.82, 88.80),
    (78.22, 69.40),
    (58.82, 69.40),
]

grid_outer = [
    (32.36, 58.82),
    (32.36, 33.25),
    (67.64, 33.25),
    (67.64, 58.82),
]
hole_bl = [
    (47.80, 37.65),
    (36.77, 37.65),
    (36.77, 43.83),
    (47.80, 43.83),
]
hole_tl = [
    (47.80, 48.24),
    (36.77, 48.24),
    (36.77, 54.41),
    (47.80, 54.41),
]
hole_br = [
    (63.23, 37.65),
    (52.20, 37.65),
    (52.20, 43.83),
    (63.23, 43.83),
]
hole_tr = [
    (63.23, 48.24),
    (52.20, 48.24),
    (52.20, 54.41),
    (63.23, 54.41),
]

polygon(page_pts, style=no_border_fill("#71C789"))
draw_round_polyline(page_pts, width_units=w, color=DARK, closed=True)

polygon(fold_pts, style=no_border_fill("#60B078"))
draw_round_polyline(fold_pts, width_units=w, color=DARK, closed=True)

draw_compound_polygon([grid_outer, hole_bl, hole_tl, hole_br, hole_tr], color=WHITE)
for ring in (grid_outer, hole_bl, hole_tl, hole_br, hole_tr):
    draw_round_polyline(ring, width_units=w_grid, color=DARK, closed=True)

save()
