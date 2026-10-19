# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: feature_store."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Left/back 3-tier database cylinder
cx = 42.0
width = 52.0
w_half = width / 2.0
ry = 8.0
eh = ry * 2.0
tier_bottoms = [20.0, 36.0, 52.0]
tier_h = 16.0
y_bot = tier_bottoms[0]
y_top = tier_bottoms[-1] + tier_h

for yb in tier_bottoms:
    ellipse(
        (cx, yb),
        width=width,
        height=eh,
        style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
    )
    rectangle(
        (cx, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=Icon.fill_style(Icon.PASTEL_BLUE),
    )

Icon.draw_round_segment((cx - w_half, y_bot), (cx - w_half, y_top), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((cx + w_half, y_bot), (cx + w_half, y_top), width_units=w, color=Icon.DARK)

ellipse(
    (cx, y_top),
    width=width,
    height=eh,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# 2. Overlapping bottom-right AI feature sparkle badge
bx, by = 68.0, 34.0
circle(
    (bx, by),
    radius=18.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

sparkle_pts = Icon.build_sparkle_4pt_polygon(bx, by, outer_r=11.5, inner_r=4.0)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
