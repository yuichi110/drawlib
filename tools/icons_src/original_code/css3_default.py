# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: css3."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 2.0
w_inner = 1.3
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


outer_shield = _sc([(20.43, 17.2), (13.85, 91.0), (86.15, 91.0), (79.57, 17.21), (49.96, 9.0)])
inner_right = _sc([(50.0, 15.27), (73.93, 21.91), (79.56, 84.97), (50.0, 84.97)])

three_tr_mr = _sc([(50.0, 58.23), (61.98, 58.23), (62.81, 67.5), (50.0, 67.5), (50.0, 76.55), (72.7, 76.55), (72.48, 74.12), (70.26, 49.18), (50.0, 49.18)])
three_bl = _sc([(50.05, 34.72), (50.01, 34.71), (39.93, 37.43), (39.29, 44.65), (30.2, 44.65), (31.47, 30.44), (50.01, 25.29), (50.05, 25.3)])
three_br = _sc([(61.21, 49.56), (60.12, 37.44), (50.02, 34.71), (50.02, 25.29), (68.58, 30.44), (68.72, 31.97), (70.29, 49.56)])
three_tl = _sc([(50.03, 76.55), (50.03, 67.5), (28.17, 67.5), (27.99, 69.53), (27.57, 74.12), (27.36, 76.55)])
three_ml = _sc([(50.0, 58.23), (50.0, 49.17), (40.05, 49.17), (39.87, 51.21), (39.45, 55.8), (39.24, 58.23)])

three_outline = _sc([
    (27.36, 76.55), (72.7, 76.55), (68.58, 30.44), (50.01, 25.29),
    (31.47, 30.44), (30.2, 44.65), (39.29, 44.65), (39.93, 37.43),
    (50.01, 34.71), (60.12, 37.44), (61.18, 49.18), (40.05, 49.17),
    (39.24, 58.23), (61.98, 58.23), (62.81, 67.5), (28.17, 67.5),
])
# fmt: on

# 1. Flat pastel blue shield halves
polygon(outer_shield, style=no_border_fill("#4F94D4"))
polygon(inner_right, style=no_border_fill("#6EAEE6"))
draw_round_polyline(inner_right, width_units=w_inner, color=DARK, closed=True)

# 2. WHITE and #F2F4F7 '3' chevrons
polygon(three_tl, style=no_border_fill("#F2F4F7"))
polygon(three_ml, style=no_border_fill("#F2F4F7"))
polygon(three_bl, style=no_border_fill("#F2F4F7"))
polygon(three_tr_mr, style=no_border_fill(WHITE))
polygon(three_br, style=no_border_fill(WHITE))

# 3. Crisp DARK outlines on '3' and outer shield
draw_round_polyline(three_outline, width_units=w_inner, color=DARK, closed=True)
draw_round_polyline(outer_shield, width_units=w_outer, color=DARK, closed=True)

save()
