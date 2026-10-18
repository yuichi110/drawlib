# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud vendor icon: kagoya."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_compound_polygon, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0

c1 = [[(91.0, 29.46), (91.0, 29.18), (84.98, 28.82), (85.45, 23.91), (85.07, 23.91), (84.53, 29.36), (76.78, 31.24), (77.16, 23.9), (60.18, 23.9), (59.73, 62.33), (55.69, 64.98), (41.73, 59.89), (41.73, 56.29), (55.69, 60.99), (55.69, 23.89), (9.0, 23.89), (14.09, 55.99), (55.69, 76.11), (81.98, 54.81), (84.47, 31.79)], [(56.16, 60.95), (56.16, 23.89), (57.73, 23.89), (57.51, 60.18)]]
draw_compound_polygon(c1, color='#4D82D4')
for ring in c1:
    draw_round_polyline(ring, width_units=w, color=DARK, closed=True)

save()
# fmt: on
