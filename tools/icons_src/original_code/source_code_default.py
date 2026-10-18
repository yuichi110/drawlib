# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: source_code."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 2.0


def _arc_points(
    cx: float, cy: float, r: float, deg_start: float, deg_end: float, steps: int = 8
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. WHITE document sheet (x=22..78, y=12..88, folded top-right from (60,88) to (78,70))
r_doc = 4.5
doc_pts: list[tuple[float, float]] = [
    (60.0, 88.0),
    *_arc_points(22.0 + r_doc, 88.0 - r_doc, r_doc, 90.0, 180.0),
    *_arc_points(22.0 + r_doc, 12.0 + r_doc, r_doc, 180.0, 270.0),
    *_arc_points(78.0 - r_doc, 12.0 + r_doc, r_doc, 270.0, 360.0),
    (78.0, 70.0),
]
polygon(doc_pts, style=no_border_fill(WHITE))
draw_round_polyline(doc_pts, width_units=w_shape, color=DARK, closed=True)

# 2. Folded top-right corner flap in PASTEL_BLUE_LIGHT
r_flap = 3.0
flap_pts: list[tuple[float, float]] = [
    (60.0, 88.0),
    *_arc_points(60.0 + r_flap, 70.0 + r_flap, r_flap, 180.0, 270.0),
    (78.0, 70.0),
]
polygon(flap_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(flap_pts, width_units=w_shape, color=DARK, closed=True)

# 3. Central `<` (PASTEL_BLUE), `/` (PASTEL_GREEN), `>` (PASTEL_BLUE) code marks around y=44
yc = 43.0

# Left `<` bracket polygon
left_chevron = [
    (27.5, yc),
    (36.5, yc + 9.0),
    (39.8, yc + 5.7),
    (34.1, yc),
    (39.8, yc - 5.7),
    (36.5, yc - 9.0),
]
polygon(left_chevron, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(left_chevron, width_units=w_shape, color=DARK, closed=True)

# Center `/` slash polygon
slash_pts = [
    (43.8, yc - 11.5),
    (48.3, yc - 11.5),
    (56.2, yc + 11.5),
    (51.7, yc + 11.5),
]
polygon(slash_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(slash_pts, width_units=w_shape, color=DARK, closed=True)

# Right `>` bracket polygon
right_chevron = [
    (72.5, yc),
    (63.5, yc + 9.0),
    (60.2, yc + 5.7),
    (65.9, yc),
    (60.2, yc - 5.7),
    (63.5, yc - 9.0),
]
polygon(right_chevron, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(right_chevron, width_units=w_shape, color=DARK, closed=True)

save()
