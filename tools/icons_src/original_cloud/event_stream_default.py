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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

for y in (70.0, 50.0, 30.0):
    Icon.draw_round_segment((14.0, y), (86.0, y), width_units=w, color=Icon.DARK)
    Icon.draw_round_polyline(
        [(79.0, y + 6.0), (86.0, y), (79.0, y - 6.0)],
        width_units=w,
        color=Icon.DARK,
    )

# Top stream (y=70.0)
circle(
    (36.0, 70.0),
    radius=7.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
circle(
    (62.0, 70.0),
    radius=6.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# Middle stream (y=50.0)
circle(
    (52.0, 50.0),
    radius=8.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)

# Bottom stream (y=30.0)
circle(
    (32.0, 30.0),
    radius=6.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
circle(
    (64.0, 30.0),
    radius=7.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)

save()
