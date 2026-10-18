# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: vuejs."""

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

w = 2.0
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


outer_v = _sc([(9.0, 85.01), (25.29, 85.12), (50.08, 42.45), (74.68, 85.12), (91.0, 85.1), (50.08, 14.87)])
inner_v = _sc([(25.31, 85.13), (40.25, 85.12), (50.02, 68.9), (59.76, 85.12), (74.69, 85.12), (50.1, 42.46)])
# fmt: on

# 1. Pastel mint green outer 'V'
polygon(outer_v, style=no_border_fill("#68CEA1"))

# 2. Flat slate inner 'V'
polygon(inner_v, style=no_border_fill("#4A5D73"))

# 3. Crisp DARK outlines
draw_round_polyline(inner_v, width_units=w, color=DARK, closed=True)
draw_round_polyline(outer_v, width_units=w, color=DARK, closed=True)

save()
