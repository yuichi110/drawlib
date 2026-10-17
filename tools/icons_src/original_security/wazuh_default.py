# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: wazuh."""

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

w = 1.9
w_inner = 1.4
r_badge = 40.0
s = r_badge / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


# 1. Pastel blue circular badge with DARK w=1.9 border
circle(
    (50.0, 50.0),
    radius=r_badge,
    style=fill_style(Colors.Blue3, border_color=DARK, border_units=w),
)

# 2. WHITE 'W' letter with DARK 1.4 outline
w_pts = _sc(
    [
        (52.34, 34.78),
        (45.32, 57.02),
        (38.28, 34.78),
        (33.02, 34.78),
        (23.64, 65.82),
        (29.5, 65.82),
        (35.94, 44.72),
        (42.38, 65.82),
        (47.66, 65.82),
        (54.1, 44.72),
        (60.54, 65.82),
        (66.4, 65.82),
        (57.62, 34.78),
    ]
)
polygon(w_pts, style=no_border_fill(WHITE))
draw_round_polyline(w_pts, width_units=w_inner, color=DARK, closed=True)

# 3. WHITE period dot with DARK 1.4 outline
dot_xy = _sc([(71.09, 38.87)])[0]
circle(
    dot_xy,
    radius=4.69 * s,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
)

save()
