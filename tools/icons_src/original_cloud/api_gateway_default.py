# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: api_gateway."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

for px in (19.0, 81.0):
    rectangle(
        (px, 50.0),
        width=14.0,
        height=68.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=5.0),
    )

Icon.draw_chunky_arrow(
    y_center=63.0,
    x_tail=33.0,
    x_tip=67.5,
    x_head_base=53.5,
    shaft_half_h=4.6,
    head_half_h=11.0,
    fill_color=Icon.PASTEL_BLUE,
    border_units=w,
)

Icon.draw_chunky_arrow(
    y_center=37.0,
    x_tail=67.0,
    x_tip=32.5,
    x_head_base=46.5,
    shaft_half_h=4.6,
    head_half_h=11.0,
    fill_color=Icon.PASTEL_GREEN,
    border_units=w,
)

save()
