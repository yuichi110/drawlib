# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: nextjs."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors, Style
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    pt,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 2.0
w_inner = 1.2
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


n_main = _sc([
    (33.6, 33.61),
    (33.6, 66.4),
    (40.5, 66.4),
    (76.88, 19.54),
    (75.5, 18.25),
    (74.08, 17.13),
    (72.62, 16.1),
    (39.12, 59.39),
    (39.12, 33.61),
])

n_right = _sc([
    (61.39, 42.3),
    (61.39, 66.4),
    (66.85, 66.4),
    (66.85, 42.3),
])
# fmt: on

# 1. Flat dark slate circle fill
circle((50.0, 50.0), radius=40.0, style=no_border_fill("#3E4756"))

# 2. WHITE 'N' bars with DARK outlines
polygon(n_main, style=no_border_fill(WHITE))
draw_round_polyline(n_main, width_units=w_inner, color=DARK, closed=True)

polygon(n_right, style=no_border_fill(WHITE))
draw_round_polyline(n_right, width_units=w_inner, color=DARK, closed=True)

# 3. Outer circle DARK border on top
circle(
    (50.0, 50.0),
    radius=40.0,
    style=Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=DARK,
        shape_line_width=pt(w_outer),
        shape_line_style="solid",
    ),
)

save()
