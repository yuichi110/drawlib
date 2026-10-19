# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: keras."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 1. Rounded square badge ("#D84A52")
rectangle(
    (50.0, 50.0),
    width=79.0,
    height=79.0,
    style=Icon.fill_style("#D84A52", border_color=Icon.DARK, border_units=w, shape_r=11.0),
)

# 2. Bold geometric chamfered 'K' polygon (WHITE) outlined in DARK
k_pts = [
    (30.9, 27.3),
    (32.4, 25.8),
    (37.4, 25.8),
    (39.0, 27.3),
    (39.0, 42.7),
    (45.2, 48.7),
    (60.8, 25.8),
    (67.8, 25.8),
    (69.1, 28.4),
    (51.1, 54.6),
    (67.7, 71.6),
    (66.6, 74.2),
    (59.8, 74.2),
    (39.0, 53.5),
    (39.0, 72.6),
    (37.4, 74.2),
    (32.4, 74.2),
    (30.9, 72.6),
]

polygon(k_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(k_pts, width_units=1.8, color=Icon.DARK, closed=True)

save()
