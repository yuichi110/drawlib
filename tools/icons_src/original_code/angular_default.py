# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: angular."""

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

w = 1.7
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


left_wing = _sc([(40.84, 91.0), (11.24, 77.35), (14.06, 33.41)])
right_wing = _sc([(59.16, 91.0), (88.76, 77.35), (85.94, 33.41)])
center_tri = _sc([(50.0, 69.15), (39.43, 43.4), (60.57, 43.4)])
bottom_base = _sc([(33.92, 30.46), (29.82, 20.53), (50.0, 9.0), (70.18, 20.53), (66.14, 30.46)])
# fmt: on

# 1. Left wing in pastel red-pink
polygon(left_wing, style=no_border_fill("#F2727F"))
draw_round_polyline(left_wing, width_units=w, color=DARK, closed=True)

# 2. Right wing in pastel magenta-pink
polygon(right_wing, style=no_border_fill("#E66AB2"))
draw_round_polyline(right_wing, width_units=w, color=DARK, closed=True)

# 3. Center triangle and bottom base in pastel purple
polygon(center_tri, style=no_border_fill("#B37CF5"))
draw_round_polyline(center_tri, width_units=w, color=DARK, closed=True)

polygon(bottom_base, style=no_border_fill("#B37CF5"))
draw_round_polyline(bottom_base, width_units=w, color=DARK, closed=True)

save()
