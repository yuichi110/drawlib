# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: email."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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


# 1. Envelope WHITE body (x=13..81, y=21..69)
x0, y0, x1, y1 = 13.0, 21.0, 81.0, 69.0
r_env = 5.0
rectangle(
    ((x0 + x1) / 2.0, (y0 + y1) / 2.0),
    width=x1 - x0,
    height=y1 - y0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=r_env),
)

# 2. Subtle inner lower fold creases
Icon.draw_round_segment((15.5, 23.5), (36.5, 44.5), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((78.5, 23.5), (57.5, 44.5), width_units=w_inner, color=Icon.DARK)

# 3. Top envelope flap (PASTEL_BLUE_LIGHT)
flap_pts: list[tuple[float, float]] = [
    *_arc_pts(x0 + r_env, y1 - r_env, r_env, 180.0, 90.0, 8),
    *_arc_pts(x1 - r_env, y1 - r_env, r_env, 90.0, 0.0, 8),
    (50.2, 41.8),
    *_arc_pts(47.0, 44.6, 4.2, -50.0, -130.0, 10),
    (43.8, 41.8),
]
polygon(flap_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(flap_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 4. Top-right notification badge circle (PASTEL_GREEN)
circle(
    (77.5, 69.0),
    radius=10.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)

save()
