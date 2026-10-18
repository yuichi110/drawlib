# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: slack."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
s = 38.8 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale points around (50, 50) to fit safely within [10, 90]."""
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


def _arc(cx: float, cy: float, r: float, deg0: float, deg1: float, steps: int = 20) -> list[tuple[float, float]]:
    """Sample circular arc from deg0 to deg1 inclusive."""
    return [
        (
            cx + r * math.cos(math.radians(deg0 + (deg1 - deg0) * i / steps)),
            cy + r * math.sin(math.radians(deg0 + (deg1 - deg0) * i / steps)),
        )
        for i in range(steps + 1)
    ]


def _pill_v(xc: float, y_bot: float, y_top: float, r: float) -> list[tuple[float, float]]:
    """Build vertical stadium pill with cap centers at (xc, y_bot) and (xc, y_top)."""
    return _sc([*_arc(xc, y_top, r, 0.0, 180.0, 20), *_arc(xc, y_bot, r, 180.0, 360.0, 20)])


def _pill_h(x_left: float, x_right: float, yc: float, r: float) -> list[tuple[float, float]]:
    """Build horizontal stadium pill with cap centers at (x_left, yc) and (x_right, yc)."""
    return _sc([*_arc(x_left, yc, r, 90.0, 270.0, 20), *_arc(x_right, yc, r, -90.0, 90.0, 20)])


def _droplet(xc: float, yc: float, r: float, corner: str) -> list[tuple[float, float]]:
    """Build a 3/4-circle Slack droplet with one sharp corner ('tr', 'br', 'bl', 'tl')."""
    if corner == "tr":
        pts = [(xc + r, yc + r), *_arc(xc, yc, r, 90.0, 360.0, 30)]
    elif corner == "br":
        pts = [(xc + r, yc - r), *_arc(xc, yc, r, 0.0, 270.0, 30)]
    elif corner == "bl":
        pts = [(xc - r, yc - r), *_arc(xc, yc, r, -90.0, 180.0, 30)]
    else:  # "tl"
        pts = [(xc - r, yc + r), *_arc(xc, yc, r, 180.0, 450.0, 30)]
    return _sc(pts)


r_slack = 8.61

shapes: list[tuple[list[tuple[float, float]], Any]] = [
    # Bottom-left pair (Red3)
    (_droplet(17.68, 39.17, r_slack, "tr"), Colors.Red3),
    (_pill_v(39.20, 17.64, 39.17, r_slack), Colors.Red3),
    # Top-left pair (Blue2)
    (_droplet(39.20, 82.36, r_slack, "br"), Colors.Blue2),
    (_pill_h(17.61, 39.20, 60.76, r_slack), Colors.Blue2),
    # Top-right pair (Green3)
    (_droplet(82.32, 60.76, r_slack, "bl"), Colors.Green3),
    (_pill_v(60.80, 60.76, 82.36, r_slack), Colors.Green3),
    # Bottom-right pair (Amber2)
    (_droplet(60.80, 17.64, r_slack, "tl"), Colors.Amber2),
    (_pill_h(60.80, 82.39, 39.17, r_slack), Colors.Amber2),
]

for pts, col in shapes:
    polygon(pts, style=no_border_fill(col))
    draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
