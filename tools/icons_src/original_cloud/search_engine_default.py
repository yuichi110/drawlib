# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: search_engine."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Stack of 3 horizontal index bars (back/left)
bars = [
    (68.0, Icon.PASTEL_BLUE),
    (50.0, Icon.WHITE),
    (32.0, Icon.WHITE),
]
for yc, col in bars:
    rectangle(
        (42.0, yc),
        width=52.0,
        height=12.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w, shape_r=4.0),
    )

# 2. Magnifying glass handle (drawn before lens so joint is clean)
p_start = (70.0, 34.0)
p_end = (84.0, 20.0)
Icon.draw_capsule(p_start, p_end, width_units=9.0, color=Icon.DARK)
Icon.draw_capsule(p_start, p_end, width_units=9.0 - 2.0 * w, color=Icon.PASTEL_GREEN)

# 3. Magnifying glass lens
lens_center = (60.0, 44.0)
circle(
    lens_center,
    radius=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    lens_center,
    radius=11.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

save()
