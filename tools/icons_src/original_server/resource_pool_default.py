# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: resource_pool."""

from drawlib.canvas import save
from drawlib.shapes import circle, wedge
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Outer circular pool ring
circle(
    (50.0, 50.0),
    radius=38.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 3-slice pie/gauge chart representing CPU / Memory / IOPS allocation
slices = [
    (90.0, 220.0, PASTEL_BLUE),
    (220.0, 330.0, PASTEL_BLUE_LIGHT),
    (330.0, 90.0, PASTEL_GREEN),
]
for ang_start, ang_end, fill_col in slices:
    wedge(
        (50.0, 50.0),
        radius=30.0,
        angle_start=ang_start,
        angle_end=ang_end,
        style=fill_style(fill_col, border_color=DARK, border_units=2.2),
    )

# Crisp continuous outer perimeter stroke around the 3 slices
circle(
    (50.0, 50.0),
    radius=30.0,
    style=stroke_style(DARK, width_units=2.2),
)

# Central WHITE hub circle
circle(
    (50.0, 50.0),
    radius=9.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)

save()
