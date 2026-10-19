# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: burp_suite."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
Icon.setup()

w = 2.0
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# fmt: off
outer_sq = _sc([(9.0, 9.0), (91.0, 9.0), (91.0, 91.0), (9.0, 91.0)])

left_half = _sc([
    (9.0, 91.0), (48.59, 91.0), (48.59, 86.0), (20.98, 59.67),
    (48.59, 59.67), (48.59, 37.38), (71.14, 37.38), (48.59, 15.02),
    (48.59, 9.0), (9.0, 9.0),
])

right_half = _sc([
    (52.31, 91.0), (91.0, 91.0), (91.0, 9.0), (52.31, 9.0),
    (52.31, 13.8), (80.62, 41.93), (52.31, 41.93), (52.31, 64.16),
    (31.61, 64.16), (52.31, 85.04),
])
# fmt: on

# 1. White square base so the lightning-step zig-zag channel is WHITE
polygon(outer_sq, style=Icon.no_border_fill(Icon.WHITE))

# 2. Left half in dark slate (Colors.Gray6) and right half in pastel orange (Colors.Orange3)
polygon(left_half, style=Icon.no_border_fill(Colors.Gray6))
polygon(right_half, style=Icon.no_border_fill(Colors.Orange3))

# 3. DARK w=1.9 outlines on both halves and the outer square badge
Icon.draw_round_polyline(left_half, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(right_half, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(outer_sq, width_units=w, color=Icon.DARK, closed=True)

save()
