# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: jwt."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# 3-part token card (Header . Payload . Signature)
tiers = [
    (72.0, Icon.PASTEL_BLUE),
    (50.0, Icon.WHITE),
    (28.0, Icon.PASTEL_GREEN),
]
for yc, col in tiers:
    rectangle(
        (50.0, yc),
        width=76.0,
        height=18.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w, shape_r=5.0),
    )
    Icon.draw_round_segment((24.0, yc), (56.0, yc), width_units=w * 1.2, color=Icon.DARK)
    circle(
        (72.0, yc),
        radius=4.0,
        style=Icon.fill_style(
            Icon.WHITE if col != Icon.WHITE else Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w
        ),
    )
save()
