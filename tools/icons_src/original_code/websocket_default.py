# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: websocket."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0

# 1. Central horizontal PASTEL_BLUE pipe body (width=52, height=28 at (50, 50))
rectangle(
    (50.0, 50.0),
    width=52.0,
    height=28.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_shape),
)

# 2. Left and right PASTEL_BLUE_LIGHT pipe flanges
for x_flange in (20.0, 80.0):
    rectangle(
        (x_flange, 50.0),
        width=8.0,
        height=38.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_shape, shape_r=3.0),
    )

# 3. Top rightward PASTEL_GREEN arrow shooting left-to-right through open channel
Icon.draw_chunky_arrow(
    y_center=56.0,
    x_tail=10.5,
    x_tip=89.5,
    x_head_base=79.5,
    shaft_half_h=2.5,
    head_half_h=5.2,
    fill_color=Icon.PASTEL_GREEN,
    border_units=w_shape,
    border_color=Icon.DARK,
)

# 4. Bottom leftward WHITE arrow shooting right-to-left through open channel
Icon.draw_chunky_arrow(
    y_center=44.0,
    x_tail=89.5,
    x_tip=10.5,
    x_head_base=20.5,
    shaft_half_h=2.5,
    head_half_h=5.2,
    fill_color=Icon.WHITE,
    border_units=w_shape,
    border_color=Icon.DARK,
)

save()
