# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: campus."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Connecting ground plaza / courtyard lobby link (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 24.5),
    width=26.0,
    height=9.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.5),
)

# 2. Left taller modern campus building (PASTEL_BLUE)
# x=13..39, y=20..80
rectangle(
    (26.0, 50.0),
    width=26.0,
    height=60.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=3.0),
)
for wy in (68.0, 56.0, 44.0):
    for wx in (21.0, 31.0):
        rectangle(
            (wx, wy),
            width=6.2,
            height=6.2,
            style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.2),
        )

# 3. Right mid-rise modern campus building (WHITE + PASTEL_BLUE_LIGHT top band)
# x=61..87, y=20..66
rectangle(
    (74.0, 43.0),
    width=26.0,
    height=46.0,
    style=no_border_fill(WHITE, shape_r=3.0),
)
draw_rounded_corner_block(
    61.0,
    59.0,
    87.0,
    66.0,
    r=3.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE_LIGHT,
)
draw_round_segment((61.0, 59.0), (87.0, 59.0), width_units=w_inner, color=DARK)
rectangle(
    (74.0, 43.0),
    width=26.0,
    height=46.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w_outer, shape_r=3.0),
)
for wy in (50.0, 38.0):
    for wx in (69.0, 79.0):
        rectangle(
            (wx, wy),
            width=6.2,
            height=6.2,
            style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_inner, shape_r=1.2),
        )

# 4. Shared campus plaza terrace base (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 17.0),
    width=78.0,
    height=6.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.5),
)

# 5. PASTEL_GREEN tree centered cleanly in the courtyard gap (x=42.8..57.2)
draw_round_segment((50.0, 20.0), (50.0, 34.0), width_units=w_outer, color=DARK)
circle(
    (50.0, 40.5),
    radius=7.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer),
)
circle(
    (50.0, 48.0),
    radius=5.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer),
)
circle((50.0, 40.5), radius=6.2, style=no_border_fill(PASTEL_GREEN))

save()
