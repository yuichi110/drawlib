# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud vendor icon: ovhcloud."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_compound_polygon, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0

c1 = [[(85.72, 71.94), (76.98, 56.49), (67.81, 56.49), (57.01, 37.46), (66.19, 37.46), (59.28, 25.25), (81.84, 25.25), (83.36, 27.28), (84.74, 29.38), (85.99, 31.55), (87.1, 33.78), (88.08, 36.05), (88.91, 38.38), (89.61, 40.74), (90.17, 43.13), (90.59, 45.55), (90.86, 47.99), (91.0, 50.44), (90.99, 52.89), (90.84, 55.34), (90.55, 57.79), (90.11, 60.22), (89.53, 62.64), (88.8, 65.02), (87.92, 67.37), (86.9, 69.68), (85.72, 71.94)], [(41.26, 25.25), (69.86, 74.75), (45.68, 74.75), (29.28, 46.22), (14.38, 72.05), (13.19, 69.79), (12.15, 67.48), (11.26, 65.12), (10.52, 62.73), (9.92, 60.32), (9.47, 57.88), (9.17, 55.42), (9.01, 52.96), (9.0, 50.5), (9.13, 48.04), (9.41, 45.6), (9.84, 43.17), (10.4, 40.77), (11.11, 38.4), (11.97, 36.07), (12.97, 33.79), (14.11, 31.56), (15.39, 29.38), (16.81, 27.28), (18.38, 25.25)]]
draw_compound_polygon(c1, color='#576CE0')
for ring in c1:
    draw_round_polyline(ring, width_units=w, color=DARK, closed=True)

save()
# fmt: on
