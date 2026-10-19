# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: chat_message."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 10,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Back-left chat bubble (PASTEL_BLUE, x=13..65, y=45..83)
bx0, by0, bx1, by1 = 13.0, 45.0, 65.0, 83.0
rb = 8.0
back_pts: list[tuple[float, float]] = [
    *_arc_pts(bx0 + rb, by1 - rb, rb, 90.0, 180.0),
    *_arc_pts(bx0 + rb, by0 + rb, rb, 180.0, 270.0),
    (22.0, by0),
    (17.5, 34.5),
    (31.5, by0),
    *_arc_pts(bx1 - rb, by0 + rb, rb, 270.0, 360.0),
    *_arc_pts(bx1 - rb, by1 - rb, rb, 0.0, 90.0),
]
polygon(back_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(back_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Two text lines inside back-left bubble (spaced cleanly above front bubble)
Icon.draw_round_segment((23.5, 71.0), (54.0, 71.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((23.5, 62.5), (39.5, 62.5), width_units=w_inner, color=Icon.DARK)

# 3. Front-right chat bubble (PASTEL_GREEN, x=37..87, y=24..58)
fx0, fy0, fx1, fy1 = 37.0, 24.0, 87.0, 58.0
rf = 8.0
front_pts: list[tuple[float, float]] = [
    *_arc_pts(fx0 + rf, fy1 - rf, rf, 90.0, 180.0),
    *_arc_pts(fx0 + rf, fy0 + rf, rf, 180.0, 270.0),
    (68.5, fy0),
    (82.5, 14.0),
    (78.0, fy0),
    *_arc_pts(fx1 - rf, fy0 + rf, rf, 270.0, 360.0),
    *_arc_pts(fx1 - rf, fy1 - rf, rf, 0.0, 90.0),
]
polygon(front_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(front_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 4. Three typing dots inside front-right bubble
for dx in (51.0, 62.0, 73.0):
    circle((dx, 41.0), radius=2.6, style=Icon.fill_style(Icon.DARK))

save()
