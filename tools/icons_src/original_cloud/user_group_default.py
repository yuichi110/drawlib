# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: user_group."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE


def _build_dome(
    cx: float,
    rx: float,
    y_bot: float,
    y_arch_base: float,
    ry: float,
    corner_r: float,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    steps_corner = 10
    steps_arch = 36

    c_bl = (cx - rx + corner_r, y_bot + corner_r)
    for i in range(steps_corner + 1):
        ang = math.radians(180.0 + 90.0 * (i / steps_corner))
        pts.append((c_bl[0] + corner_r * math.cos(ang), c_bl[1] + corner_r * math.sin(ang)))

    c_br = (cx + rx - corner_r, y_bot + corner_r)
    for i in range(steps_corner + 1):
        ang = math.radians(270.0 + 90.0 * (i / steps_corner))
        pts.append((c_br[0] + corner_r * math.cos(ang), c_br[1] + corner_r * math.sin(ang)))

    for i in range(steps_arch + 1):
        ang = math.radians(180.0 * (i / steps_arch))
        pts.append((cx + rx * math.cos(ang), y_arch_base + ry * math.sin(ang)))

    return pts


# Back/right secondary avatar
polygon(
    _build_dome(cx=66.0, rx=20.5, y_bot=22.0, y_arch_base=28.0, ry=19.0, corner_r=4.5),
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
circle(
    (66.0, 64.0),
    radius=11.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# Front/left primary avatar
polygon(
    _build_dome(cx=36.0, rx=23.5, y_bot=16.0, y_arch_base=23.0, ry=23.0, corner_r=5.0),
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (36.0, 66.0),
    radius=13.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

save()
