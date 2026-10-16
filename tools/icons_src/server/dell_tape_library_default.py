# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_tape_library_default."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DELL_BLUE,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

# Circular media/tape reel arc (cx=51.0, cy=49.0, r=35.0) counter-clockwise from 180 deg to top-left
cx, cy = 51.0, 49.0
r_reel = 35.0
st_stroke = stroke_style(DELL_BLUE, width_units=4.8)

arc(
    (cx, cy),
    width=r_reel * 2.0,
    height=r_reel * 2.0,
    angle_start=180.0,
    angle_end=154.6,
    style=st_stroke,
)

# L-shaped recovery arrowhead at top-left (vertical leg at x=16.0 aligned with 180-deg reel start, flat butt ends)
polygon(
    [
        (13.6, 84.0),
        (13.6, 61.6),
        (35.0, 61.6),
        (35.0, 66.4),
        (18.4, 66.4),
        (18.4, 84.0),
    ],
    style=fill_style(DELL_BLUE, shape_r=(0.0, 2.5, 0.0, 0.0, 0.0, 0.0)),
)

# Center tape hub ring at (51.0, 49.0) (outer r=11.0 -> centerline r=8.6, border=4.8)
circle(
    (cx, cy),
    radius=8.6,
    style=fill_style(Colors.Transparent, border_color=DELL_BLUE, border_units=4.8),
)

save()
