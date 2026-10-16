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
from drawlib.shapes import arc, polygon, rectangle
from drawlib.styles import Colors, Style
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    pt,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Bucket handle arc
arc(
    (50.0, 60.0),
    width=42.0,
    height=44.0,
    angle_start=0.0,
    angle_end=180.0,
    style=Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=DARK,
        shape_line_width=pt(w),
    ),
)

# 2. Tapered storage bucket body
polygon(
    [(25.0, 16.0), (75.0, 16.0), (83.0, 58.0), (17.0, 58.0)],
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.0),
)

# 3. Bucket top rim
rectangle(
    (50.0, 60.0),
    width=74.0,
    height=10.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=3.8),
)

# 4. AI sparkle mark on front of bucket
sparkle_pts = build_sparkle_4pt_polygon(50.0, 36.5, outer_r=13.5, inner_r=4.6)
polygon(sparkle_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(sparkle_pts, width_units=2.4, color=DARK, closed=True)

save()
