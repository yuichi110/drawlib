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
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.7
s = 0.95


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


_BLOCKS = [
    ([(91.0, 56.65), (91.0, 39.22), (53.59, 17.66), (53.59, 35.09)], "#72C7F2"),
    ([(46.44, 35.09), (46.44, 17.66), (9.0, 39.22), (9.0, 56.65)], "#58A6E8"),
    ([(65.14, 49.99), (50.01, 41.27), (34.87, 49.99), (50.01, 58.72)], "#A6B2C2"),
    ([(87.44, 62.83), (72.29, 54.11), (53.59, 64.9), (53.59, 82.34)], "#58A6E8"),
    ([(46.44, 82.34), (46.44, 64.9), (27.71, 54.12), (12.56, 62.83)], "#72C7F2"),
]

for raw_pts, fill_col in _BLOCKS:
    pts = _sc(raw_pts)
    polygon(pts, style=no_border_fill(fill_col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
