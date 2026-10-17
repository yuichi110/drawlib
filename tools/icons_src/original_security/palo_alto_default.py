# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: palo_alto."""

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

setup_icon()

w = 1.9
w_inner = 1.6
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# 1. Pastel coral-orange circular badge
circle(
    (50.0, 50.0),
    radius=40.0,
    style=fill_style(Colors.Orange3, border_color=DARK, border_units=w),
)

# 2. Three WHITE angled diamond bars inside
bar_mid = _sc(
    [
        (56.48, 66.14),
        (50.03, 59.69),
        (53.24, 56.48),
        (37.07, 40.31),
        (43.52, 33.86),
        (49.97, 40.31),
        (46.76, 43.51),
        (62.93, 59.69),
    ]
)
bar_tl = _sc(
    [
        (27.42, 49.97),
        (43.58, 66.14),
        (50.03, 59.69),
        (33.86, 43.52),
    ]
)
bar_br = _sc(
    [
        (49.97, 40.31),
        (66.14, 56.48),
        (72.58, 50.03),
        (56.42, 33.86),
    ]
)

for bar_pts in (bar_tl, bar_br, bar_mid):
    polygon(bar_pts, style=no_border_fill(WHITE))
    draw_round_polyline(bar_pts, width_units=w_inner, color=DARK, closed=True)

save()
