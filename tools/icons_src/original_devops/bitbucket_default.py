# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: bitbucket."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
scale = 0.95


def _sc(x: float, y: float) -> tuple[float, float]:
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


_RAW_OUTER: list[tuple[float, float]] = [
    (11.66, 86.87),
    (11.09, 86.81),
    (10.55, 86.64),
    (10.06, 86.35),
    (9.64, 85.96),
    (9.31, 85.48),
    (9.10, 84.96),
    (9.00, 84.40),
    (9.04, 83.82),
    (20.19, 16.11),
    (20.39, 15.38),
    (20.74, 14.72),
    (21.21, 14.15),
    (21.78, 13.70),
    (22.44, 13.36),
    (23.17, 13.17),
    (23.68, 13.13),
    (77.18, 13.13),
    (77.76, 13.19),
    (78.29, 13.36),
    (78.76, 13.63),
    (79.17, 14.00),
    (79.50, 14.45),
    (79.73, 14.96),
    (79.81, 15.34),
    (90.96, 83.81),
    (91.00, 84.38),
    (90.90, 84.94),
    (90.69, 85.47),
    (90.36, 85.94),
    (89.94, 86.34),
    (89.45, 86.62),
    (88.91, 86.80),
    (88.34, 86.86),
]

_RAW_HOLE: list[tuple[float, float]] = [
    (58.62, 37.93),
    (41.55, 37.93),
    (36.92, 62.09),
    (62.76, 62.09),
]

_RAW_SHADOW_BAND: list[tuple[float, float]] = [
    (62.76, 62.09),
    (87.42, 62.09),
    (79.81, 15.34),
    (79.73, 14.96),
    (79.50, 14.45),
    (79.17, 14.00),
    (78.76, 13.63),
    (78.29, 13.36),
    (77.76, 13.19),
    (77.18, 13.13),
    (54.37, 13.13),
    (58.62, 37.93),
]

outer_bucket = [_sc(x, y) for x, y in _RAW_OUTER]
inner_hole = [_sc(x, y) for x, y in _RAW_HOLE]
shadow_band = [_sc(x, y) for x, y in _RAW_SHADOW_BAND]

# 1. Main bucket (Colors.Blue3) with transparent center trapezoid hole
draw_compound_polygon([outer_bucket, inner_hole], color=Colors.Blue3)

# 2. Right flat shadow band (Colors.Blue4)
polygon(shadow_band, style=no_border_fill(Colors.Blue4))

# 3. Crisp DARK w=1.9 outlines on outer bucket and inner hole
draw_round_polyline(outer_bucket, width_units=w, color=DARK, closed=True)
draw_round_polyline(inner_hole, width_units=w, color=DARK, closed=True)

save()
