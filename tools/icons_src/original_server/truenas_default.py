# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: truenas (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = 2.0
s = 0.95


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


_BLOCKS = [
    ([(91.0, 56.65), (91.0, 39.22), (53.59, 17.66), (53.59, 35.09)], "#51BCF2"),
    ([(46.44, 35.09), (46.44, 17.66), (9.0, 39.22), (9.0, 56.65)], "#46A0ED"),
    ([(65.14, 49.99), (50.01, 41.27), (34.87, 49.99), (50.01, 58.72)], "#91A0B4"),
    ([(87.44, 62.83), (72.29, 54.11), (53.59, 64.9), (53.59, 82.34)], "#46A0ED"),
    ([(46.44, 82.34), (46.44, 64.9), (27.71, 54.12), (12.56, 62.83)], "#51BCF2"),
]

for raw_pts, fill_col in _BLOCKS:
    pts = _sc(raw_pts)
    polygon(pts, style=Icon.no_border_fill(fill_col))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
