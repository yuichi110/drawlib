# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: veracode."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
setup_icon()

w = 2.0
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


left_arm = _sc([(27.45, 91.0), (9.06, 91.0), (37.61, 11.99), (46.1, 36.73)])
right_arm = _sc([(72.55, 91.0), (90.94, 91.0), (61.3, 9.0), (44.33, 9.0)])

# 1. Left arm in dark slate (Colors.Gray6) with DARK w=1.9 outline
polygon(left_arm, style=no_border_fill(Colors.Gray6))
draw_round_polyline(left_arm, width_units=w, color=DARK, closed=True)

# 2. Right arm in pastel blue (Colors.Blue3) with DARK w=1.9 outline
polygon(right_arm, style=no_border_fill(Colors.Blue3))
draw_round_polyline(right_arm, width_units=w, color=DARK, closed=True)

save()
