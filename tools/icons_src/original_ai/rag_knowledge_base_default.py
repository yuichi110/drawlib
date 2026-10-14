# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: rag_knowledge_base."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

rectangle(
    (44.0, 48.0),
    width=54.0,
    height=64.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)

rectangle(
    (23.0, 48.0),
    width=12.0,
    height=64.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

draw_round_segment((36.0, 58.0), (62.0, 58.0), width_units=2.5, color=DARK)
draw_round_segment((36.0, 44.0), (62.0, 44.0), width_units=2.5, color=DARK)

circle(
    (70.0, 66.0),
    radius=17.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

sparkle_pts = build_sparkle_4pt_polygon(70.0, 66.0, outer_r=10.5, inner_r=3.6)
polygon(sparkle_pts, style=no_border_fill(WHITE))
draw_round_polyline(sparkle_pts, width_units=2.0, color=DARK, closed=True)

save()
