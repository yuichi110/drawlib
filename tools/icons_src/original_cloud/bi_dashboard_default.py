# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: bi_dashboard."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

rectangle(
    (50.0, 50.0),
    width=76.0,
    height=64.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)

bars = [
    (33.0, 18.0, Icon.PASTEL_BLUE),
    (50.0, 28.0, Icon.PASTEL_BLUE),
    (67.0, 40.0, Icon.PASTEL_GREEN),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, 26.0 + bh / 2.0),
        width=11.0,
        height=bh,
        style=Icon.fill_style(bcol, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
    )

circle(
    (33.0, 64.0),
    radius=8.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
