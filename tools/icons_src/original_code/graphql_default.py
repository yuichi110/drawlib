# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: graphql."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0
s = 40.0 / 41.0
PINK = "#F04A9D"


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


bars = [
    _sc([(20.15, 28.5), (17.14, 30.24), (50.68, 88.32), (53.69, 86.59)]),
    _sc([(16.45, 34.88), (83.52, 34.88), (83.52, 31.41), (16.45, 31.41)]),
    _sc([(51.33, 13.56), (17.78, 32.93), (19.52, 35.94), (53.07, 16.57)]),
    _sc([(80.47, 64.04), (46.93, 83.41), (48.66, 86.42), (82.21, 67.05)]),
    _sc([(19.53, 64.05), (17.79, 67.06), (51.34, 86.43), (53.08, 83.42)]),
    _sc([(79.85, 28.5), (46.32, 86.59), (49.33, 88.32), (82.86, 30.24)]),
    _sc([(19.11, 69.37), (22.59, 69.37), (22.59, 30.63), (19.11, 30.63)]),
    _sc([(77.41, 69.37), (80.89, 69.37), (80.89, 30.63), (77.41, 30.63)]),
    _sc([(50.74, 15.03), (49.22, 17.66), (78.4, 34.51), (79.91, 31.88)]),
]

node_centers = _sc([
    (50.0, 83.69),
    (79.18, 66.85),
    (79.17, 33.16),
    (50.0, 16.31),
    (20.84, 33.16),
    (20.82, 66.85),
])
node_r = 7.31 * s
# fmt: on

# 1. Hexagon edges and inner triangle chords
for bar in bars:
    polygon(bar, style=Icon.no_border_fill(PINK))
    Icon.draw_round_polyline(bar, width_units=w, color=Icon.DARK, closed=True)

# 2. Six circular nodes on top
node_style = Icon.fill_style(PINK, border_color=Icon.DARK, border_units=w)
for cx, cy in node_centers:
    circle((cx, cy), radius=node_r, style=node_style)

save()
