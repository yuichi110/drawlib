# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: lxc."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, draw_round_segment, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.5
w_inner = 1.3

orange_faces: list[list[tuple[float, float]]] = [
    [(11.0, 50.22), (49.45, 28.03), (49.45, 13.38), (11.0, 35.58)],
    [(49.56, 27.99), (89.0, 49.34), (89.0, 34.71), (49.56, 13.34)],
]
mid_gray_faces: list[list[tuple[float, float]]] = [
    [(11.0, 57.7), (49.45, 35.5), (49.45, 28.17), (11.0, 50.38)],
    [(49.81, 57.26), (69.04, 46.16), (49.4, 35.53), (30.17, 46.63)],
    [(49.51, 35.3), (69.18, 45.94), (69.18, 38.62), (49.51, 27.97)],
]
dark_gray_faces: list[list[tuple[float, float]]] = [
    [(50.39, 86.66), (88.86, 64.46), (69.21, 53.82), (30.76, 76.03)],
    [(69.4, 53.68), (88.98, 64.28), (88.98, 49.63), (69.4, 39.03)],
    [(50.0, 64.71), (69.23, 53.61), (69.23, 46.28), (50.0, 57.39)],
]
light_gray_faces: list[list[tuple[float, float]]] = [
    [(30.76, 76.03), (49.98, 64.92), (30.35, 54.29), (11.11, 65.39)],
    [(11.0, 65.2), (30.22, 54.1), (30.22, 46.77), (11.0, 57.87)],
    [(30.22, 54.15), (49.89, 64.8), (49.89, 57.47), (30.22, 46.82)],
]
inner_creases: list[tuple[tuple[float, float], tuple[float, float]]] = [
    ((30.97, 75.94), (30.71, 68.08)),
    ((50.25, 57.17), (30.71, 68.08)),
    ((30.71, 68.08), (10.92, 57.93)),
]

for pts in orange_faces:
    polygon(pts, style=no_border_fill("#F07C54"))
for pts in mid_gray_faces:
    polygon(pts, style=no_border_fill("#9BA8B8"))
for pts in dark_gray_faces:
    polygon(pts, style=no_border_fill("#5E6B7C"))
for pts in light_gray_faces:
    polygon(pts, style=no_border_fill("#DCE3EB"))

for p1, p2 in inner_creases:
    draw_round_segment(p1, p2, width_units=w_inner, color=DARK)

for group in (orange_faces, mid_gray_faces, dark_gray_faces, light_gray_faces):
    for pts in group:
        draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
# fmt: on
