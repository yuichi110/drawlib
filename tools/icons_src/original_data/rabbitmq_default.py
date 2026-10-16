# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: rabbitmq."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = 1.9

# 5x5 modular grid mapped to [12.0, 88.0] x [12.0, 88.0] (1 block = 15.2 units)
x0, x1, x2, x3, x4, x5 = 12.0, 27.2, 42.4, 57.6, 72.8, 88.0
y0, y1, y2, y3, y5 = 12.0, 27.2, 42.4, 57.6, 88.0

# 1. Main geometric rabbit block silhouette (Colors.Orange3)
rabbit_pts = [
    (x0, y0),
    (x5, y0),
    (x5, y3),
    (x3, y3),
    (x3, y5),
    (x2, y5),
    (x2, y3),
    (x1, y3),
    (x1, y5),
    (x0, y5),
]
polygon(
    rabbit_pts,
    style=fill_style(Colors.Orange3, border_color=DARK, border_units=w, shape_r=3.6),
)

# 2. Inner pastel ear accents (Colors.Orange2) inside both upright ears
for ear_cx in ((x0 + x1) / 2.0, (x2 + x3) / 2.0):
    rectangle(
        (ear_cx, 72.5),
        width=6.8,
        height=18.5,
        style=fill_style(Colors.Orange2, border_color=DARK, border_units=1.5, shape_r=3.0),
    )

# 3. Rounded-square eye cutout in lower-right head area (WHITE + Colors.Orange3 pupil ring)
eye_cx = (x3 + x4) / 2.0
eye_cy = (y1 + y2) / 2.0
rectangle(
    (eye_cx, eye_cy),
    width=16.0,
    height=16.0,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=4.2),
)
rectangle(
    (eye_cx, eye_cy),
    width=7.2,
    height=7.2,
    style=fill_style(Colors.Orange3, border_color=DARK, border_units=1.5, shape_r=2.0),
)

save()
