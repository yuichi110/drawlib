# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: webhook."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8
w_line = 2.7


def _arc_points(
    cx: float, cy: float, r: float, deg_start: float, deg_end: float, steps: int = 20
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Connector stem between event trigger node and hook eye
eye_cx, eye_cy = 44.0, 52.5
draw_round_segment((28.0, 72.0), (eye_cx, eye_cy), width_units=w_line, color=DARK)

# 2. Top-left PASTEL_BLUE event trigger node at (28, 72), r=11.0
circle(
    (28.0, 72.0),
    radius=11.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape),
)
circle(
    (28.0, 72.0),
    radius=4.2,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)

# 3. Bold interlocking PASTEL_GREEN curved hook shape curving around (58, 38)
eye_r = 7.8
hw = 3.6
bend_cx, bend_cy = 58.0, 38.0
bend_r = 14.0
r_out = bend_r + hw  # 17.6
r_in = bend_r - hw  # 10.4
tip_angle = 25.0

a_eye_right = 270.0 + math.degrees(math.asin(hw / eye_r))
a_eye_left = 270.0 - math.degrees(math.asin(hw / eye_r))

tip_cx = bend_cx + bend_r * math.cos(math.radians(tip_angle))
tip_cy = bend_cy + bend_r * math.sin(math.radians(tip_angle))

hook_pts: list[tuple[float, float]] = [
    *_arc_points(eye_cx, eye_cy, eye_r, a_eye_right, 360.0 + a_eye_left, 28),
    *_arc_points(bend_cx, bend_cy, r_out, 180.0, 360.0 + tip_angle, 28)[1:],
    *_arc_points(tip_cx, tip_cy, hw, tip_angle, tip_angle + 180.0, 12)[1:],
    *_arc_points(bend_cx, bend_cy, r_in, 360.0 + tip_angle, 180.0, 24)[1:],
]

polygon(hook_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(hook_pts, width_units=w_shape, color=DARK, closed=True)

# 4. WHITE ring eye hole inside hook head
circle(
    (eye_cx, eye_cy),
    radius=3.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
)

save()
