# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: yubico."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
setup_icon()

w_badge = 2.0
w_letter = 1.5
s = 0.96


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


y_letter = _sc([
    (50.31, 51.23),
    (57.86, 72.63),
    (68.76, 72.63),
    (50.37, 27.37),
    (38.85, 27.37),
    (44.12, 39.76),
    (31.24, 72.6),
    (42.37, 72.6),
])

# 1. Pastel lime-green circular badge (Colors.Green3 + DARK w=1.9 border)
circle((50.0, 50.0), radius=41.0 * s, style=fill_style(Colors.Green3, border_color=DARK, border_units=w_badge))

# 2. White 'y' letter (WHITE + DARK 1.5 outline)
polygon(y_letter, style=no_border_fill(WHITE))
draw_round_polyline(y_letter, width_units=w_letter, color=DARK, closed=True)

save()
