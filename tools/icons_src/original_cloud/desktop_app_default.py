# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: desktop_app."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Monitor stand neck and base
rectangle(
    (50.0, 22.0),
    width=15.0,
    height=16.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
draw_round_segment((30.0, 14.0), (70.0, 14.0), width_units=w, color=DARK)

# Monitor frame
rectangle(
    (50.0, 56.0),
    width=76.0,
    height=52.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Left sidebar and right widget layout
rectangle(
    (28.0, 56.0),
    width=16.0,
    height=36.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.2, shape_r=3.0),
)
rectangle(
    (60.0, 62.0),
    width=34.0,
    height=22.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=3.0),
)
draw_round_segment((44.0, 42.0), (76.0, 42.0), width_units=2.4, color=DARK)

save()
