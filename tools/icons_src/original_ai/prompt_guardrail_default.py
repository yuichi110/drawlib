# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: prompt_guardrail."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

rectangle(
    (42.0, 58.0),
    width=56.0,
    height=42.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

Icon.draw_round_segment((26.0, 64.0), (56.0, 64.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((26.0, 52.0), (56.0, 52.0), width_units=2.0, color=Icon.DARK)

cx = 66.0
y_bot, y_top = 16.0, 64.0
half_w = 19.0
left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(full_outline, width_units=w, color=Icon.DARK, closed=True)

circle(
    (66.0, 42.0),
    radius=5.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

save()
