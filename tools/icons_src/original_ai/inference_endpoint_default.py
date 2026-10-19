# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: inference_endpoint."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

rectangle(
    (38.0, 50.0),
    width=48.0,
    height=56.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

sparkle_pts = Icon.build_sparkle_4pt_polygon(35.0, 50.0, outer_r=14.0, inner_r=4.8)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

Icon.draw_chunky_arrow(
    y_center=50.0,
    x_tail=55.0,
    x_tip=88.0,
    x_head_base=73.0,
    shaft_half_h=5.5,
    head_half_h=13.0,
    fill_color=Icon.PASTEL_GREEN,
    border_units=w,
)

save()
