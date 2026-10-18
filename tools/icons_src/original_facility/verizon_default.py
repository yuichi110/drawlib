# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: verizon."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0
v_pts = [(16.45, 50.0), (35.46, 9.0), (45.53, 9.0), (83.55, 91.0), (71.06, 91.0), (40.5, 24.84), (28.94, 50.0)]

polygon(v_pts, style=no_border_fill("#F25353"))
draw_round_polyline(v_pts, width_units=w, color=DARK, closed=True)

save()
# fmt: on
