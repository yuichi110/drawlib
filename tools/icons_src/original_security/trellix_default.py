# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: trellix."""

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


x_mark = _sc(
    [
        (74.49, 9.0),
        (26.65, 70.21),
        (9.37, 70.21),
        (33.28, 39.62),
        (9.37, 9.0),
        (26.65, 9.0),
        (41.92, 28.56),
        (57.21, 9.0),
    ]
)

slash_blue = _sc(
    [
        (41.76, 50.57),
        (59.04, 50.57),
        (70.51, 65.25),
        (61.50, 75.83),
    ]
)

slash_green = _sc(
    [
        (61.50, 75.83),
        (70.51, 65.25),
        (90.63, 91.0),
        (73.35, 91.0),
    ]
)

slash_outer = _sc(
    [
        (41.76, 50.57),
        (59.04, 50.57),
        (90.63, 91.0),
        (73.35, 91.0),
    ]
)

# 1. Upper-right diagonal slash in flat pastel blue & green
polygon(slash_blue, style=Icon.no_border_fill(Colors.Blue3))
polygon(slash_green, style=Icon.no_border_fill(Colors.Green3))
Icon.draw_round_segment(slash_blue[3], slash_blue[2], width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(slash_outer, width_units=w, color=Icon.DARK, closed=True)

# 2. Dark slate X mark on lower-left
polygon(x_mark, style=Icon.no_border_fill(Colors.Gray6))
Icon.draw_round_polyline(x_mark, width_units=w, color=Icon.DARK, closed=True)

save()
