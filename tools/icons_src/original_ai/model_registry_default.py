# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: model_registry."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

Icon.draw_iso_cube(
    46.0,
    46.0,
    radius=34.0,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_BLUE_LIGHT,
    border_color=Icon.DARK,
    border_units=w,
)

circle(
    (72.0, 70.0),
    radius=16.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)

sparkle_pts = Icon.build_sparkle_4pt_polygon(72.0, 70.0, outer_r=9.5, inner_r=3.3)
polygon(sparkle_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(sparkle_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
