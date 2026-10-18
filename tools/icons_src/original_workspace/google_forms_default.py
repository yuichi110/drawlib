# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: google_forms."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import DARK, WHITE, draw_round_polyline, fill_style, no_border_fill, setup_icon

setup_icon()
w = 2.0
w_inner = 1.6

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

bar1 = [
    (43.83, 33.25),
    (65.87, 33.25),
    (65.87, 37.65),
    (43.83, 37.65),
]
bar2 = [
    (43.83, 43.83),
    (65.87, 43.83),
    (65.87, 48.24),
    (43.83, 48.24),
]
bar3 = [
    (43.83, 54.41),
    (65.87, 54.41),
    (65.87, 58.82),
    (43.83, 58.82),
]

dot_centers = [(36.77, 35.45), (36.77, 46.03), (36.77, 56.61)]

polygon(page_pts, style=no_border_fill("#B388EB"))
draw_round_polyline(page_pts, width_units=w, color=DARK, closed=True)

polygon(fold_pts, style=no_border_fill("#9568D4"))
draw_round_polyline(fold_pts, width_units=w, color=DARK, closed=True)

for cx, cy in dot_centers:
    circle((cx, cy), radius=2.65, style=fill_style(WHITE, border_color=DARK, border_units=w_inner))

for b_pts in (bar1, bar2, bar3):
    polygon(b_pts, style=no_border_fill(WHITE))
    draw_round_polyline(b_pts, width_units=w_inner, color=DARK, closed=True)

save()
