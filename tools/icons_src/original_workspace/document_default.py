# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: document."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
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
    steps: int = 8,
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            cy + r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. WHITE folded-corner page body (x=20..80, y=13..87)
r_doc = 4.5
doc_pts: list[tuple[float, float]] = [
    (62.0, 87.0),
    *_arc_pts(20.0 + r_doc, 87.0 - r_doc, r_doc, 90.0, 180.0),
    *_arc_pts(20.0 + r_doc, 13.0 + r_doc, r_doc, 180.0, 270.0),
    *_arc_pts(80.0 - r_doc, 13.0 + r_doc, r_doc, 270.0, 360.0),
    (80.0, 69.0),
]
polygon(doc_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(doc_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Top-right corner fold flap (PASTEL_BLUE_LIGHT)
r_flap = 3.0
flap_pts: list[tuple[float, float]] = [
    (62.0, 87.0),
    *_arc_pts(62.0 + r_flap, 69.0 + r_flap, r_flap, 180.0, 270.0),
    (80.0, 69.0),
]
polygon(flap_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(flap_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. Header block (PASTEL_BLUE)
rectangle(
    (41.5, 73.0),
    width=27.0,
    height=8.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_inner, shape_r=2.2),
)

# 4. Three DARK text lines
Icon.draw_round_segment((28.0, 56.5), (72.0, 56.5), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((28.0, 46.0), (72.0, 46.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((28.0, 35.5), (57.0, 35.5), width_units=w_inner, color=Icon.DARK)

# 5. Bottom accent tag (PASTEL_GREEN)
rectangle(
    (37.5, 23.5),
    width=19.0,
    height=7.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner, shape_r=3.5),
)

save()
