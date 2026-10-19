# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: rest_api."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Top rightward PASTEL_GREEN request arrow
Icon.draw_chunky_arrow(
    y_center=81.5,
    x_tail=24.0,
    x_tip=76.0,
    x_head_base=65.0,
    shaft_half_h=3.2,
    head_half_h=6.5,
    fill_color=Icon.PASTEL_GREEN,
    border_units=w_shape,
    border_color=Icon.DARK,
)

# 2. Bottom leftward PASTEL_BLUE_LIGHT response arrow
Icon.draw_chunky_arrow(
    y_center=18.5,
    x_tail=76.0,
    x_tip=24.0,
    x_head_base=35.0,
    shaft_half_h=3.2,
    head_half_h=6.5,
    fill_color=Icon.PASTEL_BLUE_LIGHT,
    border_units=w_shape,
    border_color=Icon.DARK,
)

# 3. Central WHITE rounded API card (width=54, height=44, shape_r=5.0 at (50, 50))
rectangle(
    (50.0, 50.0),
    width=54.0,
    height=44.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape, shape_r=5.0),
)

# 4. Inner PASTEL_BLUE rounded badge panel and bold `{` `}` curly braces in w_line=2.7 DARK
rectangle(
    (50.0, 50.0),
    width=42.0,
    height=32.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_shape, shape_r=3.5),
)

# Left `{` curly brace
left_brace = [
    (43.5, 60.0),
    (39.5, 60.0),
    (39.5, 53.0),
    (35.5, 50.0),
    (39.5, 47.0),
    (39.5, 40.0),
    (43.5, 40.0),
]
Icon.draw_round_polyline(left_brace, width_units=w_line, color=Icon.DARK, corner_r=2.0)

# Right `}` curly brace
right_brace = [
    (56.5, 60.0),
    (60.5, 60.0),
    (60.5, 53.0),
    (64.5, 50.0),
    (60.5, 47.0),
    (60.5, 40.0),
    (56.5, 40.0),
]
Icon.draw_round_polyline(right_brace, width_units=w_line, color=Icon.DARK, corner_r=2.0)

# Central WHITE colon/dot mark between `{` and `}`
circle((50.0, 53.5), radius=1.5, style=Icon.fill_style(Icon.DARK))
circle((50.0, 46.5), radius=1.5, style=Icon.fill_style(Icon.DARK))

save()
