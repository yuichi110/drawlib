# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: notebook."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Spiral-bound notebook card with left PASTEL_BLUE spine strip
rectangle(
    (48.0, 48.0),
    width=56.0,
    height=64.0,
    style=Icon.fill_style(Icon.WHITE, shape_r=6.5),
)
Gcp.draw_rounded_corner_block(
    20.0,
    16.0,
    32.0,
    80.0,
    r=6.5,
    round_tl=True,
    round_bl=True,
    color=Icon.PASTEL_BLUE,
)
rectangle(
    (48.0, 48.0),
    width=56.0,
    height=64.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w, shape_r=6.5),
)
Icon.draw_round_segment((32.0, 16.0), (32.0, 80.0), width_units=w, color=Icon.DARK)

# 2. Four horizontal spiral binder rings
for ry in (67.0, 54.0, 42.0, 29.0):
    Icon.draw_round_segment((14.5, ry), (25.0, ry), width_units=3.2, color=Icon.DARK)

# 3. Simple horizontal notebook lines inside page
Icon.draw_round_segment((41.0, 60.0), (63.0, 60.0), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((41.0, 48.0), (66.0, 48.0), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((41.0, 36.0), (58.0, 36.0), width_units=w, color=Icon.DARK)

# 4. Top-right AI sparkle mark
sparkle_pts = Icon.build_sparkle_4pt_polygon(75.0, 76.0, outer_r=11.5, inner_r=4.0)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
