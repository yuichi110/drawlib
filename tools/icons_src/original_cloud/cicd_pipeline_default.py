# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: cicd_pipeline."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

circle((50.0, 50.0), radius=30.0, style=stroke_style(DARK, width_units=w))

circle(
    (50.0, 80.0),
    radius=11.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (24.0, 35.0),
    radius=11.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)
circle(
    (76.0, 35.0),
    radius=11.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

polygon(
    [(45.0, 58.0), (45.0, 42.0), (59.0, 50.0)],
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.2, shape_r=1.5),
)

save()
