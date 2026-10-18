# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: tailscale."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import DARK, fill_style, setup_icon

setup_icon()

w = 2.0
r_dot = 10.23
xs = (19.50, 50.18, 80.49)
ys = (80.78, 50.29, 19.23)

active_dots = {
    (19.50, 50.29),
    (50.18, 50.29),
    (80.49, 50.29),
    (50.18, 19.23),
}

for yc in ys:
    for xc in xs:
        fill_col = Colors.Gray6 if (xc, yc) in active_dots else Colors.Gray3
        circle(
            (xc, yc),
            radius=r_dot,
            style=fill_style(fill_col, border_color=DARK, border_units=w),
        )

save()
