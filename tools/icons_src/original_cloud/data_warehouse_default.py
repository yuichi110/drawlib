# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: data_warehouse."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

rectangle(
    (50.0, 44.0),
    width=66.0,
    height=42.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

pillars = [
    (32.0, 22.0, PASTEL_BLUE),
    (50.0, 30.0, PASTEL_BLUE),
    (68.0, 36.0, PASTEL_GREEN),
]
for px, ph, pcol in pillars:
    rectangle(
        (px, 23.0 + ph / 2.0),
        width=11.0,
        height=ph,
        style=fill_style(pcol, border_color=DARK, border_units=2.2, shape_r=2.0),
    )

rectangle(
    (50.0, 18.0),
    width=76.0,
    height=10.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=3.0),
)

polygon(
    [(12.0, 65.0), (88.0, 65.0), (50.0, 86.0)],
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=3.0),
)

save()
