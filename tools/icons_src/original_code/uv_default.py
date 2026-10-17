# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: uv."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 1.9

uv_block = [(10.0, 89.64), (10.16, 49.81), (10.3, 17.94), (10.34, 17.29), (10.42, 16.65), (10.54, 16.04), (10.71, 15.43), (10.94, 14.86), (11.22, 14.3), (11.51, 13.77), (11.85, 13.25), (12.25, 12.77), (12.67, 12.33), (13.1, 11.91), (13.58, 11.53), (14.11, 11.19), (14.64, 10.9), (15.2, 10.63), (15.78, 10.42), (16.39, 10.23), (17.01, 10.12), (17.65, 10.04), (18.3, 10.02), (50.17, 10.16), (70.09, 10.23), (72.12, 10.23), (72.75, 10.28), (73.4, 10.36), (74.01, 10.48), (74.62, 10.65), (75.2, 10.9), (75.76, 11.15), (76.28, 11.47), (76.8, 11.81), (77.28, 12.21), (77.72, 12.62), (78.13, 13.08), (78.51, 13.56), (78.85, 14.08), (79.14, 14.62), (79.42, 15.18), (79.65, 15.78), (79.8, 16.37), (79.94, 17.0), (80.02, 17.63), (80.04, 18.28), (83.69, 18.28), (83.69, 10.32), (90.0, 10.32), (89.66, 89.98), (53.01, 89.82), (53.18, 58.08), (53.18, 38.2), (49.99, 38.2), (46.64, 38.2), (46.8, 58.06), (46.64, 89.8)]
# fmt: on

# 1. Flat pastel purple 'uv' block with center slot cutout and DARK border
polygon(uv_block, style=no_border_fill("#E28AF0"))
draw_round_polyline(uv_block, width_units=w_outer, color=DARK, closed=True)

save()
