# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: kiosk_terminal."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
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

# Floor pedestal column and base plate
rectangle(
    (50.0, 31.0),
    width=18.0,
    height=28.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
rectangle(
    (50.0, 15.5),
    width=46.0,
    height=6.5,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=3.0),
)

# Upper touch kiosk bezel and WHITE screen
rectangle(
    (50.0, 64.5),
    width=46.0,
    height=43.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.5),
)
rectangle(
    (50.0, 64.5),
    width=36.0,
    height=33.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=3.0),
)

# Screen text lines and PASTEL_GREEN action button
draw_round_segment((38.0, 74.0), (62.0, 74.0), width_units=2.0, color=DARK)
draw_round_segment((38.0, 68.0), (56.0, 68.0), width_units=2.0, color=DARK)
rectangle(
    (50.0, 56.5),
    width=24.0,
    height=9.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=3.0),
)

save()
