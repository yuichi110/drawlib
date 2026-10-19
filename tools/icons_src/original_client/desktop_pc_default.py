# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: desktop_pc."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Monitor stand neck and base
rectangle(
    (36.0, 26.0),
    width=10.0,
    height=14.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w),
)
rectangle(
    (36.0, 19.0),
    width=26.0,
    height=6.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=2.5),
)

# Monitor bezel and WHITE screen
rectangle(
    (36.0, 53.0),
    width=46.0,
    height=38.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=5.0),
)
rectangle(
    (36.0, 53.5),
    width=37.0,
    height=28.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)

# Desktop tower chassis on the right
rectangle(
    (75.5, 48.0),
    width=23.0,
    height=64.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=4.5),
)

# Tower drive bay, vent lines, and PASTEL_GREEN power LED
rectangle(
    (75.5, 69.0),
    width=14.0,
    height=6.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=1.5),
)
for vy in (57.0, 51.0):
    Icon.draw_round_segment((70.0, vy), (81.0, vy), width_units=2.0, color=Icon.DARK)

circle(
    (75.5, 29.0),
    radius=4.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
