# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: pdf_document."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

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


# 1. WHITE folded-corner page (x=20..80, y=13..87)
r_doc = 4.5
doc_pts: list[tuple[float, float]] = [
    (62.0, 87.0),
    *_arc_pts(20.0 + r_doc, 87.0 - r_doc, r_doc, 90.0, 180.0),
    *_arc_pts(20.0 + r_doc, 13.0 + r_doc, r_doc, 180.0, 270.0),
    *_arc_pts(80.0 - r_doc, 13.0 + r_doc, r_doc, 270.0, 360.0),
    (80.0, 69.0),
]
polygon(doc_pts, style=no_border_fill(WHITE))
draw_round_polyline(doc_pts, width_units=w_outer, color=DARK, closed=True)

# 2. Top-right fold flap (PASTEL_BLUE_LIGHT)
r_flap = 3.0
flap_pts: list[tuple[float, float]] = [
    (62.0, 87.0),
    *_arc_pts(62.0 + r_flap, 69.0 + r_flap, r_flap, 180.0, 270.0),
    (80.0, 69.0),
]
polygon(flap_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(flap_pts, width_units=w_outer, color=DARK, closed=True)

# 3. Upper 3-lobe trefoil curve / seal motif (PASTEL_GREEN)
scx, scy = 50.0, 56.5
seal_pts: list[tuple[float, float]] = []
steps_seal = 72
for i in range(steps_seal):
    theta = 2.0 * math.pi * (i / steps_seal)
    r_val = 8.6 + 4.4 * math.cos(3.0 * (theta - math.pi / 2.0))
    seal_pts.append((scx + r_val * math.cos(theta), scy + r_val * math.sin(theta)))

polygon(seal_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(seal_pts, width_units=w_inner, color=DARK, closed=True)
circle(
    (scx, scy),
    radius=3.6,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner),
)

# 4. Horizontal ribbon banner across lower half (PASTEL_BLUE)
rectangle(
    (50.0, 28.5),
    width=72.0,
    height=15.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=3.2),
)

# Subtle interior line marks on ribbon banner
draw_round_segment((28.0, 31.0), (72.0, 31.0), width_units=w_inner, color=DARK)
draw_round_segment((36.0, 26.0), (64.0, 26.0), width_units=w_inner, color=DARK)

save()
