# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: key_value_store."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Left Key card
rectangle(
    (28.0, 50.0),
    width=34.0,
    height=56.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
circle((28.0, 60.0), radius=8.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
circle((28.0, 60.0), radius=3.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
Icon.draw_round_segment((28.0, 51.5), (28.0, 34.0), width_units=w * 1.3, color=Icon.DARK)
Icon.draw_round_segment((28.0, 40.0), (34.0, 40.0), width_units=w * 1.3, color=Icon.DARK)
Icon.draw_round_segment((28.0, 34.0), (35.0, 34.0), width_units=w * 1.3, color=Icon.DARK)
# Right Value card
rectangle(
    (72.0, 50.0),
    width=34.0,
    height=56.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)
for yc in (62.0, 50.0, 38.0):
    rectangle(
        (72.0, yc),
        width=22.0,
        height=7.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=2.0),
    )
# Arrow between Key and Value
Icon.draw_chunky_arrow(
    y_center=50.0,
    x_tail=42.0,
    x_tip=58.0,
    x_head_base=51.0,
    shaft_half_h=3.5,
    head_half_h=7.5,
    fill_color=Icon.WHITE,
    border_units=w,
)
save()
