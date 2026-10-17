# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smart_speaker."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Cylindrical speaker body (PASTEL_BLUE) with PASTEL_GREEN glowing voice ring rim on top
draw_cylinder_tier(
    50.0,
    24.0,
    width=48.0,
    body_h=46.0,
    ry=11.0,
    body_color=PASTEL_BLUE,
    top_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=w,
    draw_top_cap=True,
)

# Inner WHITE top touch surface inside the glowing PASTEL_GREEN voice ring
ellipse(
    (50.0, 70.0),
    width=31.0,
    height=13.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)
circle((50.0, 70.0), radius=1.8, style=fill_style(DARK))

# Front acoustic fabric mesh dots
for row_y, xs in (
    (49.0, (36.0, 45.3, 54.7, 64.0)),
    (39.0, (32.5, 41.2, 50.0, 58.8, 67.5)),
    (29.0, (36.0, 45.3, 54.7, 64.0)),
):
    for dx in xs:
        circle((dx, row_y), radius=1.5, style=fill_style(DARK))

save()
