# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: dify."""

import math

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

w = 1.9
SCALE = 0.94


def _s(x: float, y: float) -> tuple[float, float]:
    """Scale raw icon point toward (50, 50) so outer border stays inside [9, 91]."""
    return (50.0 + SCALE * (x - 50.0), 50.0 + SCALE * (y - 50.0))


# 1. Squircle dot of "i" (Colors.Blue4)
raw_dot = [
    (33.06, 70.25),
    (35.40, 70.48),
    (37.26, 71.15),
    (38.69, 72.18),
    (39.72, 73.53),
    (40.37, 75.14),
    (40.68, 76.95),
    (40.72, 77.91),
    (40.68, 78.88),
    (40.37, 80.69),
    (39.72, 82.30),
    (38.70, 83.65),
    (37.27, 84.68),
    (35.40, 85.35),
    (33.07, 85.58),
    (30.73, 85.35),
    (28.86, 84.68),
    (27.43, 83.65),
    (26.40, 82.30),
    (25.75, 80.69),
    (25.44, 78.88),
    (25.40, 77.91),
    (25.44, 76.95),
    (25.75, 75.14),
    (26.40, 73.53),
    (27.43, 72.18),
    (28.86, 71.15),
    (30.72, 70.48),
]
dot_pts = [_s(x, y) for x, y in raw_dot]
polygon(dot_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(dot_pts, width_units=w, color=DARK, closed=True)

# 2. Geometric "if" stem and hooked crossbar (Colors.Blue4)
hook_arc: list[tuple[float, float]] = []
hook_cx, hook_cy, hook_r = 76.78, 68.60, 16.95
for i in range(17):
    ang = math.radians(90.0 + 90.0 * (i / 16))
    hook_arc.append((hook_cx + hook_r * math.cos(ang), hook_cy + hook_r * math.sin(ang)))

raw_if_body = [
    (59.83, 63.67),
    (47.28, 63.67),
    (47.28, 52.73),
    (59.85, 52.73),
    (59.85, 25.35),
    (39.07, 25.35),
    (39.07, 63.68),
    (11.74, 63.68),
    (11.74, 52.74),
    (27.04, 52.74),
    (27.04, 25.36),
    (9.00, 25.36),
    (9.00, 14.42),
    (91.00, 14.42),
    (91.00, 25.36),
    (71.87, 25.36),
    (71.87, 52.74),
    (91.00, 52.74),
    (91.00, 63.68),
    (71.87, 63.68),
    (71.87, 74.63),
    (91.00, 74.63),
    (91.00, 85.57),
    *hook_arc,
]
if_pts = [_s(x, y) for x, y in raw_if_body]
polygon(if_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(if_pts, width_units=w, color=DARK, closed=True)

save()
