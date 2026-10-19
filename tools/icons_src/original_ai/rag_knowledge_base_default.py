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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Bucket handle arc
arc(
    (50.0, 60.0),
    width=42.0,
    height=44.0,
    angle_start=0.0,
    angle_end=180.0,
    style=Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=Icon.DARK,
        shape_line_width=Icon.pt(w),
    ),
)

# 2. Tapered storage bucket body
polygon(
    [(25.0, 16.0), (75.0, 16.0), (83.0, 58.0), (17.0, 58.0)],
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=5.0),
)

# 3. Bucket top rim
rectangle(
    (50.0, 60.0),
    width=74.0,
    height=10.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=3.8),
)

# 4. AI sparkle mark on front of bucket
sparkle_pts = Icon.build_sparkle_4pt_polygon(50.0, 36.5, outer_r=13.5, inner_r=4.6)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
