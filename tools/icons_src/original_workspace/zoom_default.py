# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: zoom."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import DARK, WHITE, draw_round_polyline, fill_style, no_border_fill, setup_icon

setup_icon()
w = 2.0
w_inner = 1.8

cam_body = [
    (33.97, 38.91),
    (59.62, 38.91),
    (59.62, 57.73),
    (59.61, 58.08),
    (59.58, 58.42),
    (59.52, 58.76),
    (59.44, 59.09),
    (59.34, 59.42),
    (59.22, 59.73),
    (59.08, 60.03),
    (58.92, 60.32),
    (58.74, 60.60),
    (58.55, 60.86),
    (58.35, 61.12),
    (58.12, 61.37),
    (57.87, 61.58),
    (57.63, 61.79),
    (57.35, 61.99),
    (57.08, 62.17),
    (56.79, 62.32),
    (56.48, 62.46),
    (56.17, 62.59),
    (55.85, 62.68),
    (55.52, 62.77),
    (55.19, 62.82),
    (54.84, 62.85),
    (54.49, 62.87),
    (28.84, 62.87),
    (28.84, 44.05),
    (28.86, 43.69),
    (28.89, 43.35),
    (28.94, 43.01),
    (29.03, 42.68),
    (29.12, 42.35),
    (29.25, 42.04),
    (29.38, 41.74),
    (29.54, 41.45),
    (29.71, 41.17),
    (29.91, 40.91),
    (30.12, 40.65),
    (30.34, 40.41),
    (30.58, 40.19),
    (30.84, 39.98),
    (31.10, 39.79),
    (31.38, 39.61),
    (31.67, 39.45),
    (31.97, 39.31),
    (32.28, 39.19),
    (32.60, 39.09),
    (32.93, 39.01),
    (33.27, 38.96),
    (33.61, 38.92),
]
cam_lens = [
    (63.05, 45.76),
    (73.31, 38.92),
    (73.31, 62.87),
    (63.05, 56.02),
]

circle((50.0, 50.0), radius=38.8, style=fill_style("#51A8F2", border_color=DARK, border_units=w))

for pts in (cam_body, cam_lens):
    polygon(pts, style=no_border_fill(WHITE))
    draw_round_polyline(pts, width_units=w_inner, color=DARK, closed=True)

save()
