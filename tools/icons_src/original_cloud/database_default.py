# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: database."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx = 50.0
width = 68.0
w_half = width / 2.0
ry = 10.0
eh = ry * 2.0

tier_bottoms = [20.0, 39.0, 58.0]
tier_h = 19.0
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

for y_led in (21.0, 40.0, 59.0):
    circle(
        (68.0, y_led),
        radius=3.8,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
    )

save()
