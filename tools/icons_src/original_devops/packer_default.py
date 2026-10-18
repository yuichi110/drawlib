# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: packer."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _scale_pt(pt: tuple[float, float], s: float = 0.94) -> tuple[float, float]:
    """Scale point around (50, 50) by factor s."""
    return (50.0 + (pt[0] - 50.0) * s, 50.0 + (pt[1] - 50.0) * s)


setup_icon()

w = 2.0

# 1. Front-left isometric wing (Colors.Blue2)
raw_front_wing = [
    (24.66, 80.98),
    (51.52, 65.62),
    (51.52, 9.0),
    (24.66, 24.36),
]

# 2. Back-right interlocking isometric wing (Colors.Blue3)
raw_back_wing = [
    (64.82, 74.36),
    (35.62, 91.0),
    (35.62, 79.44),
    (55.48, 68.10),
    (55.48, 33.43),
    (64.82, 28.12),
    (66.52, 27.29),
    (68.14, 26.76),
    (69.64, 26.53),
    (71.02, 26.59),
    (72.25, 26.93),
    (73.30, 27.55),
    (74.16, 28.42),
    (74.80, 29.54),
    (75.20, 30.91),
    (75.34, 32.51),
    (75.34, 57.96),
    (75.20, 59.72),
    (74.80, 61.54),
    (74.16, 63.40),
    (73.30, 65.25),
    (72.25, 67.07),
    (71.02, 68.81),
    (69.64, 70.44),
    (68.14, 71.94),
    (66.52, 73.25),
]

front_wing = [_scale_pt(p) for p in raw_front_wing]
back_wing = [_scale_pt(p) for p in raw_back_wing]

polygon(front_wing, style=no_border_fill(Colors.Blue2))
polygon(back_wing, style=no_border_fill(Colors.Blue3))

draw_round_polyline(front_wing, width_units=w, color=DARK, closed=True)
draw_round_polyline(back_wing, width_units=w, color=DARK, closed=True)

save()
