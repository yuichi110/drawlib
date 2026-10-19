# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: message_queue."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

Icon.draw_round_segment((12.0, 74.0), (88.0, 74.0), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((12.0, 26.0), (88.0, 26.0), width_units=w, color=Icon.DARK)

block_colors = [Icon.PASTEL_BLUE, Icon.PASTEL_BLUE, Icon.PASTEL_GREEN]
for cx, col in zip((27.0, 50.0, 73.0), block_colors, strict=True):
    rectangle(
        (cx, 50.0),
        width=16.0,
        height=30.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w, shape_r=3.5),
    )

save()
