# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: powerdns."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
r = 11.67

# 6 circles in 2 rows x 3 columns (Orange2 diagonal accents, Orange3 main nodes)
nodes = [
    (22.30, 63.35, Colors.Orange2),
    (50.00, 63.35, Colors.Orange3),
    (77.70, 63.35, Colors.Orange3),
    (22.30, 36.65, Colors.Orange3),
    (50.00, 36.65, Colors.Orange3),
    (77.70, 36.65, Colors.Orange2),
]

for cx, cy, col in nodes:
    circle(
        (cx, cy),
        radius=r,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w),
    )

save()
