# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: oauth2."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
left_pts = Icon.build_shield_half_points(50.0, 12.0, 88.0, 36.0, side="left")
right_pts = Icon.build_shield_half_points(50.0, 12.0, 88.0, 36.0, side="right")
polygon(left_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
polygon(right_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
shield_outline = [*left_pts, *reversed(right_pts[1:-1])]
Icon.draw_round_polyline(shield_outline, width_units=w, color=Icon.DARK, closed=True)
# Delegated token exchange badge in center
circle((50.0, 53.0), radius=18.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
Icon.draw_chunky_arrow(
    y_center=58.0,
    x_tail=39.0,
    x_tip=61.0,
    x_head_base=54.0,
    shaft_half_h=2.5,
    head_half_h=5.5,
    fill_color=Icon.PASTEL_GREEN,
    border_units=w * 0.8,
)
Icon.draw_chunky_arrow(
    y_center=47.0,
    x_tail=61.0,
    x_tip=39.0,
    x_head_base=46.0,
    shaft_half_h=2.5,
    head_half_h=5.5,
    fill_color=Icon.PASTEL_BLUE,
    border_units=w * 0.8,
)
save()
