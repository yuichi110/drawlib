# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: pandas."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


navy_bars = [
    _sc([(24.22, 70.85), (33.18, 70.85), (33.18, 9.0), (24.22, 9.0)]),
    _sc([(38.62, 86.15), (47.58, 86.15), (47.58, 67.55), (38.62, 67.55)]),
    _sc([(38.62, 47.93), (47.58, 47.93), (47.58, 29.32), (38.62, 29.32)]),
    _sc([(52.72, 70.83), (61.68, 70.83), (61.68, 52.22), (52.72, 52.22)]),
    _sc([(52.72, 32.58), (61.68, 32.58), (61.68, 13.96), (52.72, 13.96)]),
    _sc([(66.82, 91.0), (75.78, 91.0), (75.78, 29.15), (66.82, 29.15)]),
]

yellow_block = _sc([(38.62, 62.11), (47.58, 62.11), (47.58, 53.33), (38.62, 53.33)])
pink_block = _sc([(52.72, 46.79), (61.68, 46.79), (61.68, 38.01), (52.72, 38.01)])
# fmt: on

# 1. Pastel navy vertical bars
for bar in navy_bars:
    polygon(bar, style=Icon.no_border_fill("#3B4278"))
    Icon.draw_round_polyline(bar, width_units=w, color=Icon.DARK, closed=True)

# 2. Pastel yellow and pink accent squares
polygon(yellow_block, style=Icon.no_border_fill("#F1C946"))
Icon.draw_round_polyline(yellow_block, width_units=w, color=Icon.DARK, closed=True)

polygon(pink_block, style=Icon.no_border_fill("#EF4E8E"))
Icon.draw_round_polyline(pink_block, width_units=w, color=Icon.DARK, closed=True)

save()
