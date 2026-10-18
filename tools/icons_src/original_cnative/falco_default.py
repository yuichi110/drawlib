# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: falco."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _rounded_bar(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    *,
    width_units: float,
    fill_color: str,
    border_units: float = 2.2,
    cap_end: bool = True,
) -> None:
    """Draw a stadium/capsule bar with fill and dark structural border."""
    x1, y1 = xy1
    x2, y2 = xy2
    dx, dy = x2 - x1, y2 - y1
    base_ang = math.atan2(dy, dx)
    r = width_units / 2.0
    pts: list[tuple[float, float]] = []
    steps = 14
    if cap_end:
        for i in range(steps + 1):
            ang = base_ang - math.pi / 2.0 + math.pi * (i / steps)
            pts.append((x2 + r * math.cos(ang), y2 + r * math.sin(ang)))
    else:
        nx = -math.sin(base_ang) * r
        ny = math.cos(base_ang) * r
        pts.append((x2 - nx, y2 - ny))
        pts.append((x2 + nx, y2 + ny))
    for i in range(steps + 1):
        ang = base_ang + math.pi / 2.0 + math.pi * (i / steps)
        pts.append((x1 + r * math.cos(ang), y1 + r * math.sin(ang)))
    polygon(pts, style=no_border_fill(fill_color))
    draw_round_polyline(pts, width_units=border_units, color=DARK, closed=True)


setup_icon()

# Slight down-right offset inside the circular medallion for balanced visual margins
dx, dy = 2.2, -2.2


def _s(x: float, y: float) -> tuple[float, float]:
    """Shift inner falcon coordinates by (dx, dy)."""
    return (x + dx, y + dy)


# 3 swooping upper-left falcon wing bars (135-degree tilt)
_rounded_bar(_s(51.5, 56.5), _s(31.0, 77.0), width_units=6.6, fill_color=PASTEL_BLUE)
_rounded_bar(_s(44.5, 49.5), _s(27.0, 67.0), width_units=6.6, fill_color=PASTEL_BLUE_LIGHT)
_rounded_bar(_s(37.5, 42.5), _s(26.0, 54.0), width_units=6.6, fill_color=PASTEL_BLUE)

# Lower parallel body/tail bar (45-degree tilt)
_rounded_bar(_s(38.0, 24.0), _s(67.0, 53.0), width_units=6.8, fill_color=PASTEL_BLUE_LIGHT)

# Main diagonal falcon body bar (45-degree tilt, flat collar join at _s(57, 57))
# With width = 7.071, normal offset is (-2.5, +2.5) and (+2.5, -2.5)
_rounded_bar(
    _s(27.5, 27.5),
    _s(57.0, 57.0),
    width_units=7.071,
    fill_color=PASTEL_BLUE,
    border_units=2.0,
    cap_end=False,
)

# Crisp pastel green hooked falcon head & beak continuing cleanly from _s(54.5, 59.5)-_s(59.5, 54.5)
beak_pts = [
    _s(54.5, 59.5),
    _s(63.5, 68.5),
    _s(70.5, 68.0),
    _s(78.0, 61.5),
    _s(68.0, 61.0),
    _s(59.5, 54.5),
]
polygon(beak_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(beak_pts, width_units=2.0, color=DARK, closed=True)

save()
