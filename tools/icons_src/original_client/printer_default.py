# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: printer."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Top input paper tray sheet
rectangle(
    (50.0, 73.5),
    width=40.0,
    height=23.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=2.5),
)

# Main office printer chassis
rectangle(
    (50.0, 48.0),
    width=70.0,
    height=34.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Output recess slot and PASTEL_GREEN status LED
rectangle(
    (50.0, 36.0),
    width=48.0,
    height=11.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=2.0),
)
circle(
    (74.0, 54.5),
    radius=4.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# Bottom output paper sheet with printed lines
rectangle(
    (50.0, 26.5),
    width=40.0,
    height=23.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=2.5),
)
draw_round_segment((37.5, 29.0), (62.5, 29.0), width_units=2.0, color=DARK)
draw_round_segment((37.5, 22.5), (56.0, 22.5), width_units=2.0, color=DARK)

save()
