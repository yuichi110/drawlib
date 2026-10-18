# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: echo."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_facet = 2.0
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


TOP_SLATE = "#546E7A"
TOP_GRAY = "#CFD8DC"
LEFT_CYAN = "#4BB8D4"
RIGHT_CYAN = "#4BD0EF"

top_slate_facets = [
    _sc([(10.71, 82.44), (22.06, 88.86), (33.19, 82.44), (21.63, 76.01)]),
    _sc([(24.42, 74.51), (35.76, 81.15), (47.11, 74.51), (35.55, 68.31)]),
    _sc([(50.11, 73.44), (38.76, 66.81), (49.89, 60.6)]),
]

top_gray_facets = [
    _sc([(53.32, 74.73), (64.67, 81.37), (75.8, 74.73), (64.24, 68.31)]),
    _sc([(67.45, 82.65), (78.8, 89.29), (89.93, 82.65), (78.37, 76.44)]),
    _sc([(50.11, 73.44), (49.89, 60.6), (61.24, 66.81)]),
]

left_cyan_facets = [
    _sc([(9.0, 80.3), (9.0, 66.16), (20.35, 59.74), (20.35, 73.66)]),
    _sc([(23.13, 72.37), (23.13, 58.24), (34.69, 52.03), (34.69, 65.74)]),
    _sc([(37.05, 64.88), (37.05, 50.75), (48.39, 44.54), (48.39, 58.24)]),
    _sc([(9.0, 63.38), (9.0, 49.25), (20.35, 43.04), (20.35, 56.74)]),
    _sc([(23.13, 55.67), (23.13, 41.54), (34.69, 35.12), (34.69, 48.82)]),
    _sc([(37.05, 48.18), (37.05, 34.05), (48.39, 27.84), (48.39, 41.54)]),
    _sc([(9.0, 46.68), (9.0, 32.55), (20.35, 26.13), (20.35, 40.04)]),
    _sc([(23.13, 38.76), (23.13, 24.63), (34.69, 18.42), (34.69, 32.12)]),
    _sc([(37.05, 31.27), (37.05, 17.14), (48.39, 10.93), (48.39, 24.63)]),
]

right_cyan_facets = [
    _sc([(91.0, 80.08), (91.0, 65.95), (79.44, 59.53), (79.44, 73.44)]),
    _sc([(76.66, 72.16), (76.66, 58.03), (65.31, 51.82), (65.31, 65.52)]),
    _sc([(62.74, 64.67), (62.74, 50.54), (51.39, 44.33), (51.39, 58.03)]),
    _sc([(91.0, 63.17), (91.0, 49.04), (79.44, 42.83), (79.44, 56.53)]),
    _sc([(76.66, 55.25), (76.66, 41.11), (65.31, 34.91), (65.31, 48.61)]),
    _sc([(62.74, 47.97), (62.74, 33.84), (51.39, 27.63), (51.39, 41.33)]),
    _sc([(91.0, 46.47), (91.0, 32.34), (79.44, 25.91), (79.44, 39.62)]),
    _sc([(76.66, 38.55), (76.66, 24.42), (65.31, 18.21), (65.31, 31.91)]),
    _sc([(62.74, 31.05), (62.74, 16.92), (51.39, 10.71), (51.39, 24.42)]),
]
# fmt: on

for pts in top_slate_facets:
    polygon(pts, style=no_border_fill(TOP_SLATE))

for pts in top_gray_facets:
    polygon(pts, style=no_border_fill(TOP_GRAY))

for pts in left_cyan_facets:
    polygon(pts, style=no_border_fill(LEFT_CYAN))

for pts in right_cyan_facets:
    polygon(pts, style=no_border_fill(RIGHT_CYAN))

for pts in (
    *top_slate_facets,
    *top_gray_facets,
    *left_cyan_facets,
    *right_cyan_facets,
):
    draw_round_polyline(pts, width_units=w_facet, color=DARK, closed=True)

save()
