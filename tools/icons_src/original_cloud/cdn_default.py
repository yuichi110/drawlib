# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: cdn."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

circle(
    (50.0, 50.0),
    radius=28.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

ellipse(
    (50.0, 50.0),
    width=26.0,
    height=56.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.3),
)

draw_round_segment((22.0, 50.0), (78.0, 50.0), width_units=2.3, color=DARK)

circle(
    (50.0, 50.0),
    radius=28.0,
    style=stroke_style(DARK, width_units=w),
)

for node_xy in ((50.0, 82.0), (22.3, 34.0), (77.7, 34.0)):
    circle(
        node_xy,
        radius=7.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
    )

save()
