# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: laptop."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Open clamshell screen lid
rectangle(
    (50.0, 55.5),
    width=62.0,
    height=43.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=5.0),
)

# Inner WHITE screen
rectangle(
    (50.0, 55.0),
    width=52.0,
    height=32.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)

# Webcam dot
circle((50.0, 74.0), radius=1.2, style=Icon.fill_style(Icon.DARK))

# PASTEL_GREEN screen bar and UI lines
rectangle(
    (50.0, 63.0),
    width=42.0,
    height=7.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
)
Icon.draw_round_segment((30.0, 52.0), (58.0, 52.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_segment((30.0, 45.5), (48.0, 45.5), width_units=2.0, color=Icon.DARK)

# Lower keyboard base deck and thumb notch
rectangle(
    (50.0, 30.0),
    width=76.0,
    height=9.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=4.0),
)
rectangle(
    (50.0, 32.5),
    width=16.0,
    height=4.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8, shape_r=1.5),
)

save()
