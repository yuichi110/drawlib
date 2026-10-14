# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: event_stream."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

for y in (70.0, 50.0, 30.0):
    draw_round_segment((14.0, y), (86.0, y), width_units=w, color=DARK)
    draw_round_polyline(
        [(79.0, y + 6.0), (86.0, y), (79.0, y - 6.0)],
        width_units=w,
        color=DARK,
    )

# Top stream (y=70.0)
circle(
    (36.0, 70.0),
    radius=7.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (62.0, 70.0),
    radius=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.4),
)

# Middle stream (y=50.0)
circle(
    (52.0, 50.0),
    radius=8.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

# Bottom stream (y=30.0)
circle(
    (32.0, 30.0),
    radius=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.4),
)
circle(
    (64.0, 30.0),
    radius=7.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

save()
