# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: columnar_db."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=76.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)
cols = [
    (27.0, Icon.PASTEL_BLUE),
    (50.0, Icon.PASTEL_GREEN),
    (73.0, Icon.PASTEL_BLUE_LIGHT),
]
for xc, col in cols:
    rectangle(
        (xc, 50.0),
        width=18.0,
        height=60.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w, shape_r=3.5),
    )
    for yc in (64.0, 50.0, 36.0):
        Icon.draw_round_segment((xc - 6.0, yc), (xc + 6.0, yc), width_units=w, color=Icon.DARK)
save()
