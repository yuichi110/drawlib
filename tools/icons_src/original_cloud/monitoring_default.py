# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: monitoring."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

rectangle(
    (50.0, 22.0),
    width=15.0,
    height=16.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
Icon.draw_round_segment((30.0, 14.0), (70.0, 14.0), width_units=w, color=Icon.DARK)

rectangle(
    (50.0, 56.0),
    width=76.0,
    height=52.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)

wave_pts = [
    (21.0, 54.0),
    (34.0, 54.0),
    (42.5, 73.0),
    (52.5, 39.0),
    (61.0, 62.0),
    (68.0, 54.0),
    (79.0, 54.0),
]
Icon.draw_round_polyline(wave_pts, width_units=w, color=Icon.DARK)
circle(
    (42.5, 73.0),
    radius=4.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
